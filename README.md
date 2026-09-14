# Agent Harness：架构、工程与安全

一本以中文撰写的 Agent Harness 比较研究书稿，围绕 Coding Agent 的运行循环、
上下文、工具、会话、扩展、委派与安全边界，分析七个开源系统的实现与设计取舍：
Codex、OpenCode、Pi、Gemini CLI、DeepSeek Harness、Goose 和 Aider。

全书以 Markdown 为唯一正文来源，可以直接在 GitHub 阅读，也可以编译为 PDF 和
多页面静态网站。
系统能力结论对应固定源码快照；具体版本见[版本与分析环境清单](docs/harness-survey/91_version_manifest.md)。

## 阅读入口

- [序章、阅读路线与完整目录](docs/harness-survey/00_index.md)
- [认识 Agent Harness](docs/harness-survey/01_introducing_agent_harness.md)
- [横向能力地图](docs/harness-survey/02_horizontal_capability_map.md)
- [一次任务的纵向生命周期](docs/harness-survey/03_vertical_lifecycle_walkthrough.md)
- [统一参考架构](docs/harness-survey/04_reference_architecture.md)
- [参考文献阅读入口](docs/harness-survey/93_references.md)

## 生成网页版

网页版包含左侧全书目录、右侧本章目录、前后章导航、深浅主题和 Pagefind 中文搜索。
在仓库根目录运行：

```bash
docs/web/build.sh
docs/web/serve.sh
```

构建结果位于 `site/`，本地预览地址默认为 `http://127.0.0.1:8000/`。Node 依赖由
`docs/web/package-lock.json` 锁定；脚本会自动执行 `npm ci`，无需全局安装 Mermaid
或 Pagefind。网页字体使用官方 Google Fonts 的 `Noto Serif SC` 和 `Noto Sans SC`，
并保留本机思源/Noto 字体回退。

`.github/workflows/pages.yml` 会在 Pull Request 中完整编译 PDF 和 HTML/SVG/Pagefind，
并把 PDF 保存为可下载的 Actions artifact；在 `main` 推送或手动触发时，Web job 会消费
同一提交的 PDF artifact，把下载按钮和文件一起部署到 GitHub Pages。
详细依赖、环境变量、Cloudflare Fonts 选项和故障排查见
[网页版构建文档](docs/web/README.md)。仅生成网页不需要初始化七个源码子模块。

## 编译 PDF

构建入口是 `docs/book/build.sh`。它汇编 `00`–`32`、`90`、`91`、`93` 共 36 章，
把 Mermaid 图渲染为矢量 PDF，再通过 Pandoc、Eisvogel 模板、citeproc 和 XeLaTeX
生成整本书。仅阅读或编译书稿不需要初始化根目录的七个源码子模块。

### 1. 安装依赖

以下命令面向 Apple Silicon macOS，假定已经安装 Homebrew 和 npm。其他系统需要
自行适配字体路径与浏览器环境；当前构建脚本按 macOS/MacTeX 编写。

```bash
brew install pandoc fonttools
brew install --cask mactex
brew install --cask font-source-han-serif-vf font-source-han-sans-vf
npm install --global @mermaid-js/mermaid-cli@11.16.0
npx puppeteer browsers install chrome-headless-shell
```

安装 MacTeX 后重新打开终端，或执行以下命令加载 TeX 工具路径：

```bash
eval "$(/usr/libexec/path_helper)"
```

脚本会检查 `python3`、`fonttools`、`pandoc`、`xelatex`、`kpsewhich`、`mmdc`，
以及所需 LaTeX 宏包、字体和 headless browser。完整版本说明与故障排查见
[PDF 构建文档](docs/book/README.md)。

### 2. 一键编译

在仓库根目录运行：

```bash
docs/book/build.sh
```

成功后，PDF 固定输出到仓库根目录：

```text
Agent-Harness-架构工程与安全.pdf
```

首次运行需要从思源可变字体生成四套静态字体，可能耗时十几分钟；结果缓存于
`/tmp/harness-book-fonts-$UID`，后续构建会复用，临时缓存被清理后会重新生成。
依赖就绪后，编译无需模型 API、API key 或源码子模块的运行环境。

### 3. 日志与常见问题

默认构建日志为 `${TMPDIR:-/tmp}/harness-book-build/build.log`。可以指定独立目录：

```bash
HARNESS_BOOK_BUILD_DIR=/tmp/harness-book-build-local docs/book/build.sh
```

此时查看 `/tmp/harness-book-build-local/build.log`。**脚本每次会清空指定的构建目录，
请使用专门的临时目录。** 字体预检失败时查看同目录的 `font-check.log`；
Mermaid 失败会在终端报告来源章节和图号。

- 找不到 `mmdc`：确认 Mermaid CLI 已安装，且 npm 的全局可执行目录位于 `PATH`。
- 找不到 `xelatex` 或 LaTeX 包：确认完整 MacTeX 已安装，且 `/Library/TeX/texbin`
  位于 `PATH`。
- 找不到浏览器：运行上面的 Puppeteer 安装命令，或使用下方环境变量指定已有浏览器。
- 在受限 Agent 沙箱中遇到 Chrome 的 `Permission denied`：需要允许启动本地浏览器，
  或在普通终端中运行构建脚本。

```bash
PUPPETEER_EXECUTABLE_PATH=/absolute/path/to/chrome-headless-shell docs/book/build.sh
```

构建会拒绝未定义内链、引用或超出版心浮动体警告；只有质量检查通过才替换成品，
失败构建不会覆盖上一份 PDF。

## 仓库结构

| 路径 | 用途 |
|---|---|
| `docs/harness-survey/[编号]_*.md` | 正式章节与附录 |
| `docs/harness-survey/references.bib` | 全书参考文献 |
| `docs/book/` | 编译脚本、模板、字体处理与图表主题 |
| `docs/web/` | 网页生成、主题、搜索、验证与部署资产 |
| `.github/workflows/pages.yml` | GitHub Pages 构建与部署 |
| `docs/harness-survey/WRITING_PLAN.md` | 详细编辑规范与历史章节设计 |
| `docs/harness-survey/review-report-*.md` | 历史审阅记录，不进入 PDF |
| `.agents/skills/harness-survey-source-chapter/` | 可选的 Agent 写作与核验约定 |
| `codex/`、`opencode/`、`pi/` 等根目录 | 七个固定版本的源码子模块 |

PDF 和网页构建都只读取编号章节及构建资产，计划和审阅记录不参与正文汇编。

## 参与贡献

欢迎修正文字、补充可核验的源码证据、改进图表与排版，或提出章节结构建议。
具体步骤、写作约定、版本边界和提交前检查见 [CONTRIBUTING.md](CONTRIBUTING.md)。
