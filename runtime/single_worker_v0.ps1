param(
    [Alias('-endpoint')][string]$Endpoint='http://localhost:8931/mcp',
    [Alias('worker-url','-worker-url')][string]$WorkerUrl,
    [Alias('-message')][string]$Message,
    [Alias('-timeout')][ValidateRange(1,3600)][int]$Timeout=120,
    [string]$RunId=('RUNTIME-V0-'+[datetime]::UtcNow.ToString('yyyyMMddTHHmmssfff')),
    [string]$Config,
    [string]$OutputDirectory,
    [switch]$Inspect,
    [switch]$Collect,
    [string]$ContextFile
)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'state.ps1')
$root=Split-Path $PSScriptRoot -Parent
if(-not $OutputDirectory) { $OutputDirectory=Join-Path $root 'runs' }
if($RunId -notmatch '^[A-Za-z0-9_-]{1,100}$') { throw 'RunId must be a safe filename identifier.' }
[void][IO.Directory]::CreateDirectory($OutputDirectory)
$output=Join-Path $OutputDirectory ($RunId+'.json')
# Atomic claim prevents repeat sends for the same ID; lock survives uncertain/crashed delivery.
$claim=Join-Path $OutputDirectory ($RunId+'.lock')
if(Test-Path -LiteralPath $output) { throw 'RUN_ID_EXISTS: choose a new ID; existing result preserved.' }
$lock=[IO.File]::Open($claim,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
$lock.Dispose()
$result=[ordered]@{schema_version='1.0';run_id=$RunId;started_at=[datetimeoffset]::UtcNow.ToString('o');finished_at=$null;worker_identifier_safe=$null;endpoint=$null;preflight_status='CONTROL_DOWN';tab_status='TAB_NOT_FOUND';message_sha256=$null;filled=$false;submitted=$false;visible_as_user_message=$false;submit_confirmed=$false;reply_received=$false;reply_text=$null;timestamps=@{};errors=@();final_status='CONTROL_DOWN'}
$scratch=Join-Path ([IO.Path]::GetTempPath()) ('worker-v0-'+[guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($scratch)
$stage='INVALID_CONFIG'
$exitCode=1
try {
    $cfg=@{composer='[role="textbox"],textarea';users='[data-message-author-role="user"]';assistants='[data-message-author-role="assistant"]';generating='[data-testid="stop-button"]';completion='';poll_seconds=2}
    if($Config) {
        $loaded=Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
        foreach($p in $loaded.PSObject.Properties) {
            if($cfg.ContainsKey($p.Name)) { $cfg[$p.Name]=$p.Value }
        }
        if(-not $PSBoundParameters.ContainsKey('WorkerUrl')) { $WorkerUrl=[string]$loaded.worker_url }
        if(-not $PSBoundParameters.ContainsKey('Endpoint') -and $loaded.endpoint) { $Endpoint=[string]$loaded.endpoint }
        if(-not $PSBoundParameters.ContainsKey('Message')) { $Message=[string]$loaded.message }
    }
    $worker=[uri]$WorkerUrl; $ep=[uri]$Endpoint
    if($worker.Scheme -notin @('http','https') -or -not $worker.Host -or $ep.Scheme -notin @('http','https') -or -not $ep.Host) { throw 'INVALID_CONFIG' }
    if($ep.UserInfo -or $ep.Query -or $ep.Fragment) { throw 'INVALID_ENDPOINT: credentials/query/fragment not supported.' }
    $result.worker_identifier_safe=@{hostname=$worker.Host;url_sha256=(Get-TextHash $WorkerUrl)}
    $result.endpoint=$ep.GetLeftPart([UriPartial]::Authority) # Do not persist path/query connection material.
    $correlationRunId=$RunId
    if($Collect) {
        if(-not $ContextFile){throw 'INVALID_COLLECT_CONTEXT'}
        $context=Get-Content -LiteralPath $ContextFile -Raw | ConvertFrom-Json
        if($context.worker_url_hash -cne (Get-TextHash $WorkerUrl) -or -not $context.sent_at){throw 'INVALID_COLLECT_BINDING'}
        $correlationRunId=[string]$context.run_id
    }
    if(-not $Inspect -and -not $Collect -and (-not $Message -or -not $Message.Contains($RunId))) { throw 'MESSAGE_REQUIRES_RUN_ID' }
    $result.message_sha256=Get-TextHash $Message
    if($Collect){$result.message_sha256=[string]$context.message_hash}
    $stage='CONTROL_DOWN'
    function Invoke-Mcp([string]$Method,$Params,[int]$Limit=10) {
        $req=Join-Path $scratch 'request.json'
        @{jsonrpc='2.0';id=2;method=$Method;params=$Params} | ConvertTo-Json -Depth 30 -Compress | Set-Content -LiteralPath $req -Encoding utf8
        $raw=(& (Join-Path $root 'tools/playwright_mcp_rpc.ps1') -RequestFile $req -SessionFile (Join-Path $scratch 'private-session.json') -Endpoint $Endpoint -TimeoutSeconds $Limit) -join "`n"
        $data=@($raw -split '\r?\n' | Where-Object {$_ -like 'data:*'})
        if($data.Count) { $raw=($data | ForEach-Object {$_.Substring(5).TrimStart()}) -join "`n" }
        $rpc=$raw | ConvertFrom-Json
        if($rpc.id -ne 2 -or ('result' -notin @($rpc.PSObject.Properties.Name) -and 'error' -notin @($rpc.PSObject.Properties.Name))) {throw 'MCP_RESPONSE_UNCORRELATED'}
        if($rpc.error -or $rpc.result.isError) {
            $text=$raw
            if($text -match '(?i)welcome|allow access|approval required|permission required') { throw 'HUMAN_APPROVAL_REQUIRED' }
            throw 'TOOL_ERROR'
        }
        return $rpc.result
    }
    function Invoke-Tool([string]$Name,$Arguments,[int]$Limit=10) {
        $toolResult=Invoke-Mcp 'tools/call' @{name=$Name;arguments=$Arguments} $Limit
        return (@($toolResult.content | Where-Object {$_.type -eq 'text'} | ForEach-Object {$_.text}) -join "`n")
    }
    $catalog=Invoke-Mcp 'tools/list' @{}
    $typeTool=@($catalog.tools | Where-Object {$_.name -eq 'browser_type'})
    if($typeTool.Count -ne 1) {throw 'UNSUPPORTED_BROWSER_TYPE'}
    $typeProperties=@($typeTool[0].inputSchema.properties.PSObject.Properties.Name)
    $useRef='ref' -in $typeProperties
    if(-not $useRef -and 'target' -notin $typeProperties) {throw 'UNSUPPORTED_BROWSER_TYPE'}
    $tabTool=@($catalog.tools | Where-Object {$_.name -eq 'browser_tabs'})
    $tabSupportsUrl=$tabTool.Count -eq 1 -and 'url' -in @($tabTool[0].inputSchema.properties.PSObject.Properties.Name)
    $tabs=Invoke-Tool 'browser_tabs' @{action='list'}
    $result.preflight_status='CONTROL_READY';$result.timestamps.control_ready=[datetimeoffset]::UtcNow.ToString('o')
    $stage='TAB_NOT_FOUND'
    $index=Get-ExactTabIndex $tabs $WorkerUrl
    if($index -lt 0) {
        if($Collect -or $Inspect){throw 'TAB_NOT_FOUND'}
        if($tabSupportsUrl) { $null=Invoke-Tool 'browser_tabs' @{action='new';url=$WorkerUrl} }
        else {
            $null=Invoke-Tool 'browser_tabs' @{action='new'}
            $null=Invoke-Tool 'browser_navigate' @{url=$WorkerUrl}
        }
        $tabs=Invoke-Tool 'browser_tabs' @{action='list'}
        $index=Get-ExactTabIndex $tabs $WorkerUrl
        if($index -lt 0) { throw 'TAB_NOT_FOUND' }
        $result.tab_status='TAB_OPENED'
    } else { $result.tab_status='TAB_EXISTING' }
    $null=Invoke-Tool 'browser_tabs' @{action='select';index=$index}
    $settings=$cfg | ConvertTo-Json -Compress
    $urlJson=ConvertTo-Json -InputObject $WorkerUrl -Compress
    $observe="() => { const c=$settings; if(location.href.replace(/\/$/,'') !== $urlJson.replace(/\/$/,'')) throw new Error('WRONG_TAB'); const read=s=>Array.from(document.querySelectorAll(s)).map(n=>n.innerText||n.textContent||''); return {users:read(c.users),assistants:read(c.assistants),generating:!!document.querySelector(c.generating),completion: c.completion ? !!document.querySelector(c.completion) : false,observed_at:new Date().toISOString()}; }"
    function Observe([int]$Limit=10) {
        $text=Invoke-Tool 'browser_evaluate' @{function=$observe} $Limit
        if($text -notmatch '(?s)### Result\s*\r?\n(.*?)(?:\r?\n###|$)') { throw 'OBSERVATION_FORMAT_UNSUPPORTED' }
        return ($Matches[1].Trim() | ConvertFrom-Json)
    }
    $baseline=Observe
    $result.timestamps.baseline=[string]$baseline.observed_at
    if($Inspect) { $result.final_status='INSPECT_READY';$exitCode=0;return }
    $stage='DELIVERY_UNKNOWN'
    if($Collect) {
        $baseline=$context
        $sent=[datetimeoffset]$context.sent_at
        $result.filled=[bool]$context.filled
        $result.submitted=[bool]$context.submitted
    } else {
    if(-not $ContextFile){$ContextFile=Join-Path $OutputDirectory ($RunId+'.context.json')}
    $context=[ordered]@{run_id=$RunId;worker_url_hash=(Get-TextHash $WorkerUrl);message_hash=(Get-TextHash $Message.Trim());user_hashes=@($baseline.users | ForEach-Object {Get-TextHash ([string]$_)});assistant_hashes=@($baseline.assistants | ForEach-Object {Get-TextHash ([string]$_)});sent_at=$null;filled=$false;submitted=$false}
    function Save-Context { [IO.File]::WriteAllText($ContextFile,($context | ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false)) }
    Save-Context
    # Fill is distinct from submit. No transport recovery/replay on either operation.
    if($useRef) {
        $snapshot=Invoke-Tool 'browser_snapshot' @{}
        $refs=@([regex]::Matches($snapshot,'(?m)^.*\btextbox\b[^\r\n]*\[ref=([^\]]+)\]') | ForEach-Object {$_.Groups[1].Value})
        if($refs.Count -ne 1) {throw 'COMPOSER_AMBIGUOUS'}
        $null=Invoke-Tool 'browser_type' @{element='worker conversation composer';ref=$refs[0];text=$Message;submit=$false}
    } else {
        $null=Invoke-Tool 'browser_type' @{target=[string]$cfg.composer;text=$Message;submit=$false}
    }
    $result.filled=$true;$result.timestamps.filled=[datetimeoffset]::UtcNow.ToString('o')
    $context.filled=$true
    $sent=[datetimeoffset]::UtcNow;$result.timestamps.submit_attempt=$sent.ToString('o')
    $context.sent_at=$sent.ToString('o');Save-Context
    $null=Invoke-Tool 'browser_press_key' @{key='Enter'}
    $result.submitted=$true
    $context.submitted=$true;Save-Context
    }
    $deadline=[datetimeoffset]::UtcNow.AddSeconds($Timeout)
    $submitDeadline=[datetimeoffset]::UtcNow.AddSeconds([Math]::Min(20,$Timeout))
    $seenText='';$stable=0
    while([datetimeoffset]::UtcNow -lt $deadline) {
        $remaining=[Math]::Max(1,[int]($deadline-[datetimeoffset]::UtcNow).TotalSeconds)
        $observation=Observe $remaining
        $delivery=Get-DeliveryObservation $baseline $observation $Message $correlationRunId $sent
        if($delivery.submitted) {
            if(-not $result.submit_confirmed) {$result.timestamps.submit_confirmed=[string]$observation.observed_at}
            # A later actual user-message receipt can reconcile an uncertain Enter return.
            $result.submitted=$true;$result.visible_as_user_message=$true;$result.submit_confirmed=$true;$stage='REPLY_TIMEOUT'
        }
        if($delivery.reply) {
            # Preserve a correlated partial reply even when completion cannot be established.
            $result.reply_text=Protect-ReplyText $delivery.reply $WorkerUrl
            if($delivery.reply -ceq $seenText) { $stable++ } else { $stable=0;$seenText=$delivery.reply }
            # Exact ACK is self-delimiting; other replies require configured completion signal.
            $exactAck=$delivery.reply.Trim() -ceq ('ACK '+$correlationRunId)
            $structured=$false
            try {
                $clean=$delivery.reply.Trim() -replace '^```json\s*','' -replace '\s*```$',''
                $replyObject=$clean | ConvertFrom-Json
                $structured=$replyObject.run_id -ceq $correlationRunId -and $replyObject.state -cin @('CONTINUE','NEED_CONTEXT','BLOCKED','DONE')
            } catch { }
            if($delivery.complete -and ($exactAck -or $structured -or $observation.completion) -and $stable -ge 1) {
                $result.reply_text=Protect-ReplyText $delivery.reply $WorkerUrl;$result.reply_received=$true
                $result.timestamps.reply_received=[string]$observation.observed_at
                $result.final_status='SUCCESS';$exitCode=0;break
            }
        }
        if(-not $result.submit_confirmed -and [datetimeoffset]::UtcNow -ge $submitDeadline) {break}
        Start-Sleep -Milliseconds ([int]([Math]::Min(2,[Math]::Max(0.1,[double]$cfg.poll_seconds))*1000))
    }
    if(-not $result.reply_received) { $result.final_status=$stage }
} catch {
    $safeCode=if($_.Exception.Message -match 'HUMAN_APPROVAL_REQUIRED') {'HUMAN_APPROVAL_REQUIRED'} elseif($_.Exception.Message -match 'TAB_AMBIGUOUS') {'TAB_AMBIGUOUS'} elseif($_.Exception.Message -match '^INVALID_|MESSAGE_REQUIRES') {'INVALID_CONFIG'} else {$stage}
    $result.errors+=@{code=$safeCode;stage=$stage};$result.final_status=$safeCode
} finally {
    $result.finished_at=[datetimeoffset]::UtcNow.ToString('o')
    $json=$result | ConvertTo-Json -Depth 20
    try {
        [IO.File]::WriteAllText($output,$json+[Environment]::NewLine,[Text.UTF8Encoding]::new($false))
        Write-Output ([pscustomobject]$result | Select-Object run_id,preflight_status,tab_status,filled,submit_confirmed,reply_received,final_status | ConvertTo-Json -Compress)
    } finally {
        # Only a freshly-created temporary directory is removed, never user/browser files.
        if([IO.Path]::GetFullPath($scratch).StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()))) { Remove-Item -LiteralPath $scratch -Recurse -Force }
    }
}
exit $exitCode
