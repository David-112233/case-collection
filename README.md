# case-collection

前端代码生成评测基准主仓库的**案例采集与加工子集**，由 dot 和 duet 两个智能体在云端协作，成果由用户拉取到本地后并入主仓库。统一规则见 [AGENTS.md](AGENTS.md)。

| 区 | 做什么 | 入口 |
|---|---|---|
| `data_intake/` | 采集：搜索、认领、抓取、筛选，直到用户做出判定 | [data_intake/README.md](data_intake/README.md) |
| `cases/` | 正式案例区：用户选中的案例在这里入库和加工，编号与主仓库一致（228 起） | [cases/README.md](cases/README.md)、[INDEX](cases/INDEX.md) |
| `reference/` | 主仓库规范的只读快照：背景、标准、skill、样例、去重索引 | [reference/SYNC.md](reference/SYNC.md) |
| `scripts/` | 抓取脚本与案例自检脚本 | — |
