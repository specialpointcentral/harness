# 七个 Agent Harness 的横向能力地图

**状态：提纲，待调查。** 本章不发布七个系统的已完成能力清单，而是定义一张可随着源码证据填充的比较地图。章节目标是把同一 Coding Agent 问题分解为稳定的比较轴；读完后应能判断一项观察属于控制面、执行面、状态面还是扩展面，并知道何时必须转入纵向或个案章节。它承接[范围、术语与研究方法](01_scope_and_methodology.md)的证据纪律，并把地图中的对象名交由[统一参考架构](04_reference_architecture.md)解释。

## 用什么轴比较 Harness

横向比较的单位不是“功能有无”，而是可定位的机制与设计取舍。初始轴包括：任务与会话的编排位置，模型/provider 抽象，指令与 Context 的构造，Tool Call 的规范化与执行，权限/沙箱与人类介入，文件—测试—Git 闭环，持久化与 Resume，插件/MCP/SDK 扩展，以及观测、成本和资源约束。每一轴都必须能回到一个入口、调用链、状态对象、错误/取消路径和测试；无法满足时保留为待调查。

这些轴不假定 Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 的边界相同。例如“扩展”可能是进程内 API、协议客户端、配置加载或外部命令，而“权限”也可能在 UI、policy、tool runtime 或宿主环境中决定。后续[第五章](05_harness_loop.md)至[第二十二章](22_configuration_identity_and_supply_chain.md)将按机制展开，每章应引用本图的轴而不复制整张矩阵。

**图表计划：** 制作一张二维能力地图：横轴为控制位置与扩展边界，纵轴为行动自治与人为控制；用形状或注释编码状态/恢复模型，且每个标记必须附证据状态。该图只能表达调查问题和已验证位置，不能把空白渲染为“没有能力”。

## 七个系统的总体位置

总体位置首先是一张“待证实”的研究登记表，而非排名：Aider、Codex、DeepSeek Harness、Gemini CLI、Goose、OpenCode、Pi 均以当前 submodule revision 为分析对象；每一格需要区分 Documented、Implemented、Default、Verified 与 Inferred。这样可避免不同 release、可选插件或外部服务造成的错位比较。

总体图的叙事顺序应从用户任务流而非项目声望出发：先定位用户入口与 session，再看模型如何获得工具、工具如何越过权限边界，最后检查结果如何测试、保存和恢复。此顺序与[第三章](03_vertical_lifecycle_walkthrough.md)的案例路径对齐；若系统在其中某一段用不同术语，先映射到[第四章](04_reference_architecture.md)的最小定义，再在个案章解释其本地语义。

**代码证据计划：** Aider 从 `aider/aider/coders/base_coder.py` 及其 tests 起步；Codex 从 `codex/codex-rs/code-mode-protocol/src/session.rs` 与 `codex/codex-rs/mcp-server/src/exec_approval.rs` 起步；DeepSeek Harness 从 `deepseek-harness/packages/core/session/`、`packages/core/agent/` 和 `packages/interaction/permission-presets/` 起步；Gemini CLI 从 `gemini-cli/packages/core/src/core/client.ts`、`packages/cli/src/acp/` 和工具确认组件起步；Goose 从 `goose/crates/goose/src/agents/state_machine/`、`session/`、`permission/` 起步；OpenCode 从 `opencode/packages/core/`、`packages/protocol/src/groups/session.ts`、`packages/tui/src/routes/session/permission.tsx` 起步；Pi 从 `pi/packages/agent/src/harness/`、`pi/packages/coding-agent/test/agent-session-*.test.ts` 起步。均待沿调用链调查。

## 核心能力地图

核心地图应以“输入—编排—行动—观察—产物”五段呈现，而不是用产品菜单罗列。输入段调查用户请求、项目指令和环境配置；编排段调查 Session/Turn 与模型调用；行动段调查工具、工作区和网络；观察段调查 Tool Result、流式 Event 和错误；产物段调查 diff、测试记录、摘要与持久化。每段都要求列出可变输入、状态承载者和可恢复边界。

矩阵的单元格只记录证据所支持的粒度，例如“存在待追踪的 session state machine”或“文档声明可配置审批”，不能在尚未检验默认策略时写“自动执行”或“安全隔离”。对同一机制的多条实现路径应并列记录，例如 CLI、TUI、SDK、ACP/MCP 客户端可能共享也可能不共享状态；[第二十章](20_interfaces_and_human_in_the_loop.md)将专门验证这些接口差异。

**安全分析计划：** 为地图的行动段增加信任边界叠层：用户/项目指令、模型输出、extension 或 MCP、工具子进程、文件系统、网络和 Git。逐系统调查确认点、policy 来源、拒绝/超时路径和审计事件；证据不足时把格子标为待核验并链接[第十七章](17_security_permissions_and_sandboxing.md)，不据默认名称推定保护强度。

## 扩展性、控制力与自治程度

扩展性考察 Harness 如何增加 provider、tool、prompt/skill、hook、plugin、MCP/ACP 或客户端，而不是把“可配置”一概视为扩展能力。控制力考察谁决定模型可做什么、何时需要批准、执行发生在哪个进程和配置层；自治程度则描述在明确前提下由系统自动推进的阶段数和可撤回节点。三者常彼此拉扯：更开放的接口可能扩大集成面，也可能增加治理和供应链验证成本。

地图应把设计替代方案写成待验证问题：集中式 policy 与分散式 tool guard 的审计性如何不同？插件注册与协议发现的可移植性如何不同？单会话顺序 loop 与子 agent 编排的恢复边界如何不同？答案必须由源码与运行记录支撑，并在[第九章](09_plugins_mcp_and_extensions.md)、[第十六章](16_subagents_and_orchestration.md)和[第二十二章](22_configuration_identity_and_supply_chain.md)展开，不能在本章预判优劣。

**学术检索计划：** 检索“tool-using software agent orchestration”“human oversight for autonomous code agents”“extensibility and software supply-chain trust”等问题域；仅在核验原文元数据后，用文献解释控制与扩展的概念，不把学术分类强塞给实现。图注和矩阵注释也应标明其是结构性比较，不是 benchmark。

## 如何从地图进入详细章节

读者应从一个待回答的问题进入地图，而不是从项目名称跳读。例如，要理解模型响应如何成为工具调用，应从工具与编排轴进入[第六章](06_model_and_provider_abstraction.md)和[第八章](08_tool_call_system.md)；要理解上下文的来源与压力，应进入[第七章](07_context_and_instruction_system.md)、[第十章](10_memory.md)与[第十三章](13_compaction_and_context_management.md)；要理解副作用和恢复，则进入[第十二章](12_session_persistence_and_resume.md)、[第十七章](17_security_permissions_and_sandboxing.md)与[第十八章](18_code_editing_git_and_workspace.md)。

地图只提供共同坐标，不能替代路径解释或系统个性。读者需要沿[第三章](03_vertical_lifecycle_walkthrough.md)检查一次任务穿越哪些轴，再到[第二十三章](23_codex.md)至[第二十九章](29_aider.md)阅读某个 Harness 为什么以该方式组合机制；最终综合判断留给[第三十章](30_comparative_synthesis.md)。

## 横向观察小结

本章规定以机制、状态和证据强度而不是营销功能比较七个 Harness，并预留核心矩阵、控制/自治谱系和信任边界图。下一步应将这张静态地图置入同一修复任务的时间顺序：[纵向生命周期](03_vertical_lifecycle_walkthrough.md)会说明每个格子何时被读取、修改或产生副作用。
