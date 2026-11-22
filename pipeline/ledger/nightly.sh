#!/bin/bash
# After a night is graded (daily/<date>/results.json written): rebuild the ledger rows, capture closing prices, push.
# Then load into the database with:  select public.ledger_load('<raw GitHub URL of pipeline/ledger/ledger_rows.json at the new commit>');
# Loading fills results and closing prices; the database rebuilds that night's scorecard on its own (trigger on leg_ledger).
set -e; cd "$(dirname "$0")/.."; D=$1
python3 ledger/legs.py && python3 ledger/players.py && python3 ledger/features.py && python3 ledger/kclose.py "$D" && python3 ledger/rows.py
python3 ledger/scorecard.py
