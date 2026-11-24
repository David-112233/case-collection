# AGENTS.md · case-collection 统一规则

本仓库是“前端代码生成评测基准”主项目的**案例采集与加工子集**，由 dot 和 duet 两个智能体在云端协作，成果由用户拉取到本地后再并入主仓库。本文件对两个智能体同样适用；与具体任务文档冲突时，**以本文件和 `reference/docs/output_contract_v2.md` 为准**。

## 1. 先读什么

1. 本文件。
2. [README](README.md)（三个区各做什么）。
3. 采集任务读 [data_intake/README.md](data_intake/README.md)；案例加工任务读 [cases/README.md](cases/README.md)。
4. 背景与标准：[项目背景](reference/docs/PROJECT_BACKGROUND.md)、[输出契约 v2](reference/docs/output_contract_v2.md)、[评分细则 v6](reference/docs/scoring_rubric_v6.md)、[类型与难度模型](reference/docs/difficulty_model_v2_1.md)。`reference/docs/TASK_DEFINITION_v5_2_synced.md` 中的“禁止 JavaScript”等输出限制已被输出契约 v2 取代。

## 2. 项目是什么

给模型一份 `input.json`（业务、功能、布局、动效、禁令五段），让它生成单文件 HTML。**JavaScript、外部字体和图片已放开**（DEC-048），具体案例的禁令仍以该案例的 input 为准。评测以 Evidence（每条 mandatory 条件）为计分单位，按严重度扣分；维度为 D1 静态、D2 动态。本仓库不评分，只负责找到合适的来源作品并把它加工成案例。

## 3. 角色与写入边界

| | dot | duet |
|---|---|---|
| 主要职责 | 采集：搜索、认领、抓取、筛选、整理审核清单、执行入库 | **优先加工 `cases/` 里归属自己的案例**；队列空了再采集 |
| 可以写 | `data_intake/`；入库时新建 `cases/case-NNN-TX/` 并追加 `cases/registry.csv` | `cases/` 下归属 duet 的案例目录；采集时写自己的批次目录与 `data_intake/ledger/` |
| 不可以写 | 案例内容（input、GT、规则） | `user_review` 字段、入库、`reference/` |

两者共同禁止：改 `reference/`；改对方的案例目录或批次文件；重判对方认领的作品。认领规则见 [data_intake/README.md](data_intake/README.md)：先认领并推送，成功后才抓取和判断，先到先得。工具都在 `data_intake/tools/`（`claim.py`、`decide.py`、`peek.py`、`triage.py`、`shot.py`、`registry.py`、`admit_case.py`）。

## 4. 案例加工要求（duet）

- 范围：`input.json`、`ground_truth.html`（以来源 `source.html` 为基础，只做必要的最小修改并在 README 写明）、GT 自检记录、`rules_drafts/manual_v1/eval_rules.json`、生成 Prompt、`input_problem.md`。步骤和方法见 [input-sharpening](reference/skills/input-sharpening/SKILL.md) 与 [eval-rules-refinement](reference/skills/eval-rules-refinement/SKILL.md)；完成态样板见 `reference/examples_finished/`。
- input 写作：只写结果，不写实现手段；部件清单进 `functional_requirements`，视角、位置、外观进 `layout_constraints`。
- 规则：Requirement 来源是 `input.json` 加基本常识（DEC-037）；常识条目须标 `source: common_sense` 和理由，不得引入新的业务内容或具体样式数值；GT 只用于锚点绑定与自测，**不得反推新增要求**。
- 写完用 `python scripts/case_tools/check_rules.py cases/case-NNN-TX` 自检。
- **终点是 `ready_for_review`。** 不写 `FREEZE_v*.json`，不写 accepted，不生成模型输出，不评分。用户在本地审核后，由用户指示下一步。

## 5. 硬规则（摘自主项目，不得改口径）

- 计分：FAIL 按严重度扣分，轻 0.5、中 1、重 1.5；缺证据或原因不明记 UNRESOLVED，不判 FAIL；同一事实只扣一次。
- 需求与规则先冻结，再生成模型输出；看到输出后不得为调分改条件；不得为增加扣分而拆细条件；不得为均分好看而调严重度或难度。
- 不得人工修补模型 HTML 后当原始输出评分。
- 选题标准：技术常见、答案可联网检索、单组件演示、纯装饰循环动画一律不收；多收网页类，其次 CSS 动画类，少收小游戏类。不得用被测模型的得分挑题，也不得把候选交给模型试做。
- 历史版本保留，新旧不混用；规则冲突时报告，不静默改口径。

## 6. 禁止事项

- 不执行 `git reset`、`git clean`、强制推送，不改写已推送的提交。
- 不删除远程分支、不关闭 PR，除非用户明确同意。
- 不读取或输出任何凭据（`.env`、token、密钥）；不调用任何付费 API。
- 不修改 `reference/`、`user_review` 字段、他人的案例目录。
- 不抓取非公开作品，不绕过访问验证；抓取只用 `cdpn.io` 规定入口，间隔不少于 2 秒；保留作者与原链接（CodePen 公开作品默认 MIT）。
- 未核验的内容不得写成已核验；不为凑数降低标准。

## 7. 提交约定

- 认领、入库、案例加工均直接提交 `main`，一次提交只做一件事。案例加工的提交信息固定为 `case-NNN: <阶段>`。
- 每次提交前先 `git pull --rebase origin main`；推送被拒时同步后重试，不强推。
- 不再为每个批次新建分支和 PR。
