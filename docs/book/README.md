# Agent Harness PDF 构建

本目录保存 PDF 的可复现构建资产。章节正文和参考文献仍以
`docs/harness-survey/` 为唯一来源；构建过程不会修改这些源文件。中间文件、
Mermaid 源片段和矢量 PDF 全部写入临时目录，最终文档固定输出到仓库根目录：

```text
Agent-Harness-架构工程与安全.pdf
```

## 环境准备

以下命令面向 Apple Silicon macOS 和 Homebrew：

```bash
brew install pandoc fonttools
brew install --cask mactex
brew install --cask font-source-han-serif-vf font-source-han-sans-vf
npm install --global @mermaid-js/mermaid-cli
npx puppeteer browsers install chrome-headless-shell
```

首次安装 MacTeX 后，重新打开终端，或先执行：

```bash
eval "$(/usr/libexec/path_helper)"
```

脚本要求 `python3`（含 FontTools 模块）、`pandoc`、`xelatex`、`kpsewhich` 和
`mmdc` 在 `PATH` 中，并检查 Eisvogel 定制使用的 LaTeX 包、两套思源 VF
字体以及 Puppeteer 的 `chrome-headless-shell`。如浏览器不在默认缓存目录，
可显式设置：

```bash
PUPPETEER_EXECUTABLE_PATH=/absolute/path/to/chrome-headless-shell docs/book/build.sh
```

## 依赖与版本

构建资产固定使用以 Eisvogel 3.5.1 为基线的模板，并增加了 CJK serif、sans、
mono 各自独立的 fontspec options，避免三类字体错误共享同一个 BoldFont。
2026-09-02 的端到端验证环境如下：

| 依赖 | 验证版本 |
|---|---:|
| Pandoc | 3.11 |
| MacTeX / TeX Live | 2026 |
| XeTeX | 0.999998 |
| Mermaid CLI | 11.16.0 |
| Node.js | 24.19.0 |
| chrome-headless-shell | 152.0.7977.54 |
| FontTools | 4.64.0 |
| Source Han Serif VF | 2.003R |
| Source Han Sans VF | 2.005R |
| Eisvogel | 3.5.1 |

Mermaid CLI、Puppeteer 与浏览器版本应保持相互兼容；最稳妥的方式是在安装或
升级 Mermaid CLI 后重新执行上面的 Puppeteer 浏览器安装命令。

## 一键编译

脚本可从任意工作目录运行（按实际 clone 位置调整路径）：

```bash
docs/book/build.sh          # 在仓库根目录
# 或任意目录下：
/path/to/harness/docs/book/build.sh
```

默认中间目录是 `${TMPDIR:-/tmp}/harness-book-build`。可通过
`HARNESS_BOOK_BUILD_DIR` 改写；字体静态实例缓存在
`/tmp/harness-book-fonts-$UID`，源 TTC 内容变化后自动重建。最终 PDF 的位置
不变。管线依次完成：

1. 检查命令、LaTeX 包、字体和 headless browser。
2. 从 VF TTC 的简体中文 face 临时生成 400/700 权重静态 OTF。
3. 按 `00-32、90、91、93` 顺序汇编 36 章。
4. 提取并按本目录主题把全部 Mermaid 图重渲染为矢量 PDF（当前为 35 张）。
5. 为图表生成稳定锚点，把正文中的“图 X-Y / 表 X-Y”转成 PDF 内链。
6. 归一化 GitHub 与 Pandoc 的内部链接 slug 差异。
7. 使用 Pandoc、citeproc、Eisvogel 和 XeLaTeX 生成 PDF。
8. 检查输出非空，并拒绝带未定义内链、引用或超出版心浮动体警告的结果。

PDF 先写入临时目录；只有全部质量门禁通过后才替换仓库根目录中的成品，因此
失败构建不会覆盖上一份已验证 PDF。

所有图片都启用 `keepaspectratio`，Mermaid 图同时给出最大宽度和最大高度，
由 LaTeX 选择约束更紧的一边并按自然纵横比缩放，不会拉伸图像。语义提示框
使用各自的强调色标题栏与白色标题文字。

构建器从 Mermaid 主题读取源字号，并计算通用最大缩放比例。当前源字号为 18 px，
目标有效字号上限为约 9.5 pt，因此任何图都不会因画布较小而被放大到超过该层级；
复杂图仍会受到最大宽度和高度约束而进一步缩小。该规则按图的自然尺寸自动生效，
不维护图号 override。

Mermaid 使用 `mmdc --pdfFit` 直接生成单页矢量 PDF，文字、节点和连线在放大后
仍保持清晰。矢量格式只能解决栅格模糊，不能解决构图本身过长导致的字号过小；
因此，过长图直接在 `docs/harness-survey/` 的 Mermaid 源中改成多行或阶段分组，
使 GitHub 与 PDF 使用同一份构图，避免双份来源漂移。
主题配置还收紧 flowchart 的节点与层级间距，并限制长标签的换行宽度，减少无效
留白，把页面缩放预算更多留给文字本身。

PDF 中的 Mermaid 使用受约束的 LaTeX `figure[!htbp]` 浮动体：图片与章节自带的
斜体图注始终处于同一浮动体；构建器在下一个 H2 或 H3 标题前插入 `FloatBarrier`，因此
图片可以越过本小节的后续正文，但不能漂入下一小节。引用句留在正文中，Pandoc
不再从图片 alt 文本生成第二个标题。图使用 `fig-X-Y`
锚点，表使用 `tab-X-Y` 锚点，正文中对应的“图 X-Y”和“表 X-Y”会在临时汇编稿
中自动变为可点击内链。

全部 Markdown 表按章节内出现顺序编号为“表 X-Y”，斜体表注统一置于表格上方。
已有作者表注直接复用；没有作者表注的表由构建器生成“章节名：对照表（Y）”。
构建器不再使用 Pandoc 的全书递增表号或第二个 caption。

## 目录结构

```text
docs/book/
├── README.md                 # 环境、用法和故障排查
├── build.sh                  # 一键入口与依赖预检
├── prepare.py                # 章节汇编、内链归一化、Mermaid 重渲染
├── prepare-fonts.py          # 从 VF TTC 生成临时 SC Regular/Bold OTF
├── title-page.yaml           # Eisvogel 扉页文字与颜色
├── metadata.yaml             # 页面、字体、目录、页眉页脚配置
├── header.tex                # LaTeX 颜色、框体、标题与浮动体定制
├── book-filter.lua           # 受约束浮动图、图表锚点、表题与语义提示框转换
├── mermaid-config.json       # Mermaid 主题
└── template/
    ├── eisvogel.latex        # Eisvogel 3.5.1 与 CJK options 定制
    └── LICENSE               # 上游许可证
```

`assets/` 不入库。`prepare.py` 每次从章节中的 Mermaid fenced code block 重新
生成临时 `.mmd` 和 `.pdf`，并写出 `diagram-manifest.json` 供排查。章节中的
Mermaid 是 GitHub 和 PDF 的唯一图源。

## 内链 slug 处理

GitHub 对标题 `事件溯源 Session 与 Surface / 日志分离` 生成的 fragment 是
`#事件溯源-session-与-surface--日志分离`，Pandoc 则使用单连字符版本。
`prepare.py` 只在临时汇编稿中把内部 fragment 的连续连字符折叠为一个，章节
源文件保持适合 GitHub 的原样。构建日志若仍出现 `Hyper reference ... undefined`
会直接判为失败。

## 常见故障

### VF 字体名错误

Homebrew cask 安装的是多地区 VF TTC。Fontconfig 可能把其中的 SC face 显示为
`Source Han Serif SC VF` 和 `Source Han Sans SC VF`，但 XeTeX 在 macOS 上
不一定能按这些 family 名访问 TTC 内的 SC face，直接写 TTC 文件名还可能在
`xdvipdfmx` 阶段失败。本管线因此用 FontTools 选择 SC face，再把 400/700
权重生成为临时静态 OTF，并为四个实例写入唯一的 OpenType 与 CFF PostScript
名称，避免 Regular、Bold、Serif 和 Sans 在 PDF 子集中共享 `CFF2Font` 名称。
不要把 TTC 文件名或 VF family 名直接改回
`metadata.yaml`。若此步骤失败，确认 `brew install fonttools` 已完成，并重新
安装两个字体 cask。

### 缺少 chrome-headless-shell

若预检报告找不到浏览器，运行：

```bash
npx puppeteer browsers install chrome-headless-shell
```

自定义 Puppeteer 缓存时设置 `PUPPETEER_CACHE_DIR`；已有独立浏览器时设置
`PUPPETEER_EXECUTABLE_PATH`。路径必须指向可执行文件本身。

### LaTeX 包或命令缺失

确认 `/Library/TeX/texbin` 已加入 `PATH`。BasicTeX 往往缺少模板需要的宏包；
此管线按完整 MacTeX 编写，安装完整发行版后重试。

### API、模型或网络报错

本构建不调用 OpenAI、Anthropic 或其他模型 API，不需要 API key，也不读取
Agent/provider 配置。依赖已经安装后，编译阶段除本地 Puppeteer 浏览器外没有
API 请求；任何模型额度、代理接口或 provider 报错都与本管线无关。

### 查看构建日志

Pandoc 和 XeLaTeX 的合并日志位于临时构建目录的 `build.log`。Mermaid 失败会
同时报告图号和来源章节；图的中间源文件位于临时目录的 `assets/`。
