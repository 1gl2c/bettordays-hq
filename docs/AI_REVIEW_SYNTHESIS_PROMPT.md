# AI review synthesis prompt

**How to use it:** after collecting the independent reviews made with `docs/INDEPENDENT_PICK_REVIEW_PROMPT.md`, paste everything between the `=====` lines to Claude in the BettorDays project, then fill in the paste section.

=====

I collected independent reviews of tonight's picks from several AI models. Synthesize them against our own system. Follow these rules exactly.

## Your job

1. **Load what the system calculated.** For each pick, get from our own records:
   - our grade
   - the Kalshi price and its timestamp
   - the ⚠ flag
   - the Beta sim output, if any

   Use Supabase `model_picks` / `model_beta_lines` or the current board. If a pick isn't on our board, say so. Don't invent a grade for it.

2. **Read every model response in full.** Note for each one:
   - the date/time it claimed
   - whether it had web access
   - its sources

3. **Check every factual claim the models made** about odds, lines, injuries, lineups and news.
   - Where you have web access, verify it now and note the time you checked.
   - Mark each claim one of:
     - **Verified**, with source and time
     - **Contradicted**, with what is actually true and your source
     - **Stale**: true earlier but out of date now, such as a moved line or an updated injury status
     - **Unsupported**: no source given and you can't confirm it
     - **Can't check**

   If a model cited a stat or a number you can't find anywhere, say it may be invented.

4. **Compare, don't vote.**
   - Show where the models agree with each other and with our system, and where they disagree.
   - Three models agreeing is not proof. They may share the same stale data or the same blind spot. Agreement matters only when it rests on verified evidence.

5. **Probabilities.**
   - Don't average the models' percentages unless they use comparable bases. If they don't (one from market odds, one from a hit rate, one a gut call), show them side by side and explain why they differ.
   - Never treat our grade as more reliable than the market price. Our record says the opposite so far.

6. **Highlight every disagreement about:**
   - odds or line (and which number is current)
   - injury or lineup status
   - line movement since collection
   - correlation between legs
   - key assumptions (minutes, role, pace, blowout risk)

7. **Keep hit chance and value separate**, as the models were asked to.

## Output format

**Part A: inputs check**
- Which models replied, the time each claimed, web yes/no.
- Any reply that looks stale, unsourced or possibly invented, and why.

**Part B: one table per pick.** Keep the four kinds of information in separate columns. Don't blend them.

| # | Pick | What our system calculated (grade, Kalshi + time, ⚠, sim) | What each model concluded (one short line per model, with its verdict) | What current verifiable evidence supports (source, time) | What remains uncertain |
|---|---|---|---|---|---|

**Part C: disagreements.** A short list of real conflicts on facts or assumptions, with which side the current evidence favors, or "unresolved".

**Part D: tickets.** For any ticket I listed:
- correlated legs
- the weakest leg, and whether the reviews and evidence support that
- whether any leg now breaks our rules (⚠, line moved, player status changed, under 2x payout)

**Part E: summary, at most 6 bullets**
- what changed since grading
- picks where the evidence and the reviews raise a real concern
- picks where the evidence supports our grade
- what's still unknown and when it would be known (for example the injury report at a given time)

## Limits

- **Do not create new picks** or new lines from the consensus unless I explicitly ask. If you think a line should move, say so as a note, keep the original pick in the table, and only suggest a move on the same player and same stat.
- **Do not change our grades** in the database or on the site as part of this.
- **No hype.** No "lock", "perfect" or "guaranteed".
- **Keep my rules in force:**
  - cappers' picks only
  - no James Harden
  - no unders on Wemby or Luka
  - tickets pay 2x or more
  - ⚠ legs stay off main tickets
  - Hammer = 80+ and Kalshi within 7
  - after a big loss, half stake the next day

## Paste section

```
Slate date: 
Picks or board this covers (or "tonight's board"): 

MODEL 1 name / mode (web on/off): 
[paste full reply]

MODEL 2 name / mode: 
[paste full reply]

MODEL 3 name / mode: 
[paste full reply]

MODEL 4 name / mode: 
[paste full reply]

Tickets I'm considering (optional): 
My questions (optional): 
```

=====
