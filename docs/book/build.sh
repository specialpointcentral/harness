#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SURVEY_DIR="$REPO_ROOT/docs/harness-survey"
BUILD_DIR="${HARNESS_BOOK_BUILD_DIR:-${TMPDIR:-/tmp}/harness-book-build}"
FONT_BUILD_DIR="/tmp/harness-book-fonts-${UID:-$(id -u)}"
OUTPUT="$REPO_ROOT/Agent-Harness-架构工程与安全.pdf"
STAGED_OUTPUT="$BUILD_DIR/Agent-Harness-架构工程与安全.pdf"
LOG="$BUILD_DIR/build.log"

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "缺少命令 '$1'。请参照 docs/book/README.md 安装依赖。"
}

find_chrome_headless_shell() {
  local candidate

  if [[ -n "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
    [[ -x "$PUPPETEER_EXECUTABLE_PATH" ]] || fail "PUPPETEER_EXECUTABLE_PATH 不可执行：$PUPPETEER_EXECUTABLE_PATH"
    printf '%s\n' "$PUPPETEER_EXECUTABLE_PATH"
    return
  fi

  for candidate in chrome-headless-shell google-chrome-headless-shell; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return
    fi
  done

  local cache_dir
  for cache_dir in \
    "${PUPPETEER_CACHE_DIR:-}" \
    "$HOME/.cache/puppeteer" \
    "$HOME/Library/Caches/puppeteer"; do
    [[ -n "$cache_dir" && -d "$cache_dir" ]] || continue
    candidate="$(find "$cache_dir" -type f -name chrome-headless-shell -perm -u+x 2>/dev/null | sort | tail -n 1)"
    if [[ -n "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done

  fail "未找到 Puppeteer 的 chrome-headless-shell。请运行 'npx puppeteer browsers install chrome-headless-shell'。"
}

check_tex_packages() {
  local package
  for package in tcolorbox.sty needspace.sty ragged2e.sty enumitem.sty etoolbox.sty caption.sty newunicodechar.sty chngcntr.sty; do
    kpsewhich "$package" >/dev/null 2>&1 || fail "MacTeX 缺少 LaTeX 包：$package"
  done
}

find_font_file() {
  local filename="$1"
  local candidate
  for candidate in \
    "$HOME/Library/Fonts/$filename" \
    "/Library/Fonts/$filename" \
    /opt/homebrew/Caskroom/font-source-han-*-vf/*/"$filename" \
    /usr/local/Caskroom/font-source-han-*-vf/*/"$filename"; do
    if [[ -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  fail "找不到字体文件 $filename。请安装 README 中的思源 VF 字体 cask。"
}

check_extracted_fonts() {
  cat > "$BUILD_DIR/font-check.tex" <<'EOF'
\documentclass{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont[Path=FONT_DIR/,Extension=.otf,BoldFont=SourceHanSerifSC-Bold]{SourceHanSerifSC-Regular}
\setsansfont[Path=FONT_DIR/,Extension=.otf,BoldFont=SourceHanSansSC-Bold]{SourceHanSansSC-Regular}
\setCJKmainfont[Path=FONT_DIR/,Extension=.otf,BoldFont=SourceHanSerifSC-Bold]{SourceHanSerifSC-Regular}
\setCJKsansfont[Path=FONT_DIR/,Extension=.otf,BoldFont=SourceHanSansSC-Bold]{SourceHanSansSC-Regular}
\begin{document}
思源宋体 \textbf{粗体} \textsf{思源黑体 \textbf{粗体}}
\end{document}
EOF
  sed -i.bak "s|FONT_DIR|$FONT_BUILD_DIR|g" "$BUILD_DIR/font-check.tex"

  if ! xelatex -interaction=batchmode -halt-on-error -output-directory="$BUILD_DIR" "$BUILD_DIR/font-check.tex" >/dev/null 2>&1; then
    printf '%s\n' "error: XeLaTeX 无法加载临时生成的思源 SC 静态字体。" >&2
    tail -n 30 "$BUILD_DIR/font-check.log" >&2 || true
    exit 1
  fi
}

for command in python3 pandoc xelatex kpsewhich mmdc fonttools; do
  require_command "$command"
done

[[ -d "$SURVEY_DIR" ]] || fail "找不到章节目录：$SURVEY_DIR"
[[ -f "$SURVEY_DIR/references.bib" ]] || fail "找不到参考文献：$SURVEY_DIR/references.bib"
case "$BUILD_DIR" in
  /|.|"$HOME"|"$REPO_ROOT"|"$SURVEY_DIR")
    fail "拒绝把危险路径用作临时构建目录：$BUILD_DIR"
    ;;
esac

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

check_tex_packages
FONTTOOLS_PYTHON="$(sed -n '1s/^#!//p' "$(command -v fonttools)")"
[[ -x "$FONTTOOLS_PYTHON" ]] || fail "无法确定 fonttools 使用的 Python 解释器。请重新运行 'brew install fonttools'。"
"$FONTTOOLS_PYTHON" -c 'import fontTools' >/dev/null 2>&1 || fail "fonttools 安装不完整。请重新运行 'brew install fonttools'。"
SERIF_TTC="$(find_font_file SourceHanSerif-VF.otf.ttc)"
SANS_TTC="$(find_font_file SourceHanSans-VF.otf.ttc)"
"$FONTTOOLS_PYTHON" "$SCRIPT_DIR/prepare-fonts.py" \
  --serif "$SERIF_TTC" \
  --sans "$SANS_TTC" \
  --output-dir "$FONT_BUILD_DIR" \
  --metadata "$BUILD_DIR/font-metadata.json"
check_extracted_fonts
export PUPPETEER_EXECUTABLE_PATH="$(find_chrome_headless_shell)"

printf 'Build directory: %s\n' "$BUILD_DIR"
printf 'Chrome headless shell: %s\n' "$PUPPETEER_EXECUTABLE_PATH"

HARNESS_REPO_ROOT="$REPO_ROOT" HARNESS_BOOK_BUILD_DIR="$BUILD_DIR" \
  python3 "$SCRIPT_DIR/prepare.py"

set +e
pandoc "$BUILD_DIR/book.md" \
  --from='markdown+smart+pipe_tables+fenced_code_blocks+implicit_figures+raw_tex+link_attributes+header_attributes+auto_identifiers' \
  --to=latex \
  --template="$SCRIPT_DIR/template/eisvogel.latex" \
  --pdf-engine=xelatex \
  --pdf-engine-opt=-halt-on-error \
  --pdf-engine-opt=-file-line-error \
  --lua-filter="$SCRIPT_DIR/book-filter.lua" \
  --include-in-header="$SCRIPT_DIR/header.tex" \
  --citeproc \
  --bibliography="$SURVEY_DIR/references.bib" \
  --metadata-file="$SCRIPT_DIR/title-page.yaml" \
  --metadata-file="$SCRIPT_DIR/metadata.yaml" \
  --metadata-file="$BUILD_DIR/font-metadata.json" \
  --resource-path="$BUILD_DIR:$SURVEY_DIR" \
  --toc --toc-depth=2 \
  --top-level-division=chapter \
  -o "$STAGED_OUTPUT" 2>&1 | tee "$LOG"
pandoc_status=${PIPESTATUS[0]}
set -e

[[ "$pandoc_status" -eq 0 ]] || fail "Pandoc/XeLaTeX 构建失败；完整日志见 $LOG"
[[ -s "$STAGED_OUTPUT" ]] || fail "构建命令成功，但临时 PDF 不存在或为空：$STAGED_OUTPUT"

if grep -Eq 'Hyper reference.*undefined|There were undefined references|Citation.*undefined|Float too large' "$LOG"; then
  fail "PDF 已生成，但检测到未定义内链、引用或超出版心的浮动体；请检查 $LOG"
fi

mv "$STAGED_OUTPUT" "$OUTPUT"
printf 'Built: %s\n' "$OUTPUT"
ls -lh "$OUTPUT"
