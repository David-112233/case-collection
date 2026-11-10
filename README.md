# case-collection

前端代码生成评测基准主仓库的**采集子集**：只含从 CodePen 发现、抓取、筛选候选案例所需的脚本、候选表和参考文档，目录结构与主仓库一致，便于把结果按原路径拷回。

入口：[data_intake/README.md](data_intake/README.md)。`cases/` 下只有各案例的 `metadata.json`，仅供去重；`project_state/`、`docs/` 是只读副本。
