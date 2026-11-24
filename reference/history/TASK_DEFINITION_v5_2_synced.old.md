# 任务定义（Task Definition）

> **适配版本：Scoring Rubric v6**（2026-10-18 起，DEC-038）
>
> 本文件定义“原型设计 · 前端代码生成”任务本身的输入、输出与任务边界。具体评分方法、Requirement 划分、Evidence 执行、浏览器运行环境与扣分规则以 [评分细则 v6](docs/scoring_rubric_v6.md) 为准，执行步骤见 [评测流程 v6](docs/evaluation_pipeline_v6.md)。

## 一、任务描述

评估大模型能否根据业务需求、视觉布局约束与动效约束，生成结构完整、可直接渲染的单文件 HTML 原型代码（含内联 CSS，**允许纯 CSS 动效，但不含任何 JavaScript**）。

本任务重点考察模型对自然语言需求的理解与前端实现能力，评分能力分为两个一级维度：

- **静态实现质量（Static Quality）**：页面区域、业务元素、文本内容、视觉样式、尺寸规格及元素之间的布局关系是否满足需求；
- **动态实现质量（Dynamic Quality）**：动效是否在正确对象与正确触发条件下真实发生，并满足题目要求的行为、连续性、可逆性与最终视觉效果。

模型输出首先经过 **Quality Gate** 检查，以确认 HTML 可解析、满足单文件要求、未使用题目禁止的脚本或外部依赖等。通过门禁后，再在浏览器渲染环境中依据 `eval_rules.json` 对静态与动态 Requirement 执行 Evidence 检查。

**动效范围说明：** 本基准在保持“无 JavaScript”前提下，将考察范围从纯静态布局扩展到**纯 CSS 可实现的动效**，包括过渡、关键帧动画，以及与滚动位置或元素进入/离开视口相关的滚动驱动效果。题目输入使用效果级与触发级语言描述动效，不向被测模型暴露具体 CSS 实现方式。凡必须依赖 JavaScript 才能实现的行为不在本任务范围内。

**任务输入形式说明：** 本基准采用**纯文本输入**（自然语言需求 → HTML 代码），区别于以设计截图为输入的多模态前端生成基准。该设计主要考察模型对自然语言需求的理解、分解与实现能力，而非图像理解能力。

---

## 二、期望输入（Expected Input）

### 2.1 输入字段

每道评测题的输入由四个结构化需求字段、题目特定禁止事项、全局禁止事项和输出格式要求组成。其中：

- 四个结构化字段及题目特定禁止事项存储在 `input.json`；
- 全局禁止事项和统一输出格式要求由全局 prompt 模板注入。

| 字段名 | 内容说明 | 示例 |
| :--- | :--- | :--- |
| `business_background`（业务背景） | 页面所属产品背景与使用场景，为模型提供语境；原则上不直接生成计分 Requirement | “开发一个面向企业内部的 OA 系统登录页，仅作为前端原型，不涉及后端逻辑。” |
| `functional_requirements`（功能需求） | 描述页面需要呈现哪些业务区域、业务元素、文本内容及结构归属关系 | “包含企业别名输入框、账号输入框、密码输入框、登录按钮，以及底部的‘忘记密码’链接、错误提示文本区域；每个输入框须关联文字标签。” |
| `layout_constraints`（布局约束） | 描述静态视觉、尺寸、颜色、排列、区域整体形态及响应式要求 | “PC 端表单区域宽度 400px、水平和垂直居中；移动端（<768px）表单宽度撑满可用区域并垂直堆叠。” |
| `motion_constraints`（动效约束） | 描述页面动态行为，以**效果级 + 触发级**语言说明“何时发生、什么对象发生什么变化”；无动效时可省略或置空 | “随页面向下滚动，顶部进度条从左到右逐渐填满；图片进入视口时淡入并轻微放大。” |
| `forbidden`（题目特定禁止事项） | 单题专属禁令，如禁止某类实现方式或投机路径 | 见 2.4 节 |

> **重要：** `input.json` 是 Requirement 的需求来源。`ground_truth.html` 只用于参考实现、元素锚点绑定与规则自检，不得反向新增题目未声明的要求。

---

### 2.2 字段边界规则

四个需求字段的职责由两层规则共同界定：

- **第一层 · 内容划分（“写什么”）**：每个字段负责不同类型的信息；
- **第二层 · 粒度限制（“不写什么”）**：避免把实现方法、过细技术细节或 ground-truth 特征泄漏给被测模型。

#### 第一层 · 内容划分

**业务背景** 只提供语境，不承担具体计分要求。通常包括：产品定位、目标用户、使用场景、原型边界声明等。

**功能需求** 描述“页面上有什么、内容是什么、属于哪里”。具体包括：

- 页面业务区域或区块（顶部导航、主体内容区、底部版权区、卡片组等）；
- 元素种类与数量（输入框、按钮、图片、卡片、标签组等）；
- 元素文本内容（标题、按钮文字、placeholder、链接文字等）；
- 元素层级与归属关系（按钮属于哪个表单、哪些卡片构成同一组等）；
- 题目明确要求的可访问性信息（如输入框须关联文字标签）。

**布局约束** 描述“页面静态状态下长什么样、怎么排列”。具体包括：

- 区域级视觉要求（区域高度、宽度、整体背景、整体居中、固定位置等）；
- 元素尺寸规格（宽高、字号、圆角、间距等）；
- 颜色与视觉规格（背景色、文字色、边框色、渐变等）；
- 元素之间的关系（横向并排、垂直堆叠、顺序、对齐、间距、包含关系等）；
- 响应式行为（断点值及断点两侧需要达到的实际布局效果）。

**动效约束** 描述“哪些元素在什么条件下如何变化”。具体包括：

- 时间驱动或悬停微动效；
- 循环动画；
- 状态变化过程；
- 滚动进度驱动；
- 元素进入 / 离开视口时的变化；
- 多阶段滚动过程；
- 若题目需要，可明确连续性、阶段顺序、反向恢复等动态性质。

#### 第二层 · 粒度限制

**功能需求字段不得包含：**

1. **HTML 标签提示**，如 `<h1>`、`<a>`、`<img>`、`<section>`、`<button>`、`<label>` 等；
2. **CSS 实现路径提示**；
3. 应由布局约束承担的纯视觉 / 几何细节；
4. 应由动效约束承担的动态过程描述。

**布局约束字段不得包含：**

- 用于限定实现手段的具体 CSS 属性或技术名称，如 `display: flex`、`position: fixed`、`transform: scale(...)`、`margin-top: ...` 等。

应改为**可观察结果**，例如：

```text
“始终贴在视口顶部”
“三张卡片横向并排”
“页面主标题整体居中”
“按钮为全圆角”
```

如果某个具体数值本身就是业务 / 视觉规格（如 400px 宽、10px 高、指定色号），应保留数值；禁止的是“用什么 CSS 属性实现”，不是禁止明确视觉规格。

**动效约束字段不得包含：**

- `@keyframes`、`animation-timeline`、`animation-range`、`scroll(root)`、`view()`、具体 transition 写法等实现机制提示。

应改为效果级 + 触发级语言：

```text
“随页面滚动逐渐填满”
“进入视口时淡入并轻微放大”
“滚出当前区域时逐渐淡出”
“标签随滚动横向移动，并保持连续、无明显跳变”
```

只有当**某种机制本身就是题目考点或禁令的一部分**时，才允许在任务要求中显式约束该机制，例如“必须纯 CSS 实现、禁止任何 JavaScript 滚动处理”。

**必须严格保留：**

A. **所有具体业务文本**：标题、按钮文字、列表项、placeholder、品牌大小写、特殊标点等应一字不差保留；

B. **题目明确指定的关键数值与色值**：如 `#070707`、`400px`、`40px`。这些属于用户可观察的硬规格，可由渲染态 Evidence 验证；

C. **动态中的关键时序 / 阶段关系**：若题目明确要求“先 A、再 B、最后 C”或“反向滚动恢复”，不得在清洗时删除。

#### 边界判定示例

| 表述 | 归属字段 | 是否合规 |
| :--- | :---: | :---: |
| “按钮文字为 Login” | 功能需求 | ✅ |
| “按钮宽度 200px、蓝色 `#1625e7` 背景” | 布局约束 | ✅ |
| “输入框 placeholder 为 ‘Enter Username’” | 功能需求 | ✅ |
| “h1 标题居中显示” | 布局约束 | ❌ 含 HTML 标签提示 → 改为“页面主标题居中显示” |
| “卡片以 `display:flex` 横向排列” | 布局约束 | ❌ 含实现路径 → 改为“三张卡片横向并排” |
| “Hero 左栏宽 40%、右栏宽 60%” | 布局约束 | ✅ 若 40/60 比例本身是明确视觉规格；不得写成 flex-basis 等实现属性 |
| “用户名输入框必须有 `<label>` 关联” | 功能需求 | ❌ 含标签提示 → 改为“用户名输入框须关联文字标签” |
| “使用 `animation-timeline:view()` 淡入图片” | 动效约束 | ❌ 暴露机制 → 改为“图片进入视口时淡入” |
| “卡片先缩小左移，随后标题出现，最后整体淡出” | 动效约束 | ✅ 保留阶段关系 |

---

### 2.3 输入规格约束

- **功能需求** 须明确覆盖所有需要实现的业务区域、业务元素与关键文本，不得依赖 ground truth 补充隐含要求；已要求元素应有的基本可用性（如所选文字完整可读、选项可见、图片不破图）属基本常识，可不写明而直接计分（DEC-037）；若题目考察可访问性，应使用用户可理解的效果描述，如“输入框须关联可识别的文字标签”，而不是直接指定 HTML 标签。

- **布局约束** 须提供足以判定正确性的静态视觉规格与关系约束；可包含明确尺寸、色号、断点与视觉比例，但不得提供 CSS 实现路径。对“居中、并排、固定顶部”等要求，应描述最终渲染效果。

- **动效约束** 须明确：**目标对象、触发条件、视觉变化**。复杂动效还应在需要时明确阶段顺序、连续性、反向恢复等性质。不得给出具体 CSS 动画机制，除非机制本身是考点。

- **所有要求必须可由纯 HTML + CSS 实现。** 凡必须依赖 JavaScript 才能实现的行为不得写入正式题目。

- **Requirement 可判定性：** 题目表述应尽量避免无法操作化的形容词，如“非常漂亮”“高级感很强”。若确需保留视觉主观要求，应保证可以通过截图 + LLM Judge 进行稳定二元判断。

---

### 2.4 禁止事项（Negative Constraints）

大语言模型可能主动补充题目未要求的实现或使用不允许的技术路径，因此需要显式声明禁止事项。禁止事项分为两类。

#### 全局禁止事项（所有题目通用）

以下禁止事项适用于所有案例，通过全局 prompt 模板统一注入：

- 禁止包含 `<script>` 标签或任何 JavaScript 代码；
- 禁止包含任何 JavaScript 事件处理属性（如 `onclick`、`onsubmit`、`onchange` 等）；
- 禁止引用外部 CSS 资源（如 Google Fonts、Tailwind CDN、Bootstrap 等），所有样式须通过 `<style>` 标签内嵌；
- 禁止引用外部图片 URL；题目需要图片时使用题目提供的本地资源或合法占位 `<img>`；
- 禁止引用或下载外部字体资源。默认使用通用字体族（sans-serif / serif / monospace）；仅当 input.json 明确指定本地命名字体时，才允许按指定顺序使用，并必须保留通用字体回退。字体不可用时按回退链渲染。

字体条款依据已确认的 [DEC-028](project_state/DECISIONS.md)；命名字体许可来自当前 `input.json`，不能由 GT 或模型自行补充，也不允许为满足指定字体而加载外部字体资源。

这些约束属于 Quality Gate / Compliance Evidence 的主要来源，不作为额外的静态视觉 Requirement 重复计分。

#### 题目特定禁止事项（单题专属）

某些题目可能需要额外禁止特定实现路径。例如题目考察某类纯 CSS 动态行为时，可禁止使用 JavaScript 滚动监听或其他绕过核心考点的方式。

示例：

```json
{
  "case_id": "case-XXX",
  "business_background": "...",
  "functional_requirements": "...",
  "layout_constraints": "...",
  "motion_constraints": "...",
  "forbidden": [
    "使用任何 JavaScript 滚动监听或 IntersectionObserver 实现动效",
    "使用 GIF、视频或逐帧图片序列冒充要求的连续动画"
  ]
}
```

若无题目专属禁令，`forbidden` 可省略或置为空数组。

> **禁止事项设计原则：** 禁令必须服务于任务边界或核心考点，不应为了限定 ground truth 的某一种实现方式而添加。

---

## 三、期望输出（Expected Output）

### 3.1 输出形式

被测模型须输出一份结构完整的单文件 HTML 原型，满足：

- 包含完整的 `<!DOCTYPE html>`、`<html>`、`<head>`、`<body>` 骨架；
- CSS 样式通过 `<style>` 标签内嵌；
- 不包含任何 JavaScript；
- 不依赖题目未允许的外部网络资源；
- 能在锁定的 Chromium 渲染基线中直接加载并形成可评页面；
- 页面静态与动态行为均应由 HTML + CSS 完成。

### 3.2 输出格式约束

为保障自动化评分器稳定解析，被测模型须遵守：

- **只输出 HTML 代码，不输出解释性文字。**
- **不使用 Markdown 代码块包裹。**
- 输出从 `<!DOCTYPE html>` 开始，以 `</html>` 结束。
- CSS 通过 `<style>` 内嵌于 `<head>`。

若输出包含 Markdown 包裹或额外自然语言，应由 Quality Gate / preprocessing 按统一规则处理，不得由不同案例临时采用不同清洗方式。

### 3.3 全局 Prompt 模板

输出格式约束与 2.4 节的全局禁止事项通过统一 prompt 模板注入，而非逐题重复声明。

实际主用模板为 `scripts/model_output_generation/output_prompt_v1.txt`，DeepSeek 与 Qwen 生成入口共用；`scripts/model_output_generation/prompt_template.txt` 为备用模板。以下为规范示例：

```text
请根据以下需求生成单文件 HTML 原型代码。

【业务背景】
{business_background}

【功能需求】
{functional_requirements}

【布局约束】
{layout_constraints}

【动效约束】
{motion_constraints}

【本题特定禁止事项】
{forbidden_list}

【全局禁止事项】
- 禁止包含 <script> 标签或任何 JavaScript 代码
- 禁止包含任何 JavaScript 事件处理属性（onclick、onsubmit、onchange 等）
- 禁止引用外部 CSS 资源，所有样式须通过 <style> 标签内嵌
- 禁止引用外部图片 URL；仅使用题目提供的本地图片或合法占位 <img>
- 禁止引用或下载外部字体资源。默认使用通用字体族（sans-serif / serif / monospace）；仅当 input.json 明确指定本地命名字体时，才允许按指定顺序使用，并必须保留通用字体回退。字体不可用时按回退链渲染。

【输出格式要求】
- 只输出 HTML 代码，从 <!DOCTYPE html> 开始，到 </html> 结束
- 不输出任何解释性文字、分析总结或客套话
- 不使用 Markdown 代码块包裹
- CSS 样式通过 <style> 标签内嵌于 <head> 中
```

该设计保证：

- **一致性**：所有题目共享同一组全局约束；
- **可维护性**：全局规则调整只需修改模板；
- **清晰性**：`input.json` 只保留单题特有需求；
- **公平性**：被测模型接收到的是题目需求，而不是 ground truth 实现细节。

---

### 3.4 参考实现与评测规则文件

每道题除 `input.json` 外，还应配套：

```text
ground_truth.html
eval_rules.json
```

二者作用不同，不能混用。

#### Part 1：`ground_truth.html` —— 合法参考实现

`ground_truth.html` 是人工编写或由真实项目反向工程整理得到的、能够实现题目需求的完整 HTML + CSS 页面。

其主要作用：

1. **证明题目可实现**；
2. **提供 GT Anchor**，帮助评分器把自然语言中的目标对象绑定到参考实现中的具体元素；
3. **作为 eval_rules 的阶段 C 自检对象**，检查规则是否能够在合法实现上通过；
4. 辅助发现 `input.json` 与参考实现之间的冲突。

`ground_truth.html` **不是 Requirement 的来源**，也不是要求模型复制的唯一实现方案。

不得因为 ground truth 使用了：

- 某个特定 DOM 包裹层；
- flex / grid 中的某一种；
- 某个 class 名；
- 某个未写入 input 的阴影、圆角或动画机制；

就把这些内容新增为对所有模型的强制要求。

---

#### Part 2：`eval_rules.json` —— Requirement-oriented Evaluation Rules

`eval_rules.json` 存储该案例的评分规则，其基本结构由以下部分组成：

```text
Quality Gate
Static Requirements
Dynamic Requirements
Mandatory Evidence
GT Anchors
Driver / Assertion / Screenshot Plan
Scoring Config
```

##### A. Static Requirements

静态 Requirement 按三类组织：

- **Region Requirement**：区域整体高度、背景、整体位置等；
- **Element Requirement**：单个业务对象或同质元素组本身；
- **Relation Requirement**：多个对象之间的顺序、对齐、间距、包含关系等。

##### B. Dynamic Requirements

动态 Requirement 按**独立动态子目标**组织，不按 CSS 属性或机制拆分。

一个 Requirement 可包含 Trigger、Mechanism / Compliance、Behavior、Continuity、Reversibility、Effect 等 Mandatory Evidence。

##### C. Evidence

Evidence 是计分单位：每条 mandatory Evidence 单独判 PASS / FAIL / UNRESOLVED，FAIL 按轻 0.5 / 中 1 / 重 1.5 扣分（DEC-038，详见评分细则 v6 第六章）。根据需求可使用：

- DOM / 文本检查；
- 浏览器 `getComputedStyle()`；
- `getBoundingClientRect()` 几何谓词；
- 尺寸与颜色容差；
- Playwright hover / click / scroll / wait 驱动；
- 多点动态采样；
- `monotonic`、`intermediate_value`、`continuity`、`reversibility` 等断言；
- Playwright 截图 + LLM Judge。

Requirement 负责组织条件和报告小计：所有 Mandatory Evidence 通过，Requirement 报告为 PASS；任一失败则报告为 FAIL。扣分按失败 Evidence 的严重度累计，同一 Requirement 内不同 Evidence 的扣分相加。

DEC-029（`model-dependency-fail/1.0`）：已确认模型上游失败实际阻断下游 mandatory 条件时，下游也判 FAIL，不新增状态，上下游各按自己的严重度扣分。评测器故障或原因不明的缺证据仍为 UNRESOLVED 并阻止正式发布。暂不实施根因去重；同一直接事实只扣一次（门禁与 Evidence、Evidence 之间）。完整边界见评分细则 v6 §6.5–6.7。

##### D. 渲染态优先原则

评分不以源码字符串精确匹配为主要方法。

例如：

- “居中”应优先检查渲染后的几何关系，而不是要求 `display:flex`；
- “背景色为指定颜色”应读取 `getComputedStyle()` 后比较解析值；
- “随滚动逐渐变化”应通过 Playwright 在多个滚动位置采样实际状态，而不是只检查源码是否出现 `animation-timeline`；
- 同一视觉结果允许不同合法 CSS 实现。

##### E. Requirement 生成原则

Requirement 必须从 `input.json` 生成，不能从 ground truth 反推。

生成流程原则上为：

```text
Stage A：只看 input，生成 Requirement + Evidence
    ↓
Stage B：读取 GT，只绑定 target / gt_anchor
    ↓
Stage C：在 ground truth 上执行规则自检
    ↓
Stage D：人工审核粒度、重复、可判定性
```

详细 Schema、几何谓词词表、Dynamic Driver / Assertion、Playwright 运行基线与 Failure Attribution 以评分细则为准。

---

## 四、任务边界与评分关系

### 4.1 任务定义与评分细则的职责分工

`TASK_DEFINITION.md` 负责回答：

```text
模型要接收什么输入？
模型要输出什么？
允许 / 禁止什么？
题目需求应如何表述？
```

`scoring_rubric.md` 负责回答：

```text
Requirement 如何生成？
Evidence 如何执行？
Playwright / Chromium 如何测量？
静态与动态如何判 PASS / FAIL？
失败如何扣分？
最终分如何聚合？
```

两份文档不得重复维护同一套技术细节；当评分实现更新时，应保证 Task Definition 中的概念名称与边界同步即可。

### 4.2 当前评分思想摘要

为避免 Task Definition 与评分细则再次出现概念漂移，当前版本统一采用以下术语：

```text
用户需求
→ Requirement（计分单位）
→ Evidence（检测单位）
→ PASS / FAIL
→ Failure Penalty
```

一级能力结构：

```text
D1 静态实现质量
D2 动态实现质量
Quality Gate 前置门禁
```

Task Definition 不规定 penalty 的具体数值；具体扣分参数由评分细则和 `eval_rules.json` 的 scoring config 管理。

---

## 五、相关文档

- 评分细则：[`docs/scoring_rubric.md`](./docs/scoring_rubric.md)
- 难度模型：[`docs/difficulty_model.md`](./docs/difficulty_model.md)
- 主用全局 Prompt 模板：`scripts/model_output_generation/output_prompt_v1.txt`（备用：`scripts/model_output_generation/prompt_template.txt`）
