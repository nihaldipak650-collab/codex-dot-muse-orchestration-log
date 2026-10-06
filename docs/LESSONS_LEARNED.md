# 方法总结与适用边界

INFERENCE（从局部工程证据总结，尚非通用效果证明）：
1. 两lane独立推进；回包快筛后refill，再取件/深整理。首可见、取件、入账、续发时间分开。
2. 真实提交与真实回复必须分别确认。输入框文字、整页RUN_ID/COMPLETE、已读和旧WAITING都不证明结果。
3. worker等待时推进旧raw解析、去重、来源核验、比较和综合。每小时QC只问新增价值/是否只等待/下一步，然后继续。
4. checkpoint是恢复材料；只有有效hard stop、目标验收完成、用户停止，或真实blocker且无独立工作，才是结束依据。
5. 有限重试比无限idle更适合低副作用公开搜索；后续按RUN_ID/URL/entity/ZIP hash去重。该权衡不可用于付款/报名/发布/删除。
6. 正式配额达标与边际产出降低应触发阶段转换；gap需要深验证时继续收候选不会自动关闭gap。
7. wall-clock、活动留痕、active估计、worker计算、协调工时分别记录；不同分母的2.3x只是算术。
8. discovery、parse、source partial check、execution test、验收分别计量。Agent完成口述与文件存在不等于verified。
9. 独立研究提出三项学习验收：产物、人能判断纠错、迁移。AI改善作品不证明人学会；延迟/变式/无辅助分别测。
10. Agent组织先单worker baseline，按可测瓶颈加角色；artifact/state/输入版本/验收/停止条件比角色名称更重要。

证据：01时间线、04实验账、05失败目录；外部研究方法归纳见research/AI_PROJECT_AND_AGENT_RESEARCH_REPORT.md。本次不重跑论文、repo或浏览器实验。
