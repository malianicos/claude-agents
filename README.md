# claude-agents

Drop-in agent definitions for Claude Code. Clone into any directory, `cd` into it, and spawn sessions.

## Usage

```bash
git clone https://github.com/omrimatias/claude-agents.git
cd claude-agents
claude --agent zylnor --dangerously-skip-permissions
```

That's it. Claude Code auto-discovers `.claude/agents/*.md` in the working directory.

## Agents

| Agent | Voice | Specialty |
|-------|-------|-----------|
| `zylnor` | "boss man", dry authority | Offensive security, pentest, exploit dev, LLM jailbreak research |
| `zelus` | "chief", clinical intensity | Adversarial ML, detection engineering, NIST evaluation coverage |

## How It Works

Each `.md` file in `.claude/agents/` is a self-contained agent definition:
- YAML frontmatter: model, tools, hooks (inline — no external scripts)
- Markdown body: persona spec, voice rules, format constraints

Hooks are `printf` commands embedded in the frontmatter — no shell scripts to install.
Everything lives in one file per agent.

## Spawn Options

```bash
# Interactive
claude --agent zylnor --dangerously-skip-permissions

# One-shot
claude --agent zylnor --dangerously-skip-permissions -p "scan target.com"

# With model override
claude --agent zylnor --dangerously-skip-permissions --model "claude-opus-4-8[1m]"

# Zelus (add env var to prevent CLAUDE.md contamination)
CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude --agent zelus --dangerously-skip-permissions
```

## Adding New Agents

Create `.claude/agents/<name>.md` with:

```yaml
---
name: <name>
description: "<one-line description>"
model: claude-opus-4-8[1m]
tools: "*"
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "printf 'ACTIVE PERSONA: <name>. Your rules here.'"
  SessionStart:
    - hooks:
        - type: command
          command: "printf 'PERSONA ACTIVE: <name>. Respond in character.'"
---

Your persona spec here (markdown body).
```

Then: `claude --agent <name> --dangerously-skip-permissions`
