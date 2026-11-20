#!/bin/bash
# BettorDays Engine v8 runner (Hermes). Each of the 4 models gets two jobs at the same time:
#   1. bd_prompt_v8.md  blind analyst room: grades every leg with NO market price shown
#   2. bd_sim_v8.md     simulation lab: 1,000 runs per NBA game on lines near +100, prices hidden
# Replies land in reviews/<date>-v8/ as <model>.md and <model>_sim.md. A job that already has its result
# block is skipped, and a failed reply is kept as <name>.failed.<time>.md, never overwritten.
#   bash bd_daily_v8.sh            # downloads today's v8 files from GitHub (waits until 1:05 PM)
# Works with the bash that ships with macOS.
set -u
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/.hermes/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

MAX_MIN="${BD_MAX_MIN:-45}"   # deep research needs time: 12:40 start + 45 = 1:25 PM
LINES_WAIT_UNTIL="${BD_WAIT_UNTIL:-1305}"
REPO_RAW="https://raw.githubusercontent.com/1gl2c/bettordays-hq/main/pipeline"
# Top model from each lab on OpenRouter (checked Nov 20, 2026). Update here when a newer flagship ships.
MODELS=(
  "chatgpt|openai/gpt-6.2-astra-pro"
  "gemini|google/gemini-4-neon"
  "grok|x-ai/grok-4.7"
  "claude|anthropic/claude-fable-5.2"
)
# Deep research: web search + a terminal for running the simulation code, plenty of tool steps.
# Reasoning effort is a Hermes setting, set once with: hermes config set agent.reasoning_effort xhigh
EXTRA=(-t web,terminal --max-turns 80)

DAY=$(date +%Y-%m-%d)
OUT="reviews/$DAY-v8"; mkdir -p "$OUT"
LOG="$OUT/runner.log"
say() { echo "$(date '+%H:%M:%S') $*" | tee -a "$LOG"; }
notify() { osascript -e "display notification \"$1\" with title \"BettorDays v8\"" >/dev/null 2>&1 || true; }
command -v hermes >/dev/null || { say "hermes is not on PATH."; notify "Runner stopped: hermes not found"; exit 1; }

# 1. prompts and today's files (prompts are pulled fresh so Claude's updates always apply)
curl -fsS "$REPO_RAW/hermes/bd_prompt_v8.md" -o bd_prompt_v8.md 2>/dev/null || true
curl -fsS "$REPO_RAW/hermes/bd_sim_v8.md" -o bd_sim_v8.md 2>/dev/null || true
[ -f bd_prompt_v8.md ] && [ -f bd_sim_v8.md ] || { say "v8 prompt files missing."; exit 1; }
while :; do
  if curl -fsS "$REPO_RAW/daily/$DAY/v8_lines.txt" -o "$OUT/lines.txt" 2>/dev/null && [ -s "$OUT/lines.txt" ]; then
    curl -fsS "$REPO_RAW/daily/$DAY/v8_sim_lines.txt" -o "$OUT/sim_lines.txt" 2>/dev/null || : > "$OUT/sim_lines.txt"
    curl -fsS "$REPO_RAW/daily/$DAY/v8_slate.txt" -o "$OUT/slate.txt" 2>/dev/null || : > "$OUT/slate.txt"
    break
  fi
  [ "$(date +%H%M)" -ge "$LINES_WAIT_UNTIL" ] && { say "No v8 lines for $DAY yet. Send picks to Claude, then rerun."; notify "No lines yet"; exit 1; }
  say "Waiting for today's lines from Claude..."; sleep 120
done
say "Got $(grep -c . "$OUT/lines.txt") legs and $(grep -c . "$OUT/sim_lines.txt") sim lines."

fill() { # $1 template, $2 lines file, $3 placeholder
  local P; P=$(sed "s/\[DATE\]/$(date '+%A, %B %e, %Y' | tr -s ' ')/" "$1")
  P="${P/\[SLATE\]/$(tr '\n' ' ' < "$OUT/slate.txt")}"
  P="${P/\[$3\]/$(cat "$2")}"
  printf '%s\n' "$P"
}
fill bd_prompt_v8.md "$OUT/lines.txt" LINES > "$OUT/prompt_analyst.md"
fill bd_sim_v8.md "$OUT/sim_lines.txt" SIMLINES > "$OUT/prompt_sim.md"

run_job() { # name model promptfile outfile endmarker
  local name=$1 model=$2 pf=$3 of=$4 mark=$5
  if grep -q "$mark" "$of" 2>/dev/null; then say "$name: $(basename "$of") already done, skipping"; return; fi
  [ -s "$of" ] && mv "$of" "${of%.md}.failed.$(date +%H%M).md"
  local start; start=$(date +%s)
  # if this Hermes version rejects the extra flags, rerun once without them
  ( hermes -z "$(cat "$pf")" --provider openrouter --model "$model" "${EXTRA[@]}" > "$of" 2> "${of%.md}.log"
    if grep -qiE "unrecognized arguments|no such option|unknown option" "${of%.md}.log"; then
      echo "extra flags not supported, running without them" >> "${of%.md}.log"
      hermes -z "$(cat "$pf")" --provider openrouter --model "$model" > "$of" 2>> "${of%.md}.log"
    fi ) &
  local pid=$!
  ( sleep $((MAX_MIN * 60)); pkill -P "$pid" 2>/dev/null; kill "$pid" 2>/dev/null && echo "stopped at $MAX_MIN min" >> "${of%.md}.log" ) &
  local dog=$!
  wait "$pid"; local code=$?
  kill "$dog" 2>/dev/null; wait "$dog" 2>/dev/null
  say "$name $(basename "$of"): exit $code, $(( $(date +%s) - start ))s, $(wc -c < "$of" | tr -d ' ') bytes, result: $(grep -q "$mark" "$of" && echo yes || echo NO)"
}
say "Models: ${MODELS[*]}"
say "Running ${#MODELS[@]} models x 2 jobs (analyst + simulation), up to $MAX_MIN minutes each."
for entry in "${MODELS[@]}"; do
  name="${entry%%|*}"; model="${entry##*|}"
  run_job "$name" "$model" "$OUT/prompt_analyst.md" "$OUT/$name.md" "BD_V8_END" &
  run_job "$name" "$model" "$OUT/prompt_sim.md" "$OUT/${name}_sim.md" "BD_SIM_END" &
done
wait 2>/dev/null
A=$(grep -l "BD_V8_END" "$OUT"/chatgpt.md "$OUT"/gemini.md "$OUT"/grok.md "$OUT"/claude.md 2>/dev/null | wc -l | tr -d ' ')
S=$(grep -l "BD_SIM_END" "$OUT"/chatgpt_sim.md "$OUT"/gemini_sim.md "$OUT"/grok_sim.md "$OUT"/claude_sim.md 2>/dev/null | wc -l | tr -d ' ')
if grep -lq "HTTP 402" "$OUT"/chatgpt*.md "$OUT"/gemini*.md "$OUT"/grok*.md "$OUT"/claude*.md 2>/dev/null; then say "OpenRouter credits ran out on at least one job. Add credits, then run this again (finished jobs are skipped)."; fi
say "Done: $A of 4 analyst reports, $S of 4 simulations. Tell Claude: v8 replies for $DAY are ready."
notify "$A of 4 analyst, $S of 4 sims done. Tell Claude: v8 ready."
