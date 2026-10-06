# Adapted from existing project pw_rpc.ps1 handshake; no credentials embedded.
param(
  [Parameter(Mandatory=$true)] [string]$RequestFile,
  [string]$SessionFile,
  [string]$Endpoint='http://localhost:8931/mcp',
  [int]$TimeoutSeconds=30,
  [switch]$AllowSessionRecovery
)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Net.Http
if (-not (Test-Path -LiteralPath $RequestFile)) { throw "Request file not found: $RequestFile" }
if (-not $SessionFile) {
  $SessionFile=Join-Path $env:LOCALAPPDATA 'Codex\pw_rpc-session.json'
}
$sessionParent=Split-Path -Parent $SessionFile
if ($sessionParent -and -not (Test-Path -LiteralPath $sessionParent)) { New-Item -ItemType Directory -Force -Path $sessionParent | Out-Null }

function New-Client {
  $client=[System.Net.Http.HttpClient]::new()
  $client.Timeout=[TimeSpan]::FromSeconds($TimeoutSeconds)
  return $client
}
function Send-Http([System.Net.Http.HttpClient]$Client,[string]$Json,[string]$SessionId,[string]$ProtocolVersion) {
  $requestClock=[Diagnostics.Stopwatch]::StartNew()
  $req=[System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Post,$Endpoint)
  [void]$req.Headers.Accept.ParseAdd('application/json')
  [void]$req.Headers.Accept.ParseAdd('text/event-stream')
  if ($SessionId) { [void]$req.Headers.TryAddWithoutValidation('mcp-session-id',$SessionId) }
  if ($ProtocolVersion) { [void]$req.Headers.TryAddWithoutValidation('MCP-Protocol-Version',$ProtocolVersion) }
  $req.Content=[System.Net.Http.StringContent]::new($Json,[System.Text.Encoding]::UTF8,'application/json')
  $res=$Client.SendAsync($req,[System.Net.Http.HttpCompletionOption]::ResponseHeadersRead).GetAwaiter().GetResult()
  $mediaType=''
  if ($res.Content.Headers.ContentType) { $mediaType=[string]$res.Content.Headers.ContentType.MediaType }
  if ($mediaType -eq 'text/event-stream') {
    $stream=$res.Content.ReadAsStreamAsync().GetAwaiter().GetResult()
    $reader=[System.IO.StreamReader]::new($stream)
    $eventLines=New-Object System.Collections.Generic.List[string]
    $hasData=$false
    while ($true) {
      $lineTask=$reader.ReadLineAsync()
      $remainingMs=[Math]::Max(1,($TimeoutSeconds*1000)-[int]$requestClock.ElapsedMilliseconds)
      if ($requestClock.Elapsed.TotalSeconds -ge $TimeoutSeconds -or -not $lineTask.Wait($remainingMs)) { throw "Timed out waiting for MCP SSE response after $TimeoutSeconds seconds (HTTP $([int]$res.StatusCode), $mediaType)." }
      $line=$lineTask.GetAwaiter().GetResult()
      if ($null -eq $line) { break }
      if ($line.Length -eq 0) {
        if ($hasData) { break }
        continue
      }
      $eventLines.Add($line)
      if ($line.StartsWith('data:')) { $hasData=$true }
    }
    $body=$eventLines -join "`n"
    $reader.Dispose()
  } else {
    $bodyTask=$res.Content.ReadAsStringAsync()
    $remainingMs=[Math]::Max(1,($TimeoutSeconds*1000)-[int]$requestClock.ElapsedMilliseconds)
    if(-not $bodyTask.Wait($remainingMs)) { throw 'Timed out reading MCP JSON response.' }
    $body=$bodyTask.GetAwaiter().GetResult()
  }
  $sid=$null
  $headerValues=$null
  if ($res.Headers.TryGetValues('Mcp-Session-Id',[ref]$headerValues)) { $sid=[string]($headerValues | Select-Object -First 1) }
  return [pscustomobject]@{StatusCode=[int]$res.StatusCode;IsSuccess=[bool]$res.IsSuccessStatusCode;Body=$body;SessionId=$sid;Headers=$res.Headers}
}
function Get-JsonPayload([string]$Body) {
  $payload=$Body
  $data=($Body -split "\r?\n" | Where-Object { $_ -like 'data: *' } | Select-Object -Last 1)
  if ($data) { $payload=$data.Substring(6) }
  try { return ($payload | ConvertFrom-Json) } catch { return $null }
}
function New-McpSession([System.Net.Http.HttpClient]$Client) {
  $versions=@('2025-03-26','2024-11-05','2025-06-18','2025-11-25')
  $lastError=''
  foreach ($version in $versions) {
    $init=[ordered]@{jsonrpc='2.0';id=1;method='initialize';params=[ordered]@{protocolVersion=$version;capabilities=@{};clientInfo=@{name='single-worker-v0';version='2.0'}}}
    $json=$init | ConvertTo-Json -Depth 20 -Compress
    try { $r=Send-Http $Client $json $null $null } catch { $lastError=$_.Exception.Message; continue }
    $parsed=Get-JsonPayload $r.Body
    if (-not $r.IsSuccess -or ($parsed -and $parsed.error)) {
      $lastError="HTTP $($r.StatusCode): $($r.Body)"
      if ($lastError -match '(?i)unsupported.*protocol|protocol.*unsupported|invalid.*protocol') { continue }
      throw "MCP initialize failed: $lastError"
    }
    $negotiated=$version
    if ($parsed -and $parsed.result -and $parsed.result.protocolVersion) { $negotiated=[string]$parsed.result.protocolVersion }
    $sid=$r.SessionId
    $notice=[ordered]@{jsonrpc='2.0';method='notifications/initialized'} | ConvertTo-Json -Compress
    $headerVersion=$negotiated
    if($negotiated -eq '2025-03-26'){$headerVersion=$null}
    $nr=Send-Http $Client $notice $sid $headerVersion
    if (-not $nr.IsSuccess) { $lastError="initialized notification failed HTTP $($nr.StatusCode): $($nr.Body)"; continue }
    $session=[ordered]@{endpoint=$Endpoint;sessionId=$sid;protocolVersion=$negotiated;initializedAt=(Get-Date).ToString('o');serverInfo=if($parsed.result.serverInfo){$parsed.result.serverInfo}else{$null}}
    $session | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $SessionFile -Encoding utf8
    return [pscustomobject]$session
  }
  throw "MCP initialize failed for all supported handshake versions: $lastError"
}
function Is-StaleSession([object]$Response) {
  if ($Response.Body -match '(?i)(session[^\r\n]*(expired|invalid|not found|unknown|closed|stale)|no valid session|invalid session id)') { return $true }
  if ($Response.StatusCode -eq 404 -and $Response.Body -match '(?i)session not found') { return $true }
  if ($Response.StatusCode -in @(400,401,410) -and $Response.Body -match '(?i)(missing|invalid|expired|unknown).{0,30}session|session.{0,30}(missing|invalid|expired|unknown)') { return $true }
  return $false
}

$client=New-Client
try {
  $requestText=Get-Content -LiteralPath $RequestFile -Raw
  $rpc=ConvertFrom-Json -InputObject $requestText
  $method=[string]$rpc.method
  if (-not $method) { throw 'Request has no JSON-RPC method.' }
  $session=$null
  if (Test-Path -LiteralPath $SessionFile) {
    try { $session=Get-Content -LiteralPath $SessionFile -Raw | ConvertFrom-Json } catch { $session=$null }
    if ($session.endpoint -ne $Endpoint -or -not $session.sessionId) { $session=$null }
  }
  if (-not $session) { $session=New-McpSession $client }
  $wireJson=$requestText.Trim()
  $headerVersion=[string]$session.protocolVersion
  if($headerVersion -eq '2025-03-26'){$headerVersion=$null}
  $retryForSession=$false
  try {
    $response=Send-Http $client $wireJson ([string]$session.sessionId) $headerVersion
    if (Is-StaleSession $response) { $retryForSession=$true }
  } catch {
    if ($_.Exception.Message -match '(?i)(timed out waiting for MCP SSE response|task was canceled|session.*(stale|expired|invalid))') { $retryForSession=$true }
    else { throw }
  }
  $retried=$false
  if ($retryForSession -and -not $AllowSessionRecovery) { throw 'MCP session recovery disabled for this request; delivery may be unknown.' }
  if ($retryForSession) {
    Remove-Item -LiteralPath $SessionFile -Force -ErrorAction SilentlyContinue
    $session=New-McpSession $client
    $headerVersion=[string]$session.protocolVersion
    if($headerVersion -eq '2025-03-26'){$headerVersion=$null}
    $response=Send-Http $client $wireJson ([string]$session.sessionId) $headerVersion
    $retried=$true
  }
  if (-not $response.IsSuccess) { throw "MCP HTTP $($response.StatusCode): $($response.Body)" }
  $payload=Get-JsonPayload $response.Body
  if ($payload -and $payload.error) {
    $errorText=$payload.error | ConvertTo-Json -Depth 12 -Compress
    if ($errorText -match '(?i)session') {
      if (-not $AllowSessionRecovery) { throw 'MCP session error; automatic resend disabled.' }
      if ($retried) { throw "MCP session retry returned an error: $errorText" }
      Remove-Item -LiteralPath $SessionFile -Force -ErrorAction SilentlyContinue
      $session=New-McpSession $client
      $headerVersion=[string]$session.protocolVersion
      if($headerVersion -eq '2025-03-26'){$headerVersion=$null}
      $response=Send-Http $client $wireJson ([string]$session.sessionId) $headerVersion
      $retried=$true
      if (-not $response.IsSuccess) { throw "MCP retry HTTP $($response.StatusCode): $($response.Body)" }
      $payload=Get-JsonPayload $response.Body
      if ($payload -and $payload.error) { throw "MCP retry error: $($payload.error | ConvertTo-Json -Depth 12 -Compress)" }
    } else { throw "MCP JSON-RPC error: $errorText" }
  }
  Write-Output $response.Body
} finally {
  $client.Dispose()
}
