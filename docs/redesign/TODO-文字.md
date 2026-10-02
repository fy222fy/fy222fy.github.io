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

## C. 暂缓

- [ ] 首页内容重复：蚂蚁集团的三个方向同时出现在“关于我”、“重点项目”和“教育与经历”里（用户决定先不改）。

## D. 已处理

- [x] 研究方向统一为 AI for Security（AI 安全）、形式化分析、隐私计算（简介、首页三栏、时间线、简历、站点描述）。
- [x] 简介去掉“FIDO 相关专利 2 篇”；中英文简介修正语法、用词与中英文空格；期刊统一写 IEEE TDSC。
- [x] 直播条目补年份 2022；信息安全竞赛年份 2018 确认无误（作品为 2017 年）。
- [x] 中文简历中的合作者保留英文名，不再需要中文名。
- [x] 旧简历 PDF 已从仓库删除。

- [x] 首页个人简介恢复为 `dev` 上的原文（`_pages/*/about.md`），逐字一致，只改了展示方式。
