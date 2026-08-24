# Agent Harness 调研报告章节骨架实施计划

> **供执行 Agent 使用：** 必须使用 `superpowers:subagent-driven-development`（推荐）
> 或 `superpowers:executing-plans` 按任务执行本计划。所有步骤使用复选框（`- [ ]`）
> 跟踪状态。

**目标：** 初始化固定版本的源码语料，并为已经批准的中文、代码驱动 Agent Harness
调研报告建立 37 个非空、相互链接的 Markdown 章节提纲。

**实施方式：** 将 `WRITING_PLAN.md` 视为冻结的编辑规范，按照知识依赖分组建立章节
骨架。在所有链接目标存在后再编写叙事式 `00_index.md`，最后执行覆盖整个报告目录的
结构和链接校验。本阶段交付提纲版，不提前编写完整正文。

**技术形式：** 可移植 Markdown、Git Submodule、Bash 校验、`rg`，以及兼容
GitHub/Pandoc 的相对链接。

## 全局约束

- 只修改 `docs/harness-survey/`，并只初始化现有的七个根级 Submodule checkout。
- 严格创建 `WRITING_PLAN.md` 规定的 37 个编号 Markdown 文件：`00`–`32`、
  `90`–`93`。
- 不创建空文件，也不留下没有解释文字的空标题。
- 每个编号文件只有一个 H1，通常包含五至八个叙事型 H2。只有确实需要持续展开的
  子问题才使用 H3，不使用 H4。
- 每章包含提纲状态、章节目的、学习目标、前置阅读、相关阅读、证据计划、学术内容
  计划、安全分析、图表计划和下一步阅读。
- 所有正式标题、正文说明、示例、图表说明、语义框和导航使用中文。
- 项目名、协议名、源码 symbol、配置键和命令保留精确英文；通用英文术语首次出现
  时采用“中文解释（英文原词）”。不得出现整段无中文解释的英文论述。
- 报告聚焦 Coding Agent 工作流，包括代码、文本、仓库上下文、Tool、Shell、diff、
  测试、Git、Session、Artifact 和工程控制流。
- 章节意图使用完整段落；列表只用于目标、证据入口、精确映射和检查项。
- 使用五类语义框：`学术背景`、`设计取舍`、`特色机制`、`安全提示`和`实现证据`。
- 后续工程结论必须来自固定 commit 的代码追踪。提纲阶段记录研究问题和具体源码
  入口，不把尚未验证的行为写成完成态正文。
- 后续学术判断必须来自实际文献检索和核验引用。提纲阶段只记录检索问题和候选概念，
  不编造引用键。
- `00_index.md` 是可独立阅读的叙事式序章，随后给出三种内容视角、四类读者路线和
  完整目录。
- `00` 引出问题，`03` 形式化生命周期，`04` 定义参考架构，三章不重复成段内容。
- 分支和 tag 名只记录快照来源，不自动转化为稳定性权重。
- 保留无关 worktree 状态。计划定稿后只暂存并提交 `docs/harness-survey/`；不得暂存
  Submodule checkout 或无关路径，不推送远端。计划基线与后续章节写作应分开提交，
  以便清楚区分编辑设计、章节骨架和完整正文的完成状态。
- 所有受跟踪文件的创建和修改使用 `apply_patch`。

---

## 通用章节骨架约定

普通机制章和个案章采用下面的基本结构。实际文件必须使用针对本章的问题、过渡和
标题，不能复制一套空泛说明：

```markdown
# 正式章节标题

> **状态｜提纲**
>
> 本文件已经确定章节问题、叙事结构和证据计划，尚未写成完整正文。

> **章节目标**
>
> 用一段话说明本章为哪类读者解决什么问题，以及它在全书中的作用。

> **学习目标**
>
> - 三至五个可以在章末检验的理解目标。

> **阅读关系**
>
> - 前置阅读：使用相对链接。
> - 相关章节：使用相对链接。
> - 下一步阅读：使用相对链接。

## 叙事型主题一

用一至两句话说明本节将从哪个问题出发、建立什么结论。

## 叙事型主题二

用一至两句话说明本节如何承接上一节。

## 本章小结

说明成稿小结必须回答的章首问题。

## 写作与证据计划

> **实现证据**
>
> - 七个 Harness 的分析入口、关键路径或待验证行为。

> **学术背景｜计划主题**
>
> 记录需要实际检索的理论问题和原始文献方向。

> **安全提示｜计划主题**
>
> 记录需要分析的资产、前提、边界和影响。

计划图表：列出图、表、时序图或状态机及其要回答的问题。
```

状态说明是明确的提纲元数据，不是未完成占位。每个叙事型 H2 都要写入针对本章的
意图说明。附录根据索引功能调整结构，但仍保留状态、目的、导航和证据来源。

## 已批准的文件与 H2 清单

后续实施任务使用这份清单。分号分隔的内容是按顺序写入 Markdown 的 H2 候选标题，
并根据章型补充 `本章小结` 和 `写作与证据计划`。

### 基础与总览

| 文件 | H1 | 叙事型 H2 顺序 |
|---|---|---|
| `00_index.md` | Agent Harness：架构、工程与安全 | 一个看似简单的修复任务；模型之外的系统；当任务变长、被打断或被委派；七个 Harness 与同一个工程问题；如何阅读这份报告；完整目录与版本约定 |
| `01_scope_and_methodology.md` | 范围、术语与研究方法 | 什么是 Agent Harness；为什么选择这七个系统；代码如何成为工程结论；论文如何进入学术解释；如何进行公平比较；证据状态与有效性边界；本章小结 |
| `02_horizontal_capability_map.md` | 七个 Agent Harness 的横向能力地图 | 用什么轴比较 Harness；七个系统的总体位置；核心能力地图；扩展性、控制力与自治程度；如何从地图进入详细章节；横向观察小结 |
| `03_vertical_lifecycle_walkthrough.md` | 一次 Coding Agent 任务的纵向生命周期 | 从修复请求到可执行任务；Session、指令与上下文准备；模型、Tool Call 与 Observation 循环；权限、执行与错误恢复；上下文压力、记忆与委派；验证、持久化与 Resume；七个系统的路径差异；本章小结 |
| `04_reference_architecture.md` | Agent Harness 统一参考架构 | 为什么需要统一参考架构；控制平面与执行平面；Session、Turn、Message、Event 与 Artifact；Context、Memory 与 Compaction；能力层、协议层与客户端；信任边界与副作用；七个系统到参考架构的映射；本章小结 |

### 核心机制

| 文件 | H1 | 叙事型 H2 顺序 |
|---|---|---|
| `05_harness_loop.md` | Harness Loop：从一次模型响应到持续任务 | 为什么一次响应不等于一个 Agent；Turn、状态与循环不变量；行动、执行与 Observation；流式事件与并行 Tool Call；终止、取消与防失控；七个系统如何组织 Loop；本章小结 |
| `06_model_and_provider_abstraction.md` | 模型与 Provider 抽象 | Provider 层在隔离什么；消息、代码内容块与角色模型；流式响应与 Tool Call 差异；能力发现、路由与 Fallback；Token、速率限制与认证；七个系统的抽象边界；本章小结 |
| `07_context_and_instruction_system.md` | 上下文构造与指令系统 | Context 为什么不只是 Prompt；指令来源、层级与冲突；Workspace、代码与动态上下文；文件选择、Repo Map 与检索；容量预算与不可信内容；七个系统的上下文策略；本章小结 |
| `08_tool_call_system.md` | Tool Call 系统：从模型意图到可执行能力 | 工具如何成为模型的行动空间；Schema、注册表与能力发现；请求、参数与 Call ID；执行、结果与 Observation；错误、重试与并行调用；七系统 Tool-call Envelope 对照；权限和副作用边界；本章小结 |
| `09_plugins_mcp_and_extensions.md` | Plugin、MCP 与扩展系统 | Harness 为什么需要扩展；Plugin、Extension、MCP、Skill 与 Hook；发现、注册与生命周期；MCP Transport 与双向能力；配置、分发与组合失效；七个系统的扩展路径；供应链与信任边界；本章小结 |
| `10_memory.md` | Memory：Harness 如何保存可复用经验 | Memory 与 Session 状态的区别；Working、Episodic、Semantic 与 Procedural Memory；写入、检索、更新与遗忘；项目级、用户级与 Session 级范围；Memory、Context 与 Compaction；七个系统的实际机制；污染、隐私与陈旧信息；本章小结 |
| `11_skills_prompts_commands_and_hooks.md` | Skills、Prompt、Command 与 Hook | 四类机制分别解决什么问题；Skill 的发现、选择与加载；Prompt Template 与项目定制；Slash Command 与用户控制；Hook 与生命周期拦截；权限、参数与上下文继承；七个系统的组合方式；本章小结 |
| `12_session_persistence_and_resume.md` | Session、持久化与 Resume | Session 保存的任务边界；Turn、Message、Event 与 Item；Event Log、Snapshot 与 Checkpoint；Resume、Replay、Branch 与 Fork；Tool Call 和外部副作用的一致性；七个系统的持久化路径；崩溃恢复与安全边界；本章小结 |
| `13_compaction_and_context_management.md` | Compaction 与上下文管理 | 为什么上下文最终会装不下；截断、摘要、选择与外部化；自动和手动 Compaction；Tool Result 与文件内容压缩；信息保真度与摘要漂移；Memory、Resume 与上下文重建；七个系统的机制与失效模式；本章小结 |
| `14_token_efficiency_and_cost_control.md` | Token 效率与成本控制 | Token 账本到底记录什么；减少输入与选择上下文；截断、Pruning、Spill 与 Locator；Prompt Cache、KV Cache 与稳定前缀；输出和推理预算；弱模型、路由与任务分层；Subagent 的 Token 经济性；七系统指标与质量边界；本章小结 |
| `15_goals_planning_and_todos.md` | Goal、Planning 与 Todo | Goal、Plan、Task 与 Todo；从 ReAct 到 Plan-and-Execute；计划模式与执行模式；任务分解、进度与完成判定；预算、停止与阻塞状态；持久化、恢复与用户修改；七个系统的计划机制；本章小结 |
| `16_subagents_and_orchestration.md` | Subagent 与多 Agent 编排 | 为什么委派任务；Parent、Child、Task、Thread 与 Session；创建、Prompt 传递与上下文继承；通信、通知与结果回传；父子树、Agent Graph、Task DAG 与 Workflow；Wait、Join、取消与失败传播；共享 Workspace、竞争与结果汇聚；Token、权限与责任；七个系统的编排路径；本章小结 |
| `17_security_permissions_and_sandboxing.md` | 安全、权限与沙箱 | Harness 保护什么；主体、能力与信任边界；Tool Permission 与 Human Approval；文件、进程与网络沙箱；Workspace Trust 与 Credential Isolation；Prompt Injection 到能力执行；Session、Memory、Extension 与 Telemetry；七系统安全模型；本章小结 |
| `18_code_editing_git_and_workspace.md` | 代码编辑、Git 与 Workspace | Coding Harness 的工程闭环；Workspace 发现与作用域；直接写入、Patch 与结构化编辑；Diff、审查与用户修改；Git、Worktree 与 Submodule；Test、Lint 与构建；七个系统的 Coding 路径；数据损坏与供应链边界；本章小结 |
| `19_observability_evaluation_and_replay.md` | 观测、评测与回放 | Harness 为什么需要可观测性；Log、Event、Trace 与 Metric；模型请求和 Tool Call 关联；Token、成本与延迟；Telemetry、Crash Report 与隐私；Replay 与确定性边界；Harness Eval 与模型 Eval；七个系统比较；本章小结 |
| `20_interfaces_and_human_in_the_loop.md` | 接口与 Human-in-the-loop | CLI、TUI、IDE、Desktop、Web 与 API；Headless 与非交互模式；ACP、JSON-RPC 与应用服务器；审批、编辑与中断；模式切换与流式反馈；多客户端状态一致性；七个系统的人机边界；本章小结 |
| `21_reliability_and_resource_control.md` | 可靠性与资源控制 | Harness 的 Failure Model；Retry、Backoff 与 Fallback；Timeout、Cancel 与 Interrupt；幂等性与外部副作用；后台进程与资源清理；Loop、Token、Cost 与并发预算；崩溃与 Provider 故障；七个系统比较；本章小结 |
| `22_configuration_identity_and_supply_chain.md` | 配置、身份与供应链 | 配置层级与覆盖规则；用户、项目与企业配置；Agent Identity 与调用来源；Provider Credential；Plugin、MCP 与 Skill 来源；Telemetry 与企业策略；自动更新与依赖生命周期；七系统比较；供应链风险；本章小结 |

### Harness 个案

| 文件 | H1 | 叙事型 H2 顺序 |
|---|---|---|
| `23_codex.md` | Codex：安全控制面与多入口 Runtime | 项目定位与设计问题；Rust Core、Protocol 与 App Server；Loop、Event 与 Rollout；Approval、Sandbox 与 Exec Policy；MCP、Skill、Plugin、Memory 与 Subagent；CLI、IDE 与服务入口；代表性设计和边界；适用场景与源码地图；本章小结 |
| `24_opencode.md` | OpenCode：多模型平台与 Agent Mode | 项目定位与平台形态；Core、Server、TUI、Desktop 与 SDK；Build、Plan 与 General Agent；Provider、Tool、Plugin 与 MCP；Session、存储与 Subagent；代表性设计和边界；适用场景与源码地图；本章小结 |
| `25_pi.md` | Pi：极简而可扩展的 Agent Runtime | 极简核心的设计哲学；Agent Core、AI Abstraction 与 Coding Agent；Loop、Tool State 与 TUI；Extension、Prompt、Skill 与 Session Backend；权限与外部隔离边界；Subagent 扩展示例；适用场景与源码地图；本章小结 |
| `26_gemini_cli.md` | Gemini CLI：搜索增强、扩展与自动化 | 项目定位与组件边界；CLI、Core、SDK 与 IDE Companion；模型流式调用与搜索工具；MCP、Extension、Skill 与 Hook；Planning、Checkpoint 与非交互模式；Permission、Sandbox 与 Subagent；适用场景与源码地图；本章小结 |
| `27_deepseek_harness.md` | DeepSeek Harness：组合式 Harness 架构 | 项目定位与组合原则；Cordis、Service、Provider 与 Consumer；Agent Scope、Session 与 Context；Tool、MCP、ACP、Skill 与 Subagent；Guard、Sandbox 与 Shell Provider；Workflow、Schedule 与 Job；组合失效和安全边界；适用场景与源码地图；本章小结 |
| `28_goose.md` | Goose：本地 Agent 与 MCP 生态 | 项目定位与治理；Rust Core、CLI、Desktop 与 API；Provider Abstraction 与 ACP；MCP Extension 与 Recipe；Context Management 与 Delegation；Tool Visibility 与发行版定制；代表性设计和边界；适用场景与源码地图；本章小结 |
| `29_aider.md` | Aider：Git-centric Coding Agent | 项目定位与历史角色；Coder Abstraction 与核心循环；Repo Map 与上下文选择；Edit Format 与代码修改；Git Commit、Lint 与 Test；多模型、弱模型与 Token；与平台型 Harness 的差异；适用场景与源码地图；本章小结 |

### 综合与附录

| 文件 | H1 | 叙事型 H2 顺序 |
|---|---|---|
| `30_comparative_synthesis.md` | 七个 Agent Harness 的综合比较 | 回到比较问题；架构类型与谱系；Loop、状态与上下文；Tool、扩展与接口；Session、Resume 与 Multi-agent；Permission、Sandbox 与供应链；复杂度、成本与维护；适用场景决策；主要结论 |
| `31_design_principles.md` | Agent Harness 设计原则 | 控制平面与执行平面；工具发现与授权；Context、Memory、Session 与 Compaction；权限、身份与外部副作用；失败、取消与资源上限；可观测性与来源追踪；渐进自治与 Human-in-the-loop；原则冲突与取舍 |
| `32_open_problems_and_research_agenda.md` | 开放问题与研究议程 | Harness 的形式化模型；Tool-use 与 Prompt Injection；Memory 污染和 Compaction 保真；Token 效率与质量边界；Resume 与副作用一致性；Multi-agent 权限与责任；MCP 和插件供应链；评测、真实数据与标准化；未来 Corpus 扩展 |
| `90_glossary.md` | 术语表 | 如何使用术语表；通用 Agent 术语；Harness 架构术语；Tool 与扩展术语；状态与持久化术语；安全术语；七系统专有术语映射 |
| `91_version_manifest.md` | 版本与分析环境清单 | 清单使用说明；父仓库快照；七个 Submodule 快照；许可证与上游来源；分析日期和必要环境；版本更新记录 |
| `92_evidence_index.md` | 实现证据索引 | 证据索引的使用方法；按章节索引；按 Harness 索引；结论与调用链映射；Tool-call Schema 映射；文档与运行证据；推断和更新记录 |
| `93_references.md` | 参考文献阅读入口 | 如何使用本章；Agent Loop 与 Tool Use；Planning 与 Multi-agent；Memory 与 Context；Security 与 Capability；Coding Agent 与软件 Agent；协议和互操作；检索与引用核验说明 |

---

### 任务 1：初始化并核对固定版本的 Submodule 语料

**文件：**
- 只改变 checkout 状态：`aider/`、`codex/`、`deepseek-harness/`、`gemini-cli/`、
  `goose/`、`opencode/`、`pi/`
- 不修改父仓库受跟踪文件。

**输入与产出：**
- 输入：父仓库 commit `b964dd3896239ff06e13c9efd363266755e5d9af` 记录的 gitlink。
- 产出：七个可读的 shallow 源码树，其 `HEAD` 与父仓库 gitlink 完全一致。

- [ ] **步骤 1：记录预检状态**

运行：

```bash
git status --short
git submodule status
```

预期：只有 `docs/harness-survey/` 未跟踪，七个 Submodule 在初始化前均带前导 `-`。

- [ ] **步骤 2：初始化七个固定版本 checkout**

运行：

```bash
git submodule sync --recursive
git submodule update --init --recursive --depth 1
```

预期：七个 checkout 全部完成，父仓库 gitlink 没有变化。

- [ ] **步骤 3：核对 gitlink 和 shallow 状态**

运行：

```bash
for d in aider codex deepseek-harness gemini-cli goose opencode pi; do
  recorded=$(git ls-tree HEAD "$d" | awk '{print $3}')
  checked_out=$(git -C "$d" rev-parse HEAD)
  test "$recorded" = "$checked_out"
  test "$(git -C "$d" rev-parse --is-shallow-repository)" = true
  printf '%s %s\n' "$d" "$checked_out"
done
```

预期固定 SHA：

```text
aider               5dc9490bb35f9729ef2c95d00a19ccd30c26339c
codex               bd19459358f534ed1cae464ec13d56600aeb45f2
deepseek-harness    141eb6fef83422698aef7a981029e843e8161534
gemini-cli          30573d2e4d85bdc2c0ae8218c377cd410336da77
goose               d830653309a32ebfae0b86fbe48164aaeca79fdf
opencode            2859603cbb5e346d1c32519cb3f5ee58b0d78455
pi                  5cd93f688aaab89dbb6dfa4aca535f21796ae185
```

- [ ] **步骤 4：核对初始证据入口可读**

运行：

```bash
test -f codex/codex-rs/core/src/client.rs
test -f opencode/packages/opencode/src/tool/task.ts
test -d pi/packages/coding-agent/examples/extensions/subagent
test -f gemini-cli/docs/core/subagents.md
test -f deepseek-harness/packages/subagent/subagent/README.md
test -f goose/crates/goose-context-management/src/lib.rs
test -f aider/aider/coders/architect_coder.py
```

预期：所有 `test` 均成功退出。

### 任务 2：建立方法与架构提纲

**文件：**
- 创建：`docs/harness-survey/01_scope_and_methodology.md`
- 创建：`docs/harness-survey/02_horizontal_capability_map.md`
- 创建：`docs/harness-survey/03_vertical_lifecycle_walkthrough.md`
- 创建：`docs/harness-survey/04_reference_architecture.md`

**输入与产出：**
- 输入：通用骨架约定、基础章节清单和已经初始化的固定版本源码。
- 产出：后续所有章节共用的定义、证据语言、生命周期和状态对象词汇。

- [ ] **步骤 1：确认目标文件尚不存在**

运行：

```bash
for f in 01_scope_and_methodology.md 02_horizontal_capability_map.md 03_vertical_lifecycle_walkthrough.md 04_reference_architecture.md; do
  test ! -e "docs/harness-survey/$f"
done
```

预期：所有检查成功，避免覆盖已有文件。

- [ ] **步骤 2：使用 `apply_patch` 创建四个文件**

使用基础章节清单中规定的 H1 和 H2 顺序。每个叙事型 H2 下写一至两句中文，说明
本节问题和与前后小节的过渡。加入统一的状态、目标、学习、阅读关系、证据、学术
检索、安全分析和图表计划。

- [ ] **步骤 3：校验基础章节约定**

运行：

```bash
for f in docs/harness-survey/0[1-4]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
  test "$(rg -c '^#### ' "$f")" -eq 0
done
```

预期：四个文件均非空，每个文件一个 H1、至少五个 H2，并且没有 H4。

### 任务 3：建立 Loop、Provider、Context、Tool 和扩展机制提纲

**文件：**
- 创建：`docs/harness-survey/05_harness_loop.md`
- 创建：`docs/harness-survey/06_model_and_provider_abstraction.md`
- 创建：`docs/harness-survey/07_context_and_instruction_system.md`
- 创建：`docs/harness-survey/08_tool_call_system.md`
- 创建：`docs/harness-survey/09_plugins_mcp_and_extensions.md`

**输入与产出：**
- 输入：`01`–`04` 的术语和状态定义。
- 产出：状态、安全、个案和综合章节所需的行动与执行词汇。

- [ ] **步骤 1：使用 `apply_patch` 创建五个文件**

使用核心机制清单规定的 H1 和 H2。`08` 必须规划七系统规范化的 request、response、
error 和 approval envelope，并链接到 `92_evidence_index.md` 的字段映射。

- [ ] **步骤 2：加入七系统的具体证据目标**

每个文件的证据计划都要列出七个 Harness。某项目即使不以该机制为中心，也要使用
已批准的能力状态语言提出范围明确的调查问题，而不是强行写成正面能力结论。

- [ ] **步骤 3：校验本组章节**

运行：

```bash
for f in docs/harness-survey/0[5-9]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
  rg -q 'Codex' "$f"
  rg -q 'Aider' "$f"
done
```

预期：五个提纲均有效，证据部分覆盖七系统，同时不假设它们具有同等能力。

### 任务 4：建立 Memory、定制、Session、Compaction 和 Token 提纲

**文件：**
- 创建：`docs/harness-survey/10_memory.md`
- 创建：`docs/harness-survey/11_skills_prompts_commands_and_hooks.md`
- 创建：`docs/harness-survey/12_session_persistence_and_resume.md`
- 创建：`docs/harness-survey/13_compaction_and_context_management.md`
- 创建：`docs/harness-survey/14_token_efficiency_and_cost_control.md`

**输入与产出：**
- 输入：`04` 的状态对象定义和 `05`–`09` 的 Runtime 词汇。
- 产出：Subagent、安全和综合章节所需的长期状态与上下文管理概念。

- [ ] **步骤 1：使用 `apply_patch` 创建五个文件**

使用清单规定的标题。`10` 和 `13` 显式链接 `04` 中 Session、Context、Event 和
Artifact 的最小定义；详细 Session 状态机留在 `12`。

- [ ] **步骤 2：保持 Token 与 Compaction 的边界**

提纲用正面语言说明：`13` 解释上下文压力下的连续性；`14` 解释输入选择、Tool 输出
管理、缓存、预算、路由、计量、总成本、延迟和质量。

- [ ] **步骤 3：把已经核对的源码线索带入 `14`**

加入 `WRITING_PLAN.md` Token 章节已经记录的七组项目路径，将其作为证据入口目标，
不写成完成态结论。

- [ ] **步骤 4：校验本组章节**

运行：

```bash
for f in docs/harness-survey/1[0-4]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
done
rg -q '04_reference_architecture.md' docs/harness-survey/10_memory.md
rg -q '04_reference_architecture.md' docs/harness-survey/13_compaction_and_context_management.md
```

预期：五个提纲有效，两处提前定义链接均存在。

### 任务 5：建立 Planning、Subagent、安全和 Coding 工作流提纲

**文件：**
- 创建：`docs/harness-survey/15_goals_planning_and_todos.md`
- 创建：`docs/harness-survey/16_subagents_and_orchestration.md`
- 创建：`docs/harness-survey/17_security_permissions_and_sandboxing.md`
- 创建：`docs/harness-survey/18_code_editing_git_and_workspace.md`

**输入与产出：**
- 输入：`04`–`14` 的 Loop、Session、Context、Tool 和 Token 定义。
- 产出：个案和综合章节使用的自治、信任边界和 Coding Loop 分析。

- [ ] **步骤 1：使用 `apply_patch` 创建四个提纲**

使用清单规定的标题，并为 `16` 和 `17` 保留已批准的 6,000–10,000 字正文预算。

- [ ] **步骤 2：在 `16` 中保持图结构和同步语义的区分**

分别规划父子拓扑、Agent Graph、Task DAG、Workflow Graph 和 Runtime 的 wait、join、
cancel 语义，并写明使用“同步保证”结论前所需的准确证据。

- [ ] **步骤 3：把七系统 Subagent 证据线索带入 `16`**

加入 `WRITING_PLAN.md` 中 Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、
Goose 和 Aider 的证据目标，保留 Native、Pluggable 和 Not central 等状态差异。

- [ ] **步骤 4：校验本组章节**

运行：

```bash
for f in docs/harness-survey/1[5-8]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
done
rg -q 'Task DAG' docs/harness-survey/16_subagents_and_orchestration.md
rg -q 'Telemetry' docs/harness-survey/17_security_permissions_and_sandboxing.md
```

预期：四个提纲有效，并包含 DAG 边界和 Telemetry 外传问题。

### 任务 6：建立观测、接口、可靠性和配置提纲

**文件：**
- 创建：`docs/harness-survey/19_observability_evaluation_and_replay.md`
- 创建：`docs/harness-survey/20_interfaces_and_human_in_the_loop.md`
- 创建：`docs/harness-survey/21_reliability_and_resource_control.md`
- 创建：`docs/harness-survey/22_configuration_identity_and_supply_chain.md`

**输入与产出：**
- 输入：完整的共性机制词汇。
- 产出：个案和最终综合章节使用的横切运行分析。

- [ ] **步骤 1：使用 `apply_patch` 创建四个提纲**

使用清单规定的标题。`20` 聚焦 CLI、TUI、IDE、Desktop、Web、API、审批、中断和
其他 Coding Agent 交互路径。

- [ ] **步骤 2：明确 Telemetry 的章节职责**

在 `19` 规划本地日志、产品 Telemetry、远程 Crash Report 的数据流和 opt-in/opt-out
控制；在 `22` 规划配置优先级、默认值和企业策略；两章都链接 `17` 的安全分析。

- [ ] **步骤 3：校验本组章节**

运行：

```bash
for f in docs/harness-survey/2[0-2]_*.md docs/harness-survey/19_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
done
rg -q 'opt-in' docs/harness-survey/19_observability_evaluation_and_replay.md
rg -q '企业策略' docs/harness-survey/22_configuration_identity_and_supply_chain.md
```

预期：四个提纲有效，Telemetry、隐私和配置的章节归属清楚。

### 任务 7：建立七个 Harness 个案提纲

**文件：**
- 创建：`docs/harness-survey/23_codex.md`
- 创建：`docs/harness-survey/24_opencode.md`
- 创建：`docs/harness-survey/25_pi.md`
- 创建：`docs/harness-survey/26_gemini_cli.md`
- 创建：`docs/harness-survey/27_deepseek_harness.md`
- 创建：`docs/harness-survey/28_goose.md`
- 创建：`docs/harness-survey/29_aider.md`

**输入与产出：**
- 输入：所有共性机制章节和已经初始化的源码树。
- 产出：Index 和综合章节引用的七条不同系统叙事。

- [ ] **步骤 1：使用 `apply_patch` 创建七个提纲**

使用个案清单规定的标题。每章必须提出不同的中心问题，并链接共性机制章，不重复
书写通用定义。

- [ ] **步骤 2：加入针对本章的源码地图**

记录架构、Loop、状态、Tool、扩展、安全、接口和代表性机制的具体顶层源码区域与
调查问题，不粘贴大型目录树。

- [ ] **步骤 3：校验差异性与覆盖范围**

运行：

```bash
for f in docs/harness-survey/2[3-9]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^## ' "$f")" -ge 5
  rg -q '源码地图' "$f"
done
```

预期：七个个案提纲均非空，都有源码地图和不同的 H1。

### 任务 8：建立综合章节和参考附录

**文件：**
- 创建：`docs/harness-survey/30_comparative_synthesis.md`
- 创建：`docs/harness-survey/31_design_principles.md`
- 创建：`docs/harness-survey/32_open_problems_and_research_agenda.md`
- 创建：`docs/harness-survey/90_glossary.md`
- 创建：`docs/harness-survey/91_version_manifest.md`
- 创建：`docs/harness-survey/92_evidence_index.md`
- 创建：`docs/harness-survey/93_references.md`

**输入与产出：**
- 输入：所有共性与个案提纲，以及固定版本的 Submodule 元数据。
- 产出：最终比较入口、术语、版本来源、证据映射和学术阅读入口。

- [ ] **步骤 1：使用 `apply_patch` 创建七个文件**

使用综合与附录清单规定的标题。附录可调整为表格和索引结构，但要保留提纲状态和
导航。

- [ ] **步骤 2：在 `91` 填入固定版本表**

写入父仓库 commit `b964dd3896239ff06e13c9efd363266755e5d9af` 和任务 1 的
七个精确 Submodule SHA。ref 名只用于记录来源，不作为稳定性分数。本文件只记录
版本和分析环境元数据。

- [ ] **步骤 3：在 `92` 定义证据索引结构**

定义章节到源码、Harness 到源码、结论/调用链/状态、运行证据、推断状态和规范化
Tool-call 字段映射的表格结构。

- [ ] **步骤 4：校验本组章节**

运行：

```bash
for f in docs/harness-survey/{30,31,32,90,91,92,93}_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
done
rg -q 'b964dd3896239ff06e13c9efd363266755e5d9af' docs/harness-survey/91_version_manifest.md
rg -q 'Tool-call' docs/harness-survey/92_evidence_index.md
```

预期：七个综合/参考文件均非空，并已记录固定的父仓库快照。

### 任务 9：建立叙事式 Index 和完整导航

**文件：**
- 创建：`docs/harness-survey/00_index.md`
- 修改：只修补缺少最终反向导航链接的编号章节。

**输入与产出：**
- 输入：已经存在的 36 个编号链接目标，以及 `WRITING_PLAN.md` 第 5.6 节的叙事式
  Index 设计。
- 产出：全书入口、就地机制链接、三种内容视角、四类读者路线和完整编号目录。

- [ ] **步骤 1：使用 `apply_patch` 编写六段叙事骨架**

按照 `00` 清单和已经批准的故事展开：配置解析修复请求、Workspace/Context 准备、
模型/Tool/权限循环、上下文压力、中断/委派、验证，以及 Harness 作为 Runtime 和控制层
的揭示。每节写入真实的中文提纲叙述，不写成文件链接列表。

- [ ] **步骤 2：加入随故事出现的机制链接**

普通叙事段落放置一至三个链接，紧跟在它所回答的问题之后。链接文字使用
`Tool Call 系统`、`Session、持久化与 Resume` 等内容名称，不暴露本地绝对路径。

- [ ] **步骤 3：加入三种内容视角和四类读者路线**

加入 `WRITING_PLAN.md` 第 5.5 节规定的初学者、工程师、平台开发者和安全研究者路线。

- [ ] **步骤 4：加入完整的 37 文件目录**

按编号列出每个文件的正式标题、一句读者问题和相对链接。明确所有章节处于提纲状态，
不暗示正文已经完成。

- [ ] **步骤 5：校验 Index 约定**

运行：

```bash
test -s docs/harness-survey/00_index.md
test "$(rg -c '^# ' docs/harness-survey/00_index.md)" -eq 1
test "$(rg -c '^## ' docs/harness-survey/00_index.md)" -ge 5
for f in $(find docs/harness-survey -maxdepth 1 -type f -regextype posix-extended -regex '.*/[0-9]{2}_.+\.md' -printf '%f\n' | sort); do
  rg -q "$f" docs/harness-survey/00_index.md
done
```

预期：一个 H1、至少五个叙事型 H2，并且目录包含全部 37 个编号文件名。

### 任务 10：执行覆盖整个报告目录的提纲校验

**文件：**
- 检查：所有 `docs/harness-survey/[0-9][0-9]_*.md`
- 修改：只修复未通过下列校验的文件。

**输入与产出：**
- 输入：完整提纲语料。
- 产出：结构有效、链接完整、可以评审的提纲版。

- [ ] **步骤 1：校验数量、非空文件、H1 唯一性和标题深度**

运行：

```bash
count=$(find docs/harness-survey -maxdepth 1 -type f -regextype posix-extended -regex '.*/[0-9]{2}_.+\.md' | wc -l)
test "$count" -eq 37
for f in docs/harness-survey/[0-9][0-9]_*.md; do
  test -s "$f"
  test "$(rg -c '^# ' "$f")" -eq 1
  test "$(rg -c '^#### ' "$f")" -eq 0
done
```

预期：正好 37 个非空文件，每个文件一个 H1，没有 H4。

- [ ] **步骤 2：校验 Markdown 相对链接目标**

运行：

```bash
cd docs/harness-survey
broken=0
while IFS= read -r target; do
  test -f "$target" || { printf 'broken link target: %s\n' "$target"; broken=1; }
done < <(rg --no-filename -o '\]\(([^)#]+\.md)(?:#[^)]+)?\)' -r '$1' [0-9][0-9]_*.md | sort -u)
test "$broken" -eq 0
```

预期：没有失效的 Markdown 文件链接。

- [ ] **步骤 3：扫描未完成标记和空白错误**

运行：

```bash
if rg -n 'TO''DO|TB''D|FIX''ME|[[:blank:]]+$' docs/harness-survey/[0-9][0-9]_*.md; then
  exit 1
fi
git diff --no-index --check /dev/null docs/harness-survey/00_index.md >/dev/null 2>&1 || test "$?" -eq 1
```

预期：没有未完成标记和行尾空白。no-index diff 只因文件为新文件而返回 `1`，不输出
空白错误。

- [ ] **步骤 4：校验编辑不变量和中文要求**

运行：

```bash
rg -q '叙事' docs/harness-survey/00_index.md
rg -q '代码' docs/harness-survey/01_scope_and_methodology.md
rg -q 'Session' docs/harness-survey/04_reference_architecture.md
rg -q 'Task DAG' docs/harness-survey/16_subagents_and_orchestration.md
rg -q 'Telemetry' docs/harness-survey/19_observability_evaluation_and_replay.md
rg -q '版本与分析环境' docs/harness-survey/91_version_manifest.md
if rg -n -P '^[A-Za-z][A-Za-z0-9 ,;:()/_-]{30,}[.!?]$' docs/harness-survey/[0-9][0-9]_*.md; then
  exit 1
fi
```

预期：所有已经批准的结构主题都有明确落点；代码块之外没有整段无中文解释的英文
论述。

- [ ] **步骤 5：检查最终 worktree 范围并创建范围受限的提交**

运行：

```bash
git status --short
git diff --check
git add -- docs/harness-survey
git diff --cached --name-status
git diff --cached --check
```

预期：只有 `docs/harness-survey/` 被暂存；Submodule 初始化没有改变记录的 gitlink；
暂存区不包含无关文件、凭据或私密配置。确认暂存内容后，创建一个范围明确的本地
提交；不推送。

## 执行完成后的报告内容

所有任务通过后，报告以下内容：

- 编号 Markdown 文件的准确数量；
- 每个文件均非空且只有一个 H1；
- 所有本地 Markdown 文件链接均可解析；
- `00_index.md` 包含叙事入口、三种内容视角、四类读者路线和完整目录；
- 七个 Submodule `HEAD` 与父仓库 gitlink 一致；
- 最终 `git status --short` 输出；
- 本地提交的 SHA 与准确文件清单；
- 没有推送远端。
