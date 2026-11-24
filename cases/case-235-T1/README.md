# 3D Office - ThreeJS

来源：<https://codepen.io/ricardoolivaalonso/pen/NWJeBPE>（作者 ricardoolivaalonso，CodePen 公开作品，默认 MIT 许可）

当前阶段：`gt_ready`（入库于 2026-11-24），归属 duet。阶段以 [registry.csv](../registry.csv) 为准。

- 审核编号：C010；档位：T1（入库时按来源源码暂定为 T3，GT 完成后复核改为 T1，见下文“档位复核”）。
- 特色：立体办公室、家具分层

| 文件 | 说明 |
|---|---|
| `original_srcdoc.html` | 原始捕获，不改 |
| `source.html` | 来源预览（去掉 CodePen 控制台包装） |
| `source_original.html` | 修改前的来源副本；入库时与 `source.html` 相同，GT 改动后二者会不同，**不要因为相同而删除** |
| `metadata.json` | 来源、哈希、采集记录 |
| `classification.json` | 档位与入库依据 |

下一步由 duet 按顺序做（见 [cases/README.md](../README.md)）：① 以 `source.html` 为基础改造 `ground_truth.html`（尽量尊重源码，改成准静态、无动画、只保留简单交互）并自检；② 由 GT 写出 `input.json`；③ 停下，等用户审核 GT 与 input；④ 用户通过后才写 `rules_drafts/manual_v1/`。

## GT 相对来源的改动（2026-11-24，duet）

按用户 2026-11-24 的指示：采用固定视角（从斜上方看立体办公室），只保留立体办公室的静态细节，参考 case-224，做成与用户所给目标图类似的渲染结果。`ground_truth.html` 以 `source.html` 为基础，模型、贴图、灯光、材质参数、模型位置、样式和文案都不动。完整差异见 [review_20261124/source_to_gt.diff](review_20261124/source_to_gt.diff)。

| 改动 | 原因 |
|---|---|
| 删除 CodePen 样板：apple-touch-icon、`apple-mobile-web-app-title`、favicon、mask-icon、canonical、`stopExecutionOnTimeout` 脚本、`<body translate="no">` 的属性、`//# sourceURL=pen.js` | 与作品和评分无关（用户同意删除） |
| 删除 OrbitControls 脚本引用；`handleSetControls()` 不再建轨道控制，改为 `camera.position.setLength(16)` 与 `camera.lookAt(0, 0, 0)`；`animate()` 中删去 `controls.update()` 与平移夹取 | 固定视角，不能拖动、缩放、平移，也没有阻尼惯性 |
| 删除 `body` 的 `cursor: grab` | 没有拖动后，抓手光标会误导 |
| 删除两组 `click`、`touchstart` 监听和信息卡的 `click` 监听 | 去掉点击物体弹出商品信息卡、点击吊灯切换夜间模式；按用户“只保留静态细节、参考 224”的指示，GT 不保留交互 |
| `animate()` 中删除被点中物体每帧绕 Y 轴自转 0.03 弧度的代码 | 持续动画 |
| 删除显示器的视频元素和 `VideoTexture`，屏幕材质的 `map: videoTexture` 改为 `color: 0x000000`，其余参数（`metalness .1`、`roughness .1`、`toneMapped: false` 等）不变 | 循环播放的视频属于持续动态。静止化可以定格视频的某一帧，也可以去掉视频；用户给的目标图里屏幕是深色，所以取后者，屏幕显示为黑底加灯光反光。另从 raw.githubusercontent.com 取得同一提交的 `video.mp4` 抽帧查看：内容是 30 秒的彩色虚化光斑，与目标图的深色屏幕不同，说明用户渲染时视频没有显示在屏幕上，取深色与目标图一致。若想改为定格某一帧，需要用户指定 |

- **相机参数：** 竖直视场角 15°（来源原值），相机位置为来源的 (18, 6, 18) 沿原方向缩放到长度 16，约为 (11.01, 3.67, 11.01)，看向原点 (0, 0, 0)。理由：来源 OrbitControls 的 `maxDistance = 16` 在第一次更新时就把距离夹到 16，方向角（方位 45°、俯角约 13°）都在来源允许范围内，所以这正是来源打开时的初始视角；按模型顶点投影，它与目标图的构图吻合（见 [static_check.md](review_20261124/static_check.md)）。没有另选角度。
- **保留不动的地方：** `requestAnimationFrame` 渲染循环保留，只是每帧用同一相机渲染同一静止场景，这样模型和贴图异步加载完后会自动出现在画面上；窗口缩放时更新画布和相机宽高比的逻辑保留。加载层 `#loader`（带背景图和“Loading”字样的全屏遮罩）保留，`room.glb` 加载完就隐藏，属于来源的正常行为，最终画面里没有它；如果它一直不消失，说明模型没加载成功，正好作为自检信号。信息卡 `.message` 的 DOM、样式和 `showMessage`、`nightMode` 等函数保留但不再被调用，信息卡一直停在屏幕外，不可见。
- **外部资源：** three.js r124（cdnjs）、GLTFLoader 0.126（unpkg）、Montserrat（Google Fonts）、加载层背景图、11 个 `.glb` 模型和日间烘焙贴图 `baked.jpg`（rawcdn.githack.com）。本环境被代理拦截，**都未在浏览器里核实能否加载**。另从 raw.githubusercontent.com 取得同一提交的 11 个模型文件只读核对了节点和尺寸，文件没有放进仓库。
- **档位复核：** GT 无任何动态、没有交互，按难度模型 v2.1 为 T1，已用 `registry.py retier` 由暂定 T3 改为 T1（目录名随之改为 `case-235-T1`），`classification.json` 的 `tier_status`、`tier_basis`、`tier_note` 已手动同步。
- **自检：** 本环境不能渲染，只完成了静态检查和不需要浏览器的投影核对；渲染自检脚本 `review_20261124/gt_check.py` 已备好，待本地运行。
