# 数据收集路径（供云端智能体执行）

更新：2026-11-10。整理者：Claude。本页把 DATA-001/DATA-002 已确认的做法写成一份可独立执行的说明；决策原文见 [DECISIONS](../project_state/DECISIONS.md) 的 DEC-031—036，方案原文见 [B1 工作方案](../project_state/handoffs/DATA-001-workplan-B1-20261002.md)。

## 1. 一句话任务

从 CodePen 公开作品里找出**技术罕见、对模型难**的纯 CSS（或可改成纯 CSS）作品，抓取源码，逐个判断并写出理由，最后交一份“建议入库”清单给用户挑选。

## 2. 整条路径与云端范围

| 步 | 内容 | 产出 | 云端做吗 |
|---|---|---|---|
| 1 发现 | 网页搜索，收集 CodePen 链接 | `B1/candidates_N.csv` | 做 |
| 2 获取 | 经 cdpn.io 抓编译后的 HTML+CSS | `B1/raw/{作者}__{ID}/` | 做 |
| 3 汇总 | 生成一张源码规模与特性表 | `B1/triage.csv` | 做 |
| 4 筛选 | 读源码、看渲染，定档位、难度特征、JS 处理、去留 | `B1/screening.csv` | 做 |
| **检查点 A** | **用户从“建议入库”里挑选** | — | **停在这里** |
| 5 入库 | 分配案例编号，写来源与分类文件 | `cases/case-NNN-TX/` | 不做 |
| 6 写 input | 依据源码实际效果写 `input.json` | 案例目录 | 不做 |
| 7 写 GT | 依据 input 写单文件纯 CSS 参考页并双视口自测 | 案例目录 | 不做 |
| **检查点 B** | **用户审核 input 与 GT** | — | — |

云端只做第 1—4 步。第 5 步起要占用案例编号、需要用户逐例确认，留在本地做。

## 3. 当前进度

- 已入库 7 例：case-211—217（T4 四例、T1 三例）。检查点 B 还没过，见 [B1 进度](B1/STATUS.md)。
- 已判断 265 个候选：建议入库 7、暂留 24（T2 7、T3 6、T5 11）、拒收 234。通过率约 3%，所以要多找候选。
- `B1/raw/` 里还留着 24 份暂留候选的源码，不必重抓。
- 库内现有数量（名义值，部分旧案例不合格）：T1 11、T2 43、T3 55、T4 12、T5 49、T6 50。目标各 75，共 450；T4 不设硬目标。
- **优先级：T1 和 T4 最缺；其次 T5、T6、T2、T3。** 不为凑数降低标准。

## 4. 环境准备

云端一般是 Linux，本仓库的 Windows 写法要换掉：

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium
export PYTHONUTF8=1
```

- 网络要能访问 `cdpn.io`（抓源码）和搜索引擎。`codepen.io` 本身有 Cloudflare 验证，不要去抓，也不要尝试绕过验证。
- 抓取脚本只用标准库；只有截图脚本 `B1/shot.py` 需要 Playwright。
- 以下命令都在仓库根目录执行。

## 5. 步骤

### 第 1 步：发现候选

用网页搜索找链接，写入新文件 `data_intake/B1/candidates_5.csv`（之后递增），三列：

```csv
url,target_tier,found_via
https://codepen.io/作者/pen/ID,T4,websearch-2026-11-10
```

- 搜索词用“档位 × 难度机制”组合，例如 `codepen scroll-state container query table`、`codepen pure css isometric city`、`codepen css only game checkbox`、`codepen animation-timeline view() landing page`。
- **不要**加 “no JavaScript”“pure CSS only” 这类限定词，含 JS 的作品也可能改造后收入。
- 其他线索：GitHub 上的 awesome 列表（css-art、pure-css、css-only 主题）里的 CodePen 链接；常产出难题的作者，如 argyleink、jh3y、bramus、una、thebabydino、utilitybend、giana、hexagoncircle、amit_sheen。
- 已判断过的链接都在 `B1/screening.csv`，重复提交会被第 2 步自动跳过，但尽量在发现时就避开。

### 第 2 步：获取源码

```bash
python scripts/codepen_collection/fetch_cdpn.py --candidates data_intake/B1/candidates_5.csv --out data_intake/B1/raw
```

- 脚本请求 `https://cdpn.io/{作者}/fullpage/{ID}`，默认每 2 秒一次，不要调快。
- 每个作品得到 `original_srcdoc.html`（原样）、`source.html`（去掉 CodePen 样板脚本）、`metadata.json`（作者、链接、时间、哈希、JS 与 CSS 特性标注）。
- 自动跳过三种情况：已在 `cases/` 里的作品、本目录已抓过的作品、取不到源码的页面。
- 脚本**只标注** JS，不因为有 JS 就丢弃。
- 每次运行的记录追加在 `B1/raw/fetch_log.jsonl`。

### 第 3 步：汇总

```bash
python data_intake/B1/triage.py
```

输出 `B1/triage.csv`：每个候选的 JS 字符数、CSS 字符数、元素数、keyframes 数、命中的 CSS 特性。用它先排掉明显太小的作品（元素很少、CSS 很短的单组件）。这张表每次按 `raw/` 现有内容整张重写，仓库里现存的那份是 10 月的旧快照，被覆盖属正常。

### 第 4 步：逐个筛选

每个候选都要看源码，拿不准的要看渲染结果：

```bash
python data_intake/B1/peek.py 作者__ID            # 压缩后的 CSS 与正文文字；加 --js 看脚本
python data_intake/B1/shot.py data_intake/B1/raw/作者__ID/source.html /tmp/shots/作者__ID --widths=1280,375
```

判断完用 `decide.py` 记一行（同一个 key 再记一次会覆盖旧行）：

```bash
python data_intake/B1/decide.py KEY DECISION TIER HITS REASON "证据" "备注" JS_POLICY
python data_intake/B1/decide.py una__myJOjQx accept T4 H2,H4,H6,H8 - "横向吸附日卡片；scroll-state(snapped)联动当前卡片；counter生成天数编号" "外部图标字体需替换" none
```

- `DECISION`：`accept`（建议入库，等用户挑）、`reject`、`hold`（合格但属于后续批次，或需再细看）。
- `证据`必须具体：写出哪段机制对应哪条特征，让别人不看源码也能复核。只写“很复杂”不算证据。
- `accept` 的备注里再写一句：**这个技术为什么对模型罕见或困难**。

## 6. 筛选标准

### 6.1 定档位（T1—T6）

问一个问题：这个视觉变化是谁在驱动的？完整定义见 [类型与难度模型 v2.1](../docs/difficulty_model_v2_1.md) 第三章。

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

### 6.5 含 JS 的作品

| 情况 | 处理 | `JS_POLICY` |
|---|---|---|
| 没有 JS，或只有 CodePen 样板脚本 | 正常判断 | `none` |
| JS 不是核心（埋点、装饰随机数、提示弹窗、懒加载） | 删掉后按阈值判断 | `remove` |
| 核心功能可用 CSS 等价实现（点击切换改 checkbox 或 `:target`，滚动监听改 `animation-timeline`），且改后仍达阈值 | 可收，备注里写清替换思路 | `replace` |
| JS 承担核心逻辑且 CSS 无法等价（复杂游戏规则、Canvas/WebGL、网络请求、随机生成内容） | 拒收，原因码 J1 | `reject` |

云端只需判断并写明处理思路，不必动手改写源码。

### 6.6 原因码

| 码 | 含义 |
|---|---|
| `-` | 建议入库 |
| D0 | 单组件、纯装饰、一条规则可复现 |
| D1 | 未达阈值 |
| C1 | 技术常见，或答案可联网检索（DEC-036） |
| J1 | JS 是核心且无 CSS 等价 |
| X1 | 源码不可用，或依赖外部资源、真实品牌人物 |
| R02 | 与其他候选重复 |
| T2/T3/T5/T6 | 合格但属于后续批次，`decision` 记 `hold` |
| U1/U2 | 用户在检查点未选，只由用户侧填写 |

## 7. 交付

- 在本仓库的新分支上提交，开 Pull Request，不要直接推 `main`。
- 改动只应出现在：`data_intake/B1/candidates_N.csv`、`data_intake/B1/raw/`、`data_intake/B1/triage.csv`、`data_intake/B1/screening.csv`。
- PR 说明里写清：新增候选数、抓取成功与失败数、各原因码数量、建议入库清单（链接、档位、命中特征、为什么难）、没做完的部分。
- 宁可少报。每轮建议入库控制在 10 例以内，方便用户逐个看。

## 8. 不要做

- 不要新建或修改 `cases/` 下任何目录，不要分配案例编号。本仓库的 `cases/` 只有各案例的 `metadata.json`，仅供抓取脚本去重。
- 不要写 `input.json`、`ground_truth.html`、评测规则；不要生成模型输出，不要评分。
- 不要调用任何大模型 API 来分类或筛选；不要读取或输出 `.env`、密钥等凭据。
- 不要用被测模型的得分来挑题。
- 不要修改 `project_state/`、`docs/` 下的文件（它们是主仓库的只读副本）；不要执行 `git reset`、`git clean`。
- 不要抓非公开作品，不要绕过 Cloudflare 验证；保留作者与原链接（公开作品默认 MIT 许可）。
- `accept` 只是建议，是否入库由用户决定。

## 9. 已知问题

- cdpn.io 导出的是编译后代码，没有 SCSS 原稿；个别作品的样式不随导出带出，抓到的页面没有 CSS，记 X1。
- 源码里的外部字体、图片、CDN 样式在离线环境可能加载不到，截图会走样；看渲染时不要加 `--offline`。
- 很新的特性（scroll-state、`::scroll-marker`、anchor 定位）需要较新的 Chromium，截图不对时先确认浏览器版本。
