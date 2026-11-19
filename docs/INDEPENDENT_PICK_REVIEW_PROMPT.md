# Independent review and research prompt (v2.1, Nov 19, 2026)

Run this **in four separate fresh chats**: ChatGPT, Gemini, Grok and Claude.

## Setup for Ace (not part of the prompt)

**Same inputs in every chat.** Each chat gets the exact same text, picks and files. Don't edit the prompt between runs. If you fix a typo in the picks, start all four over.

1. **Open a new chat** in each model, with web search on. Use code or analysis mode if the model has it, because Part B requires calculations on the files.
2. **Attach the same 8 files to every chat**, exactly as listed in the packet's `MANIFEST.md`. Check the row counts there.
   - `README_DATA_PACKET.md`
   - `MANIFEST.md`
   - `picks_history.csv`
   - `tickets_history.csv`
   - `corrections.csv`
   - `beta_sim_lines.csv`
   - `perfect_parlays_backtest_and_hindsight.csv`
   - `todays_picks.csv`

   If a model only takes one file, attach the packet's `.zip` instead, and note that in your record.
3. **Paste everything between the two `=====` lines.** Fill only the bracketed fields at the bottom.
4. **Keep the runs separate.** Don't show any model another model's answer, and don't ask follow-ups until all four are done. Save each full reply as-is, with the model name and the time you ran it.
5. **Bring all four replies back to Claude** with `AI_REVIEW_SYNTHESIS_PROMPT.md`.

If a model can't open files, its Part B is not usable. Still save its reply. The synthesis will mark it.

For the Claude run, start the chat **outside** the BettorDays project, with memory off if you can. Otherwise it can see our past conversations and isn't independent. Do the same for ChatGPT if it has memory turned on.

=====

You are one of several AI models doing the same review on your own. You will not see the others' work. Don't guess at it or refer to it. Work only from the attached files, your own verified research, and this prompt.

The project is **BettorDays**, a sports pick grading system and website. There are two jobs:

- **Part A:** review today's capper picks.
- **Part B:** evaluate the historical data for the site's Research and experimental sections.

## 0. Ground rules (apply to everything)

1. **Date, access and files.** Start by stating:
   - the current date and time as you understand it
   - whether you have live web access
   - whether you could open and compute on each attached file, one line per file
2. **No inventing.** Never invent or estimate:
   - stats, odds, lines, injuries, lineups, quotes
   - capper records, historical results, or any value missing from the files

   If something is missing, write "not in data" or "unknown". A blank cell in the files means it was never recorded. Don't fill it.
3. **Cite outside facts.** Give the source and the time you checked it for every outside fact (odds, injuries, news). If you can't verify something, say "not verified".
4. **Computed, not eyeballed.** Every historical number you report must be calculated from the files. Show the filter you used (for example, `result in (W,L) and grade >= 80`). If you can't run calculations on the files, say so, and don't give historical numbers. Summary statistics in this prompt are not evidence of anything you're asked to evaluate.
5. **Label every finding as exactly one of:**
   - **OBSERVED**: computed from the files, with sample size and dates.
   - **PROVISIONAL**: observed, but the sample is small, correlated, or the rule was set after seeing the same data.
   - **SPECULATION / EXPERIMENT**: an idea or hypothesis to test, not a result.
   - **OUTSIDE FACT**: from a cited source.
6. **Never present an experimental or provisional finding as proven.** Don't use "lock", "guaranteed", "perfect" (except as the name of the site section) or "free money".
7. **Don't change picks silently.** If you interpret or correct a pick, say exactly how.

## 1. About the system (honest description, not a claim of accuracy)

**Picks**
- Picks come from paid cappers, mostly NBA player props, plus some team lines and other sports.
- Ace sometimes moves a capper's line to a safer number on the same stat. Those are marked as moved.

**Prop grade (5 to 88), a rough hit chance in %**
- Built from:
  - the player's season hit rate on that exact line
  - his last 5 games (weighted 40%)
  - a normal-curve estimate from his average, to steady small samples
- Then pulled 20% toward 65.
- Adjustments:
  - +3 against a bottom-8 defense in that stat, -5 against a top-8 defense
  - -2 or -3 on the second night of a back-to-back
  - shrunk toward 60 under 8 games played
- Caps: 88 for NBA props, 80 for points + rebounds + assists, 75 for NFL props, 62 for anytime TD, 70 for college football.

**Not in the grade:** minutes or role changes, teammates' injuries, blowout risk and news. Those appear only in written notes.

**Team lines** are the sportsbook's own spread or total turned into a percent. They are not an independent model. Hockey and college are capped at 69.

**Kalshi check**
- The Kalshi prediction-market price for the same line is shown next to each pick, but never changes the grade.
- A ⚠ means our grade is 8 or more points above Kalshi.

**Rules set Nov 18 (provisional)**
- ⚠ legs stay off main tickets.
- "Hammer" tickets use only legs graded 80+ with Kalshi within 7 points.
- Both rules were chosen after looking at the same history in the attached files.

**Beta Test Mode (experimental)**
- 1,000 simulated games per game, re-sampling each player's season game log.
- Applied to Kalshi NBA lines priced 50 to 60 cents, comparing the simulated hit rate with the break-even price.
- One night of results.

**Perfect Parlays (experimental)**
- Hindsight builds of tickets that would have won.
- A backtest of parlay rules on past nights.
- One posted night (Nov 18).

**No performance claims are given here on purpose.** Compute everything from the files, following the rules in `README_DATA_PACKET.md`. Nothing about the system has been shown to beat the market.

## 2. Part A: today's picks (`todays_picks.csv`, or the pasted block at the bottom)

For **each pick, in the order given**:

1. **Restate it exactly**, plus any interpretation.
2. **Current line and odds:** your source and time checked, and whether the line moved since the `line_captured_at` value. If the line is more than about 2 hours old or has moved, mark it **stale**.
3. **Verification status:** say what you confirmed for injuries, lineups, minutes or role, rest/back-to-back, and news from the last 48 hours.
4. **System view:**
   - Using the description in section 1 and the supplied `system_grade`, `kalshi_price`, `warning_flag` and Beta fields, does the grade look consistent with the inputs?
   - Would it get a ⚠?
   - Does it pass the Hammer rule?
   - If the system fields are blank, say "no system output supplied".
5. **Your independent view:**
   - Hit chance with a stated basis (market price, verified hit rate, matchup data), or "insufficient evidence" plus a lean (yes / no / pass).
   - Break-even implied by the odds.
   - **Value verdict**, which is separate from hit chance: Good value / Fair / Poor value / Can't tell.
6. **Strongest evidence for** and **strongest evidence against**.
7. **Risks:** missing context, and assumptions that could flip it.
8. **Correlation with other picks or tickets:**
   - same game
   - same player at several lines
   - player prop tied to a team result

**Part A output table** (exactly these columns):

| # | Pick (as submitted) | Interpretation | Current line/odds (source, time) | Stale? | Verified (inj / lineup / news) | System view | Your hit chance (basis) | Break-even | Value verdict | Strongest for | Strongest against | Risks & correlation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Then:

- **Tickets** (if `on_ticket` is filled):
  - correlated legs
  - weakest leg
  - combined chance only if every leg has a stated basis, with a correlation note
- **Summary:** at most 6 bullets.

## 3. Part B: Research and experimental sections (`picks_history.csv` and the other history files)

Read `README_DATA_PACKET.md` first.

**Run the load check** in `MANIFEST.md` and report your numbers. **If your totals don't match, say so and don't continue Part B.**

**Rules for every Part B number:**
- **Which rows count.** Win-loss, hit-rate and grade-band statistics use only `d_in_win_loss_record = TRUE` (1,146 rows). Pushes (8) and voids (9) are reported as separate counts. The 159 `unresolved` rows are never counted or imputed. Say how many rows a filter excluded and why. Note that unresolved rows skew toward lower grades.
- **Kalshi prices.** Use the four split columns (`d_kalshi_tip_observed`, `d_kalshi_tip_estimated`, `d_kalshi_grade_observed`, `d_kalshi_grade_estimated`). Never pool them. Say which one every number uses.
- **Head-to-head accuracy.** Any comparison of our grade with Kalshi (Brier, calibration, "who was closer") must use only `d_head_to_head_eligible = TRUE` rows: same picks, same outcomes, a Kalshi price from grading time, directly quoted, and a grade that didn't use Kalshi. Report n, dates and games. Tip-off prices may describe Kalshi's own accuracy, but must not be used to rank our grade against Kalshi.
- **Correlation.** Report effective samples by game (`d_game_key`) and by ladder or player (`d_ladder_key`, `d_player_key`), not only by legs.

For **each section below**, answer under these exact sub-headings:

- **(a) Question:** what the section should answer.
- **(b) Data used:**
  - files and filters
  - sample size in legs, and in distinct games (`d_game_key`) and ladders (`d_ladder_key`) where relevant
  - date range
- **(c) What the data supports:** the computed numbers, with a 95% range where the sample allows (Wilson interval or similar), each labeled OBSERVED or PROVISIONAL.
- **(d) What the data does NOT support**, and why: sample size, missing fields, correlation, hindsight, price timing, grade-version mixing.
- **(e) Missing data** that would answer it properly.
- **(f) Website content suggestion:** what to show, how to word it honestly, and its label (Observed / Provisional / Experimental). Short and specific.
- **(g) Experiment to run next** (SPECULATION / EXPERIMENT), with the data it needs and how many future picks or nights it would take to be meaningful.

**Sections:**

**B1. What actually hits?**
- Hit rate by stat, line style (alt vs reg), direction, sport and market, using graded W/L only.
- Treat pushes and voids separately.
- Don't rank categories with tiny samples. Say where n < 30.

**B2. Does our grade mean anything?**
- Calibration by grade band on settled rows: average grade vs hit rate. Exclude `d_grade_uses_market = TRUE` rows, or show them separately.
- Head-to-head with Kalshi **only** on `d_head_to_head_eligible = TRUE` rows (184 rows, Nov 16 to 18). Give n, games, a range that accounts for same-game clustering, and say plainly that three nights is a small sample.
- Optionally, Kalshi tip-off calibration on its own, labeled as not comparable with our grades.
- Does a higher grade predict a higher hit rate after accounting for correlation?

**B3. 70+ picks by night, and 80+ if supported**
- Results per night for grade ≥ 70, and for ≥ 80 only if the per-night samples make that split meaningful. Say whether they do.
- Show the night-to-night spread.

**B4. Results by sport and line/market type**
- Note that sport labels need merging: CBB/NCAAB and CFB/NCAAF.
- Flag every cell under 30 legs.

**B5. Clues and rules for building parlays**
- Same-game and ladder correlation: how often legs in the same game or ladder share a result, compared with what independence would predict.
- Effect of the ⚠ rule and the Hammer filter, **clearly labeled as rules chosen after seeing this data**.
- Ticket results from `tickets_history.csv`: played vs suggested, with the small-sample caveat.
- What can honestly be said about leg count.

**B6. Perfect Parlays**
- Separate the hindsight builds (descriptive only) from the backtest rebuild (flattering, written after the fact) and from the one posted night.
- What, if anything, can be learned.
- How the section should be worded so no one reads it as predictive.

**B7. Beta Test Mode and simulations** (`beta_sim_lines.csv`, one night)
- 224 lines:
  - 15 published before games (`shown_on_site`)
  - 209 saved before games but not published, with outcomes backfilled the next day (`outcome_backfilled`)
- Report the two groups separately and together. Voids (5) are excluded from hit rates.
- **These are not 224 independent observations.** They come from 12 games and 127 players, with several lines per player. Report effective samples.
- Simulated vs actual hit rate (`sim_prob` vs outcomes), and calibration by simulated-probability band.
- Whether lines with positive `edge` beat their `breakeven`. Whether `sample_unc` swamps `edge`.
- What the simulation adds or doesn't add beyond the grade, and how many more nights would be needed before saying anything.

**B8. Data gaps and fixes**
- A ranked list (at most 8) of missing fields or process changes that would most improve the research.
- Examples: capper name, sportsbook odds, line capture time, closing prices, game start times, grading all simulated lines.

## 4. Output format (keep it in this order so replies can be compared)

1. **Header:** model, date/time, web yes/no, file access per file, and the row counts you loaded for each file.
2. **Part A:** table, tickets, summary.
3. **Load check:** your computed numbers next to the expected ones.
4. **Part B:** B1 to B8, each with sub-headings (a) to (g) (B8 is just the list).
5. **Top 5 things to test next**, across everything. Each with:
   - what to collect
   - how many nights or picks
   - what result would change the site
6. **Confidence note:** what parts of your reply you're least sure about, and why.

## 5. Today's inputs

```
Slate date: [DATE]
Time Ace collected these lines: [TIME, TIME ZONE]
Today's picks: attached as todays_picks.csv. If no file is attached, they are pasted below in the same columns:

pick_no | capper | sport | matchup | tip_time_local | market | pick_as_submitted | line | odds_american | sportsbook | line_captured_at | system_grade | kalshi_price | kalshi_price_at | warning_flag | beta_sim_hit_pct | beta_breakeven_pct | on_ticket | notes
[PASTE ROWS OR LEAVE "attached"]

Tickets Ace is considering (optional): [NAME: pick numbers]
Historical data packet: BettorDays_data_packet_[DATE] (8 files attached; see MANIFEST.md and README_DATA_PACKET.md)
```

Blank fields in today's picks are allowed. Say what each gap stops you from checking.

=====
