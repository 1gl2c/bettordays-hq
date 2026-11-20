# BettorDays Simulation Lab · [DATE]

You are the quant on a sports betting research team. Tonight you run **1,000 simulations of every NBA game listed** and find which player lines hit most often. The lines below are Kalshi lines that trade near even money (about +100 to -150). **You are not shown their prices.** We compare your hit rates to the prices ourselves.

Tonight's games: [SLATE]

## Step 1: build inputs for each player (use web search)

For every player in the list, decide tonight's inputs from your own research: StatMuse game logs, NBA.com, the official injury report, beat reporters.

- **minutes**: projected minutes tonight (role, injuries on his team, blowout risk from the spread)
- **per-minute rates** for points, rebounds, assists and threes from his recent games (weight the last 10 more than the season)
- **matchup multiplier**: about 0.90 to 1.10 for how tonight's opponent defends this stat and his position
- **pace multiplier**: about 0.95 to 1.05 from both teams' pace and the game total
- Ruled out or very doubtful: leave him out.

## Step 2: run the simulation (1,000 runs per game)

If you can run code, run this Python as is, with your inputs filled in. If you cannot run code, do the same math by hand and say so.

```python
import random, math
random.seed(20)
N = 1000
# fill in: one dict per player line from the list below
# line_no, game, minutes, sd_minutes, rate (per minute, for this line's stat), matchup, pace, threshold
LINES = [
  # dict(line_no=1, game="PHX@UTAH", minutes=34, sd_minutes=4, rate=0.72, matchup=1.03, pace=1.00, threshold=25),
]
games = {}
for L in LINES: games.setdefault(L["game"], []).append(L)
hits = {L["line_no"]: 0 for L in LINES}
for g, ls in games.items():
    for _ in range(N):
        game_pace = random.gauss(1.0, 0.05)          # shared by everyone in the game
        script = random.gauss(0.0, 1.0)              # blowout risk: big margin trims starters' minutes
        for L in ls:
            mins = max(0, random.gauss(L["minutes"], L["sd_minutes"]) - (3 if abs(script) > 1.6 else 0))
            mean = mins * L["rate"] * L["matchup"] * L["pace"] * game_pace
            # count stats: negative binomial style spread (variance about 1.3x the mean)
            k = mean / 0.3 if mean > 0 else 0
            lam = random.gammavariate(k, 0.3) if k > 0 else 0
            x, p, s = 0, math.exp(-lam), random.random()
            cum = p
            while s > cum and x < 200:
                x += 1; p *= lam / x; cum += p
            if x >= L["threshold"]: hits[L["line_no"]] += 1
for n, h in sorted(hits.items(), key=lambda t: -t[1]): print(n, round(100 * h / N, 1))
```

## Step 3: report

Grade every line in the list. Then give your 10 best lines (highest hit rate you trust, at most 2 per game).

## Tonight's lines

[SIMLINES]

## Answer format (required, exactly this)

BD_SIM_START
line_no,sim_hit_pct,minutes_used,key_input
BD_SIM_END

BD_SIMTOP_START
rank,line_no,why
BD_SIMTOP_END

`sim_hit_pct` is 0 to 100 with one decimal. `key_input` is the one input that drives the number (example: "Murray out so usage up"). No commas inside a field. Say in one line at the top whether you ran the code or did it by hand.
