function Get-TextHash([string]$Text) {
    $sha=[System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($Text)))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function Get-DeliveryObservation($Baseline,$Observation,[string]$Message,[string]$RunId,[datetimeoffset]$SentAt) {
    $baselineUsers=if($Baseline.user_hashes){@($Baseline.user_hashes)}else{@($Baseline.users | ForEach-Object { Get-TextHash ([string]$_) })}
    $baselineReplies=if($Baseline.assistant_hashes){@($Baseline.assistant_hashes)}else{@($Baseline.assistants | ForEach-Object { Get-TextHash ([string]$_) })}
    $newUsers=@($Observation.users | Where-Object { (Get-TextHash ([string]$_)) -notin $baselineUsers })
    $submitted=@($newUsers | Where-Object {
        if($Baseline.message_hash){(Get-TextHash (([string]$_).Trim())) -ceq $Baseline.message_hash}else{([string]$_).Trim() -ceq $Message.Trim()}
    }).Count -eq 1
    $newReplies=@($Observation.assistants | Where-Object {
        (Get-TextHash ([string]$_)) -notin $baselineReplies -and ([string]$_).Contains($RunId)
    })
    $fresh=[datetimeoffset]$Observation.observed_at -ge $SentAt
    $reply=$null
    if($submitted -and $fresh -and $newReplies.Count -eq 1) { $reply=[string]$newReplies[0] }
    return @{ submitted=$submitted; reply=$reply; complete=($null -ne $reply -and -not $Observation.generating) }
}
function Protect-ReplyText([string]$Text,[string]$WorkerUrl) {
    $safe=$Text.Replace($WorkerUrl,'[REDACTED_WORKER_URL]')
    $safe=[regex]::Replace($safe,'(?im)\b(authorization|cookie|token|session[_-]?(?:id|secret))\s*[:=]\s*[^\r\n]+','$1: [REDACTED]')
    $safe=[regex]::Replace($safe,'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{30,})\b','[REDACTED_CREDENTIAL]')
    return $safe
}
function Get-ExactTabIndex([string]$Text,[string]$WorkerUrl) {
    $matchesFound=@()
    foreach($line in ($Text -split '\r?\n')) {
        if($line -match '^\s*-?\s*(\d+):.*\((https?://[^\s]+)\)\s*$') {
            if($Matches[2].TrimEnd('/') -ceq $WorkerUrl.TrimEnd('/')) { $matchesFound += [int]$Matches[1] }
        }
    }
    if($matchesFound.Count -gt 1) { throw 'TAB_AMBIGUOUS' }
    if($matchesFound.Count -eq 1) { return $matchesFound[0] }
    return -1
}
