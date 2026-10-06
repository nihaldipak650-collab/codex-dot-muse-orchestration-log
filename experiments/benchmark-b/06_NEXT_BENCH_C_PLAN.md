# Next Bench C Plan — Plan Only

Do not execute this plan as Benchmark C without an explicit new start request. Keep the same isolated benchmark root and preserve the formal V2 workspace.

## Goal
Resolve the distinction between the host-connected Playwright Extension session and a separately initialized HTTP MCP session. The current helper can negotiate a session, but calls on that session do not return an SSE result. The current app-side diagnostic exposed DOT_WORKER only, while the user-confirmed Chrome state is Muse plus DOT_WORKER.

## Preflight sequence
1. Keep the existing Playwright Extension and http://localhost:8931/mcp; do not use CDP or In-App Browser.
2. Establish one session that is actually bound to the connected extension, then prove tools/list and browser_tabs list return promptly. Preserve that session for every action; do not create a fresh MCP session per request.
3. HEALTH must show the exact Muse URL and title Chat — MUSE_WORKER, and the exact DOT URL and title DOT_WORKER. If either is missing, use the existing extension MCP to restore only that exact URL and re-run HEALTH.
4. Prove SEND/POLL/FETCH_BUNDLE with a unique, harmless preflight RUN_ID and one tiny response bundle. Do not include that smoke result in the 40-lead total.
5. Validate the high-level action wrapper end-to-end. If a standalone HTTP client cannot share the host-connected extension session, use a supported shared-session configuration for the already-running Playwright MCP rather than opening parallel extension relays.
6. Only after every check passes, record a fresh BENCHMARK_START_TIME and begin the same four-round/two-lane Benchmark B protocol. Keep REFILL FIRST, FAST_TRIAGE within 30–90 seconds, and the 40-candidate / 90-minute / recovery stop rules.

## Preserve
- Keep all new benchmark artifacts under this directory.
- Keep V1_PROJECT_WHEELS_100_LEDGER.csv read-only and use it only for canonical dedupe.
- Do not send additional resources, alter formal counts, or create scheduled automation during preflight.
