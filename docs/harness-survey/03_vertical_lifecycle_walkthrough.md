# 一次 Coding Agent 任务的纵向生命周期

**状态：提纲，待调查。** 本章以同一个修复请求串联 Harness 的潜在状态转换，目的不是断言七个系统均按该顺序执行。章节目标是使读者能把横向机制放回一次 Coding Agent 任务的时间线；读完后应能分辨请求、会话准备、模型循环、执行审批和持久化各自的输入/输出。它承接[横向能力地图](02_horizontal_capability_map.md)的比较轴，并使用[统一参考架构](04_reference_architecture.md)定义 Session、Turn、Event 与 Artifact。

## 从修复请求到可执行任务

贯穿案例是：用户要求 Agent 在已有仓库定位并修复配置解析错误，运行测试并解释修改。Harness 首先需把自然语言目标与当前工作区、代码约束和风险边界放在同一任务上下文中；“可执行”并不意味着已经允许写文件或执行 Shell，而是说明请求已有足以进入后续决策的标识、输入和策略来源。

调查将比较 Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 如何接收或规范化该请求：是 CLI 输入、交互界面、SDK/协议消息还是恢复会话中的新 Turn，以及项目级指令、配置和工作区发现何时参与。这里不预设它们支持相同的计划对象；计划、todo 或 goal 的真实语义留待[第十五章](15_goals_planning_and_todos.md)通过源码路径确认。

**图表计划：** 绘制从“修复请求”到“解释修改”的泳道图，泳道为用户、控制平面、模型/provider、工具执行环境和持久化存储；每个箭头标记为候选状态转换，并以虚线表示尚待逐系统核验的分支。

## Session、指令与上下文准备

在参考模型中，Session 承载跨 Turn 的任务边界，Context 是当前模型调用可见的信息集合；二者不应混同。准备阶段可能读取系统提示、用户输入、仓库指令、文件摘要、Git 状态、模型设置和历史消息，也可能建立或选择一个恢复点。这里的关键问题是哪些输入进入模型、哪些仅留在控制面，以及它们在下一 Turn 是否仍然有效。

后续调查应沿各系统的 session 与 context 入口查验组装次序、截断/过滤、项目作用域和错误处理。特别是不要以 UI 上显示的聊天记录推定完整 prompt，也不要将“存在 session 文件”推定可恢复完整执行状态；[第七章](07_context_and_instruction_system.md)、[第十二章](12_session_persistence_and_resume.md)和[第十三章](13_compaction_and_context_management.md)将分别给出证据。

**代码证据计划：** 候选入口包括 Codex 的 `codex/codex-rs/code-mode-protocol/src/session.rs`，DeepSeek Harness 的 `deepseek-harness/packages/core/session/`，Gemini CLI 的 `gemini-cli/packages/cli/src/acp/acpSession.ts`，Goose 的 `goose/crates/goose/src/session/session_manager.rs`，OpenCode 的 `opencode/packages/protocol/src/groups/session.ts`，Pi 的 `pi/packages/agent/src/harness/session/context.ts`；Aider 的会话/提示入口须从 `aider/aider/coders/base_coder.py` 继续定位。这些仅为待调查路径。

## 模型、Tool Call 与 Observation 循环

当 Context 已准备，Harness 向模型/provider 发起一次 Turn 的请求，接收文本、流式 Event 或结构化 Tool Call，并将工具结果作为 Observation 纳入后续决策。这个循环的分析重点不是模型“思考”内容，而是请求边界、增量事件、调用 ID、工具参数规范化、结果关联、终止条件和模型/工具错误怎样改变可见状态。

七个系统可能采用不同协议、不同并发策略或不同 tool schema；本章只给出统一问题：模型输出是什么对象，何处变为可执行动作，结果如何配对回会话，何时继续或停止。实现调查需同步检查未知工具、无结果调用、流中断和 provider 拒绝，后续由[第五章](05_harness_loop.md)、[第六章](06_model_and_provider_abstraction.md)和[第八章](08_tool_call_system.md)分别展开。

**安全分析计划：** 把模型输出视为不可信的行动提议，逐段标注 schema 校验、tool allowlist、参数重写、审批、超时和错误回传的责任方。调查 `goose/crates/goose/src/agents/state_machine/ops_toolcalling.rs`、`opencode/packages/codemode/src/tool-runtime.ts`、`pi/packages/agent/src/harness/tools/tool-context.ts` 等待核实入口时，必须追到拒绝和测试路径才描述控制效果。

## 权限、执行与错误恢复

Tool Call 变成副作用之前，Harness 可能询问用户、应用 policy、在受限环境执行或直接拒绝；执行之后可能得到正常结果、部分失败、超时、取消或不可重试错误。纵向分析应区分“模型提出动作”“界面显示确认”“policy 作出决定”“子进程实际执行”四个位置，因为它们可由不同组件负责，也可能在不同客户端中变化。

贯穿案例中的文件修改、测试命令和 Git 检查应被当作三类待验证副作用，而非默认安全操作。后续应比较七系统如何保留请求、批准、命令、退出状态和错误文本的关联，以及恢复时是否重复、跳过或重新征求批准；详细安全论证留给[第十七章](17_security_permissions_and_sandboxing.md)，代码闭环留给[第十八章](18_code_editing_git_and_workspace.md)，可靠性边界留给[第二十一章](21_reliability_and_resource_control.md)。

**代码证据计划：** 待沿 `codex/codex-rs/mcp-server/src/exec_approval.rs`、`deepseek-harness/packages/interaction/permission-presets/`、`gemini-cli/packages/cli/src/ui/commands/permissionsCommand.ts`、`goose/crates/goose/src/permission/permission_judge.rs`、`opencode/packages/tui/src/routes/session/permission.tsx` 追踪 policy 到执行器；Aider 与 Pi 的对应路径须以运行入口和 tests 继续确认，不能由缺少显眼文件名反推机制不存在。

## 上下文压力、记忆与委派

长任务会让当前模型上下文接近窗口限制，Harness 可能截断、压缩、摘要、检索持久内容，或把部分工作委派给子 agent。为了避免概念漂移，本章只描述它们在时间线中可能出现的位置：Compaction 改写当前 Context，Memory 提供跨时段可取回信息，Subagent 则创建另一条或嵌套的工作流；三者的最小边界以[第四章](04_reference_architecture.md)为准。

需要分别调查七系统触发条件、状态归属、可见性、失败回退和合并策略。一个“memory”目录、摘要字符串或并发 API 都不足以证明长期记忆、自动压缩或委派安全；[第十章](10_memory.md)、[第十三章](13_compaction_and_context_management.md)、[第十四章](14_token_efficiency_and_cost_control.md)和[第十六章](16_subagents_and_orchestration.md)将以实际实现和测试决定这些标签。

**学术检索计划：** 以“long-context agent state management”“summarization-induced information loss”“delegated software-agent accountability”为检索问题；仅在验证原文后，讨论压缩可能造成的证据损失、记忆的可追溯性和委派的责任链，而不将任何一项理论保证归于本样本。

## 验证、持久化与 Resume

任务接近完成时，Harness 需要把修改、测试、解释与会话记录分别对待：测试是对代码行为的有限证据，diff/Git 状态是工作区副作用的证据，摘要是给用户的解释，持久化记录则决定能否恢复或审计。一个成功文本回复不能替代测试成功，也不能说明全部状态已经安全保存；反过来，存在历史记录也不必然代表可以恢复中间工具执行。

调查会沿 session store、事件日志、导出/恢复命令以及相应测试，识别复原的单位和不变量：是 Session、Turn、消息、执行队列还是仅文本 transcript。比较结果应回写到[第十二章](12_session_persistence_and_resume.md)和[第十九章](19_observability_evaluation_and_replay.md)，并为贯穿案例留下可审计的“修改—测试—解释”链，而不是只记录最终答案。

**图表与证据计划：** 以状态机图展示创建、执行、等待批准、失败/取消、完成和恢复等候选状态；用实线表示已由调用链和测试核验的转移，用虚线表示待验证转移。候选入口含 `goose/crates/goose/src/acp/server/load_session.rs`、`opencode/packages/core/test/session-runner.test.ts`、`pi/packages/coding-agent/test/suite/agent-session-runtime.test.ts` 和 Gemini CLI 的 `packages/cli/src/ui/components/SessionBrowser.tsx`，均须继续追踪存储与恢复实现。

## 七个系统的路径差异

统一时间线是比较镜头，不是约束七个项目的真实控制流。Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 可能在入口、状态粒度、provider 适配、工具执行、审批、扩展和恢复处产生分叉；每条分叉应先映射到参考对象，再以项目特有术语和源码路径解释。若某机制不适用，应说明任务边界或证据缺口，不将其标成落后或缺失。

后续个案章须以“同一案例在该 Harness 中经过什么状态、哪些边界由谁控制、发生失败时如何收束”为叙事主线，而不是重复横向矩阵。为了减少误读，个案章还应反查本章的每个时间段是否有源码、测试或记录支撑；无法验证的路径保留 Inferred 或待调查标记。

## 本章小结

本章将修复配置解析错误的请求拆为任务形成、Context 准备、模型—工具循环、受控执行、上下文压力、验证与恢复，并为七系统的可能分叉保留验证接口。读者下一步可回到[统一参考架构](04_reference_architecture.md)查看这些阶段操作的共同对象，或进入[第五章](05_harness_loop.md)检查循环的不变量和终止条件。
