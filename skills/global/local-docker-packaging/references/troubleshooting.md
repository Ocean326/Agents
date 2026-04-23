# Troubleshooting

## Build Context Is Too Large

Symptoms:

- `docker build` hangs while uploading multiple GB of context.
- Build fails with tar stream errors during context upload.

Action:

1. Run doctor mode and inspect `doctor.selected_context` plus `doctor.dockerignore`.
2. Confirm the chosen build context has a `.dockerignore` aligned with Dockerfile `COPY` paths.
3. If the repo uses a project build script, prefer that script instead of a generic `docker build`.
4. If generic build still uploads too much, rerun with explicit `--context`.

## Ambiguous Repo Layout

Symptoms:

- Doctor mode reports `AMBIGUOUS` for build script, bundle script, or Dockerfile selection.

Action:

1. Re-run with explicit `--build-script`, `--bundle-script`, or `--dockerfile`.
2. If Dockerfile is explicit, also pass `--context` when the build root is not obvious.
3. Do not let the wrapper guess when multiple packaging lanes exist.

## Docker Daemon Is Unreachable

Symptoms:

- `docker info` or `docker ps` reports socket/connect errors.

Action:

1. Run doctor mode:
   - `bash .../run_docker_packaging.sh --doctor-only`
2. Auto-recover with colima:
   - `bash .../run_docker_packaging.sh --ensure-colima --doctor-only`
3. If still failing, start manually:
   - `PATH=/opt/homebrew/bin:$PATH colima start -f --runtime docker`

## Artifact Verification Fails

Action:

1. Confirm the reported `result.image_tar` exists and is non-empty.
2. Confirm `result.bundle_dir` and `result.bundle_archive` both exist when bundle stage runs.
3. Re-run only the missing stage:
   - image only: add `--skip-bundle`
   - bundle only: add `--skip-image`
