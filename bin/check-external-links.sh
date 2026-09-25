#!/usr/bin/env bash
# 外部链接检查（需要联网，只手动运行，没有任何自动触发）
#
# 检查构建好的网站里所有指向外部网站的链接和图片是否还能打开，包括论文的
# DOI/PDF、博客里的参考链接、CDN 上的样式脚本，以及仓库页面的统计卡片
# （github-readme-stats）。结果写入 link-report.md。
#
# 外部网站的状态随时变化，所以这里的报错不一定是你的问题；检查结果只作参考，
# 看报告决定要不要修。
#
# 用法：
#   bundle exec jekyll build
#   bin/check-external-links.sh                                   # 检查整个网站
#   bin/check-external-links.sh _site/blog/2024/llm-fintune/index.html   # 只检查某个页面
#
# 依赖 lychee：macOS 用 'brew install lychee'，其他系统见
# https://github.com/lycheeverse/lychee/releases 。也可以用环境变量 LYCHEE 指定路径。
set -euo pipefail

LYCHEE="${LYCHEE:-lychee}"
REPORT="link-report.md"

if ! command -v "$LYCHEE" >/dev/null 2>&1; then
  echo "未找到 lychee，请先安装：macOS 用 'brew install lychee'，其他系统见 https://github.com/lycheeverse/lychee/releases" >&2
  exit 2
fi

if [ ! -d _site ]; then
  echo "找不到 _site，请先构建网站：bundle exec jekyll build" >&2
  exit 2
fi
if [ "$#" -eq 0 ]; then
  set -- "_site/**/*.html"
fi

# 403/429：Google Scholar、IEEE 等网站会拦截自动检查工具，浏览器里通常能正常打开，按"可访问"处理。
# 站内链接（fy222fy.github.io）由 bin/check-site-links.sh 离线检查，这里跳过。
# Google Fonts 的域名只用于预连接，直接访问会报错，跳过。
status=0
"$LYCHEE" \
  --no-progress \
  --root-dir "$(cd _site && pwd)" \
  --scheme https \
  --scheme http \
  --accept '200..=299,403,429' \
  --timeout 20 \
  --max-retries 2 \
  --max-concurrency 8 \
  --user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' \
  --exclude '^https?://fy222fy\.github\.io' \
  --exclude '^https://fonts\.(googleapis|gstatic)\.com' \
  --exclude-loopback \
  --format markdown \
  --output "$REPORT" \
  "$@" || status=$?

if [ "$status" -eq 0 ]; then
  echo "所有外部链接都能打开。报告：$REPORT"
else
  echo "有外部链接打不开，详见 $REPORT（外部网站可能只是暂时不可用，可以稍后再跑一次确认）" >&2
fi
exit "$status"
