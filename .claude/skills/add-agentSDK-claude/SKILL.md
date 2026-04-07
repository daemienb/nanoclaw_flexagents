---
name: add-agentSDK-claude
description: Add Anthropic Claude agent SDK. Cloud-only (no local model support). Authenticates via Claude subscription OAuth or API key.
---

# Add Claude Agent SDK

Adds Anthropic Claude runtime support. After installation, groups can use `runtime: 'claude'` for Claude models (Opus, Sonnet, Haiku).

## Phase 1: Pre-flight

Check if already applied:

```bash
ls src/runtime/claude-runtime.ts 2>/dev/null && echo "ALREADY_INSTALLED" || echo "NOT_INSTALLED"
```

If already installed, skip to Phase 3 (Configure).

## Phase 2: Apply Code Changes

### Merge the skill branch

```bash
git fetch origin skill/add-agentSDK-claude
git merge origin/skill/add-agentSDK-claude --no-edit
```

### Build

```bash
npm install && npm run build && ./container/build.sh
```

## Phase 3: Configure

### Authentication

AskUserQuestion: How do you want to authenticate with Anthropic?

1. **Claude subscription (Pro/Max)** — Run `claude setup-token` in another terminal, then add the token to `.env` as `CLAUDE_CODE_OAUTH_TOKEN=<token>`
2. **API key** — Add `ANTHROPIC_API_KEY=sk-ant-...` to `.env`

The credential proxy (port 3001) handles injection into containers.

### Set as default runtime (optional)

Only if Claude should be the default for all groups:
```
DEFAULT_RUNTIME=claude
```

Most users keep `DEFAULT_RUNTIME=codex` and set specific groups to Claude via `/model`.

### Restart service

```bash
launchctl kickstart -k gui/$(id -u)/com.nanoclaw  # macOS
# Linux: systemctl --user restart nanoclaw
```

## Phase 4: Verify

Set a group to Claude runtime:
```sql
sqlite3 store/messages.db "UPDATE registered_groups SET container_config = '{\"runtime\":\"claude\"}' WHERE jid = '...';"
```

Send a message. Check `/auth` shows Claude status.

## Removal

```bash
git log --oneline --all | grep "add Claude"  # find the merge commit
git revert <commit> -m 1
npm install && npm run build && ./container/build.sh
```
