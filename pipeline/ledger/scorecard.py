"""Nightly scorecard, readable copy (the database builds the same numbers by itself in ledger_scorecard / ledger_clv).
Only legs graded W or L whose Kalshi price was taken before the game count. Each source is scored on exactly the legs where
both it and Kalshi had a number. AI grades made after the AI looked up market prices (Nov 19 panel) are left out.
Also prints the Phase 3 gate: graded legs with a pregame market price (2,000 needed)."""
import json
R = json.load(open('ledger/ledger_rows.json'))
SRC = [('Kalshi', 'kalshi_pick'), ('Sportsbooks', 'books_pick'), ('Our blended grade', 'grade_published'), ('Our system', 'grade_system'),
       ('ChatGPT', 'grade_chatgpt'), ('Gemini', 'grade_gemini'), ('Grok', 'grade_grok'), ('Claude', 'grade_claude')]
B = [r for r in R if r['result'] in ('W', 'L') and r['priced_pregame'] and r['kalshi_pick'] is not None]
def card(rows, label):
    print(f'\n{label}: {len(rows)} graded legs priced before the game')
    print(f"{'Source':<20}{'legs':>6}{'score':>8}{'Kalshi same legs':>18}  verdict")
    for name, col in SRC:
        x = [r for r in rows if r[col] is not None and not (r['grades_saw_market'] and col in ('grade_chatgpt', 'grade_gemini', 'grade_grok', 'grade_claude'))]
        if not x: continue
        y = lambda r: 1 if r['result'] == 'W' else 0
        b = sum((r[col] / 100 - y(r)) ** 2 for r in x) / len(x); k = sum((r['kalshi_pick'] / 100 - y(r)) ** 2 for r in x) / len(x)
        v = '' if col == 'kalshi_pick' else ('beats Kalshi' if b < k else 'worse than Kalshi')
        print(f'{name:<20}{len(x):>6}{b:>8.3f}{k:>18.3f}  {v}')
    c = [r for r in rows if r['kalshi_close'] is not None]
    if c:
        mv = [r['kalshi_close'] - r['kalshi_pick'] for r in c]; bd = [r for r in c if (r['grade_published'] or 0) >= 70]
        print(f"Closing price: {len(c)} legs, price moved {sum(mv)/len(mv):+.2f} toward our side on average; moved our way {sum(m > 0 for m in mv)}, against {sum(m < 0 for m in mv)}")
        if bd:
            m2 = [r['kalshi_close'] - r['kalshi_pick'] for r in bd]
            print(f"  Board (70+): {len(bd)} legs, {sum(m2)/len(m2):+.2f} average; our way {sum(m > 0 for m in m2)}, against {sum(m < 0 for m in m2)}")
last = max(r['slate_date'] for r in B)
card([r for r in B if r['slate_date'] == last], f'Night of {last}')
card(B, 'All nights')
print(f"\nPhase 3 gate: {len(B)} of 2,000 graded legs with a pregame market price. Model training waits until then.")
