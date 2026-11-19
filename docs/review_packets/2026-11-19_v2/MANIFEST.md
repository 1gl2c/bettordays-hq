# Data packet manifest: BettorDays_data_packet_2026-11-19_v2

Give every model run (ChatGPT, Gemini, Grok, Claude) **exactly these 8 files**: this manifest plus the 7 below. If any count or checksum differs, the runs aren't comparable. Rebuild or re-attach.

| # | File | Contents | Bytes | SHA-256 (first 16) |
|---|---|---|---|---|
| 1 | `README_DATA_PACKET.md` | 159 lines | 9,637 | `96444bdfb1684b64` |
| 2 | `picks_history.csv` | 1322 rows, 45 columns | 605,625 | `6e7a7a7c6c9fdfc6` |
| 3 | `tickets_history.csv` | 61 rows, 7 columns | 14,498 | `efa6961a4b27e235` |
| 4 | `corrections.csv` | 21 rows, 6 columns | 2,985 | `b052f3e5461c6f52` |
| 5 | `beta_sim_lines.csv` | 224 rows, 33 columns | 119,380 | `222fe5c8e2c1d0d1` |
| 6 | `perfect_parlays_backtest_and_hindsight.csv` | 328 rows, 7 columns | 55,252 | `8b2162f54e47769c` |
| 7 | `todays_picks.csv` | 50 rows, 19 columns | 16,367 | `6bfc96079ca4091c` |
| 8 | `MANIFEST.md` | this file | | |

## Load check (every model computes these before Part B)

| Check | Expected |
|---|---|
| `picks_history.csv` rows | 1,322 (slates Nov 4 to 18) |
| `d_record_status`: settled_win / settled_loss / push / void / unresolved | 743 / 403 / 8 / 9 / 159 |
| `d_in_win_loss_record = TRUE` | 1,146 |
| Settled W-L with `grade` ≥ 70 | 343-99 |
| Settled W-L with `grade` ≥ 80 | 163-48 |
| Non-blank `d_kalshi_tip_observed` / `d_kalshi_tip_estimated` / `d_kalshi_grade_observed` / `d_kalshi_grade_estimated` | 623 / 136 / 225 / 11 |
| `d_grade_uses_market = TRUE` | 76 |
| `d_head_to_head_eligible = TRUE` | 184 (Nov 16: 71, Nov 17: 38, Nov 18: 75) |
| `beta_sim_lines.csv` rows | 224 (15 `shown_on_site`, 209 `outcome_backfilled`) |
| Beta `outcome_class` W / L / V | 123 / 96 / 5 (shown 15: 9 / 6 / 0) |
| Beta distinct games / players | 12 / 127 |
| `tickets_history.csv` rows | 61 |
| `todays_picks.csv` rows | 50 (in the order submitted; 47 with a system grade) |

Built by `pipeline/review_packet/build_packet.py` (history through 2026-11-18) and `pipeline/thu/todays_picks.csv` (slate 2026-11-19).
