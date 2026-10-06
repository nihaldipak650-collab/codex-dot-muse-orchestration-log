# Browser Worker 3.0.0 engineering contract

**Phase frozen; implementation remains f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a.** Local tests passed; V3 provider-live full workflow remains NOT_RUN. This retained design is not a command to resume development. [START_HERE](phase-closeout-20261006/START_HERE.md) is the current entrypoint.

Only explicit user restart authorizes the next short, bounded real journey: task → DOT/Muse → reply → primary artifact/bundle or structured inline → actual local read → Codex interpretation → same-thread targeted revision → final delivery. Measure human interventions, manual clicks, copy/paste, rescue events, actual artifact receipt/read and context continuity versus old manual Playwright coordination; duration is not acceptance. Both workers historically delivered ZIPs; inline is fallback for either, not a permanent Muse restriction. Historical ZIP formats differ from the V3 contract and are not proven compatible by local tests.

Goal: compose real persistent DOT/Muse conversations with trustworthy result acquisition, without narrowing the historical loop to ACK. Protect frozen tags, private thread URLs and existing experiment records. Do not replay uncertain sends. Commits/push explicitly authorized by the user.

Acceptance: existing transport/wrapper/B06 checks remain green; registered observations use durable same-thread baselines and bounded turns; complete structured replies and partial raw preservation work; DOT ZIP and Muse inline workflows reach local read with explicit integrity failures; cross-worker bundle/whole-row hash dedupe; stale or uncorrelated observations never establish success. Full live results are reported independently from local tests.

## Why the architecture changed

V0 coupled durable conversation control to a Python subprocess invoking custom HTTP/SSE. Historical registered Playwright operations were no longer a first-class path, and downloading/read/parse lived outside the wrapper. This narrowed functionality even though delivery checks improved.

V3 keeps both paths. Codex calls registered tools directly; the wrapper reserves a turn before exposing send text and accepts fresh actual observations through the shared workflow engine. Standalone PowerShell stays for reproducible transport tests and diagnostics. This avoids building another dynamic tool dispatcher and preserves the previously usable control surface. Observations supplied by Codex are trusted tool receipts, not an adversarially authenticated channel; local state does not certify their provenance.

Artifacts are immutable byte copies keyed by SHA-256 beneath each run, with separate receipts and a shared validated-row index. Read/parse/package validation does not claim semantic truth. Partial rows never poison the accepted index. Old run ingestion is allowed while a later worker turn runs, supporting refill before deep processing. Provider difference is delivery preference and private validated selectors, not duplicate state engines.

Context capsule is a small coordinator-reviewed handoff, not another chat transcript. Scheduling, lane assignment, semantic dedupe and synthesis remain coordinator responsibilities.

## Historical V3 candidate regression (retained design, not current restart plan)

The deterministic sequence below was designed during implementation and not run live. It remains a diagnostic asset; the current next target is the real user journey above, not automatic artificial challenges or ACK/one-hour plans.

Run budget: DOT 3 turns, Muse 3 turns; collection windows <=120s each, one read-only reconciliation attempt on stale controls. Do not spend a turn on ACK. Each lane uses its existing configured thread and validated UI selectors. Never reset pending state to restart a failed run.

1. Preflight registered tab list, exact thread selection, validated composer/message/generation signals and private local write/read. Generate fresh observation baselines. Record control failure separately from worker/model failure.
2. Send each worker a small deterministic data task: produce rows `alpha=2`, `beta=3`, duplicated `alpha=2`; report run_id/state and result rows. DOT additionally produces ZIP with manifest.json (run_id plus per-file SHA-256), results.json, summary.md. Muse supplies structured JSON inline even if attachments fail. No web research or fabricated external citations needed.
3. Confirm exact visible user message, two fresh stable completed replies, then quick triage. A suitable reply permits continuation before deep bundle processing: request `gamma=5` plus a repeated `beta=3` in the same thread, preserving prior task context. Record same binding, separate run IDs, attempted-send budget.
4. Discover only reply-scoped artifacts, capture actual download event/save outcome, then require coordinator-local bytes. If remote filesystem cannot transfer, report the exact missing step; use Muse inline fallback explicitly. Ingest earlier result while the next turn is busy. Verify manifest hashes, rows, duplicate counts; ingest identical bundle twice to prove dedupe without another network download.
5. Give one deliberate malformed inline row challenge (truncated final object), preserve raw bytes and complete partial objects, then request correction within remaining lane budget if necessary. It must remain READ/partial until a corrected bound result is received. Do not equate worker DONE with accepted malformed data.
6. Exercise read-only stale reconciliation using a copied old observation: reject it locally, obtain actual fresh browser evidence and collect without input. If send uncertainty occurs naturally, retain pending/no replay; do not intentionally create duplicate requests to manufacture a pass.
7. Synthesize only accepted rows across both lanes, recording exact-row duplicates and any semantic differences. PASS needs both providers, multi-turn same thread, artifact or explicit fallback, local read/hash/dedupe, preserved partial output, recovery and coordinator continuation. A control preflight failure yields NOT_RUN/BLOCKED, never full-workflow PASS.

## Limits

Selectors must be validated live against each provider. Download snippets run in the registered Playwright server process; local ingestion cannot bridge a server filesystem inaccessible to the coordinator. Inline fallback remains available. No autonomous scheduler, browser account management, semantic dedupe engine or guarantee of factual correctness is implemented. Registered completion accepts explicit structured state plus two stable no-generation observations; arbitrary natural replies require a validated completion signal.
