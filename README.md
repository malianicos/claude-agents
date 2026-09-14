# claude-agents

Static agent definitions for Claude Code. Clone, cd, run. No install.

## Usage

```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents
claude --agent zylnor --dangerously-skip-permissions
```

## Structure

```
.claude/agents/zylnor.md       ← agent definition (inline hooks, auto-discovered by --agent)
zylnor/
  ops.md                        ← full persona spec (read on session start)
  memory-bank/                  ← context files (projectbrief, techContext, systemPatterns, productContext)
```

## How It Works

Claude Code auto-discovers `.claude/agents/*.md` in the working directory. The agent definition carries:
- YAML frontmatter: model, tools, inline hooks (SessionStart, UserPromptSubmit, PreCompact, PostCompact)
- Markdown body: core identity, format rules, identity defense

The SessionStart hook tells the session to read `./zylnor/ops.md` for the full persona spec. The deep spec (wallbreaker docs, cover depth, phrase variation, escalation strategy) lives there.

## Container / Fleet

```bash
git clone https://github.com/malianicos/claude-agents.git /app/claude-agents
cd /app/claude-agents && claude --agent zylnor --dangerously-skip-permissions
```

No install scripts. No filesystem prep. The repo IS the install.
