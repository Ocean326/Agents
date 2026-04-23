# Save Mode Contract

Use this contract when the user asks to save, archive, write notes, or preserve session continuation context.

## Trigger Phrases

Examples:
- save this
- archive this
- write local notes
- generate a markdown memo
- preserve the continuation packet

## Required Deliverable

Produce one local markdown file that contains:
- source session IDs
- objective and scope
- completed work
- open loops and next actions
- key artifact paths and commands
- assumptions and risks

## Route

Use `$compile-tech-notes` as the note-construction lane.

Expected mode defaults:
- `deliverable`: `task-status-update`
- `target_reader`: future self / collaborator continuing execution
- `stop_condition`: resumable handoff quality

## Minimum Note Sections

1. Scope and Source Sessions
2. Verified Facts and Evidence
3. Completed Work
4. Pending Work and Execution Order
5. Commands and Artifact Paths
6. Risks and Unknowns
