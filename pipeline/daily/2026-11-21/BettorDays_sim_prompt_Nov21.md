# BettorDays Simulation Lab · Saturday, November 21, 2026

You are the quant on a sports betting research team. Tonight you run **1,000 simulations of every NBA game listed** and find which player lines hit most often. The lines below are Kalshi lines that trade near even money (about +100 to -150). **You are not shown their prices.** We compare your hit rates to the prices ourselves.

Injury notes as of 1:15 PM PT (confirm yourself): Anthony Edwards (MIN) out, Dylan Harper (SA) out, Dereck Lively II (DAL) out, Bradley Beal and Brandon Ingram (LAC) out, OG Anunoby (NY) doubtful, Karl-Anthony Towns (NY) questionable (illness), Jayson Tatum and Derrick White (BOS) questionable. Kings played at the Lakers last night (back-to-back).

Tonight's games: NBA POR@NY 4:30 PM PT; NBA LAC@DAL 5:00 PM PT; NBA MEM@MIN 5:00 PM PT; NBA NO@SA 5:00 PM PT; NBA BOS@SAC 7:00 PM PT

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
random.seed(21)
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

1 | Darius Acuff Jr. (SAC) 3+ threes | BOS@SAC 7:00 PM PT
2 | Darius Acuff Jr. (SAC) 6+ assists | BOS@SAC 7:00 PM PT
3 | Paul George (BOS) 25+ points | BOS@SAC 7:00 PM PT
4 | Paul George (BOS) 6+ rebounds | BOS@SAC 7:00 PM PT
5 | Brook Lopez (LAC) 2+ threes | LAC@DAL 5:00 PM PT
6 | Brook Lopez (LAC) 2+ assists | LAC@DAL 5:00 PM PT
7 | Brook Lopez (LAC) 20+ points + rebounds + assists | LAC@DAL 5:00 PM PT
8 | Caleb Martin (DAL) 4+ rebounds | LAC@DAL 5:00 PM PT
9 | Cooper Flagg (DAL) 6+ assists | LAC@DAL 5:00 PM PT
10 | Cooper Flagg (DAL) 25+ points | LAC@DAL 5:00 PM PT
11 | Darius Garland (LAC) 3+ threes | LAC@DAL 5:00 PM PT
12 | Darius Garland (LAC) 30+ points + rebounds + assists | LAC@DAL 5:00 PM PT
13 | Derrick Jones Jr. (LAC) 15+ points + rebounds + assists | LAC@DAL 5:00 PM PT
14 | Derrick Jones Jr. (LAC) 4+ rebounds | LAC@DAL 5:00 PM PT
15 | Keaton Wagler (LAC) 15+ points + rebounds + assists | LAC@DAL 5:00 PM PT
16 | Keaton Wagler (LAC) 10+ points | LAC@DAL 5:00 PM PT
17 | Kris Dunn (LAC) 5+ points | LAC@DAL 5:00 PM PT
18 | Kyrie Irving (DAL) 4+ rebounds | LAC@DAL 5:00 PM PT
19 | Max Strus (LAC) 20+ points + rebounds + assists | LAC@DAL 5:00 PM PT
20 | Naji Marshall (DAL) 4+ assists | LAC@DAL 5:00 PM PT
21 | Naji Marshall (DAL) 20+ points + rebounds + assists | LAC@DAL 5:00 PM PT
22 | Naji Marshall (DAL) 4+ rebounds | LAC@DAL 5:00 PM PT
23 | P.J. Washington (DAL) 20+ points + rebounds + assists | LAC@DAL 5:00 PM PT
24 | Rui Hachimura (LAC) 2+ threes | LAC@DAL 5:00 PM PT
25 | Rui Hachimura (LAC) 20+ points + rebounds + assists | LAC@DAL 5:00 PM PT
26 | Ayo Dosunmu (MIN) 4+ assists | MEM@MIN 5:00 PM PT
27 | Ayo Dosunmu (MIN) 25+ points + rebounds + assists | MEM@MIN 5:00 PM PT
28 | Ayo Dosunmu (MIN) 4+ rebounds | MEM@MIN 5:00 PM PT
29 | Bones Hyland (MIN) 2+ threes | MEM@MIN 5:00 PM PT
30 | Bones Hyland (MIN) 10+ points | MEM@MIN 5:00 PM PT
31 | Cam Spencer (MEM) 2+ threes | MEM@MIN 5:00 PM PT
32 | Cam Spencer (MEM) 10+ points | MEM@MIN 5:00 PM PT
33 | Cedric Coward (MEM) 4+ assists | MEM@MIN 5:00 PM PT
34 | Cedric Coward (MEM) 15+ points | MEM@MIN 5:00 PM PT
35 | Cedric Coward (MEM) 8+ rebounds | MEM@MIN 5:00 PM PT
36 | Isaiah Stewart (MEM) 1+ threes | MEM@MIN 5:00 PM PT
37 | Isaiah Stewart (MEM) 4+ rebounds | MEM@MIN 5:00 PM PT
38 | Jaden McDaniels (MIN) 2+ threes | MEM@MIN 5:00 PM PT
39 | Jaden McDaniels (MIN) 25+ points + rebounds + assists | MEM@MIN 5:00 PM PT
40 | Jaylen Wells (MEM) 2+ threes | MEM@MIN 5:00 PM PT
41 | Jaylen Wells (MEM) 15+ points + rebounds + assists | MEM@MIN 5:00 PM PT
42 | Jaylen Wells (MEM) 10+ points | MEM@MIN 5:00 PM PT
43 | Jonathan Kuminga (MIN) 15+ points | MEM@MIN 5:00 PM PT
44 | LaMelo Ball (MIN) 4+ threes | MEM@MIN 5:00 PM PT
45 | LaMelo Ball (MIN) 6+ assists | MEM@MIN 5:00 PM PT
46 | LaMelo Ball (MIN) 30+ points + rebounds + assists | MEM@MIN 5:00 PM PT
47 | LaMelo Ball (MIN) 20+ points | MEM@MIN 5:00 PM PT
48 | Rudy Gobert (MIN) 2+ assists | MEM@MIN 5:00 PM PT
49 | Rudy Gobert (MIN) 20+ points + rebounds + assists | MEM@MIN 5:00 PM PT
50 | Rudy Gobert (MIN) 10+ rebounds | MEM@MIN 5:00 PM PT
51 | Taylor Hendricks (MEM) 15+ points + rebounds + assists | MEM@MIN 5:00 PM PT
52 | Taylor Hendricks (MEM) 10+ points | MEM@MIN 5:00 PM PT
53 | Ty Jerome (MEM) 6+ assists | MEM@MIN 5:00 PM PT
54 | Ty Jerome (MEM) 30+ points + rebounds + assists | MEM@MIN 5:00 PM PT
55 | Zach Edey (MEM) 8+ rebounds | MEM@MIN 5:00 PM PT
56 | De'Aaron Fox (SA) 6+ assists | NO@SA 5:00 PM PT
57 | De'Aaron Fox (SA) 4+ rebounds | NO@SA 5:00 PM PT
58 | Devin Vassell (SA) 2+ threes | NO@SA 5:00 PM PT
59 | Devin Vassell (SA) 20+ points + rebounds + assists | NO@SA 5:00 PM PT
60 | Devin Vassell (SA) 4+ rebounds | NO@SA 5:00 PM PT
61 | Julian Champagnie (SA) 3+ threes | NO@SA 5:00 PM PT
62 | Stephon Castle (SA) 2+ threes | NO@SA 5:00 PM PT
63 | Stephon Castle (SA) 30+ points + rebounds + assists | NO@SA 5:00 PM PT
64 | Damian Lillard (POR) 4+ assists | POR@NY 4:30 PM PT
65 | Damian Lillard (POR) 20+ points | POR@NY 4:30 PM PT
66 | Deni Avdija (POR) 2+ threes | POR@NY 4:30 PM PT
67 | Deni Avdija (POR) 6+ rebounds | POR@NY 4:30 PM PT
68 | Donovan Clingan (POR) 2+ assists | POR@NY 4:30 PM PT
69 | Donovan Clingan (POR) 10+ points | POR@NY 4:30 PM PT
70 | Jalen Brunson (NY) 3+ threes | POR@NY 4:30 PM PT
71 | Jalen Brunson (NY) 6+ assists | POR@NY 4:30 PM PT
72 | Josh Hart (NY) 4+ assists | POR@NY 4:30 PM PT
73 | Josh Hart (NY) 20+ points + rebounds + assists | POR@NY 4:30 PM PT
74 | Josh Hart (NY) 10+ points | POR@NY 4:30 PM PT
75 | Jrue Holiday (POR) 2+ threes | POR@NY 4:30 PM PT
76 | Jrue Holiday (POR) 20+ points + rebounds + assists | POR@NY 4:30 PM PT
77 | Jrue Holiday (POR) 4+ rebounds | POR@NY 4:30 PM PT
78 | Karl-Anthony Towns (NY) 2+ threes | POR@NY 4:30 PM PT
79 | Karl-Anthony Towns (NY) 20+ points | POR@NY 4:30 PM PT
80 | Mikal Bridges (NY) 10+ points | POR@NY 4:30 PM PT
81 | Sidy Cissoko (POR) 2+ assists | POR@NY 4:30 PM PT
82 | Toumani Camara (POR) 2+ assists | POR@NY 4:30 PM PT
83 | Toumani Camara (POR) 4+ rebounds | POR@NY 4:30 PM PT

## Answer format (required, exactly this)

BD_SIM_START
line_no,sim_hit_pct,minutes_used,key_input
BD_SIM_END

BD_SIMTOP_START
rank,line_no,why
BD_SIMTOP_END

`sim_hit_pct` is 0 to 100 with one decimal. `key_input` is the one input that drives the number (example: "Murray out so usage up"). No commas inside a field. Say in one line at the top whether you ran the code or did it by hand.
