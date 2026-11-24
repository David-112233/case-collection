# 数据收集路径（供云端智能体执行）

更新：2026-11-24。整理者：Claude。本页是采集区（`data_intake/`）的执行说明。统一规则和角色边界见 [AGENTS.md](../AGENTS.md)；决策原文见 [DECISIONS](../reference/docs/DECISIONS.md)（DEC-031—036 是选题标准，**DEC-048 放开了 JavaScript、外部字体和图片**）；采集初期的旧方案在 [reference/history/](../reference/history/)，口径已过期，只供追溯。

## 0. 先读这些

| 顺序 | 文件 | 读它是为了 |
|---|---|---|
| 1 | [项目背景](../reference/docs/PROJECT_BACKGROUND.md) | 明白基准测什么、为什么只要难题、什么作品能改成案例 |
| 2 | 本页 | 步骤、标准、协作规则 |
| 3 | [reference/examples/](../reference/examples/) | 看 13 个已入库案例的题目和难点说明（先读其中的 README），知道成品长什么样；完成态样板见 [reference/examples_finished/](../reference/examples_finished/) |
| 4 | [archive/screening.csv](archive/screening.csv) | 看 265 条早期判断的写法，尤其是 7 条 accept 和被用户否掉的 U1、U2 |
| 5 | [reference/dedupe_index.csv](../reference/dedupe_index.csv) | 主仓库全部 227 例的档位、来源链接和一句话背景，避免题材重复（链接级去重由脚本自动完成） |

需要查原文时再看：[输出契约 v2](../reference/docs/output_contract_v2.md)（输出限制以它为准）、[任务定义 v5.2](../reference/docs/TASK_DEFINITION_v5_2_synced.md)（其中“禁止 JavaScript”已被取代）、[类型与难度模型 v2.1](../reference/docs/difficulty_model_v2_1.md)、[扩量方案](../reference/history/DATA-001-expansion-plan-20260928.md)。

## 1. 一句话任务

从 CodePen 公开作品里找出**技术罕见、对模型难**的作品，抓取源码，逐个判断并写出理由，最后交一份“建议入库”清单给用户挑选。**不要求纯 CSS**：JavaScript、外部字体和图片均已放开（DEC-048），原作保留原样，不为符合旧门槛而删改。

## 1.5 两个采集者的协作规则

本仓库由 dot 和 duet 两个智能体同时采集。规则只有一条主线：**先认领，后处理；谁先认领归谁。**

**公共登记表是 [ledger/claims.csv](ledger/claims.csv)。** 一行一个作品，只追加、不修改、不删除。同一个作品出现多行时，靠前的那行有效。

每一轮按这个顺序做：

```bash
git pull --rebase origin main                                   # 1 先同步
# 2 把本轮找到的链接写进本批的候选文件 data_intake/batches/20261125_dot_40/candidates.csv（批次号 日期_名字_序号）
python data_intake/tools/claim.py dot data_intake/batches/20261125_dot_40/candidates.csv    # 3 认领
git add data_intake/ledger/claims.csv data_intake/batches/20261125_dot_40/candidates.csv
git commit -m "认领：dot 第01轮" && git push origin main          # 4 立刻推到 main
```

- 第 3 步会自动跳过三类作品：对方已认领的、历史上已判断过的、已在库内的。
- 第 4 步推送被拒，说明对方刚推过。执行 `git pull --rebase origin main` 后再推即可，登记表会自动合并。然后运行 `python data_intake/tools/claim.py --check`，它会列出两边撞车的作品和归属，排在后面的一方放弃。
- **认领推送成功之后才能开始抓取和判断。** 只处理归自己的作品。

各写各的文件，互不触碰：

| 内容 | dot 写 | duet 写 |
|---|---|---|
| 候选链接 | `batches/<日期>_dot_<NN>/candidates.csv` | `batches/<日期>_duet_<NN>/candidates.csv` |
| 筛选判断 | 同批目录的 `screening.csv` | 同左 |
| 源码 | `pending/` 下自己认领的作品目录 | 同左 |

- `archive/` 下是早期历史记录（旧筛选表、旧候选表、旧脚本、dot 各分支里的批次记录），两人都只读不写。
- 默认搜索分工，减少撞车：**dot 主找 T1、T2、T6；duet 主找 T4、T5、T3。** 这只是搜索方向。顺手发现对方方向的好作品照样可以认领，谁先登记归谁。
- 不重判对方的作品。对对方的结论有不同看法时，写在自己的批次说明里，由用户裁决，不要改对方的文件。
- `pending/` 里有 233 份待用户判定的源码：约 210 份来自 dot 的空间关系候选（审核清单见 `review_lists/20261121_dot/`），另有早期 24 份暂留候选。这些都不属于任何一方，用户标 1 后才入库。
- **所有提交都直接推 `main`**（认领、抓取、筛选、清单），不再为每批新建分支和 PR。每次提交前先 `git pull --rebase origin main`；一次提交只做一件事；不强推。

## 2. 整条路径与云端范围

| 步 | 内容 | 产出 | 云端做吗 |
|---|---|---|---|
| 1 发现并认领 | 网页搜索，收集 CodePen 链接，登记到公共表 | `batches/<批次>/candidates.csv`、`ledger/claims.csv` | 做 |
| 2 获取 | 经 cdpn.io 抓编译后的 HTML+CSS | `pending/{作者}__{ID}/` | 做 |
| 3 汇总 | 生成一张源码规模与特性表 | `triage.csv`（本地辅助） | 做 |
| 4 筛选 | 读源码、看渲染，定档位、难度特征、JS 处理、去留 | `batches/<批次>/screening.csv` | 做 |
| **检查点 A** | **用户从“建议入库”里挑选** | — | **停在这里** |
| 5 入库 | 分配案例编号（从 `case-228` 起），生成案例目录，写台账 | `cases/case-NNN-TX/`、`cases/registry.csv` | **dot 执行，由用户触发** |
| 6 加工 | 先把 `source.html` 改造成准静态 GT，再由 GT 写 input | 案例目录 | **duet 执行**，见 [cases/README.md](../cases/README.md) |
| **检查点 B** | **用户在本地审核 GT 与 input**，通过后 duet 才写规则草稿，规则再由用户审核 | — | 停在这里 |

采集区只做第 1—4 步；第 5、6 步在 `cases/` 工作区进行。**入库后的参考答案（GT）会被改造成准静态：没有动画，只保留简单交互**，所以选题时要看“去掉动画之后还剩下多少难点”（空间关系、排版、遮挡、对齐、复杂布局、简单交互里的状态逻辑），难点只在动画里的作品价值有限，筛选备注里要写明。入库只在用户标 1 之后执行，不自行入库。

## 3. 当前进度

- 实时进度看 [cases/INDEX.md](../cases/INDEX.md)（已入库案例）、候选状态表 [ledger/review.csv](ledger/review.csv) 和认领表 `ledger/claims.csv`。早期进度见 [archive/STATUS.md](archive/STATUS.md)，只供追溯。
- 主仓库已有案例 `case-001`—`227`。dot 已收集约 300 个“空间关系”候选，审核清单在 [review_lists/20261121_dot/](review_lists/20261121_dot/)，**用户正在审核，任何人不得移动、改名、删除或覆盖其中的文件**。
- 已入库案例 `case-228`—`254`（27 个，来自 dot 的空间关系首轮与追加审核）；其余候选的状态见 `ledger/review.csv`（pending/reserve/hold/rejected 等）。
- 库内现有数量（名义值，部分旧案例不合格）：T1 11、T2 43、T3 55、T4 12、T5 49、T6 50。目标各 75，共 450；T4 不设硬目标。
- **档位优先级：T1 和 T4 最缺；其次 T5、T6、T2、T3。** 不为凑数降低标准。
- **题材优先级：多收网页类，其次 CSS 动画类，少收小游戏类。** 详见第 6.7 节。

## 4. 环境准备

云端一般是 Linux，本仓库的 Windows 写法要换掉（`scripts/case_tools/check_rules.py` 等脚本只用标准库）：

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium
export PYTHONUTF8=1
```

- 网络要能访问 `cdpn.io`（抓源码）和搜索引擎。`codepen.io` 本身有 Cloudflare 验证，不要去抓，也不要尝试绕过验证。
- 抓取脚本只用标准库；只有截图脚本 `tools/shot.py` 需要 Playwright。
- 以下命令都在仓库根目录执行。

## 5. 步骤

### 第 1 步：发现候选

用网页搜索找链接，写入本批的新文件 `data_intake/batches/<日期>_<名字>_<NN>/candidates.csv`（序号递增），三列：

```csv
url,target_tier,found_via
https://codepen.io/作者/pen/ID,T4,websearch-2026-11-10
```

- 搜索词用“档位 × 难度机制”组合，例如 `codepen scroll-state container query table`、`codepen pure css isometric city`、`codepen animation-timeline view() landing page`、`codepen css only dashboard layout :has()`、`codepen pure css character walk cycle animation`。
- 搜索重心放在完整页面和应用界面（落地页、仪表盘、应用原型、专题长页、信息图）以及多部件协调的 CSS 动画上；小游戏类不必专门去搜。
- **不要**加 “no JavaScript”“pure CSS only” 这类限定词：JS 已放开，含 JS 的作品同样值得收。
- 其他线索：GitHub 上的 awesome 列表（css-art、pure-css、css-only 主题）里的 CodePen 链接；常产出难题的作者，如 argyleink、jh3y、bramus、una、thebabydino、utilitybend、giana、hexagoncircle、amit_sheen。
- 写完后按第 1.5 节认领并推送。已判断过、已入库、对方已认领的链接会在认领时自动跳过。

### 第 2 步：获取源码

只抓归自己的作品：

```bash
python data_intake/tools/claim.py --owned dot > /tmp/owned_dot.csv
python scripts/codepen_collection/fetch_cdpn.py --candidates /tmp/owned_dot.csv --out data_intake/pending
```

- 脚本请求 `https://cdpn.io/{作者}/fullpage/{ID}`，默认每 2 秒一次，不要调快。
- 每个作品得到 `original_srcdoc.html`（原样）、`source.html`（去掉 CodePen 样板脚本）、`metadata.json`（作者、链接、时间、哈希、JS 与 CSS 特性标注）。
- 自动跳过三种情况：已在库内的作品（主仓库 `reference/dedupe_index.csv` 与本仓库 `cases/`）、本目录已抓过的作品、取不到源码的页面。
- 脚本**只标注** JS 和外部资源，不因为有 JS、外部图片或外链就丢弃。
- 每次运行的记录追加在 `pending/fetch_log.jsonl`。

### 第 3 步：汇总

```bash
python data_intake/tools/triage.py
```

输出 `data_intake/triage.csv`：每个候选的 JS 字符数、CSS 字符数、元素数、keyframes 数、命中的 CSS 特性。用它先排掉明显太小的作品（元素很少、CSS 很短的单组件）。这张表每次按 `raw/` 现有内容整张重写，是本地辅助文件，不入库、不提交。

### 第 4 步：逐个筛选

每个候选都要看源码，拿不准的要看渲染结果：

```bash
python data_intake/tools/peek.py 作者__ID            # 压缩后的 CSS 与正文文字；加 --js 看脚本
python data_intake/tools/shot.py data_intake/pending/作者__ID/source.html /tmp/shots/作者__ID --widths=1280,375
```

判断完用 `decide.py` 记一行（同一个 key 再记一次会覆盖旧行）。先设好自己的名字，记录会写进 `batches/<批次>/screening.csv`（批次用环境变量 `COLLECT_BATCH` 指定，默认今天的 `_01`）；不是自己认领的作品会被拒绝：

```bash
export COLLECT_AGENT=dot
python data_intake/tools/decide.py KEY DECISION TIER HITS REASON "证据" "备注" JS_POLICY   # JS_POLICY 填 none（无 JS）或 preserve（含 JS，原样保留）
python data_intake/tools/decide.py una__myJOjQx accept T4 H2,H4,H6,H8 - "横向吸附日卡片；scroll-state(snapped)联动当前卡片；counter生成天数编号" "外部图标字体需替换" none
```

- `DECISION`：`accept`（建议入库，等用户挑）、`reject`、`hold`（合格但属于后续批次，或需再细看）。
- `证据`必须具体：写出哪段机制对应哪条特征，让别人不看源码也能复核。只写“很复杂”不算证据。
- `accept` 的备注里再写一句：**这个技术为什么对模型罕见或困难**。

## 6. 筛选标准

### 6.1 定档位（T1—T6）

问一个问题：这个视觉变化是谁在驱动的？完整定义见 [类型与难度模型 v2.1](../reference/docs/difficulty_model_v2_1.md) 第三章。

| 档 | 驱动方式 |
|---|---|
| T1 | 没有任何动态 |
| T2 | 按时间自动播放；或悬停/聚焦只改变被指向元素自身，移开即还原 |
| T3 | 点击/勾选/跳锚进入会保持的状态；或悬停驱动**其他**元素显隐、展开 |
| T4 | 滚动吸附到停靠点；scroll-state 这类由滚动位置驱动的离散状态也归 T4 |
| T5 | 动画进度随滚动连续推进（`animation-timeline: scroll()/view()`） |
| T6 | 混合驱动，或依赖 `@property`、View Transitions、计数器图表等高级特性 |

多种机制并存时按较高的档标注，例如吸附加滚动驱动动画记 T5。

### 6.2 八条难度特征

| 编号 | 特征 | 判断要点 |
|---|---|---|
| H1 | 多状态耦合 | 3 个以上互相影响的状态载体（checkbox、radio、`:target`、`:has()`） |
| H2 | 一处触发多处联动 | 一个操作同时改变多个相距较远的元素，可逆，多实例互不干扰 |
| H3 | 精确时间编排 | 3 个以上阶段的 keyframes，有明确时长、错峰、循环衔接 |
| H4 | 新特性 | `animation-timeline`、`@property`、`:has()`、容器查询、anchor 定位、View Transitions、scroll-state、`::scroll-marker`/`::scroll-button` |
| H5 | 几何/3D 精度 | 3D 变换、多面体、复杂 `clip-path` 或 `conic-gradient` 图形 |
| H6 | 计算内容 | CSS 计数器、`counter()` 计分、纯 CSS 图表 |
| H7 | 大体量完整布局 | 多区块、多组件、多断点的完整页面，不是单个组件 |
| H8 | 多机制组合 | 两种以上机制叠加，如吸附加状态、滚动驱动加悬停 |

### 6.3 入库阈值

| 档 | 阈值 |
|---|---|
| T1 | 命中 2 项以上且含 H5 或 H7；或“强单项”：强 H7 = 完整页面、80 个以上元素、3 个以上不规则区块；强 H5 = 静态几何/3D 场景由大量精确拼装的部件构成 |
| T4 | 命中 2 项以上 |
| T2、T3、T5、T6 | 命中 3 项以上 |

### 6.4 一票否决

满足阈值也不收：

- 单组件演示、纯装饰循环动画、一条 CSS 规则就能复现的作品（原因码 D0）。
- **技术类型常见**（原因码 C1）：普通轮播、`::scroll-marker` 新式单组件轮播、单行吸附列表、自动播放轮播、可滚动提示、目录高亮、Netflix/Spotify 仿制页、报纸杂志网格版面。
- **答案可联网检索**（原因码 C1）：内容是公开的固定知识，模型搜一张图就能照做，如元素周期表。
- 视觉核心依赖外部图片、视频、真实品牌或真实人物，换成占位后失去意义（原因码 X1）。
- 与已收或已判断的作品代码近似、题材重复（原因码 R02）。

用户实际收过的类型，可作参照：双层嵌套吸附轮播、菜单加跨元素悬停加吸附的完整页、斜切锯齿加计数器加多断点的信息图、吸附与编号与指示点联动的行程页、scroll-state 驱动双侧箭头的表格页、针织品牌着陆页、大量部件拼装的静态 3D 等距场景。

### 6.5 含 JS 与外部资源的作品（输出契约 v2）

JS、外部字体、外部图片、普通链接都已放开，**原样保留**，不要为了通过旧的“纯 CSS 门槛”删改作品。`JS_POLICY` 只填两个值：`none`（无 JS）、`preserve`（含 JS，保留原样）。以下情况仍要在备注里写明：

| 情况 | 怎么处理 |
|---|---|
| JS 是效果的核心，且需要截很多时间帧才能评分（逐帧物理模拟、持续随机位移、全屏循环视频） | 不是因为“有 JS”，而是评分成本太高：记原因码 `DYN`，不推荐 |
| JS 只做导航、菜单开关、简单状态切换 | 正常判断，备注写明 JS 的作用 |
| 页面靠网络请求、随机或实时数据才有内容 | 同样是评分成本问题，备注写明，不推荐 |
| 视觉核心依赖外部图片或视频 | 看不到图不是拒收理由；备注写明哪些内容只能从源码推断、哪些已见画面，**不得写成已核验** |

### 6.6 原因码

| 码 | 含义 |
|---|---|
| `-` | 建议入库 |
| D0 | 单组件、纯装饰、一条规则可复现 |
| D1 | 未达阈值 |
| C1 | 技术常见，或答案可联网检索（DEC-036） |
| J1 | （已停用）旧的“JS 是核心且无 CSS 等价”，JS 放开后不再使用 |
| X1 | 源码不可用，或视觉核心是真实品牌、真实人物 |
| DYN | 动态取证成本高：需要截大量时间帧才能评分（见 6.5） |
| LAY | 布局或空间关系的复杂度未证明超过已入库案例 |
| PENDING | 难度、视觉或范围的证据尚不足，待补 |
| R02 | 与其他候选重复 |
| T2/T3/T5/T6 | 合格但属于后续批次，`decision` 记 `hold` |
| U1/U2 | 用户在检查点未选，只由用户侧填写 |

### 6.7 题材偏好

用户希望这个基准更像“前端网页”的测试，而不是小游戏合集。同样达到阈值的候选，按下面的顺序取舍：

| 顺序 | 题材 | 说明 |
|---|---|---|
| 多收 | **网页类** | 完整页面或应用界面：产品落地页、应用原型、仪表盘、看板、专题长页、信息图、行程或相册这类内容页 |
| 其次 | **CSS 动画类** | 多个部件按精确时序协同运动的场景或角色动画 |
| 少收 | **小游戏类** | 靠大量点击推进、规则复杂的纯 CSS 游戏（扫雷、棋类、闯关等） |

- 小游戏不是不收，只是少收：**每轮建议入库的清单里，小游戏类最多 1 例**，而且要是库里没有的玩法。
- 在 `decide.py` 的备注开头标明题材：`[网页]`、`[动画]`、`[游戏]`，方便用户按题材挑选。
- 题材偏好不改变阈值。网页类也必须够难，普通的登录页、定价表、营销落地页照样拒收。各类样例见 [reference/examples/](../reference/examples/)。

## 7. 交付

- 所有提交直接推 `main`（见第 1.5 节）。你的改动只应出现在：自己的 `batches/` 下本批目录、`pending/` 下自己认领的作品目录、`pending/fetch_log.jsonl`、`ledger/claims.csv`、给用户看的清单目录 `review_lists/<日期>_<名字>/`。
- 每轮写一份清单交用户挑选：新增候选数、抓取成功与失败数、各原因码数量、建议入库清单（链接、档位、命中特征、**为什么难**、已核验与未核验的范围）、没做完的部分。
- 宁可少报。每轮建议入库控制在 10 例以内，方便用户逐个看。
- 用户标 1 之后才入库；标 0 的只留原作链接，不删。

## 8. 不要做

- 不要在 `cases/` 里新建目录，**入库只在用户标 1 之后，由 dot 执行**；不要自行分配案例编号。
- 采集者不写 `ground_truth.html`、`input.json`、评测规则（这是 duet 在 `cases/` 里的工作）；不生成模型输出，不评分。
- 不要调用任何大模型 API 来分类或筛选；不要读取或输出 `.env`、密钥等凭据。
- 不要用被测模型的得分来挑题，也不要把候选交给模型试做。
- 不要修改 `reference/`（主仓库的只读副本）；不要移动、改名、删除、覆盖 `review_lists/` 里的文件；不要执行 `git reset`、`git clean`，不要强推。
- 不要抓非公开作品，不要绕过 Cloudflare 验证；保留作者与原链接（公开作品默认 MIT 许可）。
- `accept` 只是建议，是否入库由用户决定。

## 9. 已知问题

- cdpn.io 导出的是编译后代码，没有 SCSS 原稿；个别作品的样式不随导出带出，抓到的页面没有 CSS，记 X1。
- 源码里的外部字体、图片、CDN 样式在离线环境可能加载不到，截图会走样；看渲染时不要加 `--offline`。
- 很新的特性（scroll-state、`::scroll-marker`、anchor 定位）需要较新的 Chromium，截图不对时先确认浏览器版本。
- 外部字体、图片和 CDN 样式现在是允许的，但只能原样保留，抓取时不下载这些外部资源；缺图不是拒收理由。
- 2026-11-19 起 dot 另有一轮“空间关系”专项（多物体空间、叠压遮挡、三维等），其具体标准是用户当时对 dot 的口头说明，**尚未写进本页**；需要时向用户确认，不要自行推断。
