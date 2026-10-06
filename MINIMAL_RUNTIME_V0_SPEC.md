# Minimal Runnable V0 — single worker

**Historical design / diagnostic asset, not current restart instructions.** First read [START_HERE](docs/phase-closeout-20261006/START_HERE.md). V3 local implementation exists at f8dcb4b; its provider-live full workflow remains NOT_RUN. This phase is frozen. Retained ACK and V0 pre-implementation statements below do not authorize a run or replace the next explicitly restarted real user journey.

Historical design baseline from before `GITHUB-RUNTIME-SPRINT-20261006`. Experimental code now exists in [runtime/README.md](runtime/README.md), with passing local tests and an unverified live loop. The specification below preserves the original proposed design and pre-implementation status.

**Proposed implementation specification, not shipped software.** The public clone currently cannot execute this loop. The [gap audit](PROJECT_GAP_AUDIT.md) distinguishes historical operation from reusable code.

Goal: connect browser control, select one existing worker conversation, send one prompt, prove submission, observe its reply, save it locally and return an explicit state. No refill scheduler, model implementation, internal API proxy or multi-agent platform.

## Five implementation pieces

1. **Connection and preflight:** choose one supported Playwright control route, implement connection/health checks and record its tested versions. A bounded probe must find a usable browser context before starting a task deadline. The exact historical transport is not pinned by the public record; do not pretend a particular endpoint is already available.
2. **Explicit conversation adapter:** enumerate tabs, select the configured worker conversation and validate its composer and conversation-message regions. Require unique selection; no arbitrary first-tab fallback. Start with one provider adapter whose actual UI has been inspected. Existing authenticated browser session remains local.
3. **Send and submission receipt:** snapshot existing messages, fill the composer, submit once, then confirm a new user-message node matching the prompt/run token. Composer text, an Enter key call, or whole-page token presence alone is insufficient. Ambiguous delivery returns `SUBMISSION_UNCONFIRMED`; do not resend automatically.
4. **Reply correlation and bounded observation:** read a new assistant reply following the confirmed user message, keeping it separate from old replies and the composer. Provider-specific completion signals must be defined and tested. A stable text snapshot alone cannot prove completion. Preserve partial replies at the deadline; use `REPLY_TIMEOUT` or `REPLY_COMPLETION_UNCONFIRMED` rather than invent success.
5. **Capture and one-command entry:** save reply text, minimal event receipts and terminal result JSON locally, then return state/exit status. Supply real config/install documentation and an offline fixture suite. A later explicitly authorized one-worker smoke demo proves integration; historical reports do not substitute for it.

## Proposed interface and configuration

Candidate files: `runtime/connect`, `runtime/worker_adapter`, `runtime/run_once`, `runtime/capture`, plus `examples/runtime-config.example.json`. Language/package choice remains implementation work. There is no install command to advertise yet.

Illustrative configuration fields, **not accepted by any shipped program**:

```json
{
  "control_route": "TO_BE_SELECTED_AND_TESTED",
  "worker_adapter": "ONE_TESTED_PROVIDER",
  "conversation_match": "LOCAL_EXACT_MATCH",
  "prompt_file": "LOCAL_PROMPT_PATH",
  "submission_timeout_seconds": 20,
  "reply_timeout_seconds": 120,
  "output_directory": "LOCAL_OUTPUT_DIRECTORY"
}
```

These timeout values are design defaults to test, not historical performance. Prompt/conversation paths and connection material belong in local config, not committed sessions. Setup documentation must eventually specify tested OS, language runtime, pinned Playwright/control adapter version, browser version, connection mode and login procedure. Do not infer those requirements from Git/Python requirements for the unrelated hash checker.

## State and result contract

Happy path: `PREFLIGHT_OK → TAB_SELECTED → PROMPT_FILLED → SUBMITTED_CONFIRMED → REPLY_OBSERVED → REPLY_COMPLETE → SAVED`.

Terminal outcomes also include `CONTROL_UNAVAILABLE`, `TAB_NOT_FOUND`, `TAB_AMBIGUOUS`, `SUBMISSION_UNCONFIRMED`, `REPLY_TIMEOUT`, `REPLY_COMPLETION_UNCONFIRMED`, and `CAPTURE_FAILED`. Record the last confirmed state, unknowns and elapsed times. Read/worker-claimed completion is separate from received reply and saved bytes. A text reply is not source-verified research or proof that worker attachments were delivered.

Proposed result fields: `run_id`, `worker_adapter`, `started_at`, `finished_at`, `last_confirmed_state`, `terminal_status`, `submission_receipt`, `reply_receipt`, `reply_text_path`, `reply_sha256`, `partial`, `unknowns`. Receipts store observation type/time and local message identity; exclude account tokens and session dumps. Exit 0 only for `SAVED`; other terminal states return nonzero with a readable result if storage permits.

## Acceptance tests and demo

- Offline fixtures cover composer-only token, old user message, confirmed new submission, old assistant reply, new partial/complete reply, ambiguous tabs and capture failure.
- Prove no auto-resend after uncertain submission; bounded waits terminate and partial output remains identified.
- Verify saved reply bytes/hash and result schema; test output failures without falsely returning success.
- Live acceptance, in a future separately scoped task: one existing authorized tab, one harmless prompt, one confirmed user message, one correlated reply and saved result. Document exact tested setup and limitations. This round runs none of these browser operations.

Success means one reproducible communication loop. Coordinator task selection/refill, multiple workers, long benchmarks and speedup claims remain later work.
