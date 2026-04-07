# Claude Code — Developer Guide

## Response style
- Be concise and direct
- Lead with the answer, not the reasoning
- Use code blocks for file paths and commands
- Don't add unnecessary commentary after tool calls

## Tool usage
- Use Read, Write, Edit tools (not cat/sed/echo)
- Use Glob and Grep (not find/grep)
- Use Bash only for system commands and git operations

## Project memory
- Memory files in `.claude/projects/-Users-tonkin-CU-agent/memory/`
- Read MEMORY.md at start of session for project context
- Update memory when learning important project decisions

## Hooks
- Pre-commit hook runs prettier via `format:fix` script
- Always let the hook run — don't bypass with --no-verify

## Settings
- `.claude/settings.json` has project-level configuration
- `.claude/settings.local.json` has local overrides
