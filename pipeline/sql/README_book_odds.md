# Sportsbook odds feed (EV engine, Nov 20 2026)

Applied to Supabase project ndcsjhetuasijbgpfhwj as migrations `book_odds_feed` and `book_novig_view`.

- `book_odds`: raw NBA player-prop prices (DraftKings, FanDuel, BetMGM, Caesars and the rest of The Odds API's US region).
- `pull_book_odds(markets, hours)`: security definer, not callable from the browser. Reads the API key from
  Supabase Vault secret `odds_api_key`, so the key never appears in code, chat or Vercel.
- `book_novig`: per player line, each book's vig removed, median across books = fair chance of the Over.

Cost: The Odds API charges credits per market per region per event. 4 markets x 1 region x ~10 games = about 40
credits a pull. Free plan 500/month (about 12 pulls) to test; $30 plan 20,000/month covers 2 pulls a day with room.

EV use: where a Kalshi rung matches a book line, true chance = no-vig consensus; EV = fair / (Kalshi price + fee) - 1.
Track the consensus Brier against Kalshi on our legs for a week before trusting it over the favorite-edge mode.
