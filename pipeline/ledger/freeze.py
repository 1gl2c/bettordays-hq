"""Run right after a day's board is published: saves the board exactly as posted (daily/<date>/v7_merged_pick.json) and the
leg -> Kalshi event map, so later re-merges (injury checks, price refreshes) can never change what the ledger calls pick time.
Refuses to overwrite an existing freeze. Usage: python3 ledger/freeze.py 2026-11-23 [path/to/kmatch.json]"""
import os, shutil, sys
D = sys.argv[1]; dst = f'daily/{D}/v7_merged_pick.json'
if os.path.exists(dst): sys.exit(f'{dst} already frozen, not touching it')
shutil.copy(f'daily/{D}/v7_merged.json', dst)
if len(sys.argv) > 2 and not os.path.exists(f'daily/{D}/kmatch.json'): shutil.copy(sys.argv[2], f'daily/{D}/kmatch.json')
print('frozen', dst)
