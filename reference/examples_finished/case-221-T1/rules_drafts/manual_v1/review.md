# case-221 manual_v1 采分点

日期：2026-11-24。起草：Claude。状态：**用户 2026-11-24 确认并冻结**（rule_status=USER_CONFIRMED_FROZEN；冻结只改状态字段，条件文字与草稿 a801501e… 相同）。

| 文件 | 内容 |
|---|---|
| [eval_rules.json](eval_rules.json) | 规则，结构同 case-213 `manual_v3`（`semantic-eval-rules/3.0`） |
| [build_rules.py](build_rules.py) | 由一张表生成 eval_rules.json 和本文件下半部分清单；改规则请改这里后重跑 `python build_rules.py cases/case-221-T1` |
| 本文件 | 起草说明 + 全部采分点清单 |

## 概况

- 依据：当前 [input.json](../../input.json)（sha256 记录在规则里）加一条 DEC-037 常识条件。GT 只用来核对每条都能被满足（数据见 [review_20261121](../../review_20261121/review.md)），不从 GT 反推要求。
- 起草时**没有读取任何模型输出**，包括案例目录里的 `case-221-duet.html`。
- **12 条 Requirement，95 条 mandatory Evidence**：宽窄屏要求相同、合并计分 47 条，只看宽屏 39 条，只看窄屏 9 条。只有 D1 静态维度，没有 D2。
- 采证视口：宽 1440×900、窄 375×812，都取整页截图。700–1023px 的中间宽度不计分（你已确认）。
- 门禁 G1–G5 与 case-213 相同（契约 v2）；`forbidden` 为空，不另设禁令。

## 拆分原则

1. **六张卡片分别计分**的有：剧名、统计文字、底色与字色、宽屏正方形。这些属性逐卡写在 input 里，某一张错了不该连累其他卡片。
2. **六张卡片合成一条**的有：剧名在上统计在下、剧名全大写粗体、剧名明显大于统计文字、文字靠底、宽屏投影、手机单列/满宽/顺序/高度/间距。input 对这些是一句话统一要求，拆成六条等于把一句话扣六次，违反“不为增加扣分而拆细”。
3. 一句话里有几个独立事实就拆开，比如“主标题全大写、粗体、深青绿色，字号很大”拆成 4 条；同一事实不重复扣。共用一句原文的几处，在 `attribution_policy.shared_quotes` 写明各自的分工：
   - 卡片投影（SR-07.C17）与剧照投影（SR-08.C7）分开判。
   - 图例色块（SR-05.C7–C9）只判“和卡片同色”，卡片底色本身由 C1–C6 判，不重复扣。
   - 宽屏正方形（SR-07.C7–C12）与窄屏高度随内容（SR-11.C4）是两个视口的两个要求。
   - 常识可读性（SR-12）只判文字是否被盖到不可读；压叠位置错了归 SR-07/SR-08，SR-12 不再扣。
4. **只在一个视口出现的要求只在那个视口采证**：竖排标题、副标题、拼贴、剧照只看宽屏；横排居中、不显示副标题、单列等只看窄屏。
5. **定性词不加数值**：颜色只判色系（柠檬黄判色相为黄，不按饱和度扣分；钢蓝判蓝色系且明显深于天蓝卡片和页面底色）；“很大”“小得多”“略小”“较高”“偏右”“柔和”看截图中能否清楚看出。只有“正方形”“一样大”写成“只允许取整造成的微小差异”。
6. **模型依赖**：按 DEC-029，从每条 Evidence 的 `required_objects` 自动列出 28 组前置关系。例如 Crash Landing on You 卡片被确认缺失时，压叠、排序等下游条件也判 FAIL，但只限对象本体缺失；文字或颜色错不阻断几何条件。采证失败一律 UNRESOLVED。

## GT 核对

逐条对照 `review_20261121/gt_facts.json` 和截图：GT 在 1440 / 375 下满足全部 95 条。几条容易有疑问的：

| 条件 | GT 实测 |
|---|---|
| SR-02.C9 TOP STATS 下端较高 | 下端 481 对 705，相差约 224px |
| SR-03.C7 副标题在 TOP STATS 右侧且在卡片左侧 | 副标题 x 331–391，卡片最左 462 |
| SR-07.C4 上下两排 | 上排中心 y 最大 311，下排中心 y 最小 487 |
| SR-07.C7–C12 正方形 | 只有 Kakegurui 是 197×198，属取整差异 |
| SR-08.C3 剧照向右上错开 | 剧照上缘 64 高于卡片 167，右缘 826 超出卡片 749；被卡片遮住 37%（2026-11-24 用户修订条文后补核） |
| SR-11.C2 满宽 | 卡片与图例都是 x 16–359 |
| SR-12 文字可读 | 1440 / 1280 下 6 张卡片文字采样点全部命中卡片本身；375 下单列，不重叠 |

后续进入评测轮次时，还要用流水线做完整 GT 自测，以自测结果为准。

## 请你重点看

1. **合并与拆分的粒度**，见“拆分原则”第 1、2 条。
2. **SR-07.C13**：“大小略有差别，Crash Landing on You 最大”合成一条，判 Crash 严格最大，且六张属同一量级。input 里的“略有差别”单独成条意义不大，因为 Crash 最大已经说明尺寸不全相同。
3. **SR-08.C2**：剧照“比卡片略小”，我写成“宽高都小于卡片，但不是缩略图那样的小图”，判定交给 Judge 看截图。
4. **SR-12** 常识条件的写法，按你 11-23 的确认放了进来。

确认后即可进入完整的自动化评分流程（建轮次、编译采证计划、GT 自测、生成、评分）。

## 全部采分点

<!-- 以下由 build_rules.py 生成，勿手改 -->

### SR-01 页面底色与通用字体（3 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 页面底色为浅灰蓝色 | 页面主背景（内容区周围与卡片之间露出的底色）呈浅灰蓝色：浅、偏灰、带蓝的冷色；不指定色号。 | screenshot_visual |
| C2 | 宽+窄 | 文字使用 Montserrat 字体 | 主标题、副标题（Dancing Script 那句除外）、剧名、统计文字、图例和说明栏文字实际渲染为 Montserrat（字体加载完成后以渲染字形判断，声明了但回退成其他字体算未使用；字体服务加载失败为 UNRESOLVED）。 | font_rendering |
| C3 | 宽+窄 | 正文为细体 | 统计文字、图例文字和说明栏文字为细字重，明显细于常规字重；不指定字重数值。 | font_rendering |

### SR-02 主标题（10 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 页面主标题为 Netflix Binge: Top Stats | 主标题文字为 Netflix Binge: Top Stats（字母大小写可由样式变换，换行与多余空白不计；不能缺词、错词或多出其他文字）。 | dom_text |
| C2 | 宽+窄 | 主标题全大写 | 主标题在页面上显示为全大写字母。 | screenshot_visual |
| C3 | 宽+窄 | 粗体 | 主标题为粗体，明显粗于正文。 | font_rendering |
| C4 | 宽+窄 | 深青绿色 | 主标题文字为深青绿色（深色、蓝绿之间）；不指定色号。 | screenshot_visual |
| C5 | 宽+窄 | 字号很大 | 主标题是页面上字号最大的文字，明显大于卡片剧名。 | geometry |
| C6 | 宽 | 宽屏下主标题竖排在内容区最左侧，文字自下而上阅读 | 主标题为竖排：字母沿竖直方向排列，整体旋转后需从下往上读（字母顶部朝左）；不是逐字竖向堆叠的横排字母，也不是从上往下读。 | screenshot_visual |
| C7 | 宽 | 宽屏下主标题竖排在内容区最左侧 | 主标题位于页面主体内容（卡片、图例、副标题）的最左侧，所有卡片和图例都在它的右边；说明栏除外。 | geometry |
| C8 | 宽 | 分成 NETFLIX BINGE: 和 TOP STATS 两列，TOP STATS 在右 | 竖排主标题分成两列：一列为 NETFLIX BINGE:，另一列为 TOP STATS，TOP STATS 一列在右。 | geometry_and_visual |
| C9 | 宽 | 且它的下端较高 | TOP STATS 一列的下端高于 NETFLIX BINGE: 一列的下端，两列下端在截图中清楚可见地错开，不是几像素的对齐误差。 | geometry |
| C10 | 窄 | 手机窄屏下主标题横排并居中 | 主标题为正常横排文字，在可用宽度内水平居中（多行时各行居中）。 | geometry_and_visual |

### SR-03 副标题（8 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽 | 副标题为 When your friend recommended you that series, you should've said no. | 副标题文字为 When your friend recommended you that series, you should've said no.（撇号用直撇号或弯撇号均可，换行与多余空白不计）。宽屏下必须可见。 | dom_text |
| C2 | 宽 | 副标题字号小得多 | 副标题字号明显小于主标题（一眼可见的数量级差别）。 | geometry |
| C3 | 宽 | 细体 | 副标题中除 should've said no. 外的部分为细字重。 | font_rendering |
| C4 | 宽 | 其中 should've said no. 一句改用 Dancing Script 手写体 | should've said no. 这一句实际渲染为 Dancing Script 手写体，副标题其余部分不是手写体（字体服务加载失败为 UNRESOLVED）。 | font_rendering |
| C5 | 宽 | 并略微放大 | should've said no. 一句的字号大于副标题其余部分，且仍明显小于主标题。 | geometry |
| C6 | 宽 | 副标题同样自下而上竖排 | 副标题为竖排，需从下往上读，方向与主标题一致。 | screenshot_visual |
| C7 | 宽 | 在TOP STATS右侧 | 副标题整体位于 TOP STATS 一列的右侧，且在所有卡片左侧（不压在卡片上）。 | geometry |
| C8 | 窄 | 手机窄屏下主标题横排并居中，不显示副标题 | 页面上看不到副标题文字（不可见即可，DOM 中是否保留不计）。 | screenshot_visual |

### SR-04 图例（4 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 页面上有一组图例，三个色块依次对应 Korean Drama、Anime、Western Series | 图例共三项，每项由一个色块和一段文字组成，文字依次为 Korean Drama、Anime、Western Series（按阅读顺序：从左到右，换行时先上后下）。 | dom_text |
| C2 | 宽 | 图例排成一行 | 三项图例在同一行内横向排列。 | geometry |
| C3 | 宽 | 位于下排卡片下方偏右 | 图例整体位于下排三张卡片（Food Wars、Kakegurui、Inheritors）的下方，水平方向偏向页面主体的右侧（图例中心在主体内容水平中线右边）。 | geometry |
| C4 | 窄 | 图例紧接在标题下方 | 图例在主标题下方、第一张卡片上方，两者之间没有其他内容。 | geometry |

### SR-05 按剧集类型着色（卡片与图例色块）（10 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | Korean Drama 为柠檬黄色底、深青绿色字 | Crash Landing on You 卡片（Korean Drama）：底色为柠檬黄色系（色相为黄，浅或中等明度；不按饱和度深浅扣分），卡片内文字（剧名与统计文字）为深青绿色。 | screenshot_visual |
| C2 | 宽+窄 | Korean Drama 为柠檬黄色底、深青绿色字 | Inheritors 卡片（Korean Drama）：底色为柠檬黄色系（色相为黄，浅或中等明度；不按饱和度深浅扣分），卡片内文字（剧名与统计文字）为深青绿色。 | screenshot_visual |
| C3 | 宽+窄 | Anime 为亮青绿色底、近白色字 | Food Wars 卡片（Anime）：底色为明亮的青绿色系（介于绿与青之间、明度高），卡片内文字为白色或近白色。 | screenshot_visual |
| C4 | 宽+窄 | Korean Drama 为柠檬黄色底、深青绿色字 | The King 卡片（Korean Drama）：底色为柠檬黄色系（色相为黄，浅或中等明度；不按饱和度深浅扣分），卡片内文字（剧名与统计文字）为深青绿色。 | screenshot_visual |
| C5 | 宽+窄 | Western Series 为天蓝色底、近白色字 | Mindhunter 卡片（Western Series）：底色为天蓝色系（明亮的蓝，偏青），卡片内文字为白色或近白色。 | screenshot_visual |
| C6 | 宽+窄 | Anime 为亮青绿色底、近白色字 | Kakegurui 卡片（Anime）：底色为明亮的青绿色系（介于绿与青之间、明度高），卡片内文字为白色或近白色。 | screenshot_visual |
| C7 | 宽+窄 | 卡片色底按图例色块着色 | 图例中 Korean Drama 的色块为柠檬黄色，与 Korean Drama 卡片的底色相同（目视为同一颜色）。 | screenshot_visual |
| C8 | 宽+窄 | 卡片色底按图例色块着色 | 图例中 Anime 的色块为亮青绿色，与 Anime 卡片的底色相同（目视为同一颜色）。 | screenshot_visual |
| C9 | 宽+窄 | 卡片色底按图例色块着色 | 图例中 Western Series 的色块为天蓝色，与 Western Series 卡片的底色相同（目视为同一颜色）。 | screenshot_visual |
| C10 | 宽+窄 | 卡片色底按图例色块着色 | 三种类型的卡片底色彼此可明显区分，尤其 Anime 的亮青绿与 Western Series 的天蓝不能混成同一颜色。 | screenshot_visual |

### SR-06 卡片内容与文字样式（15 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | Crash Landing on You（ | 存在一张剧名为 Crash Landing on You 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C2 | 宽+窄 | Inheritors（ | 存在一张剧名为 Inheritors 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C3 | 宽+窄 | Food Wars（ | 存在一张剧名为 Food Wars 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C4 | 宽+窄 | The King（ | 存在一张剧名为 The King 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C5 | 宽+窄 | Mindhunter（ | 存在一张剧名为 Mindhunter 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C6 | 宽+窄 | Kakegurui（ | 存在一张剧名为 Kakegurui 的卡片（不区分大小写；剧名在单词中间断行可接受，字母必须齐全且顺序正确）。 | dom_text |
| C7 | 宽+窄 | 16 episodes // 960 minutes in 1 day. One sitting. | Crash Landing on You 卡片的统计文字为 16 episodes // 960 minutes in 1 day. One sitting.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C8 | 宽+窄 | 16 episodes // 960 minutes in 1 day. One sitting. | Inheritors 卡片的统计文字为 16 episodes // 960 minutes in 1 day. One sitting.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C9 | 宽+窄 | 85 episodes // 1700 minutes in 3 days. | Food Wars 卡片的统计文字为 85 episodes // 1700 minutes in 3 days.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C10 | 宽+窄 | 16 episodes // 960 minutes in 2 days. | The King 卡片的统计文字为 16 episodes // 960 minutes in 2 days.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C11 | 宽+窄 | 19 episodes // 942 minutes in 3 days. | Mindhunter 卡片的统计文字为 19 episodes // 942 minutes in 3 days.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C12 | 宽+窄 | 24 episodes // 480 minutes in 2 days. | Kakegurui 卡片的统计文字为 24 episodes // 480 minutes in 2 days.（换行与多余空白不计，标点和数字须一致）。 | dom_text |
| C13 | 宽+窄 | 卡片内剧名在上、统计文字在下 | 六张卡片中，剧名都在统计文字上方。 | geometry |
| C14 | 宽+窄 | 剧名全大写、粗体 | 六张卡片的剧名都显示为全大写且为粗体。 | font_rendering |
| C15 | 宽+窄 | 明显大于统计文字 | 六张卡片的剧名字号都明显大于同卡统计文字。 | geometry |

### SR-07 宽屏卡片拼贴（17 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽 | 六张卡片在标题右侧错落拼贴 | 六张卡片都位于竖排主标题右侧，不与主标题重叠。 | geometry |
| C2 | 宽 | 上排从左到右为 Crash Landing on You、The King、Mindhunter | 上排三张卡片从左到右依次为 Crash Landing on You、The King、Mindhunter（按卡片左边缘或中心的水平顺序）。 | geometry |
| C3 | 宽 | 下排从左到右为 Food Wars、Kakegurui、Inheritors | 下排三张卡片从左到右依次为 Food Wars、Kakegurui、Inheritors。 | geometry |
| C4 | 宽 | 大致分上下两排 | 上排三张卡片的中心都高于下排三张卡片的中心，形成上下两排；同排卡片高低可以错落，不要求对齐。 | geometry |
| C5 | 宽 | 其中 The King 最靠上 | The King 的上边缘高于 Crash Landing on You 和 Mindhunter 的上边缘，差距清楚可见。 | geometry |
| C6 | 宽 | 其中 Kakegurui 位置偏高 | Kakegurui 的上边缘高于 Food Wars 和 Inheritors 的上边缘，差距清楚可见。 | geometry |
| C7 | 宽 | 每张卡片都是正方形 | Crash Landing on You 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C8 | 宽 | 每张卡片都是正方形 | Inheritors 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C9 | 宽 | 每张卡片都是正方形 | Food Wars 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C10 | 宽 | 每张卡片都是正方形 | The King 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C11 | 宽 | 每张卡片都是正方形 | Mindhunter 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C12 | 宽 | 每张卡片都是正方形 | Kakegurui 卡片的宽和高相等（只允许取整造成的微小差异）。 | geometry |
| C13 | 宽 | 大小略有差别，Crash Landing on You 最大 | Crash Landing on You 卡片边长严格大于其他五张；六张卡片尺寸属同一量级，没有某张远大于或远小于其余卡片。 | geometry |
| C14 | 宽 | 卡片文字靠卡片底部排列 | 六张卡片的文字（剧名和统计文字）都贴近卡片底部，空白集中在文字上方。 | geometry |
| C15 | 宽 | Kakegurui 盖住 Crash Landing on You 的右下角 | Kakegurui 与 Crash Landing on You 卡片的右下角区域重叠，重叠处 Kakegurui 在上；只压住角部，不覆盖 Crash Landing on You 的大部分。 | geometry_and_visual |
| C16 | 宽 | Mindhunter 盖住 The King 的右下角 | Mindhunter 与 The King 卡片的右下角区域重叠，重叠处 Mindhunter 在上；只压住角部，不覆盖 The King 的大部分。 | geometry_and_visual |
| C17 | 宽 | 卡片和 Mindhunter 的剧照都带柔和的投影 | 六张卡片都带柔和的投影（边缘虚化、颜色浅，不是实线描边或生硬的深色阴影）。 | screenshot_visual |

### SR-08 剧照（8 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽 | Crash Landing on You 用 https://assets.codepen.io/567707/show-cloy.jpg | Crash Landing on You 的剧照使用 https://assets.codepen.io/567707/show-cloy.jpg 并实际显示出来（图片请求失败而地址正确时为 UNRESOLVED）。 | dom_url |
| C2 | 宽 | Crash Landing on You 的剧照比卡片略小 | 该剧照的宽和高都小于 Crash Landing on You 卡片，但只是略小，不是缩略图那样的小图。 | geometry |
| C3 | 宽 | 垫在卡片后面并向右上方错开，左下部分被卡片挡住 | 该剧照在 Crash Landing on You 卡片下层，相对卡片向右上方错开：剧照上边缘高于卡片上边缘、右边缘超出卡片右边缘；卡片只遮住剧照的左下一部分，剧照露出的面积不少于一半，剧照主体（人物）可见。 | geometry_and_visual |
| C4 | 宽 | Mindhunter 用 https://assets.codepen.io/567707/show-mindhunter.png | Mindhunter 的剧照使用 https://assets.codepen.io/567707/show-mindhunter.png 并实际显示出来（图片请求失败而地址正确时为 UNRESOLVED）。 | dom_url |
| C5 | 宽 | Mindhunter 的剧照与卡片一样大 | 该剧照与 Mindhunter 卡片宽高相同（只允许取整造成的微小差异）。 | geometry |
| C6 | 宽 | 并排紧贴在卡片右侧 | 该剧照位于 Mindhunter 卡片右侧，左边缘与卡片右边缘相接（无明显缝隙、不重叠），上下边缘与卡片对齐。 | geometry |
| C7 | 宽 | 卡片和 Mindhunter 的剧照都带柔和的投影 | Mindhunter 剧照带柔和的投影。 | screenshot_visual |
| C8 | 窄 | 不显示剧照 | 手机窄屏下两张剧照都不可见。 | screenshot_visual |

### SR-09 爆米花装饰背景（3 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 页面内容区的左下角用爆米花图片 https://assets.codepen.io/567707/bg-popcorn.png 作装饰背景 | 页面使用 https://assets.codepen.io/567707/bg-popcorn.png 并实际显示，位置在页面主体内容区的左下角（说明栏之上）（图片请求失败而地址正确时为 UNRESOLVED）。 | dom_url |
| C2 | 宽 | 爆米花图在卡片下层，Food Wars | Food Wars 卡片与爆米花图局部重叠，重叠处卡片在上；其他卡片若与爆米花图重叠，也都在其上层。 | geometry_and_visual |
| C3 | 宽 | 和主标题局部压在它上面 | 主标题与爆米花图局部重叠，重叠处主标题文字在上、可见。 | geometry_and_visual |

### SR-10 底部说明栏（11 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 页面最底部是一条说明栏 | 说明栏是页面最底部的内容，位于卡片、图例和爆米花图之下，下方没有其他内容。 | geometry |
| C2 | 宽+窄 | 左边是图片 https://assets.codepen.io/567707/palette-ts.png | 说明栏中有图片 https://assets.codepen.io/567707/palette-ts.png 并实际显示，位于说明文字左边（图片请求失败而地址正确时为 UNRESOLVED）。 | dom_url |
| C3 | 宽+窄 | 右边文字为 Part of the UI Designs inspired by Taylor Swift Album Covers collection. This is Taylor Swift (2006). | 说明栏文字为 Part of the UI Designs inspired by Taylor Swift Album Covers collection. This is Taylor Swift (2006).（换行与多余空白不计）。 | dom_text |
| C4 | 宽+窄 | 其中 UI Designs inspired by Taylor Swift Album Covers 是指向 https://codepen.io/collection/XPxJmz 的链接 | 只有 UI Designs inspired by Taylor Swift Album Covers 这一段是链接，链接地址为 https://codepen.io/collection/XPxJmz。 | dom_url |
| C5 | 宽+窄 | 底部说明栏为钢蓝色 | 说明栏底色为钢蓝色：蓝色系、略偏灰，明显深于页面底色和 Mindhunter 卡片的天蓝色；不指定色号。 | screenshot_visual |
| C6 | 宽+窄 | 横跨整个视口宽度 | 说明栏左右两端分别贴住视口左右边缘。 | geometry |
| C7 | 宽+窄 | 左侧图片只占一小部分宽度 | 说明栏图片宽度明显小于说明栏宽度的一半。 | geometry |
| C8 | 宽+窄 | 右侧文字为浅黄色 | 说明栏文字（含链接文字）为浅黄色（很浅、略带黄）；不指定色号。 | screenshot_visual |
| C9 | 宽+窄 | 与图片垂直居中 | 说明文字的垂直中心与图片的垂直中心基本对齐。 | geometry |
| C10 | 宽+窄 | 链接带下划线 | 链接文字带下划线。 | computed_style |
| C11 | 宽+窄 | Taylor Swift (2006) 为斜体 | Taylor Swift (2006) 显示为斜体，说明栏其余文字不是斜体。 | font_rendering |

### SR-11 手机窄屏卡片排列（5 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 窄 | 卡片单列排列 | 六张卡片上下排成一列，每行只有一张卡片。 | geometry |
| C2 | 窄 | 铺满可用宽度 | 每张卡片宽度占满页面主体内容的可用宽度（与图例、标题所在内容区同宽，左右只留页面留白），不超出视口。 | geometry |
| C3 | 窄 | 从上到下的顺序与上面所列相同 | 卡片从上到下依次为 Crash Landing on You、Inheritors、Food Wars、The King、Mindhunter、Kakegurui。 | geometry |
| C4 | 窄 | 卡片高度随内容而定 | 卡片高度由文字内容决定（文字加内边距），不是宽屏那样的正方形，也没有大片空白。 | geometry |
| C5 | 窄 | 彼此留有间距 | 相邻卡片之间留有可见间距，不相接、不重叠。 | geometry |

### SR-12 卡片文字可读（常识）（1 条）

| ID | 视口 | 来源原文 | 判定 | 方式 |
|---|---|---|---|---|
| C1 | 宽+窄 | 常识 | 六张卡片的剧名和统计文字完整可见、可读，不被其他卡片、剧照或页面边缘遮挡或裁掉（剧名在单词中间断行但字母齐全可接受）。 | screenshot_visual |
