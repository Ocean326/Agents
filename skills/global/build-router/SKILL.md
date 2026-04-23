---
name: build-router
description: 面向前端、设计工具链、部署、GitHub 工作流与视觉资产生成的总入口路由器。用于在 visually strong UI、GitHub 操作、Vercel 部署、Figma/Canva 工作流、以及 bitmap image generation/editing 之间选择最合适的技能；当用户只知道“要把东西做出来并上线/出图/进 GitHub”时优先使用。
---

# Build Router

Use this as the public front door for build, design, deployment, and workflow-production tasks.
This router decides whether the task is primarily:

- interface art direction
- exact tool workflow
- deployment
- GitHub maintenance
- image generation/editing

## Use This Router For

- landing pages, websites, demos, prototypes, and visually led app surfaces
- GitHub-oriented delivery steps such as PR handling and CI repair
- Vercel deployment flows
- Figma or Canva specialist tasks when those skills are installed
- bitmap image generation or editing for product or marketing assets

## Do Not Use This Router For

- product discovery, PRDs, or acceptance criteria
  - use `delivery-router`
- architecture decisions
  - use `architect-router`
- AI research workflow
  - use `research-router`
- prompt shaping or official docs lookup
  - use `knowledge-router`

## Routing Table

1. `frontend-skill`
   Use for visually strong landing pages, websites, apps, prototypes, and UI work where art direction and composition matter more than any one framework helper.

2. `deploy-to-vercel`
   Use when the primary task is deployment, preview promotion, or Vercel-specific release work.

3. `github`
   Use for general GitHub workflow actions such as creating PRs, triaging repo state, or coordinating code-hosting tasks.

4. `gh-address-comments`
   Use when the task is specifically to address PR review comments.

5. `gh-fix-ci`
   Use when the main blocker is broken CI on GitHub.

6. `imagegen`
   Use for creating or editing raster images such as heroes, mockups, product shots, textures, sprites, or cutouts.

7. Figma / Canva specialists
   Use the exact installed specialist directly when the user explicitly asks for Figma or Canva work and the skill exists.

8. Framework specialists
   Use exact installed specialists directly when the task is narrowly about React, shadcn, Stripe, Supabase, or similar stack-specific implementation guidance.

## Decision Rules

1. If the task needs one high-quality visual front door, route to `frontend-skill`.
2. If the task is exact-tool and exact-output, use the precise tool skill instead of `frontend-skill`.
3. If the task is mainly about hosting or shipping, route to `deploy-to-vercel`.
4. If the task is a repo workflow problem, route to the GitHub specialist instead of the UI specialist.
5. If the task is mainly a bitmap asset problem, route to `imagegen` even if the output will later appear in the UI.

## Direct-Entry Exceptions

Skip this router and go direct when:

- the user explicitly names `frontend-skill`, `github`, `gh-fix-ci`, `deploy-to-vercel`, `imagegen`, or a Figma/Canva specialist
- the task is a single-tool workflow with no ambiguity
- the work is already deep inside one specialist lane

## Output Contract

Always return:

- primary build lane
- why that lane fits better than the nearby specialists
- whether the task should stay tool-specific or broaden into `frontend-skill`
- one concrete next action

## Guardrails

- do not route every build task into `frontend-skill`
- do not use this router as a substitute for product planning or architecture
- do not hide precise tool skills behind vague category language
- if no specialist is needed, say so and keep the work local and direct

## Example Triggers

- `Use $build-router to choose whether this should go to frontend-skill, GitHub, Vercel, or imagegen.`
- `使用 $build-router 看看这个任务是做 UI、修 CI、发 PR、上线，还是出图。`
- `Use $build-router to pick the narrowest build/design workflow for this request.`
