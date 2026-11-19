# Independent pick review prompt

**How to use it:**
1. Copy everything between the two `=====` lines into a fresh chat with ChatGPT, Claude, Gemini or Grok. Use web search mode if the model has it.
2. Fill in the paste section at the bottom. Blank fields are fine.
3. Send it, and save the reply exactly as given.
4. Do the same with each model, each in its own new chat. Don't show any model another model's answer.

Then take all the replies to `docs/AI_REVIEW_SYNTHESIS_PROMPT.md`.

=====

You are reviewing a batch of sports picks on your own. Other AI models are reviewing the same batch separately. You will not see their answers, and you should not guess what they said. Give your own work.

## 1. About the system that graded these picks

I use a personal grading system. Here is an honest description so you can judge it fairly. **None of this is proven to beat the market.**

**What the picks are**
- Picks come from paid cappers, mostly NBA player props.
- Some are moneylines, spreads and totals, plus some NHL and college.
- I sometimes move a line to a safer number on the same stat (for example 25+ points instead of 30+). Those are marked "moved".

**How a prop is graded**
- The grade is 5 to 88 and is meant as a rough hit chance in percent.
- Inputs:
  - the player's hit rate on that exact line this season
  - the last 5 games (weighted 40%)
  - a normal-curve estimate from his average, used to steady small samples
- Then it is pulled 20% toward 65.
- Adjustments:
  - +3 against a bottom-8 defense in that stat, -5 against a top-8 defense
  - -2 or -3 on the second night of a back-to-back
  - shrunk toward 60 if he has played fewer than 8 games
  - capped at 88 (80 for points + rebounds + assists)

**Not in the grade:** minutes or role changes, injuries to teammates, blowout risk, rest, travel, and news. Those are only noted by hand.

**Team lines** (moneyline, spread, total) are graded by turning the sportsbook's own spread or total into a percent. That is the market's view, not an independent model. Hockey and college are capped at 69.

**Kalshi check**
- Each leg is shown next to the Kalshi prediction market price for the same line, when one exists.
- Kalshi does not change the grade.
- A ⚠ is shown when our grade is 8 or more points above Kalshi.
- So far ⚠ legs have hit less often than the rest, so they are kept off main tickets.

**Simulation ("Beta")** is experimental.
- It runs 1,000 simulated games per game, re-sampling each player's season game log, with shared game and team noise.
- It scans all Kalshi NBA lines priced 50 to 60 cents and compares the simulated hit rate with the break-even price after fees.
- It is one night old. On that night it averaged 72% while the lines actually hit 60%, so treat it as reading high.

**Track record, Nov 4 to Nov 18, 2026**
- 1,146 graded legs, 743-403 (65%). Grade 70+: 343-99.
- These are the cappers' picks, not a random sample.
- Many legs are on the same player or the same game, so the real sample is much smaller than the count.
- On legs with a Kalshi price, Kalshi's prices were more accurate than our grades. Brier score 0.189 vs 0.211 for Nov 4 to 17 (lower is better).
- High grades have been overconfident: 85+ grades hit about 72%.
- **Treat our grade as one opinion with a known lean toward overconfidence, not as a probability you can trust.**

## 2. Rules for your review

1. **Date and sources.** Start by stating the current date and time as you understand it and whether you have live web access. List every source you used, with the time you checked it where possible.
2. **Verify when you can.** If you have web access, check:
   - current odds and lines, from at least one sportsbook or Kalshi if available
   - official injury reports and starting lineups
   - rest and back-to-back status
   - relevant news from the last 48 hours

   If you have no web access, say so clearly and mark every time-sensitive item "not verified".
3. **Invent nothing.** Do not make up stats, game logs, odds, injury news, lineups, quotes, picks or capper records. If you don't have a number, write "unknown". A plausible-sounding guess is worse than "unknown".
4. **Don't change picks silently.** Review each pick exactly as submitted. If a pick is unclear, a line has moved, or I made an obvious typo, say what you think it means and grade it under that stated reading. Note it in the "Interpretation / corrections" column.
5. **Two separate views per pick:**
   - **System view.** How does this pick look under the system described above? Does its grade seem consistent with the inputs I gave, and would it get a ⚠?
   - **Your view.** Your own independent assessment.
6. **Hit chance and value are different questions.**
   - "Likely to hit" asks how often this would win.
   - "Good value at this price" asks whether the payout is worth that chance. Compare your estimate with the break-even implied by the odds.

   A 75% pick at -400 is likely to hit and still bad value.
7. **Probabilities need a basis.** Give a percent only if you can name what it rests on (market price, season rate, matchup data, and so on). Otherwise write "insufficient evidence" and give a direction only (lean yes, lean no, pass).
8. **Strongest case both ways.** For each pick, give the single strongest piece of evidence for it and the single strongest against it.
9. **Flag risks:**
   - stale lines (collected more than about 2 hours before you checked, or the line has since moved)
   - missing context (injury questionable, minutes limit, new role, blowout risk, rest)
   - assumptions that could flip the result
10. **Correlation.** Point out legs that depend on each other:
    - same game
    - same player at several lines
    - player props tied to a team result
    - same-team legs

    Say whether a ticket combining them is riskier than it looks.
11. **No hype.** Never call a pick or parlay "perfect", a "lock", "guaranteed", "free money" or similar. Parlays multiply risk.
12. **Don't trust the system blindly.** If its grade looks too high or too low, say so and explain why.

## 3. Output format

**Part A: header**
- Date/time
- Web access yes/no
- Sources list

**Part B: one table, one row per pick, in the order submitted**

| # | Pick (as submitted) | Interpretation / corrections | Current line & odds (source, time) | Verified? (odds / injury / lineup) | System view | Your hit chance (basis) | Break-even at listed odds | Value verdict | Strongest for | Strongest against | Risks & correlation |
|---|---|---|---|---|---|---|---|---|---|---|---|

Value verdict is one of: Good value / Fair / Poor value / Can't tell.

**Part C: tickets.** If I listed any tickets or parlays:
- list which legs are correlated
- give a combined hit chance only if each leg has a stated basis, with a note on correlation
- name the weakest leg

**Part D: summary, at most 8 bullets**
- the picks you'd most trust and why
- the picks you'd pass on and why
- anything that changed since the lines were collected
- what you could not verify

## 4. Paste section

Fill what you have; leave the rest blank or write "unknown". You may review picks with missing fields. Just say what the gap stops you from checking.

```
Date and time I collected these lines: 
My time zone: 
Book or app I'm betting on (Kalshi, PrizePicks, FanDuel, etc.): 

PICKS (one per line; copy this row for each):
Capper | Sport | Matchup | Market / prop | Line | Odds | Book | Time collected | System grade | Kalshi price | Sim output | Notes
       |       |         |               |      |      |      |                |              |              |            |

TICKETS I'M CONSIDERING (optional):
Ticket name | Legs (by #) | Stated payout

ANYTHING ELSE (injury news I saw, line moves, my concerns):
```

=====

## Notes for Ace (not part of the prompt)

- **Field mapping.** "System grade" is the number on the board. "Kalshi price" is the `K nn` chip. "Sim output" is from Beta Test Mode, only for lines it covered (sim %, break-even, edge).
- **Capper names and book odds aren't stored anywhere yet.** The database has no column for them. Fill those from your own notes.
- **Keep the description current.** If the track record or rules change, update section 1 so the models aren't working from old numbers. Last updated from the code on Nov 19, 2026.
