#!/bin/bash
# BettorDays daily multi-AI review through Hermes.
# Usage (from your bettordays folder):  bash bd_daily.sh picks.txt
# picks.txt = today's picks, one per line, as you'd send them to Claude.
# Each AI runs in its own separate Hermes session (its own web search and Python),
# so no model sees another model's answer. Replies land in reviews/<date>/.
set -u
cd "$(dirname "$0")"
PICKS="${1:-picks.txt}"
[ -f "$PICKS" ] || { echo "Can't find $PICKS. Put today's picks in a text file and pass its name."; exit 1; }
[ -f bd_prompt.md ] || { echo "Can't find bd_prompt.md next to this script."; exit 1; }
command -v hermes >/dev/null || { echo "The hermes command isn't on your PATH. Open the Hermes app terminal, or run: hermes --version"; exit 1; }

# Models via OpenRouter. Edit this list any time (IDs from openrouter.ai/models).
MODELS=(
  "chatgpt|openai/gpt-6.2-sol"
  "gemini|google/gemini-4-neon"
  "grok|x-ai/grok-4.7"
  "claude|anthropic/claude-sonnet-5.5"
)

DAY=$(date +%Y-%m-%d)
OUT="reviews/$DAY"; mkdir -p "$OUT"
PROMPT=$(sed "s/\[DATE\]/$(date '+%A, %B %-d, %Y')/" bd_prompt.md)
PROMPT="${PROMPT/\[PASTE PICKS HERE, ONE PER LINE, NUMBERED\]/$(nl -w1 -s'. ' "$PICKS")}"
printf '%s\n' "$PROMPT" > "$OUT/prompt_sent.md"

echo "Running ${#MODELS[@]} independent reviews for $DAY. This usually takes 5 to 20 minutes."
for entry in "${MODELS[@]}"; do
  name="${entry%%|*}"; model="${entry##*|}"
  (
    start=$(date +%s)
    hermes -z "$PROMPT" --provider openrouter --model "$model" > "$OUT/$name.md" 2> "$OUT/$name.log"
    code=$?
    echo "$name ($model): exit $code, $(( $(date +%s) - start ))s, $(wc -c < "$OUT/$name.md") bytes"
  ) &
done
wait
echo
echo "Done. Replies are in $OUT/. Send the four .md files (and prompt_sent.md) to Claude in the BettorDays project and say: Hermes reviews for $DAY. Merge them."
