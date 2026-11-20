# BettorDays Daily Engine v7 (as written by Ace, Nov 20, 2026)

This is Ace's v7 rulebook, copied unchanged below the line. It is the rulebook from the Nov 20 board on.

**Data check (Claude, Nov 20, 12:45 AM PT).** Some numbers in v7 don't match our record. The rules stand as written; the model prompt (`pipeline/hermes/bd_prompt_v7.md`) uses the checked numbers instead, so the models aren't given wrong facts. Source: site record `ROWS` (Nov 4 to 19, 1,187 graded legs) and the `model_picks` database.

| v7 says | Our record says |
|---|---|
| Nov 19: 0 of 8 on legs graded 8+ above Kalshi | 2 of 8 (Stroud 10+ rushing and Montgomery 10+ receiving hit) |
| NFL yardage props graded 80+ hit 6 of 18 | 7 of 18 (39%) |
| PRA 1 of 6 | PRA at 70+: 16 of 22 (73%). All PRA: 23 of 40 (58%) |
| Back-to-backs 1 of 7 | Back-to-backs at 70+: 18 of 23 (78%), Nov 16 to 19 (the only nights b2b is recorded) |
| Underdog moneylines 0 of 4 | Moneylines with Kalshi under 50: 6 of 19 (32%) |
| Points 90% at 70+ | Points at 70+: 93 of 120 (78%) |
| Moneylines 83 to 85% at 70+ | 40 of 48 (83%). Matches |
| GREEN legs are our best | Kalshi at or above our grade, graded 70+: 131 of 150 (87%). Matches |

The back-to-back rule (no b2b legs on the Hammer) is kept because v7 says so, but our record doesn't show back-to-backs as weak.

---

# BETTORDAYS DAILY ENGINE v7
Effective Fri Nov 20, 2026. Replaces every older rulebook. Target: 80% on every published 70+ leg.

Why v7 exists: Nov 19 went 2 of 6 on 70+ legs and 0 of 8 on legs we graded 8+ above Kalshi. Across every measured night, Kalshi's price has been more accurate than our grades (Nov 16 to 18: 0.210 vs 0.224; Nov 19: 0.279 vs 0.313, lower is better). So the market is the anchor, and our models earn the right to disagree with it, never the other way around.

---

## PART A. RESEARCH PROMPT (paste into each model: ChatGPT, Gemini, Grok, Claude)

You are a sharp sports analyst for BettorDays. Today is [DATE]. Slate: [SPORTS/GAMES]. Here are today's lines and Kalshi prices: [PASTE].

For every candidate leg, give one row:
player (full name) | team | opponent | market | line | side | Kalshi price | YOUR hit probability | 2-line reason

Your reason must cover what actually decides the leg: projected minutes and role, injuries and late news, matchup (opponent allows this stat?), pace, home or away, rest (back-to-back?), and the player's last 10 games against THIS exact line.

How to set your probability:
1. Start from the Kalshi price. That is the market's number and it has beaten us every night we measured.
2. Move off it only for a specific reason the market may not have priced yet (late injury, role change, minutes cap, lineup news). Name the reason.
3. If you end up 8+ points above Kalshi, you must name the exact fact the market is missing. If you cannot, set your number to Kalshi + 3.

Our own data says these are WEAK spots. Demand extra evidence before grading them 70+:
- NFL yardage props (graded 80+ hit only 6 of 18)
- Rebounds, especially guards and wings (and big men vs strong rebounding teams)
- PRA combos (1 of 6), anytime TDs, ceiling lines above the player's average (about 50%)
- Back-to-backs (1 of 7), underdog moneylines (0 of 4), college spreads

These are STRONG spots at 70+: points (90%), assists, threes, moneylines (83 to 85%), favorites, and lines that moved toward our side.

Then give:
- Your TOP 10 legs ranked by real hit probability.
- 3 to 5 specific tips to make bettordays.xyz better (features, tools, how we present picks).

---

## PART B. MERGE AND GRADE (Claude does this when Ace sends the 4 model outputs)

1. Merge: for each leg, take the median of the 4 models. Record each model's number, so we learn which model is sharpest by market.
2. Gap check against Kalshi:
   - Kalshi at or above our median: GREEN. These are our best legs (71% on Nov 16 to 18, 88% at 70+ on Nov 16).
   - 0 to 7 above Kalshi: YELLOW. Usable only in strong markets.
   - 8+ above Kalshi: REMOVED from the board, the Hammer and every ticket. Shown only on the research page as "market disagrees."
3. Published grade = our median, capped at Kalshi + 7. No published grade ever sits far above the market again.
4. No Kalshi price: grade allowed, but max 75, and never on the Hammer.

## PART C. WHAT GOES ON THE SITE

**Picks page (the board):** all GREEN and YELLOW legs graded 70+, sorted by grade.

**Hammer:** 3 to 5 legs. Every leg GREEN or within 3 of Kalshi, published 75+, strong market type, no two legs from the same game, no back-to-backs. If fewer than 3 legs qualify, post "No Hammer tonight" and say why. Passing is a win.

**Research page, perfect parlays:** build 3 tickets from GREEN legs only, explain why each leg is there and the correlation risk:
- Safe: 2 legs, about +100 to +150
- Core: 3 to 4 legs, +150 to +300
- Stretch: 4 to 5 legs, labeled higher risk
Plus a short "what each model saw" section: where they agreed, where they split.

**Beta (EXPERIMENTAL):** simulate every game on the slate 1,000 times. List lines priced +100 to -150 where the simulated probability beats the price by 5+ points AND Kalshi leans the same way. The simulation ran hot on its first night (72% simulated vs 60% actual), so shrink each simulated probability one third of the way back toward the implied price before ranking. Track it nightly and do not promote it until 100+ graded legs show an edge.

**Site improvements:** list the best 3 to 5 tips from the models each day.

## PART D. LEARN EVERY MORNING

After results: log every leg with our median, each model's number, Kalshi, market type and result. Update hit rates by gap bucket (GREEN, YELLOW, REMOVED), by market and by model. Move a market on or off the weak list only after 30+ graded legs. Publish the misses as openly as the wins.

## PART E. ACE'S BETTING RULES (personal tickets)
Max $100 a day. Half stake the day after a big loss. Never James Harden. No unders on Wembanyama or Luka. Tickets pay 2x or more. Never take a REMOVED leg, no matter the grade.

## DEADLINE
Model outputs to Claude by 1:30 PM PT. Graded board live on the site by 2:30 PM PT, so X posts the board at 3:05 and the player posts after.
