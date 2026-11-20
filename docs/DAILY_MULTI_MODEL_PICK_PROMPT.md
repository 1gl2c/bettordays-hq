# Daily multi-model pick prompt

## How to run it (for Ace, not part of the prompt)

1. **Use a fresh chat in each model:** ChatGPT, Gemini, Grok. Turn web search on. Turn memory off if you can.
2. **Attach the same 2 files to all three chats**, from `daily/<date>/`:
   - `BD_DAILY_PICKS_<date>.csv`
   - `BD_DAILY_BETA_CANDIDATES_<date>.csv`
3. **Paste everything between the `=====` lines**, unchanged. Fill in only the date line at the bottom.
4. **Keep the runs separate.** Don't show any model another model's answer. Copy each full reply, including the three result blocks at the end, and note which model wrote it.
5. **Paste all three replies back to Claude** in the BettorDays project with: "Daily reviews for <date>. Merge them." Claude checks them against our data and current sources, then updates the board and the site after you approve.

Attach the files in the order listed. If a model rejects a file, paste its contents into the chat instead and note that.

=====

You are reviewing today's sports picks for BettorDays. Other AI models are doing the same review separately. Don't guess at or refer to their answers.

**Two attached files:**
- `BD_DAILY_PICKS_<date>.csv`: today's capper picks, in the order submitted, with our system's grade and flags.
- `BD_DAILY_BETA_CANDIDATES_<date>.csv`: tonight's Beta Test Mode candidate lines, with our simulation's output.

If you can't open a file, say so and stop that part.

## Ground rules

- **Header:** start with the date and time you're working, whether you have live web access, and the row count you read from each file.
- **Sources:** for every injury, lineup, news item or odds you use, give the source and the time you checked it. If you can't verify something, write "not verified".
- **No inventing:** never invent stats, odds, injuries, lineups or results. Blank means unknown.
- **Odds:** the `odds_american` column is blank unless Ace filled it in.
  - Without odds for a pick, say you **cannot assess value** for it. Never make up a payout.
  - `kalshi_price` is the Kalshi prediction-market price for that exact line at the time shown. You may use it as a market price, but say that's what you used.
  - If you find current sportsbook odds yourself, cite them with source and time.
- **Two views, never blended:**
  - **System grade:** given in the file. Don't change it. You may say whether it looks too high or too low, and why.
  - **Your grade:** your own independent hit chance, 0 to 100, with a one-line basis (market price, recent games, matchup, news). If you can't support a number, write "insufficient evidence".
- **No hype:** never call a pick or a parlay a lock, guaranteed, safe or perfect. Parlays multiply risk.
- **Don't change picks silently:** keep each pick number and wording. If you read a pick differently, say how.

## How our system grades (so you can judge it; it is not proven)

**Player props.** Grade = rough hit chance, 5 to 88.
- Starts from the player's season hit rate on that exact line and his last 5 games (weighted 40%), smoothed by a normal-curve estimate from his average. Then pulled 20% toward 65.
- Adjustments:
  - +3 against a bottom-8 defense in that stat; -5 against a top-8 defense.
  - -2 or -3 on the second night of a back-to-back.
  - Pulled toward 60 if he has played fewer than 8 games.
- Caps: 88 for NBA props, 80 for points + rebounds + assists, 75 for NFL props, 62 for anytime TD.
- **Not modeled:** minutes, role changes, teammate injuries and blowout risk. These appear only in the note.

**Team lines.** The sportsbook spread or total turned into a percent. This is not an independent model.
- College basketball and hockey are capped at 69.
- NFL team lines get **no system grade**.

**Kalshi check.** The Kalshi price never changes the grade. `warning_8plus_above_kalshi = YES` means our grade is 8 or more points above Kalshi.

**Track record:** the market has been more accurate than our grades on comparable picks. Treat our grade as one opinion.

## Ticket rules (applied when the file's `ticket_eligible` and `hammer_eligible` columns were made)

A leg can go on today's recommended parlay only if all of these hold:
- It is one of today's submitted picks. No new players, stats or games.
- It is not void, not a duplicate, and has a system grade of 60 or higher.
- It has no ⚠, meaning the grade is not 8 or more above Kalshi.
- It doesn't break Ace's rules: never James Harden; no unders on Wembanyama or Luka Doncic.
- Its game has not started.

The ticket as a whole:
- Pays at least **2x**.
- Has **6 legs or fewer**.
- Has no two legs from the same game unless you explain the correlation, and **never the same player twice**.

**Hammer** (the top ticket) needs every leg graded 80+ with a Kalshi price within 7 of the grade. The file shows which picks qualify. If none do, say there is no Hammer today.

You may drop a `ticket_eligible = YES` leg because of news you verify. You may not add a `NO` leg.

**Payout.** Estimate it as 1 ÷ (product of each leg's price as a decimal). Use Kalshi prices or cited sportsbook odds, before fees. If any leg has no price, say the payout can't be calculated reliably.

## Beta Test Mode (what you can and cannot do)

**What our system did** (you can't reproduce it; you don't have our code or game logs):
- Took every Kalshi NBA player line tonight priced 50 to 60 cents with a tight spread, for players with 8+ games who aren't ruled out.
- Simulated each game 1,000 times by re-sampling each player's season game log, with recent games weighted double and shared game and team swings.
- Reported:
  - `sim_hit_pct`, the simulated hit rate.
  - `breakeven_pct`, the ask price plus Kalshi's fee.
  - `edge_pct`, simulated hit rate minus break-even.
- `system_rank` is our Top list: highest edge, one line per player, at most 2 per game, questionable players skipped.

**What you do:** review and re-rank the **system's** candidates using your own checks: injuries, minutes, rest, line moves, news, and whether the simulated rate looks believable.
- You are ranking our simulation's output. You are not running a new simulation. Don't call your ranking simulated.
- Rank up to 15 lines, all from the file, keeping the one-per-player and two-per-game limits.
- If those limits allow fewer than 15, stop there and say so.
- For each line, give keep / drop and why.

**This is experimental.** One night of results so far, and the simulation read high on that night.

## Output, in this order

**1. Header:** date and time, web yes/no, rows read per file.

**2. Picks table**, one row per pick number:

| # | Pick | System grade | Your grade (basis) | Value (or "cannot assess: no odds") | Key news (source, time) | Strongest for | Strongest against | Ticket-eligible after your checks? |
|---|---|---|---|---|---|---|---|---|

**3. Recommended candidate parlay** (one):
- legs
- why each leg
- correlation check
- payout estimate with its basis, or "cannot calculate"
- your combined hit chance with its basis
- the weakest leg

If no ticket meets the rules, say so. Don't bend a rule.

**4. Beta ranking:** up to 15 lines, each with keep / drop and a reason.

**5. Summary:** at most 5 bullets, including what you could not verify.

**6. Result blocks.** Copy these exactly so they can be merged. Use CSV, one line per row, no extra text inside the blocks:

```
BD_PICKS_START
pick_no,your_grade,value_verdict,ticket_ok,key_risk,sources_checked_at
...
BD_PICKS_END
BD_TICKET_START
leg_pick_no,price_used,price_source
...
payout_estimate,combined_hit_chance,weakest_leg_pick_no
BD_TICKET_END
BD_BETA_START
your_rank,kalshi_ticker,keep_or_drop,reason
...
BD_BETA_END
```

- `value_verdict`: good / fair / poor / cannot assess.
- `ticket_ok`: yes / no.
- `your_grade`: a number, or "insufficient".

Slate date: [DATE]

=====
