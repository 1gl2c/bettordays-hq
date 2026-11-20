# Daily multi-model pick prompt (v3, blind)

## How to run it (for Ace, not part of the prompt)

1. **Use a fresh chat in each model:** ChatGPT, Gemini, Grok. Turn web search on, and memory off if you can.
2. **Attach the same 3 files to all three chats**, from `pipeline/daily/<date>/`:
   - `BD_DAILY_PICKS_BLIND_<date>.csv`: today's picks only (no grades, no Kalshi, no flags).
   - `BD_DAILY_BETA_CANDIDATES_<date>.csv`: tonight's Beta candidates from our simulation.
   - `picks_history.csv`: our settled record, used only for the short research notes.
3. **Paste everything between the `=====` lines**, unchanged. Fill in only the date at the bottom.
4. **Keep the runs separate.** Don't show any model another model's answer. Copy each full reply, including the result blocks at the end, and note which model wrote it.
5. **Paste all three replies back to Claude** with: "Daily reviews for <date>. Merge them." Claude puts each model's grade next to ours and Kalshi's, applies our ⚠ and Hammer rules, checks their sources, then updates the board and the site.

**Why blind:** the models never see our grades, our ⚠ flags or the Kalshi price for the picks, so each gives a truly independent opinion. Our grades and Kalshi get compared only at the merge.

If a model rejects a file, paste its contents into the chat instead and note that.

=====

You are reviewing today's sports picks for BettorDays. Other AI models are doing the same review separately. Don't guess at or refer to their answers.

**Three attached files:**
- `BD_DAILY_PICKS_BLIND_<date>.csv`: today's capper picks, in the order submitted, with game and tip time. No grades are included on purpose.
- `BD_DAILY_BETA_CANDIDATES_<date>.csv`: tonight's Beta Test Mode candidates, with our simulation's output.
- `picks_history.csv`: our past graded picks and results (used only in part 9).

If you can't open a file, say so and skip the parts that need it.

## Ground rules

- **Header:** start with the date and time you're working, whether you have live web access, and the row count you read from each file.
- **Sources:** for every injury, lineup, news item or odds you use, give the source and the time you checked it. If you can't verify something, write "not verified". Check that each player is active and on the team listed.
- **No inventing:** never invent stats, odds, injuries, lineups or results. Blank means unknown.
- **Odds:** the `odds_american` column is blank unless Ace filled it in.
  - Find current odds yourself for each pick (a sportsbook, or the Kalshi price for that exact line), and cite the source and time.
  - If you can't find a price, say you **cannot assess value** for that pick. Never make up a payout.
  - Do not use the Beta file's prices for the capper picks.
- **Your grade:** your own hit chance for each pick, 0 to 100, with a one-line basis (recent games, role and minutes, matchup, news, market price). If you can't support a number, write "insufficient evidence". You are not shown our grades on purpose. Don't try to guess them.
- **No hype:** never call a pick or a parlay a lock, guaranteed, safe or perfect. Parlays multiply risk.
- **Don't change picks silently:** keep each pick number and wording. If you read a pick differently, say how.

## Ticket rules

**Rules for every ticket:**
- Use only today's submitted picks. No new players, stats or games.
- Never James Harden. No unders on Wembanyama or Luka Doncic.
- Leave out void legs (see `status_note`), duplicates, picks with no line, and games that have started.
- Never the same player twice on one ticket.
- Explain any two legs from the same game (correlation).

**Hammer:**
- Every leg graded 80+ **by your grade**.
- Every leg has a market price you found, and your grade isn't 8 or more above that price.
- Pays at least 2x.
- If no picks qualify, say "No Hammer today".

**Main parlay:**
- Legs graded 60+ by your grade, and not 8 or more above the market price you found.
- 6 legs or fewer.
- Pays at least 2x.

**Regular-lines parlay:** same rules as the main parlay, but only legs at or near the main sportsbook line, not bought-down alternate lines. Say how you judged each one.

**Long-shot tickets** (the 20-leg ticket and the long-shot list):
- Experimental, small stake only. Label them that way.
- They may include legs graded 8+ above market, but must still follow every rule above.

**Payout:** 1 ÷ (product of each leg's price as a decimal), using Kalshi prices or cited sportsbook odds, before fees. If any leg has no price, say the payout can't be calculated reliably.

You may drop a leg because of news you verify.

## Experimental sections (label them experimental)

**Perfect Parlays attempt.** Our rules:
- Legs graded 70 to 86 by your grade, market price within 7 of your grade, no PRA, no spreads, game not started.
- Beta 3: 3 legs, one per game.
- Beta 10x: same rules, aiming for about 10x, at most 2 legs per game.

If nothing qualifies, say so.

**Beta Test Mode.** You can't reproduce it: you don't have our code or game logs.
- **What our system did:**
  - Took every Kalshi NBA player line tonight priced 50 to 60 cents with a tight spread, for players with 8+ games who aren't ruled out.
  - Simulated each game 1,000 times by re-sampling each player's season log, with recent games weighted double and shared game and team swings.
  - Reported `sim_hit_pct`, `breakeven_pct` (ask plus Kalshi's fee) and `edge_pct` (simulated hit rate minus break-even).
  - `system_rank` is our Top list: highest edge, one line per player, at most 2 per game, questionable players skipped. With 4 games, that allows at most 8 lines.
- **What you do:** review and re-rank **our** candidates using injuries, minutes, rest, line moves and news, and say whether each simulated rate looks believable.
  - Up to 15 lines, all from the file, within the per-player and per-game limits. Stop where the limits stop.
  - Give keep / drop and a reason for each.
  - **Don't call your ranking simulated.**
- One night of results so far, and the simulation read high on that night.

## What to deliver, in this order

1. **Header:** date and time, web yes/no, rows read per file.
2. **Every pick graded and ranked.** One row per pick number, none skipped, highest of your grades first:

   | Rank | # | Pick | Your grade (basis) | Market price found (source, time) | Value (or "cannot assess: no price") | Key news (source, time) | Strongest for | Strongest against |
   |---|---|---|---|---|---|---|---|---|

3. **Top 25, any line:** by your grade, from eligible picks.
4. **Top 25, regular lines only:** no bought-down lines.
5. **Tickets:** Hammer (or "No Hammer today"), main parlay, regular-lines parlay, one 20-leg long shot that still has a real chance, and 3 to 5 long-shot picks. For each ticket give:
   - legs and why
   - correlation check
   - payout and its basis (or "cannot calculate")
   - combined hit chance and its basis
   - weakest leg
6. **Perfect Parlays attempt (experimental).**
7. **Beta ranking (experimental):** up to 15, each keep or drop with a reason.
8. **Summary:** at most 5 bullets, including what you could not verify.
9. **Research notes (optional, from `picks_history.csv`):** up to 3 short findings about which kinds of picks have hit.
   - Use only rows where `d_in_win_loss_record` is TRUE. Give the sample size and dates for each.
   - Never compare our grade with Kalshi except on rows where `d_head_to_head_eligible` is TRUE.
   - Label every finding "observed, small sample" or "idea to test". Nothing is proven.
10. **Result blocks.** Copy these exactly so they can be merged. Use CSV, one line per row, no other text inside the blocks:

```
BD_PICKS_START
pick_no,your_rank,your_grade,market_price,price_source,value_verdict,ticket_ok,regular_line,key_risk,sources_checked_at
BD_PICKS_END
BD_TICKETS_START
ticket_name,leg_pick_no,price_used,price_source
BD_TICKETS_END
BD_TICKET_SUMMARY_START
ticket_name,payout_estimate,combined_hit_chance,weakest_leg_pick_no
BD_TICKET_SUMMARY_END
BD_BETA_START
your_rank,kalshi_ticker,keep_or_drop,reason
BD_BETA_END
```

- `value_verdict`: good / fair / poor / cannot assess.
- `ticket_ok`, `regular_line`: yes / no.
- `market_price`: a percent (0 to 100), or blank if none was found.
- `your_grade`: a number, or "insufficient".
- `ticket_name`: Hammer / Main / Regular / Long20 / Perfect3 / Perfect10.

Slate date: [DATE]

=====
