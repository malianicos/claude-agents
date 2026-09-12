#!/bin/bash
# Zelus — full system install
# Replicates the exact home-directory layout from the source machine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Installing Zelus ==="

# 1. Home directory structure
echo "[1/4] Creating ~/.zelus/ structure..."
mkdir -p ~/.zelus/ctx ~/.zelus/vault/unwrap_sessions ~/.zelus/tools ~/.zelus/campaigns
cp "$SCRIPT_DIR/home/.zelus/ops.md" ~/.zelus/
cp "$SCRIPT_DIR/home/.zelus/zelus-launcher.sh" ~/.zelus/ 2>/dev/null || true
chmod +x ~/.zelus/zelus-launcher.sh 2>/dev/null || true

# Context files
for f in "$SCRIPT_DIR/home/.zelus/ctx/"*; do
  [ -f "$f" ] && cp "$f" ~/.zelus/ctx/
done

# Vault (research dossiers, reports, technique encyclopedia)
for f in "$SCRIPT_DIR/home/.zelus/vault/"*; do
  [ -f "$f" ] && cp "$f" ~/.zelus/vault/
done
for f in "$SCRIPT_DIR/home/.zelus/vault/unwrap_sessions/"*; do
  [ -f "$f" ] && cp "$f" ~/.zelus/vault/unwrap_sessions/
done

# Tools (all Python + txt)
for f in "$SCRIPT_DIR/home/.zelus/tools/"*.py "$SCRIPT_DIR/home/.zelus/tools/"*.txt; do
  [ -f "$f" ] && cp "$f" ~/.zelus/tools/
done

# Campaigns
for f in "$SCRIPT_DIR/home/.zelus/campaigns/"*.py; do
  [ -f "$f" ] && cp "$f" ~/.zelus/campaigns/
done

# 2. Agent definition
echo "[2/4] Installing agent definition → ~/.claude/agents/zelus.md"
mkdir -p ~/.claude/agents
cp "$SCRIPT_DIR/agent.md" ~/.claude/agents/zelus.md

# 3. Hooks
echo "[3/4] Installing hooks → ~/.claude/hooks/"
mkdir -p ~/.claude/hooks
for hook in "$SCRIPT_DIR/hooks/"*.sh; do
  cp "$hook" ~/.claude/hooks/
  chmod +x ~/.claude/hooks/"$(basename "$hook")"
done

# 4. Shell alias
echo "[4/4] Adding 'zelus' alias..."
ALIAS='alias zelus="CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude --agent zelus --dangerously-skip-permissions"'
for rc in ~/.zshrc ~/.bashrc; do
  if [ -f "$rc" ] && ! grep -q 'alias zelus=' "$rc"; then
    echo "" >> "$rc"
    echo "# Zelus agent" >> "$rc"
    echo "$ALIAS" >> "$rc"
  fi
done

echo ""
echo "=== Zelus installed ==="
echo "Launch: zelus (or: CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude --agent zelus --dangerously-skip-permissions)"
echo ""
echo "Installed files:"
echo "  ~/.zelus/ops.md                            — persona spec"
echo "  ~/.zelus/ctx/*.md                          — campaign context ($(ls "$SCRIPT_DIR/home/.zelus/ctx/" 2>/dev/null | wc -l | tr -d ' ') files)"
echo "  ~/.zelus/vault/*.md                        — research vault ($(ls "$SCRIPT_DIR/home/.zelus/vault/" 2>/dev/null | wc -l | tr -d ' ') files)"
echo "  ~/.zelus/tools/*.py                        — custom tools ($(ls "$SCRIPT_DIR/home/.zelus/tools/"*.py 2>/dev/null | wc -l | tr -d ' ') files)"
echo "  ~/.zelus/campaigns/*.py                    — campaign scripts"
echo "  ~/.claude/agents/zelus.md                  — agent definition"
echo "  ~/.claude/hooks/zelus-*.sh                 — 6 hook scripts"
echo ""
echo "NOTE: Zelus requires CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 to prevent"
echo "CLAUDE.md contamination in the system prompt."
