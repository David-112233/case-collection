# 参考资料同步记录

同步日期：2026-11-24　方向：主仓库 → 本仓库，单向。**只有 Claude 在本地同步；云端智能体不得修改 `reference/`。**
主仓库文件后来有更新时，这里不会自动变，以主仓库为准；发现与任务矛盾的地方，写进备注并告诉用户，不要自行改口径。

| 主仓库路径 | 本仓库路径 | 源文件 SHA-256（前 16 位） | 说明 |
|---|---|---|---|
| `docs/output_contract_v2.md` | `reference/docs/output_contract_v2.md` | `5a55237d5b42bd7c` | 链接保留 2，主仓库专有文件的链接已改为纯文字 2 |
| `docs/scoring_rubric_v6.md` | `reference/docs/scoring_rubric_v6.md` | `7affa039ddefbdff` | 链接保留 3，主仓库专有文件的链接已改为纯文字 0 |
| `docs/evaluation_pipeline_v6.md` | `reference/docs/evaluation_pipeline_v6.md` | `bd785b3c76dc4225` | 链接保留 3，主仓库专有文件的链接已改为纯文字 4 |
| `docs/difficulty_model_v2_1.md` | `reference/docs/difficulty_model_v2_1.md` | `bd97fb0e20194152` | 链接保留 2，主仓库专有文件的链接已改为纯文字 1 |
| `TASK_DEFINITION_v5_2_synced.md` | `reference/docs/TASK_DEFINITION_v5_2_synced.md` | `cf3e0a54f68e138a` | 链接保留 4，主仓库专有文件的链接已改为纯文字 2 |
| `project_state/DECISIONS.md` | `reference/docs/DECISIONS.md` | `0b1d729c08d72e2f` | 链接保留 2，主仓库专有文件的链接已改为纯文字 18 |
| `.agents/skills/input-sharpening/SKILL.md` | `reference/skills/input-sharpening/SKILL.md` | `7d8010051729fe5a` | 链接保留 4，主仓库专有文件的链接已改为纯文字 6 |
| `.agents/skills/input-sharpening/scroll_trace_probe.py` | `reference/skills/input-sharpening/scroll_trace_probe.py` | `49147f8a60de2886` | 原样复制 |
| `.agents/skills/eval-rules-refinement/SKILL.md` | `reference/skills/eval-rules-refinement/SKILL.md` | `5d39290368b1a8e4` | 链接保留 6，主仓库专有文件的链接已改为纯文字 3 |
| `.agents/skills/eval-rules-refinement/references/semantic-review.md` | `reference/skills/eval-rules-refinement/references/semantic-review.md` | `45bc3cf576977aaa` | 链接保留 1，主仓库专有文件的链接已改为纯文字 11 |
| `.agents/skills/eval-rules-refinement/references/scroll-and-capability-review.md` | `reference/skills/eval-rules-refinement/references/scroll-and-capability-review.md` | `3fb7b6a681583e27` | 链接保留 1，主仓库专有文件的链接已改为纯文字 10 |
| `scripts/eval_rules_generation/preparation/output_contract_v2.json` | `reference/schemas/output_contract_v2.json` | `996d65a6ee14bba1` | 原样复制 |
| `scripts/eval_rules_generation/preparation/evaluation_policy_v2.json` | `reference/schemas/evaluation_policy_v2.json` | `510132ae8bd165f1` | 原样复制 |
| `scripts/eval_rules_generation/preparation/severity_anchors_v1_1.json` | `reference/schemas/severity_anchors_v1_1.json` | `51a76331102f44ac` | 原样复制 |
| `cases/case-217-T1/ground_truth.html` | `reference/examples_finished/case-217-T1/ground_truth.html` | `6f1583604e7fd6ad` | 原样复制（完成态样板） |
| `cases/case-217-T1/input.json` | `reference/examples_finished/case-217-T1/input.json` | `d78afc395ad0201a` | 原样复制（完成态样板） |
| `cases/case-217-T1/rules_drafts/manual_v3/eval_rules.json` | `reference/examples_finished/case-217-T1/rules_drafts/manual_v3/eval_rules.json` | `c8cb6c66955dd64e` | 原样复制（完成态样板） |
| `cases/case-217-T1/rules_drafts/manual_v3/review.md` | `reference/examples_finished/case-217-T1/rules_drafts/manual_v3/review.md` | `c48bcf0a756bc23a` | 原样复制（完成态样板） |
| `cases/case-221-T1/ground_truth.html` | `reference/examples_finished/case-221-T1/ground_truth.html` | `e7ab090520448369` | 原样复制（完成态样板） |
| `cases/case-221-T1/input.json` | `reference/examples_finished/case-221-T1/input.json` | `bee4cbeb4b9b6ff0` | 原样复制（完成态样板） |
| `cases/case-221-T1/rules_drafts/manual_v1/eval_rules.json` | `reference/examples_finished/case-221-T1/rules_drafts/manual_v1/eval_rules.json` | `f0619eb216f73198` | 原样复制（完成态样板） |
| `cases/case-221-T1/rules_drafts/manual_v1/review.md` | `reference/examples_finished/case-221-T1/rules_drafts/manual_v1/review.md` | `33ddad50402b3848` | 原样复制（完成态样板） |
| `cases/case-222-T2/ground_truth.html` | `reference/examples_finished/case-222-T2/ground_truth.html` | `1f827dbb37b986a4` | 原样复制（完成态样板） |
| `cases/case-222-T2/input.json` | `reference/examples_finished/case-222-T2/input.json` | `6afe8fab7796db5f` | 原样复制（完成态样板） |
| `cases/case-222-T2/rules_drafts/manual_v1/eval_rules.json` | `reference/examples_finished/case-222-T2/rules_drafts/manual_v1/eval_rules.json` | `df2c5f1ecf9518ad` | 原样复制（完成态样板） |
| `cases/case-222-T2/rules_drafts/manual_v1/review.md` | `reference/examples_finished/case-222-T2/rules_drafts/manual_v1/review.md` | `00ffd27442afc0cb` | 原样复制（完成态样板） |
| `cases/case-222-T2/rules_drafts/manual_v1/gt_selfcheck.py` | `reference/examples_finished/case-222-T2/rules_drafts/manual_v1/gt_selfcheck.py` | `9525db5dcb41da5a` | 原样复制（完成态样板） |
| `cases/case-222-T2/rules_drafts/manual_v1/gt_selfcheck_results.txt` | `reference/examples_finished/case-222-T2/rules_drafts/manual_v1/gt_selfcheck_results.txt` | `b5af395c9180a1cd` | 原样复制（完成态样板） |
| `cases/case-227-T1/ground_truth.html` | `reference/examples_finished/case-227-T1/ground_truth.html` | `3d76d1a5e533d987` | 原样复制（完成态样板） |
| `cases/case-227-T1/input.json` | `reference/examples_finished/case-227-T1/input.json` | `8aaa972efd799f71` | 原样复制（完成态样板） |
| `cases/case-227-T1/rules_drafts/manual_v1/eval_rules.json` | `reference/examples_finished/case-227-T1/rules_drafts/manual_v1/eval_rules.json` | `3d6a5fcf8cc99a7a` | 原样复制（完成态样板） |
| `cases/case-227-T1/rules_drafts/manual_v1/review.md` | `reference/examples_finished/case-227-T1/rules_drafts/manual_v1/review.md` | `52007a25d0b3b570` | 原样复制（完成态样板） |
| `cases/case-227-T1/rules_drafts/manual_v1/gt_selfcheck.py` | `reference/examples_finished/case-227-T1/rules_drafts/manual_v1/gt_selfcheck.py` | `76ebb9cf1bc0fcde` | 原样复制（完成态样板） |

`dedupe_index.csv`：主仓库 `cases/` 全部 227 例的编号、档位、来源链接，供去重；其中 192 例有 CodePen 来源链接。
`history/`：采集初期的旧快照（旧任务定义、旧决策、旧扩量方案、旧案例目录），只供追溯，**口径已过期**（例如当时禁止 JavaScript，2026-11-16 起已放开，见 `docs/output_contract_v2.md`）。
