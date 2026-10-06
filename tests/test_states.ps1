$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../runtime/state.ps1')
$fixture=Get-Content (Join-Path $PSScriptRoot 'fixtures/delivery-states.json') -Raw | ConvertFrom-Json
$count=0
foreach($case in $fixture.cases) {
    $baseline=$fixture.baseline | ConvertTo-Json -Depth 10 | ConvertFrom-Json
    if($case.baseline_assistants) { $baseline.assistants=$case.baseline_assistants }
    $users=@($case.users)
    if($case.new_user) {$users=@('old prompt',$fixture.message)}
    $observed=if($case.observed_at){$case.observed_at}else{'2026-01-01T00:00:01Z'}
    $ob=@{users=$users;assistants=$case.assistants;generating=$case.generating;observed_at=$observed}
    $got=Get-DeliveryObservation $baseline $ob $fixture.message $fixture.run_id ([datetimeoffset]'2026-01-01T00:00:00Z')
    if($got.submitted -ne $case.submitted -or [bool]$got.reply -ne $case.reply) {throw ('Fixture failed: '+$case.name)}
    if($case.name -eq 'reply_visible' -and $got.complete) {throw 'Generating reply incorrectly marked complete'}
    $count++
}
$text="- 0: Chat (https://worker.example/thread/a)`n- 1: Chat (https://worker.example/thread/b)"
if((Get-ExactTabIndex $text 'https://worker.example/thread/b') -ne 1) {throw 'Exact tab mismatch'}
if((Get-ExactTabIndex $text 'https://worker.example/thread') -ne -1) {throw 'Prefix matched incorrectly'}
try {Get-ExactTabIndex ($text+"`n- 2: Other (https://worker.example/thread/a)") 'https://worker.example/thread/a';throw 'Expected ambiguity'} catch {if($_.Exception.Message -ne 'TAB_AMBIGUOUS'){throw}}
Write-Output "PASS: $count delivery fixtures and 3 tab matching checks"
