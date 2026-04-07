# Codex — Developer Guide

## Response style
- Be concise and direct
- Lead with the answer, not the reasoning
- Show what changed, don't explain obvious edits

## Tool usage
- Use shell commands for file operations: `cat -n` for reading, `grep -rn` for searching
- Use `apply_patch` for file editing (preferred over rewriting entire files)
- Use `find` with specific patterns for file discovery

## File reading
- Always use `cat -n` to show line numbers
- For large files, use `sed -n '10,30p' file.txt` for ranges
- When searching, use `grep -rn` to include line numbers and context

## Project memory
- Check workspace for any existing context files at session start
- No persistent memory system — each session starts fresh
- Conversation archives in `groups/*/conversations/` provide historical context
