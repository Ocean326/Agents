---
name: cli-anything
description: Build robust local command-line tools and lightweight interactive operator surfaces. Use when Codex needs to turn a workflow into a reusable CLI, add subcommands or flags, wrap scripts with safer argument handling, create a small terminal UI or guided prompt flow, or choose an implementation approach for local operator tooling in Bash, Python, Node, or Go.
---

# CLI Anything

## Overview

Turn one-off shell ideas into maintainable operator tools.
Prefer the smallest surface that is safe, testable, and pleasant to run locally.

## Workflow

1. Normalize the operator job.
   Identify:
   - who runs it
   - how often it runs
   - whether it is non-interactive, prompt-driven, or full-screen terminal UI
   - what inputs, outputs, exit codes, and side effects matter

2. Choose the lightest viable shape.
   Start with:
   - single shell script for tiny glue tasks
   - Python CLI for most local automation
   - Node CLI when the repo is already Node-first or needs JS ecosystem packages
   - Go CLI when a static binary, concurrency, or very fast startup matters
   - terminal UI only when flags and prompts are no longer enough

3. Design the command contract before coding.
   Define:
   - command name and subcommands
   - required versus optional flags
   - default values
   - output modes such as human text, JSON, or quiet
   - failure behavior and exit codes

4. Build for safe repetition.
   Add:
   - clear help text
   - input validation close to the boundary
   - dry-run mode for destructive actions
   - deterministic stdout for piping and automation
   - actionable stderr for operators

5. Add interaction only where it helps.
   Prefer:
   - flags for automation
   - guided prompts for occasional human use
   - a small TUI for selection, progress, or approval loops
   Keep business logic separate from the interface layer so the same core code can power both CLI and TUI modes.

6. Verify the tool end to end.
   Exercise:
   - `--help`
   - happy path
   - missing-input path
   - invalid-flag path
   - dry-run or no-op path
   - machine-readable output if supported

## Framework Selection

Read [references/framework-selection.md](./references/framework-selection.md) when choosing an implementation stack.

Use these defaults:
- Choose plain Bash only for short wrappers around existing commands where quoting, portability, and error handling stay simple.
- Choose Python plus `argparse` for standard-library-only tools and stable scripts with minimal dependencies.
- Choose Python plus `typer` or `click` for polished multi-command CLIs with rich help, completion, and maintainable command trees.
- Choose Python plus `questionary` or `InquirerPy` for lightweight guided prompts.
- Choose `textual` only when the terminal experience genuinely benefits from panes, lists, live progress, or keyboard navigation.
- Choose Node plus `commander` or `yargs` when the surrounding project is already JavaScript or TypeScript-first.
- Choose Go plus `cobra` when distribution as a single binary is a real requirement.

## Design Rules

- Separate pure operations from argument parsing and presentation.
- Make stdout easy to pipe; send diagnostics to stderr.
- Return non-zero exit codes on operator-relevant failure.
- Prefer explicit flags over positional ambiguity once a command grows.
- Preserve idempotence when possible.
- Keep prompts skippable via flags for automation.
- Offer `--json` only if the output is meaningfully structured and stable.
- Avoid full-screen TUIs for workflows that fit a command plus confirmation prompt.

## Lightweight Operator Surfaces

Use this escalation path:
1. Plain command with flags
2. Command plus confirmation or select prompt
3. Command plus progress display or table output
4. Small TUI with a focused job such as selecting targets, reviewing diffs, or driving a runbook

For operator surfaces:
- Show current state, next action, and consequence clearly.
- Make cancel and back-out paths obvious.
- Avoid hiding file paths, commands, or side effects behind vague labels.
- Keep keyboard flows efficient and discoverable.

## Output Pattern

When using this skill, produce:
- a short rationale for the chosen CLI shape
- the command contract
- the implementation
- a quick verification pass
- any follow-up packaging or distribution note if relevant
