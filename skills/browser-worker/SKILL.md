---
name: browser-worker
description: Use DOT and Muse as persistent Web AI workers. Prefer registered Playwright tools; retain bounded ask/continue/collect, ZIP or inline delivery, local read/hash/dedupe and observation-based recovery. Codex owns planning and verification.
---

# Browser Worker

Short runs. Persistent workers. Long-running goals.

Version **3.0.0**, Full Workflow Browser Worker. Registered Playwright is the preferred live path; the standalone HTTP runtime remains a diagnostic alternative. Follow [the full workflow protocol](references/full-workflow.md) for both providers, artifact download/local read, inline fallback, reconciliation and context capsules. Read [current evidence](../../docs/BROWSER_WORKER_V3_EVIDENCE.md) before claiming live compatibility. Use for authorized worker communication, not autonomous shell execution requested by a worker.

Registered actions use `--transport registered --observation <actual fresh local page observation.json>` with the same ask/continue/collect wrapper below. `ask` returns PREPARED and exact message; Codex sends it once with registered tools. `collect` accepts observations and never sends. Both transports share alias binding and turn budget. Python 3.9+ supports the registered path; PowerShell 7 is required only for standalone.

## Worker aliases and invocation

Current phase is frozen: first read [START_HERE](../../docs/phase-closeout-20261006/START_HERE.md). Only explicit user restart permits one short, bounded real user journey. Registered examples below are reference shapes after fresh observations, not authorization to run. The unchanged wrapper default is standalone; select transport explicitly.

Work from the repository root containing `runtime/`. Python 3.9+ is required; PowerShell 7 is required only for standalone mode. Copying this Skill directory alone does not include the repository runtime dependencies. Copy `workers.example.json` to ignored `workers.local.json`; replace URLs locally and point each alias to its provider-selector config. Never paste private URLs into public artifacts. Alias binding is hashed in ignored `sessions.local/`; browser conversations retain semantic history. If an alias URL changes, stop on THREAD_BINDING_MISMATCH rather than silently continuing another thread.

```sh
python skills/browser-worker/scripts/worker.py inspect --transport registered --worker dot --observation sessions.local/observation.json
python skills/browser-worker/scripts/worker.py ask --transport registered --worker dot --observation sessions.local/observation.json --message "<authorized task>"
# PREPARED: Codex sends with registered tools, then saves fresh actual observations.
python skills/browser-worker/scripts/worker.py collect --transport registered --worker dot --observation sessions.local/observation.json
python skills/browser-worker/scripts/worker.py continue --transport registered --worker dot --observation sessions.local/observation.json --message "Revise the identified section using actual received results."
```

`--workers`, `--state-dir`, `--timeout` and `--max-turns` configure local operation. Default max turns is 6; hard ceiling 20. Sending attempts consume the persistent worker budget even when they fail. No automatic loop/reset is implemented. An operator may archive a completed local state explicitly when beginning a separate goal; do not erase uncertain delivery state.

## Actions

Use explicit --transport standalone only for diagnostic, local test or selected standalone usage. ACK smoke and [one-hour trial](../../ONE_HOUR_SINGLE_WORKER_TRIAL.md) remain historical diagnostic assets. Registered collect consumes one supplied observation per invocation; Codex bounds the observation window, Python does not poll registered tools automatically.

Both DOT and Muse historically delivered ZIPs. Either may deliver structured inline results or one primary artifact/bundle according to actual provider capability and page state. Inline is a reliable fallback, not Muse's permanent-only mode. [Benchmark B's four original ZIPs/hash evidence](../../docs/phase-closeout-20261006/SOURCES.md) use formats different from the V3 contract; local tests do not prove historical compatibility.

- **inspect(worker):** inspect control and existing tab, without filling/submitting or opening a missing tab. Return pending/session truth alongside diagnostics. It does not infer application downtime or extension disconnection from a timeout.
- **ask(worker, task):** reserve a turn. Standalone invokes one runtime send; registered returns PREPARED text for Codex to send using its existing browser tools. A pending/uncertain previous turn blocks new sends. The wrapper prefixes a fresh RUN_ID and substitutes `{RUN_ID}` in the task.
- **continue(worker, message):** same alias/thread binding; requires a confirmed successful prior turn and no pending delivery. It adds feedback to the existing conversation, not a fresh worker or a copied chat transcript.
- **collect(worker):** reconcile the pending turn using its saved baseline and original RUN_ID. Never fill, press Enter, navigate a missing conversation or resend. Standalone performs a bounded read window with a separate result receipt; registered reconciles one actual supplied observation into the durable turn.

## Truthful status and next turn

FILLED ≠ SENT. ENTER_ATTEMPT ≠ SUBMIT_CONFIRMED. TEXT_VISIBLE ≠ NEW_REPLY. WORKER_SAYS_DONE ≠ VERIFIED_EXTERNAL_FACT. Read [runtime statuses](../../runtime/README.md) when a result is unclear. Only actual user-message/reply receipts update confirmed hashes. State stores alias, thread hash, last run, confirmed hashes, pending, status and turn count, not full chat history or MCP session secrets.

Optional worker reply JSON can use `state: CONTINUE | NEED_CONTEXT | BLOCKED | DONE`, with `reason`, `next_step` or `requested_context`. The reply must include RUN_ID for correlation. Ordinary natural-language replies remain usable and yield `next_state: UNSTRUCTURED`; Codex decides what to do. DONE is a worker report, not factual verification. No worker output is executed as shell commands or file operations.

Codex owns goal decomposition, worker choice, evidence checks and stopping. Supply only actual results/feedback before another turn; never invent tool outcomes. On MAX_TURNS, stop this bounded goal and report remaining work.

If the worker requests context, continue the same alias with a verified summary, source pointers and current constraints. A reminder refreshes instructions; it does not establish tool success or verify a worker claim.

## Pending, recovery and human intervention

On REPLY_TIMEOUT or DELIVERY_UNKNOWN, retain pending state and switch to independent local work. Return later for one explicit collect call when useful; do not form an endless polling loop. V0 has no automatic wake/resume service. A failed collect preserves the original pending run and baseline.

Never automatically replay uncertain submission, IN_FLIGHT after a crash, or UNKNOWN_RUNTIME_TIMEOUT_NO_REPLAY. Use inspect/collect and reconcile with observed conversation evidence; if that cannot establish delivery, ask the human before a replacement send. Lock files after a crash require operator inspection, not automatic deletion.

If the browser explicitly requests Welcome/Allow/login, report HUMAN_APPROVAL_REQUIRED once and continue local tests/docs while awaiting human action. Ask a human when alias configuration is absent, thread binding changed, or manual reconciliation is needed. Do not ask again for already-authorized ordinary continuation within the agreed goal/budget.
