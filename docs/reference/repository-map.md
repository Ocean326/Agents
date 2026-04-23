# Repository Map

## Goal

Keep agent material organized by portability and scope:

- global reusable skills
- project-bound skills
- config examples
- usage documentation

## Tree

```text
.
├── AGENTS.md
├── README.md
├── configs/
│   └── examples/
│       └── codex/
├── docs/
│   ├── reference/
│   └── usage/
└── skills/
    ├── INDEX.md
    ├── global/
    └── project/
        └── transfer_recovery/
```

## Placement Rules

### `skills/global/`

Use for reusable custom skills that are not tied to a single repo.

Examples:

- delivery / orchestration skills
- research workflow skills
- synthesis and documentation skills

### `skills/project/`

Use for skills that make sense only with project context.

Each project gets its own namespace folder.

Current example:

- `skills/project/transfer_recovery/`

### `configs/examples/`

Use for public-safe examples only.

Examples that belong here later:

- sample `config.toml` fragments
- example `AGENTS.md` snippets
- example automation prompt shapes

### `docs/usage/`

Use for "how to use this repo" material.

### `docs/reference/`

Use for stable repository documentation and indexes.
