#!/usr/bin/env bash
set -euo pipefail

MODEL=""
WORKSPACE=""
MODE="plan"
PROMPT=""
SKILL_PATHS=()
OUTPUT_FORMAT="text"
STREAM_PARTIAL_OUTPUT=0
RENDER="raw"

usage() {
  cat <<'EOF'
Usage:
  run_cursor_subagent.sh --model MODEL --workspace PATH --prompt TEXT [--mode MODE] [--skill FILE ...] [--output-format FORMAT] [--stream-partial-output] [--render MODE]

Options:
  --model      Cursor model id, e.g. claude-4.6-sonnet-medium
  --workspace  Absolute workspace path
  --prompt     Prompt to send to cursor-agent
  --mode       plan | ask | none
  --skill      Path to a Codex skill or reference file to inline into the prompt
  --output-format
               Cursor print format: text | json | stream-json
  --stream-partial-output
               Forward Cursor partial text deltas (requires --output-format stream-json)
  --render     raw | assistant-text | md
               raw: preserve Cursor output
               assistant-text: strip stream-json envelope and stream only assistant text
               md: stream assistant text inside a compact Markdown envelope for Codex handoff

Notes:
  - Repeat --skill to attach multiple skill files.
  - Defaults to --mode plan for read-only safety.
  - Use --mode none to omit Cursor's read-only mode.
  - Non-raw render modes internally use Cursor stream-json + partial output.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="${2:-}"
      shift 2
      ;;
    --workspace)
      WORKSPACE="${2:-}"
      shift 2
      ;;
    --prompt)
      PROMPT="${2:-}"
      shift 2
      ;;
    --skill)
      SKILL_PATHS+=("${2:-}")
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --output-format)
      OUTPUT_FORMAT="${2:-}"
      shift 2
      ;;
    --stream-partial-output)
      STREAM_PARTIAL_OUTPUT=1
      shift
      ;;
    --render)
      RENDER="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$MODEL" || -z "$WORKSPACE" || -z "$PROMPT" ]]; then
  echo "Missing required arguments." >&2
  usage >&2
  exit 2
fi

if ! command -v cursor-agent >/dev/null 2>&1; then
  echo "cursor-agent not found in PATH." >&2
  exit 127
fi

if [[ ! -d "$WORKSPACE" ]]; then
  echo "Workspace does not exist: $WORKSPACE" >&2
  exit 2
fi

case "$RENDER" in
  raw|assistant-text|md)
    ;;
  *)
    echo "Invalid --render: $RENDER (expected raw, assistant-text, or md)" >&2
    exit 2
    ;;
esac

if (( ${#SKILL_PATHS[@]} > 0 )); then
  for skill_path in "${SKILL_PATHS[@]}"; do
    if [[ ! -f "$skill_path" ]]; then
      echo "Skill file does not exist: $skill_path" >&2
      exit 2
    fi
    if [[ ! -r "$skill_path" ]]; then
      echo "Skill file is not readable: $skill_path" >&2
      exit 2
    fi
  done
fi

cmd=(cursor-agent -p --trust --workspace "$WORKSPACE" --model "$MODEL")

case "$MODE" in
  plan|ask)
    cmd+=(--mode "$MODE")
    ;;
  none)
    ;;
  *)
    echo "Invalid --mode: $MODE (expected plan, ask, or none)" >&2
    exit 2
    ;;
esac

if [[ "$RENDER" == "raw" ]]; then
  case "$OUTPUT_FORMAT" in
    text|json|stream-json)
      cmd+=(--output-format "$OUTPUT_FORMAT")
      ;;
    *)
      echo "Invalid --output-format: $OUTPUT_FORMAT (expected text, json, or stream-json)" >&2
      exit 2
      ;;
  esac

  if (( STREAM_PARTIAL_OUTPUT > 0 )); then
    if [[ "$OUTPUT_FORMAT" != "stream-json" ]]; then
      echo "--stream-partial-output requires --output-format stream-json" >&2
      exit 2
    fi
    cmd+=(--stream-partial-output)
  fi
else
  cmd+=(--output-format stream-json --stream-partial-output)
fi

if (( ${#SKILL_PATHS[@]} > 0 )); then
  COMBINED_PROMPT=$'Treat the attached skill files as explicit operating instructions for this task.\n'
  COMBINED_PROMPT+=$'Read them first, follow their workflow when relevant, and do not claim native automatic skill triggering.\n\n'

  for skill_path in "${SKILL_PATHS[@]}"; do
    COMBINED_PROMPT+=$'===== BEGIN ATTACHED SKILL FILE: '"$skill_path"$' =====\n'
    COMBINED_PROMPT+="$(cat "$skill_path")"
    COMBINED_PROMPT+=$'\n===== END ATTACHED SKILL FILE =====\n\n'
  done

  COMBINED_PROMPT+=$'===== USER TASK =====\n'
  COMBINED_PROMPT+="$PROMPT"
  cmd+=("$COMBINED_PROMPT")
else
  cmd+=("$PROMPT")
fi

if [[ "$RENDER" == "raw" ]]; then
  exec "${cmd[@]}"
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found in PATH; required for --render $RENDER." >&2
  exit 127
fi

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
RENDER_SCRIPT="${SUBAGENT_CURSOR_RENDER_SCRIPT:-$CODEX_HOME/skills/subagent-cursor/scripts/render_cursor_stream.py}"
if [[ ! -f "$RENDER_SCRIPT" ]]; then
  echo "Render script does not exist: $RENDER_SCRIPT" >&2
  exit 2
fi

python3 -u "$RENDER_SCRIPT" \
  --render "$RENDER" \
  --requested-model "$MODEL" \
  --workspace "$WORKSPACE" \
  --mode "$MODE" \
  -- "${cmd[@]}"
