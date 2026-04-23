---
name: conductor-remote-long-task
description: Coordinate recoverable remote SSH compute from any local project by using the central Conductor runtime at <PERSONALBRAIN_ROOT>/.local/conductor, selecting a verified SSH route for either a workstation or a shared compute server, dispatching direct remote commands or scripts, and closing the job with local review. Use when Codex should run tests, builds, data processing, or other compute remotely over SSH instead of delegating to a second remote AI runtime, especially when the work may outlive the current thread and needs receipts, logs, and recoverable closeout.
---

# Conductor Remote Long Task

Use this skill as a thin Conductor wrapper around remote SSH compute.
Keep durable control state local and keep remote execution ordinary shell compute.

Read these bundled resources only when needed:

- `scripts/select_ssh_route.py` to probe `workstation` or `shared-server` and return the best SSH alias plus remote shell command.
- `references/command-patterns.md` to copy exact helper commands, dispatch patterns, and close-out shapes.

## Installed Defaults

Use these fixed paths and values unless the user explicitly overrides them:

- PersonalBrain root: `<PERSONALBRAIN_ROOT>`
- helper path: `<PERSONALBRAIN_ROOT>/30_skills/personal/conductor_runtime/conductor_runtime_v1.py`
- runtime root: `<PERSONALBRAIN_ROOT>/.local/conductor`
- supported target machines:
  - `workstation`
  - `shared-server`
- preferred workstation Linux route order:
  - `workstation-linux-primary`
  - `workstation-linux-via-host`
  - `workstation-linux-campus`
- preferred shared-server route order:
  - `shared-server-primary`
  - `shared-server-via-linux`
  - `shared-server-via-workstation`

Always call the helper with:

- `--runtime-root <PERSONALBRAIN_ROOT>/.local/conductor`

Never rely on a project-local relative `.local/conductor`.

## Public-Safe Environment Notes

This public copy keeps route names, toolchain paths, and machine inventory generic on purpose.
Keep the workflow shape here, then fill in the real aliases, paths, and package/runtime details only in your private install.

Recommended pattern:

- keep one primary Linux route for workstation compute
- keep one fallback Linux bridge route through the workstation host shell
- keep one Windows-native route for toolchains that must stay in the Windows shell
- keep one primary shared-server route and one or two documented fallback routes
- store CUDA, compiler, and virtual-environment specifics in private machine notes, not in the public skill body
- if remote shells need extra environment setup, source one stable shell-init file instead of repeating many exports in every command
- if Windows-native package builds are sensitive to proxies or codepage issues, clear those environment variables in a private wrapper before networked build steps

## Use This Skill For

- remote tests, builds, data processing, or material-processing tasks on a workstation or shared compute server
- tasks that need a receipt, recoverable checkpoints, and local close-out
- tasks started from any local project directory but coordinated by the central Conductor runtime

Do not use this skill for:

- whole-machine administration
- interactive long-lived remote sessions
- remote LLM orchestration or a second remote AI runtime
- broad multi-machine fanout where several targets should run in parallel
- short local tasks that do not need remote orchestration

## Required Intent Fields

Resolve these fields from the user's request before dispatch:

- `target_machine`
- `runtime_family`
- `workspace_or_root`
- `task_class`
- `objective`
- `success_criteria`

Default rules:

- infer `target_machine=workstation` when the request does not name a machine
- allow only `workstation` or `shared-server`
- default `runtime_family=linux` for workstation compute unless the task clearly needs the Windows shell
- force `runtime_family=linux` for `shared-server`
- infer `task_class=research` only when the request is clearly about collecting, organizing, or summarizing material
- otherwise use `task_class=project`
- ask a minimal follow-up only when `workspace_or_root` or `success_criteria` is too ambiguous to run safely

## Fixed I/O Contract

Local input contract:

- `target_machine`
- `runtime_family`
- `workspace_or_root`
- `task_class`
- `objective`
- `success_criteria`

Always resolve missing fields from natural language first.
Ask the smallest possible follow-up only when a safe run still cannot be inferred.

Remote evidence contract:

- a remote exit status or detached-session marker
- remote absolute paths for output files, logs, or result folders when those paths matter later
- a local dispatch log under `.local/conductor/artifacts/<job_id>/`

Local close-out contract:

- `complete`
- `gate`
- `review`

Use the local dispatch log as fallback evidence when the remote task itself does not emit a richer artifact set.

## Workflow

### 1. Create the central receipt

Run:

- `submit`

Then keep the returned `job_id`.

### 2. Select the SSH route

Run `python3 scripts/select_ssh_route.py --target-machine <workstation|shared-server> --runtime <linux|windows>`.

Carry forward these fields from the result:

- `selected_alias`
- `remote_shell_command`
- `route_family`

If no route succeeds:

- treat it as a transport failure
- write a local checkpoint with the failed aliases
- stop before mutating remote state further

### 3. Reserve a job-local tool path when a script is clearer than one command

Run:

- `tool-path --job-id <job_id> --tool-name run_remote_compute.sh`

Write task-specific scripts only inside:

- `<PERSONALBRAIN_ROOT>/.local/conductor/artifacts/<job_id>/tools/`

Prefer:

- `dispatch` for a short one-shot command
- `dispatch-script` for multi-line shell logic, environment setup, or result capture

Do not place task-specific executors in the skill folder.

### 4. Execute direct remote compute

Run:

- `dispatch --job-id <job_id> --ssh-target <selected_alias> --command "<remote command>"`
- or `dispatch-script --job-id <job_id> --local-script <job_local_script_path> --ssh-target <selected_alias> --remote-shell-command "<remote shell>"`

Use these shell rules:

- workstation Linux-path tasks:
  - prefer `workstation-linux-primary` with `bash -s`
  - otherwise bridge through `wsl -e bash -s`
- workstation Windows-shell tasks:
  - use `powershell -NoProfile -NonInteractive -Command -`
- shared-server tasks:
  - use `bash -s`

For workstation Linux CUDA/Python tasks, prefer the primary direct route and a preconfigured shell init file so routine jobs do not need to repeat environment exports inline.

For workstation Windows-native CUDA/Python builds, prefer a `cmd /c` wrapper that:

- calls the local Visual Studio build-tools bootstrap first when native extensions require MSVC
- clears stale proxy variables before networked package installs
- sets `PYTHONUTF8=1` when source installs are sensitive to README or metadata encoding
- exports `CUDA_PATH` from your private machine config before invoking GPU build tools
- uses one documented GPU-capable Python environment from your private machine notes when the task matches a previously verified workflow

Do not launch `codex exec`, supervisor wrappers, or a remote agent as part of this skill.

If the task truly needs to outlive the current thread, use ordinary remote primitives such as `tmux`, `nohup`, or a job-local shell wrapper and then poll with short SSH probes. Keep that detached mode exceptional.

### 5. Close the job locally

After the remote command or script finishes:

1. call `complete`
2. call `gate`
3. call `review`

Decision rules:

- if the remote command returns `0`, prefer `review --decision done`
- if the remote command returns nonzero but the failure is informative and final, prefer `review --decision blocked`
- if transport fails or the detached job disappears without usable evidence, prefer `review --decision needs_followup`

Include in `evidence_pointers`:

- the local dispatch log
- any remote output path that the user may need next
- any detached-session marker such as `tmux:<session>` or `pid:<pid>`

## Guardrails

- keep the runtime centralized under `<PERSONALBRAIN_ROOT>/.local/conductor`
- treat the skill as a protocol adapter, not a second execution engine
- prefer direct SSH compute over remote agent orchestration
- prefer `workstation-linux-primary` for workstation Linux-path work when available
- if `workstation-linux-primary` is down, fall back to `workstation-linux-via-host` or `workstation-linux-campus` plus `wsl -e bash -s`
- prefer direct `shared-server-primary` for shared compute, then `shared-server-via-linux`, then `shared-server-via-workstation`
- treat host-key verification failures as route failures; choose another verified alias instead of mutating SSH trust mid-task
- treat the shared server as compute only, not as a durable knowledge home
- do not reopen a closed receipt
- respect same-job locking; if a helper command returns `job_lock_conflict`, wait and retry the next polling cycle instead of forcing a write
- if a helper command returns `protocol_conflict` for a closed receipt, stop mutating that job
- if SSH transport is down, record the transport failure and retry only after a route probe succeeds again

## Example Triggers

- `Use $conductor-remote-long-task to run this test suite on my workstation over SSH and close with evidence.`
- `Use $conductor-remote-long-task to run shared compute on my server and choose the best reachable SSH path.`
- `Use $conductor-remote-long-task from this project and keep the central Conductor runtime.`
