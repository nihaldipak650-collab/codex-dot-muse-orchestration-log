# Codex / DOT / Muse：工程与研究冻结快照

这是 engineering/research log。目标是保存多阶段长程协调的真实文件、演化与失败，支持审计和恢复，不将候选发现写成实测产品。

1. **项目是什么？** Codex总控两条独立worker lane（DOT、Muse），以RUN_ID、工件和本地ledger管理资源发现及四轨研究。
2. **为什么开始？** 在文献助手、动画、游戏、网站、科研SOP五个真实项目方向找可复用资源，再研究学习与Agent工作组织；源任务动机见ORCHESTRATOR_CONTEXT。更早V0的完整操作史UNKNOWN。
3. **真实跑过什么？** V1保存100候选；V2正式100后扩到221；26h文件跨度复盘；90m Benchmark B；正式8h FOUR_TRACK；B06/B07恢复与审计；独立8h文献研究；当前regression。
4. **证明了什么？** 本地ledger计数与工件存在；Benchmark重复ZIP字节相同；B06填入/提交混淆可由原始工具记录定位。这里只证明局部事实。
5. **没证明什么？** 候选有效性、稳定2.3x提速、通用学习迁移效果、所有71条全量核验、B07当前结果、补丁长期可靠性。
6. **最大失败？** 正式100后继续至221且无储备上限；B06未提交却长期WAITING；B07重复轮询后以checkpoint自行收尾。
7. **当前调度原则？** LONG_RUN_PATCH_V2：progress-first、lane独立、refill-first、有限重试、等待时独立工作、每小时轻QC、checkpoint≠结束、饱和后综合。
8. **怎么复现/继续？** 先按哈希验证本地快照，读handoff与未决项；下一轮需授权控制、定义单worker baseline与验收指标。本归档不发送任何worker消息。

证据分级：CONFIRMED=本次核对本地原始记录/工件；REPORTED=既有Agent或worker报告，未独立复核；INFERENCE=基于证据的解释；UNKNOWN=现有证据不能确定。文件存在、Agent声称完成、结构检查通过均不等于内容正确或运行验收通过。

采集阶段：final；截止：2026-10-06T14:02:51.194154+08:00（Asia/Shanghai）。
regression状态（源状态文件）：INVALIDATED_PREFLIGHT_NOT_CONFIRMED；run_id=REGRESSION-20261006-131237。
REPORTED：原13:12:37起点已invalidated=True；actual_start_utc=None，actual_hard_stop_utc=None。原16:12:37不得当新回归截止。
REPORTED：运行Agent在14:01记录读到B07的11:53回复元数据，worker自报研究COMPLETE、保留A1/B2，但实际items交付0；本Archivist只核对保存元数据，未看在线页面。
本版本是**截至截止时间的冻结**。如果regression仍在运行，后续结果不包含在此截止包内；二次扫描符合用户允许的“最终阶段时”扫描，不表示等待完整回归结束。

阅读顺序：[时间线](docs/TIMELINE.md) → [当前状态](docs/CURRENT_STATE.md) → [失败](docs/FAILURE_MODES.md) → [安全](docs/SECURITY_REDACTION_REPORT.md) → [交接](docs/NEXT_STEPS.md)。

本地原件在source_snapshots；09_ARTIFACT_INDEX.csv定位每次采集及类别副本，10_FILE_HASHES.sha256校验冻结目录文件（排除哈希清单自身和.git）。GitHub只上传github_safe，不上传本地整个冻结目录。

公开副本不包含source_snapshots；文中的archive证据路径用docs/ARCHIVE_INDEX.csv匹配原件哈希与本地冻结路径。原件仅本地可得，未上传下载端点。恢复步骤需本地完整包。
