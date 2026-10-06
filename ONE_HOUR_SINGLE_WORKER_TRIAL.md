# One-hour single-worker trial

**HISTORICAL TEST DESIGN / DIAGNOSTIC ASSET — superseded as the next validation target.** This file is retained, not deleted. The ACK prerequisite and timed windows below describe the earlier plan, not current restart instructions. The phase is frozen; do not automatically run ACK → one hour. Read [START_HERE](docs/phase-closeout-20261006/START_HERE.md). Only explicit user restart permits a short, bounded real journey covering both workers, actual artifact/inline receipt and local read, Codex interpretation, same-thread revision and final delivery; measure user interventions/clicks/copy-paste/rescues and continuity rather than elapsed duration.

Prepared, not executed. Use only `dot` and an authorized existing conversation. Prerequisite: inspect then an exact ACK smoke must confirm submission, correlated reply and saved result. If control is unavailable or approval required, stop live actions; do not count the hour as a successful run.

Configure `workers.local.json`, selectors and ignored state locally. Set a finite budget, e.g. `--max-turns 6`. Record action times from local result files and a small local trial ledger; no private URLs or transcripts in public summaries.

| Window | Action and acceptance |
|---|---|
| 0–10 min | inspect(dot); ask exact `ACK {RUN_ID}`. Require SUCCESS with real receipts, not composer visibility. |
| 10–40 min | Three substantive consecutive turns in the same conversation: draft a comparison of three public tools for a small offline document workflow; supply actual source/check results; ask worker to revise a recommendation. Each reply includes RUN_ID. Codex verifies citations locally; no worker-requested command is executed automatically. |
| 40–50 min | Request rework of one explicitly identified section while retaining earlier constraints. Compare the reply against those constraints and source evidence. |
| 50–60 min | Use a short bounded observation window on the next permitted turn; if genuinely pending, do independent local work, then collect once. A task already completed cannot be relabeled pending merely to satisfy the test. If no genuine pending case occurs, mark this part NOT_EXERCISED. |

Measure: HUMAN_INTERVENTIONS (reason/count); FALSE_SENT (must be zero); DUPLICATE_SEND (must be zero); WRONG_REPLY_CORRELATION (must be zero); CONTEXT_CONTINUITY (constraint/source retention, human-checked); TURNS_COMPLETED; RECOVERY (status before/after explicit collect); IDLE_BUBBLE (coordinator idle time separate from worker latency). Record unknowns. A MAX_TURNS result stops the trial, even if the hour is not over.

Stop on uncertain delivery, wrong thread, repeated control failure or side effects outside scope. Preserve pending state; no automatic resend. Trial readiness means a documented procedure and tested local harness, not live acceptance. Do not start an eight-hour or multi-worker run from this plan.
