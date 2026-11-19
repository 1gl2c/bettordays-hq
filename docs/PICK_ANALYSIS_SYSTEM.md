# BettorDays pick analysis system: how it actually works

Last verified against the code: **Thu Nov 19, 2026** (repo commit `9a66cfa`).

This guide describes the system as it exists today. Every formula below was copied from the code, not from memory or from conversation. Where something is manual, experimental, stale or unverified, it says so.

Three labels are used throughout:

- **[BUILT]** the current code does this.
- **[INTENDED]** we discussed or decided it, but the code does not fully do it yet.
- **[TO DO]** still to be built or checked.

---

## 1. Read this first

The system has **two halves that live in different places**:

| Half | Where it lives | Durable? |
|---|---|---|
| Website + member app + API | GitHub repo `1gl2c/bettordays-hq`, deployed by Vercel to bettordays.xyz | Yes |
| Grading pipeline (fetch stats, grade picks, grade results, simulations, audits) | Python scripts in Claude's session scratchpad: `/tmp/claude-0/-home-claude/a51ac9e7-b9b5-5441-8a1a-5d02537c46e5/scratchpad/` | **No.** It is temporary storage. It can be wiped when the session ends. |
| Pick history (source of truth) | Supabase project `ndcsjhetuasijbgpfhwj`, tables `model_picks`, `model_pick_corrections`, `model_tickets`, `model_beta_lines` | Yes |

**[TO DO] The grading scripts are not in the repo.** They are copied and edited by hand each day (for example `tue/grade.py` became `wed/grade_head.py` + `wed/grade_body.py`). If the scratchpad is lost, the formulas below are the only written record. Moving these scripts into the repo (for example `pipeline/`) is the top recommendation in this document.

Scratchpad paths below are written relative to that scratchpad folder.

---

## 2. End-to-end flow

```
You send a list of capper picks (text in chat)
        │
        ▼
Claude transcribes each pick into a line like add('Luka Doncic','pts',30)      [manual]
        │
        ▼
Fetch inputs: ESPN game logs, injuries, scoreboard/spreads, Kalshi prices     [scripts]
        │
        ▼
Grade each pick: season + last 5 + matchup + back-to-back + caps → pct 5-88   [script]
        │
        ▼
Attach Kalshi price at grading time (k) → ⚠ if pct ≥ k + 8                     [script + site]
        │
        ▼
Build suggested tickets (Hammer, second ticket) by hand using the rules        [manual]
        │
        ▼
Patch the site HTML with the day's board, rebuild index.html, push to GitHub   [scripts]
Save every pick to Supabase model_picks with timestamps                       [manual SQL load]
        │
        ▼
Next morning: fetch ESPN box scores, grade each pick W/L/P                    [script]
        │
        ▼
Update Supabase, site ROWS, record.json, recap, research pages                [scripts + manual]
```

---

## 3. Stage by stage

### 3.1 What you provide and how it enters

**[BUILT, manual]**
- You paste capper picks as text (player, stat, line; or team ML/spread/total).
- There is **no automatic parser**. Claude reads the list and writes one `add(...)` call per pick in `wed/grade_list.py`. Examples:
  - `add('Julius Randle','ast',5,orig='over 4 assists')`
  - `add('Luka Doncic','pts',25,moved=True)`
- Team picks are written by hand in `wed/grade_team.py`.

**Line conversion rules (set by hand at entry):**
- "N+" stays N+.
- "over N" on a whole number becomes **(N+1)+**. "over 4 assists" became 5+.
- "over N.5" becomes **(N+1)+**. "over 2.5 threes" became 3+.
- "under N" is graded as staying below N. The Kalshi price is inverted from the N+ market.

**Not captured [TO DO]:**
- **Capper name.** There is no capper column anywhere, so per-capper records cannot be computed.
- **Sportsbook odds and book name.** Only Kalshi prices are stored.
- **The time you collected the line.**

**Moving lines.**
- **[BUILT]** Moved lines are labeled "Moved line" or "Your line was ..." in the note and flagged `moved` in the data.
- **[INTENDED, enforced by convention only]** Only the cappers' picks are graded, and lines move only within the same stat. No code enforces this.

### 3.2 Inputs fetched

| Input | Script | Source | Notes |
|---|---|---|---|
| Player game logs (this season), team, injuries | `wed/fetch.py` → `wed/logs.json` | ESPN `site.web.api.espn.com/apis/common/v3/...` search + gamelog | Takes the first ESPN search hit in the right league |
| Team injury report | `wed/sb.py` → `wed/nba_inj.json` | ESPN injuries endpoint | Read by Claude to write notes and flags; not used in the formula |
| Scoreboard, game times, spreads, totals, moneylines | `wed/sb.py` → `wed/sb.json` | ESPN scoreboard | Spreads were copied **by hand** into `G` in `wed/grade_head.py` lines 16-18 |
| Opponent stats allowed (pts/reb/ast/3PM), with league rank | `wed/opp.py` → `wed/nba_opp.json` | Every completed NBA box score Oct 20 → yesterday | Rank 1 = fewest allowed |
| Kalshi prices | `wed/kalshi.py` → `wed/kalshi.json`; timestamp in `wed/kalshi_ts.txt` | Kalshi public API `/markets?series_ticker=...&status=open` | Mid of bid/ask, in cents |
| Back-to-back teams | Typed by hand: `B2B={...}` in `wed/grade_head.py` line 20 | Claude reads yesterday's schedule | Manual |

### 3.3 Prop grading formula

**[BUILT]** Code: `wed/grade_head.py` `prob()` lines 36-41; `wed/grade_body.py` `add()` lines 2-31.

For a player, stat and threshold `k` (needs k or more):

1. Season values `v` come from the game log. PRA is points + rebounds + assists.
2. `mu` is the mean. `sd = max(stdev(v), 1.0 + 0.25*sqrt(max(mu,1)))`. For the CFB/NFL yardage stats the floor is `0.35*mu+5` instead.
3. **Normal estimate:** `pn = 1 - Phi((k - 0.5 - mu) / sd)`.
4. **Season hit rate, shrunk toward pn:** `ps = (hits_season + 2*pn) / (n + 2)`.
5. **Last-5 hit rate, shrunk toward ps:** `p5 = (hits_last5 + 2*ps) / (min(5,n) + 2)`.
6. **Blend:** `pr = 0.6*ps + 0.4*p5`. For an under, `pr = 1 - pr`.
7. **Pull toward 65:** `pct = 0.8*100*pr + 0.2*65`.
8. **Matchup** (`matchup()` lines 43-48): the opponent's rank in that stat allowed (PRA uses points).
   - Rank ≥ 23 (allows a lot) → **+3**, tagged "good".
   - Rank ≤ 8 → **-5**, tagged "bad".
   - For unders the two are swapped.
9. **Back-to-back:** -3 for points, threes and PRA; -2 for rebounds and assists. Unders flip the sign, so it becomes a bonus.
10. **Small sample:** if `n < 8` games, `pct = 0.7*pct + 0.3*60`.
11. **Caps:** NBA 88, NBA PRA 80, CFB 70. In the Nov 16 NFL script (`mon/grade.py` lines 102-104): NFL 75, anytime TD 62.
12. **Floor and rounding:** `pct = max(5, round(pct))`.

Each grade note shows the inputs in plain words: "Hit X of N this season, Y of 5 last 5 (avg Z)", plus the matchup and back-to-back text when they applied.

**Important properties:**
- **Grades cluster toward 65.** Because of step 7, grades rarely go below about 15, and the formula can only exceed 88 through the cap logic.
- **The 88 cap is a ceiling, not an estimate.** Many 88s are "the formula said higher".
- **Starting role is not modeled.** Minutes, role changes, blowout risk and teammates returning only enter through notes Claude writes by hand. They don't change the number.
- **The Kalshi price does not change the grade.** It is display only. One exception: on Nov 16, 16 grades were pulled toward Kalshi in a version that was later withdrawn. Those are labeled `grade_version = 'v8 ...'` in `model_picks`.

### 3.4 Team lines (moneylines, spreads, totals)

**[BUILT]** Code: `wed/grade_team.py`.

- **NBA moneyline:** `pct = 100*Phi(-spread/12)`, using the sportsbook spread from ESPN, typed into `G`. There is no back-to-back or injury adjustment in the number. This gap was one cause of the Nov 18 Lakers miss.
- **NHL moneyline:** set by hand from the betting line, capped at 69. There is no hockey model.
- **College basketball:**
  - Moneyline: `Phi(spread/11)`.
  - Spread: `Phi((cover margin)/11)`.
  - Total: `Phi((book total - line)/15)`.
  - All capped at 69. There is no college model.
- **These grades are the sportsbook's own line turned into a percent.** They are not an independent model.

### 3.5 Kalshi comparison and the ⚠ rule

**[BUILT]**
- `k` is Kalshi's mid price (cents = percent) for the exact same N+ line, at grading time. For unders it is `100 - price`.
- **Matching** (`KT` in `wed/grade_head.py` lines 9-14): by player name and stat. Only exact thresholds are matched; no interpolation at grading time.
- **Site display** (index.html around line 584 legend; board render around line 1358):
  - `K nn` next to each leg.
  - **⚠ when `pct >= k + 8`.**
- **Note text:** "far below us" when Kalshi is 15+ under our grade, and "well above us" when 15+ over (`wed/grade_body.py` lines 20-22).

**Rules in force (approved Nov 18, provisional):**
- ⚠ legs stay out of Hammer and main tickets. **[BUILT on site text; applied by hand when building tickets.]**
- Hammer filter: grade 80+ and Kalshi within 7. **[INTENDED: applied by hand. The ticket builder's "Hammer check" only checks for ⚠ legs, not 80+/within 7. See section 4.1.]**
- No grade caps or deductions beyond section 3.3 were adopted. The proposed 85+ cap and rebounds deduction were dropped. NFL yardage changes are provisional and not in code.

### 3.6 Suggested tickets

**[BUILT, manual]**
- Hammer and second ticket are chosen by Claude in `wed_patch.py` (`TIX` list). An assertion checks each leg is graded 78+ with Kalshi within 7 and no flag.
- Payout shown is `1 / product(Kalshi prices)`. It is an estimate, not the real Kalshi combo price, which was lower in practice.
- "About X% by our grades" is the product of our grades. It assumes legs are independent, and they often aren't.

### 3.7 Simulations (Beta Test Mode)

**[BUILT, experimental]** Code: `beta/sim.py`. Results go to `beta/beta_tonight.json`, Supabase `model_beta_lines`, and the `BETA` constant in index.html (around line 1717).

**What it checks:**
- **Universe:** every Kalshi NBA player line (points, rebounds, assists, threes, PRA) tonight with ask between **50¢ and 60¢** (about +100 to -150), bid > 0 and spread ≤ 5¢.
- **Who's excluded:**
  - players with fewer than 8 games
  - players on a hand-typed OUT list
  - (Top 15 only) players on a hand-typed questionable list
- **This is not limited to the cappers' picks.** It scans the whole market.

**Per game, 1,000 runs (`N=1000`, lines 44-62):**
1. Draw a shared game factor `Normal(1, 0.04)` and a team factor `game * Normal(1, 0.07)` for each team.
2. For each player line, draw one game from his season log. The last 5 games are weighted 2x.
3. Scale it by the team factor:
   - ±3% for a soft or tough matchup (same rank cutoffs as grading)
   - ×0.97 for a back-to-back on points, PRA and threes
   - rebounds and assists use `factor^0.7`
4. Add noise: `Normal(0, 0.6)` for threes, rebounds and assists; `Normal(0, 1.5)` for points and PRA.
5. Count a hit when `value >= k - 0.5`.

**Outputs:**
- `sim` = hit share in %.
- `se` = Monte Carlo error, about ±1.2 to 1.6.
- `be` = break-even = `ask + 0.07*ask*(1-ask)` (Kalshi's fee formula), in %.
- `edge` = sim - be.
- `unc` = sample uncertainty = `1.96*sqrt(max(p(1-p), 0.04)/n_games)`. Usually ±20 to 25 points.
- Top 15 = largest edge, one line per player, max 2 per game.

**What it means:** it is the same season-log information our grade uses, re-sampled. It adds a way to model same-game correlation. It does **not** add new information for a single leg. The sample uncertainty is larger than every edge it has shown.

**Track record:** Nov 18 only, 9-6. Top 5 went 5-0, lines 6 to 15 went 4-6, flat ROI +2.7% after fees. The sim averaged 72% against 60% actual, so it reads high.

### 3.8 Other analysis

| Analysis | Code | What it does | Status |
|---|---|---|---|
| Result grading | `wed/res/fetch.py`, `wed/res/grade.py` | ESPN box scores. N+ → value ≥ N; "under N" → value < N; ML by score; spread/total margin, exact = push | **[BUILT]** |
| Full-history Kalshi backfill | `audit/kxfetch.py`, `audit/kmatch.py`, `audit/kprice.py`, `audit/enrich.py` | Settled Kalshi markets Nov 4-17; matches legs by name + threshold; price = last hourly quote before tip | **[BUILT, one-off]**. 745 of 1,060 legs priced; 136 interpolated between two lines |
| Audit statistics | `audit/full.py`, `audit/beta_bt.py` | Buckets, Wilson 95% ranges, Brier score, calibration, same-game and ladder correlation, game-cluster bootstrap, time-split out-of-sample tests | **[BUILT, one-off]**. Not re-run automatically |
| Opponent ranks | `wed/opp.py` | Recomputed from all box scores | **[BUILT]**, re-run by hand |

### 3.9 How the site turns this into pages

The site source is a single HTML file edited in the scratchpad (`bettordays-hq.html`). `buildsite.py` wraps it into repo `index.html`, then writes `board.json` (latest board, for the app) and `stats.json` (tiles). Line numbers below are in repo **`index.html`**.

| Page / feature | Data | Code (index.html) | Status |
|---|---|---|---|
| Home board (current night) | `const WE18` (board rows), `WETIX` (tickets), `CUR=WE18` | ~1463-1465; `boardFilters()` ~1427; ⚠ rendering `pct>=k+8` ~1358 onward | **[BUILT]** |
| Ticket builder (/easy) | current board | ~1645-1715. Our grades, record at those grades (`recP` ~1661, from ROWS grade bands with 20+ legs, otherwise the grade itself), Kalshi product (each price clamped 1 to 99), payout `1/Πk`, warnings ~1677-1689, Hammer check ~1690/1693 | **[BUILT]** |
| Record explorer (/record) | `record.json` | ~1785. W-L, n, Wilson 95% range, small-sample flag (<30) | **[BUILT]**. Kalshi price for Nov 4-17 is tip-off; Nov 18 on is grading-time |
| Research hub | `ROWS` (~1116) | hub `CARDS` ~1735; What hits `rsCats` ~1844, Grade tiers `rsTiers` ~1847, nights `rsDays` ~1849 / `rsDays80` ~1754, lines `rsLines` ~1852, clues `rsClues` ~1856 | **[BUILT]**. Some clue text is hard-coded |
| Perfect parlays: tonight's attempt + ticket record + backtest + hindsight | `ROWS`, day boards, ticket constants | `beta()` ~1886, `TK` ~1721, `rsBack` ~1893, `rsToday` ~1897, hindsight `build()` ~1868 | **[EXPERIMENTAL]** |
| Beta Test Mode | `BETA` | ~1717 + `btTop`/`btMeth` | **[EXPERIMENTAL]** |
| Results recaps | hand-written sections `review11`-`review18` | static HTML | **[BUILT, manual]** |
| Method page (thesis, calibration, edge map, rulebook) | static | ~989-1060 | **[STALE]**. Written around Nov 9 ("5 days of data"); does not reflect current rules |
| Founders list | Supabase `founders_waitlist` insert + `waitlist_count` RPC | ~1810-1818 | **[BUILT]** |
| Member app (/app) | Supabase `picks`, `profiles`, rooms, etc.; reads `/board.json` | `app.html` | **[BUILT]**. Member picks and leaderboard are separate from the model record |
| Kalshi account sync | `api/kalshi-key.js`, `api/kalshi-sync.js`, `lib/server.js` | encrypted key storage, imports positions | **[BUILT, not verified in this task]**. Needs `KEY_ENCRYPTION_SECRET` |
| Email announcements and feedback | `api/announce.js`, `api/feedback.js` | needs `RESEND_API_KEY` | **[Depends on env vars; not verified]** |

### 3.10 How results are tracked over time

- **Source of truth [BUILT]:** Supabase `model_picks`. One row per pick with:
  - `slate_date`, `posted_at` (grade time), game, player, market, stat, direction, line
  - `capper_line`, `moved`, `grade`, `grade_version`
  - `kalshi_price_grade` + `_ts`, `kalshi_price_close` + `_ts`
  - `result` (W/L/P/V), `actual`, `result_source`, `status`, `data_gaps`
- **Corrections** go to `model_pick_corrections`. Tickets go to `model_tickets`; beta lines to `model_beta_lines`.
- **Coverage:**
  - Nov 4 to 18: 1,146 graded legs (743-403). Graded 70+: 343-99.
  - Grading timestamps exist only from Nov 18. Nov 16-17 have a grading-time Kalshi snapshot.
- **The site does not read the database.** `ROWS` and `record.json` are written by scripts at the same time as the database load. **[TO DO]** Generate them from the database so they can't drift.

---

## 4. Limitations and ways the numbers can mislead

1. **Samples are small and correlated.** About 2.3 legs per game, and many player ladders (the same player at 2-4 lines). Ladder legs share a result 77% of the time. The effective sample is far smaller than the leg count.
2. **The market has been more accurate than our grades.**
   - Nov 4-17 Brier score: Kalshi 0.189, ours 0.211 (lower is better).
   - Nov 18: Kalshi 0.234, ours 0.239.
   - Buying every leg at Kalshi's tip price returned about +2% before fees. **No proven edge.**
3. **Calibration.** 85+ grades hit 72%; grades under 75 hit more often than graded.
4. **The "hit rate" is on the cappers' picks only.** It can't be generalized to every line.
5. **Many steps are manual:** transcription, back-to-back list, spreads, injury flags, ticket building. Typos are possible and have happened (a stat mis-parsed as assists, a dropped line).
6. **Hindsight.** The "Perfect parlays" hindsight builds and the Beta backtest use rules written after seeing the same nights. The site says this.
7. **Mixed price timing.** The record mixes tip-off prices (Nov 4-17) and grading-time prices (Nov 18+).
8. **Unrecorded history.** Before Nov 13 the original capper line and the moved flag were mostly not recorded. Before Nov 8 there are no game times or notes.
9. **Stale content.** The Method page and some Research clue sentences quote numbers from early November.

### 4.1 Known code inconsistencies (found while writing this, not fixed)

1. **Ticket builder "Hammer check"** (index.html line 1690: `const ham=!warn.length`) passes any ticket with no ⚠ legs. It does not check grade 80+ or Kalshi within 7, so it can call a ticket Hammer eligible when our rule would not.
2. **Research "Lines we moved"** (`rsLines`, line 1852) counts rows where `boost` is set. 169 rows from Nov 5 to Nov 17 have it. The Nov 18 rows all have `boost: 0`, even though Nov 18 moved lines are flagged `moved` in Supabase. Nov 18 moved lines are missing from that segment.
3. **Perfect parlays "last night"** (`rsToday`, line 1897+) shows the Beta 3 rebuilt by the backtest (`bt`), not the ticket that was actually posted that night. The two can differ (Nov 18: the backtest used a different Flagg line than the posted attempt).
4. **Method page** (around line 990) still quotes "5 days of data" and early rules.
5. **Some Research clue sentences** have hard-coded numbers that do not update when ROWS changes.

---

## 5. A vs B vs C summary

**A. What the code does today**
- Grades capper props with the formula in 3.3, and team lines from sportsbook lines (3.4).
- Shows the Kalshi price and the ⚠ flag.
- Grades results from box scores.
- Stores everything in Supabase.
- Runs a 1,000-run-per-game simulation on Kalshi near-even lines.
- Renders the board, ticket builder, record explorer, research hub, Beta pages and app.

**B. What we intended or decided but is enforced only by hand**
- Cappers' picks only, same-stat line moves.
- Hammer = 80+ and Kalshi within 7, no ⚠.
- No leg on more than 2 tickets.
- A second injury check before each tip window.
- Back-to-back factored into team moneylines.
- Beta Test Mode stays market-wide (your call on Nov 19).

**C. To build or verify**
1. Put the pipeline scripts in the repo, with one entry point per step.
2. A pick parser for pasted lists, plus capper name, book odds and collection time fields.
3. Generate `ROWS` and `record.json` from Supabase.
4. Fix the items in 4.1, and enforce the Hammer filter and the 2-ticket concentration rule in the ticket builder.
5. Back-to-back and injury inputs for team moneylines.
6. Automate the lock-time Kalshi snapshot and store it as a second price.
7. Rewrite or retire the stale Method page.
8. Verify the Kalshi sync and email env vars in Vercel.

---

## 6. Code map (quick reference)

| Stage | File | Function / block |
|---|---|---|
| Player data | `scratchpad/wed/fetch.py` | `one()` |
| Scoreboard + injuries | `scratchpad/wed/sb.py` | top level |
| Opponent ranks | `scratchpad/wed/opp.py` | `box()` + rank loop |
| Kalshi prices | `scratchpad/wed/kalshi.py` | `get()` |
| Prop grade | `scratchpad/wed/grade_head.py` | `prob()`, `matchup()` |
| Prop grade + notes | `scratchpad/wed/grade_body.py` | `add()` |
| Your picks (transcribed) | `scratchpad/wed/grade_list.py` | `add(...)` calls |
| Team lines | `scratchpad/wed/grade_team.py` | `team()`, `cbb()`, `kinterp()` |
| Publish board | `scratchpad/wed_patch.py`, `scratchpad/buildsite.py` | patch + build |
| Grade results | `scratchpad/wed/res/fetch.py`, `scratchpad/wed/res/grade.py` | `find()`, main loop |
| Simulation | `scratchpad/beta/sim.py` | per-game loop |
| History audit | `scratchpad/audit/*.py` | `full.py` `rule_test()`, `boot()` |
| Site | repo `index.html` (built from `scratchpad/bettordays-hq.html`) | see 3.9 |
| App | repo `app.html` | `loadBoard()` line 159 |
| API | repo `api/*.js`, `lib/server.js` | handlers |
| Database | Supabase `ndcsjhetuasijbgpfhwj` | `model_picks`, `model_pick_corrections`, `model_tickets`, `model_beta_lines`, `founders_waitlist` |
