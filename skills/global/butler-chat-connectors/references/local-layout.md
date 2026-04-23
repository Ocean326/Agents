# Example Local Layout

## Purpose

Document a public-safe example layout for Butler chat connector work so the
skill stays understandable without exposing one operator's real machine setup.

## Example Local Repo

- Repo root:
  - `<BUTLER_REPO_ROOT>`
- Feishu bot config:
  - `<BUTLER_REPO_ROOT>/butler_main/butler_bot_code/configs/butler_bot.json`
- Weixin state dir:
  - `<BUTLER_REPO_ROOT>/workspace/weixin_state`
- Weixin state files:
  - `<BUTLER_REPO_ROOT>/workspace/weixin_state/weixin.json`
  - `<BUTLER_REPO_ROOT>/workspace/weixin_state/weixin_qr_login.md`

## Example Remote Source

- Remote alias:
  - `<BUTLER_REMOTE_ALIAS>`
- Remote repo root:
  - `<BUTLER_REMOTE_REPO_ROOT>`
- Remote Feishu config:
  - `<BUTLER_REMOTE_REPO_ROOT>/butler_main/butler_bot_code/configs/butler_bot.json`
- Remote Weixin address config:
  - `<BUTLER_REMOTE_REPO_ROOT>/workspace/weixin_state/weixin.json`

## Public-Safe Verified Facts

- The local Feishu config may need to be refreshed from a remote source and have
  `workspace_root` rewritten to the local repo path.
- A successful Feishu preflight proves local token acquisition, not global
  connector correctness.
- `weixin.json` is only an address/config hint. It is not proof of an
  authenticated session.
- LAN bridge addresses, SSH aliases, and live session files are environment
  specific and should be supplied through local configuration, not hardcoded
  into the public skill.
- If no reusable session file is present, treat Weixin as requiring a fresh
  local QR login.

## Operational Meaning

- Feishu can be considered locally usable only after a real preflight succeeds.
- Weixin can be considered locally connected only after a valid local session or
  successful fresh login exists.
- The safest default Weixin recovery path is:
  1. start a local bridge
  2. generate a fresh QR entry page
  3. re-scan locally
