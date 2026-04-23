---
name: attach-personalbrain
description: Attach a PersonalBrain repository to the current task using a minimal, upgrade-friendly context rooted at the PersonalBrain path. Use when Codex should treat a PersonalBrain vault as shared durable memory for routing, retrieval, external-project awareness, or thin writeback, especially for external repo work, cross-machine lookup, or query tasks. Prefer an explicit root when provided, but if the current workspace or one of its ancestors already contains the stable anchors AGENTS.md and 40_governance/catalog.jsonl, attach automatically instead of asking for the path. In this installation, when running outside PersonalBrain and no local match exists, fall back to <PERSONALBRAIN_ROOT> after verifying the same anchors. Avoid hardcoding internal page paths beyond those stable anchors.
---

# Attach PersonalBrain

Use this skill as a thin attachment layer between the current task and a PersonalBrain repo.
Do not turn it into a heavy front gate or a reason to preload half the vault.

## Installed Default

For this installation, the verified PersonalBrain root is:

- `<PERSONALBRAIN_ROOT>`

Use this as the default fallback only after checking for a local or ancestor match and only if both required anchors still exist.

## Inputs

- `brain_root`
  - preferred: an explicit absolute path to the PersonalBrain repo
- `task`
  - the actual user request
- `external_project`
  - optional machine, root path, role, and entry point for a non-PersonalBrain project
- `mode`
  - optional intent hint:
    - `attach_only`
    - `retrieve_knowledge`
    - `reuse_skill`
    - `thin_writeback`
    - `register_project`
    - `append_signal`
- `writeback`
  - optional: whether durable notes or outputs should be written back

## Workflow

### 1. Resolve the root

Prefer this order:

1. use the explicit `brain_root` from the user
2. otherwise inspect the current working directory and walk upward through its ancestors
3. if any directory in that chain looks like PersonalBrain, use the nearest matching root
4. otherwise check the installed default root `<PERSONALBRAIN_ROOT>`
5. otherwise ask for the root path instead of guessing broadly

Treat a directory as a PersonalBrain root only if it contains both:

- `AGENTS.md`
- `40_governance/catalog.jsonl`

If the current task is already running inside a PersonalBrain repo, do not stop to ask for `brain_root`.
Only ask when there is no explicit root, no local or ancestor match, and the installed default root does not verify.

The installed default root is a local configuration for this environment, not a license to guess arbitrary PersonalBrain paths on other machines.

### 2. Read the minimum anchors

Read these first:

- `${brain_root}/AGENTS.md`
- `${brain_root}/40_governance/catalog.jsonl`

These are the stable attachment anchors.
Do not preload lots of other files unless the task needs them.

### 3. Discover task-specific context dynamically

Use the catalog to find the next files to read.
Prefer searching by:

- page id
- title
- tags
- obvious keywords from the task

For external project tasks, search the catalog before assuming any current page path.
Start with keywords such as:

- `project registry`
- `heartbeat protocol`
- `project awareness`
- the external project name or slug
- the concrete problem domain, such as `deploy`, `triage`, `debugging`, or `weekly review`

Current PersonalBrain installs often contain pages for:

- the heartbeat protocol
- the project registry
- active project snapshots
- prior outputs and reusable skills

Treat the catalog as the discovery surface and those pages as implementation details that may move.

### 4. Keep the attachment minimal

For a simple task, the minimum attachment is:

- the root path
- `AGENTS.md`
- `catalog.jsonl`

Add more only when justified by the task:

- machine routing pages for cross-machine work
- the heartbeat or project-awareness protocol for external repo tracking
- active project pages or fresh project signals for current execution context
- outputs, topics, or skills for prior conclusions
- governance logs only when a writeback or audit update will happen

### 5. Separate memory from execution

Use PersonalBrain for:

- durable memory
- routing
- reusable outputs
- summarized conclusions
- bounded project-awareness metadata

Use the external project repo for:

- implementation
- project-local artifacts
- runtime details
- volatile logs
- repo-specific scratch notes

Do not copy whole repos into PersonalBrain.
Do not treat `.local`, caches, sessions, embeddings, or search indexes as shared truth.

## External Project Integration

### Decision Rule

Choose the lightest mode that still solves the task:

1. one-off task or first contact with a repo
   - use ad-hoc path handoff only
   - do not create durable PersonalBrain changes just because the repo exists
2. repeated repo, active focus, or heartbeat should follow it
   - propose registration, or register it only when the task explicitly includes that write
3. need current status or blockers from that repo
   - read or append project signals only if the repo is already registered
4. need reusable knowledge from prior work
   - retrieve outputs, topics, or skills through the catalog
5. current task produces a reusable lesson
   - write back one focused durable page instead of dumping artifacts

### Project Awareness v1 Rules

When connecting an external repo to PersonalBrain awareness, keep these invariants:

- opt-in only
- repo-local first
- only repos explicitly listed in the project registry may feed project awareness
- only repo-local paths explicitly declared in `signal_paths` may be read automatically
- expired signals are `unknown`, not current truth
- do not silently widen awareness to task systems, chats, calendars, or ticket tools unless the user explicitly asks for that broader scope

### When To Register A Project

Register a project when at least one of these is true:

- the same repo keeps coming back across tasks
- the user wants PersonalBrain to auto-follow the repo
- the repo has stable local files that reflect status, blockers, or recent changes
- the repo should have a freshness-bound active project snapshot inside PersonalBrain

Stay ad-hoc when:

- the repo is being touched once
- there is no stable repo-local signal source yet
- the only benefit would be storing the path again

### Minimum Registration Contract

When a repo should join project awareness, the minimum contract is:

- `project_id`
- `repo_root`
- `signal_paths`
- `snapshot_file`
- `default_ttl`
- and usually `name`, `owner`, and `active`

Recommended row pattern:

```text
| `my_app` | `My App` | `/absolute/path/to/my_app` | `README.md`; `docs/status.md`; `CHANGELOG.md` | `10_state/active_projects/project_my_app.md` | `24h` | `ocean` | `true` |
```

Rules for registration:

- keep `signal_paths` narrow, repo-local, and human-legible
- prefer status files, changelogs, milestone notes, or concise roadmap docs
- `snapshot_file` should point to a freshness-bound state page, not a durable knowledge canon page
- follow the PersonalBrain repo contract for writes
- in the current PersonalBrain, `10_state/projects/registry.md` is suggest-first, so propose the row unless the user explicitly asked you to edit it

### Freshness And Signals

When the repo is already registered:

- read only declared `signal_paths`
- respect `default_ttl`
- treat stale or missing signals as `unknown`
- do not infer freshness from memory alone

If the task needs a fresh project signal, append one bounded signal that points back to a repo-local source.
Do not convert raw logs or build output into durable shared truth.

Current command pattern:

```bash
python3 30_skills/personal/heartbeat_runtime/heartbeat_runtime_v1.py append-signal \
  --brain-root <PERSONALBRAIN_ROOT> \
  --project-id my_app \
  --source-path docs/status.md \
  --summary "Current blocker moved from API auth to deploy config." \
  --origin-ref /absolute/path/to/my_app/docs/status.md \
  --ttl-hours 24
```

## Common External Project Modes

### Retrieve Knowledge Only

Use this when an external repo needs prior conclusions from PersonalBrain.

Do this:

1. attach PersonalBrain
2. read the minimum anchors
3. search the catalog using the project name plus the current problem keywords
4. if the repo is registered, also load the relevant active project snapshot or fresh project signals
5. return only the most relevant pages and explain how they apply

### Reuse A Skill Or Workflow

Use this when the external repo likely benefits from an existing PersonalBrain workflow.

Do this:

1. attach PersonalBrain
2. search for skills, outputs, or topics that match the external repo's current task
3. load only the smallest relevant workflow
4. apply it in the external repo without dragging unrelated pages into context

Prefer reusable `30_skills/` entries and outputs with strong next-use hints.
If no relevant reusable workflow exists, say so plainly and continue with normal reasoning.

### Thin Writeback

Use this when work in the external repo produces something reusable beyond that repo.

Do this:

1. solve the repo-local task in the external repo
2. summarize the durable lesson
3. write back one focused output page only if it is reusable or meaningfully updates project understanding
4. update governance records when a durable page is created or materially changed

Prefer the current durable writeback home:

- `${brain_root}/20_knowledge/outputs/`

Current governance records usually include:

- `${brain_root}/40_governance/catalog.jsonl`
- `${brain_root}/40_governance/changes.jsonl`

Skip writeback when the result is too repo-specific, too noisy, or not worth future reuse.

### Register Repo Or Refresh Signals

Use this when the user wants PersonalBrain to track an external repo over time.

Do this:

1. decide whether ad-hoc handoff is enough or registration is justified
2. if registration is justified, propose the registry row, or update it only when the task explicitly includes that write
3. if the repo is already registered and fresh status is needed, append one project signal from a declared repo-local path
4. keep the resulting snapshot freshness-bound and state-like, not canonical knowledge

Do not silently register every repo you touch.
Do not silently widen `signal_paths` after the repo is already registered.

## Output Modes

### Mode A: Execute With PersonalBrain Attached

Use this when the user wants actual work done.

Do this:

- resolve the root
- read the minimum anchors
- choose the lightest external-project mode if an external repo is involved
- load only the relevant pages
- do the task
- write back only if justified and permitted

### Mode B: Emit Compact Prompt Blocks

Use this when the user wants a reusable prompt snippet for another agent.

Default block:

```text
Use PersonalBrain as shared memory and routing context.
PersonalBrain root: <PERSONALBRAIN_ROOT>

Before doing substantial work, read:
- <PERSONALBRAIN_ROOT>/AGENTS.md
- <PERSONALBRAIN_ROOT>/40_governance/catalog.jsonl

Treat PersonalBrain as durable shared truth.
Do not treat .local, caches, sessions, embeddings, or search indexes as shared truth.
```

External repo retrieval:

```text
Use PersonalBrain as shared memory and routing context.
PersonalBrain root: <PERSONALBRAIN_ROOT>

Before doing substantial work, read:
- <PERSONALBRAIN_ROOT>/AGENTS.md
- <PERSONALBRAIN_ROOT>/40_governance/catalog.jsonl

External project for this task:
- Project: <name>
- Machine: <Mac|Windows|Linux|179>
- Root path: <absolute path>
- Role: <what this project is for>
- Start here: <file/folder/command>

Task:
- Find any existing PersonalBrain knowledge related to this repo's current problem.
- Return only the most relevant pages and explain how they apply here.
```

External repo skill reuse:

```text
Use $attach-personalbrain with <PERSONALBRAIN_ROOT>.

External project:
- Project: <name>
- Machine: <Mac|Windows|Linux|179>
- Root path: <absolute path>
- Role: <what this project is for>
- Start here: <file/folder/command>

Task:
- Search PersonalBrain for reusable skills or outputs related to this repo's current problem.
- Apply only the smallest relevant workflow instead of loading unrelated pages.
```

External repo thin writeback:

```text
Use $attach-personalbrain with <PERSONALBRAIN_ROOT>.

External project:
- Project: <name>
- Machine: <Mac|Windows|Linux|179>
- Root path: <absolute path>
- Role: <what this project is for>
- Start here: <file/folder/command>

Task:
- Inspect the repo, do the work locally, and summarize the durable lesson.
- If the lesson is reusable beyond this repo, write back one focused output page to PersonalBrain and update governance records.
- Do not copy raw logs, caches, or whole project files into PersonalBrain.
```

Register repo or append signal:

```text
Use $attach-personalbrain with <PERSONALBRAIN_ROOT>.

External project:
- Project: <name>
- Machine: <Mac|Windows|Linux|179>
- Root path: <absolute path>
- Role: <what this project is for>
- Start here: <repo-local status file or entry point>

Task:
- Decide whether this repo should stay ad-hoc or be registered into PersonalBrain project awareness.
- If registration is justified, propose the smallest registry entry with narrow repo-local signal paths and a freshness-bound snapshot file.
- If the repo is already registered, append or refresh one bounded project signal from a declared signal path.
- Do not widen project awareness beyond repo-local sources unless the user explicitly asks.
```

Keep prompt blocks short.
Do not expand them into long checklists unless the downstream task is high risk.

## Guardrails

- preserve user intent
- keep the attachment surface minimal
- prefer discovery over hardcoded internal paths
- let the repository contract override this skill when they conflict
- treat project awareness as opt-in and freshness-bound
- use repo-local-first signals for external project tracking
- avoid silent writes to identity, preferences, anti-goals, or working agreement files

## Common Mistakes

- treating this skill as a reason to preload half the vault
- hardcoding today's internal page paths into every prompt
- registering every repo instead of using ad-hoc handoff when enough
- reading undeclared repo files into project awareness
- treating stale project signals as if they were current
- using PersonalBrain as a dump for raw project artifacts
- writing durable notes without updating governance records
- failing to detect that the current workspace is already inside PersonalBrain
- guessing an unrelated root path when there is no explicit root and no local match

## Example Triggers

- `Use $attach-personalbrain with <PERSONALBRAIN_ROOT> for this query task.`
- `Use $attach-personalbrain and connect this external repo to <PERSONALBRAIN_ROOT>.`
- `Use $attach-personalbrain to retrieve prior knowledge for this repo without importing it.`
- `Use $attach-personalbrain to find a reusable PersonalBrain skill for this repo.`
- `Use $attach-personalbrain to write back one reusable lesson after solving this issue.`
- `Use $attach-personalbrain to generate the smallest prompt block for another agent.`
- `Use $attach-personalbrain here; this repo is already my PersonalBrain.`
