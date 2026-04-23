---
name: butler-chat-connectors
description: Sync, validate, and operate Butler-style chat connectors on this machine, including a local Feishu bot config, the Weixin bridge and QR login flow, and the newer official Lark/Feishu CLI and MCP routes. Use when Codex needs to migrate Butler chat capability from another machine, copy or refresh bound config safely, run Feishu preflight, start or rebind Weixin locally, or choose between a Butler-native Feishu access path and the official Lark CLI/MCP route for broader user-identity access.
---

# Butler Chat Connectors

## Overview

Use this skill to keep Butler chat access practical on the local Mac without rediscovering where config, secrets, bridge state, and newer official Feishu tooling live.

Start with the narrowest lane that matches the task.

## Lane Selection

### 1. Butler-native Feishu bot

Use this lane when the goal is to keep the existing Butler chat assistant working with its current bot identity and message flow.

Do this:

1. Read [references/local-layout.md](./references/local-layout.md).
2. If config may be stale, run `scripts/sync_from_remote_linux.sh`.
3. Run `scripts/feishu_preflight.sh`.
4. Only claim success after preflight can obtain a tenant token locally.

Choose this lane over `lark-cli` when the task depends on Butler's existing chat runtime, memory behavior, or bot-facing message flow.

### 2. Butler-native Weixin bridge

Use this lane when the goal is to receive and send Weixin messages through Butler's own bridge protocol.

Important:

- Do not assume a previously bound session can be copied.
- Check whether `工作区/weixin_state/weixin_session.json` exists before claiming the binding migrated.
- Treat `weixin.json` as bridge addressing, not proof of an active login.

Default local recovery path:

1. Read [references/local-layout.md](./references/local-layout.md).
2. Start a local bridge with `scripts/start_local_weixin_bridge.sh`.
3. Generate a fresh QR entry page with `scripts/write_local_weixin_qr.sh`.
4. Re-scan and rebind locally if there is no usable session file.

Use the older remote bridge only if the user explicitly wants that topology and the endpoint is confirmed live.

### 3. Official `lark-cli`

Use this lane when the user wants broader, freer Feishu access than the Butler bot exposes, especially user-identity access to personal docs, messages, mail, calendar, or a wider command surface.

Read [references/feishu-cli-2026-04.md](./references/feishu-cli-2026-04.md) before acting.

Prefer this lane when:

- the user wants official, current, open tooling
- the task spans many Feishu business domains
- the task needs `--as user`
- the task is better expressed as direct commands instead of Butler chat orchestration

Keep the default flow small:

1. Install the CLI if it is missing.
2. Run `lark-cli config init --new`.
3. Run `lark-cli auth login --recommend`.
4. Verify with `lark-cli auth status`.
5. Use shortcut commands first, then API commands, then raw API calls only if needed.

### 4. Official `lark-mcp`

Use this lane when the user wants MCP-style integration into an agent client instead of an interactive CLI shell.

Read [references/feishu-cli-2026-04.md](./references/feishu-cli-2026-04.md) for the current official MCP route and token-mode caveat.

Prefer `lark-mcp` when:

- the agent host already supports MCP
- the user wants fine-grained tool whitelists
- the work should stay as tool calls instead of command-line invocations

## Working Rules

- Never print app secrets, tokens, or API keys into chat unless the user explicitly asks for the raw value.
- Back up local config before overwriting it.
- Keep `workspace_root` pointed at the local repo, not the remote machine path.
- Distinguish three different things:
  - app credentials
  - bridge address config
  - active login/session state
- When you infer that a binding is missing, say so plainly instead of pretending the migration is complete.
- Prefer the official `lark-cli` or `lark-mcp` lane for new free-form Feishu capability expansion.
- Prefer the Butler-native lane when continuity with the existing Butler runtime matters more than breadth.

## Output Contract

Return:

- which lane you chose
- what was already present locally
- what you synced or regenerated
- what was verified
- what still needs human action, such as browser auth or QR scan

## Resources

- Local path and current machine-specific findings: [references/local-layout.md](./references/local-layout.md)
- Official Feishu CLI and MCP notes: [references/feishu-cli-2026-04.md](./references/feishu-cli-2026-04.md)
- Sync remote Butler config: `scripts/sync_from_remote_linux.sh`
- Run local Feishu preflight: `scripts/feishu_preflight.sh`
- Start local Weixin bridge: `scripts/start_local_weixin_bridge.sh`
- Write a fresh local Weixin QR page: `scripts/write_local_weixin_qr.sh`
