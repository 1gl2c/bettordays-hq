#!/bin/bash
# BettorDays product audit: the same 4 flagship models as the daily runner each audit bettordays.xyz.
#   bash bd_audit.sh        replies land in reviews/<date>-audit/<model>.md (finished ones are skipped)
set -u
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/.hermes/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
MAX_MIN="${BD_MAX_MIN:-30}"
MODELS=("chatgpt|openai/gpt-6.2-astra-pro" "gemini|google/gemini-4-neon" "grok|x-ai/grok-4.7" "claude|anthropic/claude-fable-5.2")
EXTRA=(-t web,browser)
DAY=$(date +%Y-%m-%d); OUT="reviews/$DAY-audit"; mkdir -p "$OUT"; LOG="$OUT/runner.log"
say() { echo "$(date '+%H:%M:%S') $*" | tee -a "$LOG"; }
curl -fsS "https://raw.githubusercontent.com/1gl2c/bettordays-hq/main/pipeline/hermes/bd_audit.md" -o bd_audit.md 2>/dev/null || true
[ -f bd_audit.md ] || { say "bd_audit.md missing"; exit 1; }
sed "s/\[DATE\]/$(date '+%A, %B %e, %Y' | tr -s ' ')/" bd_audit.md > "$OUT/prompt.md"
for entry in "${MODELS[@]}"; do
  name="${entry%%|*}"; model="${entry##*|}"; of="$OUT/$name.md"
  grep -q "BD_AUDIT_END" "$of" 2>/dev/null && { say "$name already done, skipping"; continue; }
  [ -s "$of" ] && mv "$of" "${of%.md}.failed.$(date +%H%M).md"
  (
    start=$(date +%s)
    ( hermes -z "$(cat "$OUT/prompt.md")" --provider openrouter --model "$model" "${EXTRA[@]}" > "$of" 2> "${of%.md}.log"
      if grep -qiE "unrecognized arguments|no such option|unknown option|is not a .hermes. command|unknown toolset|Usage:|unknown toolset" "${of%.md}.log"; then
        hermes -z "$(cat "$OUT/prompt.md")" --provider openrouter --model "$model" > "$of" 2>> "${of%.md}.log"
      fi ) &
    pid=$!
    ( sleep $((MAX_MIN * 60)); pkill -P "$pid" 2>/dev/null; kill "$pid" 2>/dev/null ) & dog=$!
    wait "$pid"; kill "$dog" 2>/dev/null
    say "$name ($model): $(( $(date +%s) - start ))s, $(wc -c < "$of" | tr -d ' ') bytes, result: $(grep -q BD_AUDIT_END "$of" && echo yes || echo NO)"
  ) &
done
wait
say "Done. Tell Claude: audit replies for $DAY are ready."
osascript -e 'display notification "Audit done. Tell Claude." with title "BettorDays"' >/dev/null 2>&1 || true
