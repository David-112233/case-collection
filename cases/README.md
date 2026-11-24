# cases/ · 正式案例区

已被用户选中的案例在这里加工。**目录名、编号、文件格式与主仓库 `cases/` 完全一致**，加工完成后整个目录原样拷回主仓库。

- 编号从 `case-228` 起连续；编号只在入库时分配，不预留、不跳号。主仓库现有 `case-001`–`227` 的去重信息在 [reference/dedupe_index.csv](../reference/dedupe_index.csv)。
- 总览看 [INDEX.md](INDEX.md)（由台账生成，不要手写）；状态来源是 [registry.csv](registry.csv)。
- 谁写什么见 [AGENTS.md](../AGENTS.md) 第 3、4 节：dot 入库并建目录，duet 加工内容，`user_review` 只有用户能改。

## 一个案例目录里有什么

| 文件 | 谁产生 | 说明 |
|---|---|---|
| `README.md` | 入库时 dot，之后 duet 补 | 来源链接、状态、各文件用途、GT 相对来源的改动点 |
| `classification.json` `metadata.json` | 入库时 dot | 档位与难度特征、来源、哈希、批次 |
| `original_srcdoc.html` | 入库时 dot | 原始捕获，不改 |
| `source.html` `source_original.html` | 入库时 dot | 来源预览与修改前副本，二者内容可能相同，**不要因为相同而删除** |
| `input.json` | duet | 给模型的题目 |
| `ground_truth.html` | duet | 参考答案 |
| `rules_drafts/manual_v1/eval_rules.json` | duet | 规则草稿，附 `review.md` |
| `generation_prompt.txt` | duet | 用 `output_prompt_v2` 生成的 Prompt |
| `input_problem.md` | duet | input 的问题与取舍记录 |
| `review_<YYYYMMDD>/` | duet | GT 自检的截图、测量与脚本 |

## 阶段

`admitted` → `input_draft` → `gt_ready` → `rules_draft` → `ready_for_review`（duet 的终点）→ `frozen`（用户本地确认并冻结后）→ `synced`（已拷回主仓库）。只前进不回退；回退须在 `note` 写明原因。
