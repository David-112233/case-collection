# cases/ · 正式案例区

已被用户选中的案例在这里加工。**目录名、编号、文件格式与主仓库 `cases/` 完全一致**，加工完成后整个目录原样拷回主仓库。

- 编号从 `case-228` 起连续；编号只在入库时分配，不预留、不跳号。主仓库现有 `case-001`–`227` 的去重信息在 [reference/dedupe_index.csv](../reference/dedupe_index.csv)。
- 总览看 [INDEX.md](INDEX.md)（由台账生成，不要手写）；状态来源是 [registry.csv](registry.csv)。
- 谁写什么见 [AGENTS.md](../AGENTS.md) 第 3、4 节：dot 入库并建目录，duet 加工内容，`user_review` 只有用户能改。

## 加工顺序

**来源源码 → 准静态 GT → 由 GT 写出 input → 用户审核 → 规则草稿 → 用户审核 → 本地冻结。** 详细要求见 [AGENTS.md](../AGENTS.md) 第 4 节。

## 一个案例目录里有什么

| 文件 | 谁产生、何时 | 说明 |
|---|---|---|
| `README.md` | 入库时 dot，之后 duet 补 | 来源链接、状态、各文件用途、**GT 相对来源的改动点** |
| `classification.json` `metadata.json` | 入库时 dot | 档位（暂定）与难度特征、来源、哈希、批次 |
| `original_srcdoc.html` | 入库时 dot | 原始捕获，不改 |
| `source.html` `source_original.html` | 入库时 dot | 来源预览与修改前副本，二者内容可能相同，**不要因为相同而删除** |
| `ground_truth.html` | duet，第一步 | 以 `source.html` 为基础改造的**准静态**参考页：尽量尊重源码，无动画，只留简单交互 |
| `review_<YYYYMMDD>/` | duet，随 GT | GT 自检的截图、测量与脚本 |
| `input.json` | duet，第二步，**由 GT 写出** | 给模型的题目 |
| `input_problem.md` | duet | input 的问题与取舍记录 |
| `rules_drafts/manual_v1/eval_rules.json` | duet，**用户通过 input 之后** | 规则草稿，附 `review.md` |
| `generation_prompt.txt` | duet，随规则 | 用 `output_prompt_v2` 生成的 Prompt |

## 阶段与审核关卡

`admitted` → `gt_ready` → `input_draft`（**duet 停下，等用户审核 GT 与 input**）→ `input_approved`（只有用户能设置）→ `rules_draft` → `ready_for_review`（**duet 再停下，等用户审核规则**）→ `frozen`（本地）→ `synced`（已拷回主仓库）。只前进不回退；回退须在 `note` 写明原因；没到 `input_approved` 不能进入 `rules_draft`；`frozen`、`synced` 由用户或 Claude 在本地设置。

## 档位在 GT 之后复核

目录名里的档位在入库时按来源源码暂定。GT 改成准静态之后，驱动方式往往变了（例如时间动画被去掉，T2 就成了 T1），所以 GT 完成后要重新判定，不同就运行 `python data_intake/tools/registry.py retier case-NNN-TX T1 --apply`，它会改目录名并同步台账。用户通过 input 之后不再改名。
