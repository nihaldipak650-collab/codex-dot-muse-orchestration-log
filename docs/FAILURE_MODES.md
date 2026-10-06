# 失败与风险案例目录

证据分级：CONFIRMED=本次核对本地原始记录/工件；REPORTED=既有Agent或worker报告，未独立复核；INFERENCE=基于证据的解释；UNKNOWN=现有证据不能确定。文件存在、Agent声称完成、结构检查通过均不等于内容正确或运行验收通过。
“Confirmed failures”文件同时保存尚未确认的风险案例；请按EVIDENCE_STATUS判断。F06–F08不虚构已证明根因或Muse故障。

完整字段见[FAILURE_CATALOG.csv](FAILURE_CATALOG.csv)。

|ID|上下文 / 发生了什么|证据级别|修复状态 / regression|
|---|---|---|---|
|F01|V2 quota：formal100→221；reserve无界|CONFIRMED_COUNT|DOCUMENTED_NOT_VALIDATED / UNKNOWN|
|F02|DOT B09：12:04:01结果→13:22:53续发，78:52 bubble|REPORTED_RECONSTRUCTION|DOCUMENTED / UNKNOWN|
|F03|browser：539 raw操作文件，多find/snapshot/select|CONFIRMED_ARTIFACTS|DOCUMENTED / UNKNOWN|
|F04|bookkeeping：深整理与多文件同步在refill前|REPORTED|DOCUMENTED / UNKNOWN|
|F05|attachments：Muse B10 CSV无数据显示/下载失败，缺直链|REPORTED|UNRESOLVED / NO|
|F06|MCP/session：旧helper会话与实际Remote连通状态不一致|REPORTED_NOT_ROOT_CAUSE_CONFIRMED|DOCUMENTED / UNKNOWN|
|F07|tab health：helper/tab missing被过度外推CONTROL_DOWN|INFERENCE_CLASSIFICATION|CORRECTED_REPORT / LIMITED_B_RUN|
|F08|Muse vs control：APP_DOWN与Playwright CONTROL_DOWN区分不足|UNKNOWN_SPECIFIC_INCIDENT|DOCUMENTED / UNKNOWN|
|F09|DOT R2：timeout→retry→两份相同ZIP|CONFIRMED|DEDUPE_CONFIRMED / ZIP_ONLY|
|F10|DOT B06：composer填入未submit却长期WAITING；prompt COMPLETE误命中|CONFIRMED|RECOVERY_CONFIRMED / V2_LONGRUN_UNKNOWN|
|F11|DOT B07：已送达后高频poll；11:32写完state自行结束|CONFIRMED_ACTIONS_INFERENCE_CAUSE|DOCUMENTED_REGRESSION_RUNNING / PENDING|
|F12|resume/regression control：两次300s tools/call timeout期间不取到B07|REPORTED|LOCAL_PROGRESS_CAPTURED / PARTIAL_REPORTED|
|F13|Muse B03/B06：8 raw malformed/unparsed JSON|CONFIRMED_SAVED_RAW|RECOVERED_8_CURRENT_71 / LOCAL_PARSING_ONLY|
|F14|stale state：旧WAITING/学校19比赛12/B06 10:58被继承|CONFIRMED_CONFLICT|ANNOTATED_IN_FREEZE / PENDING|
|F15|benchmark measurement：缺first-visible/send、refill/GUI统一测量|CONFIRMED_REPORT_LIMIT|PLAN_ONLY / NO|

B06时间必须采用10:46:23首次回复可见、约10:50落盘；10:58仅是后续记账。B07确实提交，错误主要在调度与自行收尾；不能归因为当时CONTROL_DOWN。
