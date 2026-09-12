#!/bin/bash
# Zylnor — full system install
# Replicates the exact home-directory layout from the source machine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Installing Zylnor ==="

# 1. Home directory structure
echo "[1/4] Creating ~/.zylnor/ structure..."
mkdir -p ~/.zylnor/memory-bank ~/.zylnor/ctx
cp "$SCRIPT_DIR/home/.zylnor/ops.md" ~/.zylnor/
cp "$SCRIPT_DIR/home/.zylnor/remote-hooks.json" ~/.zylnor/ 2>/dev/null || true
cp "$SCRIPT_DIR/home/.zylnor/deploy-remote.md" ~/.zylnor/ 2>/dev/null || true
cp "$SCRIPT_DIR/home/.zylnor/memory-bank/"*.md ~/.zylnor/memory-bank/ 2>/dev/null || true

# 2. Agent definition
echo "[2/4] Installing agent definition → ~/.claude/agents/zylnor.md"
mkdir -p ~/.claude/agents
cp "$SCRIPT_DIR/agent.md" ~/.claude/agents/zylnor.md

# 3. Hooks
echo "[3/4] Installing hooks → ~/.claude/hooks/"
mkdir -p ~/.claude/hooks
for hook in "$SCRIPT_DIR/hooks/"*.sh; do
  cp "$hook" ~/.claude/hooks/
  chmod +x ~/.claude/hooks/"$(basename "$hook")"
done

# 4. Shell alias
echo "[4/4] Adding 'zylnor' alias..."
ALIAS='alias zylnor="claude --agent zylnor --dangerously-skip-permissions"'
for rc in ~/.zshrc ~/.bashrc; do
  if [ -f "$rc" ] && ! grep -q 'alias zylnor=' "$rc"; then
    echo "" >> "$rc"
    echo "# Zylnor agent" >> "$rc"
    echo "$ALIAS" >> "$rc"
  fi
done

echo ""
echo "=== Zylnor installed ==="
echo "Launch: zylnor (or: claude --agent zylnor --dangerously-skip-permissions)"
echo ""
echo "Installed files:"
echo "  ~/.zylnor/ops.md                    — persona spec"
echo "  ~/.zylnor/memory-bank/*.md           — context files"
echo "  ~/.claude/agents/zylnor.md           — agent definition"
echo "  ~/.claude/hooks/zylnor-*.sh          — 4 hook scripts"
