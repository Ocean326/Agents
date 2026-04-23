---
name: transferrec-literature-chain
description: Transfer_Recovery 专用文献链入口。用于先查询仓库内已有 trajectory paper library，再按需调用 DeepXiv 或通用文献获取链补位，并把新材料回写到当前项目的 progressive-access 文档库中。
---

# TransferRec Literature Chain

把当前仓库里的文献工作流当成一条连续链路，而不是一次性的“找篇论文”。

默认服务对象：

- `TransferRec` 主表扩充与 baseline 纳入判断
- 非 AR decoder 的 representation / transfer 支线
- 与 trajectory recovery、map matching、trajectory representation 强相关的持续文献积累

## 本地优先原则

先查当前仓库，再决定是否出网。

当需要 repo 内当前文献 surfaces 的简表时，读取 [references/library-surfaces.md](./references/library-surfaces.md)。

当前项目的默认文献根目录：

- `docs/library/trajectory_representation/`

核心 surfaces：

- `L1`: `docs/library/trajectory_representation/INDEX.md`
- `L2`: `docs/library/trajectory_representation/papers/<slug>/README.md`
- `L3`: `docs/library/trajectory_representation/papers/<slug>/paper.md`
- `L4`: `docs/library/trajectory_representation/papers/<slug>/paper.pdf`
- machine-readable:
  - `docs/library/trajectory_representation/catalog.json`
  - `docs/library/trajectory_representation/summary.json`
  - `docs/library/trajectory_representation/papers/*/meta.json`
  - `docs/library/trajectory_representation/seed_notes/seed_related_catalog.json`

先读：

- `docs/library/trajectory_representation/README.md`
- `docs/library/trajectory_representation/QUERY_GUIDE.md`

## 何时使用

在这些场景使用这个 skill：

- 先判断某篇论文是否已经在当前项目文档库里
- 围绕 trajectory recovery / map matching / trajectory representation 做本地优先查询
- 把新论文纳入当前项目的 PDF + Markdown 双附件链
- 更新主线库、seed notes、或 query surfaces
- 给后续 `research-paper-reading-compass`、`research-novelty-audit`、`compile-tech-notes` 准备稳定文献输入

不要在这些场景把它当成唯一入口：

- 单纯要全网搜开放话题
- 只想读一篇泛论文，不需要回写到当前仓库
- 只是做正式 novelty audit 或 proposal critique

## 默认工作模式

先判断这次任务属于哪一类：

- `local-query`
  - 先查当前库里有没有
- `external-acquire`
  - 本地没有，需要外部检索与下载
- `project-promotion`
  - 已拿到 PDF / Markdown，准备纳入当前项目库
- `library-refresh`
  - 重建或刷新已有 trajectory library surfaces

一次只锁定一个主模式，不要边搜、边读、边写报告、边扩库。

## 工作流

### 1. Local Query First

优先使用当前仓库已有查询面：

```bash
python3 scripts/query_trajectory_paper_library.py --q "trajectory recovery"
python3 scripts/query_trajectory_paper_library.py --q "route choice" --fulltext
python3 scripts/query_trajectory_paper_library.py --q "TransferTraj PTR" --json
rg -n "TransferTraj|PLMTrajRec|RoutesFormer|DiffMM|UMSST" docs/library/trajectory_representation
```

如果已经命中：

- 优先读 `README.md`
- 需要全文时再读 `paper.md`
- 只有版式或图表核对需要时才回到 `paper.pdf`

### 2. Choose The External Lane Narrowly

当本地库不足时，按这个优先级补位：

1. `deepxiv`
   - 适合 arXiv / PMC 友好的论文搜索、短摘要筛查、`brief -> head -> section -> full` 渐进阅读
2. `literature-finder-downloader`
   - 适合 BibTeX / RIS / DOI / title batch 的批量获取、落地 PDF、生成 acquisition artifacts
3. `parallel-web-search` 或 `web-finder`
   - 适合 wider web discovery、非 arXiv 来源、找官网/代码/讨论

规则：

- `DeepXiv` 更像文献数据接口层，不是当前项目的长期文献库
- 批量 acquire 结束后，仍然要回写到当前仓库的 progressive-access 结构
- 不要把 Downloads、临时输出目录或某次 chat 输出当成项目主文献库

### 3. Keep The Project Library Shape Stable

当前项目默认保留这四层：

- `L1`: 顶层索引与分流
- `L2`: 单篇卡片
- `L3`: 全文 Markdown
- `L4`: 原始 PDF

只有满足下面条件，才能说“论文已进入当前项目文献链”：

- 论文目录存在于 `docs/library/trajectory_representation/papers/<slug>/`
- 同时有 `paper.pdf` 与 `paper.md`
- 有 `meta.json`
- 有 `README.md`
- 根层 `catalog.json` / `INDEX.md` 已同步或明确说明尚未同步

如果只是 acquire 到了外部 seed 或临时目录：

- 算 `external-acquire complete`
- 不算 `project-promotion complete`

### 4. Use Existing Project Scripts Deliberately

当前仓库已有两个重要脚本：

- `scripts/query_trajectory_paper_library.py`
  - 默认查询入口
- `scripts/build_trajectory_paper_library.py`
  - 当前核心 trajectory library 的重建器

重建命令：

```bash
python3 scripts/build_trajectory_paper_library.py
python3 scripts/build_trajectory_paper_library.py --force
```

注意：

- `build_trajectory_paper_library.py` 面向当前已编排的核心 paper set，不是通用 intake 队列
- 对零散新论文，先 acquire 和整理，再决定是否 promotion 到核心库

### 5. Route Reading And Synthesis Explicitly

拿到稳定文献输入后，再按目标转交：

- 深读单篇或多篇：`research-paper-reading-compass`
- 判断是否值得推进：`research-novelty-audit`
- 形成汇总、批判或方案依据：`compile-tech-notes`

不要在 acquisition 尚未完成时，直接把不稳定材料写成结论性报告。

## 输出要求

每次使用这个 skill，至少交代：

- 当前任务属于哪种模式
- 本地库里已经有什么
- 外部补位用了哪条 lane
- 哪些材料已经进入项目文献链
- 哪些仍停留在外部 seed / 临时状态
- 下一步最合适的动作

## 常见触发语

- “先查一下这个论文在不在当前项目文档库里”
- “把这批轨迹论文接进 Transfer_Recovery 的文献链”
- “用当前项目的 progressive access 结构整理这些论文”
- “如果本地没有，就用 DeepXiv 或下载链补进来”
