# Feishu CLI 2026-04

## Purpose

Summarize the current official Feishu/Lark CLI and MCP routes that are most relevant when extending beyond the Butler-native bot.

## Latest Snapshot Verified On 2026-04-20

- npm package: `@larksuite/cli`
- npm latest version: `1.0.14`
- Official GitHub repo: <https://github.com/larksuite/cli>
- Official article: <https://www.feishu.cn/content/article/7623291503305083853>
- Official MCP repo: <https://github.com/larksuite/lark-openapi-mcp>

## What `lark-cli` Is Good For

Use `lark-cli` when you want the official, broad, agent-friendly command surface instead of Butler's narrower bot runtime.

Strong fits:

- user-identity access to private messages, calendar, docs, mail, or personal data
- broad cross-domain Feishu automation
- direct terminal commands that an agent can call with small prompts
- current official support instead of a private wrapper

## Official Capabilities

Observed from the official GitHub README and Feishu article:

- official Lark/Feishu CLI maintained by the `larksuite` team
- 200+ commands and 22 AI Agent skills
- three layers:
  - shortcut commands
  - API commands
  - raw API calls
- covers IM, Docs, Drive, Sheets, Slides, Base, Calendar, Mail, Tasks, Contact, Wiki, Meetings, and more
- supports both `user` and `bot` identities

## Recommended Install And Auth Flow

```bash
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g
lark-cli config init --new
lark-cli auth login --recommend
lark-cli auth status
```

Useful examples:

```bash
lark-cli calendar +agenda --as user
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --text "Hello"
lark-cli api GET /open-apis/calendar/v4/calendars
```

## Why This Matters For Butler

Butler-native Feishu access is best when you want continuity with the current chat runtime and memory flow.

`lark-cli` is better when you want:

- a wider official command surface
- easier user authorization
- less custom connector maintenance
- direct access to newer domains like mail, meetings, and broader docs workflows

## Official MCP Route

The official MCP server is `@larksuiteoapi/lark-mcp`.

Basic user login:

```bash
npx -y @larksuiteoapi/lark-mcp login -a cli_xxxx -s your_secret
```

Typical MCP config shape:

```json
{
  "mcpServers": {
    "lark-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a",
        "<your_app_id>",
        "-s",
        "<your_app_secret>",
        "--oauth",
        "--token-mode",
        "user_access_token"
      ]
    }
  }
}
```

Important caveat from the official MCP README:

- if you enable `--oauth`, prefer `--token-mode user_access_token` for user-resource access
- otherwise some calls may fall back to `tenant_access_token` and lose access to private user resources

## Practical Choice Guide

- Choose Butler-native Feishu when you need the existing Butler bot behavior.
- Choose `lark-cli` when you want official, free-form terminal access with broad coverage.
- Choose `lark-mcp` when your host agent is already MCP-native and should consume Feishu as tools.

## Sources

- GitHub README: <https://github.com/larksuite/cli/blob/main/README.md>
- GitHub changelog: <https://github.com/larksuite/cli/blob/main/CHANGELOG.md>
- Official Feishu article: <https://www.feishu.cn/content/article/7623291503305083853>
- Official MCP repo: <https://github.com/larksuite/lark-openapi-mcp>
- MCP command reference: <https://github.com/larksuite/lark-openapi-mcp/blob/main/docs/reference/cli/cli.md>
