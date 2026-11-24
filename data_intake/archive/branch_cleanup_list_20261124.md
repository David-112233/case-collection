# 远程分支清理清单（只出清单，未删除任何分支、未关闭任何 PR）

日期：2026-11-24。口径：对每个分支，取它相对 `main` 新增或修改的全部文件，检查其内容是否已出现在整理后的 `main` 里（文本文件忽略换行符差异）。
已入库案例的 `metadata.json`、`classification.json` 在入库时补写了案例号，已按“已并入”处理。

共 66 个分支：**66 个内容已全部并入 `main`**，0 个仍有文件未并入（见最后一列）。删除须你逐条同意；删分支不影响 Git 历史里的提交，但 PR 页面会显示分支已删除。

| 分支 | 最后提交 | PR | 新增/修改文件 | 已并入 | 建议 | 说明 |
|---|---|---|---|---|---|---|
| `collect/dot-2026-11-10-01` | 2026-11-10 | #1 | 121 | 121 | 可删除 | 任务三：dot 第01轮39份源码及32条初筛记录 |
| `collect/dot-2026-11-16-02` | 2026-11-16 | #2 | 201 | 201 | 可删除 | 交付10项建议清单，明确静态多页成本与所有证据边界 |
| `collect/dot-2026-11-18-02` | 2026-11-18 | #3 | 16 | 16 | 可删除 | 补充第07轮五条空间候选筛选意见（待用户审核） |
| `collect/dot-2026-11-18-03` | 2026-11-18 | #4 | 19 | 19 | 可删除 | collect: preserve batch 08 candidate evi |
| `collect/dot-2026-11-18-04` | 2026-11-18 | #5 | 13 | 13 | 可删除 | Collect spatial candidate batch 09: B1/s |
| `collect/dot-2026-11-18-05` | 2026-11-18 | #6 | 10 | 10 | 可删除 | Collect batch 10 candidate evidence; awa |
| `collect/dot-2026-11-18-06` | 2026-11-18 | #7 | 13 | 13 | 可删除 | Collect batch 11: B1/screening_dot_11.cs |
| `collect/dot-2026-11-18-07` | 2026-11-18 | #8 | 19 | 19 | 可删除 | archive batch12 candidate source and con |
| `collect/dot-2026-11-18-01` | 2026-11-18 | #10 | 30 | 30 | 可删除 | 补归档：首批 10 个空间关系候选的原始采集文件（待审核） |
| `collect/dot-2026-11-19-14` | 2026-11-18 | #11 | 32 | 32 | 可删除 | Archive 10 spatial frontend candidates a |
| `collect/dot-2026-11-19-02` | 2026-11-18 | #12 | 32 | 32 | 可删除 | Archive 10 spatial CodePen candidates an |
| `collect/dot-2026-11-18-08` | 2026-11-18 | #9 | 21 | 21 | 可删除 | Backfill triage metadata for six round 1 |
| `collect/dot-2026-11-19-11` | 2026-11-18 | #13 | 32 | 32 | 可删除 | Archive 10 reviewed spatial case candida |
| `collect/dot-2026-11-19-04` | 2026-11-18 | #14 | 30 | 30 | 可删除 | Archive one separately labeled source-on |
| `collect/dot-2026-11-19-06` | 2026-11-18 | #15 | 32 | 32 | 可删除 | Archive round 18 spatial candidates for  |
| `collect/dot-2026-11-19-05` | 2026-11-19 | #16 | 29 | 29 | 可删除 | Archive nine reviewed spatial-layout can |
| `collect/dot-2026-11-19-07` | 2026-11-19 | #17 | 32 | 32 | 可删除 | chore(intake): archive ten spatial floor |
| `collect/dot-2026-11-19-08` | 2026-11-19 | #18 | 29 | 29 | 可删除 | Archive 07:12 spatial candidates and one |
| `collect/dot-2026-11-19-09` | 2026-11-19 | #19 | 29 | 29 | 可删除 | Archive nine spatial candidates for user |
| `collect/dot-2026-11-19-10` | 2026-11-19 | #20 | 32 | 32 | 可删除 | chore(intake): preserve and document ten |
| `collect/dot-2026-11-19-1012-batch24` | 2026-11-19 | #21 | 32 | 32 | 可删除 | Collect 10 layered and interlocking fron |
| `collect/dot-20261119-1112z` | 2026-11-19 | #22 | 32 | 32 | 可删除 | Archive 10 verified spatial candidates f |
| `collect/dot-2026-11-19-1212` | 2026-11-19 | #23 | 32 | 32 | 可删除 | Collect 10 spatial candidates for review |
| `collect/dot-2026-11-19-1312utc` | 2026-11-19 | #24 | 26 | 26 | 可删除 | Archive 8 spatial candidates for user re |
| `collect/dot-2026-11-19-1412` | 2026-11-19 | #25 | 26 | 26 | 可删除 | Archive eight reviewed spatial frontend  |
| `collect/dot-2026-11-19-1512z` | 2026-11-19 | #26 | 20 | 20 | 可删除 | Archive six spatial candidates for manua |
| `collect/dot-2026-11-19-1612` | 2026-11-19 | #27 | 26 | 26 | 可删除 | Archive eight layered scene candidates f |
| `dot/candidates-spatial-20261119-1712` | 2026-11-19 | #28 | 32 | 32 | 可删除 | Archive 10 spatial candidates for review |
| `dot/candidates-spatial-20261119-1812` | 2026-11-19 | #29 | 26 | 26 | 可删除 | Archive 8 spatial candidates for review  |
| `dot/candidates-spatial-20261119-1912` | 2026-11-19 | #30 | 20 | 20 | 可删除 | Archive 6 spatial candidates for review  |
| `dot/candidates-spatial-20261119-2012` | 2026-11-19 | #31 | 23 | 23 | 可删除 | Archive 7 spatial candidates for review  |
| `dot/candidates-spatial-20261119-2112` | 2026-11-19 | #32 | 20 | 20 | 可删除 | Archive 6 spatial candidates for review  |
| `dot/candidates-spatial-20261119-2212` | 2026-11-19 | #33 | 14 | 14 | 可删除 | Archive 4 spatial candidates for review  |
| `dot/candidates-spatial-20261119-2312` | 2026-11-19 | #34 | 17 | 17 | 可删除 | Archive 5 spatial candidates for review  |
| `dot/candidates-spatial-20261120-0012` | 2026-11-19 | #35 | 20 | 20 | 可删除 | Archive 6 spatial candidates for review  |
| `intake/dot-20261120-0112` | 2026-11-19 | #36 | 11 | 11 | 可删除 | Stage three spatial case candidates for  |
| `dot/candidates-20261120-0212` | 2026-11-19 | #37 | 11 | 11 | 可删除 | Stage three spatial examples for review  |
| `dot/spatial-20261120-0412` | 2026-11-19 | #38 | 8 | 8 | 可删除 | Stage two unadmitted spatial candidates  |
| `dot/spatial-20261120-0512` | 2026-11-20 | #39 | 5 | 5 | 可删除 | Stage 05:12 spatial candidate for review |
| `dot/spatial-20261120-0612` | 2026-11-20 | #40 | 8 | 8 | 可删除 | Stage 06:12 UTC spatial candidates for r |
| `dot/b1-candidates-20261120-0712` | 2026-11-20 | #41 | 5 | 5 | 可删除 | Archive one spatial layering candidate f |
| `dot/spatial-batch-20261120-0312` | 2026-11-20 | #42 | 8 | 8 | 可删除 | Stage two spatial candidates for review  |
| `collect/dot-20261120-0812-independent` | 2026-11-20 | #43 | 9 | 9 | 可删除 | Stage two independent spatial demos for  |
| `collect/dot-20261120-0912-static` | 2026-11-20 | #44 | 15 | 15 | 可删除 | Stage static and settled spatial candida |
| `collect/dot-2026-11-20-42` | 2026-11-20 | #45 | 14 | 14 | 可删除 | Archive four visually checked static spa |
| `collect/dot-20261120T1112Z` | 2026-11-20 | #46 | 9 | 9 | 可删除 | Archive two quasi-static spatial candida |
| `collect/dot-20261120T1212Z` | 2026-11-20 | #47 | 9 | 9 | 可删除 | Collect two static-frame spatial device  |
| `collect/dot-2026-11-20-1312z` | 2026-11-20 | #48 | 6 | 6 | 可删除 | Archive 13:12 static-first spatial candi |
| `collect/dot-2026-11-20T1412Z` | 2026-11-20 | #49 | 9 | 9 | 可删除 | Archive two paused spatial references (2 |
| `collect/spatial-20261120T1512Z-dot` | 2026-11-20 | #50 | 9 | 9 | 可删除 | Archive two stable CSS spatial reference |
| `collect/dot-20261120-1612` | 2026-11-20 | #51 | 7 | 7 | 可删除 | Stage one quasi-static spatial candidate |
| `collect/dot-20261120-1712` | 2026-11-20 | #52 | 7 | 7 | 可删除 | Stage one quasi-static spatial candidate |
| `collect/dot-20261120-1812` | 2026-11-20 | #53 | 7 | 7 | 可删除 | Stage one settled spatial candidate (dot |
| `collect/dot-20261120-1912` | 2026-11-20 | #54 | 7 | 7 | 可删除 | Stage one nested spatial case (dot 20261 |
| `collect/dot-20261120-2012` | 2026-11-20 | #55 | 7 | 7 | 可删除 | Stage one held-view spatial candidate (d |
| `dot/cases-20261120T2212Z` | 2026-11-20 | #56 | 8 | 8 | 可删除 | Archive C283 source_audit_dot_20261120T2 |
| `dot/cases-20261120T2312Z` | 2026-11-20 | #57 | 11 | 11 | 可删除 | Archive 23:12 source_audit_dot_20261120T |
| `dot/cases-20261121T0012Z` | 2026-11-20 | #58 | 7 | 7 | 可删除 | Archive C286 source_audit_dot_20261121T0 |
| `dot/cases-20261121T0112Z` | 2026-11-20 | #59 | 12 | 12 | 可删除 | Archive 01:12 source_audit_dot_20261121T |
| `collect/dot-20261121-0125-origamio` | 2026-11-20 | #60 | 16 | 16 | 可删除 | Stage recovered Origamio candidate C289  |
| `dot/cases-20261121T0212Z` | 2026-11-20 | #61 | 22 | 22 | 可删除 | Archive 02:12 source_audit_dot_20261121T |
| `dot/cases-20261121T0312Z` | 2026-11-20 | #62 | 59 | 59 | 可删除 | Archive 03:12 spatial review cases C292– |
| `intake/dot-spatial-20261121-0412` | 2026-11-20 | #63 | 19 | 19 | 可删除 | Archive two spatial candidates for revie |
| `intake/dot-spatial-20261121-0512` | 2026-11-21 | #64 | 48 | 48 | 可删除 | Archive three spatial candidates for rev |
| `intake/dot-spatial-20261121-0612` | 2026-11-21 | #65 | 31 | 31 | 可删除 | Archive final two spatial candidates for |
| `intake/dot-2026-11-20-c001-c030` | 2026-11-21 | - | 137 | 137 | 可删除 | Add reviewed spatial case selections C03 |
