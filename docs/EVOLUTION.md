# 修复与演化

证据分级：CONFIRMED=本次核对本地原始记录/工件；REPORTED=既有Agent或worker报告，未独立复核；INFERENCE=基于证据的解释；UNKNOWN=现有证据不能确定。文件存在、Agent声称完成、结构检查通过均不等于内容正确或运行验收通过。

|版本/变更|触发|变化|验证边界|
|---|---|---|---|
|V0→V1|人工复制与微操作|Codex承担DOT/Muse协调；V1去重副本100|早期完整执行史UNKNOWN|
|V2|真实五方向资源发现|quota与RUN_ID、light review、candidate ledger|候选可计数，不等于repo可用|
|26h复盘 TWO-LANE|idle/bookkeeping/附件|independent lanes、refill-first、最小checkpoint|建议/协议文档，不等于框架实现|
|Benchmark B|验证两lane计时|90m硬停、bundle与ZIP hash dedupe|重复去重核对；缺测量，未证稳定提速|
|B06恢复|草稿错误WAITING|真实提交、回复保存、加入2B|CONFIRMED原始行和71表；正式69保留|
|V1 patch|B07提前结束|20–30m处理停滞、等待时工作、QC后继续；曾建议明示60m续跑上限|文档策略；本次归档不替运行Agent定义新时长|
|V2 patch|避免“完美状态”阻工|progress-first、有限重试、真实状态优先、checkpoint非finish、饱和综合|未进行完整补丁回归验收|
|本地raw恢复|8未解析、字段缺失|8raw恢复；60映射修复；学校28/比赛18|可解析/计数是结构结果，内容未全验|
|Regression|验证长期推进|现有资料方法纠错、B合同边界、C/D局部核验；不扩大池|运行INVALIDATED_PREFLIGHT_NOT_CONFIRMED；完整pass UNKNOWN|

原补丁见patches/LONG_RUN_PATCH_V1.md与LONG_RUN_PATCH_V2.md（本地副本）。V2允许公开检索有界再试，不扩展为副作用操作可重复。保留旧补丁不静默改写；运行源文件不受此归档影响。
