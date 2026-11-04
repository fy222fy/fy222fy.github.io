# fy222fy.github.io

冯皓楠（Haonan Feng）的个人学术主页：<https://fy222fy.github.io>

网站用 [Jekyll](https://jekyllrb.com/) 构建，提供英文（默认）和中文两个版本，推送到 `main` 分支后由 GitHub Actions 自动构建并发布。

## 内容放在哪里

| 要改的内容         | 文件                                                                            |
| ------------------ | ------------------------------------------------------------------------------- |
| 首页               | `_data/<语言>/home.yml`、`_pages/<语言>/about.md`                               |
| 论文、专利、软著   | `_bibliography/papers.bib`                                                      |
| 报告与著作         | `_data/<语言>/talks.yml`                                                        |
| 项目               | `_data/<语言>/projects.yml`                                                     |
| 开源仓库           | `_data/<语言>/repositories.yml`                                                 |
| 简历               | `assets/json/resume_<语言>.json`（[JSON Resume](https://jsonresume.org/) 格式） |
| 动态               | `_news/<语言>/`                                                                 |
| 博客               | `_posts/zh-cn/`，配图放在 `assets/posts/`                                       |
| 界面文字（导航等） | `_data/<语言>/strings.yml`                                                      |
| 站点设置           | `_config.yml`                                                                   |
| 照片               | `assets/img/prof_pic.jpg`                                                       |

`<语言>` 是 `en-us` 或 `zh-cn`，两个版本要同步修改。页面模板在 `_layouts/` 和 `_includes/`，样式在 `_sass/`。

## 本地预览

需要 Ruby 3.3 和 Bundler，以及 ImageMagick（`convert` 命令，用于生成照片的 webp 版本）。

```bash
bundle install
bundle exec jekyll serve
```

然后打开 <http://localhost:4000>。如果构建时报 `invalid byte sequence in US-ASCII`，先设置 UTF-8 环境：`export LANG=C.UTF-8 LC_ALL=C.UTF-8`。

## 检查与工具

| 脚本                          | 用途                                                 |
| ----------------------------- | ---------------------------------------------------- |
| `bin/check-site-links.sh`     | 检查站内链接和页内锚点（离线）；发布前 CI 会自动运行 |
| `bin/check-external-links.sh` | 检查外部链接是否还能打开（联网，手动运行）           |
| `bin/build-fonts.py`          | 重新生成自托管字体；只在升级字体或修改切分方式时需要 |

代码格式用 [Prettier](https://prettier.io/) 统一，CI 会检查：`npx prettier . --check`。

`docs/redesign/` 是改版的设计记录，不参与网站构建。

## 许可

网站代码最初基于 [al-folio](https://github.com/alshedivat/al-folio) 主题，按 MIT 许可发布，见 [LICENSE](LICENSE)。字体使用 SIL Open Font License，见 `assets/fonts/OFL-*.txt`。
