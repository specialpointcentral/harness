#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SITE_ROOT="${HARNESS_WEB_SITE_DIR:-$REPO_ROOT/site}"
PORT="${1:-8000}"

[[ -f "$SITE_ROOT/index.html" ]] || {
  printf 'error: 未找到已构建站点：%s\n' "$SITE_ROOT" >&2
  printf '请先运行 docs/web/build.sh。\n' >&2
  exit 1
}
[[ "$PORT" =~ ^[0-9]+$ ]] || {
  printf 'error: 端口必须是整数：%s\n' "$PORT" >&2
  exit 1
}

printf 'Serving %s at http://127.0.0.1:%s/\n' "$SITE_ROOT" "$PORT"
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$SITE_ROOT"
