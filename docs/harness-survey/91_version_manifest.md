# 版本与分析环境清单

本附录记录全书采用的版本快照（version snapshot），包括父仓库提交（commit）、[七个子模块（Submodule）](18_code_editing_git_and_workspace.md#gitworktree-与-submodule)的精确提交、上游来源、根许可证（license）和分析截止日期。正文中的固定版本结论均以这里的提交为准。

## 清单使用说明

复查正文结论时，先在表 91-1 确认父仓库版本，再在表 91-2 找到目标项目的固定提交。表中的默认分支用于识别上游入口，提交散列才是实际版本坐标。上游版本发生变化后，应新增版本记录并重新核对受影响的章节。

## 父仓库快照

父仓库固定在提交 `b964dd3896239ff06e13c9efd363266755e5d9af`。该提交固定报告结构、编辑计划与七个子模块 gitlink，并与表 91-2 的项目提交共同定义研究版本。正文保留完整散列，表格统一显示前 12 位短哈希。

| 项目 | 固定值 | 在分析中的作用 |
|---|---|---|
| 父仓库提交 | `b964dd389623` | 固定报告计划、章节组织和七个子模块 gitlink |
| 研究对象 | Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、Goose、Aider | 形成全书统一的七系统比较范围 |
| 版本坐标 | 父仓库提交与项目提交 | 定位固定研究版本 |

*表 91-1　父仓库研究快照。表内使用 12 位短哈希，完整父提交见表前正文；父提交与子模块提交共同定义本报告的源码语料边界。*

父仓库提交固定报告结构、编辑计划和七个子模块 gitlink；项目源码版本则由表 91-2 的提交分别确定。

## 七个 Submodule 快照

表 91-2 列出七个 Git 子模块的精确提交、检出时识别的上游默认分支和本报告采用的引用（ref）类型。表格显示 12 位短哈希，每个短哈希都链接到包含完整 40 位散列的固定提交页面；“默认分支”仅说明上游来源结构，“精确 commit”表示分析不随该分支继续移动。

| Harness | 固定提交 | 上游默认分支 | 所选 ref 类型 | 个案入口 |
|---|---|---|---|---|
| Aider | [`5dc9490bb35f`](https://github.com/Aider-AI/aider/commit/5dc9490bb35f9729ef2c95d00a19ccd30c26339c) | `main` | 精确 commit | [Aider：Git-centric Coding Agent](29_aider.md) |
| Codex | [`bd19459358f5`](https://github.com/openai/codex/commit/bd19459358f534ed1cae464ec13d56600aeb45f2) | `main` | 精确 commit | [Codex：安全控制面与多入口 Runtime](23_codex.md) |
| DeepSeek Harness | [`141eb6fef834`](https://github.com/deepseek-ai/deepseek-harness/commit/141eb6fef83422698aef7a981029e843e8161534) | `master` | 精确 commit | [DeepSeek Harness：组合式 Harness 架构](27_deepseek_harness.md) |
| Gemini CLI | [`30573d2e4d85`](https://github.com/google-gemini/gemini-cli/commit/30573d2e4d85bdc2c0ae8218c377cd410336da77) | `main` | 精确 commit | [Gemini CLI：搜索增强、扩展与自动化](26_gemini_cli.md) |
| Goose | [`d830653309a3`](https://github.com/aaif-goose/goose/commit/d830653309a32ebfae0b86fbe48164aaeca79fdf) | `main` | 精确 commit | [Goose：本地 Agent 与 MCP 生态](28_goose.md) |
| OpenCode | [`2859603cbb5e`](https://github.com/anomalyco/opencode/commit/2859603cbb5e346d1c32519cb3f5ee58b0d78455) | `dev` | 精确 commit | [OpenCode：多模型平台与 Agent Mode](24_opencode.md) |
| Pi | [`5cd93f688aaa`](https://github.com/earendil-works/pi/commit/5cd93f688aaab89dbb6dfa4aca535f21796ae185) | `main` | 精确 commit | [Pi：极简而可扩展的 Agent Runtime](25_pi.md) |

*表 91-2　七个子模块的固定源码提交。表内显示 12 位短哈希，链接目标保留完整散列。*

OpenCode 的默认分支为 `dev`，DeepSeek Harness 为 `master`，其余项目为 `main`。DeepSeek Harness 固定版本的开发者预览状态见[个案章的项目定位](27_deepseek_harness.md#项目定位与组合原则)。

## 许可证与上游来源

表 91-3 汇总各项目的官方仓库、根许可证，以及固定提交下的 README 和 LICENSE 入口。

| Harness | 上游来源 | 根许可证 | 固定版本核对入口 |
|---|---|---|---|
| Aider | [Aider-AI/aider](https://github.com/Aider-AI/aider) | Apache License 2.0 | [README](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/README.md)；[LICENSE.txt](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/LICENSE.txt) |
| Codex | [openai/codex](https://github.com/openai/codex) | Apache License 2.0 | [README](https://github.com/openai/codex/blob/bd19459358f534ed1cae464ec13d56600aeb45f2/README.md)；[LICENSE](https://github.com/openai/codex/blob/bd19459358f534ed1cae464ec13d56600aeb45f2/LICENSE) |
| DeepSeek Harness | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | MIT License | [README](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/README.md)；[LICENSE](https://github.com/deepseek-ai/deepseek-harness/blob/141eb6fef83422698aef7a981029e843e8161534/LICENSE) |
| Gemini CLI | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | Apache License 2.0 | [README](https://github.com/google-gemini/gemini-cli/blob/30573d2e4d85bdc2c0ae8218c377cd410336da77/README.md)；[LICENSE](https://github.com/google-gemini/gemini-cli/blob/30573d2e4d85bdc2c0ae8218c377cd410336da77/LICENSE) |
| Goose | [aaif-goose/goose](https://github.com/aaif-goose/goose) | Apache License 2.0 | [README](https://github.com/aaif-goose/goose/blob/d830653309a32ebfae0b86fbe48164aaeca79fdf/README.md)；[LICENSE](https://github.com/aaif-goose/goose/blob/d830653309a32ebfae0b86fbe48164aaeca79fdf/LICENSE) |
| OpenCode | [anomalyco/opencode](https://github.com/anomalyco/opencode) | MIT License | [README](https://github.com/anomalyco/opencode/blob/2859603cbb5e346d1c32519cb3f5ee58b0d78455/README.md)；[LICENSE](https://github.com/anomalyco/opencode/blob/2859603cbb5e346d1c32519cb3f5ee58b0d78455/LICENSE) |
| Pi | [earendil-works/pi](https://github.com/earendil-works/pi) | MIT License | [README](https://github.com/earendil-works/pi/blob/5cd93f688aaab89dbb6dfa4aca535f21796ae185/README.md)；[LICENSE](https://github.com/earendil-works/pi/blob/5cd93f688aaab89dbb6dfa4aca535f21796ae185/LICENSE) |

*表 91-3　七个固定源码树的官方上游与根许可证。README 和 LICENSE 链接指向固定提交。*

表中的许可证指项目根许可证；第三方依赖和捆绑制品仍以对应提交中的声明为准。

## 分析日期和必要环境

本报告的分析截止日期为 2026 年 9 月 2 日。复查某个项目时，应检出表 91-2 的完整提交，并采用该提交自己的锁文件、工具链声明和平台说明。正文若引用具体运行观察，会在相应位置说明必要条件。

## 版本更新记录

| 版本 | 日期 | 变更 |
|---|---|---|
| 初版 | 2026-09-02 | 建立父仓库、七个子模块、上游许可证、分析日期与必要环境的固定清单。 |

后续更新应新增记录，列出变化的快照和受影响章节，并保留旧版本坐标。
