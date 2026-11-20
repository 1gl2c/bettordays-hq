# Engine v7 daily flow (from Nov 20, 2026)

Rules: `docs/DAILY_ENGINE_V7.md`. Rule constants and logic: `v7lib.py`.

| PT | Who | Step |
|---|---|---|
| by 12:15 PM | Ace | Sends the cappers' picks to Claude. |
| by 12:35 PM | Claude | Grades them with the usual scripts (system grade + Kalshi), then `python3 v7/build_lines_v7.py <day folder>/<day>.json DATE` and pushes `pipeline/daily/DATE/v7_lines.txt` and `v7_slate.txt`. The lines file has no BettorDays grade, so the models stay blind to it. |
| 12:40 PM | Ace's Mac (launchd) | `~/bettordays/engine/bd_daily_v7.sh` downloads the lines, runs ChatGPT, Gemini, Grok and Claude through Hermes at once, 40 minutes max each. |
| about 1:20 PM | Ace's Mac | Replies saved in `reviews/DATE/` (and pushed to `pipeline/daily/DATE/replies/` if a repo clone is set up). Mac notification. |
| 1:30 PM | Ace | Tells Claude "v7 replies for DATE are ready" (or drags the four .md files in). |
| by 2:30 PM | Claude | `python3 v7/merge_v7.py DATE <replies dir>`, then `python3 v7/publish_v7.py ...`, `python3 buildsite.py`, load `daily/DATE/v7_db.sql`, commit, push. Vercel deploys in about a minute. |

What publish does: board = GREEN and YELLOW legs (and no-Kalshi legs, max 75) published 70+; published grade = models' median capped at Kalshi + 7; REMOVED legs (median 8+ above Kalshi) only on Research, Market check; Hammer per v7; Safe, Core and Stretch tickets from GREEN legs on Research; every leg with each model's number saved to `model_v7_legs`.

If fewer than 2 models return a result block, `merge_v7.py` stops and says so. Then the board goes up on the standard grading, labeled as such.
