# Browser Worker — 阶段收尾入口

本页是 2026-10-06 阶段收尾，不是新的开发或运行指令。

**本阶段正式冻结。** 新接手者先读本页；没有用户明确重启请求，不开发 V4、不启动 live、不恢复历史测试计划。

| 状态 | 接手判断 |
|---|---|
| WHAT IS REAL | 旧 registered Playwright 跑过 DOT + Muse、多轮、ZIP 交付、本地读取；CSV、MD、inline fallback 也真实出现过。 |
| WHAT IS IMPLEMENTED | Browser Worker 3.0.0 的本地实现与测试已提交。 |
| WHAT IS NOT PROVEN | V3 provider-live full workflow、旧 ZIP 与新合同的兼容、是否减少用户操作。 |
| WHAT IS CURRENT | 暂停扩功能与新 live；文档收口不改变技术实现。 |
| WHAT IS NEXT | 仅在用户明确重启后，执行一次短、有界的真实 full-workflow user journey。 |

**技术基线：`f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a`，代码内版本名 Browser Worker 3.0.0。当前选择：暂停功能扩张，有条件保留下一次真实验证。** 后续文档提交不改变技术基线，也不表示 V3 live 已通过。

## 先读这三项

- [阶段复盘与判断](REPORT.md)：起点、弯路、经验、外部参照和继续条件。
- [当前状态与剩余接缝](STATE_AND_GAPS.md)：历史能力、V3 本地能力和 live 边界。
- [三小时协调行为回归增量](../../experiments/regression/20261006_3H_COORDINATOR_SUMMARY.md)：16:12–19:12 的结果，不是 V3 live 结果。

[来源与核对范围](SOURCES.md)提供文件哈希和外部参考。原 [V3 证据](../BROWSER_WORKER_V3_EVIDENCE.md)保留其测试口径。

## 什么已经真实发生

旧方法通过注册 Playwright 管理 DOT/Muse，完成过多轮任务、文件取件和本地读取；DOT 和 Muse 都成功交付过 ZIP。Benchmark B 留有四个 ZIP、三种字节内容及 hash 证据；两份 DOT R2 包相同。上一轮阶段审计重新读取 ZIP 并核对字节，本轮只对齐文档，没有重新运行 worker 或重审原包。

下午旧协调方法的三小时回归完成，B07 三条正文追回，当前记录 74（A13/B15/C28/D18）。原八小时窗口 69、B06 补收后 71 都保留为历史口径。自然控制断线恢复仍未验证。

V3 的代码和本地测试报告已经提交。该报告记录 42 Python 测试、10 PowerShell 检查通过；本次阶段核对重算了技术基线的 86 个公开文件哈希并静态核对测试数量，没有重跑 42 测试。V3 全部 provider live 流程仍为 NOT_RUN。

## 接手时避免混淆

1. `docs/CURRENT_STATE.md` 和原 regression README 属于 14:02 的冻结，不是下午最终状态。
2. V3 文档推荐 registered，但 wrapper 缺省 `--transport` 仍为 standalone。registered 的 ask 返回 PREPARED；实际浏览器调用仍由 Codex 发起。参见[完整协议](../../skills/browser-worker/references/full-workflow.md)。
3. 旧包格式与 V3 新合同不同；本地 ZIP 测试通过不证明全部历史包直接兼容。
4. 浏览器工具宿主的下载路径，不自动等于协调端能读取的本地字节。
5. `skills/browser-worker/` 是源码入口；宿主 Skill 发现、独立安装与新人使用仍未验收。
6. worker 可交付 structured inline result 或一个主要 artifact/bundle，取决于当时真实能力和页面状态。inline 是可靠 fallback，不是 Muse 的永久唯一模式。
7. ONE_HOUR_SINGLE_WORKER_TRIAL 与早期 ACK smoke 是保留的历史测试设计/diagnostic asset，不是下一位接手者必须自动执行的顺序。

推荐 live 路径为 registered Playwright：Browser Worker 准备 RUN_ID、状态和收件逻辑；Codex 用自己已注册的 Playwright 工具执行浏览器操作，再交回实际观察。它不是 Python wrapper 自动调用的原子 MCP 工具。standalone 只保留为 diagnostic、local test 或明确选择的 standalone usage；缺省参数仍走 standalone，属于未改动的技术基线。

## 保留的版本

- `v0.1-freeze-2026-10-06` → `01e33da…`：原始研究/历史冻结。
- `v0.2-runtime-local-pass-2026-10-06` → `b14ef92…`：Skill 化前 runtime 本地通过基线。
- `f8dcb4b…`：本次核对的 V3 技术实现；不是新的 stable release 承诺。

旧 ZIP、事件、原回归报告、源码和历史标签应保留。私人线程、登录态和原始会话继续只留私有存储。

## 以后重新启动时

先由用户明确决定再验证，而不是恢复全部 TODO。第一件事应是核对当前宿主、调用路径与文件可达性，再用一个小而真实的任务比较旧路径与新 Skill。两个 worker 都在最终验证范围内，测试顺序可按环境安排。记录实际交付、同线程定向修改和人工介入，不以跑满时长或测试数量替代可用性。

当前下一次验证目标仅为：**任务 → DOT/Muse → 真实回复 → artifact 或 inline delivery → 本地真正可读 → Codex 理解结果 → 同线程定向修改 → 最终交付。** 预先约定有限回合与停止条件，交付完成即可停止，不要求 ACK→一小时。

记录 human interventions、manual clicks、copy/paste、rescue events 的次数与原因，artifact actually received/read、context continuity，以及相比旧 Playwright 手工协调是否减少用户主动操作。没测到的项目记 UNKNOWN，不用运行时长代替收益证据。

本交接不授权自动开发、部署、push/merge、移动标签、删除原件、重启浏览器或启动长跑。历史未完成计划不自动成为新任务。
