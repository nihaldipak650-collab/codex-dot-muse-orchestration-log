# 从最早现存证据到本次截止的时间线

证据分级：CONFIRMED=本次核对本地原始记录/工件；REPORTED=既有Agent或worker报告，未独立复核；INFERENCE=基于证据的解释；UNKNOWN=现有证据不能确定。文件存在、Agent声称完成、结构检查通过均不等于内容正确或运行验收通过。

|阶段|时间 / 边界|事实与证据|分类 / 限制|
|---|---|---|---|
|V0 人工复制/微操作|早于V2；准确起止UNKNOWN|后续复盘描述旧交互；缺少独立V0完整运行包|REPORTED，不能构造未保存实验|
|Phase1 V1|早于2026-10-04 V2|`source_snapshots/final/project-wheels/V1_PROJECT_WHEELS_100_LEDGER.csv`有100行|CONFIRMED行数；部分表头已乱码，不修写原件|
|Phase1 V2|10-04 14:14启动说明，15:22首非说明工件|`source_snapshots/final/project-wheels/00_START_HERE.md`与ORCHESTRATOR_CONTEXT：五方向，各20；DOT偏GitHub，Muse偏X/YouTube，具体按批次任务|CONFIRMED任务约定；未等于执行效果|
|正式100→reserve→221|10-04至10-05|02_BATCH_LOG记录正式配额100；主表232行，其中207普通+14 reserve=221 countable；11非计入|CONFIRMED表计数；候选全未实测；继续reserve曾获授权，失误是缺上限|
|Phase2 26小时审计|10-04 14:14:27→10-05 16:15:54=26:01:27|`source_snapshots/final/project-wheels/ORCHESTRATOR_POSTMORTEM_20261005.md`，raw及06_AGENT_RUNS；DOT B09 12:04:01→B10 13:22:53=78:52|REPORTED历史重建；活动6–10h低置信，文件活动窗口≠专注工时|
|Phase3 Benchmark B|10-05 22:31:43.7297116→10-06 00:01:43.7297116，90m|`source_snapshots/final/benchmark-b/04_BENCH_B_RESULT.md`与events、ZIP、staging：Muse4轮；DOT R1/R2；29 unique|CONFIRMED表/ZIP核对；窗口及控制报告REPORTED；不能宣称稳定2.3x|
|Phase4 FOUR_TRACK正式8h|10-06 01:30:57→09:30:57，checkpoint09:31:08|`source_snapshots/final/four-track-8h/12_OVERNIGHT_RUN_REPORT.md`：Muse12批46条；DOT B01–B05 23；B06当时未提交；69=61+8 raw|REPORTED正式窗口重建；当前表不能直接替代历史窗口|
|Phase5 B06恢复|10:42:06提交；10:46:23看到回复；约10:50落盘|AUDIT_POSTRUN_50MIN和source_snapshots/attachments/session-cited-lines.jsonl原行24967/25058/25128|CONFIRMED原行时间；10:58为后续记账，非首次回复|
|Phase5 B07|11:06:07真正提交；11:10后高频wait/poll；11:32收尾|同审计原行25381及动作表；截至该历史审计无B07 RESULT|CONFIRMED工具记录；最新回复与交付分开见Phase8|
|Phase6 Audit/Repair|11:32后审计、V1/V2补丁；约12:31旧raw恢复|AUDIT_POSTRUN_50MIN：89动作；LONG_RUN_PATCH_V1/V2；恢复输出与checkpoint备份|CONFIRMED文档与可解析输出；补丁建议≠验收成功|
|Phase7 独立Research Agent|01:31–09:31扩搜，之后检查交付|`source_snapshots/final/research-report/AI_PROJECT_AND_AGENT_RESEARCH_REPORT.md`，AI_RESEARCH目录；30核心案例/10部分|CONFIRMED报告结构；不是DOT/Muse orchestration run；案例内容不在此次全量外部复验|
|Phase8 Regression|旧13:12:37计时与16:12:37计划；最新源状态INVALIDATED_PREFLIGHT_NOT_CONFIRMED|logs/WORKER_STATE.regression_run、最新EVENTS、REGRESSION_*工件|本次截止2026-10-06T14:02:51.194154+08:00；REPORTED：原13:12:37起点已invalidated=True；actual_start_utc=None，actual_hard_stop_utc=None。原16:12:37不得当新回归截止。|

最新B07：REPORTED：运行Agent在14:01记录读到B07的11:53回复元数据，worker自报研究COMPLETE、保留A1/B2，但实际items交付0；本Archivist只核对保存元数据，未看在线页面。 证据：worker_outputs/REGRESSION_B07_OBSERVED_STATUS.json与EVENTS的RESET_B07_REAL_REPLY_OBSERVED。原始回复未作为实际候选交付，ledger仍71。

三个任务边界：历史Codex→DOT/Muse协调实验；独立文献Research Agent（不是协调器）；新的regression续跑（独立run_id与窗口）。本Archivist是第四个只读归档角色。
更早V0精确记录及原V1完整运行日志缺失；目前只能保存现存V1去重副本，不能声称无缺口全史。所有时间为+08:00，原UTC保留供重算。
