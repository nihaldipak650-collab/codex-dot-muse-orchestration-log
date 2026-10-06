# Single-worker communication runtime

**EXPERIMENTAL / UNVERIFIED LIVE LOOP — LIVE_SMOKE_NOT_YET_VERIFIED.** Local fake-MCP integration tests pass; the real endpoint initialized and listed tools, but browser tab discovery timed out. No live message or ACK receipt was confirmed.

## What it does

Connect to an existing Playwright MCP HTTP endpoint, list/select one exact worker URL (or open it when absent), establish conversation baseline, fill once, press Enter once, confirm a new user message, correlate a new RUN_ID-bearing assistant reply, and save one result JSON. No autonomous task selection, multi-worker scheduler or provider API proxy.

## Requirements

- PowerShell 7, tested locally with PowerShell 7.6.5. Windows PowerShell 5.1 compatibility is not verified.
- An existing Playwright MCP server exposing `browser_tabs`, `browser_type`, `browser_press_key` and `browser_evaluate` over HTTP, with an authenticated worker browser session.
- A provider-specific selector configuration identifying the composer, user messages, assistant messages and generation/completion signals. Example role selectors are a starting point, not verified DOT/Muse adapters.
- The runtime inspects `tools/list`: the existing selector-based `browser_type.target` interface is supported; a standard `browser_type.ref` interface uses a fresh snapshot with exactly one textbox. Multiple snapshot textboxes are rejected rather than guessed. Other tool interfaces are unsupported.
- Python 3.9+ only for the fake-MCP test harness; no browser, worker account or third-party Python dependency for those tests.

## Start Playwright MCP

Reuse your existing server if available; the runtime does not launch or replace it. The [official project](https://github.com/microsoft/playwright-mcp) documents standalone HTTP mode, for example:

```sh
npx @playwright/mcp@latest --port 8931
```

That upstream setup is an alternative for new users, not a guarantee it attaches to your already-authenticated browser. Follow upstream browser/session setup and log in locally. Confirm your server exposes the required tools. Record the server version you test; this sprint used the pre-existing endpoint and did not reinstall it.

## Example config and command

Copy [example.config.json](example.config.json) to `runtime/worker.local.json` (ignored by Git). Replace its placeholder URL locally and narrow the composer selector to exactly one element. For general research replies, configure a genuine completion selector; absent that, V0 accepts only an exact, self-delimiting `ACK <RUN_ID>` reply observed twice with no generating signal.

The CLI supports `-Endpoint`, `-WorkerUrl`, `-Message`, `-Timeout` and aliases `--endpoint`, `--worker-url`, `--message`, `--timeout`.

```powershell
$run = 'RUNTIME-V0-SMOKE-' + [datetime]::UtcNow.ToString('yyyyMMddTHHmmss')
$message = "RUN_ID=$run`n`nReply exactly:`nACK $run"
pwsh -NoProfile -File runtime/single_worker_v0.ps1 `
  -Config runtime/worker.local.json `
  -Endpoint http://localhost:8931/mcp `
  -RunId $run -Message $message -Timeout 120
```

`-WorkerUrl` can override config. `-Inspect` selects/opens the configured tab and reads baseline without filling or submitting. All runs require an explicit URL via command or local config. `-OutputDirectory` can place private results outside the checkout.

## Expected result and states

`runs/<RUN_ID>.json` follows [the schema](../schemas/runtime-result.schema.json); [this result example](../examples/runtime-result.example.json) is explicitly synthetic, not a live receipt. Runs and reservation locks are ignored. The result contains a URL hostname/hash, endpoint origin, prompt hash, delivery booleans, reply text, timestamps, safe error codes and terminal status. The configured worker URL, credential-like lines and recognized credential patterns are redacted from saved replies. Prompt input, MCP session IDs and raw tool errors are not serialized. Temporary session/request files stay outside the checkout and are cleaned up. Other private reply content cannot be reliably identified: keep results local and inspect before sharing.

| State | Meaning |
|---|---|
| CONTROL_READY / CONTROL_DOWN | Tab-list tool responded / control could not be established. |
| TAB_EXISTING / TAB_OPENED / TAB_NOT_FOUND | Exact URL found / opened and then confirmed / unavailable. Multiple matches return TAB_AMBIGUOUS. |
| FILLED | `filled=true`; input operation succeeded, still not delivery. |
| SUBMITTED | `submitted=true`; Enter returned, still not a user-message receipt. |
| VISIBLE_AS_USER_MESSAGE / SUBMIT_CONFIRMED | New exact user-message text absent from baseline is observed. |
| DELIVERY_UNKNOWN | Submission cannot be confirmed; no automatic resend. |
| REPLY_RECEIVED / SUCCESS | New RUN_ID-bearing reply absent from baseline is observed after send and completion criterion met; result saved. |
| REPLY_TIMEOUT | Submission confirmed, no acceptable completed reply before deadline. |
| HUMAN_APPROVAL_REQUIRED | Tool explicitly requested approval; stop browser actions and continue local work. |

Exit 0 means SUCCESS or INSPECT_READY; other runtime outcomes exit 1 and save a result where storage is writable. Existing RUN_ID results/locks are never overwritten: choose a new ID after inspecting uncertain delivery. Manual lock removal is an explicit operator decision, not automatic retry.

## Local tests

```sh
pwsh -NoProfile -File tests/test_states.ps1
python tests/test_runtime.py
```

Tests cover B06 composer-only false delivery, old replies, pre-send observations, exact/ambiguous tabs, fake success, connection failure, delivery uncertainty, reply timeout, approval and run-ID protection. Fake integration exercises the actual transport and CLI, not a substitute implementation.

## Known limitations

The [Browser Worker Skill](../skills/browser-worker/SKILL.md) wraps this runtime. New `-Collect -ContextFile <local-context>` mode observes an earlier run without filling, submitting or opening a missing tab. Send context stores only hashes, binding, original RUN_ID and timestamp in ignored local storage. Collection gets a new result filename but correlates against the original turn; the same baseline/delivery logic is reused. Inspect also leaves missing tabs unopened.

Live loop remains unverified. Exact tab matching is intentionally strict; redirects/URL changes need adapter work. Message-text hashes are baseline identities, so identical repeated content is conservatively rejected. Generic role selectors and generation/completion selectors must be validated against the actual provider UI. The reply deadline starts after submission; individual MCP requests have bounded timeouts and preflight has separate transport limits. Shared-tab concurrent navigation can invalidate observations; the runtime checks URL before every observation. Disk failures cannot guarantee a result file and cause nonzero exit. No automatic resend, file-attachment capture, context truncation recovery or multi-worker scheduling is implemented.

The reused SSE reader consumes one data event. Servers emitting progress notifications before the response currently cause a conservative unconfirmed outcome; notifications are never accepted as action receipts.
