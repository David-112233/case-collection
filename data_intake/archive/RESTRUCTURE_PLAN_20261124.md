# case-collection 仓库整理与 Duet 案例工作区方案（定稿 v3，已执行）

> **更正（2026-11-24，用户纠正）：** 本文 §5.3 和 §6 里“先写 input、再做 GT”的加工顺序**是错的**。正确顺序是：**来源源码 → 准静态 GT（尽量尊重源码，无动画，只保留简单交互）→ 由 GT 写出 input → 用户审核 → 规则草稿 → 用户审核 → 本地冻结**；入库时的档位只是暂定，GT 完成后复核。现行规则见 `AGENTS.md` 第 4 节与 `cases/README.md`，本文其余部分保留作历史记录。

日期：2026-11-24　撰写：Claude　状态：**已由 Claude 在本地全部执行（阶段 0–5），未推送前 dot、duet 不需要再做整理**
适用对象：dot、duet（按新结构工作）。**本文第 6 节的步骤已经执行完毕，保留作历史记录**；现行规则以 `AGENTS.md`、`data_intake/README.md`、`cases/README.md` 为准。本文件在主仓库 `project_state/handoffs/` 也有一份，内容相同；dot 执行完毕后把本文件移入 `data_intake/archive/`。

## 0. 已确认的决定

| # | 决定 |
|---|---|
| 1 | **编号**：云端从 `case-228` 起连续编号；主仓库现有 `case-001`–`227`。编号只在入库时分配，不预留、不跳号。本地主仓库暂不自建案例号，确需新建时由 Claude 先在云端 `registry.csv` 占号。 |
| 2 | **Duet 的终点是 `ready_for_review`**：duet 在云端加工完成后，用户把仓库拉取到本地审核；**审核后由用户指示 duet 做下一步**（按意见修改，或继续后续工作）。冻结与 accepted 都在本地由用户确认后做，duet 不写 `FREEZE_v*.json`、不写 accepted。 |
| 3 | **直推 `main`**：认领、抓取、筛选、入库、案例加工都直接提交 `main`，不再每批新建分支和 PR。 |
| 4 | dot、duet 生成的输出放在案例目录下，不作特殊处理（用户本人负责，不属于本次整理范围）。 |
| 5 | **两份审核清单必须保留**：`空间关系候选审核清单_dot.xlsx` 与 `空间关系候选审核清单_dot.md`（约 300 个候选，用户已处理 50 个，其余正在审核）。见 §4。 |

## 1. 对 dot 原建议的评估（结论）

| dot 的建议 | 结论 |
|---|---|
| 统一索引 `review_index.csv` | 采纳，改名 `review.csv`，以 `作者__作品ID` 为主键，C 编号只作历史别名列 |
| 批次表放唯一目录 | 采纳：`batches/<YYYYMMDD>_<agent>_<NN>/` |
| 删掉重复的 `source_original.html` | **只在待审阶段不再生成**；案例入库后保留（主仓库 221–227 中 224、226 的两个文件内容不同，回传时格式必须一致） |
| 历史文件加标签 | 采纳，改为直接移入 `archive/` |
| 先导航索引、再命名、最后兼容副本 | 顺序采纳，前面加“Claude 本地先做”的一步（§2） |

## 2. Claude 已在本地完成的部分（dot 不要重复做，也不要改）

这些改动随本方案一起推送到 `main`，dot 在其基础上执行：

| 项 | 内容 |
|---|---|
| `reference/` | 主仓库规范的只读快照：`docs/`（输出契约 v2、评分细则 v6、评测流程 v6、难度模型、任务定义、决策、项目背景）、`skills/`（input-sharpening、eval-rules-refinement）、`schemas/`、`examples/`（13 个参考题目）、`examples_finished/`（完成态样板）、`history/`（采集初期的过期快照）、`dedupe_index.csv`（主仓库 227 例的来源链接）、`SYNC.md`（来源路径与哈希）。**只有 Claude 本地同步，云端不得修改。** |
| 过期文档 | 已按输出契约 v2 改：JS、外部字体和图片放开；删除“纯 CSS 门槛”“JS 四种处理”“每批开 PR”；新增 `DYN`/`LAY`/`PENDING` 原因码与现行口径（§6.5）。 |
| `AGENTS.md`、`README.md` | 新增统一规则（角色、写入边界、硬规则、禁止项、提交约定）。 |
| `cases/` 骨架 | `README.md`、`INDEX.md`（占位）、`registry.csv`（只有表头，`merge=union`）；原 185 份去重用 `metadata.json` 已删除，改由 `reference/dedupe_index.csv` 提供。 |
| 脚本 | `fetch_cdpn.py`、`claim.py` 的去重改为读 `reference/dedupe_index.csv`（已实测：已入库链接提示 `already case-NNN`）；新增 `scripts/case_tools/check_rules.py`（规则文件结构自检，已在主仓库 case-227、224、217、120 上验证无误报，并用故意破坏的文件验证能报错）。 |
| 审核清单安置 | `data_intake/review_lists/20261121_dot/`（见 §4）。 |
| `.gitattributes` | 已加 `registry.csv` 合并规则、`*.xlsx binary`，并一次性统一了 csv 换行符。 |

## 3. 目标结构

```
case-collection/
├─ README.md  AGENTS.md  RESTRUCTURE_PLAN.md(执行后归档)  requirements.txt  .gitignore  .gitattributes
├─ cases/                       ★ 正式案例区（Duet 的工作区）
│   ├─ registry.csv  INDEX.md  README.md
│   └─ case-228-TX/ …           与主仓库同名、同路径、同文件格式
├─ data_intake/                 ★ 采集区
│   ├─ README.md
│   ├─ ledger/ claims.csv  review.csv
│   ├─ batches/<YYYYMMDD>_<agent>_<NN>/   candidates.csv  screening.csv  notes.md
│   ├─ pending/<作者__ID>/       待用户判定的源码（original_srcdoc.html、source.html、metadata.json）
│   ├─ review_lists/<日期>_<agent>/        给用户看的清单（**受保护**，见 §4）
│   ├─ tools/                   claim.py decide.py peek.py triage.py shot.py admit_case.py registry.py
│   └─ archive/                 旧 B1 的历史材料
├─ scripts/ codepen_collection/（fetch_cdpn.py、collect_codepen.py）  case_tools/（check_rules.py）
└─ reference/                   只读，已由 Claude 建好
```

用途：`cases/` 只放已被用户选中的案例；`data_intake/` 放“找、认领、筛”的全过程直到用户判定；`reference/` 让智能体了解项目背景。

旧位置 → 新位置：`data_intake/B1/{claim,decide,peek,triage,shot}.py` → `tools/`；`B1/claims.csv` → `ledger/claims.csv`；`B1/candidates_dot_NN.csv` → `batches/…/candidates.csv`；`B1/screening_dot*.csv`、`source_audit_*.json` → 各批目录；`B1/raw/` 与 `reviewed_spatial_*` → `pending/`（尚待判定）或 `cases/`（已入库）；`B1/{STATUS.md,checkpoint_B.md,fetch_run*.log,candidates*.csv,screening.csv,intake.py}` → `archive/`。**不要在新位置继续使用 `intake.py`，它会写 `cases/`。**

## 4. 受保护文件：审核清单

- **位置**：`data_intake/review_lists/20261121_dot/`。其中已有 `空间关系候选审核清单_dot.xlsx`；`空间关系候选审核清单_dot.md` 由用户另行放入。
- **规则**：这两个文件**任何智能体都不得移动、改名、删除、覆盖、重新生成**。dot 的整理、搬迁、清理、入库步骤都要绕开 `review_lists/`。dot 在 `review_lists/` 里新增自己的清单时，只能新建文件，不改已有文件。
- **作用**：这是用户后续筛选的依据。用户在其中标 1 的才入库，标 0 的只记原作链接，不删。
- 用户已处理的 50 个中，标 1 的 27 个按 §6 阶段 4 入库；其余约 250 个候选保持 `review.csv` 中 `status=pending`，**不入库、不删除**，等用户标注。

## 5. `cases/` 案例工作区规则

### 5.1 入库（dot 执行，由用户触发）

用户标 1 之后，每例一次提交，推 `main`：

1. 用 `tools/admit_case.py` 从 `pending/<key>/` 生成 `cases/case-NNN-TX/`，文件集合照主仓库 `case-227-T1`：`README.md`、`classification.json`、`metadata.json`（补案例号、批次、来源提交与哈希）、`original_srcdoc.html`、`source.html`、`source_original.html`。`TX` 取 `classification.json` 的 T1–T6，**入库时定，之后不改名**。
2. `registry.csv` 追加一行（阶段 `admitted`，归属 `duet`）；`review.csv` 把该 key 标为 `admitted` 并写案例号；`pending/<key>/` 删除（Git 历史与 `metadata.json` 哈希保留证据）。
3. 编号取 `registry.csv` 最大号加 1，一次一个。
4. 标 0 的写入 `review_lists/…` 的二轮备选清单，只留原作链接。

### 5.2 `registry.csv`

字段：`case_id, source_key, tier, owner, stage, updated, note, user_review`。阶段：`admitted` → `input_draft` → `gt_ready` → `rules_draft` → `ready_for_review`（**duet 的终点**）→ `frozen`（用户本地确认并冻结后）→ `synced`（已拷回主仓库）。只前进不回退，回退须在 `note` 写原因。`user_review`（`pending/accepted/rejected`）只在用户明确指示时才能改，写入时须带用户原话。

### 5.3 Duet 在案例目录里做什么

依 `reference/skills/input-sharpening` 与 `reference/skills/eval-rules-refinement`，按输出契约 v2：

| 步 | 产出 |
|---|---|
| 1 | `input.json`（部件清单进 `functional_requirements`，视角、位置、外观进 `layout_constraints`；只写结果不写手段） |
| 2 | `ground_truth.html`：以 `source.html` 为基础，只做必要的最小修改（如删 CodePen 外部脚本、外链 reset 改内联），修改点写进案例 README |
| 3 | GT 自检：Playwright 双视口，截图与测量放 `review_<日期>/` |
| 4 | `rules_drafts/manual_v1/eval_rules.json`（格式 `semantic-eval-rules/3.0`，参照 `reference/examples_finished/`）与生成 Prompt；写完运行 `python scripts/case_tools/check_rules.py cases/case-NNN-TX` |
| 5 | `input_problem.md`、说明 |

**duet 不做**：写 `FREEZE_v*.json`、宣布 accepted、生成模型输出、评分、调用付费 API、改他人案例目录、改 `reference/`、改 `user_review`。

**审核后的衔接**：duet 到 `ready_for_review` 即停。用户拉取到本地审核后，直接向 duet 下达下一步指令（修改意见或继续）；duet 每次按指令做，并在 `registry.csv` 的 `note` 记一行。

### 5.4 用户怎么看、怎么回传

- 看 `cases/INDEX.md`（`tools/registry.py render-index` 自动生成，不手写）：案例号、来源链接、档位、阶段、处理者、更新日期、备注、目录链接。
- 提交约定：每个案例每个阶段一次提交，信息固定为 `case-NNN: <阶段>`；案例目录互不重叠，不冲突；`registry.csv` 设 `merge=union`；`INDEX.md` 冲突时重新生成。
- 回传：用户说“同步”后，Claude 本地把 `ready_for_review` 的 `cases/case-NNN-TX/` 整个目录原样复制到主仓库 `cases/`，校验哈希、登记 TASKS，`registry.csv` 记 `synced`。不拷 `registry.csv`、`INDEX.md`、`reference/`。

## 6. dot 的执行步骤

每阶段独立提交，完成一阶段向用户发一份简短报告，**用户回复“继续”后再进下一阶段**。

| 阶段 | 内容 | 验收 |
|---|---|---|
| 0 | 给当前 `main` 打标签 `pre-restructure-20261124`；确认已拉到包含 §2 改动的 `main` | 标签存在；`reference/SYNC.md` 在 |
| 1 | **只移动、不改内容**：按 §3 的对应关系 `git mv`；旧 B1 历史材料进 `archive/`；**不碰 `review_lists/`** | `git diff -M` 全部为重命名；`review_lists/20261121_dot/` 的文件哈希与搬迁前一致 |
| 2 | 修路径：改 `claim.py`、`decide.py`、`peek.py`、`triage.py`、`shot.py`、`fetch_cdpn.py` 的默认路径与 `data_intake/README.md` 里的命令；建 `ledger/review.csv`（由认领表、筛选记录、审核清单合并，`status` 取 pending/selected/reserve/rejected/admitted）；把 `status=pending` 的候选源码从各分支按固定提交取回 `pending/`，逐个核对哈希 | 在干净克隆里实跑：`fetch_cdpn.py` 对已入库链接提示 `already case-NNN`，对新链接可抓取；`claim.py --check`、`peek.py`、`triage.py` 运行正常；`pending/` 每份源码哈希与 `metadata.json` 一致 |
| 3 | 建 `tools/registry.py`（`set-stage`、`set-owner`、`render-index`；改 `user_review` 须加 `--by-user "<用户原话>"`）与 `tools/admit_case.py`（默认**预演**，只打印将创建的内容，`--apply` 才写；档位缺失、案例目录已存在、key 未标为已选时拒绝） | 预演一个案例，输出的文件集合与主仓库 `case-227-T1` 一致，且不写任何文件 |
| 4 | **用户确认入库名单后**，对已选 27 个案例执行入库，从 `case-228` 起，按审核清单 C 编号顺序；`INDEX.md` 重新生成 | 27 个目录、台账 27 行、六个文件齐全；`original_srcdoc.html`、`source_original.html` 哈希与审核分支一致；`pending/` 对应目录已移除；`review_lists/` 未变 |
| 5 | 生成分支清理清单：逐个远程分支说明其内容是否已全部进入 `main`。**只出清单，不删除分支、不关闭 PR** | 用户逐条同意后才删 |

## 7. 禁止事项

- 不执行 `git reset`、`git clean`、强制推送，不改写已推送的提交。
- 不删除远程分支、不关闭 PR，除非用户明确同意。
- **不移动、改名、删除、覆盖 `review_lists/` 中的任何文件。**
- 不修改 `reference/`、他人处理的案例目录、`user_review` 字段。
- 不读取或输出凭据；不调用付费 API。
- 不为凑数降低标准；未核验的内容不得写成已核验。

## 8. 仍未固化的一点

dot 自 2026-11-19 起做的“空间关系”专项（多物体空间、叠压遮挡、三维等），其选题标准是用户当时对 dot 的口头说明，没有成文。`data_intake/README.md` 里只标注了这一缺口。请用户在方便时把标准口述一份，由 Claude 写入采集说明。

---

## 9. 执行结果（2026-11-24，Claude 本地）

| 阶段 | 结果 |
|---|---|
| 0 | 本地标签 `pre-restructure-20261124`（指向整理前的 `62aba07`） |
| 1 | 旧 `data_intake/B1/` 全部按 §3 迁移：脚本进 `tools/`，认领表进 `ledger/`，各候选名单进 `batches/<日期>_<agent>_<NN>/`，旧历史材料进 `archive/` |
| 2 | 工具与说明的路径已改；`ledger/review.csv` 共 431 行；各分支独有的候选名单、筛选记录、来源核验、dot 报告已并入 `batches/` 与 `archive/dot_branch_records/`；待判定源码 233 份放 `pending/`（哈希全部核对一致）；其余候选源码 173 份并入 `archive/dot_sources/` |
| 3 | 新增 `tools/registry.py`、`tools/admit_case.py`（默认预演）；预演与各类拒绝条件已验证 |
| 4 | 已选 27 个入库为 `case-228`–`254`，档位由 Claude 按驱动方式判定并写明依据，**待用户抽查**；三个有疑问的在 `registry.csv` 备注：case-235（WebGL 画布）、case-253（T2/T3 有争议）、case-234（外部脚本未核验） |
| 5 | 分支清理清单见 `data_intake/archive/branch_cleanup_list_20261124.md`：66 个分支内容均已并入 `main`；**未删除任何分支或 PR，须用户逐条同意** |

补充：两份早期入库清单（`入库清单_dot.md`、`二轮备选_dot.md`）已保存到 `data_intake/review_lists/20261120_dot_c001_c050/`；用户的 xlsx 在 `review_lists/20261121_dot/`，未动。
