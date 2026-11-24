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

## 4. 案例加工（duet）

**顺序（用户确认的正确流程）：来源源码 → 准静态的 GT → 由 GT 写出 input → 用户审核 → 规则草稿 → 用户审核 → 本地冻结。** 不是先写 input 再做 GT。

1. **`ground_truth.html`**：以案例目录里的 `source.html` 为基础，**尽量尊重源码**（结构、样式、文案、素材与字体引用、版式都不动），改造成**准静态**：
   - 没有动画：持续或自动播放的 CSS 动画与过渡、JS 动画循环、自动轮播、跑马灯、自动播放的视频或 GIF 都去掉；动画元素固定在一个有代表性的静止状态，写明选了哪个状态、为什么。
   - 只保留简单交互：悬停、聚焦、点击展开或折叠、菜单与开关、简单的状态切换。
   - 如果这个作品的价值主要在动画或复杂交互（拖拽、物理、游戏规则、实时或随机数据），**不要硬改**，在案例 README 报告并停下问用户。
   - 每处改动和原因写进案例 README 的“GT 相对来源的改动”；GT 自检（Playwright 双视口截图与测量）放 `review_<日期>/`。
2. **复核档位**：入库时的档位是按来源源码暂定的。GT 完成后按 GT 的驱动方式重新判定（无动态 T1；悬停只改自身 T2；点击保持状态或悬停驱动其他元素 T3…）。与目录名不同就用 `registry.py retier`（只在用户通过 input 之前允许）。
3. **`input.json`**：由 GT 写出，只写 GT 里确实有的、可判定的效果；只写结果，不写实现手段；部件清单进 `functional_requirements`，视角、位置、外观进 `layout_constraints`。
4. **停下**：把阶段设为 `input_draft`，等用户审核 GT 与 input。用户通过后由用户指示；阶段 `input_approved` 只能在用户原话下设置。
5. **规则草稿**（用户通过 input 之后才做）：`rules_drafts/manual_v1/eval_rules.json` 与生成 Prompt，格式见 `reference/examples_finished/`，写完运行 `python scripts/case_tools/check_rules.py cases/case-NNN-TX` 自检。规则的来源是 `input.json` 加基本常识（DEC-037），常识条目标 `source: common_sense` 和理由，不得引入新的业务内容或具体样式数值；**规则不得直接以 GT 为来源**，GT 只用于锚点绑定与自测。完成后阶段设为 `ready_for_review`，停下等用户。
6. 此后的冻结、生成模型输出、评分都不在云端做。

方法可参考 [input-sharpening](reference/skills/input-sharpening/SKILL.md)、[eval-rules-refinement](reference/skills/eval-rules-refinement/SKILL.md)，但前者写的是“改写已有 input”的流程，**新案例的顺序以本节为准**。

**duet 不做：** 写 `FREEZE_v*.json`、宣布 accepted、生成模型输出、评分、调用付费 API、改他人案例目录、改 `reference/`、改 `user_review`。

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
