# BettorDays nightly publish checklist

Every step runs every night, in this order. A board is not "live" until steps 6 and 7 are done.
Nov 27: added after the sim and the Perfect 3/10x Kalshi buttons were missed and Ace had to catch them.

1. **Lines**: clean Ace's capper lines into `<day>/legs.json`, write the agent prompt to `daily/DATE/`.
2. **Market data** (while the agents run): Kalshi pull and match, our system grade, The Odds API pull
   (`pull_book_odds_sport`, go easy on credits), `book_fair.json`, every posted line to `daily/DATE/book_lines.txt` and `book_main.txt`.
3. **Merge** the four agent replies: `<day>/merge<dd>.py` -> `daily/DATE/v7_merged.json`.
4. **Board**: `python3 v8/publish_v8.py ...` with tonight's notes (injuries, why the Hammer passed if it did).
5. **Tickets**: Daily 2x (points and assists lead, rebounds only with the books above Kalshi), Edge Lab scan,
   Miracle ladder (skip started games), paper tracker row.
6. **Sim**: `python3 beta/run_day.py DATE` then `python3 beta/publish_day.py DATE`. Picks up games, tips,
   back-to-backs, injuries and fresh Kalshi prices on its own; games that already tipped are skipped.
7. **Kalshi buttons**: `python3 kalshi_autolinks.py DATE make`, run `daily/DATE/autolinks.sql` through the database
   tool, save the rows to `daily/DATE/autolinks_result.json`, then `python3 kalshi_autolinks.py DATE apply`.
   Covers tonight's tickets, the Miracle, Edge Lab, the Daily 2x and the Perfect 3 and 10x. Re-run `make` after any
   change: it should print nothing, meaning every parlay has a button.
8. **Build and check**: `python3 buildsite.py && node prerender_numbers.cjs && python3 buildsite.py`, open the page,
   confirm the status line, the Hammer card, the sim and every Open on Kalshi button.
9. **Commit and push**, then X posts (Typefully needs Ace's yes for the day).
10. **Night**: grade everything, ledger nightly, hammer_learn, load SQL, nightly report.
