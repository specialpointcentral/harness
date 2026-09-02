# 术语表

## 如何使用术语表

本术语表是正文的语义索引，不是把各章定义重新缩写成另一套规范。每一条先给出中文术语和英文原词，再用一句话说明它在本报告中的含义，并链接到负责建立定义或辨析边界的正文小节。读者从[主教学案例](00_index.md#一句话请求先要落到正确的工作区)进入时，可以用这里确认一个词指的是模型输入、运行状态、外部副作用还是产品内部命名，再回到链接处阅读机制、例子和设计取舍。

同一个英文词在不同系统里可能承担不同责任。例如任务（Task）既可能只是待办文字，也可能是可调度、可结算的工作单元。记忆（Memory）既可能指跨任务可检索经验，也可能只是保存下来的聊天历史。表中的定义采用全书统一抽象，不能替代个案章对固定版本实现的限定。最后一节把七个系统的专有术语映射回这些通用概念，便于读者在源码命名与跨系统比较之间往返。

## 通用 Agent 术语

这些术语描述 Agent 怎样围绕目标持续行动，以及规划、委派和用户参与怎样改变任务拓扑。它们不预设某一种产品形态，也不表示所有系统都提供同名对象。

| 术语（英文原词） | 一句话定义与定义入口 |
| --- | --- |
| 智能体（Agent） | Agent 是围绕目标持续选择下一步，并让环境结果影响后续判断的运行行为，定义见[为什么一次响应不等于一个 Agent](05_harness_loop.md#为什么一次响应不等于一个-agent)。 |
| 智能体运行支架（Agent Harness） | Agent Harness 是把模型、真实工作区、工具执行、权限、状态和恢复组织成持续工程闭环的系统，定义见[从一次修复任务看 Harness](01_introducing_agent_harness.md#从一次修复任务看-harness)。 |
| 推理与行动（Reasoning and Acting, ReAct） | ReAct 指推理、行动与环境观察交替推进的 Agent 模式，本报告用它解释短反馈循环而不把它等同于某个 Harness 的具体实现，见[为什么一次响应不等于一个 Agent](05_harness_loop.md#为什么一次响应不等于一个-agent)。 |
| 智能体与计算机接口（Agent-Computer Interface, ACI） | ACI 是 Agent 用来观察和操作计算机环境的接口集合，其工作目录、错误和截断语义会直接影响任务行为，见[从一次修复任务看 Harness](01_introducing_agent_harness.md#从一次修复任务看-harness)。 |
| 行动空间（Action Space） | Action Space 是模型在当前上下文中可见并能向 Harness 提议的动作集合，见[工具如何成为模型的行动空间](08_tool_call_system.md#工具如何成为模型的行动空间)。 |
| 目标（Goal） | Goal 描述期望外部世界达到的终态、范围、禁止事项和验收证据，见[Goal、Plan、Task 与 Todo](15_goals_planning_and_todos.md#goalplantask-与-todo)。 |
| 计划（Plan） | Plan 是从当前状态走向 Goal 的可修订路线，负责显式表达阶段、假设和验证点，见[Goal、Plan、Task 与 Todo](15_goals_planning_and_todos.md#goalplantask-与-todo)。 |
| 任务（Task） | Task 是具有输入、状态、依赖、执行者和结果边界的可调度工作单元，见[Goal、Plan、Task 与 Todo](15_goals_planning_and_todos.md#goalplantask-与-todo)。 |
| 待办项（Todo） | Todo 是向模型和用户展示当前进度的简短状态投影，本身不证明 Goal 已经满足，见[Goal、Plan、Task 与 Todo](15_goals_planning_and_todos.md#goalplantask-与-todo)。 |
| 计划模式（Plan Mode） | Plan Mode 是限制高副作用能力、允许调查和形成计划的协作与权限状态，见[计划模式与执行模式](15_goals_planning_and_todos.md#计划模式与执行模式)。 |
| 执行模式（Execution Mode） | Execution Mode 是计划获准后重新装配写入、命令与其他副作用能力的运行状态，见[计划模式与执行模式](15_goals_planning_and_todos.md#计划模式与执行模式)。 |
| 子智能体（Subagent） | Subagent 是由 Parent 为有界子任务创建、具有独立身份或上下文并返回结果的执行单元，见[为什么委派任务](16_subagents_and_orchestration.md#为什么委派任务)。 |
| 父级与子级（Parent and Child） | Parent 和 Child 表达委派来源与责任关系，但不会自动提供任务依赖或工作区隔离，见[Parent、Child、Task、Thread 与 Session](16_subagents_and_orchestration.md#parentchildtaskthread-与-session)。 |
| 智能体图（Agent Graph） | Agent Graph 记录 Agent 之间的创建、通信或来源关系，其边语义不等于任务依赖，见[父子树、Agent Graph、Task DAG 与 Workflow](16_subagents_and_orchestration.md#父子树agent-graphtask-dag-与-workflow)。 |
| 任务有向无环图（Task Directed Acyclic Graph, Task DAG） | Task DAG 用带依赖的无环节点控制哪些 Task 可以进入就绪和执行状态，见[父子树、Agent Graph、Task DAG 与 Workflow](16_subagents_and_orchestration.md#父子树agent-graphtask-dag-与-workflow)。 |
| 工作流（Workflow） | Workflow 描述多个步骤或 Agent 如何按顺序、并行与汇合规则形成实际执行拓扑，见[父子树、Agent Graph、Task DAG 与 Workflow](16_subagents_and_orchestration.md#父子树agent-graphtask-dag-与-workflow)。 |
| 等待（Wait） | Wait 表示当前执行者暂停推进，直到消息、状态变化或超时到达，见[Wait、Join、取消与失败传播](16_subagents_and_orchestration.md#waitjoin取消与失败传播)。 |
| 汇合（Join） | Join 表示收集一个或多个已启动执行的完成、失败、取消或结果未知终态，见[Wait、Join、取消与失败传播](16_subagents_and_orchestration.md#waitjoin取消与失败传播)。 |
| 人在回路（Human-in-the-loop） | Human-in-the-loop 是把审批、编辑、模式切换、中断或验收等决定交给用户参与的控制安排，见[审批、编辑与中断](20_interfaces_and_human_in_the_loop.md#审批编辑与中断)。 |

## Harness 架构术语

这一组术语说明 Harness 把责任放在哪里，以及任务、模型输入和交付结果分别由什么对象承载。八个核心对象是全书的翻译基线，个案章中的不同类名应先映射到这些责任，再比较实现差异。

| 术语（英文原词） | 一句话定义与定义入口 |
| --- | --- |
| 控制平面（Control Plane） | Control Plane 负责任务身份、上下文构造、模型选路、编排、策略和终止判断，见[控制平面与执行平面](04_reference_architecture.md#总体结构控制平面决定执行平面行动)。 |
| 执行平面（Execution Plane） | Execution Plane 负责把已校验、已授权的动作落实为文件、进程、网络或外部服务变化，见[控制平面与执行平面](04_reference_architecture.md#总体结构控制平面决定执行平面行动)。 |
| 会话（Session） | Session 是围绕一项可连续、可查询或可恢复任务保存身份、历史与控制状态的逻辑容器，见[八个核心对象](04_reference_architecture.md#八个核心对象一项任务由什么组成)。 |
| 轮次（Turn） | Turn 是从一次新输入或内部续行开始，到完成、失败、取消、等待或交还控制为止的处理区间，见[八个核心对象](04_reference_architecture.md#八个核心对象一项任务由什么组成)。 |
| 消息（Message） | Message 是具有用户、模型、工具等语义角色的内容单元，见[Turn、Message、Event 与 Item](12_session_persistence_and_resume.md#turnmessageevent-与-item)。 |
| 事件（Event） | Event 是表示状态随时间发生变化的通知或记录，见[Turn、Message、Event 与 Item](12_session_persistence_and_resume.md#turnmessageevent-与-item)。 |
| 工作单元（Item） | Item 是可排序、引用和展示的异质工作单元，可承载 Message、Tool Call、结果、审批或摘要，见[八个核心对象](04_reference_architecture.md#八个核心对象一项任务由什么组成)。 |
| 本轮上下文（Context） | Context 是某一次模型调用实际可见的、有序且受预算约束的输入投影，见[Context 为什么不只是 Prompt](07_context_and_instruction_system.md#context-为什么不只是-prompt)。 |
| 可检索记忆（Memory） | Memory 是位于当前调用之外、可跨任务保存并在合适范围内检索或注入的信息源，见[Memory 与 Session 状态的区别](10_memory.md#memory-与-session-状态的区别)。 |
| 工作记忆（Working Memory） | Working Memory 保存当前仍在使用的目标、约束、近期 Observation 和未决事项，见[Working、Episodic、Semantic 与 Procedural Memory](10_memory.md#workingepisodicsemantic-与-procedural-memory)。 |
| 情景记忆（Episodic Memory） | Episodic Memory 保存一次具体经历的条件、行动和结果，见[Working、Episodic、Semantic 与 Procedural Memory](10_memory.md#workingepisodicsemantic-与-procedural-memory)。 |
| 语义记忆（Semantic Memory） | Semantic Memory 保存从经历中提取、具有范围和新鲜度要求的相对稳定事实与关系，见[Working、Episodic、Semantic 与 Procedural Memory](10_memory.md#workingepisodicsemantic-与-procedural-memory)。 |
| 过程性记忆（Procedural Memory） | Procedural Memory 保存怎样完成一类任务的可复用步骤、Skill、模板或经过验证的脚本，见[Working、Episodic、Semantic 与 Procedural Memory](10_memory.md#workingepisodicsemantic-与-procedural-memory)。 |
| 任务产物（Artifact） | Artifact 是任务产生并可由外部检查或后续消费的有界结果，如 diff、测试输出或报告，见[八个核心对象](04_reference_architecture.md#八个核心对象一项任务由什么组成)。 |
| 运行循环（Harness Loop） | Harness Loop 是组织模型请求、行动校验、执行、Observation、继续和终止的持续控制协议，见[Turn、状态与循环不变量](05_harness_loop.md#turn状态与循环不变量)。 |
| 模型服务适配层（Provider） | Provider 隔离不同模型服务的认证、消息、流式响应、Tool Call、错误和用量差异，见[Provider 层在隔离什么](06_model_and_provider_abstraction.md#provider-层在隔离什么)。 |
| 上下文构造器（Context Builder） | Context Builder 从指令、历史、工作区、能力和动态观察中选择并排序本次模型输入，见[Context 为什么不只是 Prompt](07_context_and_instruction_system.md#context-为什么不只是-prompt)。 |
| 能力目录（Capability Catalog） | Capability Catalog 是当前 Agent 可以发现并被投影进 Context 的能力契约集合，见[Schema、注册表与能力发现](08_tool_call_system.md#schema注册表与能力发现)。 |
| 注册表（Registry） | Registry 保存能力名称到实际运行实现的绑定，并为发现、更新和执行提供权威目录，见[Schema、注册表与能力发现](08_tool_call_system.md#schema注册表与能力发现)。 |
| 执行器（Executor） | Executor 接受已关联和已授权的调用，在受限环境中执行并产生进度、结果或错误，见[执行、结果与 Observation](08_tool_call_system.md#执行结果与-observation)。 |
| 工作区（Workspace） | Workspace 是任务实际读取、修改、测试和形成 Git 状态的文件与工程作用域，见[Workspace、代码与动态上下文](07_context_and_instruction_system.md#workspace代码与动态上下文)。 |
| 客户端（Client） | Client 是命令行、终端界面、集成开发环境、桌面、网页、软件开发工具包或接口等展示与控制入口，见[CLI、TUI、IDE、Desktop、Web 与 API](20_interfaces_and_human_in_the_loop.md#clituiidedesktopweb-与-api)。 |
| 无界面模式（Headless Mode） | Headless Mode 是没有现场交互界面的运行方式，必须用预设策略和机器可判定结果处理审批、错误与退出，见[Headless 与非交互模式](20_interfaces_and_human_in_the_loop.md#headless-与非交互模式)。 |

## Tool 与扩展术语

Tool 和扩展都会扩大系统能做的事情，但改变的层次不同。Tool Call 表达一次具体行动，Schema 和 Registry 建立调用契约，Plugin、Extension、MCP、Skill 与 Hook 则分别改变装配、协议、过程知识或生命周期。

| 术语（英文原词） | 一句话定义与定义入口 |
| --- | --- |
| 工具调用（Tool Call） | Tool Call 是模型向 Harness 提出的结构化行动请求，不是模型亲自执行动作，见[工具如何成为模型的行动空间](08_tool_call_system.md#工具如何成为模型的行动空间)。 |
| 工具描述模式（Tool Schema） | Tool Schema 用稳定名称、说明和参数约束描述模型怎样提出某项能力，见[Schema、注册表与能力发现](08_tool_call_system.md#schema注册表与能力发现)。 |
| 能力发现（Capability Discovery） | Capability Discovery 决定哪些已注册能力在当前 Agent、模式、项目和预算下进入模型可见目录，见[Schema、注册表与能力发现](08_tool_call_system.md#schema注册表与能力发现)。 |
| 调用标识（Call ID） | Call ID 把流式参数、审批、执行进度、结果和错误关联到同一次 Tool Call，见[请求、参数与 Call ID](08_tool_call_system.md#请求参数与-call-id)。 |
| 工具结果（Tool Result） | Tool Result 是工具执行后带状态、内容、错误和必要元数据的结构化结果，见[执行、结果与 Observation](08_tool_call_system.md#执行结果与-observation)。 |
| 环境观察（Observation） | Observation 是外部结果在 Loop 中用于更新下一步判断的角色，可由 Tool Result、Message 或 Event 表达，见[执行、结果与 Observation](08_tool_call_system.md#执行结果与-observation)。 |
| 请求封装（Request Envelope） | Request Envelope 规范化调用标识、能力名称、参数和来源位置，见[请求、参数与 Call ID](08_tool_call_system.md#请求参数与-call-id)。 |
| 响应封装（Response Envelope） | Response Envelope 规范化原调用的完成状态、模型可见内容、结构化值和截断元数据，见[请求、参数与 Call ID](08_tool_call_system.md#请求参数与-call-id)。 |
| 错误封装（Error Envelope） | Error Envelope 记录失败阶段、机器可判别类别、可重试性和可能存在的部分副作用，见[请求、参数与 Call ID](08_tool_call_system.md#请求参数与-call-id)。 |
| 审批封装（Approval Envelope） | Approval Envelope 把最终参数、资源范围、决定、作用域和审查者与原调用关联，见[请求、参数与 Call ID](08_tool_call_system.md#请求参数与-call-id)。 |
| 插件（Plugin） | Plugin 是把多类贡献装配进 Harness、并由宿主管理来源和生命周期的包或模块，见[Plugin、Extension、MCP、Skill 与 Hook](09_plugins_mcp_and_extensions.md#pluginextensionmcpskill-与-hook)。 |
| 扩展（Extension） | Extension 是产品公开的可编程扩展面，可注册能力并介入运行时行为，见[Plugin、Extension、MCP、Skill 与 Hook](09_plugins_mcp_and_extensions.md#pluginextensionmcpskill-与-hook)。 |
| 模型上下文协议（Model Context Protocol, MCP） | MCP 是 Host、Client 与 Server 之间发现和交换 Tool、Resource、Prompt 等能力的互操作协议，见[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)。 |
| 协议宿主（MCP Host） | MCP Host 管理一个或多个 Client、能力目录、生命周期和产品侧政策，见[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)。 |
| 协议客户端（MCP Client） | MCP Client 代表 Host 连接一个 Server，完成初始化、发现、调用和通知处理，见[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)。 |
| 协议服务器（MCP Server） | MCP Server 通过协议提供 Tool、Resource、Prompt 或其他协商能力，但通常不拥有完整 Agent Loop，见[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)。 |
| 传输（Transport） | Transport 是协议消息跨进程或网络交换的承载方式，如 stdio 或 Streamable HTTP，见[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)。 |
| 技能（Skill） | Skill 是带摘要、正文和可选资源的按需过程知识，装入 Context 不自动授予执行权限，见[Skill 的发现、选择与加载](11_skills_prompts_commands_and_hooks.md#skill-的发现选择与加载)。 |
| 提示模板（Prompt Template） | Prompt Template 把稳定任务结构与用户参数分开，并在展开后形成最终 Prompt，见[Prompt Template 与项目定制](11_skills_prompts_commands_and_hooks.md#prompt-template-与项目定制)。 |
| 斜杠命令（Slash Command） | Slash Command 是由客户端或 Harness 解析的显式控制入口，可直接改变本地状态或装配模型工作，见[Slash Command 与用户控制](11_skills_prompts_commands_and_hooks.md#slash-command-与用户控制)。 |
| 生命周期钩子（Hook） | Hook 是在模型、工具、Session、压缩或停止等固定阶段执行的拦截、改写或通知处理器，见[Hook 与生命周期拦截](11_skills_prompts_commands_and_hooks.md#hook-与生命周期拦截)。 |
| 智能体客户端协议（Agent Client Protocol, ACP） | ACP 是客户端与 Agent Server 之间传递 Session、Prompt、进度、权限和取消等控制消息的协议边界，见[ACP、JSON-RPC 与应用服务器](20_interfaces_and_human_in_the_loop.md#acpjson-rpc-与应用服务器)。 |
| JSON 远程过程调用（JSON Remote Procedure Call, JSON-RPC） | JSON-RPC 是用请求、响应、通知与错误组织双向协议消息的通用封装，见[ACP、JSON-RPC 与应用服务器](20_interfaces_and_human_in_the_loop.md#acpjson-rpc-与应用服务器)。 |
| 补丁（Patch） | Patch 是把新增、删除、更新或移动等文件变化表达为可校验编辑动作的结构化表示，见[直接写入、Patch 与结构化编辑](18_code_editing_git_and_workspace.md#直接写入patch-与结构化编辑)。 |
| 差异（Diff） | Diff 是工作区或提交之间实际内容变化的可审查表示，用于区分模型提议和最终文件状态，见[Diff、审查与用户修改](18_code_editing_git_and_workspace.md#diff审查与用户修改)。 |
| 工作树（Worktree） | Worktree 是与某个 Git 历史和索引关联的独立检出目录，可用于隔离并行 Agent 的文件修改，见[Git、Worktree 与 Submodule](18_code_editing_git_and_workspace.md#gitworktree-与-submodule)。 |
| 子模块（Submodule） | Submodule 是主仓库以固定提交引用另一个 Git 仓库的依赖边界，见[Git、Worktree 与 Submodule](18_code_editing_git_and_workspace.md#gitworktree-与-submodule)。 |
| 静态检查（Lint） | Lint 是在不等同于完整测试的前提下检查代码风格、语法或规则违例的验证步骤，见[Test、Lint 与构建](18_code_editing_git_and_workspace.md#testlint-与构建)。 |
| 测试（Test） | Test 是在明确命令、环境和代码状态下执行，用结果与退出状态验证行为的工程证据，见[Test、Lint 与构建](18_code_editing_git_and_workspace.md#testlint-与构建)。 |

## 状态与持久化术语

这组术语区分“保存了什么”“恢复时能证明什么”和“失败后还应怎样继续”。内部记录可以重建 Harness 状态，却不能自动撤销文件、进程或远端服务已经发生的副作用。

| 术语（英文原词） | 一句话定义与定义入口 |
| --- | --- |
| 持久化（Persistence） | Persistence 是把任务身份、已提交历史和必要环境绑定保存到进程之外，以便后续查询或重建连续性，见[Session 保存的任务边界](12_session_persistence_and_resume.md#session-保存的任务边界)。 |
| 事件日志（Event Log） | Event Log 按稳定顺序追加状态变化，用于重建、审计和派生历史，见[Event Log、Snapshot 与 Checkpoint](12_session_persistence_and_resume.md#event-logsnapshot-与-checkpoint)。 |
| 快照（Snapshot） | Snapshot 保存某一位置的折叠状态或工作区版本，以缩短恢复和比较路径，见[Event Log、Snapshot 与 Checkpoint](12_session_persistence_and_resume.md#event-logsnapshot-与-checkpoint)。 |
| 检查点（Checkpoint） | Checkpoint 声明越过某个语义边界前，恢复所需材料已经达到规定的耐久条件，见[Event Log、Snapshot 与 Checkpoint](12_session_persistence_and_resume.md#event-logsnapshot-与-checkpoint)。 |
| 恢复（Resume） | Resume 保持原 Session 身份，在已提交尾部之后继续并重新核对当前环境，见[Resume、Replay、Branch 与 Fork](12_session_persistence_and_resume.md#resumereplaybranch-与-fork)。 |
| 重放（Replay） | Replay 从日志或快照重新计算内部投影，默认读取已记录结果而不再次执行外部动作，见[Resume、Replay、Branch 与 Fork](12_session_persistence_and_resume.md#resumereplaybranch-与-fork)。 |
| 分支（Branch） | Branch 在同一逻辑历史中选择旧节点作为新的活动叶并继续形成另一条路径，见[Resume、Replay、Branch 与 Fork](12_session_persistence_and_resume.md#resumereplaybranch-与-fork)。 |
| 派生（Fork） | Fork 创建新的 Session 身份，复制或引用历史前缀并保留来源谱系，见[Resume、Replay、Branch 与 Fork](12_session_persistence_and_resume.md#resumereplaybranch-与-fork)。 |
| 上下文压缩（Compaction） | Compaction 在 Session 历史接近窗口上限时，用有损选择、摘要或外置形成可继续的模型输入，见[自动和手动 Compaction](13_compaction_and_context_management.md#自动和手动-compaction)。 |
| 截断（Truncation） | Truncation 在内容产生或读取时只保留有界区间，并应明确省略范围，见[截断、摘要、选择与外部化](13_compaction_and_context_management.md#截断摘要选择与外部化)。 |
| 摘要（Summarization） | Summarization 用较短文字替换较长历史或结果，同时承担信息失真和遗漏风险，见[截断、摘要、选择与外部化](13_compaction_and_context_management.md#截断摘要选择与外部化)。 |
| 选择（Selection） | Selection 按当前目标和价值保留部分原始材料，而不是改写全部内容，见[截断、摘要、选择与外部化](13_compaction_and_context_management.md#截断摘要选择与外部化)。 |
| 外部化（Externalization） | Externalization 把完整内容移到模型窗口之外，并在 Context 中留下可取回线索，见[截断、摘要、选择与外部化](13_compaction_and_context_management.md#截断摘要选择与外部化)。 |
| 修剪（Pruning） | Pruning 在历史积累后删除或替换较旧、低价值的 Tool Result，见[截断、Pruning、Spill 与 Locator](14_token_efficiency_and_cost_control.md#截断pruningspill-与-locator)。 |
| 外溢（Spill） | Spill 把超大 Tool Result 的全文保存为窗口外 Artifact，只把有界预览送入模型，见[截断、Pruning、Spill 与 Locator](14_token_efficiency_and_cost_control.md#截断pruningspill-与-locator)。 |
| 定位符（Locator） | Locator 是重新取得被截断、修剪或外置原文的位置与取回指引，见[截断、Pruning、Spill 与 Locator](14_token_efficiency_and_cost_control.md#截断pruningspill-与-locator)。 |
| 提示缓存（Prompt Cache） | Prompt Cache 复用多个请求共享的稳定前缀计算，但不减少逻辑 Context 长度，见[Prompt Cache、KV Cache 与稳定前缀](14_token_efficiency_and_cost_control.md#prompt-cachekv-cache-与稳定前缀)。 |
| 键值缓存（Key-Value Cache, KV Cache） | KV Cache 是推理服务内部保存注意力中间状态的机制，Harness 只能通过稳定前缀等条件影响复用机会，见[Prompt Cache、KV Cache 与稳定前缀](14_token_efficiency_and_cost_control.md#prompt-cachekv-cache-与稳定前缀)。 |
| 幂等性（Idempotency） | Idempotency 指同一逻辑操作执行多次时最终效果仍等同于执行一次，见[幂等性与外部副作用](21_reliability_and_resource_control.md#幂等性与外部副作用)。 |
| 重试（Retry） | Retry 是在满足错误分类、副作用和预算条件时重复同一个逻辑尝试，见[Retry、Backoff 与 Fallback](21_reliability_and_resource_control.md#retrybackoff-与-fallback)。 |
| 退避（Backoff） | Backoff 是为后续重试安排递增、封顶并可带抖动的等待策略，见[Retry、Backoff 与 Fallback](21_reliability_and_resource_control.md#retrybackoff-与-fallback)。 |
| 降级路径（Fallback） | Fallback 是在原传输、模型或运行时不可用时改走另一条路径，并显式承认能力或语义可能变化，见[Retry、Backoff 与 Fallback](21_reliability_and_resource_control.md#retrybackoff-与-fallback)。 |
| 超时（Timeout） | Timeout 为等待设置截止点，但不自动证明底层任务已经停止，见[Timeout、Cancel 与 Interrupt](21_reliability_and_resource_control.md#timeoutcancel-与-interrupt)。 |
| 取消（Cancel） | Cancel 请求正在进行的工作停止，并要求在途调用与资源收敛到可观察终态，见[Timeout、Cancel 与 Interrupt](21_reliability_and_resource_control.md#timeoutcancel-与-interrupt)。 |
| 中断（Interrupt） | Interrupt 是用户或上层控制面触发取消的入口，其结果不等同于回滚，见[Timeout、Cancel 与 Interrupt](21_reliability_and_resource_control.md#timeoutcancel-与-interrupt)。 |
| 后台作业（Background Job） | Background Job 是跨越前台 Tool Call 或 Turn 继续运行、具有稳定身份和所有者的进程或任务，见[后台进程与资源清理](21_reliability_and_resource_control.md#后台进程与资源清理)。 |
| 日志（Log） | Log 是按时间记录的离散诊断文本或结构化条目，见[Log、Event、Trace 与 Metric](19_observability_evaluation_and_replay.md#logeventtrace-与-metric)。 |
| 追踪（Trace） | Trace 用父子或关联标识串起一次模型请求、Tool Call 与后续步骤的因果路径，见[Log、Event、Trace 与 Metric](19_observability_evaluation_and_replay.md#logeventtrace-与-metric)。 |
| 指标（Metric） | Metric 是可聚合的数值观测，如 Token、费用、时延、重试和并发，见[Log、Event、Trace 与 Metric](19_observability_evaluation_and_replay.md#logeventtrace-与-metric)。 |
| 遥测（Telemetry） | Telemetry 是把运行事件、指标或可选内容采集到本地或外部观察系统的机制，见[Telemetry、Crash Report 与隐私](19_observability_evaluation_and_replay.md#telemetrycrash-report-与隐私)。 |

## 安全术语

安全术语按“谁在行动、持有什么权力、跨过哪条边界、怎样限制后果”组织。授权、隔离和验证是不同事实，任何一个词都不应被用作总体安全结论。

| 术语（英文原词） | 一句话定义与定义入口 |
| --- | --- |
| 主体（Principal） | Principal 是能够发起、批准或执行动作的逻辑身份，如用户、模型、Agent、Tool、Plugin 或 MCP Server，见[主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)。 |
| 能力（Capability） | Capability 是主体可以行使的有边界权力，如读取某个根、运行特定命令或使用某项凭据，见[主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)。 |
| 信任边界（Trust Boundary） | Trust Boundary 是权威、身份或执行环境发生变化并需要重新校验的接口位置，见[主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)。 |
| 工具权限（Tool Permission） | Tool Permission 是根据工具、最终参数、路径、网络目标、Agent 身份和模式输出 allow、deny 或 ask 的策略判断，见[Tool Permission 与 Human Approval](17_security_permissions_and_sandboxing.md#tool-permission-与-human-approval)。 |
| 人工审批（Human Approval） | Human Approval 是用户对某个具体动作、目标和作用域作出的知情决定，见[Tool Permission 与 Human Approval](17_security_permissions_and_sandboxing.md#tool-permission-与-human-approval)。 |
| 沙箱（Sandbox） | Sandbox 是对已获准动作实际可读写资源、进程、系统调用和网络范围施加的执行限制，见[文件、进程与网络沙箱](17_security_permissions_and_sandboxing.md#文件进程与网络沙箱)。 |
| 工作区信任（Workspace Trust） | Workspace Trust 决定陌生目录中的项目配置、Hook、Plugin、Skill、Prompt 或 MCP 是否能在启动期改变 Harness，见[Workspace Trust 与 Credential Isolation](17_security_permissions_and_sandboxing.md#workspace-trust-与-credential-isolation)。 |
| 凭据隔离（Credential Isolation） | Credential Isolation 把秘密值与普通配置、模型 Context 和 Tool 环境分开，并在操作边界按最小范围注入，见[Workspace Trust 与 Credential Isolation](17_security_permissions_and_sandboxing.md#workspace-trust-与-credential-isolation)。 |
| 提示词注入（Prompt Injection） | Prompt Injection 是低权威文本诱导模型违背更高权威目标或控制规则的攻击方式，见[Prompt Injection 到能力执行](17_security_permissions_and_sandboxing.md#prompt-injection-到能力执行)。 |
| 间接提示词注入（Indirect Prompt Injection） | Indirect Prompt Injection 是把恶意指令藏在仓库、网页、邮件或 Tool Result 等外部数据中，再经模型影响敏感动作，见[Prompt Injection 到能力执行](17_security_permissions_and_sandboxing.md#prompt-injection-到能力执行)。 |
| 混淆代理（Confused Deputy） | Confused Deputy 是高权限执行者被低权限输入诱导，代其访问本不应开放的资源，见[主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)。 |
| 最小权限（Least Privilege） | Least Privilege 要求主体只获得完成当前职责所需的最小能力，见[权限和副作用边界](08_tool_call_system.md#权限和副作用边界)。 |
| 完全仲裁（Complete Mediation） | Complete Mediation 要求每次资源访问都经过与最终动作相匹配的检查，见[权限和副作用边界](08_tool_call_system.md#权限和副作用边界)。 |
| 失败时关闭（Fail Closed） | Fail Closed 指安全门禁、无界面审批或隔离后端不可用时默认拒绝继续，而不是静默放行，见[Tool Permission 与 Human Approval](17_security_permissions_and_sandboxing.md#tool-permission-与-human-approval)。 |
| 智能体身份（Agent Identity） | Agent Identity 是对某个 Agent 运行实例或工作负载的可验证或可关联标识，见[Agent Identity 与调用来源](22_configuration_identity_and_supply_chain.md#agent-identity-与调用来源)。 |
| 调用来源谱系（Call Provenance） | Call Provenance 说明一次 Session、Turn 或 Tool Call 从哪个客户端、Plugin、Parent 或 Subagent 路径发起，见[Agent Identity 与调用来源](22_configuration_identity_and_supply_chain.md#agent-identity-与调用来源)。 |
| 模型服务凭据（Provider Credential） | Provider Credential 是远端模型服务接受请求所依据的 API key、OAuth token 或云身份，见[Provider Credential](22_configuration_identity_and_supply_chain.md#provider-credential)。 |
| 供应链（Supply Chain） | Supply Chain 是配置、包、依赖、Skill、MCP、构建和更新共同决定未来会装入并执行什么的来源链，见[供应链风险](22_configuration_identity_and_supply_chain.md#供应链风险)。 |
| 制品来源证明（Artifact Provenance） | Artifact Provenance 记录制品由哪个来源、构建者、输入和流程产生，但不自动证明内容无恶意，见[自动更新与依赖生命周期](22_configuration_identity_and_supply_chain.md#自动更新与依赖生命周期)。 |

## 七系统专有术语映射

下表保留各系统在固定版本中的内部命名，并把它们映射到本报告的通用责任。这里的中文说明用于帮助阅读个案章，不把一个系统的专有对象推广成其他系统也应采用的标准。

| 系统与术语（英文原词） | 一句话定义与个案入口 |
| --- | --- |
| Codex 线程（Codex Thread） | Codex Thread 包装一个 Core Session 与双向消息通道，由 Thread Manager 创建、Resume、Fork 和管理，见[Codex 的 Rust Core、Protocol 与 App Server](23_codex.md#rust-coreprotocol-与-app-server)。 |
| Codex 执行记录（Rollout） | Rollout 是 Codex 按序追加的规范持久记录，承载 Session、Item、Turn Context、World State 和终态边界，见[Codex 的 Loop、Event 与 Rollout](23_codex.md#loopevent-与-rollout)。 |
| Codex 执行策略（Exec Policy） | Exec Policy 是 Codex 对完整命令结构应用允许、询问或禁止规则的控制面，见[Codex 的 Approval、Sandbox 与 Exec Policy](23_codex.md#approvalsandbox-与-exec-policy)。 |
| OpenCode 智能体模式（Agent Mode） | Agent Mode 用 Agent 定义同时选择角色、模型、提示、步骤和权限，Build、Plan 与 General 因而拥有不同能力边界，见[OpenCode 的 Build、Plan 与 General Agent](24_opencode.md#buildplan-与-general-agent)。 |
| OpenCode 权威服务器（Server） | Server 是 OpenCode 多客户端共同读取和修改 Session、Permission、PTY 与 Event 状态的权威边界，见[Server 作为权威状态层与多客户端](24_opencode.md#server-作为权威状态层与多客户端)。 |
| OpenCode 后台作业（Background Job） | Background Job 是 OpenCode 进程内、按 Session 归属的并发运行记录，可等待、取消和向父 Session 注入结果，但不能跨重启恢复，见[后台 Job 与 Snapshot](24_opencode.md#后台-job-与-snapshot)。 |
| OpenCode 快照（Snapshot） | Snapshot 使用独立 Git 元数据记录步骤前后的文件状态，并为 Patch、Diff 与 Revert 提供边界，见[后台 Job 与 Snapshot](24_opencode.md#后台-job-与-snapshot)。 |
| Pi 智能体核心（Agent Core） | Agent Core 持有模型、活动 Tool、消息与运行状态，并执行模型响应到 Tool Result 的通用循环，见[Pi 的 Agent Core、AI Abstraction 与 Coding Agent](25_pi.md#agent-coreai-abstraction-与-coding-agent)。 |
| Pi 模型抽象层（AI Abstraction） | AI Abstraction 统一 Provider、认证、流式消息、Tool Call、Token 和成本，使 Agent Core 不依赖具体模型服务格式，见[Pi 的 Agent Core、AI Abstraction 与 Coding Agent](25_pi.md#agent-coreai-abstraction-与-coding-agent)。 |
| Pi 扩展接口（Extension API） | Extension API 是 Pi 介入输入、Context、Provider、Tool、Session、压缩和界面的可编程生命周期控制面，见[Extension API 承担高级治理](25_pi.md#extension-api-承担高级治理)。 |
| Pi 项目信任（Project Trust） | Project Trust 是 Pi 在启动期决定是否装入项目 settings、Package、Extension、Skill 和 Prompt 的资源门，见[Project Trust 是资源装入门](25_pi.md#project-trust-是资源装入门)。 |
| Gemini CLI 工具调度器（Tool Scheduler） | Tool Scheduler 独立维护 Tool Call 的解析、政策、确认、并行、进度、执行和终态，见[独立 Tool Scheduler](26_gemini_cli.md#独立-tool-scheduler把模型流与副作用提交拆开)。 |
| Gemini CLI 影子 Git 检查点（Shadow Git Checkpoint） | Shadow Git Checkpoint 在用户仓库之外保存修改前文件快照，并把 commit 与对话和 Tool Call 关联，见[Shadow Git Checkpoint](26_gemini_cli.md#shadow-git-checkpoint把恢复点放在用户仓库之外)。 |
| Gemini CLI 文件夹信任（Folder Trust） | Folder Trust 决定项目级指令和可执行贡献能否进入 Runtime，见[Folder Trust 与 Policy Engine](26_gemini_cli.md#folder-trust-与-policy-engine先决定装入什么再裁决每次行动)。 |
| Gemini CLI 策略引擎（Policy Engine） | Policy Engine 按管理层、用户、Workspace、Extension、模式、参数和 Subagent 身份裁决每次 Tool Call，见[Folder Trust 与 Policy Engine](26_gemini_cli.md#folder-trust-与-policy-engine先决定装入什么再裁决每次行动)。 |
| DeepSeek Harness 组合运行时（Cordis） | Cordis 提供 Context、Service、事件总线、Fiber 和可逆 Effect，用依赖关系组织插件激活与释放，见[Cordis、Service、Provider 与 Consumer](27_deepseek_harness.md#cordisserviceprovider-与-consumer)。 |
| DeepSeek Harness 插件执行单元（Fiber） | Fiber 是等待依赖、激活插件并拥有其注册、监听器和后台资源生命周期的执行单元，见[插件图与依赖注入装配](27_deepseek_harness.md#插件图与依赖注入装配)。 |
| DeepSeek Harness 能力接缝（Capability Seam） | Capability Seam 由 Service Definition、Service Provider 与 Consumer 组成，用稳定语义连接可替换实现和使用方，见[Cordis、Service、Provider 与 Consumer](27_deepseek_harness.md#cordisserviceprovider-与-consumer)。 |
| DeepSeek Harness 智能体作用域（Agent Scope） | Agent Scope 是合并 Tool、Prompt、Context、Skill、Job 与政策贡献的层级装配范围，不等于操作系统隔离，见[Agent Scope、Session 与 Context](27_deepseek_harness.md#agent-scopesession-与-context)。 |
| DeepSeek Harness 模型可见表面（Surface） | Surface 是从追加式 Session Event Log 中选择和替换模型当前可见历史的投影层，见[事件溯源 Session 与 Surface、日志分离](27_deepseek_harness.md#事件溯源-session-与-surface--日志分离)。 |
| Goose 工作流配方（Recipe） | Recipe 是可分享的声明式 Session 装配，组合任务说明、Provider、模型、Extension、参数、输出 Schema、重试和 Subrecipe，见[Goose 的 MCP Extension 与 Recipe](28_goose.md#mcp-extension-与-recipe)。 |
| Goose 子配方（Subrecipe） | Subrecipe 是 Recipe 中可由 Summon 加载或委派为独立 SubAgent Session 的复用角色或子工作流，见[Goose 的 MCP Extension 与 Recipe](28_goose.md#mcp-extension-与-recipe)。 |
| Goose 委派扩展（Summon） | Summon 是 Goose 创建独立 SubAgent Session、同步等待或异步返回任务身份的委派 Extension，见[Context Management 与 Delegation](28_goose.md#context-management-与-delegation)。 |
| Goose ACP 模型服务适配器（ACP Provider） | ACP Provider 把外部 Agent 作为可选 Provider 接入 Goose，并保留外部 Session、模式和权限所有权差异，见[Provider Abstraction 与 ACP](28_goose.md#provider-abstraction-与-acp)。 |
| Aider 编码器抽象（Coder Abstraction） | Coder Abstraction 是 Aider 按模型与 Edit Format 装配提示、解析器、文件集合、Repo Map、Git 和验证循环的核心点，见[Coder Abstraction 与核心循环](29_aider.md#coder-abstraction-与核心循环)。 |
| Aider 仓库地图（Repo Map） | Repo Map 是按符号定义、引用关系和 Token 预算生成的只读仓库结构摘要，不授予文件编辑权限，见[Repo Map 与上下文选择](29_aider.md#repo-map-与上下文选择)。 |
| Aider 编辑格式（Edit Format） | Edit Format 是模型表达整文件、搜索替换、Unified Diff、Patch 或两阶段编辑提议的受约束文本协议，见[Edit Format 与代码修改](29_aider.md#edit-format-与代码修改)。 |
| Aider 架构师与编辑器（Architect/Editor） | Architect/Editor 是先由架构师模型形成修改说明、再由编辑模型用专用 Edit Format 实施的固定两阶段路径，见[Edit Format 谱系与反思闭环](29_aider.md#edit-format-谱系与反思闭环)。 |
| Aider 弱模型（Weak Model） | Weak Model 是优先承担提交消息和历史摘要等边界清楚辅助任务的模型角色，见[多模型、弱模型与 Token](29_aider.md#多模型弱模型与-token)。 |

这些映射揭示了术语表的核心用法：先判断一个名称承担的是输入投影、控制状态、执行能力、持久记录还是安全边界，再比较不同系统把这项责任放在何处。专有名称能够说明项目怎样组织自身，却不能取消通用概念之间的边界。读者在后续综合比较中遇到同名异义或异名同责时，应以正文链接中的状态、数据流和副作用语义为准。
