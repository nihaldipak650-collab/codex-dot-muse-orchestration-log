# Browser Worker V3 evidence

Version: 3.0.0. Status: local implementation verified; independent review and live preflight pending at initial implementation checkpoint.

Initial local verification: 27 Python tests passed (13 standalone runtime, 7 persistent wrapper, 7 full local workflow); PowerShell delivery fixtures 7 and tab matching checks 3 passed; skill metadata validator passed. These are synthetic/local tests, not DOT/Muse live receipts. Expanded tests and review outcomes will be recorded before final delivery.

Coverage: DOT bundle bytes -> manifest/file SHA verification -> unpack/read -> duplicate rows/bundle -> same-thread continuation; Muse correlated inline fallback -> local read -> continuation; B06/no replay; stale/wrong-thread/replayed observations; generation resets reply stability; malformed raw and partial rows; hash mismatch and ZIP traversal rejection. Download event snippets exist but are not established as provider-live compatible by local tests.

Live regression plan: BROWSER_WORKER_V3_DESIGN.md. Keep private URLs, prompts, raw browser outputs and result bytes only in ignored local storage. Public evidence records sanitized statuses and counts.
