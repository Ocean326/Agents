# Framework Selection

Use this file only when the implementation stack is not already obvious from the repo.

## Pick by scope

| Need | Default |
| --- | --- |
| Tiny wrapper around existing commands | Bash |
| Local automation with moderate complexity | Python + `argparse` |
| Polished multi-command developer tool | Python + `typer` or `click` |
| Guided prompts without a full TUI | Python + `questionary` or `InquirerPy` |
| Rich terminal UI | Python + `textual` |
| JS/TS-native repo integration | Node + `commander` or `yargs` |
| Single static binary distribution | Go + `cobra` |

## Selection notes

### Bash

Choose for short glue code around existing executables.
Avoid for large stateful workflows, nested subcommands, or anything with tricky quoting and structured output.

### Python `argparse`

Choose when standard library only is a feature, not a constraint.
Good default for internal tools that need predictable packaging and low dependency weight.

### Python `typer` or `click`

Choose when command trees, typed options, shell completion, and ergonomic help matter.
Prefer `typer` for modern typed codebases; prefer `click` when the repo already uses it.

### Python prompts

Use `questionary` or `InquirerPy` for confirm/select/input flows.
Keep prompts optional so scripted usage still works.

### Python `textual`

Choose for focused operator consoles, dashboards, or approval loops in the terminal.
Do not use it as decoration for workflows that remain simple commands.

### Node `commander` or `yargs`

Choose when the tool lives beside existing JS/TS code or depends on npm packages.
Prefer `commander` for straightforward CLIs; prefer `yargs` when parsing and command composition get heavier.

### Go `cobra`

Choose when startup speed, binary distribution, or cross-platform shipping is the main requirement.
Be wary of using Go just for a local-only script if Python would ship faster.

## Contract checklist

Before implementation, write down:
- command name
- subcommands
- flags and defaults
- examples
- stdout format
- stderr conventions
- exit codes
- dry-run behavior
