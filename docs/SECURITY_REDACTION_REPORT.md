# 安全与脱敏报告

扫描时间：2026-10-06T14:08:14.168582+08:00。公开副本残留规则命中：0；已脱敏内容文件：3；本地规则候选文件：245（命中不等于都是真秘密）。
确认存在项目session文件：FOUR_TRACK/playwright/.mcp-session.json、Benchmark/tools/.mcp-session.json。原件保存在本地快照，未放入GitHub安全副本。历史原行、helper、响应headers可能含session/auth材料，因此不直接公开。
规则类别文件数：{'SECRET_ASSIGNMENT': 13, 'PRIVATE_THREAD': 106, 'LOCAL_USERNAME': 43, 'PRIVATE_EMAIL': 90, 'KNOWN_SESSION_VALUE': 4, 'SESSION_FILE': 4, 'COOKIE_HEADER': 1, 'AUTH_HEADER': 1, 'SECRET_QUERY': 1}。不在此报告打印password/token/cookie/session的值。logs/LOCAL_SECURITY_FINDINGS.json仅含位置、类别与原件hash。

公开策略：白名单UTF-8文字；私有DOT/Muse线程URL、当前账户名字、local username、email及可识别个人组合去标识；已知session值与credential模式移除。原始chat、.mcp-session、browser profiles、cookies、headers、原始worker输出、个人升学路线、二进制/ZIP均不直接公开。
research报告保留公开来源的作者/repo名称，属于公开引用，不认作私人账户。学校/比赛只公开聚合数与证据边界，私人规划与具体推荐文件不公开。
logs/REDACTIONS.json与PUBLIC_COPY_MANIFEST.json记录原→安全文件映射、类别与安全hash。公开示例只选择event/state少数键，未简单复制全部状态。GitHub的原件索引只列档案相对路径及hash，不提供credential内容。

限制：regex/已知值扫描不是完整语义隐私证明，归档完成另作独立审查；本地完整包是敏感资料，不整体上传。原始文件没被修改/删除；只在新冻结目录的安全副本脱敏。范围审查删掉14个Archivist误纳的无关媒体/部署**副本**，保留排除记录/hash，所有源文件未动。

|安全副本文件|脱敏类别|
|---|---|
|experiments/project-wheels/CURRENT_STATE.md|{"PRIVATE_THREAD": 2}|
|experiments/benchmark-b/00_PROTOCOL.md|{"LOCAL_USERNAME": 1}|
|experiments/postrun/AUDIT_POSTRUN_50MIN.md|{"LOCAL_USERNAME": 1}|
