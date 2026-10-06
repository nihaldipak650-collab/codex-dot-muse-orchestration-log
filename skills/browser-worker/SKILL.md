---
name: browser-worker
description: Use DOT and Muse as persistent Web AI workers. Prefer registered Playwright tools; retain bounded ask/continue/collect, ZIP or inline delivery, local read/hash/dedupe and observation-based recovery. Codex owns planning and verification.
---

# Browser Worker

Short runs. Persistent workers. Long-running goals.

Version **3.0.0**, Full Workflow Browser Worker. Registered Playwright is the preferred live path; the standalone HTTP runtime remains a diagnostic alternative. Follow [the full workflow protocol](references/full-workflow.md) for both providers, artifact download/local read, inline fallback, reconciliation and context capsules. Read [current evidence](../../docs/BROWSER_WORKER_V3_EVIDENCE.md) before claiming live compatibility. Use for authorized worker communication, not autonomous shell execution requested by a worker.

Registered actions use `--transport registered --observation <actual fresh local page observation.json>` with the same ask/continue/collect wrapper below. `ask` returns PREPARED and exact message; Codex sends it once with registered tools. `collect` accepts observations and never sends. Both transports share alias binding and turn budget. Python 3.9+ supports the registered path; PowerShell 7 is required only for standalone.

## Worker aliases and invocation

Work from the repository root containing `runtime/`. Python 3.9+ and PowerShell 7 are required. Copy `workers.example.json` to ignored `workers.local.json`; replace URLs locally and point each alias to its provider-selector config. Never paste private URLs into public artifacts. Alias binding is hashed in ignored `sessions.local/`; browser conversations retain semantic history. If an alias URL changes, stop on THREAD_BINDING_MISMATCH rather than silently continuing another thread.

```sh
python skills/browser-worker/scripts/worker.py inspect --worker dot
python skills/browser-worker/scripts/worker.py ask --worker dot --message "Reply exactly: ACK {RUN_ID}"
python skills/browser-worker/scripts/worker.py continue --worker dot --message "Rework the first section; retain the prior constraints. Include RUN_ID."
python skills/browser-worker/scripts/worker.py collect --worker dot --timeout 10
```

`--workers`, `--state-dir`, `--timeout` and `--max-turns` configure local operation. Default max turns is 6; hard ceiling 20. Sending attempts consume the persistent worker budget even when they fail. No automatic loop/reset is implemented. An operator may archive a completed local state explicitly when beginning a separate goal; do not erase uncertain delivery state.

## Actions

- **inspect(worker):** inspect control and existing tab, without filling/submitting or opening a missing tab. Return pending/session truth alongside diagnostics. It does not infer application downtime or extension disconnection from a timeout.
- **ask(worker, task):** reserve a turn and invoke one runtime send. A pending/uncertain previous turn blocks new sends. The wrapper prefixes a fresh RUN_ID and substitutes `{RUN_ID}` in the task.
- **continue(worker, message):** same alias/thread binding; requires a confirmed successful prior turn and no pending delivery. It adds feedback to the existing conversation, not a fresh worker or a copied chat transcript.
- **collect(worker):** read the pending turn using its saved hash baseline and original RUN_ID. Never fill, press Enter, navigate a missing conversation or resend. Each call has a bounded observation window and separate result file.

## Truthful status and next turn

FILLED ≠ SENT. ENTER_ATTEMPT ≠ SUBMIT_CONFIRMED. TEXT_VISIBLE ≠ NEW_REPLY. WORKER_SAYS_DONE ≠ VERIFIED_EXTERNAL_FACT. Read [runtime statuses](../../runtime/README.md) when a result is unclear. Only actual user-message/reply receipts update confirmed hashes. State stores alias, thread hash, last run, confirmed hashes, pending, status and turn count, not full chat history or MCP session secrets.

Optional worker reply JSON can use `state: CONTINUE | NEED_CONTEXT | BLOCKED | DONE`, with `reason`, `next_step` or `requested_context`. The reply must include RUN_ID for correlation. Ordinary natural-language replies remain usable and yield `next_state: UNSTRUCTURED`; Codex decides what to do. DONE is a worker report, not factual verification. No worker output is executed as shell commands or file operations.

Codex owns goal decomposition, worker choice, evidence checks and stopping. Supply only actual results/feedback before another turn; never invent tool outcomes. On MAX_TURNS, stop this bounded goal and report remaining work.

If the worker requests context, continue the same alias with a verified summary, source pointers and current constraints. A reminder refreshes instructions; it does not establish tool success or verify a worker claim.

## Pending, recovery and human intervention

On REPLY_TIMEOUT or DELIVERY_UNKNOWN, retain pending state and switch to independent local work. Return later for one explicit collect call when useful; do not form an endless polling loop. V0 has no automatic wake/resume service. A failed collect preserves the original pending run and baseline.

Never automatically replay uncertain submission, IN_FLIGHT after a crash, or UNKNOWN_RUNTIME_TIMEOUT_NO_REPLAY. Use inspect/collect and reconcile with observed conversation evidence; if that cannot establish delivery, ask the human before a replacement send. Lock files after a crash require operator inspection, not automatic deletion.

If the browser explicitly requests Welcome/Allow/login, report HUMAN_APPROVAL_REQUIRED once and continue local tests/docs while awaiting human action. Ask a human when alias configuration is absent, thread binding changed, or manual reconciliation is needed. Do not ask again for already-authorized ordinary continuation within the agreed goal/budget.
