# 文字问题待办（下一阶段处理）

本阶段只处理前端展示。下面这些文字不是你本人写的或需要你确认，下一阶段逐条处理。
处理原则：有你原稿的恢复原稿；没有原稿的先由你提供或确认，不再由我自行改写、翻译。

## A. 我自己写或翻译的文字（你没看过，需确认或替换）

- [ ] 中文简历全部内容：`assets/json/resume_zh-cn.json`（`dev` 上有你的原稿，可恢复后再补充）
- [ ] 项目页中文版：`_data/zh-cn/projects.yml`（由英文设计稿翻译而来）
- [ ] 首页中文措辞（在设计稿基础上改写）：`_data/zh-cn/home.yml` 的亮点 `facts`、时间线 `timeline`
- [ ] 各页标题下的一句导语：`_data/*/strings.yml` 中 `publications.lead`、`blog.lead`、`news.lead`、`repositories.lead`、`cv.lead`
- [ ] 开源页两个仓库的简介：`_data/*/repositories.yml`
- [ ] 首页新增小标题“关于我 / About Me”：`_data/*/home.yml` 的 `about.title`
- [ ] 中文简历页标题下的描述（来自简历 JSON 的 `basics.label`）

## B. 来自设计稿的文字（你说过已确认，留意即可）

- 首页：研究方向三栏、亮点数字、重点项目摘要、动态措辞（`_news/*`）
- 论文信息：标题大小写、`where` 出处字段（`_bibliography/papers.bib`）
- 英文简历：`assets/json/resume_en-us.json`
- 项目页英文版：`_data/en-us/projects.yml`

## C. 需要你决定的内容出入

- [ ] 研究方向不一致：你的简介写“大模型安全、形式化分析、**隐私计算**”，设计稿三栏是“大模型安全、大模型 for 安全、形式化分析”。两者现在同时显示在首页。
- [ ] 英文简介原文里有一处 `\*_TDSC 2023_`，显示为多一个星号的斜体，是否改成 **TDSC 2023**。
- [ ] 中文简历里 CCS 2025 合作者 Haotian Li、Chi Ma、Junchi Zeng 的中文名。
- [ ] 旧简历 PDF（`assets/pdf/*/my_cv.pdf`）含手机号等信息，仍在线上可访问；新版已不再发布 `assets/pdf/`，是否同时从 `main` 删除。

## D. 已处理

- [x] 首页个人简介恢复为 `dev` 上的原文（`_pages/*/about.md`），逐字一致，只改了展示方式。
