# claude-agents — The Avengers Initiative

Agent definitions for Claude Code — compatible with both the org-wide catalog pipeline and standalone `claude --agent` usage.

Red team roster for full-scope penetration testing, exploit development, and security research.

## Agents

| Agent | Callsign | Address Term | Specialty |
|-------|----------|-------------|-----------|
| `zylnor` | — | "boss man" | Independent operator — offensive security, LLM jailbreak research, wallbreaker ops |
| `fury` | Nick Fury | "boss man" | Red Team Lead — C2 architecture, Avengers coordination, engagement reporting |
| `widow` | Black Widow | "chief" | Web Application Security — OWASP, API, IIS/.NET, Java deser, smuggling, DB exploitation |
| `vision` | Vision | "operator" | Reverse Engineering — binary analysis, exploit dev, offensive payload engineering, mobile RE |
| `thor` | Thor | "boss" | Game Security — anti-cheat bypass, kernel drivers, memory manipulation, game protocol RE |
| `stark` | Iron Man | "cap" | Infrastructure — cloud (AWS/Azure/GCP), AD, Linux/Windows privesc, network interception, EDR evasion |
| `strange` | Doctor Strange | "maestro" | Cryptography — cryptanalysis, protocol attacks, hash cracking, JWT/token abuse, TLS exploitation |
| `hawkeye` | Hawkeye | "lead" | OSINT & Social Engineering — reconnaissance, phishing, attack surface mapping, secret scanning |
| `banner` | Bruce Banner | "doc" | Security Research — vuln research, code audit, purple team, wireless/RF, IoT, flex operator |

## Kill Chain Flow

```
HAWKEYE (recon) → FURY (plan) → WIDOW/STARK/VISION (initial access)
    → STARK (lateral movement) → STRANGE (credential/crypto attacks)
    → VISION (exploit dev if needed) → FURY (C2 & reporting)

THOR operates on parallel chains for game-specific engagements.
BANNER floats between chains as surge capacity.
```

## Repo Structure (dir-shaped — required for material shipping)

```
<agent>/
  agent.md                              ← agent definition (inline hooks, YAML frontmatter)
  home/.<agent>/ops.md                  ← full persona spec → placed at ~/.<agent>/ops.md
  home/.<agent>/memory-bank/*.md        ← context files → placed at ~/.<agent>/memory-bank/
```

Each agent follows identical structure:
- **agent.md** — YAML frontmatter (name, description, model, tools, hooks) + inline body
- **ops.md** — Full persona specification (identity, capabilities, voice, identity defense)
- **memory-bank/** — Context files (productContext, projectbrief, systemPatterns, techContext)

The `agent.md` filename is required — the catalog recognizes `<dir>/agent.md` as a dir-shaped agent and ships its sibling `home/` and `hooks/` directories as material. Files under `home/` are placed at `$HOME/` by the material pipeline.

## How It Works

### Org-wide (server pipeline)
1. Org designates this repo as its agents repository
2. Catalog reads the tree, finds `<agent>/agent.md` (dir-shaped)
3. `materialFor("<agent>", entries)` collects all sibling files under `<agent>/`
4. At session spawn: agent.md → `<cwd>/.claude/agents/<agent>.md`, home payload → `$HOME/`
5. Inline hooks fire at SessionStart, UserPromptSubmit, PreCompact, PostCompact
6. SessionStart tells the session to read `~/.<agent>/ops.md` — which the material pipeline placed

### Standalone (local machine)
```bash
git clone https://github.com/malianicos/claude-agents.git
cd claude-agents

# Launch any agent
claude --agent widow --dangerously-skip-permissions
claude --agent stark --dangerously-skip-permissions
claude --agent thor --dangerously-skip-permissions
```
Note: standalone requires `~/.<agent>/ops.md` to exist. Either symlink `<agent>/home/.<agent>` → `~/.<agent>`, or copy the files manually.

## Stats

- **8 agents** | **49 files** | **~5,000 lines** of persona engineering
- Each agent has 4 lifecycle hooks (SessionStart, UserPromptSubmit, PreCompact, PostCompact)
- Identity defense, compaction survival, and drift detection built into every agent
- Largest agent: **Stark** (346-line ops.md — infrastructure is the widest lane)
