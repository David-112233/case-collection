# B1 进度（DATA-002）

- 方案：[B1 工作方案](../../project_state/handoffs/DATA-001-workplan-B1-20261002.md)；决策 DEC-031—036。
- 完整收集路径与云端执行说明：[data_intake/README.md](../README.md)。
- 当前位置：已入库 7 例（case-211—217）。211/212/213/214/217 已写 input.json 与 GT 并自测，停在**检查点 B** 等待用户审核（见 [checkpoint_B.md](checkpoint_B.md)）；215/216 待写。

## 文件

| 文件 | 内容 |
|---|---|
| `candidates*.csv` | 网页搜索发现的候选链接（4 份） |
| `raw/{作者}__{ID}/` | 仅保留后续批次候选；拒收与已入库者已删除（2026-10-18 用户同意），可按 screening.csv 中链接重抓 |
| `screening.csv` / `decide.py` | 每个候选的判断：决定、档位、命中特征、证据、原因码（U1/U2=用户未选）、JS 处理 |
| `intake.py` | 入库脚本：写 source_original.html、source.html（JS 删除/替换）、metadata.json、classification.json。已执行列表对应的 raw 已删除，下次入库需更新 APPROVED |
| `triage.py` / `peek.py` | 只读汇总与查看工具 |
| `shot.py` | Playwright 无头截图/测量（--offline 拦截外部请求，--evalfile、--click） |
| `checkpoint_B.md` | 检查点 B：5 例待审版本哈希、自测要点、相对来源的改动 |

## 已入库

| 案例 | 来源 | 说明 | input/GT |
|---|---|---|---|
| case-211-T4 | HejChristian/azzWVWL | 双层吸附轮播；删除非核心 JS | 已写，待审 |
| case-212-T4 | allanwhite/oNNbpqx | 菜单 JS 改为 checkbox 状态；删除懒加载 | 已写，待审 |
| case-213-T1 | thebabydino/gOdPzEK | 斜切锯齿信息图 | 已写，待审 |
| case-214-T4 | una/myJOjQx | 行程页：吸附+编号+滑动指针 | 已写，待审 |
| case-215-T4 | utilitybend/ZYOKRXV | 可滚动状态驱动双侧箭头的表格页 | 未写 |
| case-216-T1 | letsbleachthis/zewKYE | 针织品牌着陆页；删除 AOS 滚动动画 | 未写 |
| case-217-T1 | xdesro/dVxpgN | 静态 3D 等距塔楼 | 已写，待审 |

下一步：检查点 B 用户审核 → 冻结哈希 → 写 215/216 → 按 DEC-036 继续采集补足 T1/T4。

后续批次候选（hold）：T2 7、T3 6、T5 11，见 screening.csv。
