#!/usr/bin/env bash
# 站内链接检查（离线，不访问网络）
#
# 检查构建好的网站里所有站内链接是否有效：页面、图片、PDF、样式/脚本文件，
# 以及页内锚点（如 /cv/#教育）。写成完整网址 https://fy222fy.github.io/... 的链接
# 也会映射到本地文件一起检查。外部网站的链接不在这里检查，见 bin/check-external-links.sh。
#
# CI 在每次推送和 PR 时自动运行（.github/workflows/deploy.yml），检查失败则不发布。
#
# 本地用法：
#   bundle exec jekyll build
#   bin/check-site-links.sh            # 默认检查 _site
#   bin/check-site-links.sh path/to/site
#
# 依赖 lychee >= 0.18（需要 --root-dir 参数）：
#   macOS: brew install lychee
#   其他:  https://github.com/lycheeverse/lychee/releases
# 也可以用环境变量 LYCHEE 指定 lychee 可执行文件路径。
set -euo pipefail

SITE_DIR="${1:-_site}"
SITE_URL="https://fy222fy.github.io"
LYCHEE="${LYCHEE:-lychee}"

if ! command -v "$LYCHEE" >/dev/null 2>&1; then
  echo "未找到 lychee，请先安装：macOS 用 'brew install lychee'，其他系统见 https://github.com/lycheeverse/lychee/releases" >&2
  exit 2
fi

if [ ! -d "$SITE_DIR" ]; then
  echo "找不到 $SITE_DIR，请先构建网站：bundle exec jekyll build" >&2
  exit 2
fi

ROOT="$(cd "$SITE_DIR" && pwd)"

"$LYCHEE" \
  --offline \
  --include-fragments \
  --no-progress \
  --root-dir "$ROOT" \
  --remap "^${SITE_URL//./\\.}/(.*)\$ file://$ROOT/\$1" \
  "$ROOT/**/*.html"
