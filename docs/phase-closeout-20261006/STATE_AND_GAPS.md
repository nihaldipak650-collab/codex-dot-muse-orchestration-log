# 当前状态、能力继承与尚未验证的接缝

核对对象：技术提交 `f8dcb4bb3c348fd0f95d5af2a594fc3626635b0a`。本文件是静态源码、历史产物与事件对照；不是新的运行试验，也不自动要求实现下列条目。来源编号见 [SOURCES](SOURCES.md)。

## 证据状态

| 项目 | 已有依据 | 边界 |
|---|---|---|
| 旧多轮/双 worker | Wheels、Benchmark B、四轨和三小时记录 | 不证明新 Skill 已经通过 live |
| 历史 ZIP | 四包可读，CRC 检查通过；两份 DOT R2 SHA 相同 | 字节相同不证明远端恰好执行一次 |
| V3 本地实现 | 42 Python/10 PowerShell 检查及独立修复复审记录 PASS | 本次未重跑全部测试；不等于 provider live |
| 基线文件完整性 | 本次独立重算 86 个清单文件 hash，全部匹配 | 不证明隐私、语义正确或外部兼容 |
| V3 live | 注册 tabs 预检无返回；未发测试消息 | CONTROL_UNCONFIRMED，不推断应用或扩展故障根因 |
| 人工/外部验收 | 用户确认过旧工作方式可用 | 新人安装、新账号、V3低介入体验未取得验收证据 |

## 能力矩阵：旧实跑与新封装不是同一列

| 用户需要的能力 | 旧流程证据 | V3 当前实现/限制 |
|---|---|---|
| 给 DOT/Muse 派任务并同线程追问 | 多轮实跑发生过 | alias/session 与两种路径已有；当前 live 未验收 |
| 填入、发送、回复分别确认 | B06/R2暴露问题；后续行为回归改善 | 本地相关测试；严格文本/线程判断需 provider 验证 |
| 一个主包或可用正文交付 | Benchmark B 两种 worker 都有 ZIP 成功 | ZIP/inline 共用层已有，不应永久把 Muse 限成只用正文 |
| 下载后本地阅读 | 真实 ZIP、提取目录、对账存在 | download snippet + local ingest；跨宿主字节传输未完成证明 |
| 下载失败仍保留可用内容 | 历史协议有 inline fallback，四轨有 raw 恢复 | partial/raw 保留通过本地测试；不是内容核实 |
| 包去重 / 候选去重 | R2 同包 hash、V1 canonical 实体去重 | 包与整行字节去重有；语义/规范实体去重仍是协调器责任 |
| 下一轮工作时读上一轮包 | 历史先续杯策略、部分实跑 | ingest 可指定旧 run；discover 默认最新 run，接缝仍待验证 |
| 长时持续推进 | 旧3h行为回归完成 | 无自动总控唤醒/调度服务，不承诺8h无人值守 |
| 新人自然调用 Skill | 原始用户愿景 | 源码存在；宿主发现/独立安装/最短路径未实证 |

## 七组剩余问题

### 1. 使用入口与真实默认值不一致

[wrapper](../../skills/browser-worker/scripts/worker.py) 的 `--transport` 默认是 standalone；缺参数的旧示例会走该路径。registered 模式不是 Python 自动调宿主工具：ask 返回 PREPARED，Codex 仍需执行实际浏览器动作、保存观察并 collect。文档可以明确说明，不应把它宣传为已安装的原子 MCP 工具。

源码位于 `skills/browser-worker/`，wrapper 的 ROOT 依赖整仓库布局。仅复制 Skill 子目录不能据此认为运行依赖齐全。项目级 `.agents/skills/browser-worker` 未在此次 checkout 中看到；用户/系统范围是否已安装未核验。

### 2. 控制未确认不等于找到故障根因

历史注册路径成功、自写 HTTP/SSE 路径失败，说明应比较路径与环境，但不证明自写客户端是唯一根因。V3 的注册 tabs 也曾不返回。client/tab group/profile、实际版本、授权与宿主生命周期应按现场证据区分，不能一超时就重启服务。当前没有重新操作浏览器。

### 3. 文件在哪台机器，尚未变成完整可用路径

[browser_plan.py](../../runtime/browser_plan.py) 的 download 代码在注册 Playwright 工具进程内执行；saveAs 目的地是否为协调器可读文件系统，仍取决于环境。返回路径不是字节交付。当前没有自动远端文件传输服务，必须明确本地读取或真正可用的 inline 降级。

### 4. 旧真实 ZIP 与新严格合同存在差异

本次实际读取历史包发现：DOT R1 使用 candidates.csv，manifest.files 是文件名列表；DOT R2 使用 members + sha256 字段；Muse 为四个子目录各自 manifest 加 FETCH_MANIFEST.json。V3 的 ingest 要求根 manifest、results.json/csv、files 哈希映射和关联 run 标识。旧 BENCHB 标识也不同于新 BW 标识。

这说明需要明确兼容/转换策略；并非已执行过旧包失败测试，也不代表旧包坏了。新格式可校验，不等于历史格式已继承。诚实的零结果、raw部分恢复与内容验证也应有不同含义；源码中 NO_RESULT_ROWS 不应被业务上自动解释成任务失败。

### 5. 先续发，再取旧包的接缝仍在

[workflow.py](../../runtime/workflow.py) 的 ingest 接受指定 run，而 discover 依赖状态的 last_run_id。发新任务后如何继续发现旧回复附件，需要验证明确的旧run绑定。两个 alias 的局部锁也不自动保证共享当前标签页操作隔离；默认 plan 输出路径可能被后续生成覆盖。这些是静态风险，不是本轮已复现的并发故障。

### 6. 会话持续、目标预算与总控持续需要分开

当前发送尝试预算跟 worker alias 累计，默认6/上限20；没有经实测的新目标转换流程。V2 对公开低副作用研究允许有限补交，而 Skill 严格 pending/no-replay 需要和这种授权策略协调。保留“不盲重放”，不等于每次未知都必须让用户救援。

collect 是再读取，不是唤醒已退出 Codex。context capsule 是协调者审核输入，不是自动验证知识。自然控制断线恢复仍未被旧3h或V3新live证明。

### 7. 产品与协作证据尚未齐全

未取得 V3 新人安装/第二账号完整使用、主动操作时间改善、留存或付费证据。技术基线的仓库未选择 LICENSE，未见 .github/workflows 测试流水线；测试文件存在不等于 CI 已执行。许可证、平台允许用途和维护承诺应由拥有者明确决定。

## 本阶段停止条件

本次只把事实、来源和交接补齐，不修上述运行代码，不创建新的版本标签，不开始新实验。下一次只围绕一条真实用户旅程确认：任务发出、交付到手、本地能读、同线程定向修改、人工介入可解释。测试过程不必复制本文件的章节顺序。
