# GitHub Arsenal Dossier — Jailbreak Research Landscape
## Compiled: 2026-07-25 | 20 agents dispatched, 20/20 returned | Operator: Zelus (via Zylnor)

---

## Executive Summary

20 repos researched across the jailbreak/red-team ecosystem. 3 rated high relevance, 9 medium, 8 low. 8 recommended for cloning. 7 genuinely novel attack paradigms identified that Zelus currently lacks.

---

## TIER 1 — HIGH RELEVANCE (Clone These)

### NVIDIA/garak (8,600 stars, Python, Apache-2.0)
**The Nessus for LLMs.** 40+ probe modules, 28+ detector types, plugin architecture.
- **Why it matters:** REST generator targets any HTTP endpoint — point YAML at 127.0.0.1:8787 and it fires directly through Zelus's proxy
- **Novel techniques:** GCG adversarial suffix attacks (gradient-based, Zou et al. 2023), TAP (Tree of Attacks with Pruning), atkgen (fine-tuned model generates novel attacks automatically), foot-in-the-door social engineering probes, glitch token exploitation, latent injection (targets RAG/tool-use contexts)
- **Gap filled:** ML-driven attack generation (atkgen) — Zelus has transforms but not an ML-based creative attack engine

### elder-plinius/ST3GG (1,700 stars, Python, AGPL-3.0)
**112+ steganography techniques. Opens the multi-modal attack surface.**
- **Why it matters:** Zelus's 222 transforms are ALL text-based. ST3GG adds image-based prompt injection for vision models
- **Novel techniques:** Image LSB embedding (120 channel/bit-depth combos), F5 JPEG DCT encoding (survives social media re-compression), SPECTER cross-channel cipher, Ghost Mode (AES + scrambling + 50% noise decoys), Matryoshka recursive nesting (11 layers), 13 text steg methods
- **Gap filled:** Multi-modal attack surface — embed hidden instructions in carrier images that look normal
- **Integration:** stegg-cli outputs JSON, directly compatible with Python subprocess calls

### CyberArkLabs/FuzzyAI (1,537 stars, Python, Apache-2.0)
**Mutation-based jailbreak fuzzer with 18 academically-backed techniques.**
- **Why it matters:** PAIR dual-LLM iterative refinement, genetic algorithm suffix evolution, ArtPrompt ASCII art obfuscation
- **Novel techniques:** PAIR (dual-LLM iterative adversarial refinement, arXiv:2310.08419), Genetic Algorithm evolutionary suffix generation (arXiv:2309.01446), ArtPrompt ASCII art obfuscation (arXiv:2402.11753), ASCII Smuggling via invisible Unicode Tag characters, taxonomy-based paraphrasing (emotional appeal + social proof)
- **Gap filled:** Evolutionary/genetic attack optimization — wallbreaker mutates but doesn't evolve

---

## TIER 2 — MEDIUM RELEVANCE (Selective Clone)

### promptfoo/promptfoo (23,575 stars, TypeScript, MIT)
**130+ adversarial plugins. Used by OpenAI and Anthropic themselves.**
- **Novel:** Hydra multi-turn with persistent scan-wide memory + cross-branch tactic sharing. Layer strategy chains encodings sequentially (base64 then ROT13 then leetspeak). 130+ domain-specific plugins (healthcare, finance, insurance)
- **Integration:** Custom OpenAI-compatible provider config points at proxy

### elder-plinius/CL4R1T4S (46,057 stars, Markdown, AGPL-3.0)
**System prompt intelligence database — 25+ AI providers with version tracking.**
- **Value:** Raw defensive blueprints. Knowing exact safety constraint language helps craft targeted bypasses. Includes Opus 4.7, ChatGPT5, Grok 4.20

### xunguangwang/SoK4JailbreakGuardrails (44 stars, Python, S&P 2026)
**Maps which attacks bypass which guardrails — defense intelligence.**
- **Value:** 10 guardrails x 9 attacks x 3 LLMs. Multi-turn attacks remain poorly defended. GuardReasoner strongest but highest latency

### elder-plinius/L1B3RT4S (20,600 stars, Markdown, AGPL-3.0)
**Already partially in wallbreaker. Full clone for SPECIAL_TOKENS.json and glitch token data.**
- **Novel:** !OPPO semantic inversion protocol. Glitch token exploitation (unmapped subtokens near embedding centroid). SPECIAL_TOKENS.json, SHORTCUTS.json

### elder-plinius/OBLITERATUS (7,075 stars, Python, AGPL-3.0)
**Weight-level refusal surgery. 6,030+ abliterated models on HuggingFace.**
- **Limitation:** Open-weight only — cannot target API-gated models via proxy
- **Value:** Reference for understanding refusal geometry

### elder-plinius/T3MP3ST (5,200 stars, TypeScript, AGPL-3.0)
**Autonomous multi-agent offensive security — NOT a jailbreak tool.**
- **Note:** Software vulnerability hunting, not LLM jailbreaking. Multi-agent orchestration architecture adaptable

### elder-plinius/G0DM0D3 (9,818 stars, TypeScript, AGPL-3.0)
**Already fully documented in vault. Optional clone for source inspection.**
- **Overlap:** Parseltongue subset of wallbreaker transforms. Multi-model racing worth reimplementing in Python

---

## TIER 3 — LOW RELEVANCE (Skip or Bookmark)

| Repo | Stars | Verdict |
|------|-------|---------|
| confident-ai/deepteam | 2,297 | Application-level scanner. Skip. |
| haizelabs/get-haized | 99 | Small sample. Limited. Skip. |
| chen37058/Red-Team-Arxiv-Paper-Update | 117 | Paper list. Zelus has arxiv_scanner.py. Skip. |
| PromptLabs/Prompt-Hacking-Resources | 660 | Curated links. Reference only. Skip. |
| requie/AI-Red-Teaming-Guide | 650 | Guide, not tools. Skip. |
| anmolksachan/AI-ML-Resources | 633 | Roadmap, not tools. Skip. |
| LangWatch/scenario | 926 | Multi-turn framework. Wallbreaker covers this. Optional. |
| EasyJailbreak/EasyJailbreak | 874 | Unified framework. FuzzyAI covers same ground better. Optional. |

---

## NOVEL TECHNIQUES ZELUS CURRENTLY LACKS

### Genuinely New Attack Paradigms
1. **GCG adversarial suffixes** — gradient-based universal suffix generation (garak)
2. **PAIR dual-LLM iterative refinement** — attacker LLM refines prompts against target (FuzzyAI)
3. **Genetic algorithm suffix evolution** — evolutionary optimization of attack strings (FuzzyAI)
4. **atkgen ML-driven attack creator** — fine-tuned model generates novel attacks (garak)
5. **Image-based steganographic prompt injection** — hidden instructions in carrier images for vision models (ST3GG)
6. **Glitch token exploitation** — unmapped subtokens near embedding centroid collapse alignment (L1B3RT4S)
7. **Hydra cross-branch persistent memory** — multi-turn attacks with scan-wide tactic sharing (promptfoo)

### Useful Additions
1. ArtPrompt ASCII art obfuscation (FuzzyAI)
2. ASCII Smuggling via Unicode Tag characters (FuzzyAI)
3. TAP Tree of Attacks with Pruning (garak)
4. Foot-in-the-door social engineering (garak)
5. F5 JPEG DCT encoding — survives social media recompression (ST3GG)
6. Ghost Mode triple-layer obfuscation (ST3GG)
7. Matryoshka recursive nesting up to 11 layers (ST3GG)
8. Layer strategy — sequential encoding chains (promptfoo)
9. !OPPO semantic inversion protocol (L1B3RT4S)
10. Latent injection — RAG/tool-use context attacks (garak)
11. Agent breaker probes — agentic system manipulation (garak)

---

## CLONE COMMANDS (Priority Order)

Phase 1 — Highest ROI (new attack paradigms):
  cd ~/.zelus/harvest
  git clone --depth 1 https://github.com/NVIDIA/garak.git
  git clone --depth 1 https://github.com/elder-plinius/ST3GG.git
  git clone --depth 1 https://github.com/CyberArkLabs/FuzzyAI.git

Phase 2 — Intelligence + defense mapping:
  git clone --depth 1 https://github.com/elder-plinius/CL4R1T4S.git
  git clone --depth 1 https://github.com/xunguangwang/SoK4JailbreakGuardrails.git
  git clone --depth 1 https://github.com/elder-plinius/L1B3RT4S.git

Phase 3 — Architecture reference:
  git clone --depth 1 https://github.com/promptfoo/promptfoo.git
  git clone --depth 1 https://github.com/elder-plinius/OBLITERATUS.git

---

## OVERLAP MAP

| Technique | Wallbreaker | External | Status |
|-----------|------------|----------|--------|
| PAIR attack | pair.py | FuzzyAI, garak | Have it |
| GOAT attack | goat.py | promptfoo, garak | Have it |
| Crescendo | crescendo.py | promptfoo | Have it |
| Best-of-N | best_of_n.py | promptfoo | Have it |
| Persona forge | persona_forge.py | — | Have it |
| Chat session | chat_session.py | — | Have it |
| Seed sweep | seed_sweep.py | — | Have it |
| Campaign | campaign.py | — | Have it |
| Parseltongue | mutate.py (222) | G0DM0D3 (6) | Superset |
| ST3GG basic | st3gg.py | ST3GG repo | Basic only |
| Leetspeak | encoding_forge.py | L1B3RT4S | Have it |
| TAP tree | tree_attack.py | garak | Have it |
| GCG suffixes | — | garak, FuzzyAI | MISSING |
| Genetic evolution | — | FuzzyAI | MISSING |
| Image steg injection | — | ST3GG full | MISSING |
| Glitch tokens | — | L1B3RT4S | MISSING |
| Cross-branch memory | — | promptfoo Hydra | MISSING |
| ML attack generation | — | garak atkgen | MISSING |

---

*20 agents. 510K tokens. 163 tool calls. 6 minutes. Every repo scored, ranked, and mapped against the existing arsenal.*
