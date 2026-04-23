---
name: execution-router
description: 面向执行编排的总入口路由器。用于判断当前任务是否应该保持在本线程本地执行，还是需要远端 SSH 计算、显式并行代理、或按计划拆给实现子代理；当用户关心“怎么执行这项工作”而不是“这项工作属于哪个内容领域”时优先使用。
---

# Execution Router

Use this router for execution topology, not task content.
Its most important decision is often that no special execution lane is needed.

This router should answer:

- keep work local in the current session
- send recoverable remote SSH compute to Lenovo or `179`
- split independent tasks for explicit parallel work
- execute a clear implementation plan via explicit subagent workflow

## Use This Router For

- deciding whether a task should remain local or move onto remote SSH compute
- explicit requests for delegation, subagents, parallel work, or long-task orchestration
- tasks where execution strategy is the real blocker

## Do Not Use This Router For

- choosing the research, delivery, architecture, or build domain lane
- disguising content uncertainty as an execution problem
- automatic subagent use when policy or user intent does not allow it

## Routing Table

1. `conductor-remote-long-task`
   Use for work that should run remotely over SSH on Lenovo or `179` with receipts, route selection, and recoverable closeout.

2. `dispatching-parallel-agents`
   Use when the user explicitly wants parallel agent work and there are 2 or more independent domains that can be explored without shared state.

3. `subagent-driven-development`
   Use when the user explicitly wants delegated implementation work, a clear plan already exists, tasks are independent enough, and the work should stay inside the current session.

## Decision Rules

1. Start by deciding whether specialized execution is warranted at all.
2. If the best answer is to keep working locally in the current thread, say that explicitly instead of inventing a fake execution lane.
3. Only route to subagent skills when the user explicitly asks for delegation, subagents, or parallel agent work and the platform policy allows it.
4. Prefer `conductor-remote-long-task` when the work should move onto remote SSH compute and recoverability matters.
5. Prefer `dispatching-parallel-agents` when the domains are independent investigations.
6. Prefer `subagent-driven-development` when a concrete implementation plan already exists and the work can be split into bounded tasks.

## Direct-Entry Exceptions

Skip this router and go direct when:

- the user explicitly names `conductor-remote-long-task`
- the user explicitly asks for parallel agents and the problem split is already clear
- the user already has a detailed implementation plan and explicitly wants subagent-driven execution

## Output Contract

Always return:

- whether a specialized execution lane is justified
- chosen execution lane, or the decision to stay local
- the policy or practical reason behind the choice
- the next concrete execution step

## Guardrails

- do not turn every hard task into a remote or multi-agent task
- do not route to subagent skills without explicit delegation intent
- do not confuse execution strategy with domain routing
- if the best answer is “keep going locally,” say that plainly

## Example Triggers

- `Use $execution-router to decide whether this should stay local, go remote, or be delegated.`
- `使用 $execution-router 看看这个任务该本地做、发到 Lenovo/179 远端 SSH，还是拆成并行代理。`
- `Use $execution-router to choose the right execution pattern for this already-scoped plan.`
