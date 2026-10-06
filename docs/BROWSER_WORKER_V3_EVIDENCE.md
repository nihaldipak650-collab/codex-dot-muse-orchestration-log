# Browser Worker V3 evidence

Version: 3.0.0. Status: local implementation verified; fresh independent repair review PASS. Full live workflow NOT_RUN.

Initial checkpoint: 27 Python tests passed. Final independent consolidated Python suite: **42 tests PASS** (standalone runtime 15, persistent wrapper 8, full local workflow 16, generated JavaScript snippets 3). PowerShell delivery fixtures 7 and tab matching checks 3 passed; skill metadata validator and Python compile checks passed. These are synthetic/local tests, not DOT/Muse live receipts.

Coverage: DOT bundle bytes -> manifest/file SHA verification -> unpack/read -> duplicate rows/bundle -> same-thread continuation; Muse correlated inline fallback -> local read -> continuation; B06/no replay; stale/wrong-thread/replayed observations; generation resets reply stability; malformed raw and partial rows; hash mismatch and ZIP traversal rejection. Download event snippets exist but are not established as provider-live compatible by local tests.

Live regression plan: BROWSER_WORKER_V3_DESIGN.md. Keep private URLs, prompts, raw browser outputs and result bytes only in ignored local storage. Public evidence records sanitized statuses and counts.

## Independent review and repairs

First review FAIL identified stranded pending state when switching transport and stale original-run artifact receipts after standalone collect. Repairs set transport ownership and map original logical runs to their actual successful collection receipts, preserving original records.

Fresh repair review found Windows LF/CRLF raw preservation, corrupt compressed ZIP failure receipts and missing registered receipt thread validation. All were repaired and independently checked; review PASS at aff619b with all 42 Python tests independently rerun. Added tests reject modified inline bytes, cross-worker receipts, ambiguous Windows ZIP names and invalid encodings without upgrading artifact validity. Manifest must contain summary and result files, with exact member hashes. Validated index accepts no partial results.

## Live preflight on 2026-10-06

Preferred registered Playwright browser_tabs(action=list) was invoked. It produced no response within the bounded control attempt and the waiting invocation was terminated. No worker prompt was submitted. This establishes only CONTROL_UNCONFIRMED; it does not establish application downtime, endpoint root cause, extension disconnection or provider incompatibility.

Full regression was designed after the first local implementation/test round and is ready to execute once registered browser control returns and provider selectors can be inspected. DOT live bundle download, Muse live fallback, same-thread live continuation and server-to-coordinator file visibility remain unverified. No ACK smoke or full-workflow PASS is claimed.

## Remaining boundaries

Registered snippets need validated actual UI selectors and shared filesystem access for saveAs/local ingest. There is no automatic remote-file transfer service; use inline fallback if local bytes cannot be acquired. No autonomous wake/scheduler or semantic entity dedupe is implemented. Context capsules are coordinator-reviewed inputs, not automatically verified knowledge. Exact row dedupe and package validation do not prove worker factual claims.
