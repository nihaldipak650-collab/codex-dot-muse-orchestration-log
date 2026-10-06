# 来源、核对范围与未取得材料

核对日期2026-10-06；技术源码固定到 `f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a`。公开摘要不附私人路径、线程、账号、原始聊天或完整研究台账。哈希用于定位原件字节，不等于授权分发或事实正确。

## 本地/公开项目证据

- **R01** `ORCHESTRATOR_POSTMORTEM_20261005.md`，200行历史postmortem；当前字节核对，内容在本项目上下文中已读取。SHA `e8c8b632473f7ffe441f8ebee0f565a0cfe23fa0d9c80c776db62fd613d5b588`。公开对应入口：[Wheels复盘](../../experiments/project-wheels/ORCHESTRATOR_POSTMORTEM_20261005.md)。
- **R02** `04_BENCH_B_RESULT.md`，本轮完整读取54行；SHA `82c0401beccbbb24b42f603d201336d688c267b6d8a7b874c309555b39e1d833`。[公开结果](../../experiments/benchmark-b/04_BENCH_B_RESULT.md)。其中下载时点总括有误，纠正见下。
- **R03** `02_BENCH_B_EVENTS.jsonl`，本輪定向读取download/fetch/stop/reconcile等事件，而非重新审核全部67行；SHA `19f60c8326cc57d37e86b739025063b0f23e1a952d4148b478e270c7e8716fbc`。原件私有。
- **R04** `12_OVERNIGHT_RUN_REPORT.md`，完整读取52行；SHA `5d805bca934135925c0d6e6e5a2d6fe9a23506ff0624f0f768695789305d84d4`。历史八小时口径，不替代下午回归。
- **R05** `AUDIT_POSTRUN_50MIN.md`，89动作历史审计；当前存在/hash已核，正文此前已读；SHA `4f3be1b4d6017c4e92e9885b07685e6e13067a6c0b60d59d076b23f58f085118`。[公开对应审计](../../experiments/postrun/AUDIT_POSTRUN_50MIN.md)。
- **R06** `REGRESSION_RUN_REPORT.md`，完整读取83行；SHA `99f094fe6ca0cbf88fd4978940e00771f3049004c53a02feced9828bfc68de3b`。本次补入[脱敏汇总](../../experiments/regression/20261006_3H_COORDINATOR_SUMMARY.md)，不上传全部私人运行材料。
- **R07** `09_EVIDENCE_LEDGER.csv`，本轮重数74条、A13/B15/C28/D18；SHA `d97331b32be7a4f96deb7651b0c726b84f293d6b378fc91203ee82c4188765ce`。未重新验证每条研究断言。
- **R08** `20_DECISION_READOUT.md`，当前字节核对、正文此前读过；SHA `2222d4374e5e88c8eec9a093e0ce54122007244571de07d64028b45ea54876e8`。
- **R09** `01_PROJECT_TIMELINE.md`，本轮完整读取23行冻结时间线；SHA `b6c09479b55bbc1caaad724199bbfa6aab4d259edd04524ae63cb1a39af34fb1`。
- **R10** `LONG_RUN_PATCH_V2.md`，历史progress-first规则，当前字节核对；SHA `4df3f0ace070a58ed6e13c779f20aa9989d35b81d9f49c3a2ee9e068dad29d54`。低风险有界补交与盲重放不是一回事。
- **R11** `AI_PROJECT_AND_AGENT_RESEARCH_REPORT.md`，原件150866字节/952行，10部分30具名案例标题核对；SHA `dbafe4523ca8ed7eba45f56e93df3a9f141215a220e49623fdb48c41e1b80475`。不是本轮全文重审。[公开研究副本入口](../../research/AI_PROJECT_AND_AGENT_RESEARCH_REPORT.md)。
- **R12** Library中此前`REPORT.md`全文读取，截止01:39:44；只能证明旧阶段认识，不是V3现状。未公开此私人Library条目。
- **R13** 当前Git/元数据：本地HEAD与`ls-remote main`一致，两标签目标一致，核对起点工作区干净；86个清单hash重新计算匹配，42个Python测试函数静态计数。没有重跑42个测试。
- **V3 evidence/source**：固定提交中的[证据说明](https://github.com/nihaldipak650-collab/codex-dot-muse-orchestration-log/blob/f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a/docs/BROWSER_WORKER_V3_EVIDENCE.md)、[wrapper](https://github.com/nihaldipak650-collab/codex-dot-muse-orchestration-log/blob/f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a/skills/browser-worker/scripts/worker.py)、[workflow](https://github.com/nihaldipak650-collab/codex-dot-muse-orchestration-log/blob/f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a/runtime/workflow.py)、[browser plan](https://github.com/nihaldipak650-collab/codex-dot-muse-orchestration-log/blob/f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a/runtime/browser_plan.py)、README、SKILL及完整协议。本轮静态读取，不是live。

## 历史ZIP字节（原包不随本次文档上传）

| 编号 | 文件 | 字节 | SHA-256 |
|---|---|---:|---|
| Z01 | BENCHB-DOT-R1_RESULT.zip | 3681 | `6ad6ebafc5c0896edd28a82d853e7b6fea0921b635dd47897f470706ace06b94` |
| Z02 | BENCHB-DOT-R2_RESULT.zip，delivery-01 | 5394 | `969911d807eda64ffd05bd36d526e770217e3311bbc626668a2228ccdbad1ede` |
| Z03 | BENCHB-DOT-R2_RESULT (1).zip，delivery-02 | 5394 | `969911d807eda64ffd05bd36d526e770217e3311bbc626668a2228ccdbad1ede` |
| Z04 | BENCHB-MUSE-R1-R4_FETCH.zip | 16152 | `53561a7cc5d134c1024b130025b828890ad59110537bda15de364cc4a2b423f6` |

四包本轮重新打开、CRC读取检查通过。Z02/Z03字节相同。Z01的manifest.files是列表；Z02使用members与sha256；Z04有四个嵌套轮次与FETCH_MANIFEST.json。以上是历史字节与V3合同的静态比较，不是重跑了新版旧包兼容测试。

### Benchmark B下载时点纠正

90分钟窗口从北京时间10月5日22:31:43.7297116至10月6日00:01:43.7297116。R03记录Muse包23:13:05下载，23:18:29有取件记录，发生在窗口内；DOT三份在00:10:01、00:11:59、00:14:18下载，在窗口外。因此R02中“所有附件都在窗口后取回”的表述不准确。

最终去重时间00:27:05.510，距开始约115分22秒。29/90分钟=19.3条/小时仅是原派单窗口口径；计入这段收件/对账则约15.1条/小时。两者都不是经过同任务多次受控比较的稳定提效。纠正保留为新记录，不移动冻结标签。

## 外部来源与本轮用途

所有外部条目均为候选参考/规范依据；本轮没有安装、启动或复现其系统。网页抓取可能有缓存，不把取到的README当保证最新发行版。

- **E01** [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)：官方正文，脚本可选、instruction-only、技能发现。用于纠正“Skill必须自带runtime”。
- **E02** [OpenAI Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)：官方页面取得；仅作为从示范提炼Skill的候选，未在用户机器试用。
- **E03** [Playwright扩展官方README](https://github.com/microsoft/playwright/blob/main/packages/extension/README.md)：client/tab group、首次授权、profile；不是本机根因诊断。
- **E04** [Playwright Download API](https://playwright.dev/docs/api/class-download)：download事件、saveAs、path与流；未执行下载实验。
- **E05** [MCP 2025-11-25 transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)：响应、断连、session与恢复语义；未做协议一致性测试。
- **E06** [Browse Code](https://github.com/Dedeep007/browse_code)：README与既有关键源码线索，网页工具反馈循环；未运行。
- **E07** [chatgpt-browser-agent](https://github.com/abdallhMoukdad/chatgpt-browser-agent)：README及agent-loop；同线程接续。自动shell等默认不适合照搬。
- **E08** [agent-mcp](https://github.com/Aphelion-Development/agent-mcp)：正文/已知状态披露；共识启发式和未完成人工resume为反例。
- **E09** [Playwriter](https://github.com/remorses/playwriter)：README、有状态批量操作与CLI/MCP；未迁移或安装。
- **E10** [Agents SDK Sessions](https://openai.github.io/openai-agents-python/sessions/)：官方会话接续与状态；SDK不是网页线程的直接替代。
- **E11** [Let My Agent Sleep](https://github.com/jaein4722/Let-My-Agent-Sleep)：正文；本地长任务handoff/完成后唤醒，平台条件需另外验证。
- **E12** [codex-resume-after-wait](https://github.com/zycccishere/codex-resume-after-wait)：正文；owner与不确定投递，未安装。
- **E13** [Anthropic长任务harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)：作者工程复盘；增量工作/交接，不是本项目性能证据。
- **E14** [A2A Life of a Task](https://a2a-protocol.org/latest/topics/life-of-a-task/)：官方协议，任务/消息/产物概念；不证明DOT/Muse支持。
- **E15** [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)：一手摘要/版本页；MAST分类参照，未阅读全文或复现实验。
- **E16** [GitHub Licensing](https://docs.github.com/en/enterprise-cloud%40latest/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)：官方许可说明；未替拥有者选许可证。
- **E17** [OpenAI Terms](https://openai.com/policies/terms-of-use/)：取到页面标题为Europe Terms of Use；存在自动提取/绕限制约，不能据此替用户判定具体适用条款或代替Muse条款。
- **E18** [Show HN Playwriter](https://news.ycombinator.com/item?id=46068108)：作者/社区文本，不是独立受控效率测试。
- **E19** [Bilibili演示入口](https://www.bilibili.com/video/BV1fojq62ELr/)：仅标题/描述；未完整取得视频/字幕，技术结论不依赖它。
- **E20** [Playwright MCP issue1571](https://github.com/microsoft/playwright-mcp/issues/1571)、**E21** [Playwright issue41916](https://github.com/microsoft/playwright/issues/41916)：相似连接/profile症状入口，未在本机复现。
- **E22** [codex-browser-bridge](https://github.com/DeliciousBuding/codex-browser-bridge)：此前Skill/MCP源码研究保留，本轮核到参考clone；未替换现有控制路径。

## 已有五个参考clone的固定点

browse_code `c4002fc14096056f753a1d62083847fba5f5fd68`；chatgpt-browser-agent `5f193cc5a5055424978dd5bdfbf49fc38ad646e3`；codex-browser-bridge `c692fb017d79d458927c6a8e350dc2d06224d46e`；LMAS `41de2af3ca467f0d528e4fa316d97ef9f00e2e61`；codex-resume-after-wait `5c1355d03b66aaf80c6fcaa346d309b141166d05`。源码副本存在不表示依赖已接入或live通过。

## 未取得与边界

X/YouTube定向检索未取得足以支撑升级结论的一手完整内容；B站仅入口；Discord未取得可靠相关公开线程。没有全量Library盘点或所有历史聊天导出，没有早期V0完整独立日志，没有本项目外部用户低介入成功记录。没有把这些缺口用搜索摘要补成事实。
