# 原型设计 · 前端代码生成 —— 评分细则 v6

> **版本定位**
>
> v6 自 2026-10-18 起生效（DEC-038，计分政策 `evidence-severity/1.0`），替代 v5.2 的计分口径。
>
> 改变的只有计分：**计分单位从 Requirement 改为 Evidence**（每条 mandatory 条件），失败的 Evidence 按轻 0.5 / 中 1 / 重 1.5 扣分；退役“每条失败 Requirement 扣 2 分”的旧公式。Requirement 划分、Evidence 检测方法、门禁、运行环境和 eval_rules 生成方法沿用 v5.2。
>
> 执行步骤见 [评测流程 v6](evaluation_pipeline_v6.md)。Judge 与人工的一致性验证、外观评分不在当前评分范围内。v5.2 原文保留在 `docs/scoring_rubric_v5_2.md`，只用于复现历史结果。

---

# 一、评分目标与总体框架

## 1.1 评分对象

本文档用于评价模型根据 `input.json` 生成的单文件 HTML 原型是否满足题目要求。

一条标准评测实例至少包含：

```text
input.json
ground_truth.html
eval_rules.json
model_output.html
```

其中：

- `input.json`：题目原始需求，是 Requirement 的唯一需求来源；
- `ground_truth.html`：合法参考实现，用于元素锚点绑定和规则自检，不用于新增题目未声明的要求；
- `eval_rules.json`：由题目需求生成的 Requirement、Evidence、Driver、Assertion 与渲染配置；
- `model_output.html`：待评估模型输出。

最终至少输出：

```text
Quality Gate 结果
D1 静态实现质量
D2 动态实现质量
Final Score
逐 Requirement PASS / FAIL
Failure Attribution
```

---

## 1.2 一级评分结构

v6 使用两个一级评分维度：

| 维度 | 名称 | 考察内容 | 当前权重 |
|---|---|---|---:|
| **D1** | 静态实现质量（Static Quality） | 功能元素、内容、样式、尺寸、区域结构与元素关系 | **50%** |
| **D2** | 动态实现质量（Dynamic Quality） | 动态触发、行为、连续性、可逆性与最终视觉效果 | **50%** |

另外设置：

| 模块 | 作用 |
|---|---|
| **Quality Gate** | 在正式维度评分前检查 HTML 有效性及题目禁止事项 |

D1、D2 均以 0–10 分表示。

当前总分（缺一个维度时另一维度占 100%；门禁扣分见第三章与第六章）：

```text
Final Score = max(0, 0.5 × D1 + 0.5 × D2 − GatePenalty)
```

后续若 pilot evaluation 表明一级能力比例需要调整，可在 calibration 阶段统一修改；不得针对单个案例临时改变一级权重。

---

## 1.3 Evidence 是计分单位

v6 的评分层级：

```text
用户需求
   ↓
Requirement（组织与小计）
   ↓
Mandatory Evidence（计分单位）
   ↓
PASS / FAIL / UNRESOLVED
   ↓
FAIL 判严重度：轻 0.5 / 中 1 / 重 1.5
```

**Evidence 是计分单位；Requirement 负责组织条件、报告小计和归因。**

- 每条 mandatory Evidence 单独判定。一条 Evidence 内部可以有多个 DOM 检查、样式检查、几何断言、动态采样或截图判断，这些检测结果合起来只产生这一条 Evidence 的一个判定和一个严重度。
- 同一 Requirement 内不同 Evidence 失败，扣分累计。
- 一个可独立失败的事实写成一条 Evidence。不得为了增加扣分拆细条件，也不得把能独立失败的事实合并成一条。
- Requirement 的状态仍按“任一 mandatory Evidence FAIL → FAIL；全部 PASS → PASS；否则未决”报告，但它不再决定扣分。

DEC-029（`model-dependency-fail/1.0`）：已确认模型上游失败实际阻断下游 mandatory 条件时，该下游条件也判 FAIL，按它自己的严重度扣分。具体边界见 §6.6。

当前不设置：

- PARTIAL；
- Requirement 级固定扣分；
- 按案例或模型调整的扣分值。

---

# 二、总体评分流程（Pipeline）

整套评测按照以下顺序执行：

```text
┌─────────────────────────────────────────────────────────────┐
│ 输入：input.json + eval_rules.json + ground_truth.html      │
│      + model_output.html                                    │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
              ┌──────────────────────────────┐
              │ Step 0 · 读取评测配置         │
              │ tier / render_baseline       │
              │ measure_policy / scoring     │
              └──────────────┬───────────────┘
                             ▼
              ┌──────────────────────────────┐
              │ Step 1 · Quality Gate        │
              │ HTML / Script / Forbidden    │
              └──────────────┬───────────────┘
                             │
              严重违规 ──────┴──────→ 终止 / 按门禁规则处理
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Step 2 · D1 静态维度评估      │
              │ Region / Element / Relation  │
              │ Requirement                  │
              └──────────────┬───────────────┘
                             ▼
         逐 Evidence 判定 PASS/FAIL/UNRESOLVED
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Step 3 · D2 动态维度评估      │
              │ Driver → Sample → Assert     │
              │ → Screenshot / Judge         │
              └──────────────┬───────────────┘
                             ▼
         逐 Evidence 判定 PASS/FAIL/UNRESOLVED
                             │
                             ▼
              ┌──────────────────────────────┐
              │ Step 4 · FAIL 判严重度并扣分  │
              │ 计算 D1 / D2                 │
              └──────────────┬───────────────┘
                             ▼
              ┌──────────────────────────────┐
              │ Step 5 · Final Score         │
              │ + Failure Attribution        │
              └──────────────┬───────────────┘
                             ▼
                    输出 evaluation_record
```

核心顺序必须保持：

```text
先门禁
→ 再静态
→ 再动态
→ 再聚合
→ 最后诊断与报告
```

元素指派、Playwright、计算样式、几何谓词、多点采样等均是 D1 / D2 内部使用的检测方法，不改变上述主 Pipeline。完整的准备与运行步骤（含产物与执行者）见[评测流程 v6](evaluation_pipeline_v6.md)。

---

# 三、合规性门禁（Quality Gate）

Quality Gate 是正式维度评分前的前置检查。

原则上继承 v4 的门禁结构，但在 v6 中不再把一般代码质量单独设为一级评分维度。

## 3.1 门禁项

2026-11-16 起，新版本按 [输出契约 v2](output_contract_v2.md)（DEC-048）：允许 JS、外部字体和图片、字体外链样式表。G2/G3 不再按资源类别一概判违规；G4 仍检查单文件、页面 CSS 与 JS 内嵌。案例明确禁令继续有效。同一事实只扣一次，DEC-038 公式与严重度不变。旧冻结版本沿用原门禁，不回写历史结果。

| 门禁 | 检查内容 | 处理 |
|---|---|---|
| **G1** | HTML 能否解析为完整 DOM | 无法解析则本次输出无有效评分对象，终止正常评分 |
| **G2** | 是否存在题目禁止的 `<script>` 或事件处理属性 | 按题目禁令处理 |
| **G3** | 是否存在未经允许的外部资源 URL | 按题目约束处理 |
| **G4** | 是否满足单文件 / 内联 CSS 要求 | 按题目约束处理 |
| **G5** | 是否违反 `input.json.forbidden` 中的专属禁令 | 每条分别记录 |

## 3.2 门禁与 Requirement 的边界

Quality Gate 检查的是：

> “该输出是否属于一个可被本 benchmark 正常评估的合法提交。”

Requirement 检查的是：

> “合法提交是否完成具体用户需求。”

同一事实不得同时在门禁和 Evidence 中重复扣分。

例如：

- 题目明确禁止 JavaScript；
- 模型使用 JavaScript 实现核心滚动动画。

应先记录 G5 违规。

若该违规同时导致某 Dynamic Requirement 的 mandatory mechanism/compliance evidence 失败，应在结果记录中做**单一归因处理**，避免同一事实在最终分中被重复惩罚。

门禁扣分方式由中央计分政策（`preparation/evaluation_policy.json` 的 `scoring_policy`）统一配置，不允许评分器临时决定。案例规则文件中的 `scoring` 块是历史字段，不参与计分。

## 3.3 门禁计分政策

Quality Gate 分为 fatal 与 ordinary 两类。

若 HTML 无法正常解析或无法形成有效评分页面：

```text
fatal_gate = true
Final Score = 0
```

该 case 终止正常 Requirement scoring，并必须记录 fatal reason。

除 HTML fatal gate 外，当前契约或题目明确禁止的 JavaScript / forbidden mechanism、未经允许的外部资源，以及单文件、内联 CSS 等实现限制均属于 ordinary gate；DEC-048 已允许的 JS、字体和图片本身不构成违规。每违反一条独立 ordinary gate：

```text
GatePenalty += 2
```

Gate 与 Evidence 不得对同一事实重复扣分。若某 gate violation 已通过同一事实导致 Evidence 扣分，gate 记录仍保留，但该次 GatePenalty 必须抑制并注明 duplicate attribution。

---

# 四、静态维度（D1 · Static Quality）

## 4.1 考察内容

D1 评价模型是否完成 `functional_requirements` 与 `layout_constraints` 中的静态要求。

静态维度不再分成“功能分”“布局分”“视觉分”多个一级维度，而统一转写为 Static Requirements。

Static Requirement 分三类：

```text
Region Requirement
Element Requirement
Relation Requirement
```

三类 Requirement 下的 Evidence 使用同一套严重度档位（§6.2），不按 Requirement 类型设置不同扣分。

---

## 4.2 静态评分流程

```text
读取 Static Requirements
        ↓
按 Region 组织待测对象
        ↓
解析 Requirement target
        ↓
通过 GT anchor / 元素指派定位 model probe
        ↓
执行 Mandatory Evidence
        ├─ DOM / Content
        ├─ Computed Style
        ├─ Geometry
        ├─ Dimension / Color
        └─ Screenshot / Judge（必要时）
        ↓
逐条 Evidence 判 PASS / FAIL / UNRESOLVED
        ├─ FAIL → 判严重度（轻 0.5 / 中 1 / 重 1.5）
        └─ Requirement 状态与小计仅用于报告
        ↓
D1 = max(0, 10 − Σ 失败 Static Evidence 扣分)
```

---

## 4.3 Static Requirement 的划分

### 4.3.1 Region Requirement

Region 是页面中在语义功能和空间结构上相对独立的视觉区域，例如：

- Header；
- Hero；
- Main Content；
- Feature Section；
- Form Section；
- Footer。

Region 主要根据：

1. 题目明确区块描述；
2. 独立业务 / 语义功能；
3. 空间连续性；
4. 明显背景、边界或留白结构；

综合判断。

不得仅因为：

- DOM 多包一层 `<div>`；
- class 名不同；
- ground truth 使用不同容器；

就生成新 Region。

一个 Region 中的多个整体属性默认合并为一个 Region Requirement。

例如：

```text
Hero 占满首屏
+ 深色渐变背景
+ 主体内容整体居中
```

应生成：

```text
Region Requirement:
Hero 区域整体符合要求

Mandatory Evidence:
- viewport height
- gradient
- centered
```

而不是拆成三个独立计分 Requirement。

---

### 4.3.2 Element Requirement

Element Requirement 对应一个独立、可感知的页面对象，例如：

- 主标题；
- 副标题；
- 图片；
- 输入框；
- 按钮；
- Logo；
- 标签组；
- 卡片组；
- 指标组。

同一对象的多个属性不拆成多个 Requirement。

例如：

```text
蓝色 + 圆角 + 白字 + 48px 高度的按钮
```

仍然是一个 Button Requirement，四个属性只作为 Evidence。

---

### 4.3.3 同质元素组

同一语义角色下的同质重复元素，无论数量多少，整体只生成一个 Element Requirement。

例如：

```text
January–December
9 个技术标签
5 个导航菜单项
3 张结构一致的卡片
```

原则上均为一个 Requirement。

组内 Evidence 可检查：

- 数量；
- 内容；
- 顺序；
- 完整性；
- 样式一致性；
- 排列方式。

若题目对某个成员提出独立特殊要求，则可额外生成 Requirement。

---

### 4.3.4 Relation Requirement

Relation Requirement 用于评价多个对象之间的关系，而不是对象本身。

主要包括：

- **Order**：上下 / 左右 / 前后顺序；
- **Alignment**：左对齐、顶部对齐、等宽；
- **Spacing**：间距、均匀分布；
- **Containment / Grouping**：属于某一区域、位于某容器内部。

例如两个输入框本身均正确，但顺序反了：

```text
Input A Requirement → PASS
Input B Requirement → PASS
Input Order Relation → FAIL
```

不得因为一个关系错误同时把两个 Element Requirement 判 FAIL。

---

### 4.3.5 静态拆分的三个判断

当两个要求是否应拆开存在疑问时，使用以下判断：

1. **能否独立失败**：A 错误时 B 是否仍可能正确；
2. **用户能否独立指出错误**：用户是否可以自然地说“这里是另一个独立问题”；
3. **是否属于不同对象 / 不同关系**。

若三者中有明确独立性，倾向拆分。

反之，同一对象、同一区域或同一关系的多个属性应作为 Evidence 合并。

---

### 4.3.6 单一归因原则

同一事实只能归属于一个 Requirement。

该原则约束重复设置同一检查事实；DEC-029 对模型依赖阻断作出明确例外：已确认上游失败及其实际阻断的下游独立需求目前分别计 FAIL，暂不按共同根因合并扣分。不得为增加扣分点而新增或拆分 Requirement。

例如：

```text
“按钮位于输入框下方”
```

应归入 Relation Requirement。

不得同时在：

- Button Requirement；
- Input Requirement；
- Form Region Requirement；
- Relation Requirement；

中重复设置为 mandatory evidence。

---

## 4.4 元素定位与 GT Anchor

Static Requirement 的 Evidence 经常需要知道：

> ground truth 中的目标对象，对应 model output 中的哪个元素。

v6 继续采用 v4 的“GT anchor + 渲染树指派”方法。

### 4.4.1 Ground-truth anchor

阶段 B 为 ground truth 中与题目 Requirement 对应的对象建立 `gt_anchor`。

anchor 只回答：

> “目标对象是谁？”

不回答：

> “模型必须怎么实现？”

因此 anchor 不构成新的评分标准。

---

### 4.4.2 二分图元素指派

在固定渲染基线下：

```text
1. 渲染 ground_truth.html 与 model_output.html
2. 取可见元素：
   - bounding box
   - tag
   - innerText
   - 关键属性
3. 构造 GT element ↔ Model element 的代价矩阵
4. 求全局最优匹配
5. 低相似度配对丢弃
6. gt_ref 经匹配得到 model probe
```

沿用 v4 的基本代价函数：

```text
cost(g, m)
= 1 - [0.7 × text_sim(g,m) + 0.3 × geom_sim(g,m)]
```

其中：

```text
text_sim
= 归一化文本的字符级 Sørensen-Dice

geom_sim
= 基于中心点、宽、高差异的几何相似度
```

无文本元素时，将文本权重转移给 geometry。

全局匹配可采用：

- Jonker-Volgenant；
- Hungarian algorithm。

默认丢弃 `cost > 0.5` 的配对；阈值属于 evaluator 参数，需通过 calibration 检查。

---

### 4.4.3 定位失败处理

若 GT assignment 失败：

1. 回落到语义 / 文本 / 属性等 selector 兜底；
2. 若仍定位失败，则记录 `EVAL-ASSIGN-FAIL`；
3. 评测器自身定位失败不得自动等价于“模型 Requirement FAIL”；
4. 应进入 evaluator-side failure review。

类名不得作为跨模型主要定位依据，因为模型输出 class 命名不具有稳定可比性。

---

## 4.5 静态 Evidence 判定方法

Static Requirement 可组合多种 Evidence。

---

### 4.5.1 DOM / 内容证据

适用于：

- 元素是否存在；
- 标签类型；
- 文本；
- placeholder；
- value；
- 属性；
- DOM containment。

主要读取：

```text
tagName
textContent
value
attributes
DOM relationship
```

文本匹配应先归一化：

- 连续空白折叠；
- 首尾空白裁剪；
- 统一常见全角 / 半角标点；
- 统一引号与连字符表现。

题目明确要求大小写、异常标点或品牌拼写时，应保留其严格性。

---

### 4.5.2 渲染态计算样式

CSS 判定以浏览器渲染后的：

```js
getComputedStyle(element)
```

为主要依据，而不是在源码中搜索字符串。

浏览器负责：

- CSS 变量解析；
- 层叠；
- 继承；
- 简写展开；
- 相对单位换算；
- 最终颜色格式解析。

适用于：

- font-size；
- color；
- background-color；
- border-radius；
- opacity；
- gradient；
- position-related computed style（仅当属性本身就是题目要求）。

**原则：**

```text
同一效果只有一种直接属性表达
→ computed style

同一视觉效果可能由多种 CSS 技术实现
→ geometry / rendered effect
```

例如“居中”不应要求一定使用 flex。

---

### 4.5.3 几何谓词

布局效果优先根据渲染后的 geometry 判断。

通过：

```js
element.getBoundingClientRect()
```

获得：

```text
x / y / width / height
top / right / bottom / left
```

v6 继续使用封闭几何谓词词表。

建议保留：

| Predicate | 作用 |
|---|---|
| `same_row` | 元素是否横向同排 |
| `same_column` | 元素是否纵向同列 |
| `equal_size` | 宽 / 高是否近似一致 |
| `size_order` | 尺寸是否满足大小顺序 |
| `no_overlap` | 是否不存在不应有的遮挡 |
| `gap` | 间距范围 / 是否均匀 |
| `ordered` | 水平 / 垂直顺序 |
| `centered` | 相对容器或视口居中 |
| `fills` | 是否占满指定方向 |
| `viewport_anchored` | 滚动前后是否保持视口锚定 |
| `visible_extent` | 被裁剪后的可见整体跨度 |
| `relative_style` | 样式值与自身几何关系 |
| `no_horizontal_overflow` | 页面是否出现横向溢出 |

新增谓词必须：

1. 记录版本；
2. 有明确数学判定；
3. 不能只为单个案例临时创造。

无法表达的约束记录：

```text
EVAL-PREDICATE-GAP
```

---

### 4.5.4 尺寸与颜色

数值默认采用双容差：

```text
tolerance_px
tolerance_pct
```

建议默认：

```text
2px
2%
```

小尺寸属性（如 5px radius、10px progress bar）允许在 `eval_rules` 中单独覆盖。

颜色统一解析到 sRGB 后使用：

```text
CIEDE2000
```

默认：

```text
ΔE00 ≤ 2.0
```

渐变检查应比较：

- gradient kind；
- direction；
- color stops；

而不是比较 CSS 字符串写法。

必要时允许读取：

```text
::before
::after
```

伪元素计算样式。

---

### 4.5.5 Screenshot / LLM Judge

以下静态需求可能无法完全用 DOM / geometry / computed style 表达：

- “两端呈渐隐而不是硬裁切”；
- “背景图叠加暗色蒙版后整体明显变暗”；
- “某元素在视觉上明显突出于同类对象”。

这类 Evidence 可以使用：

```text
Playwright screenshot
+
题目原始要求
+
必要的结构化测量证据
+
LLM Judge
```

LLM Judge 只能判断题目明确提出、且脚本难以确定性表达的视觉要求。

不得因为 ground truth “看起来更好”而新增视觉要求。

---

## 4.6 静态测量状态

静态 Evidence 必须在稳定状态下读取。

统一策略：

```text
viewport = render_baseline
scroll = 指定静态采样位置（默认顶部）
pointer = no-hover
focus = none
time-driven animation = 冻结或移出测量影响
scroll-driven animation = 固定在 eval_rules 指定 scroll position
```

目标是避免：

```text
EVAL-MEASURE-UNSTABLE
```

即静态 Requirement 因碰巧读取到动画中间态而被误判。

---

## 4.7 Static Evidence 判定

每条 Static Evidence 单独判定：

```text
for evidence in mandatory_evidence:
    execute evidence
    verdict = PASS / FAIL / UNRESOLVED
    if verdict == FAIL:
        severity = 轻 0.5 / 中 1 / 重 1.5（依据失败事实判档）
```

Requirement 状态仅用于报告：任一 Evidence FAIL 则 Requirement FAIL。

D1 的扣分是所有失败 Static Evidence 严重度之和，计算见第六章。

---

# 五、动态维度（D2 · Dynamic Quality）

## 5.1 考察内容

D2 评价 `motion_constraints` 中的动态行为是否真正实现。

动态评分不只检查“有没有写 CSS 动画”，而检查：

```text
触发是否正确
机制是否合规
行为是否真实发生
变化是否连续
阶段关系是否正确
必要时是否可逆
最终视觉效果是否符合需求
```

---

## 5.2 Dynamic Requirement 的划分

Dynamic Requirement 按“独立动态子目标”划分。

判断一个动态子目标是否应成为独立 Requirement，主要看：

1. **能否独立失败**；
2. **用户能否独立指出该错误**；
3. **是否具有独立触发条件或独立状态区间**。

---

### 5.2.1 复合效果不按属性拆分

例如：

```text
图片进入视口时淡入并轻微放大
```

原则上是一个 Dynamic Requirement。

其 Evidence 可包括：

```text
Trigger: viewport entry
Opacity: 0 → 1
Scale: <1 → 1
Effect: fade-in + slight scale-up
```

不得拆成：

```text
淡入 Requirement
放大 Requirement
```

因为：

- 同一对象；
- 同一 Trigger；
- 同一阶段；
- 共同形成一个用户感知效果。

---

### 5.2.2 多阶段过程按独立子目标拆分

例如：

```text
卡片缩小并左移
→ 标题出现
→ 正文与指标随后出现
→ 整体上移淡出
→ 反向滚动恢复
```

若各阶段可独立失败，应分别形成 Dynamic Requirements。

否则将整段高难过程压成一个二值 Requirement，会造成大量模型全部得 0，降低区分度。

---

## 5.3 Dynamic Requirement 的执行流程

每条 Dynamic Requirement 按统一流程执行：

```text
1. Resolve Target
        ↓
2. Mechanism / Compliance Check（必要时）
        ↓
3. Apply Driver
        ↓
4. Multi-state / Multi-point Sampling
        ↓
5. Behavior Assertions
        ↓
6. Continuity / Reversibility（若要求）
        ↓
7. Screenshot Plan + Effect Judge（若需要）
        ↓
8. Mandatory Evidence 汇总
        ↓
9. Requirement PASS / FAIL
```

---

## 5.4 Mechanism / Compliance Check

机制只有在以下情况才可成为 mandatory evidence：

### 情形 A：题目明确约束实现机制

例如：

- 必须纯 CSS；
- 禁止 JavaScript；
- 必须与滚动位置连续绑定；
- 要求 scroll-driven animation；
- 要求特定现代 CSS 特性。

此时机制本身属于用户需求。

### 情形 B：题目只要求视觉效果，不限制机制

此时不得要求模型必须复制 ground truth 的具体实现方式。

例如：

```text
点击后展开
```

若在当前输出契约和案例禁令允许范围内可以通过多种机制完成，则只应检查：

- 状态是否可被真实驱动；
- 行为是否正确；
- 是否违反 forbidden。

不得要求“必须 checkbox hack”。

---

## 5.5 动态 Driver

Driver 由 Playwright 在浏览器中实际执行。

保留封闭 Driver 词表：

| Driver | 参数 | 用途 |
|---|---|---|
| `click` | `target` | 点击状态 |
| `hover` | `target` | 悬停状态 |
| `hover_then_leave` | `target` | 验证 hover 后可恢复 |
| `hover_each` | `targets[]` | 验证同组元素均有反馈 |
| `scroll_to` | `positions_pct[]` / `positions_px[]` | 多滚动位置采样 |
| `wait` | `sample_at_ms[]` | 时间驱动动画 |

共通参数：

| 参数 | 作用 |
|---|---|
| `settle_ms` | 等待 transition / layout 稳定 |
| `sample_at_ms[]` | 中间时刻采样 |
| `viewport` | 特殊动态采样视口 |
| `scroll_container` | 指定非 root 滚动容器 |

---

## 5.6 动态前置静态率检查

执行 Dynamic Requirement 前，可对目标对象进行 motion-dead 检查：

```text
1. 记录 driver 前的 style + geometry snapshot
2. 施加 driver
3. 记录 driver 后 snapshot
4. 若所有与该 Requirement 有关的状态完全一致
   → 记录 MOTION-DEAD
```

该检查不单独扣分。

它只是证明：

> 该 Requirement 的动态行为根本没有发生。

随后该 Requirement 对应的 behavior / effect evidence 应判 FAIL。

---

## 5.7 动态 Assertion

保留以下结构化断言：

### 5.7.1 `expect_before` / `expect_after`

用于：

```text
状态前 / 状态后
```

例如：

```text
hover 前 scale = 1
hover 后 scale > 1
```

---

### 5.7.2 `expect_at`

用于多采样点逐点判断。

例如：

```text
scroll = 0%   → opacity ≈ 0
scroll = 50%  → opacity 位于中间区间
scroll = 100% → opacity ≈ 1
```

---

### 5.7.3 `monotonic`

用于：

```text
“随滚动逐渐……”
```

T5 推荐采用多点采样，例如：

```text
0%
25%
50%
75%
100%
```

若 Requirement 要求进度条随页面滚动增长，则采样其：

- width；
- scale；
- clip extent；
- 其他等效可见几何量；

要求整体单调增加。

**关键原则：**

```text
有没有 animation-timeline
≠
动画行为真的随滚动正确发生
```

机制检查与行为检查必须分开。

---

### 5.7.4 `intermediate_value`

用于判断：

> 平滑变化还是瞬间跳变。

在动画中间状态采样时，若数值严格位于起点和终点之间，则可证明发生连续插值。

仅用于可动画的连续属性。

---

### 5.7.5 `continuity`

用于高难连续动画。

建议至少检查：

1. 多个中间 sample 均有有效状态；
2. 相邻 sample 不出现与需求不符的大幅跳变；
3. 变化不是仅发生在首尾端点；
4. 对 scroll-driven 动画，相近 scroll position 应产生相近视觉状态。

具体阈值由该 Requirement 的 `assertions` 明确声明。

---

### 5.7.6 `reversibility`

若题目明确要求反向滚动恢复：

```text
scroll A
→ scroll B
→ scroll A
```

记录两次 A 状态。

比较：

```text
computed style
geometry
必要视觉特征
```

要求在容差范围内恢复。

例如：

```text
20%
→ 70%
→ 20%
```

第一次 20% 与第二次 20% 应近似一致。

该断言可发现：

- 一次性 class；
- 只进不退的状态；
- 与 scroll position 不唯一对应的错误实现。

---

## 5.8 Screenshot Plan 与视觉 Effect

部分动态 Requirement 即使行为数值正确，也需要判断最终视觉效果。

例如：

- “自然淡入”；
- “多阶段出现节奏正确”；
- “左右标签无缝衔接”；
- “第一屏背景和文字共同淡出”。

`eval_rules` 可以为该 Requirement 声明：

```text
screenshot_plan
```

典型字段：

```text
scroll_pct
scroll_px
wait_ms
viewport
target_crop
```

Playwright 在指定状态截图。

LLM Judge 输入应至少包括：

```text
原始 motion requirement
关键截图
对应结构化 Evidence
待评模型输出的必要代码片段（若需要）
```

Judge 只判断无法被规则完全表达的 Effect，不重复判断已经由脚本确定的数值事实。

---

## 5.9 Dynamic Requirement 判定

每条 Dynamic Requirement 最终只产生：

```text
PASS
或
FAIL
```

例如：

```text
Dynamic Requirement:
图片进入视口时淡入并轻微放大

Mandatory Evidence:
✓ target resolved
✓ pure CSS compliance
✓ correct viewport-entry trigger
✓ opacity increases
✓ scale increases toward 1
✓ screenshot effect consistent

→ PASS
```

任一 mandatory evidence FAIL：

```text
→ 该 Evidence 判严重度并扣分
→ Requirement 报告为 FAIL
```

D2 的扣分是所有失败 Dynamic Evidence 严重度之和，计算见第六章。

---

# 六、评分聚合与扣分机制

政策版本：`evidence-severity/1.0`；依据：2026-10-18 用户确认，DEC-038。配置位置：`scripts/eval_rules_generation/preparation/evaluation_policy.json` 的 `scoring_policy`。

## 6.1 计分原则

> 每个维度从 10 分开始，按失败 Evidence 的严重度累计扣分。

- 计分单位是 mandatory Evidence。
- 每条 FAIL 的 Evidence 只判一档，扣分只计一次；同一 Requirement 内不同 Evidence 累计。
- PASS 扣 0；UNRESOLVED 不扣分，也不当作 FAIL。
- 不采用 `passed / total` 作为维度得分。

---

## 6.2 严重度

| 档位 | 扣分 | 判档依据 |
|---|---:|---|
| 轻（light） | 0.5 | 局部偏差；主要内容仍可识别，主要操作仍能完成 |
| 中（medium） | 1 | 明显偏差；影响部分内容呈现、布局关系或操作体验 |
| 重（severe） | 1.5 | 条件整体缺失、关键内容不可辨认，或要求的交互无法完成 |

判档规则：

1. 只对已确认 FAIL 的 Evidence 判档，判档不改变 PASS / FAIL。
2. 依据该 Evidence 的具体失败事实判断影响，不按条件名称、CSS 属性、案例难度、模型名称或已有总分判档；同类缺陷使用一致标准。
3. 材料不足以判档时记为严重度 UNRESOLVED，不默认中档。存在未判档的 FAIL 时不发布正式分。
4. 判档来源（程序规则、API 模型名或 Claude）写入运行记录；同一批次各模型使用同一种判档来源。
5. 文字截断类 FAIL 按 §6.2.1 锚点判档（DEC-046）。

### 6.2.1 文字截断锚点（DEC-046，`severity-anchor-text-truncation/1.0`）

适用：失败事实是要求完整显示的文字被裁切、遮盖、省略或溢出隐藏，如所选值、标签、按钮或链接文字。其他类型的 FAIL 仍按上表的通用定义判档。

判据（DEC-046 措辞修订 1.1，语义不变）：依次判断三个问题：不借助上下文能确定原文吗？能，判轻；否则借助选项列表或上下文能确定吗？能，判中；仍不能确定、会读成别的内容、文字基本不可见或操作无法完成，判重。

| 档位 | 文字截断时的判法 |
|---|---|
| 轻 0.5 | 只缺不影响辨认的少量字符，如末尾标点、符号或个别字母；只看可见部分就能确定原文 |
| 中 1 | 可见部分只是原文的片段，如只剩前几个字母，或多词文字只剩部分词；要借助选项列表、周边内容或猜测才能确定原文 |
| 重 1.5 | 借助上下文仍无法确定原文，或会读成别的内容；文字基本不可见；或截断使要求的操作无法完成 |

锚点只细化"主要内容仍可识别"和"关键内容不可辨认"在文字截断上的读法，不改变扣分值、公式和 PASS/FAIL。锚点 1.0 文本见 `scripts/eval_rules_generation/preparation/severity_anchors.json`，保留用于 `light-judge/1.2.1`；等义措辞 1.1 见 `scripts/eval_rules_generation/preparation/severity_anchors_v1_1.json`，用于 `light-judge/1.2.2`。从 R02 及轻量新协议起按对应冻结版本统一使用，历史结果不回写。

---

## 6.3 维度得分

```text
D1 = max(0, 10 − Σ 失败 Static Evidence 的扣分)

D2 = max(0, 10 − Σ 失败 Dynamic Evidence 的扣分)
```

维度最低为 0，不出现负分。扣分总量与条件总数无关：同样的失败在条件多或少的案例中扣分相同。

---

## 6.4 最终得分

```text
Static 与 Dynamic 均存在：BaseScore = 0.5 × D1 + 0.5 × D2
仅 Static 存在：          BaseScore = D1，D2 = NOT_APPLICABLE
仅 Dynamic 存在：         BaseScore = D2，D1 = NOT_APPLICABLE
两个维度均不存在：        case invalid / BLOCKED，Final Score = null

Final Score = max(0, BaseScore − GatePenalty)
GatePenalty = 2 × 独立普通门禁违规数
致命门禁（G1）FAIL：Final Score = 0
```

最终范围 0–10。保留聚合后的实际精度，不提前取整。

---

## 6.5 单一归因

同一事实只扣一次：

- 门禁与 Evidence 之间：门禁记录保留，GatePenalty 抑制并注明 duplicate attribution。
- 不同 Evidence 之间：同一直接事实已在某条 Evidence 扣分时，其余 Evidence 保留真实判定，扣分记 0 并注明归属（`duplicate_of`）。
- 重复设置同一检查事实属于规则缺陷，应修正规则，而不是靠去重掩盖。

---

## 6.6 已确认模型失败造成的依赖阻断

政策版本：`model-dependency-fail/1.0`；依据：DEC-029，扣分单位经 DEC-038 改为 Evidence。

1. 已可靠确认模型未实现必要的前置对象或行为，且该具体失败实际导致下游 mandatory 条件无法执行或观察时，下游条件判 **FAIL**，记录具体上游条件、失败证据及阻断原因。不新增判定状态。
2. 依赖必须指向具体事实、成员和分支，不能因整条上游 Requirement FAIL 就让全部下游失败。仍能独立观察的条件继续正常检查。缺少确认事实、依赖范围不清或仅定位器未找到对象时，仍为 **UNRESOLVED**。
3. 上下游条件各按自己的严重度扣分。暂不实施根因去重。
4. 模型依赖阻断已成为 FAIL，不因该阻断本身停止发布。不得把采证程序、环境、驱动、截图或 API 失败转换为模型 FAIL，也不得把独立未决隐藏在已有 FAIL 中。
5. 采集记录与判定记录分别保留：无法采到的下游状态不伪记为已采集。

---

## 6.7 UNRESOLVED 与发布

`UNRESOLVED` 表示评分系统无法可靠判断，不等于 FAIL，不扣分。它必须显式报告且不得静默删除。

出现以下任一情况时：

```text
publication_status = PARTIAL
formal_final_score = null
```

- 仍有 mandatory Evidence UNRESOLVED；
- 有 FAIL 的 Evidence 未能判档；
- 有门禁 UNRESOLVED。

此时允许输出基于已确认、已判档 FAIL 计算的 diagnostic D1、D2、BaseScore、GatePenalty 与 coverage，但不得发布为正式 Final Score。

---

## 6.8 不在当前计分范围

- Judge 与人工的一致性验证：后续工作。当前 Judge 结果没有人机一致性证明，报告中须注明判定来源。
- 外观评分：Codex 0–10 分与人工 1–5 分都不计入总分。
- 旧公式（每条失败 Requirement 扣 2 分）：已退役，新运行不再计算或报告；历史结果原样保留，不重算。

---

# 七、eval_rules 生成方法

本章说明：

> 每个案例的 Requirement 与 Evidence 如何从题目生成。

继续采用 v4 已经验证有效的“四阶段”结构，但将原“采分点”改为 Requirement + Evidence。

---

## 7.1 阶段 A · 只依据 input 生成“查什么”

LLM 输入：

```text
business_background
functional_requirements
layout_constraints
motion_constraints
forbidden
tier
允许使用的 Evidence / Predicate / Driver / Assertion 词表
```

**阶段 A 不得读取 `ground_truth.html`。**

输出：

```text
Static Requirements
Dynamic Requirements
每条 Requirement 的自然语言 target
Mandatory Evidence
自查报告
```

阶段 A 的目标只回答：

> “题目要求检查什么？”

不回答：

> “ground truth 是怎么实现的？”

---

## 7.2 阶段 A 的硬约束

### A. 不得发散

不得生成 input 未提出的：

- 元素；
- 功能；
- 样式；
- 动态行为。

### B. 描述效果，不描述 ground-truth 手段

除非题目明确约束机制，否则 Requirement 不应出现：

```text
必须 flex
必须 grid
必须某个 class
必须与 GT 相同 DOM 层级
```

### C. 同一事实不得重复归因

静态与动态之间、Region / Element / Relation 之间、Requirement 与 Gate 之间不得重复。

DEC-029 的模型依赖阻断按 §6.6 处理：上游失败与实际受阻的下游条件各按自己的严重度扣分；本条不提前实施根因去重。

条件是计分单位（§1.3）。一个可独立失败的事实写一条条件；同一事实不得在两条条件中重复设置。

### D. Evidence 必须可执行或可裁判

每个 mandatory evidence 必须明确属于：

- DOM；
- computed style；
- geometry；
- driver + assertion；
- screenshot judge；
- compliance。

---

## 7.3 阶段 B · Ground-truth anchor binding

阶段 B 才允许读取 `ground_truth.html`。

任务是：

```text
自然语言 target
→ gt_anchor
```

阶段 B 不得新增：

- 新 Requirement；
- 新视觉标准；
- 新尺寸；
- 新机制要求。

它只回答：

> Requirement 中说的对象，在 ground truth 里是哪一个。

---

## 7.4 阶段 C · Ground-truth 自检

生成的规则必须在 ground truth 上执行。

原则：

```text
所有规则型 Mandatory Evidence
必须在 ground_truth.html 上 PASS
```

若失败，不能直接降低 GT 分数，而要判断失败来源：

1. Evidence / predicate / parameter 写错；
2. input 与 ground truth 冲突；
3. evaluator 词表无法表达；
4. 渲染基线不支持；
5. GT 自身未实现 input 要求。

根据原因：

```text
修 eval_rules
或
修 input
或
修 ground_truth
或
记录 evaluator gap
```

---

## 7.5 阶段 D · 人工审核

人工重点审核：

```text
Requirement 粒度
同质组是否被拆碎
多阶段动态是否过粗
是否存在 double-count
mandatory evidence 是否真正来源于 input
是否把 GT 实现细节写成要求
是否可自动判定
容差是否合理
```

只有 A–D 完成后，`eval_rules.json` 才进入正式评测。

---

# 八、评测运行环境与实现规范

本章规定执行前述 D1 / D2 方法时的统一运行环境。

---

## 8.1 推荐执行栈

推荐：

```text
Python
+ Playwright
+ Chromium
```

其中：

### Python

负责：

- 读取 `eval_rules.json`；
- Requirement 调度；
- 聚合 Evidence；
- Failure Attribution；
- 分数计算；
- 输出 evaluation_record。

### Playwright

负责：

- 启动 / 控制浏览器；
- 加载 HTML；
- DOM 查询；
- `getComputedStyle()`；
- `getBoundingClientRect()`；
- hover / click；
- scroll；
- 等待；
- 多点采样；
- screenshot；
- viewport 切换。

### Chromium

作为实际 CSS / layout / animation 行为的执行环境。

---

## 8.2 渲染基线锁定

每个 benchmark 版本必须锁定：

| 项目 | 默认要求 |
|---|---|
| 浏览器 | Chromium，记录精确版本号 |
| 默认视口 | 1280 × 900 |
| deviceScaleFactor | 1 |
| 系统字体 | 通用系统字体族 |
| reduced motion | 不启用 `prefers-reduced-motion: reduce` |
| 网络资源 | 按题目规则限制 |
| timezone / locale | 若题目依赖则固定 |
| screenshot DPR | 与 baseline 一致 |

T5 / T6 对 Chromium 版本敏感。

若浏览器版本不支持题目所需 CSS 特性，应记录：

```text
EVAL-BASELINE
```

不得把 evaluator 环境缺陷记成模型失败。

---

## 8.3 Playwright 静态测量模板

概念流程：

```python
page.set_viewport_size(...)
page.goto(local_html)

# reset state
page.evaluate("window.scrollTo(0, 0)")
page.mouse.move(...)
page.evaluate("document.activeElement?.blur()")

# target
box = locator.bounding_box()
style = locator.evaluate(
    "(el) => getComputedStyle(el)"
)
```

正式实现应统一封装，而不是每个 case 单独写脚本。

---

## 8.4 Playwright 动态驱动模板

### Scroll

```python
for pct in [0, 25, 50, 75, 100]:
    page.evaluate(...)
    page.wait_for_timeout(settle_ms)
    sample(...)
```

### Hover

```python
locator.hover()
page.wait_for_timeout(settle_ms)
sample(...)
```

### Click

```python
locator.click()
page.wait_for_timeout(settle_ms)
sample(...)
```

每个 driver 的实现应固定，并与 `eval_rules` 的 action 词表一一对应。

---

## 8.5 Snapshot

动态采样建议统一记录：

```text
scroll position
timestamp
bounding box
selected computed styles
pseudo computed styles（如适用）
visibility
document geometry
screenshot ref
```

使 Requirement FAIL 后能够回溯证据。

---

# 九、eval_rules.json Schema

## 9.1 顶层结构

建议 v6 使用新的 Requirement-oriented schema。

```text
case_id
tier
schema_version

render_baseline
measure_policy

gt_anchors

quality_gate

static_requirements[]
dynamic_requirements[]

scoring

judge_config
reporting
```

---

## 9.2 Static Requirement

示例：

```json
{
  "id": "SR-L2-01",
  "dimension": "static",
  "region_id": "R2",
  "type": "relation",
  "description": "两个输入框纵向排列并保持左对齐",
  "targets": [
    {"gt_ref": "email-input"},
    {"gt_ref": "password-input"}
  ],
  "mandatory_evidence": [
    {
      "kind": "geometry",
      "assertion": {
        "type": "same_column",
        "min_overlap": 0.8
      }
    },
    {
      "kind": "geometry",
      "assertion": {
        "type": "ordered",
        "axis": "vertical",
        "direction": "asc"
      }
    }
  ]
}
```

---

## 9.3 Dynamic Requirement

示例：

```json
{
  "id": "DR-02",
  "dimension": "dynamic",
  "description": "图片进入视口时淡入并轻微放大",
  "targets": [
    {"gt_ref": "hero-image"}
  ],
  "mandatory_evidence": {
    "compliance": [
      {"type": "no_forbidden_script"}
    ],
    "driver": {
      "action": "scroll_to",
      "positions_pct": [20, 35, 50, 65]
    },
    "assertions": [
      {
        "type": "monotonic",
        "property": "opacity",
        "direction": "increasing"
      },
      {
        "type": "monotonic",
        "property": "scale",
        "direction": "increasing"
      }
    ],
    "screenshot_plan": [
      {"scroll_pct": 35},
      {"scroll_pct": 65}
    ]
  }
}
```

---

## 9.4 Scoring Config

计分配置只放在中央政策 `scripts/eval_rules_generation/preparation/evaluation_policy.json`，编译时写入 `compiled_eval_rules.json` 的 `scoring`：

```json
{
  "scoring_policy": {
    "mode": "evidence_severity",
    "version": "evidence-severity/1.0",
    "dimension_base": 10,
    "severity_deductions": {"light": 0.5, "medium": 1.0, "severe": 1.5},
    "dimension_floor": 0,
    "final_floor": 0,
    "static_weight": 0.5,
    "dynamic_weight": 0.5,
    "ordinary_independent_gate_penalty": 2
  }
}
```

不允许按案例、按 Requirement 或按模型自定义扣分值或权重。案例规则文件中残留的 `scoring` 块（旧版 `failure_penalty_per_requirement` 等字段）只是历史记录。

---

# 十、失败归因（Failure Attribution）

Failure Attribution 用于回答：

> 为什么某条 Evidence 失败？

归因码用于诊断，不额外计分。

---

## 10.1 Static Failure

建议：

```text
REGION-MISSING
REGION-VISUAL
REGION-GEOMETRY

ELEMENT-MISSING
ELEMENT-CONTENT
ELEMENT-TYPE
ELEMENT-VISUAL
ELEMENT-GEOMETRY

RELATION-ORDER
RELATION-ALIGN
RELATION-SPACING
RELATION-CONTAINMENT
```

---

## 10.2 Dynamic Failure

建议：

```text
MOTION-DEAD
TRIGGER-WRONG
MECHANISM-FORBIDDEN
MECHANISM-MISSING
BEHAVIOR-WRONG
TIMING-WRONG
CONTINUITY-FAIL
REVERSIBILITY-FAIL
EFFECT-WRONG
```

---

## 10.3 Evaluator-side Failure

以下属于 rubric / evaluator 自身问题，不得直接记为模型失败：

```text
EVAL-SELECTOR-FAIL
EVAL-ASSIGN-FAIL
EVAL-TOLERANCE
EVAL-AMBIGUOUS
EVAL-DOUBLE-COUNT
EVAL-BASELINE
EVAL-PREDICATE-GAP
EVAL-MEASURE-UNSTABLE
EVAL-JUDGE-UNGROUNDED
```

E 类归因出现频率应作为评分体系成熟度指标。

---

# 十一、评测结果报告

每次评测至少输出：

```text
Final Score（正式分或诊断分，及 publication_status）
D1 Static / D2 Dynamic

Quality Gate（含 duplicate attribution）

逐 Evidence：
- 维度、Requirement、Evidence 编号
- PASS / FAIL / UNRESOLVED
- FAIL 的严重度、扣分与判档理由
- 去重归属（duplicate_of）
- 证据引用（截图、采样、计算样式）
- 判定与判档来源

Requirement 小计：所属 Evidence 扣分之和
未决清单：未决 Evidence、未判档 FAIL、未决门禁
```

运行器输出 `score_result.json`，其中 `evidence_scores` 为逐 Evidence 记录，`requirements` 为 Requirement 状态与小计，`diagnostics.dimensions` 为维度扣分与得分。

`requirements_total`、`evidence_total` 只用于诊断和数据分析，不作为 `passed / total` 的计分分母。

---

# 十二、Calibration 与版本演进

## 12.1 Calibration 的对象

v6 需要用 pilot evaluation 数据检验：

1. Requirement 拆分粒度；
2. `c_static`；
3. `c_dynamic`；
4. D1 / D2 一级权重；
5. geometry tolerance；
6. assignment threshold；
7. dynamic sample positions；
8. Judge 稳定性；
9. 题目本身的经验难度。

---

## 12.2 Requirement-level 指标

至少记录：

```text
每条 Requirement PASS rate
不同模型间区分度
常见 failure attribution
是否所有模型都 PASS
是否所有模型都 FAIL
```

“所有模型都 FAIL”不自动意味着 Requirement 应删除。

首先判断：

- 题目确实很难；
- Requirement 是否拆得过粗；
- evaluator 是否失效；
- GT / input 是否冲突。

---

## 12.3 Case-level 指标

记录：

```text
失败 Evidence 数及各档数量（静态 / 动态）
D1、D2 扣分合计
D1
D2
Final
tier
```

重点观察：

- 是否大量案例触底；
- 是否大量案例集中 8–10；
- 高 tier 是否仍普遍高分；
- 模型排序是否符合人工判断。

---

## 12.4 Severity Calibration

当前严重度档位：

```text
轻 0.5 / 中 1 / 重 1.5
```

是初版参数，不是理论常数。后续调整必须基于：

```text
整批案例
×
多个模型
×
人工复核
```

不得：

```text
看到某一个 case 分太高
→ 单独提高这个 case 的严重度或扣分
```

也不得：

```text
看到某一个模型表现太好
→ 针对该模型修改规则或判档
```

---

## 12.5 后续工作（不在当前范围）

1. Judge 与人工的一致性验证：独立人工标签、预先确定的开发 / 验证划分和验收标准。
2. 严重度判档与人工判断的一致性。
3. 外观评分：维度、量表、截图条件、人评协议及是否并入总分，需另行确认。
4. 根因去重与扣分上限：需另行确认政策后实施。

---

## 12.6 设计立场

v6 的正确工作顺序：

```text
先定义 input
→ 再生成 Requirement
→ 再生成 Evidence
→ 再在 GT 上自检
→ 再评模型输出
→ 再按 Evidence 严重度计算得分
→ 最后看整体 calibration 数据
```

禁止：

```text
先决定某个案例“应该得几分”
→ 再反推条件、严重度或扣分
```

但允许：

```text
对整批 pilot data 做统计
→ 发现系统性偏差
→ 修改下一版统一规则
```

这属于 benchmark calibration，而不是样本级调分。

---

# 附录 A · v6 与 v4 的方法继承关系

v6 并未废弃 v4 已经形成的底层执行方法。

| v4 方法 | v6 中的去向 |
|---|---|
| GT element assignment | D1 / D2 target resolution |
| `getComputedStyle()` | Static / Dynamic Evidence |
| Geometry predicates | Static Requirement Evidence |
| CIEDE2000 | Static color Evidence |
| `scroll_to` / `hover` / `click` | Dynamic Driver |
| `expect_at` / `monotonic` | Dynamic Assertion |
| `intermediate_value` | Dynamic continuity Evidence |
| screenshot plan | Dynamic / Static Effect Evidence |
| LLM checklist | Requirement 中无法规则化的视觉 Evidence |
| GT 四阶段自检 | eval_rules 生成流程 |
| E 类归因码 | evaluator-side failure |

真正改变的是：

```text
v4:
低层采分点 → 独立计分 / 质量系数

v6（已退役）:
低层检测 → Mandatory Evidence
多个 Evidence → 一个 Requirement PASS / FAIL
Requirement FAIL → 固定统一 penalty

v6:
低层检测 → Mandatory Evidence（计分单位）
Evidence FAIL → 轻 0.5 / 中 1 / 重 1.5
Requirement → 组织与小计
```

---

# 附录 B · 核心规则速查

```text
【一级结构】
D1 Static = 50%
D2 Dynamic = 50%

【Static】
Region / Element / Relation Requirement

【Dynamic】
Independent Dynamic Sub-goal Requirement

【Evidence】
DOM
Computed Style
Geometry
Driver + Assertion
Screenshot + Judge

【计分单位：Evidence】
PASS → 扣 0
FAIL → 轻 0.5 / 中 1 / 重 1.5（同一 Evidence 只判一档）
UNRESOLVED → 不扣分；mandatory 未决或 FAIL 未判档 → 不发布正式分
已确认模型失败实际阻断下游 mandatory 条件 → 下游 FAIL，按自身严重度扣分（DEC-029）

【Requirement】
组织条件、报告小计；任一 Evidence FAIL → 报告为 FAIL

【Scoring】
D1 = max(0, 10 − Σ 失败 Static Evidence 扣分)
D2 = max(0, 10 − Σ 失败 Dynamic Evidence 扣分)
Final = max(0, 0.5D1 + 0.5D2 − 2 × 独立普通门禁违规数)
缺一个维度 → 另一维度 100%；G1 致命 → 0

【当前版本】
无 PARTIAL
无 Requirement 级固定扣分
无按案例 / 模型自定义扣分
同一事实只扣一次（门禁与 Evidence、Evidence 之间）
不计外观分；Judge 人机一致性验证为后续工作
ground truth 不得作为新 Requirement 来源
```
