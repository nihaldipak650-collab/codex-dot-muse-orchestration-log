# Baseline A — Prior Orchestration

Source set was read from the formal workspace without modification: ORCHESTRATOR_POSTMORTEM_20261005.md, 06_AGENT_RUNS.jsonl, 02_BATCH_LOG.md, CURRENT_STATE.md. The V1 ledger is held separately as a read-only dedupe reference.

## Prior result
The postmortem records a 26h01m27s file-evidence wall span and estimates 6–10 hours of active coordinator effort at low confidence. The formal quota was already complete at 100/100. The candidate pool reached 221 (207 ordinary candidates plus 14 reserve records); the formal ledger had 232 rows, 221 countable candidates, and 11 preflight/conditional/rejected rows. Source totals were GitHub 132, X 9, YouTube 80. Second-pass accepted/verified remained 0.

## Pipeline evidence
The clearest avoidable refill bubble was DOT B09: first complete result visible 12:04, next send 13:22:53, a 78m52s gap. Other examples include Muse B06 (16m22s) and Muse B07 (11m). Some overnight/file-evidence gaps cannot be attributed to active coordinator work. The prior postmortem counted 539 raw browser-control artifacts: 64 browser_find, 50 snapshots, 50 tab selections, 30 waits, 20 refreshes, 29 attachment opens, 22 downloads, 5 reconnect/reopen, and 24 identity checks (categories can overlap and were inferred from filenames).

## Reliability evidence
The shared Playwright Extension session intermittently failed. The formal state records browser_tabs list and read-only calls timing out, extension inventory showing no tabs / nodeRepl.fetch failure, and a brief recovery where exact tabs were Muse (tab 0) and DOT_WORKER (tab 1). The formal task then stopped without alternate browser or substitute worker. These are historical observations, not a claim about current health.

## Benchmark purpose
Benchmark B tests whether a thin high-level control surface and refill-first, two-lane dispatch reduce refill latency and idle bubbles. It is isolated and does not change the formal V2 ledger, its quota, candidates, or second-pass status.
