# 参考文献阅读入口

## 如何使用本章

本章把 `references.bib` 中已经核验的 86 条文献组织成面向读者的注释式入口，而不是把 BibTeX 清单换一种排版重复一遍。每条说明只回答三个问题：文献主要讲什么，它支撑正文哪一章的哪个论断，以及它与[智能体脚手架（Agent Harness）的工作定义](01_introducing_agent_harness.md#从一次修复任务看-harness)是什么关系。这里使用四种关系类型：**概念来源**表示正文直接借用其问题定义或分析框架，**分析类比**表示它帮助解释工程机制但不证明七个 Harness 实现了该方法，**风险证据**表示它展示了攻击、失效或评测偏差，**协议契约**表示正文依赖某个有版本或访问日期的正式接口与规范。

如果从全书的[“一句话请求先要落到正确的工作区”教学案例](00_index.md#一句话请求先要落到正确的工作区)进入，可以先按当前问题选择下面一个主题，再沿每条说明中的章节链接回正文。读者不需要先记住全部论文名称，也不应把同一组里的文献看成排名。论文、标准和工程文档解释机制来源与边界，七个 Harness 的实现事实仍由各正文章的固定版本源码证据支撑。

这些条目的检索与核验集中在 2026 年 9 月 1 日至 2 日完成，主要入口包括 arXiv、ACL Anthology、ACM Digital Library、IEEE Xplore、USENIX、PMLR、Crossref、DBLP，以及 MCP、OpenAI、Anthropic、Git、Temporal、OpenTelemetry、SLSA 和 AWS 的官方文档。正文引用以 `references.bib` 的核验记录为准；预印本没有独立核验到会议 DOI 或页码时，本章不补写推测性元数据，持续更新的规范则以条目记录的版本或访问日期为边界。

## Agent Loop 与 Tool Use

智能体循环（Agent Loop）解释一次模型生成怎样经过行动、执行与环境观察继续推进，[第 05 章给出了循环不变量](05_harness_loop.md#turn状态与循环不变量)；工具使用（Tool Use）则把行动表示、能力发现、参数校验与结果回写连成[可执行行动空间](08_tool_call_system.md#工具如何成为模型的行动空间)。本组从“为什么需要循环”读到“工具很多、接口会变、动作可以怎样表达”，适合先建立控制流直觉。

**ReAct**说明推理与行动交错后，外部观察能够更新后续决定，支撑第 05 章“单次响应不等于持续 Agent”的核心论断，关系类型为**概念来源、分析类比** [@yao2023react]。

**Chain-of-Thought Prompting**说明中间推理步骤可以改善复杂推理，却没有引入环境读取、执行和取消语义，支撑第 05 章区分单次推理与闭环任务，关系类型为**概念来源** [@wei2022chain]。

**Reflexion**把失败后的语言反思写入情景记忆供后续试次使用，支撑第 05 章“语言反馈可以修正下一轮但不能恢复外部现场”的论断，关系类型为**分析类比** [@shinn2023reflexion]。

**CoALA**把语言 Agent 组织为含工作记忆、内部行动和外部行动的持续决策过程，支撑第 05 章把 Loop 解释为大于一次模型调用的运行周期，关系类型为**分析类比** [@sumers2024coala]。

**Toolformer**把工具使用拆成是否调用、选择工具、填写参数和吸收结果，支撑第 08 章“工具改变行动空间而不只是增加提示词”的论断，关系类型为**概念来源** [@schick2023toolformer]。

**Gorilla**展示模型会编造 API 用法而检索最新文档可以缓解接口漂移，支撑第 08 章把 Schema 与工具文档视为可更新系统事实，关系类型为**风险证据** [@patil2024gorilla]。

**API-Bank**以可运行 API 对话任务分开评估规划、工具检索、参数调用和结果解释，支撑第 08 章“工具能力需要执行式评测而非只看文本”的论断，关系类型为**概念来源** [@li2023apibank]。

**ToolLLM**面对大规模 API 集合先检索相关能力再调用，支撑第 08 章“拥有许多工具不等于把全部 Schema 塞进每轮 Context”的论断，关系类型为**分析类比** [@qin2023toolllm]。

**CodeAct**用可执行代码统一表达复合行动，支撑第 08 章比较结构化 Tool Call 与代码行动的组合力、校验成本和隔离责任，关系类型为**分析类比** [@wang2024codeact]。

## Planning 与 Multi-agent

规划（Planning）在本书中是从当前状态走向目标的可修订路线，[第 15 章将 Goal、Plan、Task 与 Todo 分层](15_goals_planning_and_todos.md#goalplantask-与-todo)；多智能体（Multi-agent）则关注多个执行者之间的角色、通信、依赖、等待和责任，[第 16 章从委派动机开始建立这些边界](16_subagents_and_orchestration.md#为什么委派任务)。本组的阅读重点不是寻找一个万能编排框架，而是分清计划文本、执行状态、对话拓扑和任务图分别解决什么问题。

**HuggingGPT**让语言模型规划任务、选择外部专家模型并汇聚结果，支撑第 09 章“扩展能力可以来自可发现的外部专家”以及第 16 章的角色分工类比，关系类型为**分析类比** [@shen2023hugginggpt]。

**ReWOO**把推理蓝图与外部观察解耦以减少交错调用的重复上下文，支撑第 15 章比较逐步反应与先计划后执行的适用前提，关系类型为**概念来源、分析类比** [@xu2023rewoo]。

**Plan-and-Solve**先生成分解计划再逐步求解，支撑第 15 章“显式规划可以减少漏步但仍不等于持久 Todo Runtime”的论断，关系类型为**概念来源、分析类比** [@wang2023planandsolve]。

**LLM Agent 规划综述**把规划工作区分为任务分解、计划选择、外部模块、反思与记忆，支撑第 15 章拒绝用一个“会规划”标签覆盖多种机制，关系类型为**概念来源、分析类比** [@huang2024planningagentsurvey]。

**Plan-and-Act**把高层 Planner 与把计划翻译为环境动作的 Executor 分开，支撑第 15 章“长程目标需要规划、执行与环境变化后的重规划闭环”，关系类型为**概念来源、分析类比** [@erdogan2025planandact]。

**AutoGen**以可对话 Agent 组合模型、人类和工具，支撑第 16 章区分通信拓扑与具有依赖语义的 Task DAG，关系类型为**概念来源、分析类比** [@wu2023autogen]。

**MetaGPT**用标准操作流程、角色和中间产物校验约束软件工程协作，支撑第 16 章“多 Agent 不能只靠自由对话维持阶段和责任”，关系类型为**概念来源、分析类比** [@hong2024metagpt]。

**MAST**把多 Agent 失败归入系统设计、Agent 间错位与任务验证等类别，支撑第 16 章“子 Agent 返回文本不等于 Join 后结果已验证”的风险判断，关系类型为**风险证据、分析类比** [@cemri2025mast]。

**LLM 多 Agent 综述**把角色画像、通信方式、能力增长和评测环境分开讨论，支撑第 16 章把通信视为独立于父子谱系与任务依赖的设计轴，关系类型为**概念来源、分析类比** [@guo2024llmmultiagentsurvey]。

**新兴 AI Agent 架构综述**从推理、规划、工具调用以及单 Agent 和多 Agent 架构梳理常见设计，支撑[第 32 章关于 Harness 形式化模型的判断](32_open_problems_and_research_agenda.md#harness-的形式化模型)，即阶段分类仍不足以构成可检验形式模型，关系类型为**分析类比** [@masterman2024agentarchitectures]。

**AI Agents 与 Agentic AI 分类研究**区分模块化单任务 Agent 与多 Agent 协作、动态分解和持久记忆组成的系统，支撑第 32 章把协调失败、记忆持续性和责任归属列为独立研究问题，关系类型为**概念来源、分析类比** [@sapkota2025agenticai]。

**Internet of Agents**以异构 Agent 集成、动态组队和对话流控制暴露硬编码通信管道的局限，支撑第 32 章“Agent 间互操作不止是共享工具 Schema”的问题陈述，关系类型为**概念来源、分析类比** [@chen2024internetofagents]。

## Memory 与 Context

可检索记忆（Memory）保存跨任务仍可能有用的经验，[第 10 章先把它与 Session 状态分开](10_memory.md#memory-与-session-状态的区别)；本轮上下文（Context）是一次模型调用实际可见的输入投影，[第 07 章说明它不只是 Prompt](07_context_and_instruction_system.md#context-为什么不只是-prompt)。本组沿“取回什么、怎样管理、窗口不足时怎样缩短或外置、如何维持恢复与成本边界”展开，因此同时对应第 07、10、11、12、13 和 14 章。

**Retrieval-Augmented Generation**把参数记忆与外部检索材料结合，支撑第 07 章“系统拥有的信息可以多于模型此刻看见的信息”，关系类型为**概念来源、分析类比** [@lewis2020rag]。

**Lost in the Middle**展示长输入中相关信息的位置会影响模型利用质量，支撑第 07 与第 13 章把排序、选择和位置偏差视为 Context 管理问题，关系类型为**风险证据、分析类比** [@liu2024lostinthemiddle]。

**MemGPT**用主上下文与外部存储之间的显式换入换出扩展可见信息，支撑第 10 与第 13 章区分 Memory、窗口外置和 Session 全量保存，关系类型为**分析类比** [@packer2023memgpt]。

**Generative Agents**把经历写入 memory stream，再按相关性、近因和重要性检索并形成反思，支撑第 10 章“长期记忆包含记录、取回、抽象和再写入的生命周期”，关系类型为**概念来源、分析类比** [@park2023generativeagents]。

**LLM Agent 记忆机制综述**以来源、存储形式以及写入、管理、读取三轴组织已有方法，支撑第 10 章不把“是否有向量库”当成 Memory 的唯一比较标准，关系类型为**概念来源** [@zhang2024memorysurvey]。

**MemoryBank**用分层摘要、用户画像和随时间衰减的更新策略管理长期对话记忆，支撑第 10 章比较永不删除与显式遗忘的设计取舍，关系类型为**分析类比** [@zhong2024memorybank]。

**Voyager**把经过环境反馈和自验证的可执行程序存入可检索技能库，支撑第 10 与第 11 章“过程性记忆可以外置为技能而不只是自然语言摘要”，关系类型为**分析类比** [@wang2024voyager]。

**Prompt Pattern Catalog**把可复用提示描述为带意图、结构和后果的模式，支撑第 11 章区分一次性对话与可参数化 Prompt Template，关系类型为**概念来源** [@white2023promptpatterns]。

**The Prompt Report**系统整理 Prompt、模板、链和提示技术的术语边界，支撑第 11 章“项目 Prompt 文件与 Command 参数槽属于可复用模板实例化而非同一种运行时”，关系类型为**概念来源** [@schulhoff2024promptreport]。

**Event Sourcing**以有序事件作为状态变化记录并支持重建、时间查询和分支，支撑第 12 与第 19 章区分权威事件历史、派生快照和外部副作用，关系类型为**概念来源** [@fowler2005eventsourcing]。

**Durable Functions**用记录与重放为有状态 Serverless 工作流提供持久语义，支撑第 12 与第 21 章“崩溃恢复可以依赖事件历史而不必保存语言运行时进程”，关系类型为**分析类比** [@burckhardt2021durablefunctions]。

**Faithfulness and Factuality in Abstractive Summarization**区分摘要中的内在与外在幻觉，支撑第 13 章“模型压缩会改写或增添原历史无法支持的内容”，关系类型为**风险证据** [@maynez2020faithfulness]。

**LLMLingua**用分层预算和 token 级选择压缩 Prompt，支撑第 13 与第 14 章把提示压缩视为有损缩短而非普通截断，关系类型为**分析类比** [@jiang2023llmlingua]。

**LongLLMLingua**结合问题感知压缩、文档重排和动态压缩率处理长上下文，支撑第 13 章“压缩还会改变关键信息密度与位置”，关系类型为**分析类比** [@jiang2024longllmlingua]。

**Prompt Cache**研究跨请求复用稳定 Prompt 模块的注意力状态，支撑第 14 章“稳定前缀影响首 Token 延迟，但不等于减少输出 Token”，关系类型为**分析类比** [@gim2024promptcache]。

**OpenAI Prompt Caching**规定当前 API 中前缀匹配、缓存读写与 `cached_tokens` 等行为，支撑第 14 章“Token 账本要区分缓存写入、命中和 Compaction 破坏前缀”，关系类型为**协议契约** [@openai2026promptcaching]。

**FrugalGPT**用提示适配、模型近似和级联在费用与质量之间分配请求，支撑第 14 章“弱模型路由是任务分层而不是随机降级”，关系类型为**概念来源、分析类比** [@chen2024frugalgpt]。

**Agentic RAG 综述**把反思、规划、工具使用和多 Agent 协作引入动态检索流程，并把评测、协调、记忆、效率与治理列为开放挑战，支撑第 32 章连接 Memory 污染、Token 质量边界和多 Agent 责任，关系类型为**概念来源、分析类比** [@singh2025agenticrag]。

**A-MEM**用动态索引、链接和回溯更新组织可演化记忆，支撑第 32 章“长期记忆能够改写旧关系后，污染、陈旧链接与审计不再是静态检索问题”，关系类型为**分析类比、风险证据** [@xu2025amem]。

## Security 与 Capability

安全（Security）在这里指保护代码、凭据、进程、网络、状态和责任边界，[第 17 章从受保护资产开始展开](17_security_permissions_and_sandboxing.md#harness-保护什么)；能力（Capability）是主体可行使的有界权力，其定义与信任边界见[主体与能力的统一模型](17_security_permissions_and_sandboxing.md#主体能力与信任边界)。本组也收入人机控制、评测偏差、可靠性与供应链资料，因为它们共同回答“行动如何被授权、限制、观察、恢复和归责”。

**自动化类型与水平模型**把信息获取、分析、决策和行动实施分成可独立分配的人机阶段，支撑第 05 与第 20 章“人在回路不是全自动与全手动之间的单一开关”，关系类型为**分析类比** [@parasuraman2000automation]。

**回滚恢复协议综述**指出内部检查点不能自然撤销已经发往外部系统的输出，支撑第 05、12、19 与 21 章对取消、Resume、Replay 和副作用恢复的边界判断，关系类型为**分析类比** [@elnozahy2002rollback]。

**计算机系统保护原则**提出最小权限、失败安全默认与完全仲裁等原则，支撑第 08、17 与 22 章把能力注册、逐调用授权和执行环境限制分层，关系类型为**概念来源** [@saltzer1975protection]。

**ToolEmu**用语言模型仿真工具执行并独立评估 Agent 风险，支撑第 05、08 与 19 章“任务成功率不能代替工具风险检查”，关系类型为**风险证据、分析类比** [@ruan2024toolemu]。

**Instruction Hierarchy**讨论高特权与低特权指令冲突及相应训练方法，支撑第 07 与第 17 章“仓库或工具文本不应与系统和用户意图平权”，关系类型为**概念来源** [@wallace2024instructionhierarchy]。

**Indirect Prompt Injection**说明恶意指令可以藏在被检索的网页、邮件、文件或工具结果中，支撑第 08、09、17 与 22 章从不可信数据追踪到能力执行的攻击路径，关系类型为**风险证据** [@greshake2023indirectpromptinjection]。

**InjecAgent**以工具集成 Agent 的间接注入用例展示受控 Observation 如何改变后续 Tool Call，支撑第 08 与第 17 章“结果回流也是行动边界”，关系类型为**风险证据** [@zhan2024injecagent]。

**AgentDojo**在动态工具环境中同时评估任务效用与提示注入防御，支撑第 17 与第 19 章“安全控制不能只看攻击成功率或任务成功率其中一项”，关系类型为**风险证据** [@debenedetti2024agentdojo]。

**AgentPoison**展示少量恶意记忆或知识库条目可经检索影响后续行动，支撑第 10 与第 17 章“Memory 写入和读取都必须仲裁”，关系类型为**风险证据** [@chen2024agentpoison]。

**LLM-as-a-Judge 研究**分析位置、冗长和自我增强等评分偏差，支撑第 19 章“模型评委不能替代可执行测试和原始评分依据”，关系类型为**风险证据、概念来源** [@zheng2023llmjudge]。

**Mixed-Initiative User Interfaces**按动作价值、代价和意图不确定性分配系统与用户的主动权，支撑第 20 章设计审批和自动继续边界，关系类型为**概念来源** [@horvitz1999mixedinitiative]。

**Guidelines for Human-AI Interaction**把及时反馈、范围说明、可纠正性和能力变化通知分到不同交互阶段，支撑第 20 章“审批不能退化为脱离上下文的 Yes/No”，关系类型为**概念来源、分析类比** [@amershi2019guidelines]。

**Predicting Human Interruptibility with Sensors**把“何时适合打断用户”建模为可变化状态，支撑第 20 章区分注意力中断与进程取消，关系类型为**分析类比** [@fogarty2005interruptibility]。

**Direct Manipulation for Comprehensible, Predictable and Controllable User Interfaces**强调对象与动作可见、操作增量且效果及时可见，支撑第 20 章解释 diff、计划预览和取消为何是控制面而不只是界面装饰，关系类型为**概念来源** [@shneiderman1997directmanipulation]。

**Dependable and Secure Computing Taxonomy**区分 fault、error 与 failure，并组织预防、容错、移除和预测手段，支撑第 21 章建立分层 Failure Model，关系类型为**概念来源** [@avizienis2004dependability]。

**The Tail at Scale**说明扇出系统中的尾延迟与对冲请求控制，支撑第 21 章区分 hedged request、普通重试以及有副作用工具不适用的边界，关系类型为**分析类比** [@dean2013tail]。

**Sagas**把长事务拆为子事务并以补偿动作处理已提交步骤，支撑第 21 章“Undo 是资源特定的语义补偿而非世界状态回滚”，关系类型为**概念来源** [@garciamolina1987sagas]。

**Idempotence Is Not a Medical Condition**说明至少一次投递需要自然幂等或请求身份与去重记录，支撑第 21 章“Tool 超时后的重试可能重复副作用”，关系类型为**概念来源** [@helland2012idempotence]。

**Exponential Backoff And Jitter**说明无抖动退避会让失败客户端同步重试，支撑第 21 章“重试需要封顶退避、抖动和总预算共同约束”，关系类型为**协议契约、分析类比** [@brooker2015backoff]。

**SLSA v1.2**把软件供应链威胁分到 source、build 与 dependency 等阶段，并界定 provenance 只能证明构建事实，支撑第 22 章“有来源证明不等于源码可信或无漏洞”，关系类型为**协议契约** [@slsa2026specification]。

**Sigstore**用 OIDC 身份、短期证书和透明日志把身份声明绑定到制品摘要，支撑第 22 章区分发布身份、制品完整性和代码安全，关系类型为**概念来源、协议契约** [@newman2022sigstore]。

**npm 生态安全研究**展示传递依赖和高影响维护者会扩大隐式信任集，支撑第 22 章“扩展来源不能只检查顶层仓库 URL”，关系类型为**风险证据** [@zimmermann2019npm]。

**解释型语言包管理器供应链测量**分析 typosquatting、名字空间混淆以及安装和导入时执行，支撑第 22 章“依赖解析顺序和安装 Hook 本身就是攻击面”，关系类型为**风险证据** [@duan2021packagemanagers]。

**CaMeL**在模型之外分离可信控制流、不可信数据流与工具侧能力检查，支撑第 17 章“提示注入缓解可以依赖结构性隔离而不只是提示过滤”，关系类型为**概念来源、风险证据** [@debenedetti2025camel]。

**Progent**把工具和参数权限写成可确定检查、可单调收窄的规则，支撑第 17 章“权限扩张应独立批准而收窄可以自动执行”，关系类型为**概念来源、分析类比** [@shi2025progent]。

**AgentSpec**用触发器、谓词与运行时强制机制约束 Agent 执行，支撑第 17 章“权限与操作系统沙箱之间还可以存在独立的规则执行层”，关系类型为**概念来源、分析类比** [@wang2025agentspec]。

**Agent Security Bench**把攻击面覆盖到提示、工具和记忆等阶段，支撑第 17 章“Agent 安全评测不能只测最终任务成功率”，关系类型为**风险证据** [@zhang2025asb]。

**IsolateGPT**从第三方应用身份、数据可见性和相互调用出发设计执行隔离，支撑第 17 章“沙箱需要约束谁能以何种身份触达资源，而不只是拦一条命令”，关系类型为**概念来源、分析类比** [@wu2025isolategpt]。

## Coding Agent 与软件 Agent

编码智能体（Coding Agent）以代码库、编辑器、命令、测试和 Git 作为主要工作环境，[第 18 章把它们组织成工程闭环](18_code_editing_git_and_workspace.md#coding-harness-的工程闭环)；软件智能体（Software Agent）在本组中是更宽的研究对象，包括仓库修复平台、固定流水线和结构化程序分析方法。它们提供任务与评测坐标，但不替代本书对七个 Harness 固定版本的实现调查。

**SWE-agent**说明智能体—计算机接口的参数、工作目录、错误、截断和调用配对会影响软件工程任务表现，支撑第 01、07、08、18 与 19 章“评测对象是模型与 Harness 的组合”，关系类型为**概念来源、分析类比** [@yang2024sweagent]。

**RepoCoder**以相似度检索和迭代生成处理跨文件仓库补全，支撑第 07 与第 18 章“仓库信息需要迭代定位而不能一次全部塞入窗口”，关系类型为**分析类比** [@zhang2023repocoder]。

**SWE-bench**用真实仓库 Issue、代码快照、补丁和测试定义执行式修复任务，支撑第 18 与第 19 章“测试是可操作成功信号但不自动证明补丁完整可维护”，关系类型为**概念来源、风险证据** [@jimenez2024swebench]。

**OpenHands**把写代码、命令行、浏览器、沙箱和评测接入同一开放平台，支撑第 18 章“执行环境本身属于 Coding Agent 系统而非外部背景”，关系类型为**概念来源、分析类比** [@wang2024openhands]。

**Agentless**用定位、修复和补丁验证的固定三阶段流水线对照开放式 Agent Loop，支撑第 18 章“复杂自主循环不是软件修复的唯一工程基线”，关系类型为**分析类比、风险证据** [@xia2024agentless]。

**AutoCodeRover**结合 AST 结构搜索与测试故障定位收窄仓库上下文，支撑第 18 章“结构化定位、编辑表达和 Git 事务是不同层次”，关系类型为**概念来源、分析类比** [@zhang2024autocoderover]。

**AgentBench**以多个交互环境评测模型作为 Agent 的长期推理、决策和指令遵循，支撑第 32 章“单一总分会掩盖环境差异且不能直接代表 Harness 产品质量”，关系类型为**概念来源、风险证据** [@liu2024agentbench]。

**LLM Agent 评测综述**把核心能力、应用基准、通用评测和开发工具放入同一地图，并指出成本、安全、鲁棒性与细粒度评测仍不足，支撑第 32 章的评测与真实数据议程，关系类型为**概念来源、风险证据** [@yehudai2025agentevalsurvey]。

## 协议和互操作

协议（Protocol）规定组件交换消息和状态的可检查契约，互操作（Interoperability）关注不同 Provider、客户端、扩展和观测后端能否在不丢失语义的情况下连接，[统一参考架构已经把能力、协议与客户端分层](04_reference_architecture.md#能力协议与客户端同一工具为什么会有不同体验)。本组优先收录正式规范和官方文档，并保留版本与访问日期意识，因为这些条目的价值来自契约边界，而不是一组永远不变的字段名。

**OpenAI Function Calling**规定工具定义、结构化调用、调用标识和结果回写由模型协议与应用共同完成，支撑第 06 与第 08 章“模型返回调用不等于工具已经执行”，关系类型为**协议契约** [@openai2025functioncalling]。

**MCP 2025-06-18 规范**定义 Host、Client、Server、能力协商、Tools、Resources、Prompts、roots 及传输语义，支撑第 09 章“MCP 标准化上下文与能力交换但不定义完整 Agent Loop 或权限系统”，关系类型为**协议契约** [@mcp20250618]。

**MCP Architecture Overview**说明 Host 通常为每个 Server 建立 Client 并统一管理连接，支撑第 09 章把生命周期、能力目录和工具名冲突归到 Host 组合层，关系类型为**协议契约** [@mcp2024architecture]。

**JSON-RPC 2.0**定义请求、通知、响应、错误和批处理的传输无关消息形状，支撑第 09 与第 20 章区分带 ID 请求、无响应通知和协议错误，关系类型为**协议契约** [@jsonrpc2013]。

**Anthropic Agent Skills 工程文档**以元数据预载、正文按需读取和附加资源渐进展开描述文件夹级 Skill，支撑第 11 与第 22 章“Skill 是可分发的过程性制品并带来来源风险”，关系类型为**协议契约** [@anthropic2025agentskills]。

**Git githooks 手册**规定不同 Git 生命周期阶段 Hook 的输入、退出码、可绕过性与通知语义，支撑第 11 章区分能够阻止动作、修改输入和只能事后通知的 Hook，关系类型为**协议契约、分析类比** [@git2026githooks]。

**Temporal Workflows 文档**以持久 Event History、确定性重放和外部 Activity 隔离定义 Durable Execution，支撑第 12 与第 21 章“恢复应复用已记录结果而不能重复外部调用”，关系类型为**协议契约、分析类比** [@temporal2026durableexecution]。

**Dapper**以共享 Trace ID 和父子 Span 串联跨进程请求，支撑第 19 章“模型请求、Tool Call 与子任务需要传播关联身份而不能只靠本地日志时间戳”，关系类型为**概念来源、分析类比** [@sigelman2010dapper]。

**OpenTelemetry 1.60.0**把 Trace、Metric、Log 和上下文传播分成可组合信号，并为 GenAI 调用提供仍在演进的语义约定，支撑第 19 章“互操作遥测应与业务 Event 分离且敏感内容默认不必全量采集”，关系类型为**协议契约** [@otel2026specification]。

**AI Agent 协议综述**区分面向上下文的协议与面向 Agent 间通信的协议，并以安全、可扩展性和延迟比较其边界，支撑第 32 章“MCP 契约不能自动承担异构 Agent 协作与责任归属”，关系类型为**概念来源、分析类比** [@yang2025agentprotocols]。

## 主题阅读顺序与正文对应关系

前六节按文献的主要用途各收录一次，实际阅读却经常需要跨主题组合。表 93-1 把常见问题、建议起点与回到正文后的继续路径放在同一视图中；它不是课程先修图，也不表示同一文献只能服务一个章节，而是帮助读者避免从 86 条记录中逐项试错。

| 读者问题 | 先读本章主题 | 回到正文的起点 | 继续阅读 |
|---|---|---|---|
| 一次模型回答怎样成为持续任务 | Agent Loop 与 Tool Use | [为什么一次响应不等于一个 Agent](05_harness_loop.md#为什么一次响应不等于一个-agent) | 第 08 章行动空间、第 21 章取消与资源控制 |
| 计划、Todo、子任务和多 Agent 怎样分工 | Planning 与 Multi-agent | [Goal、Plan、Task 与 Todo](15_goals_planning_and_todos.md#goalplantask-与-todo) | 第 16 章通信、Task DAG、Wait 与结果汇聚 |
| 历史、记忆、当前窗口和压缩怎样区分 | Memory 与 Context | [Memory 与 Session 状态的区别](10_memory.md#memory-与-session-状态的区别) | 第 07 章 Context、第 12 章 Resume、第 13 至 14 章压缩与成本 |
| 提示注入怎样跨过工具、权限和沙箱 | Security 与 Capability | [主体、能力与信任边界](17_security_permissions_and_sandboxing.md#主体能力与信任边界) | 第 19 章评测、第 20 章人在回路、第 22 章供应链 |
| 代码修改凭什么算完成 | Coding Agent 与软件 Agent | [Coding Harness 的工程闭环](18_code_editing_git_and_workspace.md#coding-harness-的工程闭环) | 第 07 章仓库上下文、第 19 章 Harness Eval |
| Provider、MCP、客户端和遥测怎样互联 | 协议和互操作 | [能力、协议与客户端](04_reference_architecture.md#能力协议与客户端同一工具为什么会有不同体验) | 第 06 章 Provider、第 09 章 MCP、第 20 章客户端、第 19 章观测 |
| 已有机制还缺少哪些可检验定义与公共证据 | 按问题组合前六个主题 | [Harness 的形式化模型](32_open_problems_and_research_agenda.md#harness-的形式化模型) | 第 32 章的安全、记忆、效率、恢复、多 Agent、协议与评测议程 |

*表 93-1　从读者问题进入主题文献，再回到正文机制章的建议路径。*

表 93-1 的关键用法是先确定当前判断需要哪一种证据。若问题是某个固定版本怎样实现 Tool Call、Memory 或 Sandbox，应回到相应正文和源码证据，而不是从论文名称推断实现；若问题是某种抽象从哪里来、已知失败怎样发生、协议承诺了什么，则从本章相应主题进入原始论文或正式规范。这样阅读可以把概念、类比、风险和契约保持在各自证据边界内，也让参考文献真正成为全书的第二条导航路径。
