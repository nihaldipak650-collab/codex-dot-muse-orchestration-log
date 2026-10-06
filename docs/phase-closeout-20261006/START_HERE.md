# Browser Worker — 阶段收尾入口

本页是 2026-10-06 阶段收尾，不是新的开发或运行指令。

**技术基线：`f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a`，代码内版本名 Browser Worker 3.0.0。当前选择：暂停功能扩张，有条件保留下一次真实验证。** 后续文档提交不改变技术基线，也不表示 V3 live 已通过。

## 先读这三项

- [阶段复盘与判断](REPORT.md)：起点、弯路、经验、外部参照和继续条件。
- [当前状态与剩余接缝](STATE_AND_GAPS.md)：历史能力、V3 本地能力和 live 边界。
- [三小时协调行为回归增量](../../experiments/regression/20261006_3H_COORDINATOR_SUMMARY.md)：16:12–19:12 的结果，不是 V3 live 结果。

[来源与核对范围](SOURCES.md)提供文件哈希和外部参考。原 [V3 证据](../BROWSER_WORKER_V3_EVIDENCE.md)保留其测试口径。

## 什么已经真实发生

旧方法通过注册 Playwright 管理 DOT/Muse，完成过多轮任务、文件取件和本地读取。Benchmark B 留有四个 ZIP、三种字节内容；两份 DOT R2 包相同。本次重新读取 ZIP 并核对字节，没有重新运行 worker。

下午旧协调方法的三小时回归完成，B07 三条正文追回，当前记录 74（A13/B15/C28/D18）。原八小时窗口 69、B06 补收后 71 都保留为历史口径。自然控制断线恢复仍未验证。

V3 的代码和本地测试报告已经提交。该报告记录 42 Python 测试、10 PowerShell 检查通过；本次阶段核对重算了技术基线的 86 个公开文件哈希并静态核对测试数量，没有重跑 42 测试。V3 全部 provider live 流程仍为 NOT_RUN。

## 接手时避免混淆

1. `docs/CURRENT_STATE.md` 和原 regression README 属于 14:02 的冻结，不是下午最终状态。
2. V3 文档推荐 registered，但 wrapper 缺省 `--transport` 仍为 standalone。registered 的 ask 返回 PREPARED；实际浏览器调用仍由 Codex 发起。参见[完整协议](../../skills/browser-worker/references/full-workflow.md)。
3. 旧包格式与 V3 新合同不同；本地 ZIP 测试通过不证明全部历史包直接兼容。
4. 浏览器工具宿主的下载路径，不自动等于协调端能读取的本地字节。
5. `skills/browser-worker/` 是源码入口；宿主 Skill 发现、独立安装与新人使用仍未验收。

## 保留的版本

- `v0.1-freeze-2026-10-06` → `01e33da…`：原始研究/历史冻结。
- `v0.2-runtime-local-pass-2026-10-06` → `b14ef92…`：Skill 化前 runtime 本地通过基线。
- `f8dcb4b…`：本次核对的 V3 技术实现；不是新的 stable release 承诺。

旧 ZIP、事件、原回归报告、源码和历史标签应保留。私人线程、登录态和原始会话继续只留私有存储。

## 以后重新启动时

先由用户明确决定再验证，而不是恢复全部 TODO。第一件事应是核对当前宿主、调用路径与文件可达性，再用一个小而真实的任务比较旧路径与新 Skill。两个 worker 都在最终验证范围内，测试顺序可按环境安排。记录实际交付、同线程定向修改和人工介入，不以跑满时长或测试数量替代可用性。

本交接不授权自动开发、部署、push/merge、移动标签、删除原件、重启浏览器或启动长跑。历史未完成计划不自动成为新任务。
