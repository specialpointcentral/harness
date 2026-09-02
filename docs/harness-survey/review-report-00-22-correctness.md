# 00–22 事实正确性评审报告

> 评审日期：2026-09-02
>
> 评审范围：`00_index.md` 至 `22_configuration_identity_and_supply_chain.md`。按文件计实际为 23 章（00–22），不是任务文字中的“十九章”；05–22 共 18 份证据台账。
>
> 评审方法：按仓库内 `academic-research-suite` 路由，采用 `ars/deep-research/WORKFLOW.md` 的 `fact-check` 模式；核对固定提交、各章比较表、系统专段、Mermaid 图及 `.superpowers/sdd/chapter-05-ledger.md` 至 `chapter-22-ledger.md`。
>
> 证据范围：只读源码与仓库文档；未运行真实 Provider、MCP、沙箱、故障注入或跨客户端实验，因此本报告不把静态阅读写成 Runtime Verified。

## 一、总体结论

七个源码树均处于台账声明的固定提交：Aider `5dc9490bb35f`、Codex `bd19459358f5`、DeepSeek Harness `141eb6fef834`、Gemini CLI `30573d2e4d85`、Goose `d830653309a3`、OpenCode `2859603cbb5e`、Pi `5cd93f688aaa`。正文整体事实质量高，关键机制大多能回到台账中的入口、类型和调用链；尤其对“取消不是回滚”“Call ID 只提供关联”“Project Trust 不等于逐调用授权”“实验路径不等于默认路径”等边界处理较好。

本轮未发现可直接判定为**高严重度事实错误**的问题。发现 **9 项中严重度问题**，主要不是源码行为写反，而是正文在跨章概括或比较表中省略了功能开关、构建 feature、实验状态或可选装配条件，使 `Implemented` 容易被读成 `Default`。另有 **7 项低严重度问题**，主要是概念图没有足够醒目地声明“规范性抽象而非七系统共同状态机”，以及亮点被压缩在表格中。

最需要优先修正的四处是：

1. 02、03、16 对 Codex Subagent 的概括应补 `multi_agent_v2` 暴露条件。
2. 12 对 Goose ACP Fork 应补 `unstable_session_fork` 构建 feature。
3. 15 不应把 Gemini CLI 的计划文件到实验 Tracker 写成自动或事务性转换。
4. 21 不应把 Pi 新 durable harness 的 NodeJS 进程树清理写成默认 Coding Agent 主路径保证。

## 二、逐章评审

### 00_index.md

**结论：未发现高、中严重度事实问题。** 对七系统的定位均保持在架构归纳强度，没有把某个功能写成运行验证或成熟度排名。Codex 的安全控制面、Aider 的 Git-centric 路线、DeepSeek Harness 的插件装配、Goose 的扩展平台、OpenCode 的平台化与 Pi 的小内核都已出现，但只是一段并列导览，尚未形成足够鲜明的“为什么与众不同”记忆点。

**[低] 亮点定位缺少后续落点。**

- **原文位置**：第 53–66 行，“用三种视角理解七个 Harness”。
- **证据判断**：这段定位与 05–22 的源码结论一致，但没有把每个定位链接到最能证明它的机制章；读者难以区分“序言宣传语”和“后文将证实的设计中心”。
- **修改建议**：保留短段落，在每个系统名称后加一个内容性链接：Aider→18，Codex→17，DeepSeek Harness→09，Gemini CLI→09/11，Goose→09/20，OpenCode→12/20，Pi→09/16。

### 01_introducing_agent_harness.md

**结论：未发现高、中严重度事实问题。** “Aider 编辑格式”“DeepSeek Harness 由 preset/宿主组合能力”“Goose 以 Provider、MCP 扩展和持久 Session 为平台中心”“Pi 默认少量工具并把高级治理交给扩展”均与后续台账一致。

**[低] Codex 子任务能力仍缺可用性限定。**

- **原文位置**：第 38 行把 Codex 概括为通用本地 Agent 运行时，后续 03 又直接写“提供内建子任务”。
- **源码证据**：`codex/codex-rs/core/src/session/mod.rs::resolve_multi_agent_version` 会按 feature、历史与继承状态决定 V1/V2/Disabled；`codex/codex-rs/core/src/session/multi_agents.rs::effective_multi_agent_mode` 只在 V2 时形成使用模式；`spawn_agent` 实现在 `core/src/tools/handlers/multi_agents_v2/spawn.rs`。
- **修改建议**：本章若预告子任务，使用“固定版本实现了可配置的内建多 Agent 路径”，不要让初学者理解为每个入口默认暴露。

### 02_horizontal_capability_map.md

**[中] Codex 行把条件能力写成无条件能力。**

- **原文位置**：表 2-1 第 26 行，“会话和轮次组织结构化工具循环，可派生子任务”。
- **源码证据**：`multi_agent_v2` 有配置层和模型/会话适用条件；`resolve_multi_agent_version` 可返回 `Disabled`，`effective_multi_agent_mode` 仅为 V2 生成模式。第 16 章台账 C1 也明确写为“是否暴露由配置/模型能力决定”。
- **修改建议**：改为“会话和轮次组织结构化工具循环；启用并暴露多 Agent 路径时可派生子线程任务”。

**亮点判断**：Goose 双循环入口与 Pi 的 Project Trust 已用特色框呈现，形式合适；但 Aider、DeepSeek Harness、Codex 的控制中心仍只在四种类型段落里各占一段，建议后文用独立 H3 承接，而不是继续增加表格列。

### 03_vertical_lifecycle_walkthrough.md

**[中] “Codex 提供内建子任务”省略了 feature/入口条件。**

- **原文位置**：第 85 行，“Codex 提供内建子任务，OpenCode 用父子会话承载委派……”。
- **源码证据**：同 02；Codex 的 `spawn_agent`、`wait_agent`、`send_message` 等在 multi-agent 工具路径中实现，但工具是否进入当前 Turn 的能力表由 multi-agent version/configuration 决定。
- **修改建议**：改为“Codex 在启用的 multi-agent 路径中提供内建子线程任务”；OpenCode、Pi 句子已分别保留父子 Session 和 Extension 边界，可保持。

### 04_reference_architecture.md

**[低] 概念图容易被读成七系统均具备同一组件集合。**

- **原文位置**：图 4-1、图 4-2，尤其 Memory Store、统一 Policy、Sandbox/Container 的实线节点。
- **源码证据**：Aider 主路径集中在 `aider/aider/coders/base_coder.py` 和 Git/交互确认，不存在同型通用 Memory/Policy/Sandbox 服务；Pi 的 `packages/agent/src/agent-loop.ts` 提供 before hook，但默认 Coding Agent 不内建统一逐调用审批或沙箱。正文第 70 行虽说明“逻辑概念”，图本身未标可选性。
- **修改建议**：对 Memory、独立 Policy、外部 Sandbox 等非必选组件使用虚线或“可选实现”标签；图注增加“责任角色可合并、缺席或由宿主外置，不表示七系统都有同名组件”。

### 05_harness_loop.md

**[中] Aider 专段把可选 Test/Commit 写成循环固有组成。**

- **原文位置**：第 142 行，“在一个编码器对象中组织模型请求、编辑应用、自动提交、lint、测试和反思”。
- **源码证据**：`aider/aider/coders/base_coder.py` 中 `auto_lint=True`、`auto_test=False`；`auto_commits=True` 但 `auto_commit()` 还要求存在 repo、未关闭 auto commits、非 dry-run。`aider/aider/args.py` 和 `main.py` 支持 `--no-git` 与关闭自动提交。台账 L18-01 也明确“自动 Test 非 Default；自动提交取决于配置”。
- **修改建议**：改为“组织模型请求、编辑应用、默认 lint，以及按配置启用的测试和 Git 提交”；这样不会削弱 Aider 的编辑事务亮点，反而更准确。

并发池、屏障与提交顺序的比较经源代码抽查一致：DeepSeek Harness 的动态并行/独占分类、Pi 的批次级顺序切换、Gemini CLI Scheduler 和 Codex 在途工具收敛均没有发现反向描述。

### 06_model_and_provider_abstraction.md

**结论：未发现高、中严重度问题。** Fallback 被正确拆成模型、传输、Runtime 和元数据四层；OpenCode 原生 Runtime 回到 AI SDK 被标为实验路径，Codex WebSocket→HTTP 没有被写成任意 Provider 故障转移；未运行真实 Provider 的边界也与台账一致。

建议只做低强度呈现改进：表 6-3 可增加“默认/实验/可配置”的短标签，否则读者仍需回正文才能知道 OpenCode 双 Runtime 和 Gemini 候选链的启用条件。

### 07_context_and_instruction_system.md

**结论：未发现高、中严重度问题。** Aider Repo Map、Codex 分层 `AGENTS.md`、DeepSeek Harness 动态 Context/preset、Gemini CLI 分层 `GEMINI.md`、Goose hints、OpenCode 局部指令、Pi Project Trust 的边界均与台账一致。特别是 Pi 一行没有把 Project Trust 误写成文本全面隔离，这是正确的。

**[低] “未识别 trust gate”在表格里容易被误读成绝对不存在。**

- **原文位置**：表 7-2 Goose、OpenCode 行。
- **源码证据**：台账只对当前项目指令加载路径作“未识别”结论，并明确未穷尽 SaaS/外壳或所有入口。
- **修改建议**：把表格文字统一为“固定版本当前指令路径未识别同型 Workspace Trust gate”，保留调查范围。

### 08_tool_call_system.md

**结论：未发现高、中严重度问题。** 四类 envelope 明确写成作者的规范化坐标而非共享线协议；Aider 旧 function-call 编辑路径没有被当作主路径；Pi 的 hook 控制点没有被夸大为默认 Human Approval；Call ID、结果顺序和取消边界均与源码相符。

亮点呈现上，Codex 的“Schema/Registry/Approval/Sandbox 分层”已经出现，但仍埋在七系统表中，建议把它与第 17 章的安全控制面合并成一个独立 H3，而不是在 08 重复展开。

### 09_plugins_mcp_and_extensions.md

**[中] 图 9-1 的“统一生命周期”措辞会暗示这是七系统共同实现。**

- **原文位置**：第 41–58 行，图注“扩展从发现到活动、刷新、失败和卸载的统一生命周期”。
- **源码证据**：DeepSeek Harness 的 `packages/mcp/mcp-client/src/index.ts::apply` 和 Cordis Fiber 确有激活、失败、重连、dispose；Gemini CLI、Goose、OpenCode、Pi 各自覆盖不同子集；Aider 固定版本未识别第一方通用扩展生命周期。图中“原子发布新目录”“失败后卸载部分初始化结果”等是规范性要求，不是七系统共同状态机。
- **修改建议**：图名改为“扩展生命周期的规范化检查表”，图注加“真实系统可只实现其中子集；Aider 不映射到该状态机”。

DeepSeek Harness 的 MCP Fiber 回滚、Codex resolve-without-activate、Gemini Extension 管理、Goose Extension Manager、OpenCode Plugin/MCP/Skill 并行服务及 Pi 默认不内建 MCP 的事实均与源码一致。

### 10_memory.md

**结论：未发现高、中严重度问题。** Codex Memory 与 Gemini Auto Memory 都清楚标为默认关闭；Goose Memory 是需启用的内建 MCP Extension；DeepSeek Harness 只提供外部 Memory Provider 互操作入口；Aider、OpenCode、Pi 没有被反向写成“缺少记忆能力”，而是区分 Session、指令、Skill 与第三方扩展。

亮点方面，Codex 两阶段提取/全局整合已有特色框，形式足够；建议在第 17 章安全小节反向链接该框，避免读者只看到功能亮点而漏掉旧 Session 上传给 Provider 的隐私边界。

### 11_skills_prompts_commands_and_hooks.md

**结论：未发现高、中严重度问题。** Skill 渐进披露、Template 参数展开、Command 控制面、Hook 生命周期四者没有混写；项目模板可能触发文件/Shell 读取的副作用边界与各系统实现一致。Pi 修改参数后不再 Schema 重验、DeepSeek Human Command 不自动进入模型消息、Goose Recipe/Skill 冲突顺序均被准确保留。

**[低] 表 11-3 缺少状态列。** 该表同时放入 Codex/Gemini 受管理 Hook、Goose Plugin Command Hook、OpenCode/Pi 进程内 Extension Hook 和 Aider 的“未识别”；虽然正文说明不同语义，扫描表格时仍容易把“Implemented”读成“默认启用”。建议增加“主要路径状态”列，值只用 Default / opt-in / feature-gated / not identified。

### 12_session_persistence_and_resume.md

**[中] Goose ACP Fork 缺少不稳定 feature 限定。**

- **原文位置**：表 12-4 第 135 行，“ACP Fork 复制并可截断 Conversation”。
- **源码证据**：实现位于 `goose/crates/goose/src/acp/server/fork_session.rs::handle_fork_session`，但 `goose/crates/goose/Cargo.toml` 的 ACP feature 集合显式包含 `unstable_session_fork`；台账 L12-13 写明“具体暴露面需按构建确认”。
- **修改建议**：改为“启用 `unstable_session_fork` 的 ACP 构建可复制并截断 Conversation”。

其余关键边界正确：Codex JSONL 是规范历史、SQLite 是投影；DeepSeek checkpoint policy 是可选装配；Gemini checkpoint opt-in；Pi JSONL 与 SQLite 是两条不同后端路径；Resume 没有被写成进程镜像或外部副作用回滚。

### 13_compaction_and_context_management.md

**[低] 图 13-1 把理想保护条件画成“共同流程”。**

- **原文位置**：第 44–67 行，图注“自动与手动 Compaction 的共同流程”。
- **源码证据**：Gemini CLI 明确拒绝空摘要/膨胀摘要，Codex 有 Hook/远端 fallback，DeepSeek Harness 有可重放括号和 pruning，Aider/Goose/Pi/OpenCode 的校验点并不完全相同。图中的“保护未闭合调用”“摘要完整且确实缩小”“发布 checkpoint”是规范化设计要求。
- **修改建议**：改为“建议流程/评审检查表”，并在图中用虚线标出各实现可选的校验节点。

比较表对各系统真实压缩形状、旧 Tool Result 处理和失败边界的陈述与台账一致。

### 14_token_efficiency_and_cost_control.md

**结论：未发现高、中严重度问题。** Token 包含关系、窗口压力、账单、辅助调用与质量结果被分开；Subagent 只减少父 Context、不保证减少总账的结论准确。Codex Session cache key、Aider keepalive、Gemini caching 的认证限制、Goose one-shot 与 Pi one-shot cache policy 均能在台账所列路径中闭合。

建议在表 14-2 的 Gemini CLI 行补一句“Subagent/Agent definition 受 preview 与模型适用条件限制”，但当前表没有把它列为默认能力，因此只属低优先级完整性改进。

### 15_goals_planning_and_todos.md

**[中] Gemini CLI 计划文件到 Tracker 的关系写得过于自动。**

- **原文位置**：第 106 行，“把批准的计划文件作为实施依据，再由实验性 Tracker 分解成持久 Task Graph”。
- **源码证据**：`write_todos` 是默认轻量路径；Tracker 由实验配置启用并替换 legacy todo，状态文件写在 Session tracker 目录。台账 G3 明确指出 Plan 与 Tracker 双向同步主要由 Prompt 纪律维持，没有事务或 revision fence；并不存在批准计划后 Runtime 自动、确定地把 Markdown 转成 Tracker 图的统一转换器。
- **修改建议**：改为“启用实验 Tracker 时，执行 Agent 可依据获批计划创建/更新持久 Task Graph；计划文件与 Tracker 的一致性主要由 Prompt 约束维持”。

其余系统的 Goal/Plan/Todo 状态强度基本准确：Codex Thread Goal 明确写为 feature-gated，DeepSeek Resume 后 disarm，Goose Todo 默认扩展，Pi 只写官方示例。

### 16_subagents_and_orchestration.md

**[中] 章末归纳把四种条件能力压成同一“Runtime 能力”。**

- **原文位置**：第 205 行，“Codex、OpenCode、Gemini CLI 与 DeepSeek Harness 把 Subagent 做成模型可调用的 Runtime 能力”。
- **源码证据**：Codex `multi_agent_v2` 是否暴露由 feature/模型/会话决定；Gemini `invoke_agent` 有 preview/模型适用条件；DeepSeek Harness 由 provider/bundle/preset 装配；OpenCode 前台 Task 与实验后台 Job 不是同一稳定层。表 16-3 虽在部分单元格提示实验/装配，章末一句又把状态压平。
- **修改建议**：改为“这四个系统都实现了模型可调用的 Subagent 路径，但可用性分别受 feature、preview/模型条件、bundle/provider 装配或实验后台开关约束”。

图 16-2 对 Parent/Child、Agent Graph、Task DAG 与 Workflow Graph 的区分准确，是全书最清楚的图表之一；不建议简化。

### 17_security_permissions_and_sandboxing.md

**结论：未发现高、中严重度问题。** 审批、权限画像和实际沙箱被正确分层；DeepSeek Harness 的 full/partial 结果没有被写成完全隔离；OpenCode pattern permission 没有被写成 OS 沙箱；Pi 明确没有默认统一审批/沙箱；Aider 与 Goose 的宿主权限边界也保留了入口条件。

亮点呈现不足：Codex 安全控制面当前散布在多个段落和表 17-5 中，尚未形成一个能被读者复述的机制链，建议改为独立 H3，见本文末尾建议。

### 18_code_editing_git_and_workspace.md

**[中] “Aider 把事务中心放在 Git commit”强于源码默认边界。**

- **原文位置**：第 112 行。
- **源码证据**：Aider 确实默认 `auto_commits=True` 并用 `dirty_commit`、`auto_commit`、`/diff`、`/undo` 形成 Git-centric 路线；但 `--no-git`、关闭 auto commits、dry-run 或无 repo 时提交路径不成立。核心编辑解析和反思仍能工作，自动测试默认也为 false。
- **修改建议**：改为“Aider 把编辑事务与 Git commit 绑定得最紧，在启用 Git/auto-commit 时以提交形成基线和结果边界”；不要把 commit 写成所有 Aider 会话的必要中心。

Gemini Shadow Git、OpenCode 独立 Snapshot、DeepSeek 文件版本守卫、Codex Turn Diff 只覆盖精确 mutation、Pi 单文件 mutation queue 的描述均与源码一致。

### 19_observability_evaluation_and_replay.md

**结论：未发现高、中严重度问题。** Event/Item、Log/Trace/Metric、Eval Artifact 被正确分层；Replay、Re-run 与 Resume 没有混称。Aider benchmark、Gemini Behavioral Eval、Goose Harbor、Pi Evals 的定位均保留环境、预算和 scorer 条件，没有写成七系统统一质量排名。

建议在 OpenCode 行继续保留“实验 V2”限定；当前文本已经做到，不需改事实。

### 20_interfaces_and_human_in_the_loop.md

**结论：未发现高、中严重度问题。** Codex App Server、DeepSeek Web/automation-only ACP、Gemini TUI/Headless/ACP、Goose Desktop ACP、OpenCode HTTP/SSE/WebSocket 与 Pi 实验 Session Server 的控制边界均与源码一致。图 20-1 明确写为“最小双向关系”，没有声称使用同一协议。

亮点呈现上，OpenCode 的“Server 是权威状态边界”值得独立 H3；目前放在比较表中，读者不容易看出这正是其平台化设计与其他本地 CLI 的根本差异。

### 21_reliability_and_resource_control.md

**[中] Pi 的新 durable harness 进程树清理被放进默认产品比较行。**

- **原文位置**：第 75 行与表 21-2 第 120 行，“NodeJS harness env 跟踪 PID 并 cleanup 进程树”。
- **源码证据**：`pi/packages/agent/src/harness/env/nodejs.ts` 的确维护 `activeChildPids` 并在 `cleanup()` 调用 `killProcessTree`；但台账 I3 明确指出这是新的 NodeJS harness environment，固定版本 Coding Agent 主 Shell 位于 `packages/coding-agent/src/core/tools/bash.ts`，两条路径不能合并成单一 Default 保证，且新 durable harness 的部分 API 仍 unavailable。
- **修改建议**：表格改为“新 durable harness 的 NodeJS env 可登记并清理进程树；默认 Coding Agent Shell 另有 timeout/abort kill 路径”，正文分别描述两条路径。

其他系统的 retry、Retry-After、cancel 和后台资源结论没有发现事实错误；尤其 DeepSeek 的合作式 deadline 与结果闭合、OpenCode 最多五次 Session retry、Goose kill 后 wait 均有直接源码支撑。

### 22_configuration_identity_and_supply_chain.md

**结论：未发现高、中严重度问题。** 配置覆盖与约束、用户身份/Agent Identity/调用来源/Provider Credential、扩展来源与更新验证被正确分开。Goose Sigstore/SLSA 验证被限定为二进制更新路径；Gemini 本地 HMAC 没有被写成发布者签名；Aider PyPI/pip 路径没有被写成有 provenance；Pi npm install 生命周期风险也被明确保留。

**[低] 图 22-1 的“Project Trust/企业约束”仍像共同必经节点。**

- **原文位置**：图 22-1。
- **源码证据**：Pi、Gemini CLI 有明确 Project Trust；Codex 有托管 requirements；Aider 配置链没有同型 trust gate，DeepSeek/OpenCode/Goose 的企业约束与装配形态不同。
- **修改建议**：把 Project Trust、企业约束画成可选分支，图注说明它们是可实现的仲裁层而非七系统共同顺序。

## 三、图表如实性总评

本报告中的 Mermaid 图大多是**概念图或规范性检查表**，正文通常已经用“通用”“最小”“参考”限定，没有发现把某个概念图直接冒充具体系统调用图的高严重度问题。仍建议建立统一图注规则，避免读者只看图不看上下文时误解：

1. 图注以“概念图”“规范化检查表”“系统机制图”三选一开头。
2. 概念图统一追加：“不表示七个固定版本都具有同名组件或全部转换。”
3. 可选组件、feature-gated 路径和实验路径使用虚线，并在图例中标注。
4. 系统机制图必须在图内或图注写出 Harness 名称、固定 commit 和 Default/opt-in/experimental。
5. 当前最需改图注的是图 4-1/4-2、9-1、13-1、22-1；图 16-2 已清楚区分不同图语义，可作为范例。

## 四、亮点呈现形式建议

当前“七系统比较表 + 段内点名”适合查表，但不适合传达控制中心：表格会把最重要的设计与普通功能压成同一字号，也会迫使读者跨 18 章自己拼出系统画像。建议保留比较表作为索引，同时把以下内容升级为独立 H3；每个 H3 使用“问题 → 机制链 → 代价/边界 → 相关章节链接”的四段式，不再重复七列矩阵。

1. **第 17 章：`### Codex：审批、权限画像、沙箱、网络与凭据代理组成安全控制面`**

   展开 Call ID 绑定审批、Exec Policy/Permission Profile、平台沙箱、受管理网络代理与 Credential Broker 的分层；强调每层不能证明什么。该亮点是 Codex 最与众不同的整体设计，目前表 17-5 不足以传达。

2. **第 18 章：`### Aider：以 Git 基线组织编辑事务，而不是通用工具总线`**

   用一条真实链说明 dirty commit（可配置）→ edit format 解析/dry-run → 写入 → 默认 lint/可选 test → auto commit（可配置）→ `/diff`/受约束 `/undo`。标题避免把 Git commit 写成所有模式的必要条件。

3. **第 09 章：`### DeepSeek Harness：Cordis 插件图让产品行为成为可组合生命周期`**

   从 bundle/preset/Scope/Fiber/MCP Client 的激活、回滚、HMR 和 dispose 展开；保留“保证取决于实际装配”这一核心代价。现有特色框信息正确，但不足以承载其系统级差异。

4. **第 09 章：`### Gemini CLI：Extension 不只是插件包，而是受管理的贡献集合`**

   把 MCP、Policy、Hook、Skill、Agent、Command、Context 的同包贡献，与来源同意、allowlist、完整性记录、启停和热重载连成管理面；再链接 07 的 Context 层级、11 的 Skill/Hook 和 20 的 IDE/ACP。

5. **第 09 或 20 章：`### Goose：以 MCP Extension 和 ACP 把能力生态与客户端状态接在一起`**

   说明 Extension Manager 如何管理 Tool/Resource/Prompt、反向能力、OAuth 和在途调用，以及 Desktop/IDE 如何通过 ACP 看到同一 Session/permission 状态。不要只以“支持 MCP”概括。

6. **第 20 章：`### OpenCode：Server 是权威状态边界，客户端只是不同投影`**

   连接 SQLite Session/Message/Part、HTTP API、SSE、PTY WebSocket、Desktop sidecar、SDK 与 child Session；这是其平台化亮点，比“工具很多”更具区分度。

7. **第 09 或 16 章：`### Pi：小内核不是缺功能，而是把治理和编排变成 Extension 责任`**

   并列默认 read/edit/write/bash、小型 AgentLoop、树形 Session 与 Extension API；再用“默认无 MCP/统一审批/Subagent”说明扩展边界，而不是能力缺失。现有两个特色框可合并为一个更完整 H3。

8. **第 02 章末增加 `### 七个控制中心，一句话不能替代表格证据`**

   只放七条两句式索引：一句亮点、一句代价，并链接上述 H3。这样 00–04 建立记忆点，05–22 提供源码机制，避免每章都重新发明系统画像。

## 五、建议修订顺序

1. 先修正 12、15、21 三处明确的 feature/实验/默认强度问题。
2. 再统一 02、03、16 的 Codex multi-agent 可用性措辞。
3. 修正 05、18 对 Aider test/commit 的配置限定。
4. 统一 Mermaid 图注类别与虚线规则。
5. 最后按第 17、18、09、20、16 章的顺序增加七个亮点 H3，并从 00/02 建立链接。

修订时不需要重写章节结构；多数事实问题可用一句限定或一个状态标签修复。真正值得扩写的是七个控制中心的独立 H3，而不是继续扩大比较表。
