# Benchmark B — Final Result

BENCH_B_DONE = YES
PRE_FLIGHT = PASS
BENCHMARK_START_TIME_UTC = 2026-10-05T14:31:43.7297116Z
BENCHMARK_DEADLINE_UTC = 2026-10-05T16:01:43.7297116Z
MEASURED_WALL_CLOCK = 90m 00s
STOP_REASON = 90_MINUTE_DEADLINE

## Outcome

The existing Playwright Remote session showed both exact worker pages before timing began: Muse / Chat — MUSE_WORKER and DOT / DOT_WORKER. Benchmark B ran against those tabs; no RPC wrapper, new session, CDP, In-App Browser, or replacement search was used. The formal V2 workspace remained unchanged.

Four Muse rounds completed (5 results each). DOT R1 returned 5 candidates; DOT R2 produced two assistant result cards with the same RUN_ID after a send timeout and retry. The two R2 ZIP files are byte-identical (SHA-256 `969911D807EDA64FFD05BD36D526E770217E3311BBC626668A2228CCDBAD1EDE`), so the second delivery did not add distinct candidates. DOT R3 was left unsent when the 90-minute deadline passed.

## Candidate counts

| Direction | Muse retained | DOT retained | Unique accepted |
|---|---:|---:|---:|
| Literature assistant | 5 | 5 | 10 |
| Pixel/scientific animation | 5 | 4 | 9 |
| Management/simulation game | 5 | 0 | 5 |
| Research SOP/scientific workflow | 5 | 0 | 5 |
| **Total** | **20** | **9** | **29** |

Thirty-five candidate rows were reported across worker result files. The repeated, hash-identical R2 archive contains 5 rows already present in its first delivery, leaving 30 distinct candidate entities before V1 comparison. One distinct entity (`tween.js`, V1 PW-033) is already in V1, leaving 29 unique accepted candidates. The staging CSV keeps all 35 rows: 29 `CANDIDATE_UNVERIFIED` and 6 `REJECTED_DUPLICATE` rows (5 repeat-delivery rows plus the first-delivery V1 duplicate; the second `tween.js` row overlaps both categories). No obvious off-topic or malformed-link drops were made. All unique candidates remain unverified; no repository was cloned, installed, run, or tested.

Unique accepted source mix: 9 GitHub, 19 YouTube, 1 X. V1 dedupe used its 100 rows read-only. Muse's consolidated four-round ZIP and the three DOT attachment downloads (one R1 and two identical R2 copies) were fetched after the timed window; retrieval and review were post-stop and did not extend the benchmark.

## Timed metrics

- Unique candidates per hour: 29 / 1.5 = **19.3**.
- Raw reported candidate rows per hour: 35 / 1.5 = **23.3**.
- Batches: Muse 4 completed; DOT R1 and R2 completed; DOT R2 had one duplicate delivery; DOT R3 not sent.
- Bundle downloads: 4 attachments in total (1 consolidated Muse bundle plus 3 DOT downloads); 3 unique archive contents.
- CONTROL_DOWN / APP_DOWN: **0 / 0**. The worker page stayed reachable and DOT eventually replied; the long R1 wait is recorded as worker latency, not a control outage.
- Recovery attempts: 0. Human interventions during the timed window: 0.
- IDLE_BUBBLE: not reliably measurable; no explicit classification was recorded, and first-result/next-send timestamps are incomplete.
- Mean/max refill latency and GUI action count: **not reliably measured**. The event log lacks complete first-visible/send markers, and the Remote click tool timed out while some sends later took effect.

## Reliability notes

The DOT R1 request was delivered at 14:39:18 UTC and its completed result appeared with a minute-rounded local UI time of 23:42 (about 63 minutes later). After a DOT R2 send call timed out, I re-entered and retried before resolving delivery; this created a second delivery and two identical outputs. This is a confirmed coordinator duplicate-send error, not a control outage. DOT R3's send call timed out near the deadline; an exact-thread check found no R3 message, the unsent composer text was cleared, and no dispatch occurred after the deadline.

The append-only event log retains correction records for one late-entered send-failure note and one local-time arithmetic error in an intermediate checkpoint; the final duration above uses UTC offsets and the protocol's exact 90-minute window.

## Artifacts

- `03_BENCH_B_STAGING.csv` — all reported rows, dedupe outcomes, and provenance.
- `02_BENCH_B_EVENTS.jsonl` — sends, polls, downloads, corrections, dedupe, and stop condition.
- `artifacts/BENCHB-MUSE-R1-R4_FETCH/` — consolidated Muse results.
- `artifacts/BENCHB-DOT-R1/` — DOT literature result.
- `artifacts/BENCHB-DOT-R2/delivery-01/` and `delivery-02/` — identical duplicate R2 bundles.
