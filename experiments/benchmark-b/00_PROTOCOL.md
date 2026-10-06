# ORCHESTRATOR BENCHMARK V2 — Protocol

## Scope and safety
This is an isolated benchmark of the two-lane Dot/Muse coordinator loop. The formal workspace at D:\PROJECT_WHEELS_100_V2_20261004 is read-only. No formal candidates, reserves, quota, ledger, or state are changed. No scheduled automation is created. Use only the pre-existing Chrome Playwright Extension shared session through D:\PROJECT_WHEELS_100_V2_20261004\tools\pw_rpc.ps1. Do not use CDP, In-App Browser, substitute searches, or alternate worker channels. If the shared control plane is down, use RECOVER up to three times; never switch technologies or ask the user to reconnect during the timed run.

## Benchmark B
Four rounds, two independent worker lanes, up to five leads per lane per batch:
- R1 Literature assistant
- R2 Pixel/scientific animation
- R3 Management/simulation game
- R4 Research SOP/scientific workflow

DOT returns GitHub leads; Muse returns X/YouTube leads. Maximum 40 total candidate leads. Each prompt is an isolated benchmark request. Do not import benchmark leads into the formal V2 ledger. Use V1 only as a canonical duplicate reference. Keep the two lanes independent.

## Operating loop
Before timed work: preflight, at most five minutes. Confirm the exact Dot and Muse tabs, extension health, and Downloads readability. Only after successful preflight set BENCHMARK_START_TIME; the 90-minute wall-clock starts then.

For each lane:
SEND → POLL → FAST_TRIAGE (30–90 seconds) → immediately SEND next round to that same worker → FETCH_BUNDLE → DEEP_PROCESS → DEDUPE → ACCEPT/REJECT → CHECKPOINT → GAP → NEXT.
Refill first. As soon as one worker's result is visible, triage only enough to determine relevance, parseability, and obvious duplicates, then send that lane's next batch before processing full files. Do not wait for the other worker. While a lane is busy, fetch and process the previous bundle and update staging/metrics.

Each run has a unique RUN_ID:
- DOT: BENCHB-DOT-R1 through BENCHB-DOT-R4
- Muse: BENCHB-MUSE-R1 through BENCHB-MUSE-R4

Prompts ask for at most five leads and exactly one result bundle, preferably {RUN_ID}_RESULT.zip containing manifest.json, candidates.csv, summary.md, rejected.csv, next_gaps.json. If a zip cannot be provided, request one JSON result. The chat response must contain only:
RUN_ID=<id>
STATUS=COMPLETE
COUNT=<n>
BUNDLE=<filename or INLINE_JSON>
Do not ask the worker to attach several separate files.

## High-level control surface
All normal coordination uses tools/benchctl.ps1:
- SEND
- POLL
- FETCH_BUNDLE
- HEALTH
- RECOVER
- FAST_TRIAGE
- CHECKPOINT
Low-level browser tool calls are encapsulated by the helper and recorded under logs/rpc. Use raw low-level calls only to diagnose helper/control failures.

## Light review and staging
At candidate stage: accept as CANDIDATE_UNVERIFIED if source URL has a normal shape, topic is relevant, and the claimed reuse is understandable. Remove only obvious off-topic, unusable, malformed-link, or canonical duplicate leads. Record source and provenance, candidate status, and duplicate/drop reason. No license audit, release/commit audit, clone, execution, PoC, YouTube subtitle extraction, or independent replacement search. Do not mislabel searches as tests.

Canonical duplicates are compared against:
1. V1 PW-001–PW-100 ledger
2. already staged Benchmark B entries
3. the other row(s) in the same batch.
GitHub canonical key is host + normalized owner/repo; X is normalized post URL/status ID; YouTube is normalized video ID.

## State, events, and timing
Immediately append only:
- 02_BENCH_B_EVENTS.jsonl
- 03_BENCH_B_STAGING.csv
Each run records RUN_ID, WORKER, PROMPT_READY_TIME, SEND_TIME, WORKER_ACK_TIME, FIRST_RESULT_VISIBLE_TIME, FAST_TRIAGE_START, FAST_TRIAGE_END, NEXT_BATCH_SEND_TIME, BUNDLE_FETCH_START, BUNDLE_FETCH_END, DEEP_PROCESS_END. Also record status transitions and failures/recoveries.
Refill latency = NEXT_BATCH_SEND_TIME − FIRST_RESULT_VISIBLE_TIME.
State values are restricted to WORKER_BUSY, COORDINATOR_BUSY, IDLE_BUBBLE, CONTROL_DOWN, APP_DOWN, PAUSED.
Do not call a lane IDLE_BUBBLE if it has already received the next batch or if control/app is down. Classify CONTROL_DOWN for unavailable tabs/select/send/poll, extension no-tabs, or relay failure. Classify APP_DOWN if control works but the worker app/service fails. IDLE_BUBBLE only means worker returned, no next batch sent, and neither control nor app is down.

Write human-readable checkpoint/report updates every two rounds, not every action. The event stream and staging ledger are append-only. Preserve raw helper I/O in logs/rpc and downloaded bundles in artifacts/{RUN_ID}/.

## Refill-first and artifact handling
Worker response should be read from the exact thread. Send the next batch immediately after fast triage. Fetch one bundle after refill; try one primary download. If unavailable, record INLINE_FALLBACK and use the response body for light review. Do not repeatedly open previews. For downloads, use the existing Chrome Downloads folder C:\Users\LOCAL_USER\Downloads, then copy the bundle to artifacts/{RUN_ID}/ and extract/read locally. Browser operations are limited to SEND/POLL/DOWNLOAD and exact-thread identity checks.

## Recovery and stop rules
On CONTROL_DOWN: RECOVER, at most three attempts. Record downtime start, each attempt, recovery timestamp, downtime. If not recovered within ten minutes, end benchmark with CONTROL_FAILURE; no user-driven reconnect and no fallback technology.
Hard stops:
- 40 candidate leads reached
- 90 minutes since BENCHMARK_START_TIME
- CONTROL_DOWN exceeds ten minutes
- both workers are unrecoverable APP_DOWN
Do not dispatch more after a hard stop. Benchmark ends at the first hard stop.

## Metrics
Report WALL_CLOCK, TOTAL_CANDIDATES, candidates/hour, batch counts, mean/max refill latency per lane, total IDLE_BUBBLE, GUI action count, bundle downloads, CONTROL_DOWN count/duration, APP_DOWN count/duration, recovery success, human interventions, duplicates, off-topic/malformed drops.

## Deliverables
00_PROTOCOL.md
01_BASELINE_A.md
02_BENCH_B_EVENTS.jsonl
03_BENCH_B_STAGING.csv
04_BENCH_B_RESULT.md
05_A_VS_B.md
06_NEXT_BENCH_C_PLAN.md (plan only; do not execute)
artifacts/, prompts/, logs/, tools/

The formal V2 workspace must remain unchanged.

## Preflight outcome — 2026-10-05
The pre-existing localhost:8931 endpoint was reached and an MCP initialize handshake returned a new dynamic session (server Playwright 1.64.0-alpha; protocol 2025-11-25). The subsequent tools/call requests returned HTTP 200 with a text/event-stream response but no response event before timeout. The helper reinitialized and retried once; the result was the same. Therefore HEALTH did not pass and BENCHMARK_START_TIME was not set. No worker search batch was sent and no Benchmark B candidates were collected.
