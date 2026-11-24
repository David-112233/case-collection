# CSS leaning card effect

来源：https://codepen.io/lynnandtonic/pen/dyGjvLB

当前版本为 **v1**：input 由用户定稿，规则经用户确认（2026-11-17）。已在 R02 完成评测：本轮得分 DeepSeek-V4-Pro 1.5（含用户确认的 1 条复核改判）、Qwen3.8-max 2.5，Kimi-K3 生成失败未评测，见 [评测报告](../../evaluations/R02_20261117_static-v3/cases/case-227-T1/评测报告.md)。未经独立 Review 或用户验收。

| 职责 | 当前文件 |
|---|---|
| 当前输入 | [input.json](input.json) |
| 当前标答 | [ground_truth.html](ground_truth.html)：由 source.html 复制，仅删除 CodePen 外部脚本、外链 reset 样式表改为内联原文；6 个视口截图与 source 逐像素一致 |
| 采分点 | [manual_v1/eval_rules.json](rules_drafts/manual_v1/eval_rules.json)；人可读版 [review.md](rules_drafts/manual_v1/review.md)：7 Requirement / 72 mandatory，用户已确认；R02 副本与此逐字节相同 |
| 源码审核与 input 逐句取舍 | [review_20261117_draft/review.md](review_20261117_draft/review.md) |
| 来源 | original_srcdoc.html 为完整抓取原文；source_original.html 仅移除 CodePen console shim；source.html 与之逐字节相同，未修改 |
| 通用政策 | [输出契约 v2](../../docs/output_contract_v2.md) |

页面内容：上方 4 张原图悬浮展示，下方同样 4 张海报斜靠在墙角，带多层投影、光泽、厚度边和向右后方的纵深。准静态，无动画、无交互；仅桌面宽屏。
