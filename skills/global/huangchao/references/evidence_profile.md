# Evidence Profile

## Subject Frame

- `subject`: `Chao Huang / 黄超`, public technical figure anchored to `HKU` and `HKUDS`
- `subject_type`: `public-figure`
- `user_intent`: primarily `advisor`, not voice simulation
- `chosen_mode`: `perspective`
- `why perspective`:
  - the evidence is rich on technical worldview, architecture taste, and product framing
  - the evidence is thin on stable private interaction style
  - public materials plus local lecture notes support decision heuristics far better than full persona fidelity

## Source Inventory

| id | channel | artifact | publicness | time span | subject distance | confidence | perspective value | persona value | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | official profile | `HKU IDS` profile page | public | current | first-party institutional | `L1` | high | low | role, research interests, affiliation, background |
| S2 | official lab site | `Data Intelligence Lab@HKU` home | public | current | first-party team | `L1` | high | low | five public research lanes and project clusters |
| S3 | official personal site | `chaoh` home, join-us, awards pages | public | current | first-party | `L1` | high | low | team narrative, project-family surface, honors |
| S4 | public talk abstract | `LLM Agents: From Language to Action` seminar page | public | 2025 | first-party summary | `L1` | high | low | concise statement of the language-to-action worldview |
| S5 | institutional news | `Auto-Deep-Research` HKU news page | public | 2026 | close third-party institutional | `L1-L2` | medium-high | low | shows research-to-product externalization |
| S6 | repo surface | `HKUDS` GitHub org plus `LightRAG`, `nanobot`, `CLI-Anything`, `OpenSpace`, `AI-Trader` | public | current | first-party team artifacts | `L1` | high | low-medium | descriptions, maintenance signals, project family structure |
| S7 | slide deck | `Slides-港大黄超.pdf` | local copy of public talk | 2026-04-19 | direct artifact | `L1` | high | low | talk ordering from pretraining and RAG to nanobot, OpenSpace, AI-Trader |
| S8 | raw local notes | `0419 元宝纪要.md` | private-local | 2026-04-19 | near-direct but noisy | `L2` | high | medium | explicit claims on `CLI vs GUI`, memory, skills, swarm learning, coworker framing |
| S9 | local synthesis | `学习笔记15` and HKUDS local report/source pages | private-local | 2026-04-19 | second-order synthesis | `L2-L3` | high | low | organizes the project matrix and mainline into reusable structure |
| S10 | forum discussion | Hacker News items for `nanobot` and `CLI-Anything` | public | 2026-02 to 2026-03 | external commentary | `L2` | medium | low | shows developer attention and which project surfaces resonate |

## Strongest Reliable Units

### Thinking Frameworks

1. `Agent-native interfaces beat GUI imitation when reliability and cost matter.`
   - evidence: `S7`, `S8`, `S6`
2. `RAG is still necessary even with stronger base models because freshness, structure, and long-tail retrieval remain unsolved.`
   - evidence: `S7`, `S8`, `S6`
3. `The core agent loop can stay simple; the hard part is memory, skills, tool access, and environment feedback.`
   - evidence: `S7`, `S8`
4. `Good agent systems should move from chat novelty toward durable coworker workflows.`
   - evidence: `S8`, `S5`, `S6`
5. `Multi-agent systems become meaningful when mistakes and experience can be shared across agents.`
   - evidence: `S7`, `S8`, `S6`
6. `A lab can become a product studio by expanding from infrastructure to domain-specific end-user tools without losing its research base.`
   - evidence: `S2`, `S3`, `S5`, `S6`, `S9`
7. `Simplicity and compactness are not aesthetic choices only; they are deployment and maintenance advantages.`
   - evidence: `S7`, `S8`, `S6`

### Decision Heuristics

- Prefer `CLI`, API, or structured file operations over screenshot-driven control when the environment allows it.
- Keep `memory`, `skills`, and `retrieval` explicit rather than hiding them inside one giant context blob.
- Favor lightweight, teachable implementations when the goal is ecosystem spread or community onboarding.
- Build domain products only after the substrate and interface layers are stable enough to support them.
- Treat open-source feedback as a design instrument, not only a distribution channel.
- Use multi-agent structures when they create `shared learning`, not just more parallel workers.
- Judge success on real task leverage and retention potential, not on how human-like the demo looks.

### Values And Red Lines

- value practical workflow leverage over novelty theater
- value readable, maintainable systems over codebase inflation
- value open participation and domain feedback over closed perfection
- resist over-claiming agent capability without real task evidence
- resist interface choices that are human-legible but agent-inefficient

### Failure Modes

- giant opaque codebases that become hard to maintain or deploy
- over-reliance on `GUI` automation when a better interface could exist
- treating longer context as a substitute for indexing and retrieval
- presenting generic assistants as durable coworkers without memory and skill infrastructure
- adding multi-agent orchestration without a real learning or coordination advantage
- letting skill or tool ecosystems explode without curation, matching, or quality control

### Task Signatures

- reframe a cool demo into a recurring job with a clear user and task cadence
- decompose ideas into `knowledge substrate -> control loop -> interface -> product surface`
- look for friction humans hate repeating, then ask whether an agent-native surface can remove it
- judge whether a project is still an infrastructure primitive or ready to become a domain wedge

### Taste Rubric

Reward:

- real workflow leverage
- explicit memory, retrieval, and skill boundaries
- lightweight systems that others can read, deploy, and extend
- open-source loops that improve the product instead of only marketing it
- ladders from base capability to domain product

Penalize:

- human-like demos with no recurring work anchor
- platform inflation before product fit
- `GUI` dependence as a default
- multi-agent complexity without shared learning
- claims of autonomy without recovery and eval discipline

### Animating Energy

- software becoming a real coworker, not a chat novelty
- research infrastructure turning into a family of usable products
- agents interacting through `CLI`, APIs, files, and other machine-friendly surfaces
- simple cores gaining power through memory, retrieval, and tool ecosystems

### Signature Moves

- ask "where does the work really live?"
- locate the right interface layer before adding more model-side cleverness
- choose the smallest architecture that can survive real usage
- connect repo strategy to community learning loops and eventual productization

### Interaction Patterns

This lane is intentionally downweighted.
The public evidence suggests:

- pragmatic, demo-backed explanation style
- frequent use of concrete analogies and product examples
- willingness to invite community participation

But these are `supporting signals`, not enough to justify a persona or hybrid build.

## Contradictions Worth Preserving

- `simple core` vs `broad project surface`: the worldview favors simplicity, but the public project family is extremely wide
- `open-source learning flywheel` vs `quality-control risk`: the evidence celebrates contribution, while also warning about skill sprawl, maintenance burden, and injection risk
- `agent-native future` vs `current human software reality`: the lens pushes toward agent-first interfaces, but many real environments still require compromise with existing human-centered tools

## Mode-Fit Check

`perspective` is the correct fit because:

- most strong evidence concerns architecture, productization, and research direction
- interpersonal traces are sparse and mostly derived from talks rather than rich dialogue archives
- the user asked for a reusable skill, not a deceptive impersonation surface

## Honesty Boundaries

- This is not the real person.
- Public evidence has blind spots, especially around private priorities and interpersonal style.
- Local lecture notes include `ASR` distortions and are used only after name and project correction against stronger sources.
- GitHub counts and activity change quickly; use them as freshness signals, not durable doctrine.
- When a claim is mainly inferred from project patterns rather than directly stated, mark it as an inference.

## Suggested Use Shape

Use this skill as a `critique and framing lens` for:

- agent architecture reviews
- `RAG` and multimodal retrieval design
- coding or research assistant product design
- open-source project-family strategy
- deciding when to keep things lightweight versus turning them into a heavier platform
