# BettorDays historical data packet (v2)

- **Built:** Nov 19, 2026, by `pipeline/review_packet/build_packet.py`.
- **Sources:** the BettorDays pick database (Supabase tables `model_picks`, `model_tickets`, `model_pick_corrections`, `model_beta_lines`) and the site's Perfect Parlays calculations.
- **History covers:** slates Nov 4 to Nov 18, 2026.
- **Nothing in these files was estimated or filled in.** A blank cell means the value was never recorded. Columns starting with `d_` were derived by the build script from the other columns, with rules described here.

`MANIFEST.md` lists the exact files, row counts and checksums every model run must receive.

## 1. The record: which rows count in which statistic

`picks_history.csv` has **1,322 rows**, one per graded capper pick. **The 743-403 record uses only the 1,146 settled rows.** The other 176 are kept so nothing is hidden. They are excluded from every win-loss statistic.

| `d_record_status` | Rows | In W-L record? | In hit-rate and grade-band stats? | Notes |
|---|---|---|---|---|
| `settled_win` | 743 | Yes | Yes | |
| `settled_loss` | 403 | Yes | Yes | |
| `push` | 8 | No | No | Landed exactly on the number. Report separately. |
| `void` | 9 | No | No | Player did not play. Report separately. |
| `unresolved` | 159 | No | No | No result was ever logged. Reasons below. |

The 159 unresolved rows, by `d_unresolved_reason`:

| Reason | Rows |
|---|---|
| Graded before games, result never logged | 147 |
| Player out or flagged to skip before games, no result logged | 7 |
| An actual stat appears in the note, but no W/L was entered | 2 |
| Game started before the list arrived, never graded | 2 |
| Player ruled out; the note says void, but the result field was never set | 1 |

By date, 48 of them are Nov 8, 28 Nov 9, 19 Nov 10, and 34 Nov 16.

**Bias warning.** Unresolved rows average a grade of 51, against 62 for settled rows, and only 11% of them are 70+ (39% of settled rows). The settled record is therefore weighted toward higher grades. Results for low grades rest on a less complete sample.

Rules for every statistic:
- **Win-loss and hit rate:** `d_in_win_loss_record = TRUE` only (1,146 rows).
- **Pushes and voids:** reported as their own counts. Never folded into wins or losses.
- **Unresolved rows:** never counted, never imputed.

## 2. Kalshi prices: four separate kinds, never mixed

| Column | What it is | Rows (settled rows) | Dates |
|---|---|---|---|
| `d_kalshi_tip_observed` | Price just before tip-off: the last hourly quote before the game, pulled later from Kalshi's price history. A direct quote for that exact line. | 623 (603) | Nov 4 to 17 |
| `d_kalshi_tip_estimated` | Tip-off price **estimated** between the two nearest Kalshi lines, because that exact line was not listed. Not a quote. | 136 (134) | Nov 4 to 17 |
| `d_kalshi_grade_observed` | Price quoted **when we graded** the pick, hours before tip. A direct quote. | 225 (219) | Nov 16 to 18 |
| `d_kalshi_grade_estimated` | Grading-time price estimated between two Kalshi lines. | 11 (11) | Nov 16 to 18 |

Timestamps are in `d_kalshi_tip_ts` and `d_kalshi_grade_ts`. The raw columns `kalshi_price_close` and `kalshi_price_grade` are kept as stored, but use the split columns.

**Comparison rule.**

An accuracy comparison between our grade and Kalshi (Brier score, calibration, "who was closer") is only valid when all four of these hold:
1. The same picks.
2. The same settled outcomes.
3. A Kalshi price from the same moment the grade was made.
4. A grade that did not itself use the Kalshi price.

`d_head_to_head_eligible = TRUE` marks those rows: **184 rows** (Nov 16: 71, Nov 17: 38, Nov 18: 75), from 30 games.

- **Tip-off prices are hours later than our grades** and include later news, so a grade-vs-tip comparison is not like for like. Tip-off prices can be used to describe how Kalshi's own prices performed, not to rank our grade against them.
- **Estimated prices** should be left out of any accuracy claim, or reported separately.

`d_grade_uses_market = TRUE` (76 rows) marks grades that were taken from Kalshi or pulled toward it. These can never count as an independent grade:
- 47 rows: graded at the Kalshi price (markets with no model of our own)
- 16 rows: the withdrawn v8 pull toward Kalshi
- 13 rows: Nov 16 and 17 NBA team lines graded as the average of a spread model and Kalshi

## 3. Files

### `picks_history.csv` (1,322 rows, 45 columns)

Original database fields:

| Field | Meaning |
|---|---|
| `pick_key` | Unique id. |
| `slate_date` | Night of the games. |
| `game_time_text` | Tip time as text, Pacific. Blank Nov 4 to 7. |
| `sport` | Sport label. CBB/NCAAB and CFB/NCAAF are the same sports under two labels. Some rows on Nov 8 to 10 have no sport. |
| `event` | Game. **Often team-level only on Nov 4 to 7.** |
| `player`, `market`, `stat`, `direction`, `line`, `line_style` | Parsed fields, sometimes blank. `direction` is `o` (over or N+) or `u` (under). `line_style` is `alt` (bought-down) or `reg`. |
| `pick_text` | The pick as shown on the site. |
| `capper_line` | The capper's original wording. Only 10 rows. |
| `moved` | Unknown before Nov 11. **TRUE on Nov 18 also for 10 notation rewrites.** Use `d_real_line_move`. |
| `grade`, `grade_version` | Our grade (5 to 88) and the method version. |
| `b2b`, `matchup` | Back-to-back flag and matchup tag. Only recorded Nov 16 to 18, partly on Nov 16 and 17. |
| `kalshi_*` | Raw stored Kalshi fields. Use the `d_kalshi_*` columns (section 2). |
| `result` | W, L, P, V, or blank. |
| `actual` | The settling stat. Missing for many rows. |
| `status`, `data_source`, `data_gaps` | Row status, where the row came from, and what is missing. |
| `notes` | Our published reasoning. **Not independent evidence.** |

Derived fields:

| Field | Meaning |
|---|---|
| `d_record_status`, `d_unresolved_reason`, `d_in_win_loss_record` | Section 1. |
| `d_game_key` | Same-game grouping. Team-level on Nov 4 to 7. |
| `d_ladder_key` | The same player, stat and direction on one night. |
| `d_real_line_move` | A real line move, not a notation rewrite. Blank when unknown. |
| `d_kalshi_*`, `d_grade_uses_market*`, `d_head_to_head_eligible` | Section 2. |

### `tickets_history.csv` (61 rows)

Suggested and played parlays, Nov 9 to 18.
- `played` = TRUE means Ace placed it. FALSE means it was suggested.
- `result` codes `CO` and `?` appear once each. Their meaning was never recorded, so treat them as unknown. One row has no result.
- Stakes and real payouts are mostly not recorded.
- Nov 18 includes the posted Beta 3 (W) and Beta 10x (L). They were recovered from the site versions published before tip-off.

### `corrections.csv` (21 rows)

Every after-the-fact correction, with the reason.

### `beta_sim_lines.csv` (224 rows; Nov 18 only)

Every Kalshi NBA player line that night priced 50 to 60 cents, with Beta Test Mode's simulated hit rate (1,000 simulated games per game).

**Where the predictions came from (`pregame_record`):**
- **15 lines** (`shown_on_site = TRUE`, `rank` 1 to 15) were published on the site, and committed to GitHub at 3:00 PM PT Nov 18, from a simulation run at 2:58 PM.
- **209 lines** (`shown_on_site = FALSE`) come from a file saved at 3:44 PM PT Nov 18, before the first tip at 4:00 PM. That was a re-run of the same simulation on the same pregame inputs, and it reproduces the 15 published lines exactly. The 209 were **not published** before the games.

**How the outcomes were recorded:**
- The 15 were graded the next morning from box scores.
- The 209 were backfilled on Nov 19 (`outcome_backfilled = TRUE`) from two sources: the ESPN box score and Kalshi's own settlement of the exact market.
  - 204 settled lines: both sources agree on every one.
  - 5 voids: the player did not play, and Kalshi settled those markets as no contest ("scalar").
  - No line was unverifiable. No push is possible, because every line is N+ on a whole number.

**Totals:** 123 W, 96 L, 5 V. Shown 15: 9-6. Backfilled 209: 114-90, plus 5 voids.

**These are not 224 independent observations.**
- They come from 12 games and 127 players (`d_game_key`, `d_player_key`).
- Many players have several lines (points, rebounds, threes, PRA), which move together.
- One night's game flow affects every line in that game.

Count effective samples by game and by player.

### `perfect_parlays_backtest_and_hindsight.csv` (328 rows)

- **Backtest rebuilds:** past nights replayed with rules written after seeing them. These flatter the rules, and have no Kalshi prices.
- **Hindsight builds:** legs chosen after results were known. Descriptive only.
- **Neither is a forward-looking record.**

### `todays_picks.csv` (50 rows)

The slate under review: picks in the order submitted, our system grade, the Kalshi price at grading time, and flags. Capper, sportsbook, odds and capture time are blank because they weren't provided.

## 4. Things that make naive analysis wrong

1. **Correlation.** Same game, ladders, and the same player at several stats. Count effective samples, not legs.
2. **Price timing.** Section 2. No head-to-head claim outside `d_head_to_head_eligible`.
3. **Selection.** These are paid cappers' picks, not a random sample of lines.
4. **Missing fields.** No capper names, sportsbook odds, line capture times or game start timestamps.
5. **The grade changed over time** (`grade_version`). Some grades used the market (`d_grade_uses_market`).
6. **Hindsight.** The ⚠ rule, the Hammer filter and the Perfect Parlays rules were set after looking at this same data. Only later nights can test them.
7. **Unresolved rows skew low** (section 1).
