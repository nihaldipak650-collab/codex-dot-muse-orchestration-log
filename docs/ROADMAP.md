# Roadmap

**Phase frozen; this backlog is not an execution queue.** Current entrypoint: [START_HERE](phase-closeout-20261006/START_HERE.md). Browser Worker 3.0.0 at f8dcb4b has local implementation and recorded passing tests; V3 provider-live full workflow remains NOT_RUN. The proposal tables below originated before that implementation and remain historical planning assets, not claims that those capabilities are all absent.

Only explicit user restart permits the next short, bounded real user journey: task → DOT/Muse → reply → artifact or inline → actual local read → Codex interpretation → same-thread revision → final delivery. Prefer registered Playwright executed by Codex; standalone remains diagnostic/local-test/explicit usage. Both workers historically delivered ZIPs; inline is fallback for either, not Muse-only delivery. Historical ZIP formats are not proven compatible with the V3 contract.

Measure human interventions, manual clicks, copy/paste, rescue events, actual artifact receipt/read and context continuity against old manual Playwright coordination. No automatic ACK → one-hour sequence, V4 development, new release/tag or framework installation follows from this roadmap. No new runtime experiment was performed for this closeout.

## P0: reliable coordination

| Work | Why | Acceptance before claiming success |
|---|---|---|
| Reliable Playwright bootstrap | The frozen regression lacks confirmed preflight | Bounded health check records environment, usable session and failure reason; run start/deadline are assigned only after confirmed preflight. No credentials in logs. |
| Composer versus sent-message detection | B06 draft text was treated as delivered | Separate draft, submission and reply signals; synthetic positive/negative fixtures and observable delivery receipts. Whole-page text matching alone is insufficient. |
| Progress-first coordinator loop | B07 pending work replaced useful coordinator progress | Independent lane transitions, bounded retries, refill/action timestamps and explicit stop conditions; measure idle time and duplicate delivery before making speedup claims. |

Read the [V2 playbook](../patches/LONG_RUN_PATCH_V2.md) and [failure modes](FAILURE_MODES.md). These tasks require a maintainer-agreed implementation and test plan. They are not beginner-sized browser operations.

## P1: inspectable results

| Work | Acceptance |
|---|---|
| Event timeline viewer | Load sanitized fixtures, distinguish observed/reported/unknown events, retain timestamps and provenance, display missing observations without inventing continuity. |
| Artifact/result contract | Version field meanings and delivery IDs; deduplicate repeated artifacts without confusing worker-complete with item-received. Reconcile raw, structured and verified counts separately. |
| Regression benchmark harness | Finite run window after preflight, comparable workloads, measured refill latency/idle time/duplicates and repeatable offline fixture checks before live trials. |
| Worker state visualization | Show independent lanes and uncertainty; never infer completion from pending UI or composer text. |

## First steps without worker accounts

The [contribution guide](../CONTRIBUTING.md#first-contributions) specifies three bounded tasks: an English B06/B07 walkthrough, synthetic delivery-state fixtures and an event-field guide. Each has an output and acceptance criteria; none requires a long run or private original data.

## Owner decisions

- Select a project license before advertising unrestricted reuse. No license is implied by public visibility.
- Establish a supported private reporting channel and response expectations before promising them.
- Introduce CODEOWNERS only with accepted review responsibilities; enable Discussions only when there is an actual moderation plan.
- Create curated issues and labels from accepted task scopes rather than populating an empty issue list with fictional activity.
- Produce and review the [social preview](../SOCIAL_PREVIEW_SPEC.md) before uploading it.
