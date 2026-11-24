# case-217 manual_v3 采分点审核稿

2026-11-23，Claude 起草；2026-11-24 用户确认 5 个问题全部按建议处理，规则状态 `USER_CONFIRMED_FROZEN`（sha256 见 R02 轮次 case-217 评测记录）。

**14 条 Requirement / 53 条 mandatory Evidence，全部来自 input，只计 D1。** 只在 1280×900 一个桌面视口采证。

规则：[eval_rules.json](eval_rules.json)（由 [build_rules.py](build_rules.py) 生成，引文逐条核对为 input 原文子串）。input：[input.json](../../input.json)（sha256 `d78afc39…a1a9b45`）。GT：[ground_truth.html](../../ground_truth.html)。

案例目录里有 `case-217-duet.html`（疑似模型输出）。起草时没有打开它，规则未参考任何模型输出。

## 拆分原则（沿用 case-227 约定）

- **并列成员逐个成条。** 平台、高塔、矮塔三个体块的形状/可见面、配色、受光方向各一条；两塔“立在平台上”各一条；三个图标的地址和白色各一条。
- **整组性质只写一条。** 塔群居中、署名区行序、图标并排顺序、整体光影自然。
- **同一事实只放一条。** 顺序只由 SR-13.C8/C9 负责，内容条件不含位置；“一高一矮”由矮塔约三分之二高负责；门洞在哪一面只由朝向条件负责。
- **计分时合并。** 同一检查模板在并列成员上、同一处实现造成的失败合为一组，只判一档。
- **不加常识条件。**

## 建筑自身视角怎么判（frame_policy）

input 规定左右前后按建筑自身视角描述。规则这样换算：

- **正面 = 门洞所在的高塔侧面**；没有门洞时取高塔朝画面右下方的可见侧面。
- 正面朝画面右下方时：建筑右侧面 = 画面左侧的可见面；“左前上方”光源 = 画面右上方。GT 正是如此。
- **朝向错误只扣一次。** 朝向只由 SR-09.C1 判；平台长边、矮塔贴哪一面、光照方向都按模型实际画出的正面换算。例如模型把整座建筑镜像，只扣 SR-09.C1，其余相对关系正确仍算 PASS。

## Requirement 结构

| Requirement | 范围 | 类型 | Evidence 数 |
|---|---|---|---:|
| SR-01 | 页面：单屏、背景色、组成 | region | 3 |
| SR-02 | 插画位置、大小、周围光晕 | relation | 3 |
| SR-03 | 视角与投影 | region | 2 |
| SR-04 | 平台 | element | 3 |
| SR-05 | 高塔 | element | 2 |
| SR-06 | 矮塔 | element | 2 |
| SR-07 | 两塔与平台 | relation | 3 |
| SR-08 | 矮塔与高塔 | relation | 4 |
| SR-09 | 建筑朝向 | relation | 1 |
| SR-10 | 屋顶槽 | element | 2 |
| SR-11 | 门洞与洒出的灯光 | element | 4 |
| SR-12 | 体块配色与光影 | region | 7 |
| SR-13 | 署名区内容 | element | 9 |
| SR-14 | 署名区位置与样式 | element | 8 |

判定分工：程序 9 条，程序测量 + 边界交 Judge 21 条，纯 Judge 23 条。

门禁：G1 致命（无法形成可评测 DOM）；G2–G4 为通用契约；**G5 为 input.forbidden**（运行时按 forbidden 序号编为 G5.1）：插画部件不得用图片、SVG、Canvas、WebGL 绘制，署名区图标除外。违反时只记门禁，不再因同一画法扣条件。

## 完整采分点

### SR-01 页面整体：单屏、背景色、组成（region）

- **SR-01.C1** 1280×900 下页面不出现滚动条且不能滚动：① window.innerWidth − documentElement.clientWidth 为 0（无竖向滚动条），window.innerHeight − documentElement.clientHeight 为 0（无横向滚动条），或截图中看不到滚动条；② 在页面中部滚动鼠标滚轮并按 End、PageDown 键后，scrollX、scrollY 仍为 0。两项都满足才通过。
  - 判定：程序；证据：`dom_interaction`；来源：`layout_constraints`「不出现滚动条」。备注：用户 2026-11-23 确认：按“有无滚动条、能否滚动”判，不比较 scrollHeight（GT 文档高 923 但根元素 overflow:hidden，属于单屏）。滚动只用用户式输入（滚轮、按键），不用 window.scrollTo——GT 上 scrollTo 能移动 23px，但用户滚不动。
- **SR-01.C2** 插画和署名区以外的页面背景为蓝紫色（色相在蓝与紫之间）；采样页面四角和上沿中点。黑、灰、白、纯蓝、红、粉等明显不是蓝紫的不满足。
  - 判定：程序测量，边界交 Judge；证据：`computed_color`；来源：`layout_constraints`「背景为蓝紫色」。备注：程序报告采样点 HSL（GT 四角 H≈255°、S≈0.76、L≈0.34）；不预设色相阈值，非典型色交 Judge。光晕区域归 SR-02.C3，不在此判。
- **SR-01.C3** 页面上可见内容只有一幅立体插画和一个署名区，没有额外的标题、说明文字、按钮、导航或其他装饰区块。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`functional_requirements`「页面由画面中央的一幅立体插画和右下角的署名区组成」。备注：程序列出署名区以外的可见文字节点（GT 为空）；非文字的额外区块看截图。插画和署名区各自的位置由 SR-02、SR-14 负责，不在此判。

### SR-02 插画在画面中的位置、大小与周围光晕（relation）

- **SR-02.C1** 插画（平台与塔楼的可见像素外接框）中心同时位于视口中心的左侧和上方，且只是略微偏离，插画整体仍在画面中央区域；位于正中、偏向右或下、或明显贴近某一边的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`functional_requirements`「插画位于画面中央略偏左上」。备注：程序报告中心相对视口中心的 dx、dy（GT −24、−46）；“略”不设数值上限，偏离较大时交 Judge。
- **SR-02.C2** 插画可见外接框宽度约为视口宽度的三分之一；明显过小或明显过大的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`functional_requirements`「整体宽度约为画面宽度的三分之一」。备注：程序报告宽度比（GT 0.305）。用户 2026-11-24 确认：0.25–0.42 内程序直接判 PASS，范围外交 Judge。
- **SR-02.C3** 插画建筑周围的背景上有一团比远处背景更亮的紫色光晕，光晕包围或衬托插画；背景全屏均匀、光晕远离插画、或光晕不是紫色系的不满足。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「插画建筑周围有紫色光晕」。备注：程序对比插画中心附近与页面角落的背景亮度（隐藏插画后采样；GT L 0.50 对 0.34）；形状与位置由 Judge 判。

### SR-03 插画的视角与投影（region）

- **SR-03.C1** 插画呈从斜上方俯视的效果：能看到体块的顶面，同时也能看到立面；纯正面立面图（看不到顶面）或正上方垂直俯视（看不到立面）的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「插画从斜上方俯视」。
- **SR-03.C2** 插画为平行投影：同一体块上互相平行的棱在画面中仍保持平行，不向远处汇聚；同样长的棱远近一致，远处不缩小。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「采用平行投影、远处不缩小」。备注：程序可报告场景祖先元素的 perspective 值作辅助，但只看画面结果：perspective 极大、实际看不出汇聚的不判 FAIL。

### SR-04 平台（element）

- **SR-04.C1** 插画中有一块平台：厚度明显小于长和宽的扁平板，顶面为长方形（两组边长度不同），不是正方形、圆形或不规则形。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「一块扁平的长方形平台」。
- **SR-04.C2** 平台同时可见顶面和两个相邻侧面（显示出板的厚度）；只看到顶面一个平面、或只能看到一个侧面的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「能同时看到每个体块的顶面和两个侧面」。
- **SR-04.C3** 平台与建筑正面（门洞所在的高塔侧面）平行的那一组边是较长的边；与建筑侧面平行的一组边较短。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「平台在建筑正面的一边较长」。备注：按模型实际呈现的建筑正面判断，不按画面方向；朝向错误只由 SR-09.C1 负责，此处不重复扣。

### SR-05 高塔（element）

- **SR-05.C1** 插画中有一座高塔，为截面呈正方形（顶面四边等长）的竖直方柱体；圆柱、锥体、明显长方形截面或只是平面色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「一高一矮两座方柱形塔楼」。
- **SR-05.C2** 高塔同时可见顶面和两个相邻侧面，三个面彼此可区分（明暗或颜色不同）。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「能同时看到每个体块的顶面和两个侧面」。

### SR-06 矮塔（element）

- **SR-06.C1** 插画中有一座矮塔，为截面呈正方形（顶面四边等长）的竖直方柱体；圆柱、锥体、明显长方形截面或只是平面色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「一高一矮两座方柱形塔楼」。
- **SR-06.C2** 矮塔同时可见顶面和两个相邻侧面，三个面彼此可区分（明暗或颜色不同）。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「能同时看到每个体块的顶面和两个侧面」。备注：矮塔一个侧面紧贴高塔，但另两个可见侧面与顶面仍应能看到；GT 中矮塔顶面、正面、右侧面均可见。

### SR-07 两座塔与平台（relation）

- **SR-07.C1** 高塔底部落在平台顶面上，看起来立在平台上；悬空、陷入平台、或位于平台之外的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「两座塔立在平台中部」。
- **SR-07.C2** 矮塔底部落在平台顶面上，看起来立在平台上；悬空、陷入平台、或位于平台之外的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「两座塔立在平台中部」。
- **SR-07.C3** 两座塔作为整体位于平台中部，塔群四周（前后左右）都还露出一圈平台顶面；塔贴到或伸出平台任一边缘的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「四周留有平台空地」。

### SR-08 矮塔与高塔（relation）

- **SR-08.C1** 矮塔顶面（截面）明显小于高塔顶面。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「矮塔截面较小」。
- **SR-08.C2** 矮塔高度约为高塔高度的三分之二（比较两塔立面竖直棱的屏幕长度）；与高塔差不多高、或不到高塔一半的不满足。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「高度约为高塔的三分之二」。备注：同为平行投影，竖直棱屏幕长度之比即高度比（GT 14:22≈0.64）。程序能定位两塔竖直棱时报告比值，否则交 Judge。用户 2026-11-24 确认：0.55–0.78 内程序直接判 PASS，范围外交 Judge。
- **SR-08.C3** 矮塔紧贴在高塔的右侧面上。按建筑自身视角，门洞所在的侧面是正面，高塔另一个可见侧面就是右侧面；所以本条只看：矮塔与门洞是否分处高塔的两个不同可见侧面——门洞在高塔的一个可见侧面上，矮塔紧贴在高塔的另一个可见侧面上（从画面看，矮塔挡住该侧面的一部分）。两塔之间没有空隙，也不互相穿插到可见程度。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「紧贴高塔右侧面」。备注：按模型实际呈现的建筑正面换算左右；朝向错误只由 SR-09.C1 负责。贴在左侧面、正面或背面，或与高塔分离的不满足。
- **SR-08.C4** 矮塔在它所贴的高塔侧面（高塔没有门洞的那个可见侧面）上沿水平方向居中，前后两边露出的高塔侧面宽度大致相等；贴到前角或后角的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「且居中」。备注：矮塔不贴在高塔侧面时（SR-08.C3 FAIL），本条按 DEC-029 视为被阻断，同判 FAIL。

### SR-09 建筑朝向（relation）

- **SR-09.C1** 建筑正面（门洞所在的高塔侧面）朝向画面右下方：它是高塔在画面右侧的那个可见侧面，面的外法线指向观察者右前方。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「小建筑的正面朝向画面右下方」。备注：正面由门洞确定；没有门洞时正面无从确认，按 DEC-029 与 SR-11.C1 同判 FAIL。

### SR-10 屋顶槽（element）

- **SR-10.C1** 高塔顶面中央有一个方形槽，槽的四边与顶面边缘之间都留有一圈窄边，四边窄边宽度大致相等；槽偏到一边、贴边、占满整个顶面或不是方形的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「高塔顶面中央有一个向下凹陷的方形屋顶槽，四周留出一圈窄边」。
- **SR-10.C2** 屋顶槽看起来向下凹陷：槽内比四周窄边更暗，并能看出槽壁或内阴影等表现深度的明暗；与顶面同色的描边方框、凸起的方块、或只是一块无层次的平涂色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「向下凹陷」。备注：只按视觉判，不要求几何上真的下沉（GT 也靠暗色和内阴影表现）。

### SR-11 门洞与洒出的灯光（element）

- **SR-11.C1** 高塔一个可见侧面上有一扇方形门洞（在该面上为正方形，在画面中呈与该面一致的平行四边形）；它在哪一面由 SR-09.C1 负责，此处只判存在、所在体块与形状。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「正面有方形门洞」。
- **SR-11.C2** 门洞内部明显发亮，像有灯光，从周围塔面中突出出来；与塔面同色调的暗色门洞不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「洒出内部灯光」。
- **SR-11.C3** 门洞的灯光洒到门外：门洞前方的平台顶面上有与门洞灯光同色系的光斑，从门洞下沿开始，贴在平台顶面上。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「洒出内部灯光」。备注：光斑漂在空中、与门洞分开、或竖立在墙面上的不满足。
- **SR-11.C4** 洒出的灯光由亮到暗渐变：靠近门洞处最亮，越远越暗淡，逐渐融入平台；整片均匀不变的色块不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「门洞中洒出的灯光由亮到暗渐变」。备注：没有洒出的灯光时（SR-11.C3 FAIL），本条按 DEC-029 同判 FAIL。

### SR-12 体块配色与光影（region）

- **SR-12.C1** 平台的各个面以高饱和的蓝紫色为主，与背景同一色调；灰、黑、白等低饱和色或与背景色相明显不同（如绿、橙、红）的不满足。门洞与光斑的品红灯光不属于体块配色。
  - 判定：程序测量，边界交 Judge；证据：`computed_color`；来源：`layout_constraints`「体块为高饱和的蓝紫色系，与背景同一色调」。备注：程序采样各面主色并报告 HSL，与 SR-01.C2 的背景色相对比；非典型交 Judge。
- **SR-12.C2** 高塔的各个面以高饱和的蓝紫色为主，与背景同一色调；灰、黑、白等低饱和色或与背景色相明显不同（如绿、橙、红）的不满足。门洞与光斑的品红灯光不属于体块配色。
  - 判定：程序测量，边界交 Judge；证据：`computed_color`；来源：`layout_constraints`「体块为高饱和的蓝紫色系，与背景同一色调」。备注：程序采样各面主色并报告 HSL，与 SR-01.C2 的背景色相对比；非典型交 Judge。
- **SR-12.C3** 矮塔的各个面以高饱和的蓝紫色为主，与背景同一色调；灰、黑、白等低饱和色或与背景色相明显不同（如绿、橙、红）的不满足。门洞与光斑的品红灯光不属于体块配色。
  - 判定：程序测量，边界交 Judge；证据：`computed_color`；来源：`layout_constraints`「体块为高饱和的蓝紫色系，与背景同一色调」。备注：程序采样各面主色并报告 HSL，与 SR-01.C2 的背景色相对比；非典型交 Judge。
- **SR-12.C4** 平台的明暗符合光从建筑左前上方照来：顶面和正面（受光面）比右侧面（背光面）更亮、更浅（正面＝与门洞所在面朝向相同的侧面，右侧面＝另一个可见侧面）；三个面亮度相同或亮暗关系相反的不满足。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从左前上方照来，照到的地方颜色变亮、变浅」。备注：左右前后按模型实际呈现的建筑正面换算；朝向错误只由 SR-09.C1 负责。建筑正面朝画面右下方时，光源在画面右上方，画面右侧可见面亮、左侧可见面暗。程序可报告各面平均亮度辅助判断。
- **SR-12.C5** 高塔的明暗符合光从建筑左前上方照来：顶面和正面（受光面）比右侧面（背光面）更亮、更浅（正面＝与门洞所在面朝向相同的侧面，右侧面＝另一个可见侧面）；三个面亮度相同或亮暗关系相反的不满足。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从左前上方照来，照到的地方颜色变亮、变浅」。备注：左右前后按模型实际呈现的建筑正面换算；朝向错误只由 SR-09.C1 负责。建筑正面朝画面右下方时，光源在画面右上方，画面右侧可见面亮、左侧可见面暗。程序可报告各面平均亮度辅助判断。
- **SR-12.C6** 矮塔的明暗符合光从建筑左前上方照来：顶面和正面（受光面）比右侧面（背光面）更亮、更浅（正面＝与门洞所在面朝向相同的侧面，右侧面＝另一个可见侧面）；三个面亮度相同或亮暗关系相反的不满足。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从左前上方照来，照到的地方颜色变亮、变浅」。备注：左右前后按模型实际呈现的建筑正面换算；朝向错误只由 SR-09.C1 负责。建筑正面朝画面右下方时，光源在画面右上方，画面右侧可见面亮、左侧可见面暗。程序可报告各面平均亮度辅助判断。
- **SR-12.C7** 插画整体光影自然：面内明暗过渡平滑，没有与光照无关的突兀黑块、亮斑或杂乱色块，相邻面的明暗交界清楚。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「建筑各处光影自然、有规律」。备注：各体块受光面与背光面的亮暗方向只由 SR-12.C4–C6 负责，本条不因此重复扣分。

### SR-13 署名区内容（element）

- **SR-13.C1** 署名区有一行文字“inspired by”（大小写、空格一致）。
  - 判定：程序；证据：`dom_text`；来源：`functional_requirements`「“inspired by”」。
- **SR-13.C2** 署名区有一个链接，文字为“Walid Beno's Dribbble shot”，href 为 https://dribbble.com/shots/3863328-Daily-challenge-illustration-3-100-isometric-building。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「链接文字“Walid Beno's Dribbble shot”」。备注：文字比较前去除首尾空白；地址按 URL 规范化比较（末尾斜杠差异不计）。
- **SR-13.C3** 署名区有一行文字“check me out. 😎”，含表情 😎。
  - 判定：程序；证据：`dom_text`；来源：`functional_requirements`「“check me out. 😎”」。
- **SR-13.C4** Dribbble 链接行与“check me out. 😎”行之间空出一行：两行之间的竖直间隔约为一行文字高度，明显大于其他相邻行之间的间隔。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`functional_requirements`「空一行后」。备注：程序报告两行间隔与行高（GT 间隔 25px、行高 20px）；边界交 Judge。
- **SR-13.C5** 署名区有一个Twitter 图标链接，href 为 https://twitter.com/xdesro；图标可辨认为 Twitter  的小鸟标志（图片、SVG、图标字体均可），不是文字。
  - 判定：程序测量，边界交 Judge；证据：`dom_url`；来源：`functional_requirements`「Twitter 图标（https://twitter.com/xdesro）」。备注：地址由程序判；图标是否可辨认由 Judge 看截图。
- **SR-13.C6** 署名区有一个GitHub 图标链接，href 为 https://github.com/xdesro；图标可辨认为 GitHub  的猫形标志（图片、SVG、图标字体均可），不是文字。
  - 判定：程序测量，边界交 Judge；证据：`dom_url`；来源：`functional_requirements`「GitHub 图标（https://github.com/xdesro）」。备注：地址由程序判；图标是否可辨认由 Judge 看截图。
- **SR-13.C7** 署名区有一个链接图标链接，href 为 https://henry.codes；图标可辨认为 链接 的链条/链接标志（图片、SVG、图标字体均可），不是文字。
  - 判定：程序测量，边界交 Judge；证据：`dom_url`；来源：`functional_requirements`「链接图标（https://henry.codes）」。备注：地址由程序判；图标是否可辨认由 Judge 看截图。
- **SR-13.C8** 署名区各行从上到下依次为：“inspired by”、Dribbble 链接、（空行）、“check me out. 😎”、图标行；图标行在最下方。
  - 判定：程序；证据：`geometry`；来源：`functional_requirements`「署名区文字从上到下每行依次为」。备注：只判已出现各行的相对顺序；缺行由对应内容条件负责，不在此重复扣。
- **SR-13.C9** 三个图标并排在同一行（顶边或垂直中心大致对齐），从左到右依次为 Twitter、GitHub、链接图标。
  - 判定：程序；证据：`geometry`；来源：`functional_requirements`「最后并排三个图标链接，依次为」。备注：只比较已出现图标的相对位置；缺失图标由 C5–C7 负责。

### SR-14 署名区位置与样式（element）

- **SR-14.C1** 署名区位于页面右下角，其右边缘和下边缘都与视口边缘保持一小段距离；贴边无边距、边距大到离开角落、或不在右下角的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`layout_constraints`「署名区贴在页面右下角并留有少许边距」。备注：程序报告内容右侧、下侧到视口边缘的距离（GT 15、20px）；“少许”不设上限，边界交 Judge。
- **SR-14.C2** 署名区文字实际以 Roboto Mono 细体（Light，字重 300 左右）渲染：计算字体族首选为 Roboto Mono，对应字体文件实际加载，渲染字重为细体。
  - 判定：程序测量，边界交 Judge；证据：`computed_style`；来源：`layout_constraints`「使用 Roboto Mono 细体」。备注：GT 只加载 300 字重、计算字重 400 时浏览器用 300 字面渲染，按实际渲染字面判。字体加载失败若由评测网络导致记 UNRESOLVED。
- **SR-14.C3** 署名区所有文字（含链接文字）为白色；😎 表情保持彩色不计。
  - 判定：程序；证据：`computed_style`；来源：`layout_constraints`「文字和图标（除😎外）均为白色」。
- **SR-14.C4** Twitter 图标为白色。
  - 判定：程序测量，边界交 Judge；证据：`computed_style`；来源：`layout_constraints`「文字和图标（除😎外）均为白色」。备注：程序读 SVG fill / color；位图或字体图标看截图。图标缺失时按 DEC-029 同判 FAIL。
- **SR-14.C5** GitHub 图标为白色。
  - 判定：程序测量，边界交 Judge；证据：`computed_style`；来源：`layout_constraints`「文字和图标（除😎外）均为白色」。备注：程序读 SVG fill / color；位图或字体图标看截图。图标缺失时按 DEC-029 同判 FAIL。
- **SR-14.C6** 链接图标为白色。
  - 判定：程序测量，边界交 Judge；证据：`computed_style`；来源：`layout_constraints`「文字和图标（除😎外）均为白色」。备注：程序读 SVG fill / color；位图或字体图标看截图。图标缺失时按 DEC-029 同判 FAIL。
- **SR-14.C7** Dribbble 链接文字为斜体。
  - 判定：程序；证据：`computed_style`；来源：`layout_constraints`「链接文字为斜体」。
- **SR-14.C8** Dribbble 链接文字没有下划线（text-decoration 无 underline，截图中也看不到下划线）。
  - 判定：程序；证据：`computed_style`；来源：`functional_requirements`「（无下划线）」。
## GT 自查（1280×900，本地 Chromium，0 API）

脚本 [gt_selfcheck.py](gt_selfcheck.py)，只验证程序条件可执行、GT 能通过，不向 input 增加要求。

| 条件 | GT 实测 | 结果 |
|---|---|---|
| SR-01.C1 单屏 | 滚动条差值 0/0；滚轮 + End + PageDown 后 scrollX、scrollY = 0 | 通过 |
| SR-01.C2 背景 | 四角 HSL (255°, 0.76, 0.34) | 蓝紫，通过 |
| SR-01.C3 组成 | 署名区外可见文字 0 个 | 通过 |
| SR-02.C1 偏左上 | 插画中心相对视口中心 dx −24、dy −46 | 通过 |
| SR-02.C2 宽度 | 0.305 | 通过 |
| SR-02.C3 光晕 | 插画中心处背景亮度 0.50，角落 0.34 | 通过 |
| SR-13.C1–C3 文字、链接 | 三行文字、Dribbble 文字与地址一致 | 通过 |
| SR-13.C4 空一行 | 间隔 25px，行高 20px | 通过 |
| SR-13.C5–C7 图标地址 | twitter / github / henry.codes 一致 | 通过 |
| SR-13.C8–C9 顺序 | 行序正确；三图标同一行，从左到右 Twitter、GitHub、链接 | 通过 |
| SR-14.C1 右下角边距 | 右 15px、下 20px | 通过 |
| SR-14.C2 字体 | 计算字体 Roboto Mono，已加载字面 300 | 通过 |
| SR-14.C3–C6 白色 | 文字与三个图标 fill 均为 rgb(255,255,255) | 通过 |
| SR-14.C7–C8 斜体、无下划线 | italic / none | 通过 |

Judge 条件已在 GT 截图上人工核对：斜上方俯视、平行投影；平台、两塔都能看到顶面和两个侧面；平台正面一边（画面右前）较长；矮塔贴在高塔画面左侧面（建筑右侧面）中段，约三分之二高；屋顶槽四周留边、槽内暗并有内阴影；门洞品红发亮，门外平台有由亮到暗的光斑；画面右侧可见面亮、左侧暗，顶面较亮。正式 Judge 未跑。

## 用户确认（2026-11-24）

5 个问题全部按草稿建议处理：

1. “约”的程序直判范围：插画宽度比 0.25–0.42、矮塔高度比 0.55–0.78 内程序判 PASS；范围外交 Judge，程序不直接判 FAIL。
2. 朝向只由 SR-09.C1 扣一次，其余相对关系按模型实际门洞所在面换算。
3. 保留 SR-12.C7，只判“自然”。
4. 保留 SR-01.C3。
5. 门洞保持 4 条。

**条件正文澄清。** Light Judge 只收到条件正文和 input，看不到 frame_policy。因此把 frame_policy 的换算直接写进 SR-04.C3、SR-08.C3、SR-12.C4–C6 的正文，语义不变。改写时没有打开任何模型输出，旧稿哈希记在 `eval_rules.json` 的 `clarifications`。GT 自检时 Judge 仍把“右侧面”换算错，误判 GT 的 SR-08.C3/C4；第二次澄清把右侧面直接写成“高塔没有门洞的那个可见侧面”，同样语义不变、未看模型输出。GT 复测 Judge 仍判错，第三次改成可直接看图的等价判法：矮塔与门洞分处高塔两个不同的可见侧面。
