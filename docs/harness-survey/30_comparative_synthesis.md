# 七个 Agent Harness 的综合比较

本章回到全书最初的教学案例：[用户要求系统在已有仓库中定位并修复配置解析错误、运行测试并解释修改](00_index.md#一句话请求先要落到正确的工作区)。这句话在七个系统中都可能得到可用结果，但结果怎样形成，取决于[运行循环（Harness Loop）](05_harness_loop.md#为什么一次响应不等于一个-agent)、[会话（Session）](12_session_persistence_and_resume.md#session-保存的任务边界)、[本轮上下文（Context）](07_context_and_instruction_system.md#context-为什么不只是-prompt)、[工具调用（Tool Call）](08_tool_call_system.md#工具如何成为模型的行动空间)、[权限与执行环境](17_security_permissions_and_sandboxing.md#主体能力与信任边界)怎样组合。前面的机制章已经逐项拆开这些责任，个案章又说明了每个系统为何采用特定组合。本章只综合这些已有结论，不把功能数量、界面数量或项目规模改写成排名。

比较的基本单位也不是模型回答，而是从请求进入[工作区（Workspace）](18_code_editing_git_and_workspace.md#workspace-发现与作用域)，到形成可检查[任务产物（Artifact）](04_reference_architecture.md#八个核心对象一项任务由什么组成)的完整路径。模型能否提出正确修改只是其中一环。[统一参考架构](04_reference_architecture.md#总体结构控制平面决定执行平面行动)还要求说明谁组织任务、谁决定模型看到什么、谁批准和执行动作、什么状态能够恢复，以及最终代码差异（diff）与测试怎样证明任务完成。只有把这些责任放回同一条链，七个 Harness 的差异才具有工程意义。

## 回到比较问题

横向能力地图提出了四个决定体验的问题：谁推进任务，模型看见什么，行动怎样跨入现实世界，任务怎样保持连续。[这四个问题](02_horizontal_capability_map.md#先抓住四个决定体验的问题)仍是综合比较的主轴，但经过机制章与个案章之后，还需要补上一个更深的判断：系统把控制状态集中在哪里。控制中心决定了失败首先在哪里被解释，也决定新增能力会扩大哪一类维护成本。

| 比较问题 | 需要观察的机制 | 不能据此直接推出 |
|---|---|---|
| 任务怎样推进 | [轮次（Turn）、行动、环境观察（Observation）与终止](05_harness_loop.md#turn状态与循环不变量) | 模型调用次数越多，任务就越自主或越可靠 |
| 模型看见什么 | [指令层级、Workspace 与动态 Context](07_context_and_instruction_system.md#context-为什么不只是-prompt) | 输入越长，模型掌握的事实就越完整 |
| 行动怎样发生 | [工具模式定义（Schema）、调用标识（Call ID）、审批与执行结果](08_tool_call_system.md#请求参数与-call-id) | 工具已注册或获准，就已经成功执行且可以回滚 |
| 任务怎样连续 | [Session、任务恢复（Resume）、分支（Branch）与派生（Fork）](12_session_persistence_and_resume.md#resumereplaybranch-与-fork) | 历史能够读取，外部文件、进程和网络状态就已恢复 |
| 系统怎样演进 | [扩展生命周期](09_plugins_mcp_and_extensions.md#发现注册与生命周期)与[配置来源](22_configuration_identity_and_supply_chain.md#配置层级与覆盖规则) | 扩展入口越多，系统越适合所有部署环境 |

表中的五个问题必须一起使用。Aider 可以在较少通用运行时（Runtime）对象下形成紧密的代码编辑闭环，Codex 可以用更细的线程（Thread）、Turn、工作单元（Item）和安全状态支持多入口，Pi 可以让宿主自行组合治理。三者的差异不是“功能完整”和“功能不足”，而是责任被放在了不同位置。[横向地图归纳的四种控制中心](02_horizontal_capability_map.md#四种控制中心)与七篇个案共同支持这一判断。

因此，本章不建立单一总分。一个系统在本地 Git 编辑中路径短，不等于它适合多客户端远程控制。一个系统具有事件日志、插件和子 Agent，也不等于它对小任务的部署与调试成本更低。公平比较应先固定任务、入口、权限、工作区、模型和验证要求，再判断所选架构是否把关键状态放在可观察、可控制的位置。[核心能力地图](02_horizontal_capability_map.md#核心能力地图)和[Harness Eval 的比较边界](19_observability_evaluation_and_replay.md#harness-eval-与模型-eval)都采用了这一口径。

## 架构类型与谱系

七个系统可以按责任聚合方式分成四条架构谱系。这里的“谱系”描述控制中心与扩展方向，不表示线性年代或高低阶段。第一条是[编辑事务中心](29_aider.md#coder-abstraction-与核心循环)。Aider 以 Coder、编辑格式、仓库地图（Repo Map）、Git、静态检查（Lint）与可选测试（Test）形成集中闭环，模型输出首先被解释为可检查的代码修改。它的主要优势来自专门化：编辑匹配错误能直接进入反思，用户改动与 Agent 改动可以借助 Git 基线区分。相应地，通用工具注册表（Tool Registry）、多客户端 Session 和动态扩展并不是默认核心。

第二条是[分层 Session 运行时](04_reference_architecture.md#七个系统怎样落在这张架构图上)。Codex、Gemini CLI、Goose 与 OpenCode 都把会话、工具状态和事件（Event）放在比单次回复更中心的位置，但内部重心不同。Codex 让 Thread Manager、Core Session、协议（Protocol）与 Rollout 统一多入口的任务身份。Gemini CLI 让模型 Turn 与独立工具调度器（Tool Scheduler）分工。Goose 以 Rust Core、SessionManager、模型服务提供者（Provider）与模型上下文协议扩展（Model Context Protocol Extension，MCP Extension）连接本地和协议入口。OpenCode 则让服务端（Server）成为 Session、权限和客户端事件的权威边界。这些差异分别由[Codex 的共享 Core](23_codex.md#多入口共享-core-session)、[Gemini CLI 的独立 Scheduler](26_gemini_cli.md#独立-tool-scheduler把模型流与副作用提交拆开)、[Goose 的入口与执行边界](28_goose.md#rust-coreclidesktop-与-api)和[OpenCode 的 Server 状态层](24_opencode.md#server-作为权威状态层与多客户端)展开。

第三条是[组合式插件图](27_deepseek_harness.md#插件图与依赖注入装配)。DeepSeek Harness 不把一个固定产品行为写死在主 Loop 中，而是由 Profile、Bundle、Cordis Service、Fiber 和 Agent Scope 装配 Provider、Session、Tool、权限、沙箱与自动化。插件图同时承担依赖与释放关系，使替换和热重载成为系统能力，也使组合正确性、服务代际和格式迁移成为主要维护对象。它与普通“核心加插件（Plugin）列表”的区别，在于当前产品到底具有什么能力，本身就是运行时装配结果。

第四条是[可编程小内核](25_pi.md#极简内核的取舍什么不做以及为什么)。Pi 固定模型抽象、Agent Loop、工具结果（Tool Result）、Session tree 与事件接缝，把规划模式（Plan Mode）、权限（Permission）、MCP 和子智能体（Subagent）等高级政策留给扩展（Extension）或宿主。这一取舍降低了默认路径中的政策耦合，却要求使用者明确选择扩展、冲突规则和外部隔离。它和 DeepSeek Harness 都具有深扩展面，但前者强调稳定小内核与宿主组合，后者强调服务图本身的动态装配，二者不能合并成同一种“插件式架构”。

这四条谱系并不互斥。Goose 既是 Session 运行时，也把 MCP 作为主要外部能力边界。OpenCode 既是 Server 平台，也允许进程内 Plugin 深入生命周期。Gemini CLI 既有明确 Core，也用 Extension 聚合 Policy、钩子（Hook）、技能（Skill）与 Agent。综合比较真正要找的是出现歧义时的第一责任点：Aider 回到编辑与 Git，Codex 回到 Thread 与安全控制面，Gemini CLI 回到 Scheduler 与 Policy，OpenCode 回到 Server Session，Goose 回到 Core 与 Extension Manager，DeepSeek Harness 回到插件图和 Scope，Pi 回到小内核接缝与宿主。这一归纳与[统一参考架构中的责任聚合比较](04_reference_architecture.md#七个系统怎样落在这张架构图上)一致。对 13 个开源 Coding Agent 固定提交的独立源码分类也得到相近方法论结论：Loop、工具、状态和 Context 策略更适合按多个可组合维度描述，而不是压成互斥产品类别 [@rombaut2026insidescaffold]。

## Loop、状态与上下文

所有样本都实现了行动、执行、环境观察（Observation）和继续判断的闭环，但它们选择的最小可控单位不同。[七个系统的 Loop 对照](05_harness_loop.md#七个系统如何组织-loop)显示，Aider 以一次编辑事务及其反思为中心。Codex 与 OpenCode 让持久 Session 中的 Turn、Item 或 Message Part 承担状态。DeepSeek Harness 显式保存 Turn/Step 事件并让并行结果按模型顺序收敛。Gemini CLI 把工具批次交给独立 Scheduler。Goose 同时保留经典循环与可选状态机。Pi 则用小型事件循环处理工具批次、steering 与 follow-up。差异的实质是继续条件、并发提交和终态由哪一层拥有，而不是界面上是否显示“Agent 正在思考”。

状态越结构化，越容易支持流式界面、取消、恢复和多客户端，却也需要维护更多顺序不变量。Codex 要协调 Event、Rollout flush 与 Turn 终态，OpenCode 要让数据库 Part、运行状态与客户端事件一致，DeepSeek Harness 要维护 Event Log、Surface 和替换来源。Aider 的状态面较小，却能把编辑失败、Lint 和 Test 直接变成反思输入。[观测章节对规范状态与遥测（Telemetry）距离的比较](19_observability_evaluation_and_replay.md#七个系统比较)说明，结构化状态既增加诊断能力，也增加敏感内容、投影和版本治理责任。

Context 路线同样与控制中心一致。Aider 用显式全文文件和 Repo Map 提供结构先验。Codex 把项目指令、环境和工具计划固化为 Step 级现场。Gemini CLI 合并分层指令、IDE 现场、搜索与工具目录。OpenCode、Goose 和 DeepSeek Harness 通过 Session、扩展或 Scope 持续装配。Pi 以可重建系统提示和 Extension 改写保持小核心。[七系统 Context 策略](07_context_and_instruction_system.md#七个系统的上下文策略)支持一个共同结论：第一轮预装配与后续按需读取必须配合，单独依赖全量注入或临时搜索都会在窗口、时效性或规则发现上付出代价。

上下文变长后，各系统也没有收敛到一种压缩方法。Aider 摘要较早历史并控制 Repo Map，Codex、Gemini CLI 与 Pi 把压缩放入 Turn 生命周期，Goose 与 OpenCode 改变 Session 的模型可见投影，DeepSeek Harness 则分开原始 Event、Surface replacement 与外置 Artifact。[上下文压缩（Compaction）对照](13_compaction_and_context_management.md#七个系统的机制与失效模式)表明，可靠性不取决于摘要文字是否流畅，而取决于目标、未决调用、最近修改、Tool pairing 与原文 locator 是否仍可追踪。相应地，[可检索记忆（Memory）的七系统比较](10_memory.md#七个系统的实际机制)也说明跨任务经验、当前 Session 历史和压缩摘要必须继续分层。

令牌（Token）与成本控制最终是质量约束。Repo Map、Tool Result 外置、稳定前缀、提示缓存（Prompt Cache）、弱模型、辅助搜索和 Subagent 都可能减少主 Context 压力，也可能把成本转移到额外调用、存储或父子任务汇聚。[七系统 Token 指标与质量边界](14_token_efficiency_and_cost_control.md#七系统指标与质量边界)因此要求比较每个成功任务的总资源，并同时检查目标、约束、退出状态、diff 和测试是否保留。只报告输入 Token 或缓存命中率，无法说明 Harness 是否以更低成本完成了同一工程任务。

## Tool、扩展与接口

Tool 层最明显的分叉，是专用行动协议与通用工具运行时。Aider 的 Edit Format 把代码修改表达为整文件、搜索替换、Diff 或 Patch，再由解析器、文件准入和 Git 路径处理。其他六个系统更普遍地使用 Tool Schema、Call ID、状态和结构化 Tool Result。[七系统 Tool-call Envelope](08_tool_call_system.md#七系统-tool-call-envelope-对照)说明，两种路线都必须让现实错误回到下一轮，但通用运行时更自然地支持动态工具、并行、协议客户端和多界面，专用编辑协议则能提供更精确的匹配诊断与修改反馈。

扩展机制不能压成一列“支持或不支持”。Codex 与 Gemini CLI 让受管理包贡献多类资源。DeepSeek Harness 让 Cordis Plugin 和 Service 构成产品图。OpenCode 与 Pi 允许进程内扩展深入模型、工具、Session 和界面。Goose 以 MCP Extension 作为主要外部能力边界。Aider 保持固定编辑核心，把较多集成留在 CLI、编辑器和外部进程。[七个系统的扩展路径](09_plugins_mcp_and_extensions.md#七个系统的扩展路径)表明，跨语言互操作、同进程可编程性、统一治理和默认可预测性是不同目标，不存在一条由“扩展少”到“扩展多”的成熟度直线。

接口形态进一步揭示状态所有权。[命令行界面（CLI）、终端用户界面（TUI）、集成开发环境（IDE）、桌面端（Desktop）、网页端（Web）与软件开发工具包（SDK）](20_interfaces_and_human_in_the_loop.md#clituiidedesktopweb-与-api)只是不同入口。Aider 与 Pi 的默认路径更接近进程内交互。Codex、Gemini CLI 和 Goose 通过应用服务器（App Server）、IDE 伴随组件（IDE Companion）或 Agent 客户端协议（Agent Client Protocol，ACP）让富客户端参与。OpenCode 与 DeepSeek Web 更依赖服务端状态和订阅重建。[七系统人机边界](20_interfaces_and_human_in_the_loop.md#七个系统的人机边界)支持的结论是，多入口只有在展示、控制和状态三个契约都成立时才真正复用同一 Harness。界面能够显示工具进度，不等于它拥有权威 Session。协议能够传递审批，也不等于远端执行环境具有相同沙箱。

因此，Tool、扩展与接口应当沿一条连续责任链评估：能力从哪里发现，以什么 Schema 进入 Context，最终参数在哪里获准，哪个进程或服务执行，结果怎样关联原调用，客户端又怎样重建权威状态。[能力、协议与客户端的三层区分](04_reference_architecture.md#能力协议与客户端同一工具为什么会有不同体验)正是七系统比较中最稳定的接口坐标。

## Session、Resume 与 Multi-agent

七个系统的持久化可以概括为三种承诺强度。Aider 主要保存对话连续性。Gemini CLI、Goose 与 OpenCode 保存结构化 Session、Conversation、Message 或 Part，并在部分路径关联文件快照。Codex、DeepSeek Harness 与 Pi 更强调有序追加历史、分支或可重建投影。[七个系统的持久化路径](12_session_persistence_and_resume.md#七个系统的持久化路径)说明，格式本身不是关键，关键是活动 Turn 是否闭合、Tool Call 与结果是否关联、恢复后的 Context 是否重新装配，以及损坏尾部或版本变化如何处理。

文件恢复与任务恢复仍是两条路径。Gemini CLI 的影子 Git 检查点（Shadow Git Checkpoint）、OpenCode 的快照与恢复（Snapshot/Revert）和 Aider 的受约束 `/undo` 能在不同范围内补偿文件变化，但它们都不覆盖任意 Shell、网络、数据库和后台进程。Codex 与 DeepSeek Harness 的规范日志能表达中断或结果未知，也不能撤销现实副作用。这一共同边界由[Tool Call 和外部副作用的一致性](12_session_persistence_and_resume.md#tool-call-和外部副作用的一致性)以及[幂等性与外部副作用](21_reliability_and_resource_control.md#幂等性与外部副作用)共同支撑：Resume 的正确动作通常是重新观察，而不是自动重试或假定未发生。

多 Agent（Multi-agent）比较也必须先区分拓扑。Aider 的 Architect/Editor 是固定双阶段流水线。Codex 使用独立子线程（child Thread）与智能体关系图（Agent Graph）。OpenCode 用带 `parentID` 的子会话（child Session）。Gemini CLI 用独立 Agent executor 和 Registry。Goose 用 Summon 创建同步或异步 SubAgent Session。DeepSeek Harness 同时提供可继续 child Session 与脚本工作流（Workflow）。Pi 则用 Extension 示例启动独立进程。[七系统编排路径](16_subagents_and_orchestration.md#七个系统的编排路径)表明，这些实现分别解决规划实施、上下文隔离、并行调查、长期协作或可替换拓扑，不能仅凭“能启动子 Agent”视为同一种能力。

所有委派路径都共享一项限制：独立 Context 不等于独立 Workspace。子 Agent 即使拥有自己的模型历史、预算和工具目录，也可能与父任务或兄弟任务读写同一个仓库。取消 child 也不会撤销已经产生的修改。[共享 Workspace、竞争与结果汇聚](16_subagents_and_orchestration.md#共享-workspace竞争与结果汇聚)因此把任务分区、单一写入所有权、来源记录和父级复验列为必要条件。Multi-agent 的价值来自分离真正独立的工作，而不是把一个强依赖步骤拆成更多并发模型调用。

## Permission、Sandbox 与供应链

七个系统的安全差异可以用三个连续问题概括：模型能看见什么能力，最终动作是否获准，执行环境实际能触达什么资源。[主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)说明，工具隐藏、人工审批（Human Approval）与操作系统沙箱分别作用于不同层。Codex、DeepSeek Harness 与 Gemini CLI 把策略（Policy）、审批（Approval）和沙箱（Sandbox）拆得较细。Goose 与 OpenCode 以工具权限和扩展链为中心，并可由外部容器或部署补强。Aider 用文件准入和 Shell 确认约束集中编辑路径。Pi 明确把默认进程权限作为边界，把统一审批与强隔离交给 Extension 或宿主。[七系统安全模型](17_security_permissions_and_sandboxing.md#七系统安全模型)不支持从这些结构推出跨平台安全排名，只支持比较控制点和责任范围。

工作区信任（Workspace Trust）处理的又是启动期问题。Codex、Gemini CLI 与 Pi 都以不同方式阻止陌生项目的配置、钩子（Hook）、Extension、技能（Skill）或高权限政策自动进入 Runtime。这并不把仓库文本变成可信内容，也不批准后续 Tool Call。OpenCode、Goose、Aider 与 DeepSeek Harness 采用不同配置和装配路径，更需要部署者说明项目文件、用户配置和系统政策怎样合并。[Workspace Trust 与 Credential Isolation](17_security_permissions_and_sandboxing.md#workspace-trust-与-credential-isolation)和[七系统配置比较](22_configuration_identity_and_supply_chain.md#七系统比较)共同说明，装入门、调用门和执行边界必须分别验证。

供应链风险随扩展深度扩大，但风险形态并不相同。进程内 Plugin 继承宿主权限，stdio MCP Server 由宿主启动，远端 MCP 引入服务身份与网络，Skill 和工作流配方（Recipe）主要通过 Context 与后续动作产生影响，自动更新则替换运行制品。[扩展供应链的四道边界](09_plugins_mcp_and_extensions.md#供应链与信任边界)与[配置、身份和更新比较](22_configuration_identity_and_supply_chain.md#七系统比较)表明，来源、版本、完整性、激活范围、凭据和运行权限需要形成一条链。Goose 的 Sigstore/SLSA 更新验证只覆盖其具体 CLI 更新路径。Gemini CLI 的 Extension 完整性记录、Codex 的托管来源约束或 Pi 的 Package pin 也各自只有明确适用范围，不能互相替代。

安全控制还必须与工程验证分开。沙箱限制命令最多能改哪里，不能判断补丁是否正确。审批表达用户同意，不能证明执行成功。供应链来源证明说明制品从哪里构建，也不证明任务结果可信。[Coding Harness 的工程闭环](18_code_editing_git_and_workspace.md#coding-harness-的工程闭环)要求最终回到实际 diff、测试与构建，而[可靠性章节](21_reliability_and_resource_control.md#七个系统比较)要求取消、超时和后台资源有可解释终态。安全、可靠性与正确性相互约束，却不能被一个“安全模式”或绿色状态合并。

## 复杂度、成本与维护

Harness 的复杂度不会因架构简化而消失，只会移动位置。Aider 把主要复杂度投入编辑协议、Repo Map、Git 基线和反思。Codex 投入 Protocol、Rollout、权限层和多入口一致性。Gemini CLI 投入 Scheduler、Policy、Extension 与跨平台沙箱。OpenCode 投入 Server、数据库、客户端同步和 Plugin。Goose 投入 Provider、MCP Host、ACP 与 Recipe。DeepSeek Harness 投入插件图、Service 生命周期、Event projection 和组合迁移。Pi 则把较多复杂度转交 Extension 作者与宿主。[各个案章的代表性设计](23_codex.md#代表性设计和边界)、[OpenCode 边界](24_opencode.md#代表性设计和边界)、[Pi 的扩展治理](25_pi.md#extension-api-承担高级治理)、[Gemini CLI 的控制链](26_gemini_cli.md#本章小结)、[DeepSeek Harness 的组合失效](27_deepseek_harness.md#组合失效和安全边界)、[Goose 的定制取舍](28_goose.md#tool-visibility-与发行版定制)和[Aider 的平台差异](29_aider.md#与平台型-harness-的差异)分别给出了这些成本来源。

| 架构重心 | 主要收益 | 主要维护对象 |
|---|---|---|
| 编辑事务 | 修改、Git 与验证反馈路径紧密 | 编辑格式兼容、文件新鲜度、Git 状态、模型特例 |
| 分层 Session 运行时 | 多入口、结构化恢复和细粒度控制 | 协议版本、事件顺序、持久投影、权限组合、客户端重连 |
| MCP 与外部能力平台 | 跨语言复用和独立部署 | Server 身份、认证、连接、Schema 漂移、在途调用 |
| 组合式插件图 | 部署可以重组能力和执行后端 | 依赖、代际、热重载、释放、配置与格式迁移 |
| 可编程小内核 | 默认路径清楚，宿主可深度定制 | Extension 冲突、策略一致性、外部隔离与集成测试 |

表中的收益与成本是成对出现的。平台化并非只增加抽象，它也把原先散落在客户端和脚本中的状态提升为共同协议。小内核并非没有维护，它把维护责任转移给具体部署。选择架构时，应判断团队愿意长期拥有哪一组状态和失败模式，而不是只比较首次安装或演示任务的步骤数。这一分析与[可靠性闭环](21_reliability_and_resource_control.md#harness-的-failure-model)和[扩展生命周期](09_plugins_mcp_and_extensions.md#发现注册与生命周期)相互印证。

成本也不只指模型费用。长 Context、辅助摘要、网页搜索（Web Search）、Tool Result 存储、Subagent fan-out、后台进程、遥测和人工审批都会消耗时间或运维资源。[Token 账本](14_token_efficiency_and_cost_control.md#token-账本到底记录什么)要求区分请求压力、实际计费、辅助调用和任务质量。[观测章节](19_observability_evaluation_and_replay.md#token成本与延迟)又要求把延迟与具体模型、Tool Call、重试和终态关联。没有这两层账本，“更省”可能只是把成本从主模型移到扩展服务、子 Agent 或人的等待时间。

维护能力最终取决于能否定位失败。集中式路径较容易复现单次编辑，却可能缺少跨客户端追踪（Trace）。事件化系统能够保留丰富因果，却需要控制内容采集、数据保留和投影一致性。组合式系统还要同时观察插件代际和外部进程。[七系统观测与评测比较](19_observability_evaluation_and_replay.md#七个系统比较)因此不把日志数量当作可维护性指标，而是要求规范状态、Tool Call、资源和验证结果能够被同一任务身份关联。

## 适用场景决策

选择 Harness 应从任务和治理条件出发，而不是先选项目再为其功能寻找用途。[横向地图的控制问题](02_horizontal_capability_map.md#先抓住四个决定体验的问题)提供了统一入口。下表把七个固定版本的个案结论压缩为决策入口。它描述“何时这种责任分配更合适”，不构成产品推荐顺序。

| 系统 | 更匹配的场景 | 采用前应确认的边界 |
|---|---|---|
| [**Aider**](29_aider.md#适用场景与延伸阅读) | 目标是边界明确的本地 Git 编辑，希望 Repo Map、edit format、提交和 Lint/Test 形成紧密反馈 | 是否需要多客户端、动态 MCP、精确崩溃恢复或内建操作系统沙箱（OS Sandbox）；测试和 Git Hook 的真实配置 |
| [**Codex**](23_codex.md#适用场景与延伸阅读) | 同一 Agent 核心需要服务 TUI、IDE、Desktop 或自动化，并要求 Thread、审批、沙箱与 Rollout 共享语义 | 目标平台的沙箱与网络配置、App Server 认证、Plugin/MCP 来源以及协议维护成本 |
| [**DeepSeek Harness**](27_deepseek_harness.md#适用场景与延伸阅读) | 团队要研究或构造可替换的 Provider、Session、Tool、Sandbox、Subagent 与 Workflow 组合 | 实际 Profile 装入了什么，插件格式与持久事件如何迁移，进程内 Plugin 和开发者预览边界 |
| [**Gemini CLI**](26_gemini_cli.md#适用场景与延伸阅读) | 终端任务需要搜索、IDE Context、受管理 Extension、Plan、无界面模式（Headless）与文件 checkpoint 协同 | SDK 与 CLI 的能力差异，Extension 组合、跨平台 Sandbox、Checkpoint 覆盖范围与额外调用成本 |
| [**Goose**](28_goose.md#适用场景与延伸阅读) | 本地通用 Agent 需要自由选择 Provider，并通过 MCP、ACP 与 Recipe 接入外部能力和多种客户端 | MCP/ACP 的身份与 Context 所有权、Auto 子任务权限、远端服务生命周期和下游发行维护 |
| [**OpenCode**](24_opencode.md#适用场景与延伸阅读) | 需要 Server 作为权威状态层，以 TUI、Desktop、Web 或 SDK 操作多模型、多 Agent Session | Server 暴露与认证、服务器发送事件（Server-Sent Events，SSE）重建、进程内 Plugin、后台任务耐久性和缺少内建通用 OS 沙箱的部署补强 |
| [**Pi**](25_pi.md#适用场景与延伸阅读) | 需要直接可用又可嵌入的小型 Agent Runtime，并已有自己的扩展、容器或宿主治理方案 | 项目可信（Project Trust）与逐调用权限的区别、Extension 同权风险、默认无内建沙箱和 Subagent 示例的非耐久性 |

这张决策表之后仍需回到实际任务。若核心需求是高频、局部、可审查的仓库修改，编辑事务中心通常更直接。若需求是多个客户端共享长任务，Session 与协议边界更重要。若组织能力主要由独立服务提供，MCP 宿主（Host）的连接和身份治理会成为中心。若产品形态需要频繁重组，插件图或小内核的可编程性更有价值。相应判断分别由[代码编辑路径](18_code_editing_git_and_workspace.md#七个系统的-coding-路径)、[多客户端状态一致性](20_interfaces_and_human_in_the_loop.md#多客户端状态一致性)、[MCP Transport 与双向能力](09_plugins_mcp_and_extensions.md#mcp-transport-与双向能力)和[架构责任聚合](04_reference_architecture.md#七个系统怎样落在这张架构图上)支撑。

安全和运维条件可以改变同一选择。在可信个人工作区中，明确的人在回路和宿主权限可能足够。在陌生仓库、无人交互、远端客户端或企业环境中，Project Trust、托管配置、逐调用政策、凭据隔离、真实沙箱和审计会成为前置条件。[Headless 的人在回路边界](20_interfaces_and_human_in_the_loop.md#headless-与非交互模式)和[供应链风险](22_configuration_identity_and_supply_chain.md#供应链风险)说明，自动化程度提高时，不能只减少确认，还必须把原本由人临场判断的条件转成可执行政策和失败状态。

## 主要结论

第一，七个 Harness 的共同底座不是聊天界面，而是一个受现实反馈约束的控制循环。任何实现都要维持目标连续、行动归属、结果闭合、Observation 优先和终止可解释。差异在于这些不变量由编辑事务、Session Runtime、Scheduler、Server、插件图还是 Extension 宿主来维护。[Harness Loop 的六条关系](05_harness_loop.md#本章小结)是理解所有个案的共同起点。

第二，架构选择首先是责任选择。Aider 把责任收紧到 Git 编辑闭环，Codex、Gemini CLI、Goose 与 OpenCode建立不同形态的 Session 平台，DeepSeek Harness 把装配本身变成架构，Pi 则固定小内核并开放深接缝。[横向控制中心](02_horizontal_capability_map.md#四种控制中心)解释了为什么相似用户体验背后会出现完全不同的调试、扩展与恢复成本。

第三，Context、Session、Memory 与 Compaction 不能互相代替。保存更多历史不保证模型本轮看见正确事实，摘要更短不保证未决状态仍然存在，跨任务记忆也不能替代当前文件和测试的新观察。[统一参考架构的信息分层](04_reference_architecture.md#本轮上下文可检索记忆与压缩保存和看见是两回事)与[Compaction 的共同正确性问题](13_compaction_and_context_management.md#本章小结)共同限定了长任务的质量边界。

第四，Tool 可见、动作获准和执行可达是三种事实。MCP、Plugin、Skill、Hook、Recipe 或智能体模式（Agent Mode）可以改变能力表面，却不能自动提供最小权限、事务或结果正确性。审批、沙箱、凭据和最终验证必须继续分层。[Tool 权限边界](08_tool_call_system.md#权限和副作用边界)与[安全控制链](17_security_permissions_and_sandboxing.md#本章小结)是综合比较中最不能被功能表省略的部分。

第五，Resume、Revert、取消（Cancel）与 Multi-agent 都会扩大状态空间，却不会自动扩大完成证明。恢复后要重新观察外部世界，撤销只在明确覆盖范围内成立，子 Agent 的结果必须回到父任务和当前 Workspace 验证。[Session 的副作用边界](12_session_persistence_and_resume.md#本章小结)和[多 Agent 的责任分配](16_subagents_and_orchestration.md#本章小结)说明，连续性和并行性越强，来源、资源所有权与验收规则越需要结构化。

第六，复杂度应按任务、治理和维护能力匹配。专用闭环、分层 Runtime、MCP 平台、组合式插件图与小内核都能形成合理系统，也都会在不同位置留下协议、配置、供应链、隔离、观测或集成责任。[可靠性与资源控制](21_reliability_and_resource_control.md#本章小结)要求这些责任在失败时能够收敛，[配置、身份与供应链](22_configuration_identity_and_supply_chain.md#本章小结)则要求它们在升级和扩展时仍能说明来源。

回到最初的配置解析错误，七个 Harness 真正不同的不是谁能够生成那段补丁，而是谁确定工作区、谁组织调查、谁控制修改、谁保存中断状态、谁承担扩展和凭据风险，以及谁在最后证明 diff 与测试仍然成立。综合比较的目的正是把这些责任显现出来。选择或设计 Harness 时，只要沿[请求到验证的完整工程闭环](18_code_editing_git_and_workspace.md#coding-harness-的工程闭环)逐段追问，系统的收益与代价就能落回可检查的边界，而不会退化为功能清单或产品排名。
