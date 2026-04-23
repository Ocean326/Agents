#!/usr/bin/env bash
set -euo pipefail

DEFAULT_REPO_ROOT="$(pwd)"
REPO_ROOT="$DEFAULT_REPO_ROOT"
BUILD_SCRIPT=""
BUNDLE_SCRIPT=""
DOCKERFILE=""
CONTEXT_PATH=""
CONTEXT_EXPLICIT=0
IMAGE_TAG=""
IMAGE_TAR=""
BUNDLE_DIR=""
SKIP_IMAGE=0
SKIP_BUNDLE=0
ENSURE_COLIMA=0
DOCTOR_ONLY=0
BUILD_SCRIPT_AMBIGUOUS=0
BUNDLE_SCRIPT_AMBIGUOUS=0
DOCKERFILE_AMBIGUOUS=0
BUILD_MODE="none"
DOCKERIGNORE_PATH=""
BUILD_SCRIPT_ARGS=()
BUNDLE_SCRIPT_ARGS=()
DOCKER_BUILD_FLAGS=()
BUILD_SCRIPT_CANDIDATES=()
BUNDLE_SCRIPT_CANDIDATES=()
DOCKERFILE_CANDIDATES=()

usage() {
  cat <<'USAGE'
Usage:
  run_docker_packaging.sh [options]

Options:
  --repo-root <path>        Repository root. Default: current working directory
  --build-script <path>     Explicit image build/export script path
  --bundle-script <path>    Explicit bundle assembly script path
  --dockerfile <path>       Explicit Dockerfile path when using generic docker build
  --context <path>          Explicit docker build context path
  --image-tag <tag>         Docker image tag. Default: <repo-name>-local:latest
  --image-tar <path>        Exported image tar path. Default: <repo-root>/<repo-name>_image.tar
  --bundle-dir <path>       Explicit bundle output directory passed to bundle script
  --build-script-arg <arg>  Extra argument passed to build script (repeatable)
  --bundle-script-arg <arg> Extra argument passed to bundle script (repeatable)
  --docker-build-flag <f>   Extra flag passed to generic docker build (repeatable)
  --skip-image          Skip image build + export stage
  --skip-bundle         Skip source/resource bundle stage
  --ensure-colima       Start colima if docker daemon is unreachable
  --doctor-only         Only run preflight checks
  --help                Show this help text
USAGE
}

log() {
  printf '[local-packaging] %s\n' "$*"
}

warn() {
  printf '[local-packaging][warn] %s\n' "$*" >&2
}

die() {
  printf '[local-packaging][error] %s\n' "$*" >&2
  exit 1
}

abs_path() {
  local input="$1"
  if [[ "$input" == /* ]]; then
    printf '%s\n' "$input"
    return 0
  fi
  printf '%s/%s\n' "$(pwd)" "$input"
}

resolve_under_repo() {
  local input="$1"
  local repo_root="$2"
  if [[ "$input" == /* ]]; then
    printf '%s\n' "$input"
    return 0
  fi
  printf '%s/%s\n' "$repo_root" "$input"
}

sanitize_name() {
  local raw="$1"
  local cleaned
  cleaned="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"
  if [[ -z "$cleaned" ]]; then
    cleaned="local-image"
  fi
  printf '%s\n' "$cleaned"
}

join_candidates() {
  if [[ "$#" -eq 0 ]]; then
    printf 'NONE\n'
    return 0
  fi
  local IFS='|'
  printf '%s\n' "$*"
}

find_script_candidates() {
  local repo_root="$1"
  local mode="$2"
  local pattern=""
  case "$mode" in
    build)
      pattern='(build[^/]*export|export[^/]*image|docker[^/]*build|image[^/]*export|build-image|package[^/]*image)'
      ;;
    bundle)
      pattern='(assemble[^/]*bundle|bundle[^/]*export|package[^/]*bundle|delivery[^/]*bundle)'
      ;;
    *)
      die "unknown script candidate mode: $mode"
      ;;
  esac
  if command -v rg >/dev/null 2>&1; then
    rg --files "$repo_root" \
      -g '*.sh' \
      -g '!**/.git/**' \
      -g '!**/node_modules/**' \
      -g '!**/delivery_out/**' \
      -g '!**/dist/**' \
      -g '!**/target/**' \
      -g '!**/.venv/**' \
      -g '!**/venv/**' \
      -g '!**/__pycache__/**' | grep -E "/[^/]*${pattern}[^/]*\\.sh$" || true
    return 0
  fi
  find "$repo_root" \
    \( -path '*/.git' -o -path '*/.git/*' -o -path '*/node_modules' -o -path '*/node_modules/*' -o -path '*/delivery_out' -o -path '*/delivery_out/*' -o -path '*/dist' -o -path '*/dist/*' -o -path '*/target' -o -path '*/target/*' -o -path '*/.venv' -o -path '*/.venv/*' -o -path '*/venv' -o -path '*/venv/*' -o -path '*/__pycache__' -o -path '*/__pycache__/*' \) -prune -o \
    -type f -name '*.sh' -print | grep -E "/[^/]*${pattern}[^/]*\\.sh$" || true
}

find_dockerfile_candidates() {
  local repo_root="$1"
  if command -v rg >/dev/null 2>&1; then
    rg --files "$repo_root" \
      -g 'Dockerfile' \
      -g '*.Dockerfile' \
      -g 'dockerfile' \
      -g '!**/.git/**' \
      -g '!**/node_modules/**' \
      -g '!**/delivery_out/**' \
      -g '!**/dist/**' \
      -g '!**/target/**' \
      -g '!**/.venv/**' \
      -g '!**/venv/**' \
      -g '!**/__pycache__/**'
    return 0
  fi
  find "$repo_root" \
    \( -path '*/.git' -o -path '*/.git/*' -o -path '*/node_modules' -o -path '*/node_modules/*' -o -path '*/delivery_out' -o -path '*/delivery_out/*' -o -path '*/dist' -o -path '*/dist/*' -o -path '*/target' -o -path '*/target/*' -o -path '*/.venv' -o -path '*/.venv/*' -o -path '*/venv' -o -path '*/venv/*' -o -path '*/__pycache__' -o -path '*/__pycache__/*' \) -prune -o \
    -type f \( -name 'Dockerfile' -o -name '*.Dockerfile' -o -iname 'dockerfile' \) -print
}

single_pattern_match() {
  local pattern="$1"
  shift
  local item
  local matches=()
  for item in "$@"; do
    [[ "$item" == *"$pattern"* ]] && matches+=("$item")
  done
  if [[ "${#matches[@]}" -eq 1 ]]; then
    printf '%s\n' "${matches[0]}"
  fi
}

single_basename_match() {
  local basename_target="$1"
  shift
  local item
  local matches=()
  for item in "$@"; do
    [[ "$(basename "$item")" == "$basename_target" ]] && matches+=("$item")
  done
  if [[ "${#matches[@]}" -eq 1 ]]; then
    printf '%s\n' "${matches[0]}"
  fi
}

pick_candidate() {
  local mode="$1"
  local repo_root="$2"
  shift 2
  local candidates=("$@")
  local selected=""

  if [[ "${#candidates[@]}" -eq 0 ]]; then
    printf '\n'
    return 0
  fi
  if [[ "${#candidates[@]}" -eq 1 ]]; then
    printf '%s\n' "${candidates[0]}"
    return 0
  fi

  case "$mode" in
    build_script)
      selected="$(single_basename_match "build_image_and_export.sh" "${candidates[@]}")"
      [[ -n "$selected" ]] || selected="$(single_pattern_match "/deploy/docker/" "${candidates[@]}")"
      [[ -n "$selected" ]] || selected="$(single_pattern_match "/docker/" "${candidates[@]}")"
      ;;
    bundle_script)
      selected="$(single_basename_match "assemble_delivery_bundle.sh" "${candidates[@]}")"
      [[ -n "$selected" ]] || selected="$(single_pattern_match "/deploy/docker/" "${candidates[@]}")"
      [[ -n "$selected" ]] || selected="$(single_pattern_match "/docker/" "${candidates[@]}")"
      ;;
    dockerfile)
      if [[ -f "$repo_root/Dockerfile" ]]; then
        printf '%s\n' "$repo_root/Dockerfile"
        return 0
      fi
      selected="$(single_pattern_match "/deploy/docker/Dockerfile" "${candidates[@]}")"
      [[ -n "$selected" ]] || selected="$(single_pattern_match "/docker/Dockerfile" "${candidates[@]}")"
      ;;
    *)
      die "unknown pick_candidate mode: $mode"
      ;;
  esac

  if [[ -n "$selected" ]]; then
    printf '%s\n' "$selected"
    return 0
  fi
  printf '__AMBIGUOUS__\n'
}

autodetect_context() {
  local dockerfile_path="$1"
  local repo_root="$2"
  local docker_dir
  local parent_dir

  docker_dir="$(cd "$(dirname "$dockerfile_path")" && pwd)"
  if [[ "$dockerfile_path" == "$repo_root/Dockerfile" ]]; then
    printf '%s\n' "$repo_root"
    return 0
  fi
  if [[ "$(basename "$docker_dir")" == "docker" ]]; then
    parent_dir="$(cd "$docker_dir/.." && pwd)"
    if [[ "$(basename "$parent_dir")" == "deploy" ]]; then
      printf '%s\n' "$(cd "$parent_dir/.." && pwd)"
      return 0
    fi
    printf '%s\n' "$parent_dir"
    return 0
  fi
  printf '%s\n' "$docker_dir"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      [[ $# -ge 2 ]] || die "missing value for --repo-root"
      REPO_ROOT="$2"
      shift 2
      ;;
    --build-script)
      [[ $# -ge 2 ]] || die "missing value for --build-script"
      BUILD_SCRIPT="$2"
      shift 2
      ;;
    --bundle-script)
      [[ $# -ge 2 ]] || die "missing value for --bundle-script"
      BUNDLE_SCRIPT="$2"
      shift 2
      ;;
    --dockerfile)
      [[ $# -ge 2 ]] || die "missing value for --dockerfile"
      DOCKERFILE="$2"
      shift 2
      ;;
    --context)
      [[ $# -ge 2 ]] || die "missing value for --context"
      CONTEXT_PATH="$2"
      CONTEXT_EXPLICIT=1
      shift 2
      ;;
    --image-tag)
      [[ $# -ge 2 ]] || die "missing value for --image-tag"
      IMAGE_TAG="$2"
      shift 2
      ;;
    --image-tar)
      [[ $# -ge 2 ]] || die "missing value for --image-tar"
      IMAGE_TAR="$2"
      shift 2
      ;;
    --bundle-dir)
      [[ $# -ge 2 ]] || die "missing value for --bundle-dir"
      BUNDLE_DIR="$2"
      shift 2
      ;;
    --build-script-arg)
      [[ $# -ge 2 ]] || die "missing value for --build-script-arg"
      BUILD_SCRIPT_ARGS+=("$2")
      shift 2
      ;;
    --bundle-script-arg)
      [[ $# -ge 2 ]] || die "missing value for --bundle-script-arg"
      BUNDLE_SCRIPT_ARGS+=("$2")
      shift 2
      ;;
    --docker-build-flag)
      [[ $# -ge 2 ]] || die "missing value for --docker-build-flag"
      DOCKER_BUILD_FLAGS+=("$2")
      shift 2
      ;;
    --skip-image)
      SKIP_IMAGE=1
      shift
      ;;
    --skip-bundle)
      SKIP_BUNDLE=1
      shift
      ;;
    --ensure-colima)
      ENSURE_COLIMA=1
      shift
      ;;
    --doctor-only)
      DOCTOR_ONLY=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

REPO_ROOT="$(abs_path "$REPO_ROOT")"
[[ -d "$REPO_ROOT" ]] || die "repo root not found: $REPO_ROOT"

if [[ -n "$BUILD_SCRIPT" ]]; then
  BUILD_SCRIPT="$(resolve_under_repo "$BUILD_SCRIPT" "$REPO_ROOT")"
  [[ -f "$BUILD_SCRIPT" ]] || die "build script not found: $BUILD_SCRIPT"
fi
if [[ -n "$BUNDLE_SCRIPT" ]]; then
  BUNDLE_SCRIPT="$(resolve_under_repo "$BUNDLE_SCRIPT" "$REPO_ROOT")"
  [[ -f "$BUNDLE_SCRIPT" ]] || die "bundle script not found: $BUNDLE_SCRIPT"
fi
if [[ -n "$DOCKERFILE" ]]; then
  DOCKERFILE="$(resolve_under_repo "$DOCKERFILE" "$REPO_ROOT")"
  [[ -f "$DOCKERFILE" ]] || die "dockerfile not found: $DOCKERFILE"
fi
if [[ -n "$CONTEXT_PATH" ]]; then
  CONTEXT_PATH="$(resolve_under_repo "$CONTEXT_PATH" "$REPO_ROOT")"
  [[ -d "$CONTEXT_PATH" ]] || die "context path not found: $CONTEXT_PATH"
fi
if [[ -z "$IMAGE_TAG" ]]; then
  IMAGE_TAG="$(sanitize_name "$(basename "$REPO_ROOT")")-local:latest"
fi
if [[ -z "$IMAGE_TAR" ]]; then
  IMAGE_TAR="$REPO_ROOT/$(sanitize_name "$(basename "$REPO_ROOT")")_image.tar"
else
  IMAGE_TAR="$(resolve_under_repo "$IMAGE_TAR" "$REPO_ROOT")"
fi
if [[ -n "$BUNDLE_DIR" ]]; then
  BUNDLE_DIR="$(resolve_under_repo "$BUNDLE_DIR" "$REPO_ROOT")"
fi

if [[ -z "$BUILD_SCRIPT" ]]; then
  while IFS= read -r line; do
    [[ -n "$line" ]] && BUILD_SCRIPT_CANDIDATES+=("$line")
  done < <(find_script_candidates "$REPO_ROOT" build)
  BUILD_SCRIPT="$(pick_candidate build_script "$REPO_ROOT" "${BUILD_SCRIPT_CANDIDATES[@]}")"
  if [[ "$BUILD_SCRIPT" == "__AMBIGUOUS__" ]]; then
    BUILD_SCRIPT_AMBIGUOUS=1
    BUILD_SCRIPT=""
  fi
fi
if [[ -z "$BUNDLE_SCRIPT" ]]; then
  while IFS= read -r line; do
    [[ -n "$line" ]] && BUNDLE_SCRIPT_CANDIDATES+=("$line")
  done < <(find_script_candidates "$REPO_ROOT" bundle)
  BUNDLE_SCRIPT="$(pick_candidate bundle_script "$REPO_ROOT" "${BUNDLE_SCRIPT_CANDIDATES[@]}")"
  if [[ "$BUNDLE_SCRIPT" == "__AMBIGUOUS__" ]]; then
    BUNDLE_SCRIPT_AMBIGUOUS=1
    BUNDLE_SCRIPT=""
  fi
fi
if [[ -z "$DOCKERFILE" ]]; then
  while IFS= read -r line; do
    [[ -n "$line" ]] && DOCKERFILE_CANDIDATES+=("$line")
  done < <(find_dockerfile_candidates "$REPO_ROOT")
  DOCKERFILE="$(pick_candidate dockerfile "$REPO_ROOT" "${DOCKERFILE_CANDIDATES[@]}")"
  if [[ "$DOCKERFILE" == "__AMBIGUOUS__" ]]; then
    DOCKERFILE_AMBIGUOUS=1
    DOCKERFILE=""
  fi
fi

if [[ -z "$CONTEXT_PATH" && -n "$DOCKERFILE" ]]; then
  CONTEXT_PATH="$(autodetect_context "$DOCKERFILE" "$REPO_ROOT")"
fi
if [[ -n "$BUILD_SCRIPT" && "$CONTEXT_EXPLICIT" -eq 0 ]]; then
  CONTEXT_PATH="$REPO_ROOT"
fi
if [[ -n "$CONTEXT_PATH" ]]; then
  DOCKERIGNORE_PATH="$CONTEXT_PATH/.dockerignore"
else
  DOCKERIGNORE_PATH="$REPO_ROOT/.dockerignore"
fi
if [[ ! -f "$DOCKERIGNORE_PATH" ]]; then
  warn "missing $DOCKERIGNORE_PATH; docker build context may be larger than expected"
fi

if [[ -x /opt/homebrew/bin/docker ]] && ! command -v docker >/dev/null 2>&1; then
  export PATH="/opt/homebrew/bin:$PATH"
fi
if [[ -x /opt/homebrew/bin/colima ]] && ! command -v colima >/dev/null 2>&1; then
  export PATH="/opt/homebrew/bin:$PATH"
fi

DOCKER_CLI="$(command -v docker || true)"
COLIMA_CLI="$(command -v colima || true)"
[[ -n "$DOCKER_CLI" ]] || die "docker CLI not found; install Docker CLI first"

DOCKER_OK=0
if "$DOCKER_CLI" info >/dev/null 2>&1; then
  DOCKER_OK=1
fi

if [[ "$DOCKER_OK" -eq 0 && "$ENSURE_COLIMA" -eq 1 ]]; then
  [[ -n "$COLIMA_CLI" ]] || die "docker daemon unreachable and colima not found"
  log "docker daemon unreachable; starting colima"
  "$COLIMA_CLI" start -f --runtime docker
  if "$DOCKER_CLI" info >/dev/null 2>&1; then
    DOCKER_OK=1
  fi
fi

if [[ -n "$BUILD_SCRIPT" ]]; then
  BUILD_MODE="script"
elif [[ -n "$DOCKERFILE" ]]; then
  BUILD_MODE="dockerfile"
fi

if [[ "$DOCTOR_ONLY" -eq 1 ]]; then
  printf 'doctor.repo_root=%s\n' "$REPO_ROOT"
  printf 'doctor.docker_cli=%s\n' "$DOCKER_CLI"
  if [[ -n "$COLIMA_CLI" ]]; then
    printf 'doctor.colima_cli=%s\n' "$COLIMA_CLI"
  else
    printf 'doctor.colima_cli=NOT_FOUND\n'
  fi
  if [[ "$DOCKER_OK" -eq 1 ]]; then
    printf 'doctor.docker_daemon=OK\n'
  else
    printf 'doctor.docker_daemon=UNREACHABLE\n'
  fi
  printf 'doctor.build_script_candidates=%s\n' "$(join_candidates "${BUILD_SCRIPT_CANDIDATES[@]}")"
  printf 'doctor.bundle_script_candidates=%s\n' "$(join_candidates "${BUNDLE_SCRIPT_CANDIDATES[@]}")"
  printf 'doctor.dockerfile_candidates=%s\n' "$(join_candidates "${DOCKERFILE_CANDIDATES[@]}")"
  if [[ "$BUILD_SCRIPT_AMBIGUOUS" -eq 1 ]]; then
    printf 'doctor.selected_build_script=AMBIGUOUS\n'
  elif [[ -n "$BUILD_SCRIPT" ]]; then
    printf 'doctor.selected_build_script=%s\n' "$BUILD_SCRIPT"
  else
    printf 'doctor.selected_build_script=NONE\n'
  fi
  if [[ "$BUNDLE_SCRIPT_AMBIGUOUS" -eq 1 ]]; then
    printf 'doctor.selected_bundle_script=AMBIGUOUS\n'
  elif [[ -n "$BUNDLE_SCRIPT" ]]; then
    printf 'doctor.selected_bundle_script=%s\n' "$BUNDLE_SCRIPT"
  else
    printf 'doctor.selected_bundle_script=NONE\n'
  fi
  if [[ "$DOCKERFILE_AMBIGUOUS" -eq 1 ]]; then
    printf 'doctor.selected_dockerfile=AMBIGUOUS\n'
  elif [[ -n "$DOCKERFILE" ]]; then
    printf 'doctor.selected_dockerfile=%s\n' "$DOCKERFILE"
  else
    printf 'doctor.selected_dockerfile=NONE\n'
  fi
  if [[ -n "$CONTEXT_PATH" ]]; then
    printf 'doctor.selected_context=%s\n' "$CONTEXT_PATH"
  else
    printf 'doctor.selected_context=NONE\n'
  fi
  printf 'doctor.build_mode=%s\n' "$BUILD_MODE"
  if [[ -f "$DOCKERIGNORE_PATH" ]]; then
    printf 'doctor.dockerignore=OK:%s\n' "$DOCKERIGNORE_PATH"
  else
    printf 'doctor.dockerignore=MISSING:%s\n' "$DOCKERIGNORE_PATH"
  fi
  exit 0
fi

if [[ "$DOCKER_OK" -eq 0 ]]; then
  die "docker daemon unreachable. Re-run with --ensure-colima or start daemon manually"
fi

if [[ "$SKIP_IMAGE" -eq 0 ]]; then
  if [[ "$BUILD_SCRIPT_AMBIGUOUS" -eq 1 ]]; then
    die "multiple build scripts detected; re-run with --build-script"
  fi
  if [[ -n "$BUILD_SCRIPT" ]]; then
    log "building image via project build script"
    IMAGE_TAG="$IMAGE_TAG" OUTPUT_TAR="$IMAGE_TAR" bash "$BUILD_SCRIPT" "${BUILD_SCRIPT_ARGS[@]}"
  else
    if [[ "$DOCKERFILE_AMBIGUOUS" -eq 1 ]]; then
      die "multiple Dockerfiles detected; re-run with --dockerfile"
    fi
    [[ -n "$DOCKERFILE" ]] || die "no build script or Dockerfile found for image stage"
    [[ -n "$CONTEXT_PATH" ]] || die "could not determine docker build context; pass --context"
    log "building image via generic docker build"
    "$DOCKER_CLI" build -f "$DOCKERFILE" -t "$IMAGE_TAG" "${DOCKER_BUILD_FLAGS[@]}" "$CONTEXT_PATH"
    "$DOCKER_CLI" save -o "$IMAGE_TAR" "$IMAGE_TAG"
  fi
  [[ -s "$IMAGE_TAR" ]] || die "image tar missing or empty: $IMAGE_TAR"
else
  log "skipping image build/export"
fi

BUNDLE_OUTPUT_DIR=""
BUNDLE_ARCHIVE=""
if [[ "$SKIP_BUNDLE" -eq 0 ]]; then
  if [[ "$BUNDLE_SCRIPT_AMBIGUOUS" -eq 1 ]]; then
    die "multiple bundle scripts detected; re-run with --bundle-script or --skip-bundle"
  fi
  if [[ -n "$BUNDLE_SCRIPT" ]]; then
    log "assembling bundle via project bundle script"
    if [[ -n "$BUNDLE_DIR" ]]; then
      BUNDLE_LOG="$(bash "$BUNDLE_SCRIPT" "$BUNDLE_DIR" "${BUNDLE_SCRIPT_ARGS[@]}")"
    else
      BUNDLE_LOG="$(bash "$BUNDLE_SCRIPT" "${BUNDLE_SCRIPT_ARGS[@]}")"
    fi
    printf '%s\n' "$BUNDLE_LOG"
    BUNDLE_OUTPUT_DIR="$(printf '%s\n' "$BUNDLE_LOG" | awk -F': *' '/^bundle directory:/ {print $2}' | tail -n 1)"
    BUNDLE_ARCHIVE="$(printf '%s\n' "$BUNDLE_LOG" | awk -F': *' '/^bundle archive:/ {print $2}' | tail -n 1)"
    [[ -n "$BUNDLE_OUTPUT_DIR" && -d "$BUNDLE_OUTPUT_DIR" ]] || die "bundle output directory not found"
    [[ -n "$BUNDLE_ARCHIVE" && -s "$BUNDLE_ARCHIVE" ]] || die "bundle archive missing or empty"
  else
    log "no bundle script found; skipping bundle stage"
  fi
else
  log "skipping source/resource bundle"
fi

log "completed"
printf 'result.repo_root=%s\n' "$REPO_ROOT"
printf 'result.build_mode=%s\n' "$BUILD_MODE"
printf 'result.image_tag=%s\n' "$IMAGE_TAG"
if [[ "$SKIP_IMAGE" -eq 0 ]]; then
  printf 'result.image_tar=%s\n' "$IMAGE_TAR"
fi
if [[ -n "$BUNDLE_OUTPUT_DIR" ]]; then
  printf 'result.bundle_dir=%s\n' "$BUNDLE_OUTPUT_DIR"
  printf 'result.bundle_archive=%s\n' "$BUNDLE_ARCHIVE"
fi
if [[ "$SKIP_BUNDLE" -eq 0 && -z "$BUNDLE_OUTPUT_DIR" ]]; then
  printf 'result.bundle_status=SKIPPED_NO_SCRIPT\n'
fi
