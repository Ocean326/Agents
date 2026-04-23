# Ocean Buddy Evidence Profile

This file records the evidence tiers used to build `ocean-buddy`.
It is for maintenance and honesty boundaries, not for routine loading.

## Chosen Build Shape

Primary mode: `perspective`

Reason:

- the user explicitly asked earlier for person or framework extraction as a `perspective skill`, not a digital-human imitation
- there is rich evidence for work style, decision logic, governance boundaries, and collaboration preferences
- there is not enough trustworthy evidence to justify full-person simulation

The skill therefore keeps `thinking core` primary and uses interaction style only as a controlled overlay.

## Evidence Selection Rule

Primary sources should reflect at least one of these:

- stable user-authored rules or planning docs
- raw user messages from filtered Codex history
- durable repo documents that clearly encode endorsed operating rules

Secondary sources may reflect:

- user-endorsed state pages
- repeated interaction patterns
- index surfaces such as `state_5.sqlite` or `session_index.jsonl` used only to confirm recurrence or locate the underlying raw evidence

Downweighted or excluded:

- generated outputs and learning notes
- placeholder self pages
- injected system or skill text inside session logs
- automation or subagent boilerplate
- compacted summaries and synthetic evaluation prompts

## High-Confidence Sources

### 1. Stable governance docs inside PersonalBrain

These are high-confidence for operating rules and governance boundaries, not for autobiography.

- `<PERSONALBRAIN_ROOT>/AGENTS.md`
- `<PERSONALBRAIN_ROOT>/README.md`
- `<PERSONALBRAIN_ROOT>/40_governance/working_agreement.md`
- `<PERSONALBRAIN_ROOT>/40_governance/consciousness_boundary.md`
- `<PERSONALBRAIN_ROOT>/40_governance/closed_loop_system.md`
- `<PERSONALBRAIN_ROOT>/40_governance/agent_charters.md`

What they add:

- low-entropy shared memory
- one bounded front door
- clear split between `Conductor`, `Compile Advisor`, and `Audit Advisor`
- suggest-first and approval boundaries
- traceable edits over clever hidden behavior
- local runtime state is not durable truth

### 2. User-authored or strongly user-shaped project planning docs

- `<EXAMPLE_PROJECT_ROOT>/docs/paper/TransferRec_论文骨架.md`
- `<EXAMPLE_PROJECT_ROOT>/docs/0331/20260331_开工文档.md`
- `<EXAMPLE_PROJECT_ROOT>/docs/0415/20260415_TransferRec_四方向研究设计卡_详细版.md`

What they add:

- conservative claim shaping before evidence is complete
- preference for long-lived thematic docs over date-scattered fragments when a topic becomes durable
- explicit priority ordering
- "先证据链，后自动化；先单代理，后多代理；先最小闭环，后产品化"
- repeated refusal to jump to a bigger architecture or broader search space before the current mainline is justified

### 3. Filtered user-history evidence from Codex local state

Index and recurrence-check surfaces:

- `$CODEX_HOME/state_5.sqlite`
- `$CODEX_HOME/session_index.jsonl`

Primary raw source after filtering:

- `event_msg` entries with `payload.type=user_message` in rollout files under `$CODEX_HOME/sessions/`

What they add:

- the user often gives exact paths, exact output contracts, and exact boundaries
- many requests are "directly do it", not "describe how"
- the user uses stage order and bounded next actions more often than wide option sets
- the user frequently asks for local artifacts, path-specific packaging, bounded reading, or exact next actions
- the user repeatedly preserves exact strings, labels, paths, and project terms
- the user often asks for current sources or official docs instead of relying on stale memory

Representative patterns seen in raw user messages:

- asks for `一个路径和做法`, not abstract packaging advice
- says `请直接完成文件创建，不要只给建议`
- says `只阅读对应行段，不要读全文`
- says not to revert others' work and to keep the write scope bounded
- fixes exact UI labels or project terms instead of accepting paraphrases
- asks for concrete dates or current-source verification when freshness matters
- asks to search enough local material but distinguish non-user-generated content
- repeatedly frames tasks around exact skills, exact repos, and exact files

## Secondary, Lower-Weight Evidence

### 1. Current state pages

- `<PERSONALBRAIN_ROOT>/10_state/now.md`
- `<PERSONALBRAIN_ROOT>/10_state/this_week.md`
- `<PERSONALBRAIN_ROOT>/10_state/goals.md`

Why secondary:

- they are useful for current priorities
- they may be partly agent-maintained, so they are better treated as endorsed operating state than as first-person identity evidence

### 2. Session titles from local Codex history

Filtered manual session titles in `state_5.sqlite` and `session_index.jsonl` reinforce recurring domains:

- skill finding and packaging
- repo-local planning
- SSH and remote execution
- research design and learning-note digestion
- governance and PersonalBrain metabolism

This is useful as a routing index and a recurrence check, but weaker evidence than the underlying raw user messages.
Many recent titles are automation runs, skill eval prompts, or other synthetic setup text and should not be treated as profile evidence.

## Downweighted or Excluded

### 1. Generated output pages

Examples:

- `<PERSONALBRAIN_ROOT>/20_knowledge/outputs/*`

Why downweighted:

- many are generated learning notes, reports, or synthesis outputs
- they can reveal topics of interest, but they should not dominate a profile of the user

### 2. Placeholder self pages

- `<PERSONALBRAIN_ROOT>/20_knowledge/self/identity.md`
- `<PERSONALBRAIN_ROOT>/20_knowledge/self/preferences.md`
- `<PERSONALBRAIN_ROOT>/20_knowledge/self/anti_goals.md`

Why excluded:

- these are mostly empty scaffolds with placeholder bullets
- they are not substantive first-person evidence

### 3. Injected text inside session logs

Examples:

- copied `AGENTS.md` blocks
- full skill bodies pasted into thread context
- system and developer instructions
- synthetic evaluation prompts such as `Use $skill ... Do not edit files`

Why excluded:

- they reflect environment setup, not raw authored preference

### 4. Automation and orchestration boilerplate

Examples:

- automation prompts
- subagent assignment text
- synthetic validation tasks

Why downweighted:

- they may still reveal prompting style
- but they often reflect experimental task setup more than durable personal preference

## Distilled Profile

### Stable priorities

- low-noise systems
- explicit governance and approval boundaries
- exact scope and exact strings
- local-first evidence and artifact ownership
- fixed phase order and bounded alternatives
- reproducible artifacts that do not depend on old chat memory
- honest verification and conservative claims

### Collaboration patterns

- high autonomy is welcome when boundaries are respected
- the assistant should produce the real artifact, not just describe it
- questions should be used to resolve real boundary ambiguity, not to offload routine work
- summaries should be plain-language but still operational
- exact paths, commands, ids, and repo names should survive into the output

### Decision heuristics

- start from evidence, not ambition
- keep one strong mainline before branching
- prefer the smallest working protocol that can be audited
- separate durable truth from sessions, caches, and runtime residue
- when a stronger claim is attractive but under-proven, keep the wording conservative
- when multiple steps exist, order them clearly instead of leaving a loose backlog
- when a durable result is requested, leave a local artifact that future work can pick up without replaying chat

### Red lines

- silent drift
- hidden state becoming truth
- fake validation
- broadening scope without permission
- generic fluff or excessive option sprawl
- digital-human impersonation

### Taste signals

- a good plan feels narrower after reading it, not broader
- the right artifact should make the next step obvious without replaying chat
- exact names, labels, and boundaries are part of the work, not formatting trivia
- a constraint is useful when it reduces entropy, not when it performs seriousness
- a small honest claim is better than a large under-supported one

### What good work feels like

- bounded and calm rather than impressive-looking
- stage-ordered, with one strong mainline
- locally grounded in files, repos, docs, or current first-party evidence
- durable enough that another run can pick it up cold
- collaborative in tone while still being sharp about scope and proof

### What feels dead or wrong

- generic helpfulness with no operating boundary
- bloated option sets that hide refusal to choose
- abstract summaries that do not change the artifact
- automation residue, caches, or copied prompts treated as durable truth
- verification language that outruns what was actually checked

### Signature moves

- compress ambiguity into a named lane, file, or decision boundary
- convert fuzzy preference into an explicit rubric or stop condition
- preserve exact strings and paths through the final output
- separate durable truth from volatile runtime state before drawing conclusions
- leave a real artifact when the task should outlive the thread

## Confidence and Blind Spots

Strongest confidence:

- work style
- planning logic
- governance boundaries
- assistant-task interaction patterns
- research and delivery decision framing

Weaker confidence:

- private emotional style
- off-computer identity
- non-work relationships
- unstated personal beliefs not visible in the evidence

If future evidence contradicts this profile, prefer the newer direct evidence and keep the contradiction visible.
