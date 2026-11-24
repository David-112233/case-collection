# 案例收集全流程

从找到候选作品，到案例入库、做准静态 GT、写 input、两次用户审核、规则、同步回主仓库。图在 GitHub 上会直接渲染；各步骤的命令和规则见 [data_intake/README.md](README.md)（采集）与 [cases/README.md](../cases/README.md)（入库后的加工）。

颜色：绿色是 dot、duet 在云端做的，橙色是用户做的，紫色是 Claude 在本地做的，灰色是结果。

## 一、从发现到用户标注（步骤 1–6）

```mermaid
flowchart TD
    A["1 发现候选<br/>网页搜索 CodePen 链接"] --> B["2 认领<br/>先推 main，自动查重"]
    B --> C["3 抓取源码<br/>存入 pending/"]
    C --> D["4 筛选并记录<br/>写入 batches/ 的筛选表"]
    D --> E["5 整理审核清单<br/>放进 review_lists/"]
    E --> F["6 用户逐个标 1 或 0<br/>本地审核清单"]
    F -->|标 0| G["二轮备选<br/>只留原作链接，不删"]
    F -->|标 1| H["进入入库<br/>见第二张图"]

    classDef cloud fill:#E1F5EE,stroke:#0F6E56,color:#085041
    classDef user fill:#FAEEDA,stroke:#854F0B,color:#633806
    classDef result fill:#F1EFE8,stroke:#5F5E5A,color:#444441
    class A,B,C,D,E cloud
    class F,H user
    class G result
```

## 二、从入库到同步回主仓库（步骤 7–14）

加工顺序是：**来源源码 → 准静态 GT → 由 GT 写出 input → 用户审核 → 规则 → 用户审核 → 本地冻结**。有两个审核关卡，每个关卡 duet 都停下等用户。

```mermaid
flowchart TD
    H["7 入库（dot）<br/>admit_case.py，编号从 case-228 起"] --> I["8 做 GT（duet）<br/>以 source.html 为基础，准静态，无动画"]
    I --> J["9 复核档位并写 input<br/>input 由 GT 写出，阶段：待审核 GT 与 input"]
    J --> K["10 用户审核 GT 与 input<br/>关卡一"]
    K -->|有意见| L["duet 按指令修改<br/>再提交"]
    L --> J
    K -->|通过| M["11 写规则草稿（duet）<br/>来源是 input，不是 GT；check_rules 自检"]
    M --> N["12 用户审核规则<br/>关卡二"]
    N -->|有意见| O["duet 修改规则<br/>再提交"]
    O --> M
    N -->|通过| P["13 本地冻结<br/>Claude 在本地做"]
    P --> Q["14 同步主仓库<br/>案例目录原样拷回"]

    classDef cloud fill:#E1F5EE,stroke:#0F6E56,color:#085041
    classDef user fill:#FAEEDA,stroke:#854F0B,color:#633806
    classDef local fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    class H,I,J,L,M,O cloud
    class K,N user
    class P,Q local
```

## 每一步对应的位置

| 步骤 | 谁 | 工具 | 产出位置 |
|---|---|---|---|
| 1 发现 | dot / duet | 网页搜索 | `data_intake/batches/<批次>/candidates.csv` |
| 2 认领 | dot / duet | `tools/claim.py` | `data_intake/ledger/claims.csv` |
| 3 抓取 | dot / duet | `scripts/codepen_collection/fetch_cdpn.py` | `data_intake/pending/<作者__ID>/` |
| 4 筛选 | dot / duet | `tools/peek.py`、`shot.py`、`decide.py` | `data_intake/batches/<批次>/screening.csv` |
| 5 清单 | dot / duet | — | `data_intake/review_lists/<日期>_<agent>/` |
| 6 标注 | 用户 | — | 审核清单里的 1 / 0；状态记入 `ledger/review.csv` |
| 7 入库 | dot | `tools/admit_case.py`（先预演，再 `--apply`） | `cases/case-NNN-TX/`（档位暂定）、`cases/registry.csv` |
| 8 做 GT | duet | Playwright 自检 | `ground_truth.html`、`review_<日期>/`、案例 README 里的改动说明；阶段 `gt_ready` |
| 9 复核档位、写 input | duet | `tools/registry.py retier` | `input.json`、`input_problem.md`；阶段 `input_draft` |
| 10 审核关卡一 | 用户 | `registry.py set-stage … input_approved --by-user` | 用户通过后阶段 `input_approved` |
| 11 写规则 | duet | `scripts/case_tools/check_rules.py` | `rules_drafts/manual_v1/`；阶段 `ready_for_review` |
| 12 审核关卡二 | 用户 | — | 用户审核规则 |
| 13 冻结 | Claude（本地） | `registry.py set-stage … frozen --local` | `FREEZE_v*.json` |
| 14 同步 | Claude（本地） | `registry.py set-stage … synced --local` | 主仓库 `cases/` |
