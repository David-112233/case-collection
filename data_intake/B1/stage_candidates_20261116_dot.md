# dot 第二轮阶段候选清单（2026-11-16）

## 当前结论
这不是10个最终合格案例。55个新候选已认领并成功获得源码；本清单用于先校准质量。重点传统网页，多物体三维空间为补充；JS、图片和链接原样保留。未加载图片不直接拒收。所有下列候选均未正式入库。

## 优先请用户校准
|候选|来源|具体难点|已知验证范围/限制|
|---|---|---|---|
|Stats Dashboard|https://codepen.io/oliviale/pen/BaKamvY|12列不规则网格、跨幅卡片、照片超出卡面、错位位移、复合阴影、竖排旋转标题；比213增加异构区块和多方向交叠|源码已读；浏览器首屏见黄色/青色错位图文，右/下裁切，尚未完整/窄屏核验；部分外部素材可能环境受限|
|Wedding Planning App|https://codepen.io/oliviale/pen/rNWyzmx|多个异构手机画布整体旋转20度并不同纵向位移，内部登录、照片墙、清单、宾客、预算等布局，照片旋转及阴影|首屏已看，真实定位是应用界面展示墙，不是单一传统应用；多画布有意出界，未操作全部交互|
|3D Modern House|https://codepen.io/ricardoolivaalonso/pen/yLOpNdZ|多建筑体块、透明玻璃、门窗、泳池、台阶、家具与统一透视投影；比217增加异构体块和遮挡|浏览器首屏已见；非传统网页，作为空间补充；鼠标小幅转视角，停止后稳定，未测试全部视角|
|3D Summer House|https://codepen.io/ricardoolivaalonso/pen/BazMqJx|建筑、玻璃、窗框、分面反光、灯光和影面关系；灯光开关两稳定状态|源码已读，未完整视觉核验；keyframes存在但未被引用，不应当作持续动画；鼠标视角/开关待测|

## 比较/备选，不先宣称更难
- Bullet Journal：https://codepen.io/oliviale/pen/aPwaXm 。异构双页手账、倾斜照片/胶带、书脊渐变与多重阴影；首屏已见，但排列较规则、色彩克制，超213的证据仍有争议。
- Job Recruiter Dashboard：https://codepen.io/aybukeceylan/pen/poEqdWZ 。多圆环、Canvas图表、多列异构信息；入场动画停止后可检查。首屏图表仅见坐标网格，原因未查明，不因此拒收，仍待素材/脚本核验。
- Three-plane Grid：https://codepen.io/andybarefoot/pen/MERBPx 。约50个异构内容项分布三倾斜平面并交叠，源码无持续动画；页面约420vw高，需报告静态长页覆盖成本，尚无视觉核验。

## 明确不适合当前方向的机制示例
- Layout is overrated：Matter.js逐帧物理模拟、随机速度和持续位移旋转。
- Creative Cloud Glassmorphism：全屏自动循环视频，不能因为CSS无关键帧就说静态。
- Synthwave / Cyberpunk City / 建造城堡：连续闪动、滚字、车辆或长时间多阶段建造，评分时间帧负担高。
这些问题在于动态评分成本，不是因为JS或外部资源被禁止；不擅自删除源码机制来让它通过。

## 仓库状态与证据
- 本轮34+21=55候选认领先于获取；main认领提交 eeb53873482cefb7eb9822eb9130fddcef41dff9、8bc7f9157ff1dd77eef2013dd2b2a489e023f4b1。
- 55源码请求成功不等于55合格。尚无本轮终判accept，也未完成全部页面、所有状态或双视口核验。
- 本草稿先保存首34份完整原始输出和部分后续已上传源码，剩余源码正在追加；不能把缺少文件视为抓取失败。
- 当前规则见同目录 collection_scope_20261116_dot.md。首轮历史判断仍在PR #1，本草稿不改变其当时口径。

