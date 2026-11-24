# case-228 manual_v1 采分点

日期：2026-11-24。起草：Claude（duet）。状态：**草稿，待用户审核**（rule_status=DRAFT_PENDING_USER_REVIEW）。

| 文件 | 内容 |
|---|---|
| [eval_rules.json](eval_rules.json) | 规则，格式 `semantic-eval-rules/3.0`，结构参照 reference/examples_finished 的 case-222、217 |
| [build_rules.py](build_rules.py) | 由一张表生成 eval_rules.json；改规则请改这里后重跑 |

## 概况

- 依据：用户 2026-11-24 修改后的 [input.json](../../input.json)（提交 945c78f，sha256 记在规则里）。GT 只用来核对条件能被满足，不从 GT 反推要求。还没有任何模型输出。
- **12 条 Requirement，47 条 mandatory Evidence**：
  - D1 静态 9 条 Requirement、37 条 Evidence；
  - D2 动态 3 条 Requirement、10 条 Evidence，来自 motion_constraints 和功能需求里的点击切换。
- D1、D2 各占 50%（DEC-038）。
- 判定方式：纯程序 3 条，程序测量、边界交 Judge 21 条，纯 Judge 23 条。立体插画的视角、形状、方位只能看截图，所以 Judge 条目较多。
- **没有常识条目**：input 已经点名了全部部件和两种模式的外观，没有需要靠常识补的基本可用性。
- 门禁 G1–G5 与 case-222 相同；`forbidden` 为空，不另设禁令。
- 没写 `generation_prompt.txt`：仓库里没有 `output_prompt_v2.txt` 模板。

## 视口与状态

| 视口 | 考什么 |
|---|---|
| 1280×800 | 全部外观与交互 |
| 1920×1080 | 只考“视口正中”“随视口宽度等比缩放”“不出现滚动条” |

播放器按视口宽度缩放，手机宽度下机身只有约 40px，图标、接口都看不清，所以不设手机视口。动态条件的驱动是点击中央圆形按钮。

## 拆分原则（沿用 case-213/217/221/222 的约定）

1. **并列成员分别成条**：四个图标各一条存在与方位；屏幕、环形“左右居中”各一条；充电口、耳机孔各一条存在。
2. **一句话统一规定的性质只写一条**：四个图标的颜色、四个图标的大小。
3. **一句话里的独立事实拆开**：机身的扁平长方体、圆角、厚度；视角、透视、正面向上、长轴方向、底端位置；投影的颜色和形状。
4. **同一事实只放一条**：屏幕“黑色”与“纯黑色”、图标“黑色”与“半透明黑色”各合为一条。
5. **方位按机身自身方向**：有接口的一端为底端，面向正面、顶端朝上时的左右即机身左右。长轴方向和底端位置各由一条负责，其余方位按模型实际呈现的机身方向换算，不因朝向错误重复扣分。
6. **恢复按字面判**：第一次点击没有切换时，页面仍是默认外观，“再次点击回到默认外观”判 PASS，不与触发条件重复扣分。
7. **计分合并**：同一检查模板在并列成员上、由同一处实现造成的失败合为一组，只判一档。

## GT 核对

没有运行程序自查脚本。按 2026-11-24 的渲染核对（云端浏览器，1280 与 500 宽，见 [../../review_20261124/static_check.md](../../review_20261124/static_check.md)）逐条比对，GT 满足全部 47 条。容易有疑问的几条：

| 条件 | GT 情况 |
|---|---|
| SR-03.C2 带透视 | GT 有透视，但很轻，底端略宽于顶端 |
| SR-09.C1 投影在机身左侧 | 投影从左侧长边一侧露出，在画面中位于机身左下方 |
| DR-01.C1 点击中央按钮 | GT 的点击绑定在整个滚轮上，中央按钮在滚轮内，点击生效 |
| DR-02 发光外观 | 正面浅灰蓝、侧边端面白、蓝色外发光、接口变蓝、中央按钮浅蓝都可见。屏幕和滚轮被正面盖住的渲染问题不在任何条件里 |

## 请你重点看

1. **触发写法不一致**：业务背景和功能需求写“点击中央圆形按钮”，动效约束写“点击滚轮”。我按点击中央圆形按钮驱动：它在滚轮中央，两种说法都满足。如果模型只让圆环可点、中央按钮不可点，DR-01.C1 会判 FAIL，并按依赖带上整组 D2。要不要把动效约束改成同一说法，或者改成“点击滚轮任意位置”？
2. **D2 依赖链很重**：点击不能进入发光模式时，DR-01.C2 和 DR-02 的 6 条都按 DEC-029 一起判 FAIL，D2 几乎清零。这是现行政策的直接结果，我没有调整。
3. **SR-03.C2“带透视”**：GT 的透视很轻，Judge 可能难以判定。如果你认为这一条判不准，可以删掉，或者改成只在明显平行投影时判 FAIL。
4. **视口**：只用 1280×800 和 1920×1080，不设手机视口。
5. **屏幕和滚轮的上下位置没有条件**：修改后的 input 不再写“屏幕靠近顶端、滚轮靠近底端”，所以没有相应条件；屏幕和滚轮上下颠倒也能通过。如需考，请在 input 里补回。

## 条件清单

**SR-01 页面整体：组成、背景色、无滚动条**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-01.C1 | 页面只展示一台立体的音乐播放器模型及其投影 | judge | desktop |
| SR-01.C2 | 页面背景为纯色珊瑚红 | program+judge | desktop |
| SR-01.C3 | 页面不出现滚动条 | program | both |

**SR-02 播放器在视口中的位置与缩放**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-02.C1 | 播放器位于视口正中 | program+judge | both |
| SR-02.C2 | 整体尺寸随视口宽度等比缩放 | program+judge | both |

**SR-03 播放器的摆放、视角与朝向**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-03.C1 | 机身平放，从斜上方俯视 | judge | desktop |
| SR-03.C2 | 带透视 | judge | desktop |
| SR-03.C3 | 机身正面（有屏幕的一面）向上 | judge | desktop |
| SR-03.C4 | 机身长轴从左上斜向右下 | program+judge | desktop |
| SR-03.C5 | 底端在右下方 | judge | desktop |

**SR-04 机身形状与配色**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-04.C1 | 一个扁平的长方体机身 | judge | desktop |
| SR-04.C2 | 四角为圆角 | judge | desktop |
| SR-04.C3 | 侧边有可见的厚度 | judge | desktop |
| SR-04.C4 | 机身为明黄色 | program+judge | desktop |
| SR-04.C5 | 正面最亮，底端端面稍暗，左侧长边更暗 | program+judge | desktop |
| SR-04.C6 | 圆角处的颜色在相邻两面之间逐级过渡 | judge | desktop |

**SR-05 屏幕**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-05.C1 | 黑色圆角矩形屏幕 | judge | desktop |
| SR-05.C2 | 屏幕为纯黑色 | program+judge | desktop |

**SR-06 环形按钮、中央按钮与四个图标**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-06.C1 | 环形按钮 | judge | desktop |
| SR-06.C2 | 滚轮为白色 | program+judge | desktop |
| SR-06.C3 | 环形中央有一个圆形按钮 | judge | desktop |
| SR-06.C4 | 上方为文字“MENU” | program+judge | desktop |
| SR-06.C5 | 右侧为快进图标 | judge | desktop |
| SR-06.C6 | 左侧为快退图标 | judge | desktop |
| SR-06.C7 | 下方为播放/暂停图标 | judge | desktop |
| SR-06.C8 | 四个图标为半透明黑色 | program+judge | desktop |
| SR-06.C9 | 环面上有四个黑色小图标 | judge | desktop |

**SR-07 屏幕与环形按钮在正面上的位置关系**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-07.C1 | 屏幕和环形按钮都左右居中 | program+judge | desktop |
| SR-07.C2 | 屏幕和环形按钮都左右居中 | program+judge | desktop |
| SR-07.C3 | 环形直径略小于屏幕宽度 | program+judge | desktop |

**SR-08 底端端面的充电口与耳机孔**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-08.C1 | 黑色宽充电口 | judge | desktop |
| SR-08.C2 | 圆形耳机孔 | judge | desktop |
| SR-08.C3 | 底端端面上并排的黑色宽充电口和圆形耳机孔 | judge | desktop |
| SR-08.C4 | 充电口和耳机孔在底端端面中部 | judge | desktop |

**SR-09 投影**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| SR-09.C1 | 机身左侧的一块投影 | judge | desktop |
| SR-09.C2 | 投影为半透明黑色 | program+judge | desktop |
| SR-09.C3 | 投影为半透明黑色的圆角矩形 | judge | desktop |

**DR-01 点击切换发光模式、保持与恢复**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| DR-01.C1 | 点击中央圆形按钮可以切换显示模式 | program+judge | desktop |
| DR-01.C2 | 点击滚轮后页面进入发光模式并保持该状态 | program+judge | desktop |
| DR-01.C3 | 再次点击滚轮回到默认外观 | program+judge | desktop |

**DR-02 发光模式的外观**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| DR-02.C1 | 页面背景变为黑色 | program | desktop |
| DR-02.C2 | 机身正面变为浅灰蓝色 | program+judge | desktop |
| DR-02.C3 | 侧边和端面变为白色 | program+judge | desktop |
| DR-02.C4 | 机身轮廓带蓝色外发光 | judge | desktop |
| DR-02.C5 | 充电接口和耳机孔变为蓝色 | program+judge | desktop |
| DR-02.C6 | 中央圆形按钮变为浅蓝色 | program+judge | desktop |

**DR-03 两种模式下画面静止**

| 条件 | input 原句 | 判定 | 视口 |
|---|---|---|---|
| DR-03.C1 | 两种模式下画面都是静止的，没有持续或循环播放的动画 | program | desktop |
