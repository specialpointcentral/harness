# Agent Harness 网页版构建

本目录把 `docs/harness-survey/` 中的 36 个编号章节生成为多页面静态网站。构建结果
写入仓库根目录的 `site/`，包括全书目录、页内目录、前后章导航、Mermaid SVG、
引用、深浅主题和 Pagefind 中文全文搜索。

## 环境

需要：

- Python 3；
- Pandoc 3.10.1 或兼容版本；
- Node.js 24 和 npm；
- Puppeteer 支持的 `chrome-headless-shell`。

Node 依赖已锁定在 `package-lock.json`。构建脚本执行 `npm ci`，并在本机没有可用
浏览器时通过 Puppeteer 安装 `chrome-headless-shell`。

网页版通过 Google Fonts CSS2 加载 `Noto Serif SC` 和 `Noto Sans SC` 可变字体，
分别对应 PDF 正文和标题使用的思源宋体、思源黑体视觉体系。Google Fonts 不可用时，
CSS 会回退到本机 Source Han、Noto CJK 或通用 serif/sans-serif，正文仍可阅读。
字体不写入 `site/`，也不进入仓库。

若以后为 GitHub Pages 配置经过 Cloudflare 代理的自定义域名，可以启用 Cloudflare
Fonts，让 Cloudflare 在边缘把 Google Fonts 改写为同域字体请求。默认 `github.io`
域名不属于项目自己的 Cloudflare zone，无法进行这种改写。

## 构建

在仓库根目录运行：

```bash
docs/web/build.sh
```

脚本会：

1. 安装锁定的 Mermaid CLI、Puppeteer 和 Pagefind；
2. 把 Mermaid 图渲染为内联 SVG；
3. 通过 Pandoc、citeproc 和 Web Lua filter 生成 36 个页面；
4. 建立 Pagefind 索引；
5. 验证页面、图表、站内链接和 fragment；
6. 只有全部检查通过才替换仓库根目录的 `site/`。

Mermaid fenced block 始终是 PDF 与网页的唯一图源。网页不会维护第二份图，也没有按图号
配置的 override。Web 渲染器对 flowchart 和 state diagram 统一使用原生 SVG `text/tspan`，
节点换行宽度为 120；超过 18 显示列的连线标签会在临时 `.mmd` 中平衡断行。SVG 生成后，
`postprocess-svg.mjs` 根据相同 `data-id` 把标签关联到自己的路径，在路径上选择最近的
无碰撞位置，并在移动后重新计算 `viewBox`。无法消除标签与标签或标签与节点碰撞时，
构建直接失败。sequence diagram 保持共享主题的原生 SVG 行为。

每张图的固有显示宽高取最终 `viewBox` 的 70%，再由 CSS 限制为正文宽度的 92% 和桌面
视口高度的 72%；窄屏取消高度上限，避免纵向图因压缩而不可读。这与 PDF 的基础缩放、
最大版心宽度和最大正文高度约束采用相同思路。这些 Web 适配不会写回正式章节，也不会
改变 PDF 图。

可使用独立临时目录：

```bash
HARNESS_WEB_BUILD_DIR=/tmp/harness-web-build-local docs/web/build.sh
```

如果浏览器不在 Puppeteer 默认缓存目录，可显式指定：

```bash
PUPPETEER_EXECUTABLE_PATH=/absolute/path/to/chrome-headless-shell docs/web/build.sh
```

在 GitHub Actions 等设置 `CI=true` 的环境中，脚本会自动加载
`puppeteer-ci.json`，为 runner 上的 Chrome 禁用不可用的进程沙箱；本地构建不使用该配置。

如果仓库根目录存在已生成的 `Agent-Harness-架构工程与安全.pdf`，构建器会把它复制到
`site/downloads/`，并显示 PDF 下载按钮。普通本地 Web 构建仍允许缺少 PDF；发布或其他
必须包含下载文件的构建可设置 `HARNESS_WEB_REQUIRE_PDF=true`，此时缺少 PDF、复制失败或
HTML 没有下载链接都会使验证失败。也可用 `HARNESS_WEB_PDF_SOURCE` 指定其他 PDF 路径。

## 本地预览

构建完成后运行：

```bash
docs/web/serve.sh
```

默认地址是 `http://127.0.0.1:8000/`。也可以指定端口：

```bash
docs/web/serve.sh 8080
```

不要直接使用 `file://` 打开 HTML；Pagefind 搜索和目录 URL 需要通过 HTTP 访问。

## GitHub Pages

`.github/workflows/pages.yml` 在 Pull Request 中只构建和验证。在 `main` 分支相关内容
变化或手动触发时，它生成相同的 `site/`、上传 GitHub Pages artifact 并部署。
工作流不会初始化七个源码子模块。

Pull Request 的检查包括精简后的 Web 行为测试、Python 编译、Shell 语法，以及完整
`docs/web/build.sh`。后者会真实生成 36 个 HTML 页面和 35 张 SVG、建立 Pagefind
索引，并验证页面数、图表数、站内链接、fragment、SVG ID 和 flowchart 原生标签。
PR 不执行 artifact 上传或 Pages 部署。`main` 和手动触发使用同一组检查，只有全部通过
后才上传 `site/` 并由独立 deploy job 发布。

仓库首次启用时，需要在 GitHub 的 Pages 设置中把 Source 选择为 GitHub Actions。
使用自定义域名时，先按 GitHub Pages 要求配置域名，再决定是否接入 Cloudflare 代理
和 Cloudflare Fonts。

## 故障排查

- Mermaid 报浏览器错误：检查 `PUPPETEER_EXECUTABLE_PATH`，或重新安装
  `chrome-headless-shell`。
- Pagefind 报中文不支持 stemming：这是提示，不影响精确中文词搜索。
- 验证器报 `broken local target`：检查源 Markdown 的相对章节链接。
- 验证器报 `missing fragment`：检查目标标题和 GitHub/Pandoc slug 差异。
- 验证器报外部运行资源：只允许官方 Google Fonts 两个域名；JavaScript、搜索索引
  和其他样式必须由站点自身提供。
- 构建失败不会覆盖上一份通过检查的 `site/`；中间文件位于指定的临时构建目录。
