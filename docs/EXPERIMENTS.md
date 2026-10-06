# 实验与结果账

证据分级：CONFIRMED=本次核对本地原始记录/工件；REPORTED=既有Agent或worker报告，未独立复核；INFERENCE=基于证据的解释；UNKNOWN=现有证据不能确定。文件存在、Agent声称完成、结构检查通过均不等于内容正确或运行验收通过。

|运行|产物/计数|已确认 / 未确认|证据|
|---|---|---|---|
|V1|100行去重副本|CONFIRMED行数；原始V1全过程UNKNOWN|V1_PROJECT_WHEELS_100_LEDGER.csv|
|V2|正式100；全池221；主表232|CONFIRMED disposition 207+14；每方向正式20为REPORTED；所有候选不等于测试成功|01_MASTER_LEDGER.csv、02_BATCH_LOG、CURRENT_STATE、batches|
|26h复盘|26:01:27 wall span；活动窗口约10h54；active估计6–10h|REPORTED重建/INFERENCE活动估计；不能把文件空档视为一直工作|ORCHESTRATOR_POSTMORTEM、raw、06_AGENT_RUNS|
|B 90m|Muse4轮20 unique；DOT9；合计29|CONFIRMED表：35 reported rows→30实体→减1 V1重复=29；6 rejected包含5重复投递+1历史实体重复|03_BENCH_B_STAGING.csv与artifacts|
|B速度|29/1.5=19.33/h；A221/26.024=8.49/h|CONFIRMED算术；2.28x不同分母与样本，INFERENCE比较不能证明稳定提速；A估计active rate22.1–36.8/h不可靠|05_A_VS_B、01_BASELINE_A|
|FOUR_TRACK正式8h|Muse12批46条（38+8raw）；DOT5完成23；69=61+8|REPORTED历史口径；B06第6槽未提交；hard stop成功与内容未全验收同时成立|12_OVERNIGHT_RUN_REPORT、checkpoints、EVENTS|
|Postrun恢复|B06增加2B，71；后来8raw恢复、60字段映射修复|CONFIRMED当前表/恢复文件；60为恢复脚本报告，原始事实不变，不新增候选|reconcile_saved_outputs、RECOVERED JSON、旧checkpoint备份|
|B07|真正发送；89动作审计窗口；18 wait_for显式438s、29 evaluate|CONFIRMED审计动作表与抽取原行；不将438秒当全部等待或worker计算时间|AUDIT_POSTRUN_50MIN、session-cited-lines|
|独立研究|30核心案例（15学习/10Agent/5外部实验）、10部分，学习与Agent方法|CONFIRMED结构；外部内容真实性/因果效果仍按报告边界，未复跑外部benchmark|主报告、FINAL_STRUCTURAL_CHECK、FINAL_REPORT_INDEPENDENT_REVIEW|
|Regression|现有A/B/C/D核验、比较与综合工件；71记录未扩池|CONFIRMED采集工件；源状态INVALIDATED_PREFLIGHT_NOT_CONFIRMED；完整结束与B07回收UNKNOWN|最新STATE/EVENTS、REGRESSION_*；二次扫描差异见logs/final_delta.json|

ZIP去重独立计算写入reports/DETERMINISTIC_VERIFICATION.json。对公开源码的读取、PDF方法抽取、candidate discovery、运行实测分别保留边界。正式window结束后取回附件不延长Benchmark计时。
独立研究的方法核心：先单worker baseline，再按可测瓶颈加角色；保存artifact/state/输入版本/验收/stop condition。学习三项分别验收：产物、人能否判断纠错、新情境迁移；纯交付可以明记后两项非目标。
