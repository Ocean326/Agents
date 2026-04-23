# Artifact Policy

## Goal

Think in a complete document chain without forcing unnecessary repo noise.

## Artifact Set

The standard set is:
- brief
- design
- implementation plan
- test plan
- verification report
- retrospective

Use only what the task needs, but always make the path, verification, and risk picture explicit.

## Placement Rules

Prefer this order:
1. existing project documentation location
2. existing workflow-specific directory if the repo already has one
3. inline conversational artifact using the templates in `assets/templates/`

Do not invent deep folder structures unless the project already uses them.

## When to Create Each Artifact

### Brief

Create when scope, audience, success criteria, or constraints need to be locked.

### Design

Create when there are multiple reasonable approaches, meaningful tradeoffs, or non-trivial behavior changes.

### Implementation Plan

Create when the work spans multiple steps, files, or verification surfaces.

### Test Plan

Create when coverage is non-trivial, requirements are formalized, or failure modes matter.

### Verification Report

Create whenever substantial work is completed.
For tiny changes, this may be folded into the closeout message.

### Retrospective

Create when the work exposed reusable lessons, follow-up opportunities, or process debt.

## Naming Guidance

Keep names simple and descriptive.
If the project has no naming convention, prefer:
- `<topic>-brief.md`
- `<topic>-design.md`
- `<topic>-implementation-plan.md`
- `<topic>-test-plan.md`
- `<topic>-verification.md`
- `<topic>-retrospective.md`

## Anti-Noise Rule

Do not create documents that only repeat the conversation.
Every artifact should either:
- reduce ambiguity
- unblock implementation
- improve verification
- preserve reusable conclusions
