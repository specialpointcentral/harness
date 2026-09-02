# Agent Harness 设计原则

前置阅读可先看[统一参考架构](04_reference_architecture.md)与[七个系统的横向能力地图](02_horizontal_capability_map.md)，但本章也可以独立进入。这里的设计原则（Design Principle）不是要求所有 Harness 采用同一组类、数据库和界面，而是从前文机制与七个个案中提炼一组可迁移的责任边界：当实现规模、部署方式和产品定位改变时，哪些问题仍必须被明确回答。

仍以[“一句话请求先要落到正确的工作区”](00_index.md#一句话请求先要落到正确的工作区)为教学案例。用户要求 Agent 定位并修复配置解析错误、运行测试并解释修改。任务看似只关乎代码，却会依次经过工作区识别、上下文选择、模型调用、工具发现、权限裁决、真实执行、失败恢复、状态保存和结果验证。任何一层把相邻概念合并成一个模糊开关，都可能让系统在正常演示中顺利运行，却在中断、扩展、无人值守或低信任输入出现时失去可解释性。

以下每节先陈述一条原则，再说明它针对的失效模式，随后用七个固定版本说明该原则怎样被实现、弱化或外置，最后指出它会与哪些其他原则发生冲突。正例表示某个边界被清楚表达，反例表示责任被集中、交给宿主或只覆盖较窄场景；二者都用于解释取舍，不构成系统排名。

## 控制平面与执行平面

第一条原则是：把[控制平面（Control Plane）与执行平面（Execution Plane）](04_reference_architecture.md#总体结构控制平面决定执行平面行动)按责任分开。控制平面解释目标、构造本轮输入、选择能力、判断是否继续并形成授权决定；执行平面只把已经确定的动作作用到文件、进程、Git、网络或外部服务。两者可以位于同一进程，却不能共享一个含义不明的“Agent 已决定”状态。模型回复是行动提议，策略允许是准入结论，执行成功又是环境事实。

这条原则解决的主要失效，是把语言判断直接当成现实结果。若客户端边消费模型流边自行执行命令，取消可能只停止文字而没有停止进程；若执行器同时决定权限，低信任输入就可能借宿主能力越过用户意图；若界面把“已提交”显示成“已完成”，[恢复（Resume）](12_session_persistence_and_resume.md#resumereplaybranch-与-fork)会从错误边界继续。控制与执行分离，使拒绝、等待、执行中、成功、失败和结果未知能够分别闭合。

七个系统展示了从显式分层到集中事务的连续谱。[Codex 的 Core、Policy 与 Sandbox](23_codex.md#approvalsandbox-与-exec-policy)和[Gemini CLI 的独立 Tool Scheduler](26_gemini_cli.md#独立-tool-scheduler把模型流与副作用提交拆开)把模型循环、政策、审批和执行拆成连续控制点；[DeepSeek Harness 的能力接缝](27_deepseek_harness.md#cordisserviceprovider-与-consumer)让 Consumer、Provider 与真实执行世界可替换。[OpenCode 的 Server 权威层](24_opencode.md#server-作为权威状态层与多客户端)与[Goose 的 Core、ACP 和 MCP 边界](28_goose.md#rust-coreclidesktop-与-api)把客户端从主要执行状态中移开。[Pi 的三层责任分配](25_pi.md#极简核心的设计哲学)保留稳定 Loop，却把强制政策交给 Extension 与宿主。[Aider 的集中式编辑闭环](29_aider.md#coder-abstraction-与核心循环)则把控制与执行压在一个 Coder 事务周围，以 Git、文件准入和确认保持局部边界；路径更短，但通用调用身份、多客户端和强隔离需要外部补足。

分层会与简单性和低延迟冲突。独立协议、状态机和执行器增加版本兼容、序列化与故障组合；集中循环更容易理解，也更适合短编辑任务。取舍标准不是组件数量，而是自治范围和副作用半径：能力越通用、入口越多、任务越可恢复，控制决定与真实执行就越需要独立身份和终态。

## 工具发现与授权

第二条原则是：把[工具发现（Tool Discovery）](08_tool_call_system.md#schema注册表与能力发现)与[工具授权（Tool Authorization）](08_tool_call_system.md#权限和副作用边界)分开。发现决定模型当前知道哪些能力及其参数模式，授权决定某一次最终调用能否以特定身份触达特定资源。工具出现在目录中，不表示它可以无条件执行；工具未出现在模型的[本轮上下文（Context）](07_context_and_instruction_system.md#context-为什么不只是-prompt)中，也不表示同进程[插件（Plugin）](09_plugins_mcp_and_extensions.md#pluginextensionmcpskill-与-hook)已失去底层权限。

合并两者会产生两种相反失效。其一是“已安装即已授权”：模型上下文协议服务器（MCP Server）、扩展（Extension）或命令解释器（Shell）一旦进入注册表，模型生成的任何参数都被放行。其二是“隐藏即安全”：系统只减少工具模式定义（Tool Schema），却没有约束 Extension、子进程或客户端仍可直接访问的资源。前者把供应链信任扩大为运行期权限，后者把 Context 优化误当成执行隔离。

[Codex 的 Step Context 快照](23_codex.md#mcpskillpluginmemory-与-subagent)让本轮工具目录与实际扩展代际对齐，调用仍进入 Exec Policy、Approval 和 Sandbox；[Gemini CLI 的 Folder Trust、Registry 与 Policy Engine](26_gemini_cli.md#folder-trust-与-policy-engine先决定装入什么再裁决每次行动)先控制项目贡献，再逐调用裁决。[OpenCode 的 Agent 权限与工具过滤](24_opencode.md#providertoolplugin-与-mcp)让 Plan、Build 和 Subagent 看见不同能力；[Goose 的 Tool Visibility](28_goose.md#tool-visibility-与发行版定制)明确只改变模型可见面，Permission 与执行环境另行决定。[DeepSeek Harness 的 Tool Pipeline](27_deepseek_harness.md#toolmcpacpskill-与-subagent)允许原生工具与代码模式共用同一 Guard、审批和执行链。[Pi 的默认四工具与 Tool Hook](25_pi.md#无内建通用-permission-system)证明小目录也需要调用前政策，同时承认同进程 Extension 不受该门强制隔离。[Aider 的文件准入和 Shell 明示确认](29_aider.md#与平台型-harness-的差异)提供窄而直接的人类授权，却没有平台型动态工具目录的统一治理面。

这条原则与可发现性和[令牌（Token）效率](14_token_efficiency_and_cost_control.md#减少输入与选择上下文)互相拉扯。目录过大增加选择错误和 Context 成本，过滤过严又会让模型无法提出本可安全完成的动作；逐调用询问提高意图清晰度，却会造成确认疲劳。较稳妥的组合是按任务阶段收窄可见能力，以确定性政策自动处理明确允许和明确拒绝，只把权限扩张、外部副作用和意图不确定交给人，同时让执行限制始终存在。

## Context、Memory、Session 与 Compaction

第三条原则是：让本轮 Context、[可检索记忆（Memory）](10_memory.md#memory-与-session-状态的区别)、[会话（Session）](12_session_persistence_and_resume.md#session-保存的任务边界)与[上下文压缩（Compaction）](13_compaction_and_context_management.md#截断摘要选择与外部化)分别承担“现在看见什么”“以后能取回什么”“任务保存了什么”和“窗口压力下怎样改变表示”。Session 可以保存完整历史，Context 仍只是一轮投影；Compaction 产生有损工作单元（Item），不能自动取得原始[事件（Event）或任务产物（Artifact）](04_reference_architecture.md#八个核心对象一项任务由什么组成)的证据地位；Memory 命中也必须允许当前工作区的新事实推翻。

这条原则针对的是状态层相互冒充。把摘要当成真实历史，会把“测试尚未完成”压成“测试已经处理”；把聊天恢复当成任务恢复，会忽略分支、依赖和后台进程已经变化；把项目约定写入全局 Memory，会让一个仓库的经验污染另一个仓库。摘要研究已经表明，流畅文本仍可能包含原材料不支持的新增或误述 [@maynez2020faithfulness]；因此来源、范围、时间和可定点复查位置是长任务正确性的一部分。

[DeepSeek Harness 的 Event Log 与 Surface](27_deepseek_harness.md#事件溯源-session-与-surface--日志分离)最明确地区分保存事实、模型视图和 Transcript；[Codex 的 Rollout、Memory 与 Turn 快照](23_codex.md#loopevent-与-rollout)也把任务记录、跨任务材料和本轮配置分开。[OpenCode 的 Session、Message、Part 与 Compaction](24_opencode.md#session存储与-subagent)和[Pi 的 JSONL Session tree](25_pi.md#extensionpromptskill-与-session-backend)保留分支历史，同时承认压缩只改变模型可见投影。[Goose 的 agent-visible 历史与项目/用户 Memory](28_goose.md#context-management-与-delegation)把原消息、摘要和跨任务存储置于不同范围。[Gemini CLI 的 Session 与 Shadow Git Checkpoint](26_gemini_cli.md#shadow-git-checkpoint把恢复点放在用户仓库之外)把对话位置和文件恢复点绑定，却不宣称网络副作用可回滚。[Aider 的 Markdown 历史、Repo Map 与摘要](29_aider.md#多模型弱模型与-token)为集中编辑提供连续性，但对在途工具、持久审批和跨任务语义 Memory 的承诺更窄。

分层与存储成本、隐私和交互连续性冲突。保留原始 Event 有利于审计，却扩大敏感数据和迁移负担；积极压缩降低 Token，却增加摘要漂移；广泛 Memory 提高复用，却放大陈旧信息与污染传播。设计者应优先保存身份、来源、未决状态和可检查 Artifact，再根据任务价值决定保留原文、外置定位引用（locator）或有损摘要，而不是把“保存更多”或“压缩更多”设为单一目标。

## 权限、身份与外部副作用

第四条原则是：让权限随[能力（Capability）、主体（Principal）和信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界)传播，并为每项[调用来源（Call Provenance）](22_configuration_identity_and_supply_chain.md#agent-identity-与调用来源)和外部副作用（External Side Effect）保留可核对身份。权限不应绑定“当前 UI 是安全模式”或“父 Agent 已经批准”这类宽标签，而应落到最终工具、参数、路径、网络目标、Credential、调用者和作用域。最小权限与完全仲裁要求能力尽可能收窄，并在每次访问时重新检查 [@saltzer1975protection]。

它主要防止混淆代理和重复副作用。低信任仓库文本可能说服模型调用高权限 Shell，Subagent 可能沿父 Session 获得不必要的写入和网络，断线后的自动重试可能重复创建远端资源。若系统只记录“用户已登录”而不记录 Agent、客户端和委派 lineage，就无法解释谁代表谁行动；若审批与 Credential 注入混在同一进程环境中，获准的一项服务访问还可能把长期秘密暴露给其他工具。

[Codex 的 originator、SessionSource、Approval 与 Credential Broker](23_codex.md#approvalsandbox-与-exec-policy)把调用来源、意图和实际可达性分层；[Gemini CLI 的 Policy、Subagent 身份和 Sandbox 扩权](26_gemini_cli.md#permissionsandbox-与-subagent)使子任务与临时权限仍回到同一决策链。[DeepSeek Harness 的 Scope、Approval 与可组合 Sandbox](27_deepseek_harness.md#可组合沙箱与策略接缝)能按 Agent 收窄可见能力，并把文件政策完整性作为结果报告。[OpenCode 的 child Session 权限继承](24_opencode.md#session存储与-subagent)保留父子来源，但进程内 Plugin 与普通 Tool 规则仍共享宿主故障域。[Goose 的 ACP、MCP 与 Auto Subagent](28_goose.md#context-management-与-delegation)扩大了身份边界，也说明审批通道不完整时必须在装配前收窄能力。[Pi 的 Project Trust 与外部隔离](25_pi.md#权限与外部隔离边界)清楚承认进程内 Hook 不是强制边界。[Aider 的文件确认、Shell 同意和 Git 归属](29_aider.md#git-commitlint-与-test)适合开发者现场监督，却更多依赖宿主账号和容器等外部限制。

权限收窄会与通用 Shell、扩展自由和无缝委派冲突。能力粒度越细，策略和审批越难维护；Credential 越晚注入，Provider 与工具适配越复杂；子 Agent 完全隔离又会失去共享工作区带来的效率。应优先保证权限不会因[用户界面（UI）模式](20_interfaces_and_human_in_the_loop.md#模式切换与流式反馈)、Resume 或父子关系而静默扩大，再按明确任务把只读范围、写入分区、网络目标和短期身份逐项开放。

## 失败、取消与资源上限

第五条原则是：先建立故障（Fault）、错误状态（Error）与失效（Failure）的分类，再设计取消（Cancellation）和资源上限（Resource Limit）。Provider 断流、权限拒绝、工具非零退出、测试超时、用户中断、预算耗尽和结果未知不能共享一个 `error` 分支。可靠性工程区分原因、内部偏离与用户可见服务失效 [@avizienis2004dependability]；Harness 还要补充动作是否越过副作用边界、结果是否持久化、资源是否仍活动。

没有这层分类，恢复会放大故障。认证错误进入重试风暴，超时被写成测试失败，取消只停止前台而留下进程树，结果未知的网络调用被再次发送，Subagent 或后台 Job 在父任务结束后继续消耗 Token 和端口。资源上限也不能只设置最大 Turn：时间、模型 attempt、Token、费用、并发、输出、进程和清理宽限期需要共同形成停止条件。

[Codex 的 TurnAborted、有限重试和 Session 所有资源](23_codex.md#loopevent-与-rollout)、[Gemini CLI 的批次取消与最大 Turn](26_gemini_cli.md#独立-tool-scheduler把模型流与副作用提交拆开)、[DeepSeek Harness 的 deadline、Job Registry 与持久屏障](27_deepseek_harness.md#workflowschedule-与-job)都把失败状态分配到不同层。[OpenCode 的 Session retry、BackgroundJob 与 Snapshot](24_opencode.md#后台-job-与-snapshot)区分运行取消和文件补偿；[Goose 的 CancellationToken、max turns 与异步 task](28_goose.md#context-management-与-delegation)提供有界委派，但远端 MCP 仍依赖 Server 合作。[Pi 的 AbortSignal、进程树清理与扩展调度](25_pi.md#subagent-扩展示例)显示小内核也能提供取消接缝，不过不同 Shell 或实验路径的保证不能合并。[Aider 的退避、Ctrl-C、有限反思和 Git `/undo`](29_aider.md#git-提交事务与-undo-边界)把恢复收窄到编辑事务，无法覆盖网络、后台进程和完整 Session。

这条原则与自动恢复和吞吐量冲突。更积极的 retry 与 fallback 能提高短暂故障下的完成率，却可能改变模型、费用和请求语义；硬终止缩短等待，却不给工具清理机会；严格预算防失控，也可能在接近完成时停止任务。可迁移的准则是先检查取消和副作用状态，再消耗新的 attempt；为清理保留预算；结果未知时优先查询、补偿或交给用户，而不是用重试次数掩盖不确定性。

## 可观测性与来源追踪

第六条原则是：让可观测性（Observability）与来源追踪（Provenance Tracking）从运行主路径自然产生，而不是事后解析最终回答。规范 Event 或 Item 负责说明业务状态，日志（Log）解释局部故障，追踪（Trace）连接 Session、Turn、模型请求、Tool Call 和 Subagent，指标（Metric）聚合 Token、费用、延迟和错误。Dapper 说明跨边界诊断依赖共享身份与父子关系，而非只有时间戳 [@sigelman2010dapper]；OpenTelemetry 则提供可组合信号与传播方向 [@otel2026specification]。

缺少来源会让成功和失败都无法解释。测试通过可能属于旧分支，Tool Result 可能被配到另一个并行调用，Subagent 结论可能只是自然语言总结，配置最终值可能来自用户、项目或企业层中的任一来源。反过来，把 Prompt、源码、路径、参数和结果全部发送到遥测后端，又会把诊断系统变成新的数据外传路径。观测必须同时回答关联性与最小披露。

[Codex 的 Rollout、typed Event 与 trace context](23_codex.md#rollout-持久化与-turn-边界)、[DeepSeek Harness 的规范 Session Event 和 Projection](27_deepseek_harness.md#事件溯源-session-与-surface--日志分离)、[Pi 的显式 TelemetryContext](25_pi.md#agent-coreai-abstraction-与-coding-agent)都让来源靠近运行对象。[Gemini CLI 的 conversation/call identity](26_gemini_cli.md#模型流式调用与搜索工具)和[OpenCode 的 Server Session/Event](24_opencode.md#server-作为权威状态层与多客户端)支持客户端下钻与重连。[Goose 的 Trace、usage ledger 和可选内容采集](28_goose.md#rust-coreclidesktop-与-api)把结构属性与正文开关分开。[Aider 的 Git commit、diff、测试和 opt-in analytics](29_aider.md#git-commitlint-与-test)对编辑结果提供强局部来源，却没有平台型跨组件 Trace 的同等中心。

可观测性会与隐私、性能和实现独立性冲突。规范 Event 不能依赖可能丢失的 exporter，遥测（Telemetry）失败也不能改变任务结果；高基数 Session ID 适合 Trace，不适合长期 Metric 标签；内容采集应默认最小化，并提供显式开启、脱敏、保留和删除语义。最重要的不是日志数量，而是用户最终能从 Artifact 回到任务、调用、身份、版本与现场。

## 渐进自治与 Human-in-the-loop

第七条原则是：采用渐进自治（Progressive Autonomy），把[人在回路（Human-in-the-loop，HITL）](20_interfaces_and_human_in_the_loop.md#审批编辑与中断)放在不确定性、权限扩张和不可逆后果增加的位置，而不是把系统分成“全自动”与“每步确认”。人在信息获取、方案判断、行动选择和后果实施中可以承担不同角色 [@parasuraman2000automation]；混合主动设计进一步要求系统依据动作价值、代价和意图不确定性决定何时交还主动权 [@horvitz1999mixedinitiative]。

过少介入会让模型在错误工作区、旧 Context 或恶意 Observation 下持续扩大副作用；过多介入则产生确认疲劳，用户最终会机械批准。[无界面（Headless）路径](20_interfaces_and_human_in_the_loop.md#headless-与非交互模式)还会暴露隐藏失效：交互版依赖弹窗才能继续，自动化版却没有稳定政策，只能永久等待或默认允许。渐进自治要求模式切换改变真实工具和权限，审批展示最终参数，拒绝和无人应答形成明确终态，并让用户可以编辑、取消和恢复。

[Aider 的文件准入、Shell 确认和 Architect/Editor](29_aider.md#edit-format-与代码修改)把人放在集中编辑事务附近；[Codex 的 TUI、exec 与 App Server](23_codex.md#cliide-与服务入口)让交互、无人值守和富客户端共享 Core，但采用不同审批能力。[OpenCode 的 Plan/Build 权限切换](24_opencode.md#planbuild-agent-的权限切换)和[Gemini CLI 的 Plan、Policy 与 Headless fail-closed](26_gemini_cli.md#planningcheckpoint-与非交互模式)把自治阶段变成运行状态。[Goose 的 Mode、Permission 与 ACP](28_goose.md#provider-abstraction-与-acp)支持多种客户端，却必须承认 Auto Subagent 会把审批问题前移。[DeepSeek Harness 的 Web、Headless 与 automation ACP](27_deepseek_harness.md#项目定位与组合原则)让部署 Profile 决定人类通道。[Pi 的 TUI 与 Extension 治理](25_pi.md#looptool-state-与-tui)提供最大的定制空间，也意味着无 UI 时的默认策略由宿主承担。

渐进自治与速度、可预测性和跨入口一致性冲突。低风险读取可以自动继续，高风险写入却可能因频繁询问拖慢任务；远程批准保留长任务进度，也增加身份、超时和多客户端竞争。设计者应把模式视为能力集合与责任契约，让自治只在政策、预算、观测和恢复边界同时成立时提高，而不是通过隐藏确认框获得表面流畅。

## 原则冲突与取舍

这些原则不会同时达到最大值。分层控制提高可解释性，却增加协议和状态成本；最小工具集降低攻击面，却可能增加搜索轮次；完整历史利于审计，却增加隐私、迁移和 Token 压力；严格审批保护意图，却会打断用户；积极恢复提高可用性，却可能重复副作用；详细 Trace 帮助诊断，却扩大内容采集。Harness 设计的任务不是消除冲突，而是让冲突落在显式、可测试和可调整的位置。

| 冲突轴 | 偏向一侧的收益 | 另一侧的代价 | 应保留的不变量 |
| --- | --- | --- | --- |
| 集中循环 / 分层运行时 | 路径短、部署简单 / 多入口复用、故障域清楚 | 通用治理较弱 / 协议与迁移复杂 | 行动提议、授权、执行结果不能混同 |
| 能力丰富 / 最小可见 | 少往返、适应面广 / Schema 更小、误用面更窄 | 选择与安全成本上升 / 可能缺失必要能力 | 发现不等于授权，隐藏不等于隔离 |
| 完整保留 / 主动压缩 | 可审计、可复查 / Token 低、当前焦点清楚 | 隐私与存储成本 / 摘要漂移 | 来源、未决状态和 Artifact 不因摘要消失 |
| 高自治 / 强 HITL | 吞吐高、适合自动化 / 意图确认与纠正更及时 | 错误放大 / 中断与确认疲劳 | 权限扩张和高副作用必须有明确责任主体 |
| 自动恢复 / 保守停止 | 短暂故障下连续完成 / 避免重复副作用 | 重试放大成本 / 人工介入增加 | 结果未知不得被改写成未执行或成功 |
| 深度观测 / 最小披露 | 根因定位、评测与审计更强 / 隐私与后端成本更低 | 内容外传与高基数 / 诊断材料减少 | 规范状态独立于 Telemetry，关联身份仍可追溯 |

表中的不变量是取舍的底线，而不是某种推荐产品形态。Aider 证明集中式、Git-centric 路径可以在窄任务上保持强工程闭环；Pi 证明小内核可以通过接缝承载多种治理；Codex、Gemini CLI 与 OpenCode 展示分层或服务化控制面怎样支持多入口；Goose 展示协议生态怎样扩大能力边界；DeepSeek Harness 则把运行时装配本身提升为可替换对象。它们的差异说明，设计原则应约束责任与证据，而不应冻结实现拓扑。

对新的 Agent Harness，最实用的检查顺序是沿一次真实任务追问：谁拥有当前任务身份，模型这轮看见什么，能力从何处发现，最终参数由谁授权，哪个执行器以什么身份产生副作用，失败后哪些事实已经提交，取消后哪些资源仍活动，结果怎样回到 Session 与用户，未来又怎样证明来源。只要这些问题有明确答案，系统可以选择集中、分层或组合式架构；若答案只能依赖界面标签、模型自述或一条最终成功消息，再丰富的功能也无法形成可迁移的工程保证。
