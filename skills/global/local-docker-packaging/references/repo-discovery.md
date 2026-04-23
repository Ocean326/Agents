# Repo Discovery

Use these rules when adapting the skill to a new repository:

## Prefer Explicit Inputs When The Repo Is Complex

- Pass `--build-script` when the repo has multiple shell entrypoints for image export.
- Pass `--bundle-script` when the repo has multiple delivery or package scripts.
- Pass `--dockerfile` and `--context` when the repo has multiple Dockerfiles or nonstandard build context rules.

## Auto-Discovery Heuristics

- Build script candidates are shell scripts whose names suggest image build or export.
- Bundle script candidates are shell scripts whose names suggest bundle assembly or delivery packaging.
- Dockerfile candidates are files named `Dockerfile`, `*.Dockerfile`, or `dockerfile`.
- The selector prefers unique matches such as `build_image_and_export.sh`, `assemble_delivery_bundle.sh`, root `Dockerfile`, or paths under `deploy/docker/`.

## Generic Fallback Behavior

- If a unique project build script exists, the wrapper exports `IMAGE_TAG` and `OUTPUT_TAR` and lets the repo-specific script drive the build.
- If no build script exists, the wrapper falls back to `docker build` plus `docker save`.
- If no bundle script exists, the bundle stage is skipped instead of inventing a repo archive format.

## Common Good Repo Shapes

- A root `.dockerignore` or context-local `.dockerignore` that matches Dockerfile `COPY` paths.
- A project script like `deploy/docker/build_image_and_export.sh`.
- A separate bundle script like `assemble_delivery_bundle.sh` when image tar is not the only artifact.
