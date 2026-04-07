#!/bin/bash
# Regenerate SDK-specific persona files from PROJECT.md + dev-guide.md
# Run after editing PROJECT.md or any dev-guide.md

set -e
cd "$(dirname "$0")/.."

echo "Regenerating persona files from PROJECT.md..."

# Claude: CLAUDE.md
cp PROJECT.md CLAUDE.md
if [ -f .claude/dev-guide.md ]; then
  echo -e "\n---\n" >> CLAUDE.md
  cat .claude/dev-guide.md >> CLAUDE.md
fi
echo "  → CLAUDE.md"

# Codex: AGENTS.md
cp PROJECT.md AGENTS.md
if [ -f .codex/dev-guide.md ]; then
  echo -e "\n---\n" >> AGENTS.md
  cat .codex/dev-guide.md >> AGENTS.md
fi
echo "  → AGENTS.md"

# Gemini: GEMINI.md
cp PROJECT.md GEMINI.md
if [ -f .gemini/dev-guide.md ]; then
  echo -e "\n---\n" >> GEMINI.md
  cat .gemini/dev-guide.md >> GEMINI.md
fi
echo "  → GEMINI.md"

echo "Done."
