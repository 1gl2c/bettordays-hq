# BettorDays ledger (our own data, Phase 1 and 2)

**What it is:** one permanent row per graded leg in `public.leg_ledger` (Supabase), frozen at pick time.
- Pick-time columns can never change. Rows can never be deleted. A database trigger enforces both.
- Only the closing price and the result get filled in later.

**What each row holds:**
- the line, the Kalshi price at pick time (with its time), the sportsbook no-vig price
- every model's grade and reasoning, our system grade and its note
- the player's pre-game stats (last 5, season, hit rates) and minutes
- rest days and back-to-back, the injury report snapshot (self, teammates, opponents)
- opponent, home or away
- closing Kalshi price, result

**No-leak rules:**
- Game-log rows count only if that game started before the leg's game.
- Injury snapshots count only if saved before the game started.
- A leg counts in the scorecard only if its Kalshi price was taken before the game (`priced_pregame`).

## Daily steps
1. After the board is posted: `python3 ledger/freeze.py <date> <kmatch.json>`. This freezes the board as posted.
2. After grading writes `daily/<date>/results.json`: `ledger/nightly.sh <date>`, commit and push, then run `select public.ledger_load('<raw URL of ledger_rows.json at that commit>');`.
3. Loading results makes the database rebuild that night's scorecard by itself (`ledger_scorecard`, `ledger_clv`).

## Phase gates
- Phase 3 (our own model, starting from Kalshi's price, walk-forward tested) waits for 2,000 graded legs with a pregame market price. `scorecard.py` prints the count.
- Nothing from a model touches the board until it beats Kalshi on games it never saw.
