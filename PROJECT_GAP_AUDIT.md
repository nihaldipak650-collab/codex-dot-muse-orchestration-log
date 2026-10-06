# Project mechanism and runtime gap audit

Audit baseline: `c2bbd4640924ca79f541e5607471c7330cd8d53d`, 2026-10-06. Written before this round's README changes. Scope is the public checkout and existing records, not a new browser test or another benchmark search.

## Actual mechanism and evidence

The recorded workflow is **Human → Codex coordinator → Playwright/MCP browser control → existing browser conversations (DOT / Muse) → replies → local artifacts/state → coordinator decisions**.

[Architecture](docs/ARCHITECTURE.md) separates control and data planes. The [B06/B07 audit](experiments/postrun/AUDIT_POSTRUN_50MIN.md) records tab listing, input filling, Enter submission, page/message observation and reply extraction. It also records the failure where input filling was mistaken for sending. The [V2 playbook](patches/LONG_RUN_PATCH_V2.md) explicitly retains the existing Playwright/browser path rather than rewriting MCP or SSE. [Benchmark B](experiments/benchmark-b/04_BENCH_B_RESULT.md) records both lanes and saved result artifacts.

Worker intelligence comes from existing web AI applications; Codex chooses and evaluates tasks, and browser tools carry interactions. Public evidence does not establish a new model, a replacement DOT/Muse application or a reverse proxy to provider-internal APIs. It also does not pin the exact control transport, extension topology or DOT-to-ChatGPT identity. The diagram should say DOT and Muse, and omit unconfirmed Chrome Extension / Remote MCP components.

## Landing-page gaps before this edit

| Question | Baseline finding | Needed change |
|---|---|---|
| A. What does it actually do? | Browser AI workers are named, but their concrete communication path is implicit. No timed user study establishes 20-second comprehension. | Say that Codex operates existing web conversations through browser automation in the opening. |
| B. How does it work? | The opening diagram jumps from Codex to workers, hiding Playwright and Browser. | Draw the control chain and name four responsibilities. |
| C. Why not just use an API? | Original tasks used existing independent web-worker conversations for resource research. No API-versus-browser comparison or universal preference is established. | Explain the studied interaction surface; do not invent cost, quality, access or policy advantages. |
| D. What is already real? | Historical sends, reply extraction, artifact/ledger work and long-run failures are documented. | Keep evidence links, historical scope and unverified candidate qualifiers. |
| E. What is not a product? | The README correctly says runtime is roadmap work. Only executable shipped here is a file-hash utility. | Make runtime absence visible beside the mechanism and exploration instructions. |
| F. Can a clone communicate with a worker? | No. Clone permits evidence exploration, not a live loop. | Provide precise gaps and a single-worker implementation specification. |

## Runnability inventory

Statuses concern artifacts in this public repository. **ALREADY_EXISTS** means usable for the stated narrow purpose. **PARTIAL** means historical operation, sample or design exists, but no reusable implementation ships here. **MISSING** means no public runnable artifact/instructions for that capability were found. Historical success is not an installable component.

| Capability | Status | Existing evidence / precise missing piece |
|---|---|---|
| Public evidence exploration and hash verification | ALREADY_EXISTS | Reports, sanitized examples and `tools/verify_public_hashes.py`; this is not a worker loop. |
| Minimal coordinator runtime | MISSING | No runtime entry point/package or executable coordinator. |
| Playwright bootstrap | PARTIAL | Historical control worked; regression preflight was invalidated. No portable connector, pinned dependencies or health check. |
| Browser / tab discovery | PARTIAL | Historical `browser_tabs` observations; no exported discovery/selection adapter. |
| Send prompt | PARTIAL | Historical fill + Enter recorded; no reusable worker-specific sender. |
| Confirm submitted | PARTIAL | Audit distinguishes submission; no implemented user-message receipt detector. |
| Read reply | PARTIAL | Historical message/page extraction; no reusable new-reply correlation/completion adapter. |
| Composer versus sent detection | PARTIAL | Failure explanation and rule exist; no executable detector/fixture suite. |
| Worker state model | PARTIAL | [Event model](schemas/event-model.md) and sanitized snapshot; no enforced runtime transition logic. |
| Artifact capture | PARTIAL | Saved historical outputs and proposed contract; no callable capture/export pipeline. |
| Refill loop | PARTIAL | V2 operating rules; no measured reusable scheduling implementation. |
| Timeout / retry | PARTIAL | Recorded waits/retries and finite-retry guidance; no reusable policy enforcement. |
| Dedupe | PARTIAL | Historical ledger deduplication and duplicate ZIP analysis; no public runtime dedupe module. |
| Runtime config example | MISSING | Research prompt examples are not connection/adapter configuration. |
| Runtime install instructions | MISSING | Git clone/hash commands install no communication runtime. |
| Runtime environment requirements | MISSING | No validated runtime dependency/version/browser/session compatibility matrix. |
| Minimal live communication demo | MISSING | Conceptual Mermaid and historical reports are not a reproducible one-prompt demo. |

## Decision: document now, build a small tool next

Current type: **research log + experiments + playbook + sanitized examples + integrity utility**. This round clarifies it; it does not implement a runtime.

To become runnable, the smallest next implementation is five pieces: connection/preflight; explicit tab adapter; send with submitted-message receipt; correlated reply observation with finite timeout; local capture and terminal status behind one command/config. See [Minimal Runtime V0](MINIMAL_RUNTIME_V0_SPEC.md). Start with one worker and one prompt, not multi-lane scheduling. Refill, broad retry and cross-worker dedupe follow only after this loop works.
