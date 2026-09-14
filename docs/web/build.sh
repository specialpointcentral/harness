#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SITE_ROOT="${HARNESS_WEB_SITE_DIR:-$REPO_ROOT/site}"
BUILD_DIR="${HARNESS_WEB_BUILD_DIR:-${TMPDIR:-/tmp}/harness-web-build}"
STAGED_SITE="$BUILD_DIR/site"
WORK_ROOT="$BUILD_DIR/work"
PDF_SOURCE="$REPO_ROOT/Agent-Harness-架构工程与安全.pdf"
REPOSITORY_URL="${HARNESS_WEB_REPOSITORY_URL:-https://github.com/specialpointcentral/harness}"

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "缺少命令 '$1'。请参照 docs/web/README.md 安装依赖。"
}

find_chrome_headless_shell() {
  local candidate cache_dir
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
  for cache_dir in "${PUPPETEER_CACHE_DIR:-}" "$HOME/.cache/puppeteer" "$HOME/Library/Caches/puppeteer"; do
    [[ -n "$cache_dir" && -d "$cache_dir" ]] || continue
    candidate="$(find "$cache_dir" -type f -name chrome-headless-shell -perm -u+x 2>/dev/null | sort | tail -n 1)"
    if [[ -n "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  done
  return 1
}

for command in python3 pandoc node npm; do
  require_command "$command"
done

case "$BUILD_DIR" in
  /|.|"$HOME"|"$REPO_ROOT"|"$SITE_ROOT")
    fail "拒绝把危险路径用作临时构建目录：$BUILD_DIR"
    ;;
esac
case "$SITE_ROOT" in
  /|.|"$HOME"|"$REPO_ROOT")
    fail "拒绝把危险路径用作站点目录：$SITE_ROOT"
    ;;
esac

PUPPETEER_SKIP_DOWNLOAD=true npm ci --ignore-scripts --prefix "$SCRIPT_DIR"
export PATH="$SCRIPT_DIR/node_modules/.bin:$PATH"

if ! chrome_path="$(find_chrome_headless_shell)"; then
  "$SCRIPT_DIR/node_modules/.bin/puppeteer" browsers install chrome-headless-shell
  chrome_path="$(find_chrome_headless_shell)" || fail "Puppeteer 安装完成，但仍找不到 chrome-headless-shell。"
fi
export PUPPETEER_EXECUTABLE_PATH="$chrome_path"

rm -rf "$BUILD_DIR"
mkdir -p "$STAGED_SITE" "$WORK_ROOT"

prepare_args=(
  --repo-root "$REPO_ROOT"
  --site-root "$STAGED_SITE"
  --work-root "$WORK_ROOT"
  --repository-url "$REPOSITORY_URL"
)
if [[ -s "$PDF_SOURCE" ]]; then
  prepare_args+=(--pdf-source "$PDF_SOURCE")
fi

python3 "$SCRIPT_DIR/prepare.py" "${prepare_args[@]}"
pagefind --site "$STAGED_SITE" --output-subdir pagefind
python3 "$SCRIPT_DIR/verify.py" "$STAGED_SITE" \
  --pages 36 --figures 35 --tables 75 --require-search

site_backup="${SITE_ROOT}.previous"
rm -rf "$site_backup"
if [[ -e "$SITE_ROOT" ]]; then
  mv "$SITE_ROOT" "$site_backup"
fi
if mv "$STAGED_SITE" "$SITE_ROOT"; then
  rm -rf "$site_backup"
else
  if [[ -e "$site_backup" ]]; then
    mv "$site_backup" "$SITE_ROOT"
  fi
  fail "无法替换站点目录：$SITE_ROOT"
fi

printf 'Built web edition: %s\n' "$SITE_ROOT"
printf 'Preview: docs/web/serve.sh\n'
