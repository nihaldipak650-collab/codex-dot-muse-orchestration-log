# Contributing

Start with evidence explanations, documentation and synthetic fixtures. This repository publishes research and coordinator playbooks; it does not yet provide a reusable browser-worker runtime. You can contribute without a DOT/Muse account or API key.

## First contributions

These are real proposed tasks, sized for roughly 1–3 hours. They are briefs, not claims that live issues have been opened. Use the bounded-contribution form to propose one and agree on scope before substantial work.

### 1. English B06/B07 walkthrough

Deliver `docs/B06_B07_WALKTHROUGH_EN.md` with a short timeline and source links to the [post-run audit](experiments/postrun/AUDIT_POSTRUN_50MIN.md) and [cutoff state](docs/CURRENT_STATE.md).

Acceptance: distinguish composer text from submission, first visible reply from bookkeeping, and historical B07 activity from the invalidated regression. B06's first reply observation is 10:46:23; 10:58 is bookkeeping. Explain why the formal window has 69 records and later accounting has 71. Mark unknowns; do not turn candidate counts into verified results. This is translation and evidence explanation, not new experimentation.

### 2. Synthetic delivery-state fixtures

Deliver `examples/delivery-state-fixtures.json` with explicitly synthetic cases for draft-only, submitted/read, reply-complete-without-result and result-received. Use the [artifact contract](schemas/artifact-contract.md) and [sanitized worker example](examples/sanitized-worker-state.json) as references.

Acceptance: each case declares its synthetic origin, observed signal, unknown fields and expected interpretation. Separate filled, sent, read, reply and received-result states. A reply-complete case may still contain zero received items. No browser automation or detector implementation is required; never present fixtures as historical worker output.

### 3. Sanitized event-field guide

Deliver `docs/EVENT_FIELD_GUIDE.md` explaining the [public event sample](examples/sanitized-events.jsonl): timestamps, lane/run identity, observation versus worker claim, and evidence confidence.

Acceptance: include a small source-linked example, explain timestamp ties/unknowns without inventing order, and preserve reported versus confirmed distinctions. No private originals or timeline viewer needed.

## Workflow

1. Choose a small brief or file an evidence correction using [issue forms](https://github.com/nihaldipak650-collab/codex-dot-muse-orchestration-log/issues/new/choose). Link public paths and state the expected outcome.
2. Fork and create a branch. Keep one purpose per pull request. English or Chinese contributions are welcome.
3. Preserve historical records. Add correction notes or new analyses rather than silently rewriting original run outcomes. Never move `v0.1-freeze-2026-10-06`.
4. Check links and evidence boundaries. If Python 3.9+ is available, refresh and verify the current-main manifest:

```sh
python tools/verify_public_hashes.py --update
python tools/verify_public_hashes.py
git diff --check
```

`--update` writes hashes for tracked and non-ignored untracked files; inspect `git status` first and keep personal files outside the checkout. The default checker is read-only. Hash matching proves byte integrity, not privacy or factual correctness.

5. Submit a PR with changed paths, public source links, validation and limitations. A maintainer reviews evidence and scope; runtime experiments need a separate agreed plan and stop conditions.

## Boundaries

Do not upload credentials, browser profiles, private chats, raw sessions or private archives. See [SECURITY.md](SECURITY.md). Mark new discovery as unverified until evidence supports more. Avoid performance claims without comparable measurements.

The [roadmap](docs/ROADMAP.md) separates runtime priorities from beginner tasks. Reliable bootstrap, sent-message detection and coordinator scheduling are substantial engineering work, not automatic good-first-issue labels.

No project license has been selected. Contribution guidance does not grant a software reuse license or establish a CLA. License selection requires an owner decision; discuss intended reuse before relying on permissions.
