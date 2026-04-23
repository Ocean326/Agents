# Output Contract

The skill aims to produce a stable local handoff package for a single page.

## Files

- `<platform>_<id>.json`
- `<platform>_<id>.md`
- `<platform>_<id>_handoff.md`
- `images/`

## JSON Shape

Common top-level keys:

- `platform`
- `status`
- `source_url`
- `resolved_url`
- `id`
- `title`
- `author`
- `published_at`
- `updated_at`
- `content_text`
- `images`
- `image_assets`
- `image_local_paths`
- `agent_handoff`
- `engagement`
- `notes`

Site-specific keys may also appear, such as:

- `answer_id`
- `question_id`
- `author_handle`
- `platform_variant`
- `excerpt`

## Handoff Rules

The handoff file should answer:

- what artifact files were written
- whether the next agent should read images first
- whether the content is text-primary, image-primary, or mixed
- what the next step should be

## Image Download Rules

- download images only when `--output-dir` is supplied
- write them into `images/`
- keep the original page URL in `image_assets[].url`
- keep the local file path in `image_assets[].local_path`
- record failures in `image_assets[].error`

## Failure Contract

On failure, print a JSON payload with:

- `status: "error"`
- `platform`
- `source_url`
- `message`

Do not leave partial temp caches behind.
