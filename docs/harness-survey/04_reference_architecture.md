# Agent Harness 统一参考架构

**状态：提纲，待调查。** 本章提出用于阅读七个 Coding Agent Harness 的分析模型，不声称任何一个项目完整实现该模型。章节目标是把跨章术语、控制流和信任边界固定在同一层次；读完后应能用最小对象定义描述一次任务，并将项目特有命名映射到共同坐标。它接住[范围、术语与研究方法](01_scope_and_methodology.md)的证据标签和[纵向生命周期](03_vertical_lifecycle_walkthrough.md)的时间线，随后成为[第十章](10_memory.md)与[第十三章](13_compaction_and_context_management.md)可直接引用的术语入口。

## 为什么需要统一参考架构

七个项目在语言、客户端、provider 和扩展方式上不同，直接按目录名称或 UI 菜单比较会把同名异义、异名同义混在一起。统一参考架构的作用是提供一个最小的翻译层：它描述一个 Harness 为了将用户目标转为可控代码行动必须面对的状态、边界和消息流，但不规定实现必须拆成哪些进程、类或数据库表。

该模型的替代方案是只逐项目叙述，或先定义一套强制的“标准 Harness”。前者不利于横向复核，后者会把样本差异误写为缺陷；因此本章选择足够小的参考对象和待验证映射。任何映射必须保留来源术语、代码位置、证据状态和不匹配之处，具体差异由[第二十三章](23_codex.md)至[第二十九章](29_aider.md)解释。

**图表计划：** 绘制分层架构图：上层是用户与客户端，中间是控制平面，下层是执行平面与外部副作用；Session/Context/Memory 横跨控制层，Event/Artifact 从执行层回流。图中每条跨层箭头显式标出数据、控制和信任边界，避免只画“模型居中”的抽象图。

## 控制平面与执行平面

**控制平面** 是决定任务如何被解释、何时调用模型、哪些工具可用、是否需要批准、如何保存和恢复状态的逻辑与策略集合。**执行平面** 是实际读取/写入工作区、启动子进程、访问网络、调用 Git 或外部服务并返回结果的组件与环境。两者可以位于同一进程，也可以分散在 CLI、服务、SDK、MCP/ACP 客户端或宿主环境；分析时不能用部署形式替代职责划分。

这一区分使“工具可用”与“工具已获执行许可”分开，也使 UI 显示的确认与最终执行器的 policy 分开。后续调查需查验 Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 的决策点、执行器、配置来源和错误回流路径；详细机制分别归入[第八章](08_tool_call_system.md)、[第十七章](17_security_permissions_and_sandboxing.md)和[第二十章](20_interfaces_and_human_in_the_loop.md)。

**安全分析计划：** 对每次跨平面动作记录发起者、目标资源、授权依据、执行位置、可观察事件和失败处理。特别检查模型或 extension 的非可信输入能否影响命令、文件路径、网络目的地或凭据，及确认/沙箱/allowlist 是在调用前、调用中还是调用后生效；没有追到执行边界的实现不可标作防护。

## Session、Turn、Message、Event 与 Artifact

以下是供全书使用的最小工作定义，后续章节必须先引用本处再补充各项目本地语义：**Session** 是围绕一个可连续或可恢复任务的状态容器；**Turn** 是 Session 内由一个新输入或内部续行触发、直到等待、完成、失败或交还控制的一段处理；**Message** 是参与者或系统之间有语义角色的内容记录，如用户输入、模型响应或工具结果；**Event** 是按时间记录的状态变化或增量通知，可用于驱动界面、日志或重放；**Item** 是可被序列化、排序、引用或展示的最小工作单元，其具体类型可包括 Message、Tool Call、Tool Result、审批请求或摘要；**Artifact** 是任务产生、可供外部检查或后续消费的有界结果，如 diff、文件、测试输出、导出记录或最终解释。

这些定义刻意允许一对多和不同持久化策略：一个 Turn 可产生多个 Message/Event/Item；一个 Artifact 可由多个工具与 Turn 共同形成；某系统也可能只存 transcript 而不存全部 Event。实现调查应先查 project 的真实数据结构，再记录其与本定义的映射，不能因 API 使用 `session`、`thread`、`history` 或 `item` 便认定语义相同。[第十二章](12_session_persistence_and_resume.md)和[第十九章](19_observability_evaluation_and_replay.md)将用该字典讨论恢复与审计。

**代码证据计划：** 初始可追踪点包括 `codex/codex-rs/code-mode-protocol/src/session.rs`、`deepseek-harness/packages/core/session/`、`goose/crates/goose/src/acp/server/manage_sessions.rs`、`opencode/packages/protocol/src/groups/session.ts`、`pi/packages/agent/src/harness/session/session.ts` 及其 tests。Gemini CLI 与 Aider 应从已确认的 CLI/core 入口和对应测试追踪实际状态对象；此处不假定它们使用同名实体。

## Context、Memory 与 Compaction

**Context** 是某次模型调用实际可见、可序列化或可推导的输入集合，可能含当前请求、指令、消息、工具定义、文件内容、摘要和环境信息；它是调用视图，不等同于整个 Session。**Memory** 是在当前调用之外保存、索引或可检索，并可能影响后续 Context 的信息；它可以是显式用户记录、项目知识或系统产生的摘要，不能仅凭存储目录推定其自动注入。**Compaction** 是为适应上下文预算而选择、压缩、重写、丢弃或外置一部分可见信息的过程及其产物。

三者的关键边界是可追溯性：Context 回答“本次模型看到了什么”，Memory 回答“跨时段什么可能被重新取回”，Compaction 回答“信息如何从一个可见表示变为另一个”。它们与 Session 有关联但不互为别名；例如持久化 Session 未必能恢复调用时 Context，保存摘要也未必是可检索 Memory。后续[第十章](10_memory.md)、[第十二章](12_session_persistence_and_resume.md)、[第十三章](13_compaction_and_context_management.md)和[第十四章](14_token_efficiency_and_cost_control.md)必须以此边界报告实现、默认值与信息损失风险。

**图表与学术检索计划：** 画出 Session 存储、Memory store、一次 Turn 的 Context 和 Compaction 前后表示之间的边界图，箭头标注“注入”“检索”“摘要”“持久化”而非暗示自动化。学术检索以“context management for tool-using agents”“memory provenance in LLM agents”“lossy summarization and task recovery”为问题，逐条核验原文和稳定标识后才用于解释，不在本章预置引文或经验结论。

## 能力层、协议层与客户端

能力层提供模型调用、工具、文件/终端、编辑、Git、搜索和测试等可行动能力；协议层定义组件之间如何表达消息、调用、结果、取消和错误；客户端则把这些能力暴露为 CLI、TUI、IDE、Web、SDK 或其他交互入口。同一能力可以被多个客户端共享，同一客户端也可能绕过某条协议直连控制平面，因此“支持某协议”不能代替对真实任务路径的判断。

比较时应追踪能力声明如何变成可执行工具、客户端如何订阅 Event、协议适配如何保留调用 ID 和错误语义，以及扩展注册是否改变默认信任边界。MCP、ACP、plugin、hook 与 provider adapter 的细节分别留给[第六章](06_model_and_provider_abstraction.md)、[第九章](09_plugins_mcp_and_extensions.md)和[第二十章](20_interfaces_and_human_in_the_loop.md)；本章只提供它们在架构图中的责任位置。

**代码证据计划：** 待查看 `codex/codex-rs/mcp-server/src/codex_tool_runner.rs`、`deepseek-harness/packages/subagent/` 与 `packages/core/tools/`、`gemini-cli/packages/cli/src/acp/`、`goose/crates/goose/src/acp/`、`opencode/packages/codemode/src/tool-runtime.ts`、`pi/packages/agent/src/harness/tools/` 的注册、协议、错误和测试链。Aider 的能力注册从 coder 与 tool 相关模块反向定位；不得将目录存在写成协议兼容结论。

## 信任边界与副作用

参考架构把用户与项目指令、模型/provider 返回、插件/协议对端、配置与凭据、工具子进程、工作区、Git、网络和持久化存储视为不同信任域。副作用是对这些域中可观察资源的改变或外发，例如改写文件、运行命令、提交 Git、访问网络、写入 session 或传递凭据；纯文本解释也可能影响人类决策，但不应与可执行副作用混写。

安全分析要沿“输入来源—策略判断—执行点—记录—恢复/撤销”绘制攻击面，而非仅统计工具数量。应特别验证 prompt/配置是否可扩展工具权限、session resume 是否复用旧的授权上下文、extension 或协议适配是否引入新的命令/网络边界，以及错误是否泄漏敏感输出。该模型为[第十七章](17_security_permissions_and_sandboxing.md)、[第十八章](18_code_editing_git_and_workspace.md)和[第二十二章](22_configuration_identity_and_supply_chain.md)预留共同语言。

## 七个系统到参考架构的映射

映射表应以 Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 为行，以控制/执行平面、Session/Turn/Item、Context/Memory/Compaction、能力/协议/客户端和信任边界为列。每格保存“项目术语—源码入口—证据状态—未决问题”，允许一个项目映射多个对象，也允许没有证据的格子为空或明确写待调查。表的价值在于暴露需要追踪的接口，而不是产生一个整齐的评分表。

填表顺序应先锁定各项目的用户入口和持久化状态，再追 loop、tool dispatch、approval、客户端事件及测试；这样可避免从扩展目录或 README 反向猜测控制流。完成后的表将服务于横向综合和个案解读：同一行的异常分支进入[第二十一章](21_reliability_and_resource_control.md)，同一列的跨项目差异进入[第三十章](30_comparative_synthesis.md)，而项目为何采用特定组合留给各个案章。

**验证计划：** 每个已填单元格至少核验一个入口、调用链、状态对象、异常或取消路径以及测试；可运行时另记录环境、配置、命令、观察和局限。映射时严格使用 Documented、Implemented、Default、Verified、Inferred 五级状态，避免以测试存在替代默认行为或以实现存在替代运行验证。

## 本章小结

本章给出控制平面/执行平面、八个最小状态对象及能力、协议、客户端和信任边界的统一坐标。它不是第八个 Harness，而是一份可被七个固定 revision 证伪或细化的分析接口；读者可据此进入[第十章](10_memory.md)与[第十三章](13_compaction_and_context_management.md)的状态问题，或回到[第三章](03_vertical_lifecycle_walkthrough.md)将对象置于一次完整任务流中。
