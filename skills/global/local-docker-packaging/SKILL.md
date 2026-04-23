---
name: local-docker-packaging
description: Build, export, and validate local Docker packaging artifacts for arbitrary repositories on this Mac. Use when Codex needs to ensure Docker or Colima is running, discover project-specific Docker build or bundle scripts, build an image from a Dockerfile, export a `docker save` tar, assemble a delivery bundle, or troubleshoot oversized build context and packaging failures across different projects.
---

# Local Docker Packaging

Use this skill to package a repository with Docker in a repeatable local workflow.

## Start With Doctor Mode

Inspect the repo before building:

```bash
bash $CODEX_HOME/skills/local-docker-packaging/scripts/run_docker_packaging.sh \
  --repo-root "$PWD" \
  --doctor-only
```

Doctor mode reports:

- whether Docker daemon is reachable
- whether Colima is available for auto-recovery
- candidate build scripts
- candidate bundle scripts
- candidate Dockerfiles
- selected auto-detected inputs when unambiguous

## Run The Standard Flow

If doctor mode shows a clean match, use the wrapper script directly:

```bash
bash $CODEX_HOME/skills/local-docker-packaging/scripts/run_docker_packaging.sh \
  --repo-root "$PWD" \
  --ensure-colima
```

Useful flags:

- `--build-script <path>`: force a project-provided image build/export script.
- `--bundle-script <path>`: force a project-provided bundle script.
- `--dockerfile <path>`: force a Dockerfile when no build script is used.
- `--context <path>`: override the Docker build context for generic `docker build`.
- `--image-tag <tag>`: override the image tag.
- `--image-tar <path>`: override the exported tar path.
- `--bundle-dir <path>`: pass an explicit output directory to the bundle script.
- `--docker-build-flag <flag>`: append raw flags to generic `docker build`.
- `--skip-image`: skip image build/export.
- `--skip-bundle`: skip bundle assembly.

## Follow The Selection Rules

1. Prefer a project-provided build/export script when exactly one clear candidate exists.
2. Fall back to generic `docker build -f ...` plus `docker save` when no build script exists and one Dockerfile can be selected safely.
3. Treat the bundle stage as optional: run it only when the repo exposes a clear bundle script or you pass one explicitly.
4. When multiple scripts or Dockerfiles are detected, stop auto-execution and rerun with explicit paths instead of guessing.

## Verify Before Declaring Success

Always verify:

1. `docker info` succeeds or the wrapper can recover with Colima.
2. The exported image tar exists and is non-empty when image stage runs.
3. The bundle directory and archive both exist when bundle stage runs.
4. The chosen build context has a sensible `.dockerignore` when the repo is large.

## Load References On Demand

Read these files only when needed:

- Discovery rules and common repo shapes: [references/repo-discovery.md](./references/repo-discovery.md)
- Troubleshooting patterns: [references/troubleshooting.md](./references/troubleshooting.md)
