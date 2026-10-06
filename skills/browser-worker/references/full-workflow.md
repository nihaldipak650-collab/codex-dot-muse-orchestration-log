# V3 full workflow

**Operational reference, not a current run instruction.** The phase is frozen; first read [START_HERE](../../../docs/phase-closeout-20261006/START_HERE.md). Only explicit user restart permits a short, bounded task → DOT/Muse → reply → artifact/inline → actual local read → Codex interpretation → same-thread revision → final delivery. Measure interventions, manual clicks, copy/paste, rescues, artifact receipt/read and continuity versus old manual Playwright coordination. ACK/one-hour plans are historical diagnostics.

Registered browser tools remain owned by Codex. Python does not pretend it can call tools registered in the agent. The common state engine reserves sends and verifies subsequent page observations; artifact ingestion works with either transport.

Browser Worker prepares RUN_ID, state and receipt logic. Codex invokes its already-registered Playwright tools and returns actual observations; this is not an atomic MCP tool automatically called by a Python wrapper. standalone remains diagnostic, local-test or explicit standalone usage. Choose transport explicitly: the unchanged CLI default is standalone.

## Observe, reserve, send, reconcile

Select the exact configured DOT/Muse tab using registered browser_tabs. Inspect a fresh snapshot and validate composer, user-message, assistant-message and generation selectors. Set provider and selectors in ignored workers.local.json. Do not guess Muse selectors from DOT markup. The example aliases are placeholders, not validated adapters.

Generate `python runtime/browser_plan.py --worker dot`. Read its private browser-plan.local.json, pass observation_function to registered browser_evaluate and save the actual result object to sessions.local/observation.json. Tool errors are not observations. Confirm message scopes and real generation signal through UI inspection; an empty new conversation is allowed only after inspection.

Reserve:

```sh
python skills/browser-worker/scripts/worker.py ask --transport registered --worker dot --observation sessions.local/observation.json --message "<task>"
```

PREPARED reserves a durable RUN_ID/baseline/turn budget before returning exact text; it means no delivery yet. Type that message verbatim into the unique inspected composer (submit=false), then press Enter once. An uncertain fill/Enter is never replayed. A crash before input remains pending conservatively.

Generate a fresh plan with `--run-id <id>`, observe/save, then:

```sh
python skills/browser-worker/scripts/worker.py collect --transport registered --worker dot --observation sessions.local/observation.json
```

Collect never sends. Repeat only within a bounded explicit collection window (default 10s, ceiling 300s), with fresh observations and spacing. An exact new user message absent from baseline is required. A unique correlated new assistant reply must be stable in two distinct timestamped observations, with no generation and explicit completion. Structured completion is JSON with matching run_id, enum state CONTINUE/NEED_CONTEXT/BLOCKED/DONE and optional results array. Natural text needs a validated UI completion signal. Old replies, B06 composer text, stale/replayed observations and wrong tabs cannot establish success.

On timeout, preserve pending; perform independent work and later collect. One read-only UI refresh/reselect is allowed, followed by fresh observation. Refresh is not send. Missing original baseline or unprovable delivery remains uncertain. Never silently rebind aliases or delete crash locks.

## Discover and download

Either worker may deliver structured inline results or one primary artifact/bundle according to actual provider capability and page state. DOT and Muse both historically delivered ZIPs; CSV/MD and inline also occurred. Inline is a reliable fallback for either, not Muse's permanent-only mode. The implementation's BUNDLE_FIRST/INLINE_FALLBACK preference labels are not provider capability limits. Discover only attachment locators scoped to the correlated reply:

```sh
python runtime/workflow.py discover --worker dot --observation sessions.local/observation.json
```

Observation includes the exact reply hash, actual artifact names and unique scoped targets. Prefer primary ZIP. Refresh discovery after UI changes before clicking. Generate a download plan with browser_plan.py `--run-id <id> --target <fresh target> --extension zip`. Pass its download_code to registered browser_run_code_unsafe. This narrow Playwright snippet checks exact URL/unique locator, waits for the download event and calls saveAs with a unique private filename. Suggested filenames never control local paths.

The snippet needs server filesystem access. If the remote server does not share local storage, report transfer missing and use inline fallback. A click/event/save return never proves local readable bytes. Reconcile uncertain download by checking the generated local destination before another click; do not blindly redownload.

## Local receipt and validation

```sh
python runtime/workflow.py ingest --worker dot --run-id <id> --source <actual local downloaded file>
```

ZIP contract: root manifest.json with run_id and files mapping every non-manifest archive-relative path to SHA-256; results.json or results.csv; summary.md. Ingest preserves original bytes, safely unpacks within private state, reads/parses, verifies binding/hashes, saves rows and receipt, and updates the shared bundle/row dedupe index only for validated results. Reject traversal/symlink/duplicate-name/size violations. Partial recovery preserves complete rows without accepting them into the validated index.

This new V3 contract is verified by local tests. Benchmark B retains four original ZIPs with hashes, including Muse's bundle; their list/members/nested manifests and BENCHB IDs differ. No blanket historical compatibility is established or tested in this closeout. See [source evidence](../../../docs/phase-closeout-20261006/SOURCES.md).

For inline fallback from either worker, copy the preserved reply.raw.txt **bytes** to a local .json and ingest with --inline. Do not reserialize JSON or translate LF/CRLF; exact correlated reply hash, matching run_id and nonempty real rows are required. No downloadable file is claimed. For malformed replies use reply.raw.txt and reply.parsed.json for correction. VALIDATED is package integrity, not proof of factual correctness.

Artifact stages are separate: worker declarations are DECLARED; observed correlated targets VISIBLE; copied local bytes DOWNLOADED; read/parsed files READ; nonempty results plus run binding/file integrity VALIDATED. Communication SUCCESS does not imply any artifact stage. Unsupported or malformed bytes remain preserved. Exact bundle hash and canonical whole-row JSON equality dedupe across workers; semantic/entity dedupe belongs to Codex.

## Continuation and context

Use continue with the same registered flags and fresh baseline. Refill before deep processing when the next independent task is clear; ingest an earlier run while the worker is busy on a new confirmed turn. Pending submission/reply blocks refill.

Save a compact capsule using workflow.py capsule --worker dot --source <local capsule.json>, with exactly goal, constraints, accepted_facts, artifact_refs. The record is coordinator-supplied and requires review; no automatic fact verification is claimed. On NEED_CONTEXT, review the capsule then send a bounded same-thread reminder. Browser thread is the semantic history; local records hold control truth and evidence pointers.

Codex owns lane scheduling, stop conditions and synthesis. DOT and Muse use independent alias locks; shared artifact index has its own ingest lock. Crash locks need explicit inspection. The Skill installs no scheduler/wake service.
