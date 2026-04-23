# Codex Skill Routers v2

Last updated: `2026-04-18`

## Summary

- Scope: runtime public-front-door catalog for `$CODEX_HOME/skills`
- Public policy: expose `7` stable router entrypoints and keep specialist leaf skills installed
- Goal: let users remember category routers, not every leaf skill or unstable plugin surface
- Direct-entry rule: if the user explicitly names a precise specialist and the task is clearly one-lane, go direct instead of forcing a router hop
- Lenovo WSL target: mirror the runtime catalog and the skill/plugin payload needed for parity, without syncing sessions, logs, or state databases

## Router Index

| Router | Label | Public entry | Routed skills | Source |
| --- | --- | --- | ---: | --- |
| `research-router` | 科研总入口 | `research-router` | 10 | `local-skills` |
| `delivery-router` | 交付与产品总入口 | `delivery-router` | 10 | `local-skills` |
| `architect-router` | 架构总入口 | `architect-router` | 8 | `mixed-local+plugin-cache` |
| `build-router` | 构建设计总入口 | `build-router` | 22 | `mixed-system+plugin-cache` |
| `execution-router` | 执行编排总入口 | `execution-router` | 3 | `local-skills` |
| `knowledge-router` | 知识与上下文总入口 | `knowledge-router` | 3 | `mixed-local+system` |
| `skillops-router` | 技能运维总入口 | `skillops-router` | 6 | `mixed-local+system` |

## Routers

### `research-router`

- Label: 科研总入口
- Use first: `research-router`
- Role: 统一路由 AI 研究链路，在读论文、想法澄清、新颖性压测、实验设计、结果分析、写作、展示与网页材料抓取之间选最合适的下一步。
- Routed skills: `research-flow-navigator`, `research-paper-reading-compass`, `research-supplement-digestion`, `web-page-capture`, `research-idea-clarifier`, `research-novelty-audit`, `research-experiment-design-planner`, `research-training-and-ablation-loop`, `research-paper-production-pipeline`, `research-slides-and-poster-studio`
- Direct-first when explicit: `research-paper-reading-compass`, `research-experiment-design-planner`, `research-novelty-audit`, `web-page-capture`

### `delivery-router`

- Label: 交付与产品总入口
- Use first: `delivery-router`
- Role: 在 discovery、proposal generation、requirements、critique、test planning、verification 与端到端交付 owner 之间分流；广义交付工作优先交给最小可用 lane，而不是默认全走一个 manager。
- Routed skills: `delivery-conductor`, `brainstorming`, `proposal-synthesis`, `business-analyst`, `product-manager`, `product-requirements`, `proposal-critique-refine`, `test-cases`, `verification-before-completion`, `bmad-orchestrator`
- Direct-first when explicit: `delivery-conductor`, `proposal-synthesis`, `product-manager`, `product-requirements`, `proposal-critique-refine`, `test-cases`, `verification-before-completion`

### `architect-router`

- Label: 架构总入口
- Use first: `architect-router`
- Role: 给架构类工作提供稳定前门，在 broad architect synthesis 与 narrow specialist lanes 之间做选择。
- Routed skills: `architect`, `architecture-governance`, `codebase-architecture`, `spec-driven-architecture`, `ddd-clean-architecture`, `agent-systems-architecture`, `architecture-docs-review`, `architecture-workbench`
- Direct-first when explicit: `architect`, `architecture-governance`, `codebase-architecture`, `spec-driven-architecture`, `ddd-clean-architecture`, `agent-systems-architecture`, `architecture-docs-review`

### `build-router`

- Label: 构建设计总入口
- Use first: `build-router`
- Role: 处理 UI、GitHub 工作流、部署、Figma/Canva 工具链与 bitmap 视觉资产生成，让“做出来并上线/出图/进 GitHub”有稳定前门。
- Routed skills: `frontend-skill`, `deploy-to-vercel`, `github`, `gh-address-comments`, `gh-fix-ci`, `imagegen`, `react-best-practices`, `shadcn-best-practices`, `stripe-best-practices`, `supabase-best-practices`, `web-design-guidelines`, `canva-branded-presentation`, `canva-resize-for-all-social-media`, `canva-translate-design`, `figma-code-connect-components`, `figma-create-design-system-rules`, `figma-create-new-file`, `figma-generate-design`, `figma-generate-library`, `figma-implement-design`, `figma-use`, `yeet`
- Direct-first when explicit: `github`, `gh-address-comments`, `gh-fix-ci`, `deploy-to-vercel`, `imagegen`, exact Figma/Canva specialists

### `execution-router`

- Label: 执行编排总入口
- Use first: `execution-router`
- Role: 决定任务应留在当前线程本地执行，还是走 Lenovo/179 远端 SSH 计算、显式并行代理、或子代理执行计划；它解决的是执行拓扑，不是内容领域。
- Routed skills: `conductor-remote-long-task`, `dispatching-parallel-agents`, `subagent-driven-development`
- Direct-first when explicit: `conductor-remote-long-task`, `dispatching-parallel-agents`, `subagent-driven-development`
- Policy note: router may explicitly decide that no specialized execution lane is needed and the work should stay local
- Policy note: `dispatching-parallel-agents` and `subagent-driven-development` require explicit delegation intent and must still respect current agent-policy constraints.

### `knowledge-router`

- Label: 知识与上下文总入口
- Use first: `knowledge-router`
- Role: 在 PersonalBrain 挂接、OpenAI 官方文档检索、prompt 优化与“无需额外上下文层”之间做最薄的上下文决策。
- Routed skills: `attach-personalbrain`, `openai-docs`, `thinking-lenses`
- Direct-first when explicit: `attach-personalbrain`, `openai-docs`, `thinking-lenses`
- Policy note: router may explicitly decide that no extra knowledge layer is needed

### `skillops-router`

- Label: 技能运维总入口
- Use first: `skillops-router`
- Role: 处理技能发现、安装、来源材料蒸馏成 skill、创建/更新、插件脚手架与使用复盘，并在可能时先做“扩现有 skill 还是新建 skill”的 intake 判断。
- Routed skills: `skill-finder`, `skill-installer`, `source-to-skill`, `skill-creator`, `plugin-creator`, `skill-skill-usage-close-loop`
- Direct-first when explicit: `skill-finder`, `skill-installer`, `source-to-skill`, `skill-creator`, `plugin-creator`, `skill-skill-usage-close-loop`
- Optional workspace lane: use a repo-local intake router first when the current workspace provides one
- Packaging rule: prefer plain skills over plugins unless distribution, namespacing, or marketplace packaging is the actual requirement

## Direct-Entry Policy

- Route first when the user speaks in outcomes, categories, or uncertainty.
- Go direct when the user names an exact skill or the task is cleanly one-lane.
- A router is allowed to decide that no specialized lane is needed.

## Sync Policy

- Sync to the target Codex install: `$CODEX_HOME/skills/` including this file and `packages.catalog.json`.
- Sync cached plugins for parity when the remote side does not already have the same plugin surface.
- Do not sync volatile runtime state such as `sessions/`, `logs_*.sqlite`, `history.jsonl`, or `state_*.sqlite`.
