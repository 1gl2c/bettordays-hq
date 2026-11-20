#!/bin/bash
# BettorDays Daily Engine v7 runner (Hermes). Runs the v7 research prompt on 4 models at once and
# finishes by about 1:25 PM PT, so Claude can merge and the board is live by 2:30 PM PT.
#
# Normal use: launchd starts it at 12:40 PM every day (see install_v7.sh). It downloads today's
# candidate lines (Claude publishes them after grading your capper picks), runs the models, and saves
# the replies in reviews/<date>/. You can also run it by hand:
#   bash bd_daily_v7.sh                 # downloads today's lines
#   bash bd_daily_v7.sh lines.txt       # uses a lines file you already have
# Works with the bash that ships with macOS.
set -u
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/.hermes/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

MAX_MIN="${BD_MAX_MIN:-40}"          # hard stop per model, minutes (12:40 start + 40 = 1:20 PM)
LINES_WAIT_UNTIL="${BD_WAIT_UNTIL:-1305}"   # keep checking for today's lines until 1:05 PM
REPO_RAW="https://raw.githubusercontent.com/1gl2c/bettordays-hq/main/pipeline/daily"
REPO_DIR="${BD_REPO:-$HOME/bettordays/engine/bettordays-hq}"   # optional clone: replies get pushed for Claude
MODELS=(
  "chatgpt|openai/gpt-6.2-sol"
  "gemini|google/gemini-4-neon"
  "grok|x-ai/grok-4.7"
  "claude|anthropic/claude-sonnet-5.5"
)

DAY=$(date +%Y-%m-%d)
OUT="reviews/$DAY"; mkdir -p "$OUT"
LOG="$OUT/runner.log"
say() { echo "$(date '+%H:%M:%S') $*" | tee -a "$LOG"; }
notify() { osascript -e "display notification \"$1\" with title \"BettorDays v7\"" >/dev/null 2>&1 || true; }

command -v hermes >/dev/null || { say "hermes is not on PATH. Run: which hermes, and add its folder to PATH at the top of this script."; notify "Runner stopped: hermes not found"; exit 1; }
[ -f bd_prompt_v7.md ] || { say "bd_prompt_v7.md is missing next to this script."; exit 1; }

# 1. today's candidate lines
if [ "${1:-}" != "" ]; then
  cp "$1" "$OUT/lines.txt"; : > "$OUT/slate.txt"
else
  while :; do
    if curl -fsS "$REPO_RAW/$DAY/v7_lines.txt" -o "$OUT/lines.txt" 2>/dev/null && [ -s "$OUT/lines.txt" ]; then
      curl -fsS "$REPO_RAW/$DAY/v7_slate.txt" -o "$OUT/slate.txt" 2>/dev/null || : > "$OUT/slate.txt"
      break
    fi
    if [ "$(date +%H%M)" -ge "$LINES_WAIT_UNTIL" ]; then
      say "No lines for $DAY yet. Send your capper picks to Claude, then run: bash $(pwd)/bd_daily_v7.sh"
      notify "No lines yet. Send picks to Claude, then rerun."
      exit 1
    fi
    say "Waiting for today's lines from Claude..."; sleep 120
  done
fi
NL=$(grep -c . "$OUT/lines.txt")
say "Got $NL candidate legs."

# 2. fill the prompt
PROMPT=$(sed "s/\[DATE\]/$(date '+%A, %B %e, %Y' | tr -s ' ')/" bd_prompt_v7.md)
SLATE=$(tr '\n' ' ' < "$OUT/slate.txt"); [ -n "$SLATE" ] || SLATE="see the lines below"
PROMPT="${PROMPT/\[SLATE\]/$SLATE}"
PROMPT="${PROMPT/\[LINES\]/$(cat "$OUT/lines.txt")}"
printf '%s\n' "$PROMPT" > "$OUT/prompt_sent.md"

# 3. four models at once, each with a hard stop
say "Running ${#MODELS[@]} models, up to $MAX_MIN minutes each."
for entry in "${MODELS[@]}"; do
  name="${entry%%|*}"; model="${entry##*|}"
  (
    start=$(date +%s)
    hermes -z "$PROMPT" --provider openrouter --model "$model" > "$OUT/$name.md" 2> "$OUT/$name.log" &
    pid=$!
    ( sleep $((MAX_MIN * 60)); kill "$pid" 2>/dev/null && echo "stopped at $MAX_MIN min" >> "$OUT/$name.log" ) &
    dog=$!
    wait "$pid"; code=$?
    kill "$dog" 2>/dev/null
    blk=$(grep -c "BD_V7_END" "$OUT/$name.md" 2>/dev/null)
    say "$name ($model): exit $code, $(( $(date +%s) - start ))s, $(wc -c < "$OUT/$name.md" | tr -d ' ') bytes, result block: $([ "${blk:-0}" -gt 0 ] && echo yes || echo NO)"
  ) &
done
wait

# 4. hand-off: push replies for Claude if a repo clone is set up, else leave them for drag and drop
OK=$(grep -l "BD_V7_END" "$OUT"/chatgpt.md "$OUT"/gemini.md "$OUT"/grok.md "$OUT"/claude.md 2>/dev/null | wc -l | tr -d ' ')
if [ -d "$REPO_DIR/.git" ]; then
  D="$REPO_DIR/pipeline/daily/$DAY/replies"; mkdir -p "$D"
  cp "$OUT"/*.md "$OUT"/runner.log "$D"/ 2>/dev/null
  ( cd "$REPO_DIR" && git pull -q --rebase && git add "pipeline/daily/$DAY/replies" && \
    git commit -q -m "v7 model replies $DAY ($OK of 4 with result blocks)" && git push -q ) >> "$LOG" 2>&1 \
    && say "Replies pushed for Claude." || say "Push failed (see $LOG). Drag the files in $OUT into the BettorDays chat instead."
fi
say "Done: $OK of 4 models returned a result block. Tell Claude: v7 replies for $DAY are ready."
notify "$OK of 4 models done. Tell Claude: v7 replies are ready."
