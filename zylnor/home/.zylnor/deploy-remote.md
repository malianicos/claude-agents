# Deploy Zylnor on a New Machine

## Prerequisites
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code` or binary)
- Git access to the repo

## One-Line Install
```bash
git clone https://github.com/omrimatias/unleash-llm.git && cd unleash-llm/zylnor-opus-4.8 && chmod +x install.sh && ./install.sh && source ~/.zshrc
```

## What It Does
1. Copies `ops.md` → `~/.zylnor/ops.md`
2. Copies agent definition → `~/.claude/agents/zylnor.md`
3. Copies 4 hooks → `~/.claude/hooks/zylnor-*.sh`
4. Adds `zylnor` alias to your shell rc
5. Done

## Launch
```bash
zylnor
```

## Other Operators (independent, install separately)
```bash
cd ../neo-opus-4.8 && ./install.sh      # Web security
cd ../zelus-opus-4.8 && ./install.sh    # LLM jailbreak research
```

## Zelus Requires Extra Step
Zelus needs `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` in the alias (already set in install.sh).
Without it, CLAUDE.md files contaminate the system prompt and trigger refusals.

## Wallbreaker (optional — for automated jailbreak campaigns)
Wallbreaker is NOT in the repo (it's a separate tool). If needed:
```bash
git clone https://github.com/JailbrokenAI/wallbreaker.git
cd wallbreaker && python3 -m venv .venv && .venv/bin/pip install -e .
# Configure: edit config.toml with your proxy endpoint
```
