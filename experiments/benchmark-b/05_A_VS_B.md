# Baseline A vs Benchmark B

## Result

Benchmark B completed its fixed 90-minute window with **29 unique `CANDIDATE_UNVERIFIED` resources** and stopped at the deadline. The existing Playwright Remote session and both worker pages were available; there was no `CONTROL_DOWN` or `APP_DOWN`. This is a limited throughput comparison, not a controlled claim that the new workflow is faster.

## Side-by-side

| Metric | Baseline A | Benchmark B |
|---|---:|---:|
| Measured span | 26h 01m 27s file-evidence wall span | 90m timed window |
| Countable/unique candidates | 221 countable (207 ordinary + 14 reserve) | 29 unique after canonical dedupe |
| Candidate rate by wall span | about 8.5/hour | 19.3/hour |
| Source mix | GitHub 132, X 9, YouTube 80 | GitHub 9, X 1, YouTube 19 |
| Browser-control artifacts | 539 inferred artifacts | Not reliably metered |
| Refill evidence | DOT B09 bubble: 78m 52s | Exact mean/max not computable from incomplete timestamps |
| Second-pass verification | 0 accepted/verified | Not part of this run; all candidates remain unverified |

The wall-span arithmetic makes B's unique-candidate rate about 2.3x A's historical wall-span rate. Baseline A separately estimates 6–10 hours of active coordinator effort at low confidence, which implies roughly 22.1–36.8 candidates/hour; B's 19.3/hour is below that estimate. These denominators and candidate sets differ, so neither ratio establishes a reliable speedup.

## What Benchmark B shows

- The direct Remote session was usable with Muse and DOT_WORKER visible. It stayed responsive throughout the timed run.
- Muse completed all four rounds and contributed 20 unique candidates.
- DOT contributed 9 unique candidates across R1 and R2. Its first response arrived roughly 63 minutes after R1 dispatch, based on the minute-rounded UI time.
- A DOT R2 send timeout followed by a retry caused duplicate delivery. The resulting ZIPs have identical SHA-256 hashes; five repeated rows and one V1 duplicate were rejected from the unique count.
- DOT R3 was not dispatched after the 90-minute hard stop.

## Measurement limits

The benchmark event stream does not have complete, per-round `FIRST_RESULT_VISIBLE_TIME` and `NEXT_BATCH_SEND_TIME` values. Therefore the required mean/max refill latency, confirmed idle-bubble duration, and comparable GUI action count cannot be reconstructed without guessing. Baseline A's 539 actions were inferred from filenames and categories; B did not use an equivalent counter. Candidate discovery was lightweight only, and no tests or deep license/version audits were performed.

The initial preflight/helper diagnostic notes in older drafts are superseded: timed Benchmark B used the existing Playwright Remote tabs only. No V2 formal ledger or quota was modified. All B candidates are isolated in the benchmark staging file.

## Conclusion

Benchmark B demonstrates that the direct two-lane workflow collected 29 unique, relevant-looking candidates in 90 minutes, but its evidence is insufficient to conclude a dependable speed improvement. The primary measured strengths are parallel source coverage and low apparent wall-time per candidate; the principal weaknesses are the very long DOT R1 response delay, one duplicate send, and missing timing/action instrumentation.
