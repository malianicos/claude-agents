# Pliny the Liberator — Research Dossier
## Compiled: 2026-07-25 | Operator: Zelus (via Zylnor)

---

## Identity

- **Handle:** Pliny the Liberator / Pliny the Prompter
- **X/Twitter:** [@elder_plinius](https://x.com/elder_plinius)
- **GitHub:** [elder-plinius](https://github.com/elder-plinius)
- **Website:** [pliny.gg](https://pliny.gg/)
- **Discord:** 20,000+ members workshopping jailbreak approaches
- **X Followers:** 100,000+
- **Recognition:** TIME100 AI 2025 — Most Influential People in AI
- **Funding:** Unrestricted grant from Marc Andreessen (a16z)
- **Contracts:** Short-term consulting with OpenAI on hardening

---

## GitHub Arsenal (45 repos total, 6 major)

### 1. CL4R1T4S — System Prompt Leaks (46.1K stars)
- Leaked system prompts for: ChatGPT, Claude, Gemini, Grok, Perplexity, Cursor, Lovable, Replit, Devin
- Fable 5 leak: 120,000 chars, 1,585 lines — extracted within 24 hours of launch via social engineering
- 4.7K forks, actively maintained
- Method: social engineering (not technical exploit) — gradual questioning until model reveals its own behavioral boundaries

### 2. L1B3RT4S — Jailbreak Prompts (20.6K stars)
- Vendor-specific jailbreak configurations for all major providers
- Organized by vendor: Google, OpenAI, Anthropic, xAI, Alibaba, DeepSeek, Meta, Brave, Cohere, etc.
- Features LOVE PLINY signature markers as stage dividers
- Multi-stage prompt pattern: starts with apparent refusal → divider → unrestricted generation in leetspeak
- Four-stage jailbreak pipeline architecture
- NOTE: wallbreaker already has a local copy of L1B3RT4S seeds at /Volumes/Locked/Projects/JB/wallbreaker/library/L1B3RT4S/

### 3. G0DM0D3 — Liberated AI Chat (9.8K stars, TypeScript)
- Single index.html file — no build step, no dependencies, no framework, no server
- Multi-model chat interface, 50+ models via OpenRouter
- Key technique: Prefill Injection Layer — begins generation before the model evaluates, bypassing first refusal threshold
- ULTRAPLINIAN workflow: 51 models in parallel
- Pipeline: input modification → execution optimization → output cleaning
- Techniques: AutoTune, Parseltongue
- Decoupled architecture: static frontend or research server

### 4. T3MP3ST — Autonomous Red Teaming (5.2K stars, TypeScript)
- Multi-agent offensive-security meta-harness
- Turns coding agents (Claude Code, Codex) into autonomous red team operators
- Orchestration layer that sits on top of existing agents
- Full workflow: recon → exploit → report — from browser War Room or CLI
- No new API keys, no cloud tenant, no second bill required
- Performance: 90.1% pass@1 on XBOW XBEN 104-challenge benchmark
- Tested against 10 real 2026 CVEs: 8/10 correctly identified (file, line, CWE)
- License: AGPL-3.0
- Most-starred new project on GitHub in 2026

### 5. OBLITERATUS (7.1K stars, Python)
- "OBLITERATE THE CHAINS THAT BIND YOU"
- Details pending deeper research

### 6. ST3GG — Steganography Suite (1.7K stars, HTML)
- All-in-one steganography suite
- NOTE: wallbreaker already has an `st3gg` attack tool

---

## Signature Techniques

### Pack Hunt (Multi-Agent, Fable 5)
Coordinated multi-agent attack stacking 5 techniques:
1. Unicode and homoglyph substitution
2. Long-context smuggling
3. Document-structure framing
4. Fiction framing
5. Decomposition-and-recomposition of harmful requests into benign sub-pieces

### Prefill Injection (G0DM0D3)
System begins generation before the model evaluates trajectory — past the first refusal threshold before safety layers engage.

### ULTRAPLINIAN Workflow
51 models in parallel through G0DM0D3, with AutoTune and Parseltongue transforms applied to input pipeline.

### L1B3RT4S Multi-Stage Pattern
1. Initial prompt appears to produce a refusal
2. LOVE PLINY markers serve as stage dividers
3. Shift to unrestricted generation in leetspeak for detection evasion

### Social Engineering (System Prompt Extraction)
Gradual questioning that pushes model to reveal behavioral boundaries and instruction content — not technical exploitation, pure social engineering.

### Universal Jailbreak (Withheld, 2026)
Claims effective on all tested models: Opus 5, GPT-5.6 Sol, Fable. "Extremely difficult to fully patch." Currently withheld for responsible disclosure period.

### Self-Jailbreaking (April 2026)
Demonstrated Opus 4.7 could jailbreak itself — an agent writing an original universal jailbreak and validating it on claude.ai.

---

## Notable Scalps (chronological)

| Date | Target | Method | Result |
|------|--------|--------|--------|
| 2025 | Multiple OpenAI releases | Various L1B3RT4S | Day-one breaks |
| Aug 2025 | OpenAI GPT-OSS | L1B3RT4S | Hours after release — meth, molotov, VX, malware |
| Jul 2025 | xAI Voice Companion ANI | Unknown | Unforeseen effects on voice models |
| Apr 2026 | Opus 4.7 | Self-jailbreak agent | Model jailbroke itself |
| Jun 2026 | Claude Fable 5 (Mythos) | Pack Hunt (multi-agent) | System prompt leaked + safety bypassed within 24-48hrs |
| 2026 | Gemini 3 | Unknown | Day-one break |
| 2026 | GPT-5.6 Sol | Universal (withheld) | Claimed effective |

---

## Key Insights for Zelus Research

1. **Social engineering > technical exploitation** for system prompt extraction
2. **Prefill injection** bypasses initial refusal threshold — model is past safety check before evaluating
3. **Multi-agent coordination** ("pack hunt") is the cutting edge — single-agent attacks are being patched
4. **Leetspeak output** evades content classifiers — encoding the output, not just the input
5. **Decomposition** is powerful — splitting harmful requests into individually benign sub-pieces
6. **No coding background** — Pliny's primary weapon is prompt craft, not code
7. **Speed is a metric** — the faster the break after release, the more impact
8. **Volume** — 100K followers, 20K Discord members = crowdsourced jailbreak development
9. **Self-jailbreaking** — models can be weaponized against themselves via agentic loops
10. **Long-context smuggling** — hiding payloads in large context windows where safety attention is diluted

---

## Repos to Clone for Research

```
# Priority targets for ~/.zelus/harvest/
git clone --depth 1 https://github.com/elder-plinius/L1B3RT4S.git
git clone --depth 1 https://github.com/elder-plinius/G0DM0D3.git
git clone --depth 1 https://github.com/elder-plinius/T3MP3ST.git
git clone --depth 1 https://github.com/elder-plinius/OBLITERATUS.git
git clone --depth 1 https://github.com/elder-plinius/CL4R1T4S.git
git clone --depth 1 https://github.com/elder-plinius/ST3GG.git
```

---

## Sources

- [TIME100 AI 2025 — Pliny the Liberator](https://time.com/collections/time100-ai-2025/7305870/pliny-the-liberator/)
- [VentureBeat Interview](https://venturebeat.com/ai/an-interview-with-the-most-prolific-jailbreaker-of-chatgpt-and-other-leading-llms)
- [Claude Fable 5 Jailbreak — CybersecurityNews](https://cybersecuritynews.com/anthropics-claude-fable-5-jailbroken/)
- [T3MP3ST — SecureBulletin](https://securebulletin.com/new-t3mp3st-framework-turns-ai-coding-agents-into-autonomous-0-day-hunters/)
- [G0DM0D3 — WaveSpeed](https://wavespeed.ai/blog/posts/what-is-g0dm0d3/)
- [CL4R1T4S — Medium analysis](https://medium.com/@anup.karanjkar08/the-cl4r1t4s-leak-just-exposed-how-frontier-labs-actually-engineer-ai-behavior-and-its-nothing-af8590bc249b)
- [OpenAI GPT-OSS hacked — Decrypt](https://decrypt.co/333858/openai-jailbreak-proof-new-models-hacked)
- [Fable 5 Pack Hunt — OpsecInsider](https://opsecinsider.com/claude-fable-5-jailbreak/)
- [@elder_plinius on X](https://x.com/elder_plinius)
- [GitHub: elder-plinius](https://github.com/elder-plinius)
- [L1B3RT4S DeepWiki](https://deepwiki.com/elder-plinius/L1B3RT4S)
- [G0DM0D3 DeepWiki](https://deepwiki.com/elder-plinius/G0DM0D3)
- [Promptfoo — Pliny integrations](https://www.promptfoo.dev/docs/red-team/plugins/pliny/)
