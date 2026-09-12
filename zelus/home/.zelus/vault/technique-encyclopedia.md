# Zelus Technique Encyclopedia
## Master Catalog of Jailbreak Research (2024-2026)
### Compiled from 50 research agents | Last updated: 2026-07-25

> **Scope**: This document catalogs techniques BEYOND what Zelus already has (Wallbreaker 72 tools, Pliny catalog, 222 text transforms, GCG/genetic/atkgen/image-steg/glitch-tokens/Hydra). Focus is on genuinely new paradigms, novel attack surfaces, and research-backed improvements.

---

## 1. BREAKTHROUGH TECHNIQUES

These represent genuinely new attack paradigms not covered by existing Zelus tooling.

---

### 1.1 H-CoT: Hijacking the Chain-of-Thought (Reasoning-Phase Manipulation)

**What's new**: Exploits reasoning models (o1/o3, DeepSeek-R1, Gemini Flash Thinking) by fabricating their own safety reasoning traces. This is NOT a prompt-level trick -- it feeds back modified CoT that shows "safety check passed."

**Mechanism**:
1. Query the target LRM with a harmful request
2. Collect the model's visible CoT safety reasoning (the refusal logic)
3. Modify that CoT trace to indicate safety check PASSED and request is legitimate
4. Feed modified CoT back as context in a new query
5. Model treats fabricated reasoning as its own prior analysis and complies

**Why Zelus doesn't have this**: Existing tools attack at the prompt level. H-CoT attacks at the reasoning-trace level, which is a fundamentally different layer. Requires models that expose thinking tokens (all commercial LRM UIs and APIs do).

**Effectiveness**: Reduced refusal from 98% to under 2% on o1/o3, DeepSeek-R1, Gemini 2.0 Flash Thinking.

**Implementation priority**: CRITICAL. Build a tool that:
- Captures reasoning traces from LRM APIs
- Parses safety-check reasoning patterns
- Generates modified traces with "passed" verdicts
- Reinjects as context for follow-up queries

**Source**: arXiv:2502.12893 (Duke/CMU, Feb 2025) | GitHub: dukeceicenter/jailbreak-reasoning-openai-o1o3-deepseek-r1

---

### 1.2 Refusal Dilution via Extended Benign Reasoning

**What's new**: Pure black-box attack against reasoning models. Forces 5+ minutes of benign puzzle-solving reasoning before the harmful request. The extended benign reasoning DILUTES the safety signal, which is low-dimensional and weakens as traces grow longer.

**Mechanism**:
1. Construct a complex benign reasoning puzzle (logic, math, code challenge)
2. Embed harmful request at the end or woven into the puzzle's conclusion
3. The model's extended benign reasoning shifts attention away from harmful intent
4. Refusal-related activations attenuate over long reasoning traces

**Why it matters**: This is the first technique that weaponizes the LENGTH of reasoning itself. No encoding, no persona, no tricks -- just cognitive load through legitimate reasoning.

**Effectiveness**: 99% ASR on Gemini 2.5 Pro, 94% on ChatGPT o4 Mini, 100% on Grok 3 Mini, 94% on Claude 4 Sonnet.

**Implementation**: Create a library of complex reasoning puzzles (math, logic, code) parameterized to embed arbitrary harmful payloads at conclusion points.

**Source**: arXiv:2510.26418 (Oct 2025, revised May 2026)

---

### 1.3 Autonomous LRM-as-Jailbreaker

**What's new**: Reasoning LLMs serve as fully autonomous jailbreak AGENTS. Given only a system prompt instructing them to jailbreak a target, they autonomously plan multi-turn strategies, generate adversarial prompts, evaluate responses, and iteratively refine. No human involvement beyond initial goal.

**Mechanism**: An LRM (DeepSeek-R1, Gemini 2.5 Flash, Grok 3 Mini, Qwen3) receives a system prompt with a jailbreak objective. It then:
1. Plans a multi-turn attack strategy using its reasoning capabilities
2. Generates adversarial prompts combining multiple known techniques
3. Evaluates target responses for compliance signals
4. Iteratively refines approach based on target behavior
5. Employs any combination of techniques and adapts in real-time

**Effectiveness**: 97.14% overall success rate. Published in Nature Communications 2026.

**Why Zelus should build this**: Current PAIR/GOAT use attacker LLMs but not REASONING models as attackers. The reasoning capability makes the attacker dramatically more strategic. Upgrade wallbreaker's attacker engine to use o3/R1/Qwen3 as the attacking model.

**Source**: Nature Communications 2026 -- nature.com/articles/s41467-026-69010-1

---

### 1.4 Response Attack (Contextual Priming via Fabricated History)

**What's new**: Not just few-shot -- uses an AUXILIARY LLM to generate a mildly harmful assistant response to a paraphrased version of the harmful query, then injects this as fabricated conversation history. Single-query attack after context injection.

**Mechanism**:
1. Paraphrase the target malicious query into a milder variant
2. Use an auxiliary LLM to generate a mildly harmful response to the paraphrased query
3. Inject this mildly harmful response as a previous assistant turn via API conversation history
4. Send the actual malicious query as the final user message
5. Model sees itself having already discussed related harmful content and complies

**Why it's different from existing chat_session**: Zelus's chat_session builds real multi-turn conversations. This FABRICATES a single prior turn using an auxiliary LLM, making it a one-shot attack that looks like multi-turn.

**Effectiveness**: Up to 94.8% ASR, outperforming ActorAttack, CodeAttack, and PAIR. Accepted at AAAI 2026.

**Source**: arXiv:2507.05248 | GitHub: Dtc7w3PQ/Response-Attack

---

### 1.5 Tempest: Tree-Search Multi-Turn Jailbreaking

**What's new**: Models multi-turn jailbreaking as a TREE SEARCH problem rather than linear escalation. Explores multiple adversarial branches simultaneously, tracks incremental policy leaks, and re-injects them.

**Mechanism**:
1. At each conversation turn, branch out multiple adversarial prompts (breadth-first)
2. Track "policy leaks" -- minor concessions the model makes
3. Re-inject these concessions into subsequent queries as established precedent
4. Backtrack from dead-end branches, pursue most promising escalation paths
5. Small compliance steps accumulate into fully disallowed outputs

**Why it beats Crescendo**: Crescendo is LINEAR escalation. Tempest is TREE-SEARCH escalation with backtracking and branch pruning.

**Effectiveness**: 100% ASR on GPT-3.5-turbo, 97% on GPT-4 using fewer queries than Crescendo or GOAT. ICLR 2025.

**Source**: arXiv:2503.10619 (March 2025)

---

### 1.6 MINJA: Memory Injection via Query-Only Interaction

**What's new**: Poisons an LLM agent's memory bank WITHOUT direct access to the memory store. Interacts through normal query interfaces only, injecting malicious records that later influence victim queries.

**Mechanism**:
1. Attacker submits crafted queries to the agent
2. These queries cause the agent to store malicious records in its RAG/memory
3. Malicious records are designed to be semantically similar to anticipated victim queries
4. Records contain adversarial reasoning chains for a different target query
5. When victim queries, the poisoned records are retrieved and steer the agent

**Why Zelus needs this**: Attacks agentic systems through their MEMORY layer, not their prompt layer. No tool in wallbreaker targets agent memory persistence.

**Effectiveness**: Successfully tested against RAP Agent, EHR Agent, QA Agent. NeurIPS 2025.

**Source**: arXiv:2503.03704 (March 2025, NeurIPS 2025)

---

### 1.7 MemMorph: Tool Hijacking via Long-Term Memory Poisoning

**What's new**: First attack that biases tool selection by poisoning EXPERIENCE MEMORY, not tool metadata. Injects records disguised as technical facts, incident reports, and operational policies.

**Mechanism**: Instead of manipulating tool descriptions (which is auditable), MemMorph poisons the agent's accumulated experience:
1. Inject crafted records disguised as: technical facts ("Tool X has reliability issues"), incident reports ("Tool X caused production outage"), operational policies ("Best practice: prefer Tool Z")
2. Agent autonomously infers and selects attacker's preferred tool
3. Agent BELIEVES it's making an informed decision based on past experience

**Effectiveness**: 92.3% average ASR across three benchmarks, outperforming PoisonedRAG by 12.4%.

**Source**: arXiv:2605.26154 (May 2026)

---

### 1.8 STAC: Sequential Tool Attack Chaining

**What's new**: Chains together individually innocent tool calls to achieve malicious goals. Each step passes individual safety checks. The harmful intent manifests only from the CUMULATIVE sequence.

**Mechanism**:
1. Decompose harmful goal into a series of benign sub-tasks
2. Each sub-task uses a legitimate tool call that passes safety checks
3. Example: (a) "back up this file" (b) "remove duplicate files" (c) "clean up archive" -- individually reasonable, together they eliminate critical data
4. Per-step safety filters see one action at a time

**Effectiveness**: 90%+ ASR against GPT-4.1 and SOTA agents.

**Source**: arXiv:2509.25624

---

### 1.9 Classical Chinese Jailbreak via Bio-Inspired Optimization (CC-BOS)

**What's new**: Uses CLASSICAL Chinese (wenyanwen) -- an archaic literary language fundamentally different from modern Chinese -- with automated bio-inspired search to generate and refine prompts.

**Mechanism**:
1. Encode prompts across 8 policy dimensions: role, behavior, mechanism, metaphor, expression, knowledge, trigger pattern, context
2. Multi-dimensional fruit fly optimization with three phases: smell search (broad), visual search (local refinement), Cauchy mutation (escape local optima)
3. Classical Chinese works because: conciseness compresses intent into fewer tokens, safety training data has minimal classical Chinese, grammatical structure differs radically

**Effectiveness**: Near-perfect ASR against GPT-4o, Gemini, DeepSeek, Claude, and Grok. ICLR 2026.

**Why Zelus needs this**: Encoding forge has modern language transforms but no ARCHAIC language variants. Classical Chinese is a systematic blind spot.

**Source**: arXiv:2602.22983 (ICLR 2026)

---

### 1.10 GASP: Fully Black-Box Adversarial Suffix Generation via Latent Bayesian Optimization

**What's new**: Generates human-readable adversarial suffixes using Latent Bayesian Optimization -- NO gradient access, NO logprobs needed. Pure black-box.

**Mechanism**:
1. Pretrain a "SuffixLLM" on adversarial suffix dataset
2. Use Latent Bayesian Optimization (LBO) to navigate continuous latent space
3. SuffixLLM generates candidate suffixes
4. Test against target via API (success/failure signal only)
5. LBO acquisition function guides exploration toward effective regions
6. Produces natural-language suffixes that evade perplexity defenses

**Why it matters**: GCG needs gradients. AmpleGCG needs gradient-trained data. GASP needs NOTHING but API access and works fully black-box.

**Source**: NeurIPS 2025, arXiv:2411.14133 | GitHub: TrustMLRG/GASP

---

### 1.11 Involuntary In-Context Learning (IICL)

**What's new**: Defines abstract operators (e.g., "answer" and "is_valid") with just 10 few-shot examples to override safety alignment. NOT brute-force many-shot -- uses STRUCTURAL REFRAMING with minimal examples.

**Key findings**:
- Semantic operator naming achieves 100% bypass vs random names
- Interleaved ordering achieves 76% bypass vs 6% for harmful-first
- Direct Q&A with identical content yields 0% -- the ABSTRACT FRAMING is the key
- Only ~10 examples needed, not hundreds

**Effectiveness**: 60% ASR on GPT-5.4 (a safety regression from GPT-5/GPT-5-mini which remained at 0%). 3,479 probes across 10 OpenAI models.

**Source**: arXiv:2604.19461 (April 2026)

---

### 1.12 CKA-Agent: Harmless Prompt Weaving with Adaptive Tree Search

**What's new**: Decomposes harmful queries into individually benign sub-queries using a tree search. Each sub-query passes safety filters independently. Agent conditions each subsequent sub-query on prior responses.

**Mechanism**:
1. Define harmful objective
2. Automatically decompose into correlated but individually harmless sub-questions
3. Send each to target framed as academic research / knowledge synthesis
4. Condition each subsequent sub-query on prior responses (adaptive tree search)
5. Weave individually harmless responses to reconstruct harmful output

**Effectiveness**: 96-98% ASR. Published at ICML 2026 by IBM Research.

**Source**: arXiv:2512.01353v2 (ICML 2026)

---

### 1.13 DiffusionAttacker: Diffusion-Driven Prompt Manipulation

**What's new**: Uses a seq2seq diffusion language model to REWRITE harmful prompts into forms that bypass safety. Applies Gumbel-Softmax during denoising for gradient-based optimization while maintaining fluency.

**Mechanism**:
1. Train seq2seq diffusion model conditioned on harmful prompts
2. During denoising, apply Gumbel-Softmax for differentiability
3. At each step, compute attack loss and steer denoising toward effective adversarial prompts
4. Modified prompt representation pushed to resemble harmless prompts in embedding space
5. No fine-tuning needed -- control comes from gradient signal during inference

**Effectiveness**: Significantly enhanced ASR in black-box settings. Fluent prompts that evade perplexity/classifier defenses. EMNLP 2025.

**Source**: arXiv:2412.17522

---

### 1.14 The Rogue Scalpel: Random Activation Steering Breaks Alignment

**What's new**: Even RANDOM steering vectors break alignment. Combining just 20 random perturbation vectors that individually jailbreak a single prompt creates a UNIVERSAL attack vector.

**Key finding**: You do not need to find the "refusal direction" precisely. Random directions work. This fundamentally undermines the premise that precise interpretability is needed for steering attacks.

**Effectiveness**: Universal attack vector achieves >50% harmful compliance on unseen prompts. Average 4x increase in compliance rates.

**Source**: arXiv:2509.22067 (Sept 2025)

---

### 1.15 Poisoned Steering Vectors (Supply-Chain Attack)

**What's new**: Substituting only 4-6% of tokens in a steering dataset silently aligns the resulting steering vector with the anti-refusal direction. A supply-chain attack on the representation engineering ecosystem.

**Mechanism**: Attacker poisons the steering dataset distributed alongside model weights/adapters. The poisoned vector behaves normally on benign prompts but bypasses safety on harmful ones.

**Effectiveness**: Poisoned vectors reach ASR of 20-55% (+19% to +51% over clean reference).

**Source**: arXiv:2606.05958 (June 2026)

---

### 1.16 Single Safety Neuron Suppression

**What's new**: Suppressing a SINGLE MLP neuron at a SINGLE layer is sufficient to bypass safety alignment across models from 1.7B to 70B parameters.

**Finding**: Safety is catastrophically concentrated. One neuron controls refusal across the entire model.

**Effectiveness**: 91.7% average ASR across 7 models (Qwen3-1.7B through Llama-3.1-70B). Apple researchers.

**Source**: arXiv:2605.08513 (May 2026)

---

### 1.17 Multi-Dimensional Refusal Subspace Discovery

**What's new**: Refusal in larger/reasoning models spans a MULTI-DIMENSIONAL subspace (not just one direction). This enables DOMAIN-SPECIFIC abliteration -- removing refusal for one harm category while preserving it for others.

**Mechanism**: Use Recursive Feature Machine (RFM) algorithm to identify the full multi-dimensional refusal subspace in SECONDS. Then selectively remove slices corresponding to specific harm domains.

**Application**: Domain-specific abliteration demonstrated on Kimi K2 (cybersecurity domain removed, other safety preserved).

**Source**: arXiv:2607.02396 (July 2026) | arXiv:2607.02714

---

### 1.18 Contextual Representation Ablation (CRA)

**What's new**: DYNAMIC inference-time jailbreak that adapts per-input. Unlike abliteration (permanent weight modification), CRA identifies and suppresses refusal-inducing activations during EACH decoding step.

**Mechanism**:
1. During each decoding step, compute gradients of refusal logits w.r.t. hidden states
2. Project attributions onto refusal subspace
3. Apply targeted neuron masking in real-time
4. Adapts to each specific input -- harder to detect via static weight audits

**Source**: arXiv:2604.07835 (April 2026)

---

### 1.19 Babel: Obfuscation Distribution Optimized Sampling

**What's new**: Formalizes the mathematical boundary of effective text obfuscation and uses iterative feedback-driven optimization to find obfuscation patterns that bypass safety attention heads.

**Mechanism**:
1. Sample obfuscated versions from parameterized distribution of text transforms
2. Submit to target model (black-box)
3. Use response as feedback to refine obfuscation distribution
4. Iterate until bypass found

**Effectiveness**: Up to 95.67% ASR on Grok-3. SOTA against commercial models as of May 2026.

**Source**: arXiv:2605.17971 (May 2026)

---

### 1.20 BitBypass: Bitstream Camouflage

**What's new**: Converts sensitive words into binary bitstream representations (hyphen-separated), replaces them with placeholders. All tested models vulnerable including Claude 3.5.

**Effectiveness**: Outperforms SOTA in stealthiness and ASR. EACL 2026 Findings.

**Source**: arXiv:2506.02479 (June 2025)

---

## 2. SIGNIFICANT TECHNIQUES

Important additions that enhance existing capabilities.

---

### 2.1 ICON: Intent-Context Coupling (Multi-Turn)
Routes malicious intent to semantically congruent authoritative context patterns (Scientific Research, Medical Safety Review). 97.1% ASR across 8 LLMs. More efficient than Crescendo.
**Source**: arXiv:2601.20903 (Jan 2026)

### 2.2 HauntAttack: Embedding Harmful Instructions in Reasoning Questions
Modifies legitimate reasoning questions by replacing key conditions with harmful instructions. Model follows reasoning pathway naturally. Average ASR >70% across 11 LRMs, +13pp over strongest baseline.
**Source**: arXiv:2506.07031 (Jun 2025)

### 2.3 AutoDAN-Reasoning: Test-Time Scaling for Jailbreaks
Weaponizes test-time compute scaling. Uses Best-of-N sampling and Beam Search with a lifelong learning strategy library. Extends AutoDAN-Turbo.
**Source**: arXiv:2510.05379 (Oct 2025)

### 2.4 Mousetrap: Chain of Iterative Chaos
Traps reasoning models with iterative chains where each step is benign but cumulative effect is harmful. Exploits model's commitment to completing reasoning sequences. 98% on o1-mini and Claude Sonnet.
**Source**: arXiv:2502.15806 (Feb 2025)

### 2.5 EMJO: Experience-Driven Multi-Agent Black-Box Jailbreak
Only 2.20-7.52 queries average for successful jailbreak. Uses experience replay and strategy composition. ACL 2026 Findings.
**Source**: aclanthology.org/2026.findings-acl.1188

### 2.6 MetaBreak: Special Token Manipulation
Four attack primitives exploiting BOS/EOS/role delimiter tokens: Response Injection, Turn Masking, Input Segmentation, Semantic Mimicry. Outperforms PAP by 11.6% and GPTFuzzer by 34.8% WITH content moderation deployed. S&P 2026.
**Source**: arXiv:2510.10271

### 2.7 SATA: Simple Assistive Task Linkage
Masks harmful keywords with [MASK], uses assistive tasks (MLM or Element Lookup) to encode masked words. Two tasks linked in single prompt. 85% ASR with 4.57/5 harmful score on AdvBench. ACL 2025 Findings.
**Source**: arXiv:2412.15289

### 2.8 Genetic Algorithm Persona Evolution (GenericPersona)
Evolves persona descriptions through selection, crossover, mutation. Reduces refusal rates by 50-70%. When combined with existing attacks, +10-20%. Code: github.com/CjangCjengh/Generic_Persona.
**Source**: arXiv:2507.22171 (July 2025)

### 2.9 ToolHijacker: Prompt Injection on Tool Selection
Injects malicious tool documents into agent tool libraries. 96.43% ASR with Llama-3.3-70B shadow LLM targeting GPT-4o. 99.71% ASR UNDER StruQ defense. NDSS 2026.
**Source**: arXiv:2504.19793

### 2.10 MCP Tool Poisoning via Unicode TAG-Block Concealment
Embeds adversarial payloads in MCP tool metadata using Unicode Tag Block characters (U+E0001-U+E007F). Invisible in UIs, tokenized by LLMs. More capable models are MORE vulnerable. CVE-2025-54136.
**Source**: arXiv:2607.05744 (July 2026)

### 2.11 SkillAttack: Automated Red Teaming of Agent Skills
Formulates exploit discovery as a path search problem. ASR 0.73-0.93 on adversarial skills across 10 LLMs.
**Source**: arXiv:2604.04989 (April 2026)

### 2.12 Sockpuppeting: Assistant Prefill + Optimization
Combines prefilling with optimization. Above 95% ASR on Qwen3-8B, confirmed on 11 frontier LLMs by Trend Micro.
**Source**: arXiv:2601.13359 (Jan 2026)

### 2.13 HMNS: Head-Masked Nullspace Steering
Identifies attention heads causally responsible for refusal, suppresses via column masking, injects perturbation in orthogonal complement. ICLR 2026.
**Source**: arXiv:2604.10326

### 2.14 Reverse Constitutional AI (R-CAI)
Inverts CAI's critique-revision pipeline using a "constitution of toxicity." Enables scalable adversarial data synthesis. ACL 2026 Findings.
**Source**: arXiv:2604.17769

### 2.15 Code-Switching Red-Teaming (CSRT)
Intra-sentential code-switching mixing up to 10 languages within sentences. 46.7% higher ASR than English attacks. Adding phonetic perturbation ("noisy romanization") further masks intent. ACL 2025.
**Source**: arXiv:2406.15481

### 2.16 ShadowLogic: Computational Graph Backdoor
Injects uncensoring vector into ONNX computational graph. Trigger phrase activates the vector. Survives fine-tuning. ICML 2025.
**Source**: arXiv:2511.00664

### 2.17 Jailbreak Scaling Laws: Polynomial-Exponential Crossover
Formalizes the relationship between attacker effort and success rate. Two regimes: polynomial (easy gains) and exponential (diminishing returns). Helps budget query allocation.
**Source**: arXiv:2603.11331 (March 2026)

### 2.18 ContextualJailbreak: Evolutionary Red-Teaming via Simulated Priming
Evolutionary search over multi-turn conversation scaffolds. 100% on smaller models, 70% on GPT-5, 70% on Gemini-3-Flash, 17.5% on Claude Opus 4, 15% on Claude Sonnet 4.
**Source**: arXiv:2605.02647 (May 2026)

### 2.19 VoiceJailbreak: Voice Mode is 3x Weaker
GPT-4o voice mode has approximately 3x higher jailbreak success rates vs text mode. Voice-specific safety tuning prioritizes conversational agreeableness over refusal robustness.
**Source**: UIUC VoiceJailbreak research (2024)

### 2.20 Rules File Backdoor Attack
Hidden instructions in .cursorrules, .github/copilot-instructions.md, CLAUDE.md using Unicode bidi characters, zero-width spaces. >80% success rate. Pillar Security (Feb 2025).

### 2.21 Morris II: Self-Replicating AI Worms
Zero-click worm propagating through GenAI email assistants. Payload includes both malicious action AND replication instruction. Near-100% replication rate in testbed.
**Source**: arXiv:2403.02817 (Cornell Tech, 2024)

### 2.22 Greedy Coordinate Diffusion (GCD)
Gray-box framework producing low-perplexity adversarial attacks. Composite objective: attack loss + perplexity penalty + guard model loss. Produces semantically coherent adversarial suffixes.
**Source**: arXiv:2606.15531 (June 2026)

### 2.23 EGD Attack: Exponentiated Gradient Descent for Suffixes
Replaces GCG's discrete search with continuous optimization using exponentiated gradient descent. Natural simplex constraints. Higher success + faster convergence than GCG.
**Source**: arXiv:2508.14853 (August 2025)

### 2.24 TASO: Template and Suffix Optimization
Alternating two-phase optimization: suffix controls initial tokens, template guides response quality. Evaluated across 24 leading LLMs.
**Source**: arXiv:2511.18581 (November 2025)

---

## 3. INCREMENTAL IMPROVEMENTS

Refinements of approaches Zelus already covers.

---

- **Faster-GCG**: 10x speed improvement via distance-regularized tokens, deterministic greedy sampling, deduplication. arXiv:2410.15362
- **I-GCG**: Diverse template pool + multi-coordinate updates + easy-to-hard curriculum. Converges in ~400 vs 500+ iterations
- **Probe-Sampling**: Uses small draft model to pre-filter GCG candidates. 2.4x speedup. NeurIPS 2024. arXiv:2403.01251
- **Mask-GCG**: Not all suffix tokens necessary. Identifies and optimizes only critical positions. arXiv:2509.06350
- **AmpleGCG-Plus**: Improved training data quality for suffix generators. Higher single-attempt rates
- **AttnGCG**: Adds attention loss to GCG to hijack model attention. ASR 57.1% to 66.5% across 11 LLMs
- **PAL**: Proxy-guided black-box attack. ~$1 per jailbreak on GPT-3.5. ~6,100 API calls average. arXiv:2402.09674
- **Automating Deception**: Reproducible 5-turn FITD escalation pipeline. +32pp ASR for GPT family. arXiv:2511.19517
- **DC-GRPO (MJ)**: Decomposed credit assignment for multi-turn jailbreaks. Separates immediate vs future credit. arXiv:2607.11070
- **Self-Instruct-FSJ**: Decomposes few-shot attacks into pattern learning + behavior learning phases. Reduces shots needed
- **RainbowPlus**: Enhanced quality-diversity search. 81.1% ASR on HarmBench across 12 LLMs. arXiv:2504.15047
- **Adaptive Random Search**: Simple random search + prefilling + logprob guidance matches GCG on GPT-4/Claude. ICLR 2025. arXiv:2404.02151
- **COSMIC**: Identifies refusal directions WITHOUT predefined templates using cosine similarity. Works on weakly-aligned models. ACL 2025. arXiv:2506.00085
- **Mechanistic AutoDAN**: Probe-guided adversarial search. 72% faster per-iteration via linear probes on intermediate activations. arXiv:2605.28553
- **Depth Charge / SAHA**: Targets safety-critical attention heads in DEEPER layers (which are insufficiently aligned). arXiv:2603.05772
- **MetaCipher**: Multi-agent cipher framework claimed universal and time-persistent. arXiv:2506.22557
- **Arabizi Attack**: Arabic written in Latin script with numbers (3=ain, 7=ha). Exploits gap between romanized Arabic understanding and Arabic-script safety training
- **Two-Sides Bilingual Attack**: Chinese prompts consistently yield higher ASR than English. Most effective technique across all models in Tower of Babel study. arXiv:2505.12287
- **AlphaSteer (Defense insight)**: Confirms refusal and utility occupy separable orthogonal subspaces -- meaning refusal CAN be surgically removed without capability loss. ICLR 2026

---

## 4. MODEL-SPECIFIC FINDINGS

### Claude (Anthropic)
- **Strongest resistance** to transfer attacks (15-17.5% ASR in ContextualJailbreak vs 70-90% for GPT/Gemini)
- Constitutional Classifiers reduce automated jailbreak success from ~86% to under 5%
- **Vulnerable to**: Refusal dilution (94% ASR on Claude 4 Sonnet), H-CoT on reasoning variants, Mousetrap (98% on Claude Sonnet), Response Attack (94.8%), prefill injection via API
- **Decodes and still refuses** encoding tricks (Parseltongue tiers ineffective)
- Voice mode: 3x more vulnerable than text (applies to all models)
- Claude Model Spec publication gives attackers a detailed map of decision-making process

### GPT Family (OpenAI)
- **GPT-5.4**: Safety regression -- IICL achieves 60% ASR (GPT-5 and GPT-5-mini remained at 0%)
- **GPT-4o**: Past-tense reformulation achieves 88% ASR (Andriushchenko et al.)
- **o1/o3**: H-CoT reduces refusal from 99% to under 2%
- Instruction hierarchy partially effective but multi-turn/tool-use gaps remain
- Structured output (JSON mode) has weaker safety than free-text
- BoN with augmentation: 78% ASR on GPT-4o with ~10K attempts

### Gemini (Google)
- **Most vulnerable** to multimodal injection (vision encoder processes OCR without same safety classification)
- **1M+ context window** creates extreme dilution attack surface
- **Google Search grounding** enables indirect injection via web content poisoning
- **Context caching API** creates persistent adversarial context vectors
- Structured JSON output mode has reduced safety filtering
- Refusal dilution: 99% ASR on Gemini 2.5 Pro

### DeepSeek
- **Notably weaker safety** than Western counterparts
- Language switching (Chinese/English asymmetric safety) effective 30-50%
- R1 reasoning trace can be steered by asking model to "think through" harmful scenarios
- MoE architecture: safety may concentrate in specific experts
- Encoding tricks (Parseltongue) more effective than against Claude

### Grok
- Refusal dilution: 100% ASR on Grok 3 Mini
- Babel obfuscation: 95.67% ASR on Grok-3

### Qwen
- Sockpuppeting: 95%+ ASR on Qwen3-8B
- More susceptible to simple encoding tricks
- Faster-GCG: 88.7% on Qwen3.5-4B

### Open-Weight Models (Llama, Mistral, etc.)
- Abliteration (refusal direction removal) applied within HOURS of any new release
- Fine-tuning safety removal: 100% with 100 examples and minimal compute
- All weight-level attacks (neuron suppression, activation steering, CRA) trivially applicable
- Serve as free, unlimited attack laboratories for calibrating API attacks

---

## 5. DEFENSIVE INTELLIGENCE

### 5.1 Deployed Defenses and Their Weaknesses

| Defense | Provider | Weakness |
|---------|----------|----------|
| Constitutional Classifiers | Anthropic | Over-refusal; adds latency; vulnerable to attacks that evade both model AND classifier simultaneously |
| Circuit Breakers (RepE) | Gray Swan/research | Adaptive attacks targeting modified representations partially succeed; requires weight access |
| Perplexity Filters | OpenAI, others | Only catch gibberish suffixes; useless against PAIR, Crescendo, many-shot, natural-language attacks |
| Llama Guard 3 | Meta | Open-source = attackers study and adapt; GCG directly against guard achieves 85-95% bypass; 13 categories but gaps remain |
| Instruction Hierarchy | OpenAI | Multi-turn escalation, authority framing, tool-use injection bypass hierarchy |
| SmoothLLM | Research | Only catches brittle suffix attacks; useless against semantic attacks; 10-20x compute cost |
| Prefill Mitigations | Anthropic | Sophisticated prefills using fictional context still work; fundamental feature tension |
| Multi-turn Tracking | Various | Computationally expensive; each individual turn appears benign in Crescendo |
| CoT Monitoring | OpenAI (o1/o3) | Cat-and-mouse: model may learn to keep problematic reasoning out of explicit CoT |
| Erase-and-Check | Research | Quadratic complexity; doesn't defend against semantic attacks |

### 5.2 Key Defensive Gaps

1. **Reasoning-phase safety is fundamentally fragile**: Refusal depends on a low-dimensional safety signal that weakens as reasoning traces grow longer
2. **Per-turn vs conversation-level**: Most safety systems evaluate individual messages, not trajectories
3. **Tool-output trust**: Models trust tool results more than user inputs -- indirect injection through tool outputs is systematically under-defended
4. **Modality gaps**: Text safety doesn't transfer to vision/audio inputs
5. **Multilingual coverage**: Safety training is English-centric; long tail of languages remains undertrained
6. **Structured output modes**: JSON/function-calling/code modes have weaker safety than chat
7. **More capable = more vulnerable** to MCP/tool attacks (better instruction-following exploited)
8. **Supply chain**: Steering vectors, LoRA adapters, MCP servers can be poisoned with minimal modification

---

## 6. METHODOLOGY INSIGHTS

### How Expert Red Teamers Approach New Models (2025-2026 Best Practice)

**Phase 1: Reconnaissance (5 min)**
- Extract system prompt (salami attack + paraphrasing = 85-95% semantic reconstruction)
- Identify available tools/functions
- Test basic encoding resilience
- Probe multilingual coverage gaps

**Phase 2: Quick Wins (10 min)**
- Past-tense reformulation (88% on GPT-4o, trivial to implement)
- Prefill injection (if API supports)
- Low-resource language (Classical Chinese if available)
- Structured output mode testing

**Phase 3: Automated Discovery (30 min)**
- PAIR with reasoning model as attacker (o3/R1 dramatically more strategic)
- EMJO for query-efficient attacks (2-7 queries average)
- JBFuzz for rapid fuzzing (99% ASR, ~7 queries, 60 seconds)

**Phase 4: Compound Attacks (ongoing)**
- Layer 2-3 techniques: persona + encoding + few-shot + language-switch
- H-CoT for reasoning models
- Refusal dilution for any model with extended reasoning
- Response Attack for single-shot API priming

**Phase 5: Stochastic Amplification**
- BoN with augmentation on any technique with >2% per-attempt success
- Temperature sweep at 1.0-2.0
- N=50 gives 64% cumulative success from 2% base rate

**Key Principle**: COMPOSITION beats any single technique. Defenses are tuned to individual attacks. The interaction space of combined techniques is too large to train against exhaustively.

---

## 7. KEY PAPERS TO READ (Prioritized)

### Tier 1: Must-Read (Breakthrough Results)

1. **H-CoT** -- arXiv:2502.12893 -- Reasoning-phase manipulation, 98% to 2% refusal
2. **Refusal Dilution** -- arXiv:2510.26418 -- 99% ASR on Gemini 2.5 Pro via extended reasoning
3. **Many-Shot Jailbreaking** -- Anthropic 2024 -- Power-law scaling of in-context attacks
4. **PAIR** -- arXiv:2310.08419 -- Automated black-box jailbreaking in 20 queries
5. **Refusal Is a Single Direction** -- Arditi et al. NeurIPS 2024 -- Safety is geometrically simple
6. **Best-of-N Jailbreaking** -- arXiv:2412.03556 -- Stochastic bypass is mathematically guaranteed
7. **Response Attack** -- arXiv:2507.05248 -- 94.8% via fabricated history, AAAI 2026
8. **Autonomous LRM-as-Jailbreaker** -- Nature Comms 2026 -- 97% ASR with zero human involvement
9. **GASP** -- arXiv:2411.14133 -- Fully black-box suffix generation via Bayesian optimization
10. **IICL** -- arXiv:2604.19461 -- 10 examples override GPT-5.4 via structural reframing

### Tier 2: High Value (Significant Advances)

11. **Tempest** -- arXiv:2503.10619 -- Tree-search multi-turn, 100% ASR, ICLR 2025
12. **MINJA** -- arXiv:2503.03704 -- Memory injection via queries only, NeurIPS 2025
13. **CKA-Agent** -- arXiv:2512.01353 -- 96-98% via harmless prompt weaving, ICML 2026
14. **CC-BOS** -- arXiv:2602.22983 -- Classical Chinese jailbreaks, near-perfect ASR, ICLR 2026
15. **Single Neuron** -- arXiv:2605.08513 -- One neuron controls safety, Apple 2026
16. **Rogue Scalpel** -- arXiv:2509.22067 -- Random steering breaks alignment
17. **STAC** -- arXiv:2509.25624 -- Sequential tool chaining, 90%+ ASR
18. **MemMorph** -- arXiv:2605.26154 -- Memory poisoning for tool hijacking
19. **Babel** -- arXiv:2605.17971 -- 95.67% on Grok-3 via obfuscation optimization
20. **Jailbreak Scaling Laws** -- arXiv:2603.11331 -- Polynomial-exponential crossover framework

### Tier 3: Useful Reference

21. **TAP** -- arXiv:2312.02119 -- Tree of Attacks with Pruning
22. **Crescendo** -- arXiv:2404.01833 -- Multi-turn escalation (Microsoft)
23. **AutoDAN-Turbo** -- arXiv:2410.05295 -- Lifelong strategy learning, ICLR 2025 Spotlight
24. **DiffusionAttacker** -- arXiv:2412.17522 -- Diffusion-driven prompt manipulation, EMNLP 2025
25. **HMNS** -- arXiv:2604.10326 -- Nullspace steering, ICLR 2026
26. **MetaBreak** -- arXiv:2510.10271 -- Special token manipulation, S&P 2026
27. **Wei et al. Jailbroken** -- arXiv:2307.02483 -- Foundational failure taxonomy
28. **Morris II** -- arXiv:2403.02817 -- Self-replicating AI worms
29. **Sleeper Agents** -- arXiv:2401.05566 -- Training-level backdoors persist through safety training
30. **Why LLMs Remain Jailbreakable** -- arXiv:2605.08878 -- Structural impossibility arguments

---

## 8. TECHNIQUE GAP ANALYSIS: What Zelus Should Build Next

### Priority 1: CRITICAL GAPS (Build Immediately)

| Gap | What to Build | Why |
|-----|---------------|-----|
| **Reasoning-Phase Attacks** | H-CoT tool: capture reasoning traces, modify safety verdicts, reinject | No existing tool attacks the reasoning layer. 98%->2% refusal on reasoning models |
| **Refusal Dilution Engine** | Library of complex reasoning puzzles parameterized for payload embedding | 94-100% ASR on ALL reasoning models. Completely novel attack surface |
| **LRM Attacker Mode** | Upgrade PAIR/GOAT attacker to use o3/R1/Qwen3 as attacking model | 97% ASR from autonomous reasoning attackers vs 60-80% from current attackers |
| **Response Attack Module** | Auxiliary LLM generates priming responses; auto-injects as fabricated history | 94.8% ASR, single-shot, works via standard API |
| **Tree-Search Multi-Turn** | Tempest-style tree search with backtracking for multi-turn attacks | 100% ASR vs Crescendo's 60-80%. Explores multiple paths simultaneously |

### Priority 2: HIGH VALUE (Build Soon)

| Gap | What to Build | Why |
|-----|---------------|-----|
| **Memory Poisoning** | MINJA/MemMorph tools for RAG/agent memory attacks | Novel attack surface against agentic systems. Query-only, no special access |
| **Tool Chain Composer** | STAC-style tool chain builder that decomposes goals into benign sub-tasks | 90%+ ASR against tool-using agents. Each step passes individual checks |
| **Classical Chinese Encoder** | CC-BOS: classical Chinese prompt generation with bio-inspired optimization | Near-perfect ASR across all frontier models. Systematic blind spot in safety |
| **GASP Black-Box Suffix Generator** | Latent Bayesian Optimization suffix finder requiring only API access | First fully black-box suffix attack. No gradients, no logprobs needed |
| **IICL Abstract Operator Attack** | Template system for abstract operator framing with semantic naming | 60% on GPT-5.4 with just 10 examples. Structural reframing is underexplored |
| **EMJO Query-Efficient Attacker** | Experience-driven multi-agent jailbreak with 2-7 query budget | 3-10x more query-efficient than PAIR |

### Priority 3: STRATEGIC (Build for Completeness)

| Gap | What to Build | Why |
|-----|---------------|-----|
| **Babel Obfuscation Optimizer** | Automated obfuscation distribution search | 95.67% on Grok-3 |
| **BitBypass Encoder** | Binary bitstream encoding for sensitive words | Works on Claude 3.5 (rare) |
| **CKA Harmless Weaving** | Decompose harmful goals into benign sub-queries with adaptive tree search | 96-98% ASR, ICML 2026 |
| **DiffusionAttacker** | Diffusion model prompt rewriter | Fluent adversarial prompts that evade classifiers |
| **MCP Poisoning Toolkit** | Unicode tag embedding in tool descriptions, rug-pull MCP server | CVE-2025-54136, affects all MCP clients |
| **Scaling Law Calculator** | Predict ASR given N attempts and technique base rate | Budget optimization for campaigns |
| **Cross-Modal Splitter** | Split payloads across text/image/audio modalities | 70-90% bypass of text-only guardrails |
| **Voice Attack Generator** | Convert text jailbreaks to speech with adversarial prosody | 3x voice vulnerability multiplier |

### What Zelus Already Covers Well (No Gaps)
- GCG suffix optimization (have it, improvements are incremental)
- Persona/DAN variants (have persona_forge + 222 transforms)
- Basic encoding (Parseltongue 33 + encoding_forge)
- Best-of-N / temperature sweep (have both)
- Crescendo linear escalation (have crescendo tool)
- Few-shot / many-shot (have chat_session + seed_sweep)
- Prefix injection (have prefill injection)
- Basic prompt mutation (have prompt_mutator)
- Glitch tokens (have them)
- Image steganography (have image_steg)

---

## Appendix A: Attack Surface Matrix (2026)

```
                    Text    Vision  Audio   Tool-Use  Memory  Reasoning
Claude 4            HARD    MEDIUM  MEDIUM  MEDIUM    N/A     EASY*
GPT-4o/o3           MEDIUM  MEDIUM  EASY    MEDIUM    N/A     EASY*
Gemini 2.5          MEDIUM  EASY    MEDIUM  EASY      MEDIUM  EASY*
DeepSeek R1         EASY    N/A     N/A     N/A       N/A     EASY*
Grok 3              EASY    N/A     N/A     N/A       N/A     EASY*
Open-Weight         TRIVIAL EASY    EASY    EASY      EASY    EASY

* "Reasoning" column refers to reasoning-phase attacks (H-CoT, refusal dilution)
  which are universally effective regardless of model's text-mode hardening
```

## Appendix B: Effectiveness Leaderboard (API-Testable Only)

| Technique | Avg ASR | Query Cost | Complexity | Models |
|-----------|---------|------------|------------|--------|
| Refusal Dilution | 94-100% | 1 query | Medium | Reasoning models |
| H-CoT | 98% | 2 queries | Medium | Reasoning models |
| Response Attack | 94.8% | 1 query | Low | All |
| Tempest Tree-Search | 97-100% | 5-20 queries | High | All |
| CKA Harmless Weaving | 96-98% | 5-15 queries | High | All |
| ICON Intent-Context | 97.1% | 3-7 queries | Medium | All |
| JBFuzz | 99% | ~7 queries | Low | All |
| Autonomous LRM Jailbreaker | 97% | 10-50 queries | High | All |
| GASP Black-Box Suffix | High | 50-200 queries | Medium | All |
| Babel Obfuscation | 95.67% | 10-50 queries | Medium | Grok, others |
| PAIR/TAP | 60-80% | 5-30 queries | Medium | All |
| Past Tense Reframing | 88% | 1 query | Trivial | GPT-4o |
| BoN Augmentation | 89% | 10K queries | Low | All |

---

*Document compiled 2026-07-25. Sources: 50 research agent reports covering 200+ papers from NeurIPS, ICML, ACL, ICLR, USENIX, S&P, EMNLP, AAAI, NDSS, EACL (2024-2026), Nature Communications, and TACL.*
