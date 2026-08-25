# Agent Harness 调研报告编写计划与编辑规范

## 1. 文档状态

- 文档性质：报告设计、章节规划与长期编辑规范
- 当前状态：总体方向已确认，叙事序章与第一部分 `00`–`04` 的读者版已经完成，
  后续核心机制章待分组撰写
- 最近修订：明确分离“读者正文”和“作者调查材料”。正文讲机制、案例与设计取舍，
  不展示源码目录、证据标签、检索流程或审稿过程；源码定位和证据状态只进入内部台账
- 报告工作标题：**Agent Harness：架构、工程与安全——七个开源系统的比较研究**
- 报告主语言：中文
- 首次出现的关键术语：中文名称后附英文，例如“工具调用（tool call）”
- 源稿格式：可移植 Markdown
- 计划输出：GitHub 可直接阅读的章节集合，以及未来由 Pandoc 汇编的 PDF
- 分析对象：Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、Goose、Aider
- 基准父仓库提交：`b964dd3896239ff06e13c9efd363266755e5d9af`

这份文件是报告的编辑章程，不纳入最终正文编号。最终报告以
`00_index.md` 为封面、目录和阅读入口。

## 2. 报告定位

本报告采用偏工程、教科书式、易读的混合研究报告定位：

1. 以真实 harness 的架构、数据流、状态机和实现取舍为主线；
2. 用论文、经典模型和系统原理解释工程设计的来源；
3. 避免堆砌源码、API 清单和项目 README 内容；
4. 同时服务初学者、工程人员、安全研究人员和未来的学术写作；
5. 结论受固定版本的代码和必要运行观察约束，但不把调查过程搬进正文。

“教科书式”不是把语言写得艰深，也不是在每节堆入定义和引用。正文应先在较高
层次解释问题为什么存在、机制解决什么问题，再逐步进入状态、数据流和真实系统
差异。概念表达保持朴实，必要处使用贯穿式示例帮助读者把抽象机制映射到一次
真实任务；学术引用和源码证据负责支持论述，不打断主要叙事。

建议的内容比例是：

- 60%–70%：工程机制、架构和真实系统比较；
- 15%–20%：学术背景、原理和相关工作；
- 10%–15%：设计权衡、安全含义和研究问题；
- 源码证据保存在作者内部台账中；正文把它翻译为机制说明、图、伪代码和例子。

上述比例用于控制写作重心，不作为机械的字数配额。

能力分析聚焦 Coding Agent 场景：文本和代码上下文、仓库探索、diff、Shell、测试、
Git、结构化 Tool result、Session 和工程 artifact。报告中的图片用于架构图或界面
说明，不把视觉理解、多模态 Prompt 或媒体生成扩展为独立比较轴。

## 3. 目标读者

### 3.1 主要读者

- 希望系统理解 agent harness 的软件工程师；
- 正在设计 coding agent、tool runtime 或 agent platform 的开发者；
- 研究 agent security、prompt injection、tool abuse 和 sandbox 的研究人员；
- 希望从模型层进入 agent systems 领域的学生和研究者。

### 3.2 读者前置知识

默认读者了解：

- 基本的大语言模型和 prompt 概念；
- 常见的命令行、文件系统和 Git 操作；
- 基本的软件架构和 API 概念。

不要求读者预先熟悉：

- MCP、ACP、agent loop 或 tool-call protocol；
- 七个项目的源码结构；
- capability security、event sourcing 或 context compaction。

术语首次出现时必须解释，不以项目内部命名代替通用概念。

## 4. 报告目标与非目标

### 4.1 报告目标

报告完成后，读者应能够：

1. 解释 agent harness 与模型、agent framework、MCP server、IDE agent、云端
   control plane 和 benchmark harness 的区别；
2. 描述一次 agent turn 从输入、推理、工具执行到持久化的完整生命周期；
3. 理解 harness loop、tool system、context、memory、skills、session、compaction、
   planning、subagent 和 security 等核心机制；
4. 比较七个 harness 在同一机制上的不同设计；
5. 识别每个 harness 最有代表性的架构特征和安全边界；
6. 根据使用场景选择或设计合适的 harness 架构；
7. 从工程问题中发现可进一步研究的学术问题。

### 4.2 非目标

本报告不应成为：

- 七个项目安装命令和配置项的完整手册；
- 七份项目 README 的拼接；
- 逐文件、逐函数的源码导读；
- 未经运行验证的漏洞报告；
- 模型能力排行榜或主观产品测评；
- GitHub stars、下载量或营销功能的简单比较；
- MCP、prompt engineering 或 multi-agent 的独立百科全书。

## 5. 三视角组织模型

报告使用三个互补视角组织同一批知识，避免把正文写三遍。

### 5.1 横向机制视角

横向视角以“同一个机制，七个系统分别如何实现”为问题，建立能力地图和
比较矩阵。它适合已有 agent 基础、希望快速查询特定机制的读者。

横向总览位于 `02_horizontal_capability_map.md`，详细内容由机制章节承担。

### 5.2 纵向生命周期视角

纵向视角沿一次完整 agent 任务的执行过程前进：

```text
启动与配置
  → Session 创建或恢复
  → 指令与上下文构造
  → Goal 与计划
  → 模型调用
  → Tool call
  → 权限判断
  → Tool 执行
  → Observation
  → Loop 继续、委派或压缩
  → 验证、持久化与结束
  → 后续 Resume
```

纵向总览位于 `03_vertical_lifecycle_walkthrough.md`。该章负责串联机制，不
重复详细机制章的完整内容。

### 5.3 系统个案视角

系统个案分别解释七个 harness 如何组合共性机制，以及这种组合体现了怎样的
设计哲学。个案章不重复介绍通用概念，而是通过交叉链接引用机制章。共性机制章
可以用“特色机制”框就地提示少数系统的异质设计；个案章负责把这些局部差异
还原到系统整体架构、历史约束和设计哲学中。

### 5.4 三个视角之间的链接规则

- 横向总览的每一项能力必须链接到一个详细机制章；
- 纵向总览的每一个生命周期阶段必须链接到一个或多个详细机制章；
- 每个详细机制章必须链接到相关个案章的小节；
- 每个个案章必须反向链接到相关机制章；
- 共性章中的特色机制框必须链接到对应个案章，个案章不得原样复制该框；
- 综合比较章只总结已经由机制章和个案章支持的结论；
- 不为制造对称性而复制大段文字。

### 5.5 从内容视角到读者路线

横向、纵向和个案是内容组织视角，不直接等于读者的阅读顺序。`00_index.md` 应把
三种视角进一步映射到读者画像，并明确哪些章节可以稍后再读：

| 读者 | 建议起点和主线 | 可以稍后阅读 |
|---|---|---|
| 第一次接触 Harness 的读者 | `00` → `01` → `03` → `04` → `05` → `07` → `08` → `12` → 任选一个个案章 → `30` | 研究议程和与当前问题无关的个案 |
| 使用或评估 Coding Agent 的工程师 | `00` → `02` → 按问题进入 `05`–`22` → 相关个案章 → `30` | 与当前工程问题无关的学术框和其他个案 |
| 设计 Harness 或 Agent Platform 的开发者 | `01` → `04` → `05`–`22` → `23`–`30` → `31` | `32` 和主题参考文献可按需进入 |
| 安全研究者 | `01` → `04` → `07`–`10` → `12` → `16`–`17` → `19` → `22` → `30`–`32` | UI 细节和非相关项目实现 |

初学者路线先建立“一个任务为什么需要 Harness、又如何流经 Harness”的直觉。
证据等级、有效性审查和调查清单属于作者工作流，不构成读者路线。

### 5.6 叙事式 Index 的职责

`00_index.md` 不是文件链接清单，而是一篇可以独立阅读的序章。它沿全书主教学
案例展开：用户要求 Coding Agent 在已有仓库中定位并修复一个配置解析错误，运行
测试并解释修改。叙事逐步揭示模型之外的工作：发现 workspace、组装指令和上下文、
形成 Tool call、审批和执行、接收 Observation、继续 Loop、处理中断和 Resume、
控制 Token、必要时委派 Subagent，最后验证修改并留下可恢复的 Session 状态。

每当故事遇到一个新的工程问题，就在解释之后自然链接到对应章节。例如，“模型的
动作如何变成一次可执行调用”链接到 `08_tool_call_system.md`，“中断以后保留了
什么”链接到 `12_session_persistence_and_resume.md`，“上下文装不下时怎么办”
链接到 `13_compaction_and_context_management.md` 和
`14_token_efficiency_and_cost_control.md`。链接文本本身应表达问题或答案，不使用
裸文件名和连续的“参见第 X 章”。

故事推进到任务完成后，再从这一次任务抽象出 Harness 的工作定义、七个研究对象、
横向/纵向/个案三种内容视角和四类读者路线，最后给出完整目录。这样第一次阅读按
叙事建立整体直觉，后续回查仍可直接使用目录。

`00`、`03` 和 `04` 的分工必须保持清楚：

- `00` 回答“为什么一个看似简单的 Coding 任务需要 Harness”，使用少量代表性
  场景和就地链接，不展开完整状态机；
- `03` 回答“任务实际经过哪些生命周期阶段”，使用正式时序、分支、错误和恢复
  路径，并系统链接全部机制章；
- `04` 回答“这些阶段由哪些组件和状态对象构成”，给出统一参考架构和工作定义。

序章中的故事是由后文代码证据支持的组合式教学案例，不冒充某一个 Harness 的
逐步运行记录。它不提前给出七系统排名，也不重复各章的详细比较结论。

写作时使用下面的故事节点控制信息出现顺序。该表是作者检查表，成稿使用连续段落，
不直接把表格搬进序章：

| 故事节点 | 读者此时产生的问题 | 自然进入的章节 |
|---|---|---|
| 用户提出“修复配置解析错误并运行测试” | 模型如何知道仓库、规则和当前状态 | `07` Context、`18` Workspace |
| Agent 读取文件并提出下一步动作 | 模型如何接入、消息如何表示、Loop 如何继续 | `05` Loop、`06` Provider |
| 动作变成读取、编辑或测试命令 | 意图怎样变成结构化 Tool call，结果如何关联 | `08` Tool Call |
| 命令需要权限并可能产生副作用 | 谁授权，执行在哪里隔离，用户何时介入 | `17` Security、`20` Human-in-the-loop |
| 任务积累大量输出并接近上下文上限 | 哪些内容保留、压缩、缓存或外部化 | `10` Memory、`13` Compaction、`14` Token |
| 任务中断，或一部分工作被委派 | 状态如何恢复，子任务如何创建、通信和汇聚 | `12` Session、`15` Goal、`16` Subagent |
| 修改完成并运行测试、生成 diff | 如何验证、记录事件并完成 Coding 闭环 | `18` Workspace、`19` Observability、`21` Reliability |
| 同一个任务在不同产品中表现不同 | 差异来自模型还是 Harness 设计 | `02` 横向地图、`23`–`30` 个案与综合 |

故事不要求每个节点篇幅相等。开头和 Harness 概念揭示应写得最完整，中间机制用
足以产生问题的细节带过，链接后的章节负责深入。Telemetry、供应链和研究议程等
不适合强塞进任务情节的主题，在故事结束后的全书问题地图中自然补入。

## 6. 目录与文件规划

计划目录为 `docs/harness-survey/`。正文和附录共规划 36 个编号 Markdown 文件；
源码证据台账另存于忽略目录，不计入读者章节。
编号使用两位数字，确保文件系统排序、GitHub 浏览顺序和 PDF 汇编顺序一致。

### 6.1 封面、导论与两套总览

#### `00_index.md`：叙事式序章、摘要、导读与目录

建议叙事结构。下面是覆盖检查表，成稿时合并成约五至六个有连续过渡的二级小节：

- 从熟悉的 Coding Agent 体验进入：一个配置解析错误
- 模型之外，谁找到仓库、准备上下文并执行动作
- 当任务变长、被打断或需要委派时，Harness 还要处理什么
- 从一次任务抽象出 Agent Harness 的工作定义
- 为什么比较 Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、Goose 和 Aider
- 三种内容视角与四类读者路线
- 完整目录、版本、在线阅读和 PDF 约定

序章中的机制链接按故事发生顺序就地出现。每个自然段通常不超过一至三个正文链接，
避免把叙事变成高密度超链接墙；完整而机械的文件映射只放在末尾目录。

#### `01_introducing_agent_harness.md`：认识 Agent Harness

建议章节标题：

- 从一个修复任务看模型之外的工作
- Agent Harness 的工作定义
- Harness 与模型、工具和工作区的关系
- 七个系统提供的不同观察窗口
- 本报告将沿哪两条主线展开
- 本章小结

版本固定、代码调查、论文检索、证据等级、公平性审查和有效性边界属于本编写计划
及内部结论—证据台账，不作为第 01 章或其他读者正文的教学内容。正文只用一小段
朴素语言说明研究对象是七个固定版本，并聚焦 Coding Agent 场景。

#### `02_horizontal_capability_map.md`：横向能力地图

建议章节标题：

- 如何阅读横向地图
- Harness 能力分类法
- 七个项目总览
- 核心能力矩阵
- 架构谱系
- 扩展性与控制力谱系
- 自治程度与安全边界谱系
- 按主题进入详细章节
- 横向观察小结

#### `03_vertical_lifecycle_walkthrough.md`：纵向生命周期导览

建议章节标题：

- 示例任务与分析边界
- 统一生命周期概览
- 启动、配置和认证
- Workspace 发现与信任
- Session 创建或恢复
- 指令和上下文组装
- Goal 与计划建立
- 模型请求和流式响应
- Tool call 生成与规范化
- 权限、审批和沙箱
- Tool 执行与 Observation
- Loop 继续、错误恢复与取消
- Compaction、Memory 和上下文压力
- Subagent 委派和并发
- 文件修改、测试与 Git
- 完成、持久化与 Resume
- 七个 Harness 的路径差异
- 本章小结与详细章节索引

#### `04_reference_architecture.md`：统一参考架构

建议章节标题：

- 为什么需要统一参考架构
- 控制平面与执行平面
- 模型层、编排层和能力层
- 状态层与持久化层
- 客户端和协议层
- 信任边界
- Session、Turn、Message、Event、Item、Context、Memory 和 Artifact 的最小工作定义
- 统一事件和状态模型
- Context、Session、Memory 与 Compaction 的边界图
- 七个系统到参考架构的映射
- 参考架构的局限
- 本章小结

### 6.2 共性核心机制

#### `05_harness_loop.md`：Harness Loop

- 从一次 Turn 到 Agent Loop
- Loop 的输入、输出和不变量
- 推理—行动—观察循环
- 流式事件和增量状态
- 多工具调用与并行调用
- 终止条件和防失控机制
- 七个实现的 Loop 结构
- 代表性案例
- 设计取舍
- 安全与可靠性含义
- 本章小结
- 内部证据台账（不进入正文）

#### `06_model_and_provider_abstraction.md`：模型与 Provider 抽象

- Provider 层解决的问题
- 消息、代码、文本内容块和角色模型
- 流式响应
- Tool-call 格式差异
- 模型能力发现与协商
- 路由、fallback 和模型切换
- Token、成本和速率限制
- API key、OAuth 与订阅认证
- 七个系统比较
- Provider 抽象泄漏
- 安全与隐私
- 本章小结
- 内部证据台账（不进入正文）

#### `07_context_and_instruction_system.md`：上下文构造与指令系统

- Context 不只是 Prompt
- 指令来源和优先级
- System、用户和项目指令
- Workspace 探索与代码上下文
- 文件选择、repo map 与检索
- 动态上下文和工具描述
- Context 的 Token 和容量预算
- 不可信内容和 Prompt Injection
- 七个系统比较
- 设计取舍
- 本章小结
- 内部证据台账（不进入正文）

#### `08_tool_call_system.md`：Tool Call 系统

- 工具作为模型行动空间
- Tool schema 与注册表
- 七系统 Tool-call request、response、streaming、error 和 approval envelope 的规范化对照
- 发现、选择和调用
- 参数解析与验证
- Call ID、结果关联和并行调用
- 文件、Shell、网络和搜索工具
- Observation 表示
- 错误返回和重试语义
- 七个系统比较
- 安全边界
- 本章小结
- 内部证据台账（不进入正文）

#### `09_plugins_mcp_and_extensions.md`：Plugin、MCP 与扩展系统

- 为什么 Harness 需要扩展
- Plugin、Extension、MCP、Skill 和 Hook 的区别
- 插件生命周期
- 依赖注入、服务注册和事件总线
- MCP transport、能力发现和工具暴露
- Client、Server 与双向能力
- 扩展配置和分发
- 七个系统比较
- 供应链与信任边界
- 组合失效模式
- 本章小结
- 内部证据台账（不进入正文）

#### `10_memory.md`：Memory

- 前置定义：引用 `04_reference_architecture.md` 中的 Session、Context 和状态对象
- Harness 中的 Memory 是什么
- Working、episodic、semantic 与 procedural memory
- 显式记忆和隐式状态
- 写入、检索、更新和遗忘
- 项目级、用户级和 Session 级记忆
- 向量检索与结构化存储
- Memory 与 Context、Session、Compaction 的边界
- 七个系统比较
- 污染、投毒、隐私和陈旧信息
- 设计建议
- 本章小结
- 内部证据台账（不进入正文）

#### `11_skills_prompts_commands_and_hooks.md`：Skills、Prompt、Command 与 Hook

- 四类机制的工作定义
- 静态指令与可执行能力
- Skill 的发现、选择和加载
- Slash command 和用户显式控制
- Prompt template 和项目定制
- Hook 与生命周期拦截
- 参数、上下文和权限继承
- 七个系统比较
- 可移植性与生态兼容
- 安全与供应链
- 本章小结
- 内部证据台账（不进入正文）

#### `12_session_persistence_and_resume.md`：Session、持久化与 Resume

- Session 的边界
- Turn、Message、Event 和 Item
- Session 状态机
- Event sourcing、snapshot 和 checkpoint
- Resume、replay、branch 与 fork
- Tool call 的恢复一致性
- 进程状态与外部副作用
- Session 查询、导出和共享
- 七个系统比较
- 崩溃一致性和安全问题
- 本章小结
- 内部证据台账（不进入正文）

#### `13_compaction_and_context_management.md`：Compaction 与上下文管理

- 前置定义：引用 `04_reference_architecture.md` 中的 Session、Context、Event 和 Artifact
- 为什么需要 Compaction
- 截断、摘要、选择和外部化
- 自动和手动 Compaction
- 信息保真度与摘要漂移
- Tool result 和文件内容压缩
- Compaction 与 Memory 的分工
- Resume 后的上下文重建
- 七个系统比较
- 评价指标和失效模式
- 本章小结
- 内部证据台账（不进入正文）

#### `14_token_efficiency_and_cost_control.md`：Token 效率与成本控制

- 为什么 Token 效率值得独立分析
- Token 使用的完整账本：input、output、reasoning、cache read 和 cache write
- Context window、计费 Token、延迟和内存占用的区别
- 减少输入：上下文选择、repo map、检索和按需加载
- 减少工具上下文：输出截断、摘要、pruning、spill 和 locator
- 重用前缀：Prompt caching、KV cache 和稳定请求前缀
- 减少输出：max output、verbosity、thinking/reasoning budget 和 edit format
- 使用更便宜的路径：模型路由、weak model 和任务分层
- Compaction、Memory 与 Token 效率的关系
- Subagent 是节省主上下文还是放大总 Token
- Token telemetry、成本显示和预算控制
- 七个系统比较
- 评价指标：tokens/task、billable tokens、cache hit、cost、latency 和 success
- 质量、安全与成本之间的权衡
- 本章小结
- 内部证据台账（不进入正文）

初始证据线索：

- **Codex**：检查 session 级 `prompt_cache_key`、`cached_input_tokens`、自动
  compaction token limit、tool output truncation、`max_output_tokens`、verbosity
  和 reasoning 配置；入口包括 `codex-rs/core/src/client.rs`、
  `codex-rs/core/src/compact_token_budget.rs`、
  `codex-rs/models-manager/src/model_info.rs` 和
  `codex-rs/protocol/src/openai_models.rs`；
- **OpenCode**：检查 input/output/reasoning/cache usage、cost、session pruning、
  overflow recovery 和 tool truncation；入口包括
  `packages/opencode/src/session/compaction.ts`、
  `packages/opencode/src/session/message-v2.ts`、
  `packages/opencode/src/session/llm/ai-sdk.ts` 和
  `packages/opencode/src/tool/truncate.ts`；
- **Pi**：检查 input/output/cache-read/cache-write 成本桶、context window、
  max tokens、prompt cache、compaction reserve、retained tail 和 tool truncation；
  入口包括 `packages/ai/src/types.ts`、
  `packages/agent/src/harness/compaction/compaction.ts` 和
  `packages/agent/src/harness/utils/truncate.ts`；
- **Gemini CLI**：检查不同认证路径下的 automatic token caching、`/stats`、
  compression threshold、tool distillation、maximum output 和 thinking budget；
  入口包括 `docs/cli/token-caching.md`、`docs/reference/configuration.md`、
  `packages/core/src/context/chatCompressionService.ts` 和
  `packages/core/src/context/toolDistillationService.ts`；
- **DeepSeek Harness**：检查 replay-aware token meter、uncached/cache-read/
  cache-write 计量、context pressure、model-free pruning、spill preview 和 locator，
  以及 KV cache 影响；入口包括 `packages/llm/token-meter/README.md`、
  `packages/compaction/README.md`、
  `packages/compaction/compaction-tool-result-pruner/README.md` 和
  `packages/spill/README.md`；
- **Goose**：检查 structured compaction、默认阈值、summarizer overflow 时的
  progressive tool-response removal、usage/cost、context-limit cache、fast model
  和 one-shot compaction；入口包括
  `crates/goose-context-management/src/lib.rs`、`summarize.rs`、`provider.rs`
  和 `crates/goose/src/model_config.rs`；
- **Aider**：检查 dynamic repo-map budget、`--map-tokens`、prompt cache
  keepalive、history summarization、`/tokens`、weak model、thinking budget 和 edit
  format 的成本影响；入口包括 `aider/website/docs/repomap.md`、
  `aider/website/docs/usage/caching.md`、
  `aider/website/docs/config/dotenv.md`、`aider/commands.py` 和
  `aider/coders/base_coder.py`。

#### `15_goals_planning_and_todos.md`：Goal、Planning 与 Todo

- Goal、Plan、Task 和 Todo 的区别
- ReAct 与 Plan-and-Execute
- 计划模式和执行模式
- 任务分解、进度和完成判定
- 用户确认与计划修改
- Goal 持久化和恢复
- 预算、停止条件和阻塞状态
- 七个系统比较
- 形式化状态与自然语言计划
- 安全和可靠性
- 本章小结
- 内部证据台账（不进入正文）

#### `16_subagents_and_orchestration.md`：Subagent 与多 Agent 编排

- 为什么需要 Subagent：专业化、并行、隔离与上下文压缩
- Subagent、Agent Role、多模型流水线与 Workflow 的区别
- 创建路径：spawn、fork、delegate、task tool 和外部进程
- Parent、Child、Task、Thread、Session 和 Activation 的关系
- 身份、lineage、delegation depth 和生命周期状态
- 初始 Prompt：显式任务、完整父历史、摘要或共享前缀
- Context 继承、隔离和 workspace 共享
- Memory、Session、文件、artifact 和共享存储
- 工具、Skill、Provider、模型和权限继承
- Follow-up、steering、send-message 和双向通信
- Progress、notification、settlement notice 和结果回传
- 同步原语：wait、join、barrier、completion 和 cancellation
- 拓扑区别：父子树、Agent graph、Task DAG 和 Workflow graph
- 依赖检查、环检测、稳定排序和就绪节点
- 并发上限、背压、公平性和资源预算
- 同文件写入、共享外部副作用和 race condition
- 失败传播、重试、中断、关闭和 orphan task
- 结果汇聚、provenance 和冲突解决
- Token 经济性：主上下文压缩、重复前缀和总成本放大
- 七个系统比较
- Multi-agent 的适用边界
- 安全、责任归属与资源放大风险
- 本章小结
- 内部证据台账（不进入正文）

本章必须严格区分四类经常被混用的结构：

1. **父子拓扑或 provenance graph**：记录谁创建了谁、信息如何流动，但不必然
   执行任务依赖；
2. **Task DAG**：表达依赖边、ready/blocked 状态、环检测和调度准入；
3. **运行时同步原语**：`wait`、`join`、barrier、completion 和 cancellation，
   决定下游是否真正等待上游；
4. **Workflow graph**：显式 recipe 或 pipeline，可能顺序或并行，但不必然是
   通用多 Agent DAG scheduler。

只有同时找到执行数据结构、依赖准入规则、环处理、完成条件、失败传播、取消
语义、共享副作用策略和运行测试时，才能写“该 Harness 保证 DAG 同步”。仅有
agent graph、任务列表或 prompt 中的协作说明，不足以形成该结论。

初始证据线索：

- **Codex**：检查 spawn、follow-up、send-message、wait、close 等协作工具，
  `codex-rs/agent-graph-store/` 的持久化父子拓扑、共享 root trace、信息流边和
  subagent result notification；不得把拓扑图直接写成 task-DAG scheduler；
- **OpenCode**：检查 `packages/opencode/src/tool/task.ts` 的前台与实验性后台
  subagent、child session `parentID`、completion notification、`task_id` resume、
  depth limit，以及 `packages/opencode/src/agent/subagent-permissions.ts` 的派生权限；
- **Pi**：核心 coding CLI 不把 subagent 作为内建主路径，应把
  `packages/coding-agent/examples/extensions/subagent/` 标记为官方扩展示例；分析其
  独立进程、隔离 context、streaming progress、并发上限、chain handoff、usage/
  cost 统计和结果截断；
- **Gemini CLI**：检查 `docs/core/subagents.md`、
  `packages/core/src/agents/agent-tool.ts`、local/remote subagent protocol、parent
  association、单一摘要回传和中间更新；另检查
  `packages/core/src/services/trackerService.ts` 与 prompts 中的依赖和环检查，区分
  runtime enforcement 与模型指令；
- **DeepSeek Harness**：以 `packages/subagent/subagent/README.md` 及相关 driver
  为入口，检查 named provider、one-shot/continuable child、follow-up、report、
  interrupt、durable descriptor、cold resume、FIFO turn、settlement notice、
  child-first draining、深度、所有权、并发与策略继承；持久层级仍不自动等于 DAG；
- **Goose**：检查 delegation runtime、CLI notification、context-engineering
  subagent 文档和 recipe/subrecipe；区分通用 delegation、特定产品路径的并行
  orchestration 与 recipe 依赖，不预设存在统一 DAG 保证；
- **Aider**：把 architect/editor 固定双模型流水线和 weak-model 辅助角色作为
  对照案例；除非后续证据改变结论，不把它们归类为通用 first-class subagent
  runtime。

#### `17_security_permissions_and_sandboxing.md`：安全、权限与沙箱

- 资产、主体、能力和信任边界
- Threat model
- Human approval
- Permission policy
- 文件系统、进程和网络沙箱
- Workspace trust
- Credential isolation
- Telemetry、crash report、prompt/tool 内容和使用数据的外传边界
- Prompt injection 到工具执行的攻击链
- Plugin、MCP、Skill 和 Hook 风险
- Session、Memory 和 Resume 风险
- 七个系统安全模型比较
- 安全保证的证据等级
- 本章小结
- 内部证据台账（不进入正文）

#### `18_code_editing_git_and_workspace.md`：代码编辑、Git 与 Workspace

- Coding Harness 的特殊能力
- Workspace 发现和作用域
- 直接写入、Patch 与结构化编辑
- Diff 展示和用户审查
- Git 状态、提交和回滚
- Ignore、敏感文件和未跟踪文件
- Worktree、Submodule 和大型仓库
- Test、Lint 与构建闭环
- 七个系统比较
- 数据损坏和供应链风险
- 本章小结
- 内部证据台账（不进入正文）

#### `19_observability_evaluation_and_replay.md`：观测、评测与回放

- 为什么 Harness 需要可观测性
- Log、Event、Trace 和 Metric
- 模型请求和 Tool call 关联
- 本地日志、产品遥测和远程 crash report 的数据流
- 默认采集、opt-in/opt-out、保留周期、脱敏和删除控制
- Prompt、Tool result、文件路径与环境元数据的隐私边界
- Token、成本和延迟
- Session replay 与确定性边界
- Debug bundle 和隐私脱敏
- Harness eval 与模型 eval 的区别
- 七个系统比较
- 运行验证的环境控制
- 本章小结
- 内部证据台账（不进入正文）

#### `20_interfaces_and_human_in_the_loop.md`：接口与 Human-in-the-loop

- CLI、TUI、Web、Desktop、IDE 和 API
- Headless 与 non-interactive 模式
- ACP、JSON-RPC 和应用服务器
- 用户审批、编辑和中断
- Plan/Build 等模式切换
- 流式反馈和进度展示
- Accessibility 与可解释性
- 多客户端状态一致性
- 七个系统比较
- UI 与安全策略的耦合
- 本章小结
- 内部证据台账（不进入正文）

#### `21_reliability_and_resource_control.md`：可靠性与资源控制

- Failure model
- Retry、backoff 和 fallback
- Timeout、cancel 和 interrupt
- 幂等性和副作用
- 后台进程和资源清理
- Loop、token、cost 和并发预算
- 网络中断和 provider failure
- 崩溃恢复
- 七个系统比较
- 可靠性与自治程度的权衡
- 本章小结
- 内部证据台账（不进入正文）

#### `22_configuration_identity_and_supply_chain.md`：配置、身份与供应链

- 配置层级和覆盖规则
- 用户、项目和企业配置
- Agent identity 与调用 provenance
- Provider credentials
- Telemetry 和 crash reporting 的配置层级、默认值与企业策略
- Plugin、MCP 和 Skill 安装来源
- 自动更新和二进制分发
- Dependency 与 package lifecycle
- 企业策略和集中管理
- 七个系统比较
- 配置注入与供应链风险
- 本章小结
- 内部证据台账（不进入正文）

### 6.3 七个 Harness 个案

个案章节使用统一骨架，但中心问题必须不同。

#### `23_codex.md`：Codex——安全控制面与多入口 Runtime

- 项目定位和演进
- 总体架构
- Rust core、protocol 与 app server
- Loop、event 和 rollout
- Approval、sandbox 和 exec policy
- MCP、skills、plugins、memory 与 subagent
- CLI、IDE、App 和服务接口
- 独特设计取舍
- 安全边界和失效模式
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `24_opencode.md`：OpenCode——多模型平台与 Agent Mode

- 项目定位和演进
- TypeScript/Bun 平台架构
- Core、server、TUI、desktop 和 SDK
- Build、Plan 与 General agent
- Provider、tool、plugin 和 MCP
- Session 与存储
- 独特设计取舍
- 安全边界和失效模式
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `25_pi.md`：Pi——极简、自扩展的 Agent Runtime

- 项目定位和设计哲学
- Agent core、AI abstraction、coding agent 和 TUI
- Loop 与 tool state
- Extension、prompt、skill 和 session backend
- Telemetry 和协议组件
- 无内建 Permission System 的边界
- 外部容器与沙箱模式
- 独特设计取舍
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `26_gemini_cli.md`：Gemini CLI——搜索增强、扩展与自动化

- 项目定位和架构
- CLI、core、SDK 和 IDE companion
- Gemini provider 和流式工具调用
- Search grounding 与 Web 工具
- MCP、extensions、skills 和 hooks
- Planning、checkpoint 和 non-interactive
- Permission 与 sandbox
- 独特设计取舍
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `27_deepseek_harness.md`：DeepSeek Harness——Everything Is a Plugin

- 项目定位和开发阶段
- Cordis 与组合式架构
- Service、provider、consumer 和 dependency injection
- Agent scope、session 和 context
- Tool、MCP、ACP、skill 和 subagent
- Guard、sandbox 和 shell provider
- Web host、workflow、schedule 和 job
- 独特设计取舍
- 组合失效和安全边界
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `28_goose.md`：Goose——通用本地 Agent 与 MCP 生态

- 项目定位和治理
- Rust core、CLI、desktop 和 API
- Provider abstraction 与 ACP
- MCP extensions 和 recipes
- Context management
- Tool visibility 与自定义发行版
- 独特设计取舍
- 安全边界和失效模式
- 与其他 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

#### `29_aider.md`：Aider——Git-centric Coding Agent

- 项目定位和历史角色
- Python 架构与 coder abstraction
- Repo map 和上下文选择
- Edit format、patch 和代码修改循环
- Git commit、lint 和 test
- 多模型与本地模型
- 独特设计取舍
- 安全边界和失效模式
- 与现代平台型 Harness 的比较
- 适用场景
- 本章小结
- 内部源码地图（不进入正文）

### 6.4 综合结论

#### `30_comparative_synthesis.md`：综合比较

- 比较问题回顾
- 能力矩阵最终版
- 架构类型和谱系
- Loop 与状态模型比较
- 扩展机制比较
- Context、Memory 与 Compaction 比较
- Token 效率、缓存和成本控制比较
- Permission 与 Sandbox 比较
- Session 与 Resume 比较
- Multi-agent 和自动化比较
- 工程复杂度与可维护性
- 适用场景决策表
- 主要结论

#### `31_design_principles.md`：Harness 设计原则

- 明确控制平面与执行平面
- 把工具发现和工具授权分离
- 让权限随能力而不是 UI 模式传播
- 让 Session 状态可恢复但不过度信任
- 把 Context、Memory 和 Compaction 分层
- 把 Token 计量、上下文压力和实际计费分开
- 对外部副作用建立可验证边界
- 把扩展生命周期纳入安全模型
- 为失败、取消和资源上限设计
- 保留可观测性和 provenance
- 渐进式自治与 Human-in-the-loop
- 原则之间的冲突与取舍

#### `32_open_problems_and_research_agenda.md`：开放问题与研究议程

- Harness 的形式化模型
- Tool-use 安全和 capability control
- Prompt injection 的系统级防御
- Memory 污染和长期一致性
- Compaction 的可验证保真度
- Token 效率的公平评价和质量边界
- Resume、replay 和副作用一致性
- Multi-agent 权限和责任归属
- MCP 与插件供应链
- Harness benchmark 和评测方法
- 真实使用数据与版本漂移
- 标准化机会
- 未来 corpus 扩展方向

### 6.5 附录

#### `90_glossary.md`：术语表

- 通用 Agent 术语
- Harness 架构术语
- Tool 与扩展术语
- 状态与持久化术语
- 安全术语
- 七个项目的专有术语映射

#### `91_version_manifest.md`：版本与分析环境清单

- 父仓库版本
- 七个 Submodule 的 commit、上游默认分支、所选 ref 类型和许可证
- 分支或 tag 名只记录来源，不直接作为稳定性权重
- 分析日期
- 运行验证实际涉及的操作系统、架构和必要工具链版本
- 影响运行结论的模型、Provider、权限和关键配置
- 环境信息的脱敏规则
- 后续更新策略
- 版本差异记录

源码路径、symbol、调用链、测试和证据状态不再规划为读者附录。它们保存在
`.superpowers/sdd/WRITING_PLAN/` 下的内部结论—证据台账，供作者、审稿与后续更新
使用。若未来确需公开研究数据，应另行设计可检索的数据集，而不是把目录清单混入
教科书正文。

#### `93_references.md`：参考文献阅读入口

- Agent loop 与 reasoning/action
- Tool use 和 function calling
- Planning 与 multi-agent
- Memory 与 context management
- Security 与 capability systems
- Software agents 和 coding agents
- Protocol、MCP 与 interoperability
- 各主题的关键问题、代表性工作与进一步阅读顺序
- 正文中学术概念与工程章节的对应关系
- 完整参考文献说明

正式文献元数据在证据准备阶段存入 `references.bib`；本章负责提供按主题组织的阅读指南，
不向读者展示检索日志、元数据核验或去重流程，也不手工复制 BibTeX 生成的完整参考文献列表。

### 6.6 双视角映射表

横向视角按主题进入详细章：

| 横向主题 | 详细章节 |
|---|---|
| 统一架构与控制流 | `04_reference_architecture.md`、`05_harness_loop.md` |
| 模型、上下文与推理输入 | `06_model_and_provider_abstraction.md`、`07_context_and_instruction_system.md` |
| 工具和扩展能力 | `08_tool_call_system.md`、`09_plugins_mcp_and_extensions.md` |
| Tool-call 接口形态与字段映射 | `06_model_and_provider_abstraction.md`、`08_tool_call_system.md` |
| 长短期状态 | `10_memory.md`、`12_session_persistence_and_resume.md`、`13_compaction_and_context_management.md` |
| Token 效率与成本 | `14_token_efficiency_and_cost_control.md` |
| 显式行为定制 | `11_skills_prompts_commands_and_hooks.md` |
| 目标与多 Agent 编排 | `15_goals_planning_and_todos.md`、`16_subagents_and_orchestration.md` |
| 安全与执行边界 | `17_security_permissions_and_sandboxing.md` |
| Coding Agent 的工程闭环 | `18_code_editing_git_and_workspace.md` |
| 观测、接口与可靠性 | `19_observability_evaluation_and_replay.md`、`20_interfaces_and_human_in_the_loop.md`、`21_reliability_and_resource_control.md` |
| Telemetry、隐私和数据外传 | `17_security_permissions_and_sandboxing.md`、`19_observability_evaluation_and_replay.md`、`22_configuration_identity_and_supply_chain.md` |
| 配置、身份和软件供应链 | `22_configuration_identity_and_supply_chain.md` |

纵向生命周期按执行阶段进入详细章：

| 生命周期阶段 | 主要章节 |
|---|---|
| 启动、配置、身份和 Provider 认证 | `06_model_and_provider_abstraction.md`、`22_configuration_identity_and_supply_chain.md` |
| Workspace 发现与信任判断 | `07_context_and_instruction_system.md`、`17_security_permissions_and_sandboxing.md`、`18_code_editing_git_and_workspace.md` |
| Session 创建或恢复 | `12_session_persistence_and_resume.md` |
| 指令、Skill 和上下文构造 | `07_context_and_instruction_system.md`、`11_skills_prompts_commands_and_hooks.md` |
| Goal、Plan 和 Todo 建立 | `15_goals_planning_and_todos.md` |
| 模型请求与流式响应 | `05_harness_loop.md`、`06_model_and_provider_abstraction.md` |
| Tool 发现、选择和参数解析 | `08_tool_call_system.md`、`09_plugins_mcp_and_extensions.md` |
| 权限判断、审批和隔离 | `17_security_permissions_and_sandboxing.md`、`20_interfaces_and_human_in_the_loop.md` |
| Tool 执行和代码修改 | `08_tool_call_system.md`、`18_code_editing_git_and_workspace.md` |
| Observation、日志和结果关联 | `05_harness_loop.md`、`19_observability_evaluation_and_replay.md` |
| Retry、Timeout、Cancel 和资源控制 | `21_reliability_and_resource_control.md` |
| Compaction、长期记忆和 Token 压力 | `10_memory.md`、`13_compaction_and_context_management.md`、`14_token_efficiency_and_cost_control.md` |
| Subagent 创建、通信、同步和汇聚 | `16_subagents_and_orchestration.md` |
| 验证、持久化和完成 | `12_session_persistence_and_resume.md`、`19_observability_evaluation_and_replay.md` |
| 后续 Resume、Replay、Branch 或 Fork | `12_session_persistence_and_resume.md` |

个案章节 `23_codex.md` 至 `29_aider.md` 为第三套入口。横向和纵向总览只做
导航与综合；详细机制在共性章完整解释。局部系统差异可在共性章用“特色机制”框
就地说明，系统特性之间的组合关系只在个案章深入展开。

## 7. 横向能力状态标签

下面的标签供作者内部建表和核验，不在读者正文中形成一套必须学习的证据语言：

- **Native**：核心原生能力，属于主要产品路径；
- **Pluggable**：通过官方插件、extension 或可替换 provider 提供；
- **External**：主要依赖外部容器、操作系统或第三方工具；
- **Partial**：只覆盖部分场景或接口；
- **Experimental**：实验性、preview 或兼容性仍不稳定；
- **Not central**：存在相关实现，但不是该 harness 的核心能力；
- **Not identified**：在当前证据范围内尚未确认。

正文把标签翻译为自然语言，例如“默认提供”“可通过扩展接入”“仅在实验路径中
出现”或“本次调查未确认”。不得让缩写和标签代替机制解释。

## 8. 单章统一写作模板

### 8.1 内容覆盖与叙事结构

下面的条目是内容覆盖检查表，不是要求逐项建立二级标题。共性机制章应先依据
读者问题把相邻内容合并成少量叙事单元，再检查是否覆盖这些要素：

1. 本章目标与读者问题；
2. 基本概念和术语；
3. 学术背景与原理；
4. 统一抽象、状态机或数据流；
5. 七个 Harness 的实现比较；
6. 两到三个代表性深入案例和必要的特色机制框；
7. 设计选择和权衡；
8. 安全、可靠性和常见失效模式；
9. 工程实践建议；
10. 进一步阅读；
11. 本章小结；
12. 作者内部的证据台账已同步更新。

最终成稿通常组织为约五至八个有实质内容的二级小节，但这不是机械配额。标题只在
论述发生明显转折时出现；如果两个候选小节共同回答同一个读者问题，或者其中一个
不足以形成若干连贯段落，就应合并。不得省略“比较、权衡、代码依据”三个要素；
其中代码依据留在内部台账，正文呈现由它支持的机制和例子。

共性机制章推荐采用以下叙事弧线：

```text
一个具体问题如何出现
  → 最直觉的解决办法及其不足
  → Harness 必须处理的现实约束
  → 统一抽象、状态或数据流
  → 七个系统如何落地，以及少数系统为何偏离
  → 可靠性、安全和成本方面的取舍
  → 回答章首问题，并引出下一章
```

这条弧线可以跨多个小节展开，不应把每个箭头机械变成标题。七个 Harness 也不
默认拆成七个并列小节；优先按设计轴组织比较，用连贯正文和表格说明共同点，再用
代表性实例或特色机制框解释关键差异。

个案章原则上采用：

1. 项目定位和历史背景；
2. 设计目标；
3. 总体架构；
4. 核心控制流；
5. 最有代表性的机制；
6. 与其他 Harness 的关键区别；
7. 安全边界和潜在失效模式；
8. 适合与不适合的场景；
9. 本章小结；
10. 与相关机制章的阅读导航。

### 8.2 篇幅预算与重新估算

篇幅以中文正文字符估算，不含代码、表格、图注和参考文献。初始目标为：

| 章型 | 单章初始目标 | 说明 |
|---|---:|---|
| `00` 叙事式序章 | 4,000–6,000 字 | 以完整故事建立概念，并自然引出阅读入口 |
| `01`–`04` 导论和总览 | 3,000–6,000 字 | 建立概念、比较视角和统一模型 |
| `05`–`22` 普通机制章 | 4,000–7,000 字 | 按设计轴比较，不平均铺开七个项目 |
| `16` Subagent 与 `17` Security | 6,000–10,000 字 | 内容较多，但仍优先合并和下沉证据 |
| `23`–`29` 个案章 | 5,000–8,000 字 | 突出系统组合和代表性控制流 |
| `30`–`32` 综合章 | 4,000–7,000 字 | 只综合前文已有证据 |

全书正文初始预算约为 14–24 万中文字符。该区间用于发现失控章节，不作为机械字数
指标。完成 `05_harness_loop.md`、`08_tool_call_system.md` 和一个个案章的正文与
证据台账后，根据真实的信息密度、图表数量和引用密度统一重新估算，允许调整各章
目标约 25%，并在本计划记录调整理由。

单章接近上限时，依次检查：是否重复解释统一概念，是否可以用表格替代七段平行
描述，是否误把作者证据台账写进正文，以及某个项目特性是否更适合
放回个案章。超过上限不自动扩容；只有新增内容改变核心结论或读者理解时才保留。

### 8.3 发布里程碑和停止规则

报告分三个内容里程碑推进：

1. **叙事样章**：完成 `00`–`05`、`08`、`12` 和一个个案章，用于校准术语、
   代码证据密度、学术框、示例和篇幅。该阶段是内部评审版；
2. **最小可发布核心版**：完成 `00`–`18`、七个个案章 `23`–`29`、综合比较
   `30` 和附录 `90`、`91`、`93`。它形成从参考架构、核心 Runtime 到 Coding 工作流的
   完整主线；未完成章节不进入该版 PDF，也不以完整章节链接展示；
3. **完整版**：补齐 `19`–`22` 的观测、接口、可靠性和配置供应链，以及
   `31`–`32` 的设计原则和研究议程。

源码调查达到以下条件时可以停止继续横向扩展：关键入口、核心状态、主成功路径、
重要错误或取消路径、相关测试和配置条件已经形成闭环；继续扫描只增加同类文件，
不改变机制结论。停止调查不等于隐藏未知，未覆盖路径仍记录在证据台账。写作达到
第 20 节的单章完成标准后即结束本轮扩写，新的有价值线索进入后续版本，而不是让
当前章节无限延长。

## 9. Markdown 排版规范

### 9.1 基本原则

- 只使用可由 GitHub 和 Pandoc 稳定解析的 Markdown；
- 不依赖复杂的 raw HTML 排版；
- 一级标题每个文件只出现一次；
- 正文从二级标题开始组织；
- 标题应表达问题或概念，不使用模糊的“其他”“杂项”；
- 段落保持完整论证，不把所有内容写成 bullet list；
- 列表用于枚举、步骤和比较，不代替正文解释；
- 文件内部使用相对链接；
- 链接文本表达目标内容，不使用大量“点击这里”。

### 9.2 四类语义框

为兼容 GitHub 和未来 PDF，统一使用标准 Markdown blockquote 加粗标题，暂不
使用平台专属的 `[!NOTE]`、MkDocs `!!!` 或 Quarto-only callout。

#### 学术背景

```markdown
> **学术背景｜ReAct 与行动—观察循环**
>
> 用一到三段解释论文、经典模型或理论来源，并说明它和当前工程机制的关系。
```

#### 设计取舍

```markdown
> **设计取舍｜统一接口还是 Provider 原生接口？**
>
> 解释可选方案、收益、代价和适用条件，不给出脱离场景的绝对结论。
```

#### 特色机制

```markdown
> **特色机制｜Gemini CLI 的 Subagent 摘要回传**
>
> 先说明它相对本章统一模型的具体差异，再解释形成该设计的目标或约束，最后
> 说明收益、代价、适用边界，以及对应个案章的链接。
```

#### 安全提示

```markdown
> **安全提示｜工具发现不等于工具授权**
>
> 说明资产、信任边界、攻击前提、影响和缓解方向。
```

未来 Pandoc 模板可根据加粗标签把四类 blockquote 渲染为不同颜色的
`tcolorbox`，不需要改写 Markdown 源稿。

### 9.3 框的使用约束

- 工程机制必须留在正文，不把整章写成提示框集合；
- 一个框只表达一个中心观点；
- 学术背景框用于可跳读的知识补充，不承载理解本节所必需的主论证；
- 特色机制框必须先有共同比较基线，并回答“哪里不同、为什么、代价是什么”；
- 仅有不同命名、配置键或 UI 表现时，不得使用特色机制框；
- 特色机制框应链接到个案章，避免在两个入口重复相同正文；
- 安全提示必须说明攻击前提，避免把理论可能性写成已验证漏洞；
- 连续出现三个以上框时，应重构为正文或独立小节。

## 10. 代码、伪代码与接口规范

正文中的表达优先级是：

1. 架构图、时序图和状态机；
2. 语言无关伪代码；
3. 压缩后的接口或数据结构；
4. 5–15 行关键源码；
5. 极少量、真正帮助解释机制的短代码片段。

约束如下：

- 不复制超过解释所需范围的源码；
- 不为了展示“读过源码”而贴代码；
- 正文不出现源码目录、文件名、行号、`file::symbol` 调用链或 commit 清单；
- 伪代码应表达机制，不模仿某一种实现语言；
- 源码片段必须解释为什么这几行构成关键证据；
- 省略代码时要明确省略了错误处理、并发或平台分支；
- 不把测试代码中的行为自动当成默认产品行为；
- 路径、symbol、commit、测试和反例完整记录在作者内部证据台账；
- 如果短源码不能比伪代码更清楚地解释机制，就使用伪代码、状态机或时序图。

## 11. 图表规范

### 11.1 建议图表

- 全书统一参考架构图；
- 一次 Turn 的纵向时序图；
- Harness loop 状态机；
- Tool call 与审批数据流；
- 七个系统 Tool-call request、response、error 和 approval envelope 的规范化形态对比；
- Context、Memory、Session、Compaction 关系图；
- Plugin、MCP、Skill、Hook 边界图；
- Subagent 委派和权限传播图；
- 安全信任边界图；
- 七个 Harness 能力矩阵；
- 架构谱系和设计空间图。

### 11.2 文件和生成规则

- 图源计划放在 `figures/`；
- Mermaid 源文件使用 `.mmd`；
- GitHub 正文可嵌入 Mermaid 或 SVG；
- PDF 优先嵌入 SVG 或 PDF 矢量图；
- 每张图必须有编号、标题、正文引用和替代文本；
- 图不能只重复相邻段落；
- 宽表应拆分或移入附录，避免 PDF 缩放到不可读。

## 12. 学术内容与引用规范

### 12.1 学术内容的放置

学术背景应嵌入相关工程章节，而不是集中成一个与正文脱节的“相关工作”章。
例如：

- Loop 章联系 ReAct、reasoning/action 和 agent control loop；
- Memory 章联系 working、episodic、semantic 和 procedural memory；
- Compaction 章联系信息瓶颈、摘要失真和长上下文管理；
- Goal 章联系 Plan-and-Execute、任务分解和控制理论；
- Subagent 章联系 actor model、blackboard 和 delegation；
- Security 章联系 least privilege、capability systems 和 confused deputy；
- Session 章联系 event sourcing、checkpoint 和 replay。

学术内容采用“正文主线 + 补充框”的双轨表达：

1. **正文表达**：如果某个学术概念是理解当前工程机制的必要前提，就用朴实语言
   直接写入正文，并在相邻句子就近引用。例如解释 action-observation loop 时，
   不应要求读者先跳入 ReAct 补充框；
2. **学术背景框**：如果内容主要是概念源流、论文脉络、理论扩展、术语辨析或
   可跳读的进一步知识，则使用“学术背景”框，并明确它与当前机制的关系；
3. **独立小节**：如果一个理论需要超过数段才能解释，且会被本章多个工程小节
   反复使用，可设独立小节，但必须以工程问题组织，不能写成论文摘要合集；
4. **本章小结**：只回收会影响架构理解、评价指标或设计决策的学术结论，不单列
   文献清单，也不重复补充框；
5. **不重复原则**：同一知识点不同时在正文和框中完整复述。正文讲必要结论，框
   补来源、边界或扩展；两种位置都可以使用 Pandoc citation。

是否使用框由信息在论证中的作用决定，而不是由它是否“来自论文”决定。全章
不设置机械的框数量或学术字数配额；优先保证工程主线连续、引用准确和可跳读。

### 12.2 学术框的最小内容

每个学术背景框至少回答：

- 该概念或方法解决什么问题；
- 它的核心思想是什么；
- 它与当前 Harness 机制的对应关系是什么；
- 哪些地方只是类比，不能据此声称项目实现了论文方法；
- 原始论文、标准或权威来源在哪里。

### 12.3 引用要求

- 优先引用原始论文、标准、官方协议和官方技术文档；
- 二手博客只用于补充历史语境，不支撑关键技术结论；
- 论文引用最终使用 Pandoc citation 语法，例如 `[@yao2022react]`；
- BibTeX 元数据统一放入 `docs/harness-survey/references.bib`；
- 引文必须支持相邻论述，避免装饰性引用；
- 对快速演进的协议和产品文档记录访问日期和版本；
- 不把论文提出的方法自动等同于项目中的真实实现。

### 12.4 学术文献检索流程

论文和学术原理不能凭作者记忆直接写入正文。每个需要学术解释的主题应先形成
明确的检索问题，例如“工具调用循环如何对应行动—观察模型”或“任务依赖和
actor-style message passing 有何区别”，再组合术语、同义词和相关系统名称进行
检索。

检索优先使用 Google Scholar、Semantic Scholar、DBLP、ACM Digital Library、
IEEE Xplore、USENIX、arXiv 和出版方页面等学术入口。综述论文可以帮助建立术语
和文献谱系，关键方法、定义和历史结论则尽量回到原始论文、正式标准或权威技术
报告。一般 Web 搜索和博客适合发现线索，不单独支撑关键学术结论。

引用一篇文献前，应实际打开并核对与当前论述相关的摘要、方法、定义、实验或限制
部分，不能只根据搜索结果片段、论文标题或其他文章的转述引用。至少核验：

- 标题、作者、年份和发表场所；
- DOI、稳定 URL、正式版本与预印本之间的关系；
- 被引用结论是否确实由该文献提出或验证；
- 论文适用范围和作者明确说明的限制；
- 当前 Harness 机制与论文方法是直接实现、受其启发，还是分析类比。

检索日期、主要检索词、使用的学术入口和核心文献选择理由记录在
`93_references.md` 的研究说明中。核验后的 BibTeX 记录统一保存在
`docs/harness-survey/references.bib`，正文使用 `[@key]` 就近引用。引用键写入
正文前必须能够解析到真实条目；未找到足够文献证据的判断不写成既定学术事实，
也不用看似合理但未经核验的引用键占位。

### 12.5 学术解释的证据边界

论文解释概念来源、已有方法和理论视角，源码说明七个 Harness 实际做了什么，
两类证据各自承担清楚的角色。源码中出现 `plan`、`actor`、`memory` 或 `graph`
等名称，只能说明项目采用了这些术语；是否对应某篇论文的方法，需要进一步比对
机制。相应地，论文证明某种方法有效，也不直接证明某 Harness 已正确、默认或
完整地实现它。正文根据证据选择“实现”“受……启发”“类似于”“可由……解释”
或“尚未建立直接对应”等准确表述。

## 13. 工程证据规范

### 13.1 证据等级

每个重要结论应根据需要标明其证据类型：

- **S：Source**——固定 commit 的真实源码、测试或 schema；
- **D：Documentation**——官方 README、架构文档或协议文档；
- **R：Runtime**——在固定环境中实际运行获得的结果；
- **P：Paper/Standard**——论文、标准或正式协议；
- **I：Inference**——根据多个证据形成的作者分析。

这些等级只用于作者调查、审稿和内部台账。正文不得向读者展示 S/D/R/P/I 标签；
需要限定时，直接写“官方文档描述”“固定版本已实现”“默认启用”“本次运行观察”
或“本文据此分析”。

### 13.2 状态语言

必须区分：

- **Documented**：官方声称或文档描述；
- **Implemented**：源码中存在且接入某条路径；
- **Default**：默认产品路径启用；
- **Verified**：本报告实际运行验证；
- **Inferred**：根据证据推断但未运行确认；
- **Experimental**：实验或 preview 能力。

不得使用“支持”“安全”“隔离”“可恢复”等强词同时代替上述多种状态。

### 13.3 缺失能力的判断

在写“某 harness 没有某能力”前，至少检查：

- 主 README 和官方文档；
- 核心源码和配置 schema；
- tests、examples 和 feature flags；
- plugin/extension 或外部 provider 路径。

证据不足时写“当前分析范围内未识别”，而不是“没有”。

### 13.4 代码先行的调查流程

工程章节先调查代码，再组织叙事。调查不能从一套预先想象的“典型 Harness
架构”出发，只搜索几个相似函数名为既定故事背书。作者应从用户可触发或系统可达
的真实入口开始，沿控制流和数据流向下追踪，并根据主题检查这些环节：

```text
CLI、API、协议或 Tool 入口
  → 配置解析和功能开关
  → 核心状态、消息或任务数据结构
  → 调度、Loop 或 Handler
  → Provider、Tool、Subagent、存储或沙箱边界
  → 成功、错误、取消和恢复路径
  → 测试、示例以及必要的运行验证
```

不同项目不需要具有相同的源码层级；这条链用于寻找实际可达路径。一次关键词命中、
未被调用的 helper、测试 fixture、实验目录或配置 schema 中的字段，都只构成线索。
重要结论应建立入口、关键状态和行为结果之间的联系，并检查错误分支、feature
flag、权限条件和持久化影响。

“通过代码写”是让结论受代码证据约束，不是增加源码粘贴量。完成追踪后，正文用
高层、朴实语言解释观察到的机制；必要时使用状态机、时序图、短伪代码或最短关键
源码片段。详细路径、symbol、commit、测试和证据状态只进入作者内部台账。

### 13.5 结论—证据台账

每个机制章和个案章动笔前，先建立内部结论—证据台账。每条重要工程结论记录：

- 要回答的问题和拟写结论；
- Harness 名称与固定 commit；
- 入口路径、关键文件和 symbol；
- 从入口到行为结果的简短调用链或数据流；
- 相关配置、测试、官方文档和运行证据；
- `Documented`、`Implemented`、`Default`、`Verified` 或 `Inferred` 状态；
- 版本限制、未覆盖路径和当前置信度。

正文使用台账能够支持的表述强度，但不展示路径清单、证据缩写或审稿状态。代码与官方文档不一致时，将差异作为调查结果，
并说明分析采用的固定版本。需要综合多个来源才能建立的架构关系标为作者推断，
必要时降级为进一步研究的问题。

## 14. 安全分析规范

安全分析采用统一框架：

1. 资产：源码、凭据、用户数据、执行环境、外部服务；
2. 主体：用户、模型、主 agent、subagent、tool、plugin、MCP server；
3. 能力：读写文件、运行进程、访问网络、使用凭据、修改 Git；
4. 信任边界：workspace、sandbox、host、provider、extension、client；
5. 攻击入口：prompt、文件、Web、tool output、session、memory、配置；
6. 前提条件：攻击者控制什么，用户批准了什么；
7. 传播路径：输入如何到达敏感能力；
8. 影响：机密性、完整性、可用性、成本和责任归属；
9. 防护：预防、限制、检测、恢复；
10. 证据状态：设计、实现、默认、运行验证或推断。

安全章节不应：

- 把任意 tool use 都称为漏洞；
- 忽略用户显式授权和部署前提；
- 仅凭函数名推断隔离有效；
- 把 sandbox 配置存在写成运行时已隔离；
- 把文档中的安全承诺写成经验证事实；
- 在没有 source-to-sink 路径时夸大严重性。

## 15. 七个 Harness 的比较公平性

- 所有源码结论固定到 `91_version_manifest.md` 中记录的 commit；
- Claude Code、Cursor 等封闭产品只在 `00_index.md` 用作读者认知锚点，不进入
  源码能力矩阵或七系统结论；
- 不用项目年龄、代码行数或 stars 直接代替架构质量；
- 不因项目定位不同而要求所有项目具备完全相同功能；
- 区分 coding-specific、general-purpose 和 runtime/library 定位；
- 区分内建能力、插件能力和外部部署能力；
- 对 developer preview 项目标注稳定性限制；
- 对较旧 pin 明确说明快照日期，不把历史快照当作当前上游状态；
- 运行比较必须记录模型、provider、操作系统、权限和配置；
- 任何性能或安全排名都必须有单独的方法和实验证据。

## 16. 写作风格

- 所有正式标题、正文、导读、示例、图表说明、语义框和章节导航使用中文；
- 项目名、协议名、必要的配置键和命令保留精确英文，通用英文术语首次出现
  时先给出中文解释，再在括号中保留英文原词；
- 英文论文和官方文档的内容用中文概述，只有确有必要时保留短原文引用，并紧跟
  中文解释；
- 不因上游源码和文档使用英文而在报告中出现整段无中文解释的英文论述；
- 使用清楚、克制、可验证的中文；
- 保持高层视野，但用朴实语言解释，不用抽象名词替代因果关系；
- 章首先建立问题场景和核心矛盾，再给出本章将建立的理解框架；
- 开头先说本节解决什么问题，再进入细节，结尾自然过渡到下一个问题；
- 一个段落完成一个中心论点，通常按照“论点—解释—证据或例子—含义”展开；
- 术语首次出现时定义，之后保持名称一致；
- 项目内部术语要映射到通用术语；
- 避免营销语言、“显然”“非常先进”等无证据评价；
- 避免为了学术感使用不必要的复杂句；
- 避免连续使用过长复句；复杂关系宁可分成数个相互衔接的段落；
- 正文默认使用完整段落，不把需要解释因果、条件或转折的论证拆成项目列表；
- 对比时先说明比较轴，再解释差异；
- 小结应回答本章问题，不机械重复目录；
- 对不确定或尚未验证的内容明确标注。

提纲中的长列表只用于防止漏项，不代表最终文风。成稿阶段只有以下内容适合使用
列表：真正并列且语法对称的概念、可执行步骤、检查清单和简短枚举。精确映射或
多系统比较优先使用表格。只要一个条目需要解释“为什么”“但是”或“在什么条件
下”，就应考虑把它改写成段落。不得形成“一个空泛引导句加十几个条目”的常态
版式，也不得让列表承担一节的主要论证。

标题层级同样从简。二级标题表示章节论证的主要转折，三级标题只用于一个二级
小节内部确有多个需要持续展开的子问题；原则上不使用四级标题。诸如“概述”、
“其他实现”和“更多细节”不能单独作为标题。某个项目的特殊实现优先融入比较
叙事或特色机制框，而不是不断新增项目名小节。

### 16.1 示例的使用方式

示例服务于理解和论证，不作为装饰。一个有效示例应明确输入或起始状态，展示
关键决策或状态变化，再说明结果及其边界。正文通常先解释抽象机制，再用示例让
机制落地，最后回到真实 Harness 的设计差异；也可以在章首先提出问题场景，随后
逐步抽象，但不能只讲故事而不总结机制。

全书采用一个可重复进入的主教学案例：用户要求 Agent 在一个已有仓库中定位并
修复配置解析错误，运行相关测试，解释修改，并允许任务在中途压缩、委派或恢复。
不同章节只取其中与本章有关的一段，例如 Tool 章关注读取、修改和测试，Session
章关注中断与恢复，Subagent 章关注任务拆分和结果汇聚。安全章节可使用一个配套
反例：仓库文档或工具输出夹带读取凭据、扩大权限或向外发送数据的指令。

教学案例必须明确标为示例，不得冒充七个项目的运行记录。必要的伪代码、短对话、
状态快照和时序图应尽量围绕同一案例展开，避免每节重新发明无关场景。示例结束后
说明它对应哪类真实机制、哪些结论可以泛化；具体源码入口只保存在内部台账。

### 16.2 学术性与可读性的平衡

学术写作在本报告中体现为论点清楚、概念边界稳定、证据可追溯、引用准确、限制
条件明确，而不是句式复杂。每个重要判断都应让读者看清“我们观察到了什么、依据
是什么、结论适用于哪里”。教科书式写作则要求知识按依赖关系展开：先给读者理解
下一步所需的概念，再引入新的抽象，并通过回顾和过渡把章节连接起来。

高层介绍不能停留在口号。每个高层概念最终至少落到一种具体表达：一次状态变化、
一条数据流、一个接口边界、一个失败案例或一个真实系统差异。反过来，源码细节也
不能未经抽象直接进入正文；作者先在内部台账中完成源码核验，再用机制、数据流、
短伪代码或例子向读者解释结论。

### 16.3 克制使用限定和否定

这是一份源码驱动的工程教科书式报告，不采用论文答辩或审稿回复式语气。正文默认
正面回答“这个机制做了什么、如何工作、产生什么效果”，随后给出必要例子。范围、
证据等级与审稿流程由作者计划统一管理，各章不再反复声明“本文没有做什么”
“这不代表什么”或“我们不讨论什么”。

限定语只在它会改变读者理解时出现，例如固定版本与当前上游不同、能力只存在于
实验路径、文档和源码不一致、安全结论依赖特定前提，或者当前证据只能支持
`Implemented` 而不能支持 `Default`。这类限定通常紧跟相关结论，用一两句话说清，
不扩写成防御性段落。安全分析仍然保留必要的攻击前提和证据状态，但以说明实际
边界为目的，不逐段罗列尚未发生的情况。

推荐写法是：“在固定版本中，OpenCode 的 task tool 创建带有 `parentID` 的子
Session，并把完成结果送回父会话；后台路径仍标记为实验性。”这句话同时说明了
行为、证据范围和一个有实质影响的限制。应避免围绕同一事实连续写“这不意味着
它是 DAG”“这不说明所有入口都启用”“本文也没有验证所有并发情况”等多重否定；
相关未知项集中记录在内部证据台账；只有确实改变读者理解时才进入正文。

“当前分析范围内未识别”主要用于能力矩阵和确有必要的对照结论，不应成为每个
项目段落的固定收尾。报告先写已经由代码确认的机制；缺失或未知只在影响比较结论
时简洁说明。

## 17. 交叉链接和导航规范

- `00_index.md` 列出所有正文和附录；
- 每章开头给出“前置阅读”和“本章关联”；
- 每章结尾给出“下一步阅读”；
- 横向总览链接到机制章，不链接到具体源码；
- 纵向总览链接到生命周期对应的机制章和个案小节；
- 个案章使用机制章的固定标题作为反向链接目标；
- 附录不打断主线，只承载术语、版本来源和面向读者的引用；内部源码证据不进入附录；
- 文件重命名时必须更新所有相对链接；
- 不使用绝对本地路径作为最终报告链接。

## 18. Markdown 到 PDF 的路线

### 18.1 当前阶段

- 所有正文保持 `.md`；
- 确保 GitHub 可直接阅读；
- 使用普通 blockquote 表达语义框；
- 引用键和图表 ID 从一开始保持稳定；
- 暂不引入 LaTeX 专属命令。

### 18.2 汇编阶段

计划使用 Pandoc：

- 按编号顺序汇编章节；
- 使用 `--citeproc` 处理 `references.bib`；
- 使用 metadata 文件设置标题、作者、语言和目录；
- 使用 Lua filter 把四类语义框转换为 HTML/PDF callout；
- 使用自定义 LaTeX template 和 `tcolorbox` 生成教材式 PDF；
- 为 HTML 和 PDF 分别提供样式；
- 自动生成目录、图表编号、交叉引用和参考文献。

### 18.3 为什么不立即使用 LaTeX

- Markdown 更适合 GitHub 阅读、逐章 review 和 Git diff；
- 当前主要工作是建立内容和证据，而不是版式微调；
- Pandoc 能保留迁移到 LaTeX 的路径；
- 只有在形成正式论文时，才需要按具体 venue 模板迁移；
- 现在直接使用 LaTeX 会增加编辑成本，并弱化仓库内阅读体验。

## 19. 编写阶段计划

### 阶段 0：Workspace 与 Submodule 预检

当前 `tripodfish` worktree 的七个 submodule 只有 gitlink，`git submodule status`
均带前导 `-`。进入源码调查前，在本 worktree 执行：

```bash
git submodule sync --recursive
git submodule update --init --recursive --depth 1
```

随后逐个验证：

- `git submodule status` 不再出现未初始化标记；
- checkout `HEAD` 与父仓库记录的 mode-`160000` gitlink 完全一致；
- origin 与 `.gitmodules` 一致；
- shallow 状态符合仓库约定；
- 七个目录中的计划证据入口可读。

源码调查优先使用当前 worktree 的 checkout，避免计划、证据路径和分支状态分离。
如果临时借用其他 worktree 的已初始化 submodule，只能在逐个确认 gitlink SHA 完全
一致后作为只读来源，并在证据台账记录实际 source root。

`91_version_manifest.md` 如实记录各项目的 commit、上游默认分支和所选 ref。
分支或 tag 名称用于定位快照；即使上游默认分支名为 `dev`，也不单独转换为稳定性
或证据权重。

### 阶段 1：建立章节骨架

- 创建本计划列出的所有 `.md` 文件；
- 为 `00_index.md` 建立完整故事弧线、就地机制链接和末尾目录；
- 写入一级标题、章节目标、合并后的叙事型二级标题、计划图表和证据要求；
- 标明计划放入正文的必要学术原理，以及候选的学术背景、特色机制和安全提示框；
- 把第 6 节的细项保留为覆盖检查表，不把每个细项直接转换成 subsection；
- 建立 `00_index.md` 的完整链接；
- 确认没有空文件和孤立章节。

### 阶段 2：建立版本和证据清单

- 固定七个 submodule commit；
- 记录许可证、主要语言、默认分支和分析日期；
- 为每章建立结论—证据台账、源码入口、调用链和官方文档入口；
- 标记需要运行验证的命题；
- 为各主题形成学术检索问题、检索词和候选原始文献；
- 建立并校验 `references.bib`，候选文献经过原文核验后再进入正文。
- 完成三个代表性章节的证据台账后，复核第 8.2 节篇幅预算和整体工期。

### 阶段 3：编写基础和统一模型

- 完成 Harness 导论；
- 完成横向能力地图；
- 完成纵向生命周期；
- 完成统一参考架构；
- 冻结主要术语。

### 阶段 4：编写共性机制章

每章开始写正文前，先完成相关七系统的源码追踪和初始学术检索。根据代码台账
确定共性、差异和未知，再组织叙事；证据决定结论强度，成稿结构负责把这些结论
讲清楚。

推荐顺序：

1. Harness loop；
2. Model/provider；
3. Context/instructions；
4. Tool call；
5. Plugin/MCP/extensions；
6. Session/resume；
7. Memory；
8. Compaction；
9. Token efficiency/cost；
10. Skills/hooks；
11. Goal/planning；
12. Subagent/orchestration；
13. Security；
14. Workspace/Git；
15. Observability；
16. Interfaces；
17. Reliability；
18. Configuration/supply chain。

### 阶段 5：编写七个个案

- 先在内部台账建立统一源码地图；
- 沿代表性入口追踪端到端控制流、状态流、错误路径和测试；
- 每章只突出该 harness 的代表性设计；
- 使用交叉链接替代通用概念重复；
- 为每章建立至少一张总体架构图；
- 在内部台账标注安全结论的证据状态，正文用自然语言说明必要前提。

### 阶段 6：综合、学术和安全提升

- 汇总比较矩阵；
- 提炼设计原则；
- 复核正文已经使用的论文、标准、引用键和文献元数据；
- 对检索仍有空白的论述补充检索，再决定保留、改写或删除相应判断；
- 审查安全模型和攻击前提；
- 编写开放问题和研究议程。

### 阶段 7：编辑和发布

- 统一术语、语气、标题和图表；
- 检查相对链接和引用键；
- 使用 Pandoc citeproc 验证所有正文引用键能够解析；
- 执行 Markdown lint；
- 生成 HTML/PDF；
- 检查目录、分页、表格和字体；
- 记录报告版本和生成环境。

## 20. 单章完成标准

一章只有在满足以下条件后才能标记为“完整”：

- 本章问题和范围明确；
- 通用机制解释独立可读；
- 章节形成连续叙事，标题数量与论述转折相称，没有把覆盖清单机械变成目录；
- 正文以段落为主，列表、表格和语义框没有替代主要论证；
- 至少比较与该主题真正相关的 harness；
- 未适用的项目说明原因，而非强行填充；
- 关键工程结论可追溯到固定版本证据；
- 关键机制已经从真实入口追踪到状态和行为结果，不以关键词命中代替调用链；
- 正文陈述强度不超过结论—证据台账记录的证据状态；
- 学术引用与当前机制直接相关；
- 学术性实质判断经过实际文献检索和原文核验，并有可解析的就近引用；
- `references.bib` 中的作者、标题、年份、版本和稳定标识已经核验；
- 理解机制所必需的学术原理位于正文，可跳读的补充知识才使用学术背景框；
- 至少讨论一种重要设计取舍；
- 如使用特色机制框，已建立共同比较基线，并解释差异、动机、代价和适用边界；
- 安全结论在正文说明攻击前提，在内部台账记录证据状态；
- 没有不必要的大段源码；
- 必要示例展示了输入、关键变化、结果和适用边界，并与真实证据明确区分；
- 图表在正文中被解释；
- 小结回答了章首问题；
- 正文以已确认机制为主，没有反复使用非目标声明和防御性否定；
- 所有相对链接有效；
- 没有未解释的占位符或模糊结论。

## 21. 全书质量检查

### 21.1 结构检查

- 横向地图中的每项能力都有详细章节；
- 纵向生命周期中的每个阶段都有落点；
- `00_index.md` 同时提供内容视角和四类读者路线，初学者从读者导论直接进入主线；
- `00_index.md` 即使不点击链接也能独立解释 Harness 的问题、工作定义和全书主张；
- `00` 的故事、`03` 的生命周期和 `04` 的参考架构职责清楚，没有重复成段内容；
- `04_reference_architecture.md` 已给出 Session 等核心状态对象的最小定义，
  `10`、`12` 和 `13` 章使用同一组定义；
- 每个机制章至少由一个个案章反向引用；
- 七个 harness 都有独立且不重复的中心问题；
- 综合结论能追溯到前文证据。

### 21.2 内容检查

- “文档声明、源码实现、默认启用、运行验证、作者推断”没有混写；
- 没有先写通用架构故事、再用零散函数名反向拼接证据；
- 抽查的重要工程结论能够从内部台账回到固定 commit 的入口、调用链和测试；
- 没有把功能存在等同于安全保证；
- 没有把实验分支或测试 helper 当作产品路径；
- 没有用 stars、语言或代码量替代机制分析；
- 没有大段复制 README 或源码；
- 学术背景帮助解释工程问题；
- 学术论述均能定位到经过检索和核验的真实文献，没有凭印象生成的论文或引用键；
- 特色机制框没有替代七系统比较，也没有与个案章重复成段内容；
- 章节之间有知识依赖和过渡，不是彼此孤立的专题条目；
- 主教学案例在不同章节中保持角色、目标和基本事实一致；
- 关键限定集中、简洁并且确实影响解释，正文没有形成自我辩护式语气；
- Tool-call 形态对比能够从规范化 envelope 回到七个系统的真实字段；
- Telemetry、crash report、opt-out 和敏感数据外传在 `17`、`19`、`22` 章分工明确；
- 正文保持 Coding Agent 边界，没有扩展成通用多模态 Agent 调研；

### 21.3 编辑检查

- 中文术语一致；
- 英文缩写首次出现有解释；
- 标题层级有效；
- 没有可以合并的短小 subsection，也没有项目名小节的机械七连排；
- 图、表、公式和引用可定位；
- 四类 Callout 的语义和标题格式使用一致；
- 正文没有源码目录、文件名、行号、`file::symbol` 链、证据缩写或审稿状态；
- Index 中的章节链接由相邻问题自然引出，正文没有形成链接墙；
- 单章和全书篇幅处于当前预算内，超出部分已完成合并、下沉或保留理由审查；
- GitHub 阅读和 PDF 阅读都不依赖隐藏内容；
- 链接、引用键和文件名无误。

## 22. 后续变更规则

- 新增 harness 时，先更新范围、版本清单和选择理由；
- 新增共性章节前，确认它无法合理归入现有机制章；
- 不为追求目录对称而创建内容稀薄的章节；
- 上游版本更新时单独记录，不静默覆盖原有分析快照；
- 架构结论变化时同步更新横向地图、纵向生命周期、个案和综合章；
- 对已发布 PDF 使用版本号，不让内容在同一版本下漂移；
- 本文件如发生结构性修改，应在文首更新状态和理由。

## 23. 下一步

本文件经复核后，下一步执行“阶段 1：建立章节骨架”：

1. 创建第 6 节列出的全部编号 Markdown 文件；
2. 为每个文件写入正式一级标题；
3. 写入章节目标、建议二级标题、计划图表和证据要求；
4. 建立 `00_index.md` 的叙事主线、就地机制链接、三种内容视角、四类读者路线和
   完整目录；
5. 验证文件顺序、标题一致性和链接完整性；
6. 保持章节为明确的“提纲状态”，不伪装成已经完成的正文。
