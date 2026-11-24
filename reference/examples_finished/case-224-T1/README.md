# 3D Summer House - Pure CSS

来源：https://codepen.io/ricardoolivaalonso/pen/BazMqJx

当前状态（2026-11-17）：**input 已由用户确认；采分点 manual_v1 草稿待用户确认，未可执行化、未评分。**

| 职责 | 文件 |
|---|---|
| 当前输入 | [input.json](input.json) |
| 当前标答 | [ground_truth.html](ground_truth.html)，= source.html 删去 CodePen `stopExecutionOnTimeout` 外链脚本一行，5 个视口逐像素一致 |
| 源码审核与逐句取舍 | [review_20261117_draft/review.md](review_20261117_draft/review.md) |
| 当前采分点 | [rules_drafts/manual_v1/eval_rules.json](rules_drafts/manual_v1/eval_rules.json)，11 Requirement / 68 Evidence；人可读版 [review.md](rules_drafts/manual_v1/review.md) |
| 渲染证据 | [review_20261117_draft/probe/](review_20261117_draft/probe/) |

original_srcdoc.html为完整抓取原文，source_original.html沿用既有入库范式（仅移除CodePen console shim）。source.html仅删除视角随指针变化、3处过渡与未引用关键帧；全部3D建模及原作隐藏灯光代码保留。灯光控件原CSS为display:none，不新增可点击界面。source_annotated.html为带中文注释的阅读版，不参与出题。
