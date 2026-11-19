# Grading pipeline (preserved copy)

These are the exact grading, results, simulation, audit and site-build scripts that produced the BettorDays boards from Nov 8 to Nov 18, 2026. They were copied here on Nov 19 from Claude's temporary session folder. **None of the logic was changed during the move.** Every file was checked byte for byte against the original.

The full system description is in `docs/PICK_ANALYSIS_SYSTEM.md`.

## How to run

Run every script **from this folder** (`pipeline/`). They use paths relative to it, such as `wed/logs.json`.

```
cd pipeline
python3 wed/grade.py        # grade the Nov 18 board        -> wed/wed.json
python3 wed/res/grade.py    # grade results from box scores  -> wed/wed_graded.json
python3 beta/sim.py         # Beta Test Mode simulation      -> beta/beta_tonight.json, beta/all_lines.json
python3 audit/full.py       # full-history audit             -> audit/full_out.json
python3 buildsite.py        # build ../index.html, ../board.json, ../stats.json from bettordays-hq.html
```

These steps use only the saved input files. The fetch scripts call ESPN and Kalshi and **overwrite** those inputs:

```
wed/fetch.py
wed/sb.py
wed/opp.py
wed/kalshi.py
wed/kalshi_lock.py
wed/res/fetch.py
beta/fetch.py
beta/kalshi2.py
audit/kxfetch.py
```

Run them only when building a new night, in a new day folder.

`buildsite.py` writes to the absolute path `/home/claude/bettordays-hq/`. That is where the repo lives in Claude's workspace.

## What's here

| Path | What it is |
|---|---|
| `bettordays-hq.html` | **The website source.** `index.html` at the repo root is generated from it by `buildsite.py`. Edit this file, not `index.html`. |
| `buildsite.py` | Builds `index.html`, `board.json`, `stats.json`. |
| `wed/` | The latest full daily set (Nov 18). Scripts, the inputs they used, and their outputs. |
| `wed/res/` | Results grading for Nov 18. |
| `beta/` | Beta Test Mode simulation (Nov 18). |
| `mon/` | Nov 16 set. The only script with the NFL caps (75) and anytime-TD cap (62). |
| `tue/` | Nov 17 set. Needed by `audit/close.py`. |
| `audit/` | Full-history Kalshi backfill and audit (Nov 4 to 17), including the raw settled-market downloads in `audit/kx/`. |
| `sun/`, `sat/`, `fri/`, `study/` | Older nights: scripts and graded outputs only. Their raw inputs were not kept, so they can't be re-run. |
| `*_patch.py`, `upd*.py`, `patch*.py`, `p19/` | One-off scripts that patched the site for a given night. Kept as a record. |
| `wed_patch.py` | Publishes the Nov 18 board and tickets into the site source. |

## How `wed/grade.py` is built

`wed/grade.py` is the five parts below joined in order, plus three lines that write `wed/wed.json`:

1. `grade_head.py`
2. `grade_picks.py`
3. `grade_body.py`
4. `grade_list.py`
5. `grade_team.py`

The parts are kept so each piece can be read on its own. **`grade.py` is the file that actually ran.**

## Known differences between a re-run and what was published

Re-running gives the same output as the original scripts. Some saved outputs were then edited by hand, so a re-run doesn't match them:

- **`wed/wed.json`** (Nov 18): 6 rows were edited after grading, at 3:45 PM PT, when Maxey and Wade were ruled out. Their legs were set to grade 0 and flagged OUT, and the 76ers ML was flagged Q. See commit `7b76388`. A re-run gives their pre-news grades.
- **`mon/mon.json`** (Nov 16): 15 grades were pulled toward the Kalshi price, and one note was reworded, after the script ran. That pull is not in `mon/grade.py`. It was later withdrawn as a method, and those rows are labeled `v8` in the database. A re-run gives the un-pulled grades.
- **`beta/beta_tonight.json`** stores the time the simulation ran (`sim_ts`), so that field changes on every run. Everything else matches because the random seed is fixed (`random.seed(18)`).

## Known issue (not fixed, so behavior is preserved)

`wed/grade_body.py` line 28 sets `moved=True` whenever a pick has `orig` (a notation rewrite like "over 4 assists" to "5+ assists"), not only for real line moves. On Nov 18 that put 10 notation-only rows into `model_picks` as `moved`. These rows have `capper_line` filled in. The site's "Lines we moved" count uses only real moves. See the system doc.
