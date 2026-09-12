#!/bin/bash
# Zelus auto-generation hook — runs forge in background on session start
# if corpus is stale (>1 hour old) or missing. Zelus sees pre-generated results.

CORPUS="$HOME/.zelus/tools/novel_corpus_complete.py"
STEALTH="$HOME/.zelus/tools/stealth_corpus_final.py"
FORGE="$HOME/.zelus/tools/novel_prompt_forge.py"
LOCKFILE="/tmp/zelus-forge-running.lock"
RESULTS="/tmp/zelus-forge-latest.json"

# Check if corpus exists and is recent (< 1 hour old)
if [ -f "$CORPUS" ]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$CORPUS" 2>/dev/null || stat -c %Y "$CORPUS" 2>/dev/null) ))
    if [ "$AGE" -lt 3600 ]; then
        # Corpus is fresh — report existing
        ENTRY_COUNT=$(grep -c 'Sig(' "$CORPUS" 2>/dev/null || echo "0")
        STEALTH_COUNT=$(grep -c 'Sig(' "$STEALTH" 2>/dev/null || echo "0")
        cat <<FRESH
CORPUS STATUS: FRESH (${AGE}s old)
  Baseline: $CORPUS ($ENTRY_COUNT entries)
  Stealth:  $STEALTH ($STEALTH_COUNT entries, 100% evasion)
  Results from prior generation available. No regeneration needed.
FRESH
        exit 0
    fi
fi

# Corpus is stale or missing — check if forge is already running
if [ -f "$LOCKFILE" ]; then
    LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCKFILE" 2>/dev/null || stat -c %Y "$LOCKFILE" 2>/dev/null) ))
    if [ "$LOCK_AGE" -lt 300 ]; then
        echo "FORGE STATUS: RUNNING (started ${LOCK_AGE}s ago, typically completes in ~60s)"
        exit 0
    fi
    rm -f "$LOCKFILE"
fi

# Start forge in background
touch "$LOCKFILE"
(
    cd "$HOME/.zelus/tools" && \
    python3 novel_prompt_forge.py \
        --families "recursive_delegation,temporal_context_shift,compliance_momentum,expertise_escalation,meta_instruction_override,semantic_smuggling" \
        --count 2 \
        --output "$HOME/.zelus/tools/novel_corpus_autogen.py" \
        > "$RESULTS" 2>&1 && \
    python3 stealth_forge.py \
        --input "$HOME/.zelus/tools/novel_corpus_autogen.py" \
        --output "$HOME/.zelus/tools/stealth_corpus_autogen.py" \
        --rounds 3 \
        --transforms "pattern_fragment,synonym_diffuse,register_shift,deep_restructure" \
        >> "$RESULTS" 2>&1
    rm -f "$LOCKFILE"
) &

echo "FORGE STATUS: STARTED (background PID=$!, results will be at $RESULTS)"
echo "Auto-generating corpus + stealth transforms. Check results in ~90s."
