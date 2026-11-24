# case-227 v1 采分点审核稿

2026-11-17，Claude 起草；用户同日回复“按建议处理”，4 个问题全部按建议确认。未冻结、未采证、未调用 API、未评分。

**7 条 Requirement / 72 条 mandatory Evidence，全部来自 input，只计 D1。** 只在一个桌面视口（1280×900）采证。

规则：[eval_rules.json](eval_rules.json)。input：[input.json](../../input.json)。GT：[ground_truth.html](../../ground_truth.html)。

## 拆分原则

- **并列成员逐个成条。** 两组各四张海报的每项属性、斜靠组三对相邻关系，都单独计分。
- **整组性质只写一条。** 包括数量、整组居中、同宽、等距、两组大小比较、两组之间的空白。
- **同一事实只放一条。** 顺序错误只由“第 N 张是哪张图”负责；替代文字按图片身份核对，不因顺序错再扣一次。“正面展示”和“不倾斜”合为一条。
- **计分时合并。** 沿用 R02 case-213 的并列失败合并裁定：同一检查模板、同一处实现造成的并列失败合为一组，只判一档。该规则还没写入项目决策，用户已确认 227 沿用。
- **不加常识条件。** 用户已删去“图片内容清晰可辨”“页面无文字”，规则不补回。

## Requirement 结构

| Requirement | 范围 | Evidence 数 |
|---|---|---:|
| SR-01 | 墙角场景 | 4 |
| SR-02 | 悬浮组的图片身份、顺序与替代文字 | 9 |
| SR-03 | 斜靠组的图片身份、顺序与替代文字 | 9 |
| SR-04 | 悬浮组的位置与排布 | 17 |
| SR-05 | 斜靠组的摆放 | 15 |
| SR-06 | 斜靠组的透视纵深与卡片厚度 | 10 |
| SR-07 | 斜靠组的光影 | 8 |

## 完整采分点

### SR-01 墙角场景

- **SR-01.C1** 画面中能分辨出墙面和地面两个区域，二者相交处有可辨认的墙角线（明暗或颜色分界）；只有一块均匀背景、看不出墙和地面的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「画面中有一面墙和一块地面」。
- **SR-01.C2** 墙角线呈现墙面向右后方延伸的透视：从左向右逐渐升高（向右上方倾斜）；水平的或向右下降的墙角线不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「墙面相对观察者向右后方延伸」。备注：墙角线多由背景渐变绘制，DOM 读不到，交 Judge；程序可报告墙角线两端高度作辅助。
- **SR-01.C3** 在桌面宽屏评测视口下，墙面和地面横向延伸到页面左右两侧边缘，不是页面中间的一块有限区域。
  - 判定：Judge；证据：`screenshot_visual`；来源：`functional_requirements`「画面中有一面墙和一块地面」。备注：input 未直接写“横贯全宽”；依据是“画面中有一面墙和一块地面”作为画面背景的语义，与 GT 一致。若认为依据不足可删除。
- **SR-01.C4** 墙角场景位于悬浮组下方、页面下部；斜靠组位于墙角场景中。
  - 判定：Judge；证据：`geometry_visual`；来源：`functional_requirements`「一组悬浮展示在画面中上部，一组斜靠在墙角」。

### SR-02 悬浮组的图片身份、顺序与替代文字

- **SR-02.C1** 悬浮组恰好由四张海报图片组成（img 或 CSS 背景图均可，按可见图片计数）。
  - 判定：程序；证据：`dom_structure`；来源：`functional_requirements`「每组都是同样的四张」。
- **SR-02.C2** 悬浮组按可见位置从左到右第1张显示 https://assets.codepen.io/1025350/tahani.jpg（Tahani）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-02.C3** 悬浮组按可见位置从左到右第2张显示 https://assets.codepen.io/1025350/jason.jpg（Jason）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-02.C4** 悬浮组按可见位置从左到右第3张显示 https://assets.codepen.io/1025350/chidi.jpg（Chidi）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-02.C5** 悬浮组按可见位置从左到右第4张显示 https://assets.codepen.io/1025350/eleanor.jpg（Eleanor）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-02.C6** 悬浮组中使用 tahani.jpg 的那张海报，替代文字为 Tahani from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-02.C7** 悬浮组中使用 jason.jpg 的那张海报，替代文字为 Jason from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-02.C8** 悬浮组中使用 chidi.jpg 的那张海报，替代文字为 Chidi from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-02.C9** 悬浮组中使用 eleanor.jpg 的那张海报，替代文字为 Eleanor from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。

### SR-03 斜靠组的图片身份、顺序与替代文字

- **SR-03.C1** 斜靠组恰好由四张海报图片组成（img 或 CSS 背景图均可，按可见图片计数）。
  - 判定：程序；证据：`dom_structure`；来源：`functional_requirements`「每组都是同样的四张」。
- **SR-03.C2** 斜靠组按可见位置从左到右第1张显示 https://assets.codepen.io/1025350/tahani.jpg（Tahani）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-03.C3** 斜靠组按可见位置从左到右第2张显示 https://assets.codepen.io/1025350/jason.jpg（Jason）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-03.C4** 斜靠组按可见位置从左到右第3张显示 https://assets.codepen.io/1025350/chidi.jpg（Chidi）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-03.C5** 斜靠组按可见位置从左到右第4张显示 https://assets.codepen.io/1025350/eleanor.jpg（Eleanor）；地址完全一致，且图片实际加载成功。评测网络导致加载失败记 UNRESOLVED。
  - 判定：程序；证据：`dom_url`；来源：`functional_requirements`「两组从左到右的顺序都是 Tahani、Jason、Chidi、Eleanor」。
- **SR-03.C6** 斜靠组中使用 tahani.jpg 的那张海报，替代文字为 Tahani from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-03.C7** 斜靠组中使用 jason.jpg 的那张海报，替代文字为 Jason from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-03.C8** 斜靠组中使用 chidi.jpg 的那张海报，替代文字为 Chidi from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。
- **SR-03.C9** 斜靠组中使用 eleanor.jpg 的那张海报，替代文字为 Eleanor from The Good Place（img 的 alt，或等效的 aria-label + role="img" 无障碍名称）；按图片身份核对，不因位置顺序错误重复扣分。
  - 判定：程序；证据：`dom_accessibility`；来源：`functional_requirements`「替代文字依次为」。

### SR-04 悬浮组的位置与排布

- **SR-04.C1** 悬浮组位于页面中上部、墙角场景上方，与墙面和地面没有摆放关系：不立在地面、不靠墙、不与墙角线重叠。
  - 判定：Judge；证据：`geometry_visual`；来源：`layout_constraints`「与墙体和地面没有空间关联」。
- **SR-04.C2** 悬浮组整体在页面宽度内水平居中（整组左右边界到页面两侧距离相等，容差为舍入误差）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「水平居中」。
- **SR-04.C3** 四张悬浮海报排成一行：顶边或垂直中心在同一水平线上。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「等间距排成一行」。
- **SR-04.C4** 四张悬浮海报渲染宽度相同（容差为舍入误差）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「四张同样宽度」。
- **SR-04.C5** 相邻悬浮海报之间的三个水平间距相等（容差为舍入误差）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「等间距排成一行」。备注：等距是三个间距放在一起比较才有的整组性质，按一条计。
- **SR-04.C6** 悬浮组第1张（Tahani）渲染宽高比与原图一致，不拉伸、不裁切。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「保持原图比例」。
- **SR-04.C7** 悬浮组第2张（Jason）渲染宽高比与原图一致，不拉伸、不裁切。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「保持原图比例」。
- **SR-04.C8** 悬浮组第3张（Chidi）渲染宽高比与原图一致，不拉伸、不裁切。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「保持原图比例」。
- **SR-04.C9** 悬浮组第4张（Eleanor）渲染宽高比与原图一致，不拉伸、不裁切。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「保持原图比例」。
- **SR-04.C10** 悬浮组第1张（Tahani）正面展示，不旋转、不斜切、无透视变形。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「正面展示」。备注：input“正面展示”与“不倾斜”是同一事实，合为一条。
- **SR-04.C11** 悬浮组第2张（Jason）正面展示，不旋转、不斜切、无透视变形。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「正面展示」。备注：input“正面展示”与“不倾斜”是同一事实，合为一条。
- **SR-04.C12** 悬浮组第3张（Chidi）正面展示，不旋转、不斜切、无透视变形。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「正面展示」。备注：input“正面展示”与“不倾斜”是同一事实，合为一条。
- **SR-04.C13** 悬浮组第4张（Eleanor）正面展示，不旋转、不斜切、无透视变形。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「正面展示」。备注：input“正面展示”与“不倾斜”是同一事实，合为一条。
- **SR-04.C14** 悬浮组第1张（Tahani）周围没有可见投影。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「无投影」。备注：程序先查 box-shadow / drop-shadow；没查到也要看截图，因为影子可能由伪元素或背景画出。
- **SR-04.C15** 悬浮组第2张（Jason）周围没有可见投影。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「无投影」。备注：程序先查 box-shadow / drop-shadow；没查到也要看截图，因为影子可能由伪元素或背景画出。
- **SR-04.C16** 悬浮组第3张（Chidi）周围没有可见投影。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「无投影」。备注：程序先查 box-shadow / drop-shadow；没查到也要看截图，因为影子可能由伪元素或背景画出。
- **SR-04.C17** 悬浮组第4张（Eleanor）周围没有可见投影。
  - 判定：程序测量，边界交 Judge；证据：`screenshot_visual`；来源：`layout_constraints`「无投影」。备注：程序先查 box-shadow / drop-shadow；没查到也要看截图，因为影子可能由伪元素或背景画出。

### SR-05 斜靠组的摆放

- **SR-05.C1** 四张斜靠海报从左到右排成一排，没有上下分行或堆叠。
  - 判定：程序测量，边界交 Judge；证据：`geometry_visual`；来源：`layout_constraints`「四张排成一排」。
- **SR-05.C2** 斜靠组整体在页面宽度内大致水平居中；明显偏向一侧的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`layout_constraints`「整组大致居中」。备注：程序报告整组中心与页面中线的偏移；“大致”不预设数值，偏移明显时交 Judge。
- **SR-05.C3** 斜靠组第1张（Tahani）与第2张（Jason）之间互不重叠，并留有可见的窄缝；紧贴无缝、重叠，或间距大到不像同一排的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry_visual`；来源：`layout_constraints`「相邻海报之间留有窄缝、互不重叠」。
- **SR-05.C4** 斜靠组第2张（Jason）与第3张（Chidi）之间互不重叠，并留有可见的窄缝；紧贴无缝、重叠，或间距大到不像同一排的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry_visual`；来源：`layout_constraints`「相邻海报之间留有窄缝、互不重叠」。
- **SR-05.C5** 斜靠组第3张（Chidi）与第4张（Eleanor）之间互不重叠，并留有可见的窄缝；紧贴无缝、重叠，或间距大到不像同一排的不满足。
  - 判定：程序测量，边界交 Judge；证据：`geometry_visual`；来源：`layout_constraints`「相邻海报之间留有窄缝、互不重叠」。
- **SR-05.C6** 斜靠组第1张（Tahani）底边落在墙角线下方的地面区域。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「斜靠的一组底边立在地面上」。
- **SR-05.C7** 斜靠组第2张（Jason）底边落在墙角线下方的地面区域。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「斜靠的一组底边立在地面上」。
- **SR-05.C8** 斜靠组第3张（Chidi）底边落在墙角线下方的地面区域。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「斜靠的一组底边立在地面上」。
- **SR-05.C9** 斜靠组第4张（Eleanor）底边落在墙角线下方的地面区域。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「斜靠的一组底边立在地面上」。
- **SR-05.C10** 斜靠组第1张（Tahani）上端位于墙角线上方的墙面区域，整张呈倾斜靠墙的姿态；正立平贴或完全平放的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「上端靠着墙面」。
- **SR-05.C11** 斜靠组第2张（Jason）上端位于墙角线上方的墙面区域，整张呈倾斜靠墙的姿态；正立平贴或完全平放的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「上端靠着墙面」。
- **SR-05.C12** 斜靠组第3张（Chidi）上端位于墙角线上方的墙面区域，整张呈倾斜靠墙的姿态；正立平贴或完全平放的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「上端靠着墙面」。
- **SR-05.C13** 斜靠组第4张（Eleanor）上端位于墙角线上方的墙面区域，整张呈倾斜靠墙的姿态；正立平贴或完全平放的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「上端靠着墙面」。
- **SR-05.C14** 斜靠组海报整体尺寸比悬浮组略大：平均渲染宽度和高度都大于悬浮组，但不是成倍放大。
  - 判定：程序测量，边界交 Judge；证据：`geometry`；来源：`layout_constraints`「整体比悬浮的一组略大」。备注：程序比较平均宽高；“略”的上限不预设数值，接近成倍时交 Judge。
- **SR-05.C15** 悬浮组下边缘与斜靠组最高点之间有明显的竖直空白，两组不相接、不重叠。
  - 判定：程序测量，边界交 Judge；证据：`geometry_visual`；来源：`layout_constraints`「两组之间留有明显空白」。

### SR-06 斜靠组的透视纵深与卡片厚度

- **SR-06.C1** 斜靠组第2张（Jason）在地面上的位置比第1张（Tahani）更高，体现沿墙向右后方延伸。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较两张海报可见下边缘的最低点。
- **SR-06.C2** 斜靠组第3张（Chidi）在地面上的位置比第2张（Jason）更高，体现沿墙向右后方延伸。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较两张海报可见下边缘的最低点。
- **SR-06.C3** 斜靠组第4张（Eleanor）在地面上的位置比第3张（Chidi）更高，体现沿墙向右后方延伸。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较两张海报可见下边缘的最低点。
- **SR-06.C4** 斜靠组第2张（Jason）渲染尺寸比第1张（Tahani）更小（近大远小）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较可见区域的高度；宽度受倾斜影响，只作辅助。
- **SR-06.C5** 斜靠组第3张（Chidi）渲染尺寸比第2张（Jason）更小（近大远小）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较可见区域的高度；宽度受倾斜影响，只作辅助。
- **SR-06.C6** 斜靠组第4张（Eleanor）渲染尺寸比第3张（Chidi）更小（近大远小）。
  - 判定：程序；证据：`geometry`；来源：`layout_constraints`「大小和高低符合近大远小的透视」。备注：比较可见区域的高度；宽度受倾斜影响，只作辅助。
- **SR-06.C7** 斜靠组第1张（Tahani）可见卡片厚度：至少一侧边缘有与画面不同的窄边，表现卡片的侧面。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「海报是有一定厚度的卡片」。备注：该句紧接斜靠组的描述，只适用于斜靠组；悬浮组不要求厚度。
- **SR-06.C8** 斜靠组第2张（Jason）可见卡片厚度：至少一侧边缘有与画面不同的窄边，表现卡片的侧面。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「海报是有一定厚度的卡片」。备注：该句紧接斜靠组的描述，只适用于斜靠组；悬浮组不要求厚度。
- **SR-06.C9** 斜靠组第3张（Chidi）可见卡片厚度：至少一侧边缘有与画面不同的窄边，表现卡片的侧面。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「海报是有一定厚度的卡片」。备注：该句紧接斜靠组的描述，只适用于斜靠组；悬浮组不要求厚度。
- **SR-06.C10** 斜靠组第4张（Eleanor）可见卡片厚度：至少一侧边缘有与画面不同的窄边，表现卡片的侧面。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「海报是有一定厚度的卡片」。备注：该句紧接斜靠组的描述，只适用于斜靠组；悬浮组不要求厚度。

### SR-07 斜靠组的光影

- **SR-07.C1** 斜靠组第1张（Tahani）有可见投影：投影在海报背光的左侧或左下方，与海报相连，同时落在墙面和地面上，并有深浅过渡；没有投影、投影朝右或朝上，或只是与海报同形的平移色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从右上方照来，斜靠的海报在墙面和地面上投下自然的影子」。
- **SR-07.C2** 斜靠组第2张（Jason）有可见投影：投影在海报背光的左侧或左下方，与海报相连，同时落在墙面和地面上，并有深浅过渡；没有投影、投影朝右或朝上，或只是与海报同形的平移色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从右上方照来，斜靠的海报在墙面和地面上投下自然的影子」。
- **SR-07.C3** 斜靠组第3张（Chidi）有可见投影：投影在海报背光的左侧或左下方，与海报相连，同时落在墙面和地面上，并有深浅过渡；没有投影、投影朝右或朝上，或只是与海报同形的平移色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从右上方照来，斜靠的海报在墙面和地面上投下自然的影子」。
- **SR-07.C4** 斜靠组第4张（Eleanor）有可见投影：投影在海报背光的左侧或左下方，与海报相连，同时落在墙面和地面上，并有深浅过渡；没有投影、投影朝右或朝上，或只是与海报同形的平移色块的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「光线从右上方照来，斜靠的海报在墙面和地面上投下自然的影子」。
- **SR-07.C5** 斜靠组第1张（Tahani）表面有可见的明暗与反光，朝向光源的右上部分更亮或带反光，背光的左下部分更暗；完全没有表面光影，或亮暗方向与右上光源相反的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「表面带有与光照方向一致的明暗和反光」。
- **SR-07.C6** 斜靠组第2张（Jason）表面有可见的明暗与反光，朝向光源的右上部分更亮或带反光，背光的左下部分更暗；完全没有表面光影，或亮暗方向与右上光源相反的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「表面带有与光照方向一致的明暗和反光」。
- **SR-07.C7** 斜靠组第3张（Chidi）表面有可见的明暗与反光，朝向光源的右上部分更亮或带反光，背光的左下部分更暗；完全没有表面光影，或亮暗方向与右上光源相反的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「表面带有与光照方向一致的明暗和反光」。
- **SR-07.C8** 斜靠组第4张（Eleanor）表面有可见的明暗与反光，朝向光源的右上部分更亮或带反光，背光的左下部分更暗；完全没有表面光影，或亮暗方向与右上光源相反的不满足。
  - 判定：Judge；证据：`screenshot_visual`；来源：`layout_constraints`「表面带有与光照方向一致的明暗和反光」。
## GT 自查（1280×900，本地 Chromium，0 API）

脚本 `gt_selfcheck.py`，只验证程序条件可执行、GT 能通过，不向 input 增加要求。

| 条件 | GT 实测 | 结果 |
|---|---|---|
| SR-02/03 数量、位置-地址、替代文字 | 两组各 4 张，顺序 Tahani→Eleanor，alt 全部正确 | 通过 |
| SR-04.C2 居中 | 左右边距 340 / 340 | 通过 |
| SR-04.C3–C5 一行、同宽、等距 | 顶边都是 50；宽都是 130；间距 26.7 ×3 | 通过 |
| SR-04.C6–C13 比例、正面 | 宽高比偏差 0；transform 全为 none | 通过 |
| SR-05.C2 大致居中 | 整组中心偏右 10.9px | 通过 |
| SR-05.C3–C5 窄缝不重叠 | 外接框间距 9.9 / 6.8 / 4.7 | 通过 |
| SR-05.C14 略大 | 平均宽 1.20 倍、高 1.22 倍 | 通过 |
| SR-05.C15 明显空白 | 340px | 通过 |
| SR-06.C1–C3 逐张升高 | 底边 832 → 809 → 787 → 766 | 通过 |
| SR-06.C4–C6 逐张变小 | 高 218 → 213 → 209 → 203 | 通过 |

Judge 条件（墙角、靠墙、厚度、投影、表面光影、悬浮组无投影）已在 GT 截图上人工核对：墙角线左低右高，影子在每张海报左侧并落到地面，表面左下暗、右上有反光，左缘有灰色厚度边。正式 Judge 未跑。

## 用户确认结果（2026-11-17，“按建议处理”）

1. SR-01.C3 保留。2. 沿用并列失败合并裁定。3. 只用 1280×900。4. 投影最低标准采用。

## 原待确认问题

1. **SR-01.C3 墙角场景横贯全宽。** input 没有直接这么写，依据是“画面中有一面墙和一块地面”作为背景的语义。保留还是删除？
2. **并列失败合并裁定。** 227 是否沿用 case-213 的分组只扣一档规则？
3. **单一视口。** 只用 1280×900 采证，是否需要加一个 1920×1080？
4. **SR-07.C1–C4 投影的最低标准**写了“在背光一侧、与海报相连、落在墙面和地面、有深浅过渡，不能只是平移色块”。“自然”按这个标准判是否合适？
