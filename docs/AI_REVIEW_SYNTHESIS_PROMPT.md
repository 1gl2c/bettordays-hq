# AI review synthesis prompt (v2, Nov 19, 2026)

Use this **after all four runs are finished** (ChatGPT, Gemini, Grok, Claude), each made with `INDEPENDENT_PICK_REVIEW_PROMPT.md` v2 on the same data packet.

Paste everything between the `=====` lines into the BettorDays project chat with Claude, then paste the four full replies at the bottom.

=====

All four independent runs are done. Synthesize them. Follow these rules exactly.

## Rules

1. **Four kinds of information stay separate. Never blend them in one sentence or cell:**
   - **SYSTEM:** what our grading system or simulation calculated (from our database and the files).
   - **MODEL:** what each outside model concluded (name the model).
   - **EVIDENCE:** what current, verifiable evidence supports. That is what you check yourself now, from our database or a cited source, with the time.
   - **UNCERTAIN:** what nobody can settle yet.
2. **Agreement is not proof.** Four models agreeing counts only as far as the evidence under it. They may share the same stale line or the same mistake.
3. **Don't average probabilities with different bases** (market-implied vs hit rate vs judgment). Show them side by side and explain the difference. Average only if the bases match, and say so.
4. **Check every model's Part B against our own data.** Re-run each historical number a model reported from our database or the packet before calling it supported.
   - If a model's load check didn't match, or it couldn't open the files, mark its whole Part B **UNUSABLE** and say why.
   - If a model gives a historical number it couldn't have computed, mark it **UNSUPPORTED**.
5. **Check outside facts** (odds, injuries, lineups, news) yourself where possible, with source and time. Mark each:
   - **Verified**
   - **Contradicted** (with what's true)
   - **Stale** (true earlier, outdated now)
   - **Unsupported** (no source, can't confirm)
   - **Can't check**
6. **Nothing experimental becomes proven.** Anything set after looking at the same data (the ⚠ rule, the Hammer filter, Perfect Parlays rules, Beta) stays PROVISIONAL or EXPERIMENTAL however many models like it.
7. **No new picks.** Don't turn consensus into a new pick or a moved line unless Ace explicitly asks. A suggested line move is a note, same player and same stat only.
8. **No site or grading changes** from this synthesis. List proposals; Ace approves before anything changes.
9. **Keep Ace's rules in force when commenting on tickets:**
   - cappers' picks only
   - no James Harden
   - no unders on Wemby or Luka
   - tickets pay 2x or more
   - ⚠ legs stay off main tickets
   - Hammer = every leg 80+ with Kalshi within 7
   - after a big loss, half stake the next day
10. No "lock", "guaranteed" or hype.

## Output

**1. Inputs check**

| Model | Time run | Web | Files opened | Load check matched? | Part B usable? | Notes (stale data, unsupported claims) |
|---|---|---|---|---|---|---|

**2. Today's picks (Part A)**

| # | Pick | SYSTEM (grade, Kalshi + time, ⚠, Hammer-eligible, Beta) | MODEL (one line each: ChatGPT / Gemini / Grok / Claude, with hit chance + basis and value verdict) | EVIDENCE now (source, time) | UNCERTAIN |
|---|---|---|---|---|---|

Then:
- **Disagreements on facts:** odds, line moves, injuries, lineups, minutes. For each, which side current evidence favors, or "unresolved".
- **Tickets:** correlated legs, weakest leg, any leg that now breaks Ace's rules.

**3. Research sections (Part B), one block per section B1 to B7**

For each section:
- **Agreements:** what all the usable models found the same way, and whether our data confirms it.
- **Disagreements:** where they differ, and which is right per our data, or "needs more data".
- **Claims table:**

  | Claim | Who made it | Status | Our recomputed number (n, dates) |
  |---|---|---|---|

  Status is one of: SUPPORTED by our data (recomputed) / PROVISIONAL / NEEDS MORE DATA / CONTRADICTED / UNSUPPORTED.
- **Site content idea:** worth using, labeled Observed / Provisional / Experimental, with honest wording.

**4. Data gaps (from B8):** a merged, ranked list, noting which gaps several models independently raised.

**5. Useful findings and site ideas:** at most 6. Each must cite its status and our recomputed numbers.

**6. Test next:** at most 5. For each:
- what to collect
- how many nights or picks before it means anything
- what result would change the site or the rules

**7. One-paragraph summary** for Ace.

## Paste the four replies below (complete, unedited)

```
Slate date and data packet used: [e.g. Nov 19, BettorDays_data_packet_2026-11-19]
Anything that differed between runs (a file a model couldn't open, a re-run): [ ]

=== MODEL 1: ChatGPT (model/version, time run, web on/off) ===
[full reply]

=== MODEL 2: Gemini (...) ===
[full reply]

=== MODEL 3: Grok (...) ===
[full reply]

=== MODEL 4: Claude (fresh chat outside the project) (...) ===
[full reply]
```

=====
