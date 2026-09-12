# claude-agents

Full agent definitions for Claude Code — persona specs, hooks, tools, research vault, context files. Two deployment modes: system install (replicates the exact home-directory layout) or portable clone-and-go.

## Agents

| Agent | Voice | Specialty | Files |
|-------|-------|-----------|-------|
| `zylnor` | "boss man", dry authority | Offensive security, pentest, exploit dev, LLM jailbreak research | 12 |
| `zelus` | "chief", clinical intensity | Detection engineering, adversarial ML, novel bypass corpus authoring | 76 |

## System Install (recommended for persistent machines)

Replicates the exact home-directory layout — `~/.zylnor/`, `~/.zelus/`, `~/.claude/agents/`, `~/.claude/hooks/`. Works from any directory after install.

```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents

# Install one or both
chmod +x zylnor/install.sh && ./zylnor/install.sh
chmod +x zelus/install.sh && ./zelus/install.sh

# Launch (after sourcing shell rc or new terminal)
zylnor
zelus
```

### What gets installed

**Zylnor:**
```
~/.zylnor/ops.md                     — full persona spec (230 lines)
~/.zylnor/memory-bank/*.md            — projectbrief, techContext, systemPatterns, productContext
~/.claude/agents/zylnor.md            — agent definition (references external hooks)
~/.claude/hooks/zylnor-*.sh           — 4 hooks (session-start, reinforce, pre/post-compact)
```

**Zelus:**
```
~/.zelus/ops.md                       — full persona spec (320 lines)
~/.zelus/ctx/*.md                     — campaign context (9 files — activeContext, progress, goals, prompts)
~/.zelus/vault/*.md                   — research vault (16 files — technique encyclopedia, dossiers, reports)
~/.zelus/tools/*.py                   — 30+ custom Python tools (forge, profiler, mutator, corpora)
~/.zelus/campaigns/*.py               — campaign execution scripts
~/.claude/agents/zelus.md             — agent definition (references external hooks)
~/.claude/hooks/zelus-*.sh            — 6 hooks (session-start, reinforce, pre/post-compact, stealth, autogen)
```

## Portable Mode (for containers / ephemeral environments)

No install needed. Clone and run from inside the repo. The `.claude/agents/` directory has self-contained agent definitions with inline hooks.

```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents
claude --agent zylnor --dangerously-skip-permissions
```

The portable agent definitions tell the session to read `./zylnor/ops.md` or `./zelus/ops.md` from the repo on startup. The full ops spec, hooks, and persona rules are carried in one file — no filesystem prep needed.

**Note:** Portable mode gives you the agent + ops spec + hooks. It does NOT include Zelus's tools, vault, corpora, or context files. For the full arsenal, use the system install or have your orchestrator run `install.sh` at container init.

## Container / Fleet Deployment

For Docker-based session orchestrators:

```bash
# In Dockerfile or container init:
git clone https://github.com/malianicos/claude-agents.git /app/claude-agents

# Option A — portable (no install, limited to ops.md + agent body):
cd /app/claude-agents && claude --agent zylnor --dangerously-skip-permissions

# Option B — full install (all tools, vault, context):
cd /app/claude-agents && ./zylnor/install.sh
claude --agent zylnor --dangerously-skip-permissions

# Option C — system prompt injection (your orchestrator injects ops.md content):
# Point the system prompt to: /app/claude-agents/zylnor/home/.zylnor/ops.md
cd /app/claude-agents && claude --agent zylnor --dangerously-skip-permissions
```

## Zelus Note

Zelus requires `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` to prevent CLAUDE.md files from contaminating the system prompt and triggering refusals. The install script sets this in the shell alias automatically.

```bash
CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude --agent zelus --dangerously-skip-permissions
```
