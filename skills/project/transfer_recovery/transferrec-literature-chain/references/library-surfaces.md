# TransferRec Literature Surfaces

这是 `transferrec-literature-chain` 的 repo 内速查表，用来提醒当前项目已经有哪些稳定文献面。

## Default Root

- `docs/library/trajectory_representation/`

## Progressive Access Layers

- `L1`
  - `docs/library/trajectory_representation/INDEX.md`
- `L2`
  - `docs/library/trajectory_representation/papers/<slug>/README.md`
- `L3`
  - `docs/library/trajectory_representation/papers/<slug>/paper.md`
- `L4`
  - `docs/library/trajectory_representation/papers/<slug>/paper.pdf`

## Machine-Readable Files

- `docs/library/trajectory_representation/catalog.json`
- `docs/library/trajectory_representation/summary.json`
- `docs/library/trajectory_representation/papers/*/meta.json`
- `docs/library/trajectory_representation/seed_notes/seed_related_catalog.json`

## Human Entry Points

- `docs/library/trajectory_representation/README.md`
- `docs/library/trajectory_representation/QUERY_GUIDE.md`
- `docs/library/trajectory_representation/seed_notes/README.md`

## Main Scripts

- query:

```bash
python3 scripts/query_trajectory_paper_library.py --q "trajectory recovery"
python3 scripts/query_trajectory_paper_library.py --q "route choice" --fulltext
```

- rebuild curated core library:

```bash
python3 scripts/build_trajectory_paper_library.py
python3 scripts/build_trajectory_paper_library.py --force
```

## Interpretation Rules

- `seed_notes/` is an extension pool, not the same thing as the promoted core library
- a paper is only "in the project literature chain" after PDF + Markdown + card + metadata exist under `papers/<slug>/`
- external acquisition can finish before project promotion finishes
