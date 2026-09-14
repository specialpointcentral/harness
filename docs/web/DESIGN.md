# Agent Harness 网页版设计

> 状态：已实现并完成本地验证，待提交与 GitHub Pages 部署
>
> 日期：2026-09-14

## 1. 目标

在不改变现有书稿来源和 PDF 输出的前提下，为《Agent Harness：架构、工程与安全》
增加可本地生成、可由 GitHub Actions 自动发布到 GitHub Pages 的多页面网页版。

网页版需要满足以下读者目标：

- 每章一个独立页面；
- 左侧显示按全书分部组织的章节目录；
- 右侧显示当前章节的 H2/H3 目录；
- 支持中文全文搜索，并能跳转到命中小节；
- 支持浅色和深色主题，记住读者选择；
- 在桌面和移动设备上都能顺畅阅读；
- 图、表、引用和章节链接可点击且稳定；
- 正文字体、标题字体、语义色和 PDF 尽量一致；
- 本地构建与 GitHub Pages 使用同一入口和同一产物。

## 2. 非目标

第一版不加入评论、用户账户、服务端搜索、阅读进度同步、离线 PWA、在线编辑、
多语言切换或运行时 Mermaid 渲染。网页是纯静态产物，不需要数据库、应用服务器或
模型 API。

现有 PDF 仍由 `docs/book/build.sh` 生成。网页构建不会取代 PDF 管线，也不会要求
修改 36 个编号章节以适配某个站点框架。

## 3. 技术选择

采用 Pandoc 多页面 HTML、自定义 HTML 模板与 CSS、少量原生 JavaScript，以及
Pagefind 静态搜索。

选择这一方案的原因是现有书稿已经依赖 Pandoc 的引用处理、标题标识符和 AST filter。
继续使用 Pandoc 可以让 PDF 与网页共享 Markdown 和 `references.bib`，同时保留对
图表编号、语义提示框、字体和页面结构的精确控制。Pagefind 在 HTML 生成后建立索引，
无需把搜索逻辑耦合到正文转换过程。

不采用 Quarto Book 作为第一版框架。Quarto 能快速提供侧栏、搜索和主题，但会引入
另一套书籍约定，并需要协调现有图号、表号、提示框和链接处理。Material for MkDocs
使用不同的 Markdown 处理链，与当前 Pandoc 引用和 filter 的适配成本更高。

## 4. 源文件与输出边界

正式内容仍只有以下来源：

- `docs/harness-survey/[编号]_*.md`；
- `docs/harness-survey/references.bib`；
- `docs/book/mermaid-config.json`；
- PDF 与 Web 各自的模板和转换代码。

构建产物写入仓库根目录的 `site/`，不纳入普通 Git 提交。生成的整本 PDF、`site/`、
临时图和 Pagefind 索引中间文件应由根目录 `.gitignore` 排除。

建议的实现结构如下：

```text
docs/
├── book/
│   ├── book-manifest.json       # 两种输出共享的章节顺序与分部
│   ├── build.sh                 # 现有 PDF 入口
│   └── ...
└── web/
    ├── README.md                # 本地构建和故障排查
    ├── build.sh                 # Web 唯一构建入口
    ├── prepare.py               # 章节转换、导航和产物检查
    ├── book-filter.lua          # HTML 语义转换
    ├── package.json             # 锁定 Mermaid、Puppeteer、Pagefind
    ├── package-lock.json
    ├── template/
    │   └── page.html
    └── assets/
        ├── book.css
        ├── book.js
        └── icons/

.github/workflows/pages.yml      # 构建并发布 site/
site/                            # 本地与 CI 的同构产物，不提交
```

`book-manifest.json` 只保存章节前缀顺序和分部边界；章节标题继续从 Markdown H1 读取，
避免维护两份标题。PDF `prepare.py` 和 Web `prepare.py` 都读取该 manifest。首次抽取该
共享数据时必须运行完整 PDF 回归，证明 PDF 章节顺序和分部没有变化。

## 5. URL 与链接模型

序章生成到站点根目录：

```text
site/index.html
```

其余章节使用由源文件名确定的稳定目录 URL：

```text
docs/harness-survey/05_harness_loop.md
    -> site/chapters/05-harness-loop/index.html
    -> /chapters/05-harness-loop/
```

H1 文字变化不会改变章节 URL。章节内 H2/H3 使用 Pandoc 自动标识符；构建器需要解析
最终 HTML，验证所有相对链接的文件目标和 fragment 均存在。源文件中的 `.md` 链接在
Web 构建时转换为目标章节 URL，PDF 构建仍转换为同一文档内的锚点。

所有站内链接和静态资源使用相对路径，不假定站点部署在域名根目录。这样同一产物可以
同时工作于本地预览、GitHub 用户站点和 `/repository-name/` 形式的项目站点。每个页面
由模板得到到站点根目录的相对深度，用于加载 CSS、JavaScript 和 Pagefind 索引。

正文中的“图 X-Y”和“表 X-Y”在网页中转换为指向 `#fig-X-Y` 和 `#tab-X-Y` 的链接。
图、表自身分别使用 `<figure id="fig-X-Y">` 和带锚点的表格容器。引用链接由 Pandoc
`citeproc` 生成，并跳转到当前页面的参考文献区域或全书参考入口，具体取决于该章是否
产生参考文献列表。

## 6. 页面布局与导航

桌面页面由四个稳定区域组成：

1. 顶部工具栏：书名、搜索、主题切换、PDF 下载和仓库链接；
2. 左侧目录：按分部折叠的 36 章全书导航，当前章节高亮；
3. 中央正文：限制舒适行宽，承载章节、图表、引用和提示框；
4. 右侧目录：当前页面 H2/H3 导航，滚动时高亮当前小节。

页面底部提供上一章和下一章。序章没有上一章，最后一章没有下一章。

移动端保持单栏正文。左侧全书目录和右侧页内目录分别进入抽屉，由明确的目录按钮打开；
打开抽屉时锁定背景滚动，Escape、遮罩点击和导航完成都能关闭。主题切换和搜索始终位于
顶部工具栏，不依赖悬停操作。

布局不使用应用框架。导航高亮、目录抽屉、主题切换和当前标题观察使用原生 JavaScript，
避免为少量交互引入前端打包器和运行时依赖。

## 7. Markdown 到 HTML 的转换

Web 管线逐章调用 Pandoc，保留当前 Markdown 扩展、`citeproc` 和 bibliography。
HTML 专用 Lua filter 处理以下结构：

- 四类语义提示框转换为带标题的 `<aside>`；
- Mermaid 图转换为带稳定 ID 的 `<figure>`；
- Markdown 表格保留作者表注，增加稳定 ID 和可横向滚动容器；
- 章节交叉引用转换为多页面 URL；
- 外部链接增加一致的可访问性标识，不强制新窗口打开；
- 代码块增加语言类名和横向滚动，不加入运行时高亮库。

Web `prepare.py` 从 Mermaid fenced block 提取 `.mmd`，使用与 PDF 相同的
`mermaid-config.json` 生成 SVG。SVG 以内联方式写入 `<figure>`，使页面的 Noto Sans SC
字体、主题变量和缩放规则同时作用于图中文字。搜索索引忽略 SVG 内部文字，避免
图中文字产生重复和低质量搜索结果。

Web 不维护逐图配置或第二份图源。构建器根据图类型派生临时渲染配置：flowchart 使用
原生 SVG text/rect 标签、120px 节点换行宽度和 22px/600 的边标签；超过 18 显示列的
边标签在临时 Mermaid 文本中选择接近中点的空格、标点或中文连接位置断行。sequence
diagram 与 state diagram 不套用 flowchart 覆盖。SVG ID 从输出文件名统一生成，并以
`diagram-` 开头，避免多图内联时重复或产生无效 CSS 选择器。

PDF 继续生成矢量 PDF 图。两种输出共享 Mermaid 源、主题变量和图号，但使用适合各自
介质的矢量格式。

## 8. 字体与视觉系统

网页版使用以下字体映射：

- 正文：Google Fonts 的 Noto Serif SC Variable；
- 标题、导航、表格和提示框：Google Fonts 的 Noto Sans SC Variable；
- 代码：`Menlo, Monaco, Consolas, monospace`。

页面直接使用 Google Fonts CSS2 API，不把字体文件写入仓库或 `site/`。CSS fallback
依次使用本机 Source Han SC、Noto CJK SC 和通用 serif/sans-serif，因此字体服务失败时
正文仍可阅读。验证器只允许 `fonts.googleapis.com` 和 `fonts.gstatic.com` 作为外部
运行资源，其他外部脚本、样式、字体和搜索服务仍然失败。

默认 GitHub Pages 直接访问 Google Fonts。配置经过 Cloudflare 代理的自定义域名后，
可以启用 Cloudflare Fonts，在边缘把 Google Fonts 改写为站点自身域名下的请求。
Cloudflare 改写是可选部署优化，不进入本地构建逻辑；默认 `github.io` 域名无法由项目的
Cloudflare zone 改写。

CSS 使用 PDF 已定义的颜色作为浅色主题基线：

```text
HarnessNavy   #183247
HarnessBlue   #356C91
HarnessTeal   #2E7784
HarnessGreen  #39755E
HarnessGold   #A77332
HarnessCoral  #AA4E4B
HarnessGray   #61717E
HarnessLight  #F4F7F9
```

浅色主题尽量还原 PDF 的标题、链接、表格和四类提示框。深色主题保留相同语义色关系，
但单独定义背景、正文、边框和强调色，不通过简单反色生成。最终颜色必须通过 WCAG AA
正文对比度检查。

页面在 `<head>` 的同步短脚本中优先读取本地主题选择，其次读取系统
`prefers-color-scheme`，避免页面加载后闪烁。用户切换后写入 `localStorage`。主题按钮
具有文本替代和可见焦点状态。

字体使用 `font-display: swap` 和可变字重范围。构建检查确认页面只引用两个允许的官方
Google Fonts 域名；浏览器检查需要同时覆盖字体成功加载与字体请求失败后的可读回退。

## 9. 全文搜索

所有 HTML 页面生成后运行 Pagefind。站点语言设置为 `zh-CN`，仅中央正文容器标记为
可索引内容；全书目录、页内目录、工具栏、前后章链接和页脚排除在索引之外。

搜索结果包含：

- 章节标题；
- 命中小节；
- 带关键词上下文的摘要；
- 指向命中标题 fragment 的链接。

桌面端搜索显示为顶部展开面板或模态层，移动端使用全宽面板。键盘可以打开搜索、遍历
结果和关闭面板。搜索无结果时显示中文提示，不请求远程服务。

构建门禁要求 Pagefind 索引存在、36 个页面全部被索引。中文查询在浏览器验收中使用
“上下文压缩”“权限”“Subagent”等代表词验证，不把排序分数或结果数量固定成脆弱的
构建测试。

## 10. 本地构建与预览

本地唯一构建入口为：

```bash
docs/web/build.sh
```

脚本依次执行：

1. 检查 Pandoc、Python、Node.js 和 npm；
2. 使用 `npm ci` 安装锁定的 Mermaid CLI、Puppeteer 和 Pagefind；
3. 清理专用临时目录和 `site/`；
4. 逐章生成 HTML 与 SVG；
5. 复制版本化静态资源；
6. 生成 Pagefind 索引；
7. 验证页面数、链接、fragment、图表数、搜索和外部资源；
8. 只有全部检查通过才替换现有 `site/`。

与 PDF 一样，Web 先在临时目录完成。失败构建不得留下半成品 `site/` 或覆盖上一份通过
检查的站点。

预览入口为：

```bash
docs/web/serve.sh
```

它使用本机可用的静态 HTTP server 服务 `site/`，默认绑定回环地址，并在端口占用时给出
明确错误。不要要求读者直接以 `file://` 打开 HTML，因为搜索和干净 URL 需要 HTTP 语义。

## 11. GitHub Pages 发布

`.github/workflows/pages.yml` 使用 GitHub Pages 自定义工作流，在以下条件运行：

- `main` 分支中书稿、参考文献、Web 构建资产或共享 manifest 变化；
- 手动 `workflow_dispatch`。

工作流不初始化七个源码子模块。它使用最小权限：读取仓库内容、写入 Pages、签发部署所需
的 OIDC token。依赖和 Actions 主版本固定，Node 依赖通过 `npm ci` 安装。构建完成后
上传 `site/` artifact 并部署。

工作流设置 Pages deployment environment 和并发组。同一分支的新构建可以取消旧的未完成
构建，但正在发布的生产部署不应被不完整产物替换。Pull Request 只执行构建与验证，不发布；
如仓库策略不运行来自 Fork 的完整浏览器步骤，仍应运行不需要凭据的结构检查。

工作流产物与本地 `docs/web/build.sh` 输出结构一致。不得在 CI 中维护另一套转换命令。

## 12. 构建错误与质量门禁

以下情况必须让构建失败：

- 章节不是正好 36 个，或顺序/前缀不符合 manifest；
- 某章缺少唯一 H1；
- Mermaid 缺图注、编号重复或 SVG 生成失败；
- SVG ID 重复、flowchart 仍含 `foreignObject` 标签或长边标签未完成统一断行；
- 表号、图号或站内交叉引用无法解析；
- 任一站内文件链接或 fragment 不存在；
- Pandoc、citeproc 或 Lua filter 报错；
- Pagefind 索引缺失或页面数不符；
- 页面仍引用构建临时目录、绝对本地路径或未允许的外部资源；
- `site/` 中出现源码、凭据、日志或未计划的大文件。

错误信息需要包含章节文件、目标 URL 或图表编号。Web 构建日志位于专用临时目录；成功后
输出站点目录、页面数、图表数、表格数和搜索索引统计。

## 13. 验证策略

结构验证包括：

- 36 个页面符合预期映射，其中 `00_index.md` 生成根首页，其余 35 章生成章节页面；
- 全书目录顺序与 PDF 一致；
- 35 张 Mermaid 图和 75 张表保持当前基线，内容变化时由明确修改更新基线；
- 所有相对链接和 fragment 可解析；
- 每页只有一个主内容区域和一个 H1；
- 页面除官方 Google Fonts 外没有外部运行资源、搜索或分析请求。

浏览器验证使用 Playwright 或仓库现有可用浏览器自动化，覆盖：

- 桌面和移动视口；
- 浅色、深色和系统默认主题；
- 左侧目录、右侧目录、前后章链接；
- 中文搜索、键盘操作和命中跳转；
- 表格横向滚动、长代码块、长标题和复杂 Mermaid 图；
- 直接访问深层章节 URL和刷新；
- GitHub Pages 项目子路径部署。

视觉抽查至少包括封面/序章、目录密集章节、复杂表格页、复杂 Mermaid 图、四类提示框、
参考文献和移动端长页面。浏览器中使用 `document.fonts.check()` 与计算样式确认 Noto SC
字体生效，并检查字体失败回退、正文遮挡、裁切、横向页面溢出和主题切换闪烁。

实现共享 manifest 或公共转换逻辑后，必须重新运行 `docs/book/build.sh`，检查 PDF 构建
退出状态、页数和代表性页面，防止 Web 功能改变已验证的 PDF。

## 14. 可访问性与基础性能

站点采用语义化 `<nav>`、`<main>`、`<aside>`、`<figure>` 和标题层级。所有交互可用键盘
操作，焦点样式清晰；抽屉和搜索面板管理焦点并具有可访问名称。图注作为图的文本说明，
装饰性图标不重复朗读。

不引入前端框架、客户端 Markdown、运行时 Mermaid 或远程搜索。JavaScript 关闭时，正文、
目录、站内链接、图表和前后章仍可阅读；只有搜索、抽屉增强和主题记忆降级。大型字体设置
由 Google Fonts 分片缓存，其他静态资源使用内容版本标识。实现阶段记录代表页面的资源大小
和首次加载数据，避免站点自身资产无界增长。

## 15. 文档更新

实现完成后需要更新：

- 根目录 `README.md`：增加本地 Web 构建、预览和 Pages 地址；
- `CONTRIBUTING.md`：增加 Web 改动的验证要求；
- `docs/book/README.md`：说明 PDF 与 Web 共用的内容和 manifest；
- `docs/web/README.md`：记录依赖、命令、输出、部署与故障排查。

正式章节不增加仅供网站使用的导航文本。网站导航完全由构建器生成。

## 16. 实施顺序

实施分为四个可单独验证的阶段：

1. 建立共享章节 manifest、HTML 转换和静态页面骨架；
2. 完成字体、视觉主题、响应式导航和图表/表格语义；
3. 集成 Pagefind、链接门禁和浏览器验证；
4. 增加 GitHub Pages workflow，更新项目文档并执行 PDF 回归。

每个阶段都保持本地构建入口可运行。GitHub Pages 发布只在本地完整构建和浏览器验证通过后
启用。

## 17. 实现参考

- Pandoc HTML、模板、目录和标识符：<https://pandoc.org/MANUAL.html>
- Pagefind 多语言与中文搜索：<https://pagefind.app/docs/multilingual/>
- GitHub Pages 自定义工作流：<https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>
- Google Fonts CSS2 API：<https://developers.google.com/fonts/docs/css2>
- Cloudflare Fonts：<https://developers.cloudflare.com/speed/optimization/content/fonts/>

实现阶段应锁定并记录实际使用的工具和字体版本；这里的链接说明选型来源，不替代版本锁定。
