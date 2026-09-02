# 版本与分析环境清单

本附录把全书的源码结论绑定到一组可复查的版本快照（version snapshot）。读者若从这里独立进入，可以先回到[“一句话请求先要落到正确的工作区”教学案例](00_index.md#一句话请求先要落到正确的工作区)：案例说明工作区选错会让后续分析作用于错误对象，本清单则进一步回答“分析的究竟是哪一份源码”。它记录父仓库提交（commit）、[七个子模块（Submodule）](18_code_editing_git_and_workspace.md#gitworktree-与-submodule)的精确提交、上游来源、许可证（license）与分析环境，不承担源码证据台账或项目排名的职责。

## 清单使用说明

正文中的“固定版本”“当前分析范围”均指本清单列出的提交，而不是读者访问上游仓库时看到的最新分支。分支名只帮助识别上游的日常开发入口，精确提交才是复查结论的稳定坐标。尤其要注意，部分子模块以分离头指针（detached HEAD）检出：默认分支在分析期间继续移动，不会改变本报告已经固定的源码内容。

使用本清单复查某项工程结论时，应先在表 91-1 和表 91-2 确认父仓库与项目提交，再进入相应个案章或机制章理解结论范围。项目主页、发行说明和默认分支适合了解后续变化，不能直接替换固定提交。若上游后来重命名组件、修改默认行为或修复缺陷，应在新版本记录中重新分析，而不是把新状态静默投射到旧正文。

本附录只公开面向读者的版本与环境元数据。源码路径、符号、调用链、测试定位与证据状态继续保存在作者内部台账中；这种分工与[Git、Worktree 与 Submodule 的版本边界](18_code_editing_git_and_workspace.md#gitworktree-与-submodule)一致：父仓库负责固定研究语料，正文负责解释机制，内部台账负责保存可审查的证据链。

## 父仓库快照

父仓库固定在提交 `b964dd3896239ff06e13c9efd363266755e5d9af`。该提交是报告结构、编辑计划与七个子模块 gitlink 的共同基线；所有跨系统比较都应同时满足“父仓库文档属于该研究版本”和“子模块源码属于表 91-2 的精确提交”两个条件。

| 项目 | 固定值 | 在分析中的作用 |
|---|---|---|
| 父仓库提交 | `b964dd3896239ff06e13c9efd363266755e5d9af` | 固定报告计划、章节组织和七个子模块 gitlink |
| 研究对象 | Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、Goose、Aider | 形成全书统一的七系统比较范围 |
| 版本解释 | 精确提交优先于分支名、标签名与访问时的上游页面 | 防止把后续上游变化倒写为固定版本事实 |

*表 91-1　父仓库研究快照。父提交与子模块提交共同定义本报告的源码语料边界。*

表 91-1 的“精确提交优先”也约束结论强度。源码能够支持固定版本中已实现的结构和行为，但不能据此声称当前上游仍保持相同默认值，也不能把分支名称、发布时间或项目成熟度转换成质量判断。跨版本的新事实需要重新建立配置、入口、状态与行为结果之间的证据链。

## 七个 Submodule 快照

表 91-2 列出七个 Git 子模块的精确提交、检出时识别的上游默认分支和本报告采用的引用（ref）类型。七项都以完整提交散列固定；“默认分支”仅说明上游来源结构，“精确 commit”表示分析不随该分支继续移动。

| Harness | 固定提交 | 上游默认分支 | 所选 ref 类型 | 个案入口 |
|---|---|---|---|---|
| Aider | `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` | `main` | 精确 commit | [Aider：Git-centric Coding Agent](29_aider.md) |
| Codex | `bd19459358f534ed1cae464ec13d56600aeb45f2` | `main` | 精确 commit | [Codex：安全控制面与多入口 Runtime](23_codex.md) |
| DeepSeek Harness | `141eb6fef83422698aef7a981029e843e8161534` | `master` | 精确 commit | [DeepSeek Harness：组合式 Harness 架构](27_deepseek_harness.md) |
| Gemini CLI | `30573d2e4d85bdc2c0ae8218c377cd410336da77` | `main` | 精确 commit | [Gemini CLI：搜索增强、扩展与自动化](26_gemini_cli.md) |
| Goose | `d830653309a32ebfae0b86fbe48164aaeca79fdf` | `main` | 精确 commit | [Goose：本地 Agent 与 MCP 生态](28_goose.md) |
| OpenCode | `2859603cbb5e346d1c32519cb3f5ee58b0d78455` | `dev` | 精确 commit | [OpenCode：多模型平台与 Agent Mode](24_opencode.md) |
| Pi | `5cd93f688aaab89dbb6dfa4aca535f21796ae185` | `main` | 精确 commit | [Pi：极简而可扩展的 Agent Runtime](25_pi.md) |

*表 91-2　七个子模块的固定源码提交。项目顺序不表示排名；完整散列是复查正文结论的版本主键。*

这七个快照不是同一天的“最新版本”截面，也不要求项目具有相同发布节奏。OpenCode 使用 `dev`，DeepSeek Harness 使用 `master`，其余项目在检出元数据中使用 `main`；这些名称反映上游工作方式，不构成稳定性分数。DeepSeek Harness 的固定版本仍处于开发者预览，相关兼容性限制已在[个案章的项目定位](27_deepseek_harness.md#项目定位与组合原则)中说明。

## 许可证与上游来源

表 91-3 使用各固定源码树根目录的 README 与 LICENSE 文件核对项目身份、官方仓库和许可证。许可证列描述项目根许可证，不替代依赖、捆绑制品、模型服务、数据集或外部扩展各自的授权条件；需要分发或再利用时，仍应检查对应提交中的第三方声明和依赖清单。

| Harness | 上游来源 | 根许可证 | 固定版本核对入口 |
|---|---|---|---|
| Aider | [Aider-AI/aider](https://github.com/Aider-AI/aider) | Apache License 2.0 | [README](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/README.md)；[LICENSE.txt](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/LICENSE.txt) |
| Codex | [openai/codex](https://github.com/openai/codex) | Apache License 2.0 | [README](https://github.com/openai/codex/blob/bd19459358f534ed1cae464ec13d56600aeb45f2/README.md)；[LICENSE](https://github.com/openai/codex/blob/bd19459358f534ed1cae464ec13d56600aeb45f2/LICENSE) |
| DeepSeek Harness | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | MIT License | [README](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/README.md)；[LICENSE](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/LICENSE) |
| Gemini CLI | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | Apache License 2.0 | [README](https://github.com/google-gemini/gemini-cli/blob/30573d2e4d85bdc2c0ae8218c377cd410336da77/README.md)；[LICENSE](https://github.com/google-gemini/gemini-cli/blob/30573d2e4d85bdc2c0ae8218c377cd410336da77/LICENSE) |
| Goose | [aaif-goose/goose](https://github.com/aaif-goose/goose) | Apache License 2.0 | [README](https://github.com/aaif-goose/goose/blob/d830653309a32ebfae0b86fbe48164aaeca79fdf/README.md)；[LICENSE](https://github.com/aaif-goose/goose/blob/d830653309a32ebfae0b86fbe48164aaeca79fdf/LICENSE) |
| OpenCode | [anomalyco/opencode](https://github.com/anomalyco/opencode) | MIT License | [README](https://github.com/anomalyco/opencode/blob/2859603cbb5e346d1c32519cb3f5ee58b0d78455/README.md)；[LICENSE](https://github.com/anomalyco/opencode/blob/2859603cbb5e346d1c32519cb3f5ee58b0d78455/LICENSE) |
| Pi | [earendil-works/pi](https://github.com/earendil-works/pi) | MIT License | [README](https://github.com/earendil-works/pi/blob/5cd93f688aaab89dbb6dfa4aca535f21796ae185/README.md)；[LICENSE](https://github.com/earendil-works/pi/blob/5cd93f688aaab89dbb6dfa4aca535f21796ae185/LICENSE) |

*表 91-3　七个固定源码树的官方上游与根许可证。链接直接指向固定提交，避免访问时的默认分支变化影响核对。*

许可证只回答在其条款下使用、修改和分发项目代码的条件，不能证明来源可信、依赖无风险或自动更新经过验证。[Plugin、MCP 与 Skill 来源](22_configuration_identity_and_supply_chain.md#pluginmcp-与-skill-来源)和[自动更新与依赖生命周期](22_configuration_identity_and_supply_chain.md#自动更新与依赖生命周期)进一步解释了为什么包、插件、模型和发布制品还需要独立的来源与完整性判断。

## 分析日期和必要环境

本轮源码分析与章节撰写发生在 2026 年 8 月至 2026 年 9 月 2 日。主要方法是固定源码阅读、配置与测试入口追踪、跨项目机制归一化，以及 Markdown 结构、链接和引用键校验。它不是统一模型、统一任务和统一硬件下的性能实验，因此本清单不提供速度、成功率、成本或安全排名。

直接用于本轮分析和文档校验的本地环境为 macOS 26.6.2、Apple Silicon `arm64`、zsh 5.9、ripgrep 15.2.0、Python 3.14.7 与 Node.js 24.19.0。该环境足以读取七个固定源码树、执行文本检查和运行本附录的结构校验，但不等于七个项目均已在同一机器上完成原生构建。当前 PATH 未提供 pnpm、Bun 或 Rust 工具链，因此涉及这些生态的实现判断以固定源码与仓库测试定义为主要依据，不把“存在测试”写成“本轮已经执行测试”。

各项目声明的必要工具链也不同。Aider 要求 Python `>=3.10,<3.15`；Codex 根 JavaScript 工具要求 Node.js `>=22` 和 pnpm `>=10.33.0`，核心另含 Rust 工作区；DeepSeek Harness 要求 Node.js `^22.19.0 || >=24.0.0` 与 pnpm 11.7.0；Gemini CLI 要求 Node.js `>=20`；OpenCode 固定 Bun 1.3.14；Pi 要求 Node.js `>=22.19.0`；Goose 的 Rust 工作区声明 Rust 1.94.1。复现某一项目的构建或运行时，应采用该固定提交自己的锁文件、工具链声明和平台说明，不用本机已有版本替代项目约束。

[模型服务提供方（Provider）的抽象边界](06_model_and_provider_abstraction.md#provider-层在隔离什么)、凭据、权限模式、沙箱和网络配置都会改变运行观察。除非正文明确记录了相应条件，本报告的源码结论不假定某一商业模型、账户套餐或默认授权配置；这也符合[Provider Credential 的责任边界](22_configuration_identity_and_supply_chain.md#provider-credential)和[权限与沙箱的分层定义](17_security_permissions_and_sandboxing.md#tool-permission-与-human-approval)。环境记录只保留影响复查的系统与工具版本，不公开用户名、本地绝对路径、凭据、账户标识、代理地址或其他秘密。

## 版本更新记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 初版 | 2026-09-02 | 建立父仓库、七个子模块、上游许可证、分析日期与必要环境的固定清单。 |

本清单的初版把全书结论收束到一个父仓库提交和七个项目提交。后续更新应新增记录，说明哪些快照、环境或正文结论发生变化，并重新检查相关机制章与个案章；旧记录继续保留，避免“当前上游”覆盖“当时分析”。读者由此可以从版本坐标进入源码，也可以回到[配置、身份与供应链](22_configuration_identity_and_supply_chain.md)理解版本固定为何既是复现条件，也是工程结论的边界。
