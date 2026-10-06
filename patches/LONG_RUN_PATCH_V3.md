# LONG_RUN_PATCH_V3 — capability-superset orchestration

V3 keeps the progress-first lessons from V2, but changes the implementation philosophy.

The coordinator should not be driven by a long checklist of forbidden actions. It should pursue the user goal, reuse capabilities that have already worked, and preserve verified behavior while improving reliability.

## Core model

User gives the long-running goal.

Codex remains the coordinator.

Browser Worker Skill turns existing DOT / Muse web conversations into persistent workers.

Playwright provides browser control.

Artifacts and local state provide durable handoff between turns.

## Capability-superset rule

A new version should preserve previously verified capabilities unless a capability is explicitly deprecated with a recorded reason.

Do not narrow a regression test so much that a previously working part of the workflow silently disappears.

Historical capabilities include both conversation control and artifact handling.

## Worker loop

A useful worker loop is:

goal → send → observe → collect → evaluate → continue / correct / request artifact → receive real result → continue until bounded completion.

A worker can finish one short run while the overall Codex goal remains active.

Short worker runs can therefore compose into long-running goals.

## Truthful state

The system reports only what it actually observed.

Examples:
- composer filled is not sent;
- send attempted is not submit confirmed;
- a visible old reply is not a correlated new reply;
- worker COMPLETE is not artifact received;
- download clicked is not file downloaded;
- local state is not page truth.

Uncertain state remains uncertain until reconciled by observation.

## Artifact delivery

The worker result path should support both:
- structured inline result;
- one primary result bundle.

Preferred bundle shape when supported:

manifest.json
results.csv or results.json
summary.md
optional rejected / next_gaps

Artifact states are separate:
DECLARED → VISIBLE → DOWNLOADED → READ → VALIDATED.

DOT may prefer bundle-first delivery.

Muse must keep a usable structured inline fallback because historical attachment handling was less reliable.

## Refill and deep processing

When a worker result is good enough to determine the next independent task, refill first.

Fetch, hash, unpack, parse, dedupe, and deeper synthesis can happen while the worker is busy again.

Do not let attachment handling recreate the long idle bubbles seen in early PROJECT-WHEELS runs.

## Session continuity

The Skill keeps a small durable control/session record rather than copying the whole chat history.

It may keep a compact verified context capsule for goals, constraints, accepted facts, and artifact references when the worker forgets earlier instructions.

The browser thread remains the semantic conversation; the local record remains control truth and recovery support.

## Recovery

Recovery should prefer observation and reconciliation over replay.

If an action may already have crossed the delivery boundary, do not automatically resend.

If the page is stale or an operation times out, a bounded read-only refresh/reconciliation is allowed before declaring uncertainty.

If a download is unclear, verify the local file rather than assuming the click succeeded.

## Transport

Prefer the already-registered Playwright tool path for live Codex operation when it is available.

Keep the standalone HTTP/SSE runtime for testing, diagnostics, and environments that explicitly need it.

Do not replace a historically working control path merely to make the architecture look cleaner.

## Coordinator behavior

DOT and Muse are independent workers.

Codex decides:
- which worker receives which task;
- whether a reply needs correction;
- whether to continue the same thread;
- when an artifact must be fetched;
- when to stop discovery and synthesize;
- when the overall goal is complete.

Worker pending does not imply coordinator idle.

A report/checkpoint does not imply the project is finished.

## Regression philosophy

Each major version should run a regression that covers the actual end-to-end workflow, not only the newest subsystem.

A full workflow regression should include:
- DOT and Muse;
- send/confirm/reply;
- same-thread continuation;
- artifact or inline fallback;
- local read;
- dedupe/hash where applicable;
- bounded recovery;
- coordinator continuation.

Smaller subsystem tests remain useful, but they should be named accordingly rather than treated as full-workflow proof.

## Current direction

V1 = historical orchestration baseline.

V2 = progress-first coordinator behavior + local runtime + persistent browser-worker Skill.

V3 = capability-superset browser-worker workflow that restores artifact delivery and keeps the proven long-running coordinator behavior.

The next implementation should follow this document as a direction, not as a step-by-step script.
