# Browser Worker V0 source notes

Five shallow clones were inspected separately from this repository on 2026-10-06. No external implementation is vendored or added as a dependency. These are mechanism references, not runtime endorsements.

| Reference and inspected revision | Mechanism adopted | Boundary |
|---|---|---|
| [codex-browser-bridge](https://github.com/DeliciousBuding/codex-browser-bridge/tree/c692fb017d79d458927c6a8e350dc2d06224d46e), `skills/codex-browser/SKILL.md` | Small AI-facing instructions above runtime tools; inspect/doctor before actions | Its 52-tool bridge and browser transport are not copied. |
| [browse_code](https://github.com/Dedeep007/browse_code/tree/c4002fc14096056f753a1d62083847fba5f5fd68), Chrome content script and server | Stop at the tool boundary, feed actual results back, periodically remind the model of instructions, then continue or summarize | No extension, shell tool suite or provider-specific injection copied. Its configurable context-refresh reminder is not implemented as an automatic injector in our V0. |
| [chatgpt-browser-agent](https://github.com/abdallhMoukdad/chatgpt-browser-agent/tree/5f193cc5a5055424978dd5bdfbf49fc38ad646e3), `agent.js`, `chatgpt.js`, MCP server | Same conversation continuation, real command/check feedback, bounded turns (`MAX_TURNS` is 20 there) | Our default 6/hard 20 turns are caller-driven. No autonomous RUN/FILE execution or Puppeteer dependency. |
| [Let My Agent Sleep](https://github.com/jaein4722/Let-My-Agent-Sleep/tree/41de2af3ca467f0d528e4fa316d97ef9f00e2e61), `docs/protocol.md` | Pending work means handoff rather than repetitive polling | V0 provides manual bounded collect, not its watcher/wake infrastructure. |
| [codex-resume-after-wait](https://github.com/zycccishere/codex-resume-after-wait/tree/5c1355d03b66aaf80c6fcaa346d309b141166d05), delivery-boundary README | Uncertain delivery cannot be automatically replayed | No app-server continuation infrastructure copied; preserve pending state and original correlation context. |

[OpenAI Agents SDK Sessions](https://openai.github.io/openai-agents-python/sessions/) distinguishes persistent conversation identity from individual runs and explains resuming with the same storage/session. We use that identity distinction only: the webpage retains semantic history, and local state retains control receipts/hashes. We do not install the SDK or claim its API sessions underlie DOT/Muse browser conversations.

Our [Skill](../skills/browser-worker/SKILL.md) therefore exposes inspect, ask, continue and collect; the existing PowerShell runtime remains the sole browser communication implementation. Collect uses persisted hashes and send time, never a copied transcript or automatic resend.
