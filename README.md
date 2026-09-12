# claude-agents

Full agent packages for Claude Code — persona specs, hooks, tools, research vault, context files. Each agent lives in its own directory. Install script copies everything to the right place on the target machine.

## Agents

| Agent | Voice | Specialty |
|-------|-------|-----------|
| `zylnor` | "boss man", dry authority | Offensive security, pentest, exploit dev, LLM jailbreak research |
| `zelus` | "chief", clinical intensity | Detection engineering, adversarial ML, novel bypass corpus authoring |

## Install

```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents

# Install one or both
./zylnor/install.sh
./zelus/install.sh

# Launch (new terminal or source shell rc)
zylnor
zelus
```

## What Each Directory Contains

**zylnor/**
```
agent.md                             → installs to ~/.claude/agents/zylnor.md
home/.zylnor/ops.md                  → installs to ~/.zylnor/ops.md
home/.zylnor/memory-bank/*.md        → installs to ~/.zylnor/memory-bank/
hooks/zylnor-*.sh                    → installs to ~/.claude/hooks/
install.sh                           → runs the install
```

**zelus/**
```
agent.md                             → installs to ~/.claude/agents/zelus.md
home/.zelus/ops.md                   → installs to ~/.zelus/ops.md
home/.zelus/ctx/*.md                 → installs to ~/.zelus/ctx/
home/.zelus/vault/*.md               → installs to ~/.zelus/vault/
home/.zelus/tools/*.py               → installs to ~/.zelus/tools/
home/.zelus/campaigns/*.py           → installs to ~/.zelus/campaigns/
hooks/zelus-*.sh                     → installs to ~/.claude/hooks/
install.sh                           → runs the install
```

## Container / Fleet Deployment

```bash
git clone https://github.com/malianicos/claude-agents.git /app/claude-agents
cd /app/claude-agents && ./zylnor/install.sh
claude --agent zylnor --dangerously-skip-permissions
```

The install script copies agent definition → `~/.claude/agents/`, hooks → `~/.claude/hooks/`, persona files → `~/.<agent>/`. After install, `--agent zylnor` works from any directory.

## Zelus Note

Zelus requires `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` to prevent CLAUDE.md contamination. The install script sets this in the shell alias.
