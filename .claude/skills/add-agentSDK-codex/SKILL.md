---
name: add-agentSDK-codex
description: Add OpenAI Codex agent SDK. Supports cloud models (GPT-5.x) and local models (OMLX, Ollama). Authenticates via ChatGPT subscription or API key.
---

# Add Codex Agent SDK

Adds OpenAI Codex runtime support. After installation, groups can use `runtime: 'codex'` for GPT-5.x models, and local models via OMLX or LiteLLM.

## Phase 1: Pre-flight

Check if already applied:

```bash
ls src/runtime/openai-runtime.ts 2>/dev/null && echo "ALREADY_INSTALLED" || echo "NOT_INSTALLED"
```

If already installed, skip to Phase 3 (Configure).

## Phase 2: Apply Code Changes

### Merge the skill branch

```bash
git fetch origin skill/add-agentSDK-codex
git merge origin/skill/add-agentSDK-codex --no-edit
```

### Build

```bash
npm install && npm run build && ./container/build.sh
```

## Phase 3: Configure

### Authentication

AskUserQuestion: How do you want to authenticate with OpenAI?

1. **ChatGPT subscription** — Run `codex auth login` on the server (opens browser for OAuth)
2. **API key** — Add `OPENAI_API_KEY=sk-...` to `.env`

For subscription: tell the user to run `codex auth login` in another terminal. Wait for confirmation.

### Set as default runtime

Add to `.env`:
```
DEFAULT_RUNTIME=codex
```

### Restart service

```bash
launchctl kickstart -k gui/$(id -u)/com.nanoclaw  # macOS
# Linux: systemctl --user restart nanoclaw
```

## Phase 4: Verify

Send a message in the registered chat. Check `/auth` shows Codex status.

## Removal

```bash
git log --oneline --all | grep "add Codex"  # find the merge commit
git revert <commit> -m 1
npm install && npm run build && ./container/build.sh
```
