# Historical Capability Superset Audit

This audit compares the capabilities that were actually exercised across PROJECT-WHEELS, Benchmark B, FOUR_TRACK, the 3-hour regression, Runtime V0, and Browser Worker Skill V0.

## Conclusion

The newest stack improved truthful state handling, session continuity, bounded retries, and coordinator behavior, but it did **not** preserve every capability previously exercised in the older browser workflow.

The most important regression is that the current Skill/Runtime path mainly supports message send/read/save, while earlier runs also exercised structured attachment discovery, browser download, local artifact reading, ZIP bundle handling, hashing, unpacking, deduplication, and refill-before-deep-processing.

New versions should therefore follow one rule:

> A new orchestration version is a capability superset of previously verified behavior unless a capability is explicitly deprecated with a reason.

## Historically exercised capabilities

| Capability | Historical evidence | Current Skill V0 |
| --- | --- | --- |
| Exact DOT/Muse thread control | PROJECT-WHEELS, Benchmark B, FOUR_TRACK, 3h regression | Present |
| Unique RUN_ID per task | PROJECT-WHEELS onward | Present |
| Filled vs sent distinction | B06 failure / later regression | Present |
| Correlated reply reading | FOUR_TRACK / regression | Present |
| Same-thread continuation | Historical browser threads | Present in wrapper, live unverified |
| Independent DOT/Muse lanes | PROJECT-WHEELS, Benchmark B, FOUR_TRACK | Not in Skill; coordinator concern |
| Refill before deep processing | Benchmark B / 3h regression | Not in Skill; coordinator concern |
| CSV/Markdown attachment discovery | PROJECT-WHEELS | Missing |
| Browser attachment download | PROJECT-WHEELS | Missing |
| Consolidated ZIP bundle download | Benchmark B | Missing |
| Local artifact read / parse | PROJECT-WHEELS, Benchmark B | Missing |
| SHA-256 duplicate bundle detection | Benchmark B | Missing |
| ZIP unpack + manifest/candidate parsing | Benchmark B | Missing |
| Inline fallback when download fails | Benchmark B protocol / Muse history | Missing |
| Preserve malformed raw output + partial parse | FOUR_TRACK | Missing |
| Local state vs page reconciliation | B07 / 3h regression | Partial |
| Context refresh after worker memory loss | 3h regression | Missing |
| Bounded control recovery | Historical runs | Partial |
| Downloads/local-read preflight | Benchmark B | Missing |
| Artifact timing / fetch timing | Benchmark B | Missing |

## Important transport finding

The historically successful live runs used the already-registered Playwright control surface visible to Codex.

Runtime V0 added a lower-level path:

Python wrapper → PowerShell runtime → custom HTTP/SSE MCP RPC.

That path is useful for local tests, standalone tooling, and diagnostics, but the first live Runtime V0 smoke hit a browser_tabs SSE timeout while the registered Playwright path had previously completed long real runs.

Therefore the next version should treat the registered Playwright tool path as the preferred live path when available, with the standalone RPC runtime as a supporting implementation rather than the sole live transport.

## Artifact workflow that must return

The previously exercised full worker loop was:

SEND → confirm → read response → fast triage → refill if independent → discover artifact → download one primary bundle → verify local file → hash → unpack/read → parse → dedupe → checkpoint → continue.

Worker reply, artifact visibility, artifact download, artifact read, and artifact validation are separate states.

A worker saying COMPLETE is not equivalent to receiving the expected artifact.

## Provider-specific behavior

DOT historically produced downloadable CSV/Markdown and later ZIP bundles reliably enough to support bundle-first handling.

Muse historically had more attachment-preview/download failures, so its robust path should keep a short structured inline fallback even when an attachment is requested.

The Skill should expose one uniform worker interface while allowing provider-specific adapters underneath.

## Scope boundary

Browser Worker Skill should own:
- worker alias and thread binding
- truthful send/reply state
- session continuity
- context capsule
- artifact discovery/fetch/read status
- limited reconciliation/recovery

The higher-level coordinator should own:
- long-running goal decomposition
- DOT/Muse lane scheduling
- refill-first policy
- hourly QC
- saturation / stop conditions
- artifact-table synthesis
- wake/resume of the coordinator

## Next version

The next implementation version should be a **Full Workflow Browser Worker** rather than another narrower send/read wrapper.

Its acceptance target is not just ACK.

It should prove, with DOT and Muse separately:
1. live thread control;
2. multi-turn continuation;
3. structured result delivery;
4. artifact discovery or explicit inline fallback;
5. local acquisition/read;
6. no false success across message or artifact boundaries;
7. continued operation without losing historically verified capabilities.
