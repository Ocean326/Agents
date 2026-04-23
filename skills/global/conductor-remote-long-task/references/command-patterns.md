# Command Patterns

Use this reference when you need exact shell shapes for direct SSH compute and Conductor close-out.

## Fixed Local Paths

```bash
HELPER="<PERSONALBRAIN_ROOT>/30_skills/personal/conductor_runtime/conductor_runtime_v1.py"
RUNTIME="<PERSONALBRAIN_ROOT>/.local/conductor"
ROUTE_SELECTOR="$CODEX_HOME/skills/conductor-remote-long-task/scripts/select_ssh_route.py"
```

## Select The SSH Route

Probe the current machine against the preferred alias order and export the winning route:

```bash
eval "$(
  python3 "$ROUTE_SELECTOR" \
    --target-machine workstation \
    --runtime linux \
    --format env
)"
```

Typical results:

- workstation Linux compute:
  - `SELECTED_SSH_TARGET=workstation-linux-primary`
  - `SELECTED_REMOTE_SHELL_COMMAND='bash -s'`
- workstation fallback through host shell:
  - `SELECTED_SSH_TARGET=workstation-linux-via-host`
  - `SELECTED_REMOTE_SHELL_COMMAND='wsl -e bash -s'`
- shared-server direct compute:
  - `SELECTED_SSH_TARGET=shared-server-primary`
  - `SELECTED_REMOTE_SHELL_COMMAND='bash -s'`

If the selector exits nonzero, treat that as a transport failure and stop before dispatch.

## Local Helper Commands

Create the receipt:

```bash
python3 "$HELPER" --runtime-root "$RUNTIME" submit \
  --prompt "<natural-language task>"
```

Reserve the local script path when a multi-line remote script is clearer than a one-shot command:

```bash
python3 "$HELPER" --runtime-root "$RUNTIME" tool-path \
  --job-id "<job_id>" \
  --tool-name "run_remote_compute.sh"
```

## One-Shot Command Pattern

Use `dispatch` for a short command that is easy to quote:

```bash
python3 "$HELPER" --runtime-root "$RUNTIME" dispatch \
  --job-id "<job_id>" \
  --ssh-target "$SELECTED_SSH_TARGET" \
  --command "cd <remote_workspace> && <remote_command>"
```

Prefer `dispatch-script` once the remote shell logic spans several lines.

## Remote Script Pattern

Write a task-specific script under the job-local tools directory and replace the placeholders before dispatch:

```bash
#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="<remote_workspace>"
RUN_DIR="${WORKSPACE}/.codex-remote/<job_id>"

mkdir -p "$RUN_DIR"
cd "$WORKSPACE"

echo "$(date -Is) start" | tee "$RUN_DIR/status.log"

<remote_command_1>
<remote_command_2>

echo "$(date -Is) done" | tee -a "$RUN_DIR/status.log"
```

Dispatch it with the selected remote shell:

```bash
python3 "$HELPER" --runtime-root "$RUNTIME" dispatch-script \
  --job-id "<job_id>" \
  --local-script "<PERSONALBRAIN_ROOT>/.local/conductor/artifacts/<job_id>/tools/run_remote_compute.sh" \
  --ssh-target "$SELECTED_SSH_TARGET" \
  --remote-shell-command "$SELECTED_REMOTE_SHELL_COMMAND"
```

Shell choices:

- workstation Linux via `workstation-linux-primary`:
  - `bash -s`
- workstation Linux via host shell:
  - `wsl -e bash -s`
- workstation Windows-native tasks:
  - `powershell -NoProfile -NonInteractive -Command -`
- shared-server:
  - `bash -s`

## Detached Compute Pattern

Use detached mode only when the user explicitly needs work that may outlive the current thread.

Example tmux launch from a Linux shell target:

```bash
#!/usr/bin/env bash
set -euo pipefail

SESSION="codex_<job_id>"
WORKSPACE="<remote_workspace>"
RUN_DIR="${WORKSPACE}/.codex-remote/<job_id>"

mkdir -p "$RUN_DIR"

tmux new-session -d -s "$SESSION" "cd '$WORKSPACE' && <long_command> > '$RUN_DIR/run.log' 2>&1; echo \$? > '$RUN_DIR/exit_code.txt'"

echo "__REMOTE_SESSION__:$SESSION"
echo "__REMOTE_RUN_DIR__:$RUN_DIR"
```

Poll it with short SSH probes:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=15 "$SELECTED_SSH_TARGET" "$SELECTED_REMOTE_SHELL_COMMAND" <<'EOF'
set -euo pipefail
RUN_DIR="<remote_run_dir>"
SESSION="<remote_tmux_session>"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "__RUNNING__:$SESSION"
  exit 0
fi

if [[ -f "${RUN_DIR}/exit_code.txt" ]]; then
  echo "__EXIT_CODE__"
  cat "${RUN_DIR}/exit_code.txt"
  exit 0
fi

echo "__MISSING_SESSION_AND_EXIT_CODE__"
EOF
```

## Close-Out Mapping

Mirror results back into the local receipt:

- remote exit code `0`:
  - `complete --self-check-status pass`
  - `review --decision done`
- remote exit code nonzero:
  - `complete --self-check-status fail`
  - `review --decision blocked`
- transport failure or vanished detached job:
  - `review --decision needs_followup`

Use the local dispatch log plus any remote output paths as `evidence_pointers`.

## Validation Notes

- `workstation-linux-primary` is the cleanest Linux-path entry for workstation compute when it is reachable.
- `workstation-linux-via-host` plus `wsl -e bash -s` is the fallback when the dedicated Linux endpoint is down but the host shell is still reachable.
- `workstation-linux-campus` may fail with host-key verification if the current machine has not trusted that route yet; treat that as an unavailable route rather than auto-mutating SSH trust.
- `shared-server-primary` is the preferred shared-server path when direct access works; `shared-server-via-linux` and `shared-server-via-workstation` are valid fallbacks.
- If `dispatch-script` times out, treat it as a transport or job-shape failure; do not mark the task done, and retry only after a route probe succeeds again.
