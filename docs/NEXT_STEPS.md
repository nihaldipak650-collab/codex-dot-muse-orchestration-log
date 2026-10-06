# 下一Agent交接（只读归档→后续授权执行）

1. 先读00/01/03/05/08与14_FREEZE_MANIFEST。核对10_FILE_HASHES.sha256，不把状态字样当结果。
2. 本包截止2026-10-06T14:02:51.194154+08:00，regression源状态INVALIDATED_PREFLIGHT_NOT_CONFIRMED。REPORTED：原13:12:37起点已invalidated=True；actual_start_utc=None，actual_hard_stop_utc=None。原16:12:37不得当新回归截止。 原目录仍可能变化；不要把快照称为最新在线状态。REPORTED：运行Agent在14:01记录读到B07的11:53回复元数据，worker自报研究COMPLETE、保留A1/B2，但实际items交付0；本Archivist只核对保存元数据，未看在线页面。
3. 本Archivist没有控制DOT/Muse或修改任何源项目。下一Agent未经另行授权不要向worker发消息、改prompt、创建batch、修Playwright或修改运行日志。
4. 如需完整regression归档：先只读检查REGRESSION_RUN_REPORT.md、EVENTS尾、STATE.regression_run、worker_outputs/ledger/checkpoints/B07；在新snapshot stage中捕获增量，保留working/final；比较新增/修改/删除与EVENTS行数、ledger行数，更新索引与hashes。不要覆盖旧快照。
5. 如获准继续研究/实验：定义新窗口、目标与验收；原8h69、postrun71分别保留；先收实际B07回复并核对而非盲重发。Muse原12批限额仍是历史授权边界，不能自动扩批。
6. 学校/比赛只做个人资格与当前官方窗口核查后再行动。补丁/研究建议不授权报名、付款、发布。
7. 下一benchmark需单worker baseline、FIRST_RESULT_VISIBLE、SEND、REFILL、coordinator工作/worker等待、GUI动作计时与artifact hash；多次可比运行才评估提速。
8. GitHub只使用github_safe；原件含session/私有线程/个人资料，不能整目录上传。repo建议codex-dot-muse-orchestration-log；tag建议v0.1-freeze-2026-10-06。尚未确认远端地址，不push、不创建public repo、不发布Release。
9. 本地恢复只复制到新的工作目录，保留原snapshot；外部research-cache按attachment_index映射重建。完整多任务Codex会话不在包内，只有明确引用的项目原行；需更多证据先限定项目范围。

审计定位：09_ARTIFACT_INDEX.csv；logs/attachment_index.csv；logs/session_excerpt_provenance.json；logs/final_delta.json；reports/FAILURE_CATALOG.csv；reports/DETERMINISTIC_VERIFICATION.json。
