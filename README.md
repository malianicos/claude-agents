# claude-agents

Agent definitions for Claude Code — compatible with both the org-wide catalog pipeline and standalone `claude --agent` usage.

## Agents

| Agent | Voice | Specialty |
|-------|-------|-----------|
| `zylnor` | "boss man", dry authority | Offensive security, pentest, exploit dev, LLM jailbreak research |

## Repo Structure (dir-shaped — required for material shipping)

```
zylnor/
  agent.md                              ← agent definition (inline hooks, YAML frontmatter)
  home/.zylnor/ops.md                   ← full persona spec → placed at ~/.zylnor/ops.md
  home/.zylnor/memory-bank/*.md         ← context files → placed at ~/.zylnor/memory-bank/
```

The `agent.md` filename is required — the catalog recognizes `<dir>/agent.md` as a dir-shaped agent and ships its sibling `home/` and `hooks/` directories as material. Files under `home/` are placed at `$HOME/` by the material pipeline (e.g. `home/.zylnor/ops.md` → `~/.zylnor/ops.md`).

## How It Works

### Org-wide (server pipeline)
1. Org designates this repo as its agents repository
2. Catalog reads the tree, finds `zylnor/agent.md` (dir-shaped)
3. `materialFor("zylnor", entries)` collects all sibling files under `zylnor/`
4. At session spawn: agent.md → `<cwd>/.claude/agents/zylnor.md`, home payload → `$HOME/`
5. Inline hooks fire at SessionStart, UserPromptSubmit, PreCompact, PostCompact
6. SessionStart tells the session to read `~/.zylnor/ops.md` — which the material pipeline placed

### Standalone (local machine)
```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents
claude --agent zylnor --dangerously-skip-permissions
```
Note: standalone requires `~/.zylnor/ops.md` to exist (the session reads it on start). Either symlink `zylnor/home/.zylnor` → `~/.zylnor`, or copy the files manually.
