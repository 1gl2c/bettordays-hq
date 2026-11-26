"""ESPN box scores for Nov 25 NBA games, and a grader for any player prop text like 'AJ Dybantsa 2+ threes',
'DeMar DeRozan under 4 assists', 'Alex Sarr double-double'. Import: from tue24.res.box import grade"""
import json, re, subprocess, unicodedata
cu = lambda u: json.loads(subprocess.run(['curl', '-s', '-m', '30', u], capture_output=True, text=True).stdout)
nm = lambda n: re.sub(r'[^a-z]', '', re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()))
BOX = {}; DNP = set()
for e in cu('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261125')['events']:
    assert e['competitions'][0]['status']['type']['completed'], e['shortName']
    d = cu(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={e['id']}")
    for t in d['boxscore'].get('players', []):
        for st in t['statistics']:
            for a in st['athletes']:
                k = nm(a['athlete']['displayName'])
                if a.get('stats'):
                    x = dict(zip(st['keys'], a['stats'])); f = lambda v: float(str(v).split('-')[0])
                    BOX[k] = {'points': f(x['points']), 'rebounds': f(x['rebounds']), 'assists': f(x['assists']), 'threes': f(x['threePointFieldGoalsMade-threePointFieldGoalsAttempted'])}
                else: DNP.add(k)
def grade(p):
    """returns (result 'W'/'L'/'V', actual text)"""
    t = re.sub(r'\s*\(could sit\)', '', p)
    m = re.match(r"(.+?) (?:(\d+)\+|under (\d+)) (points \+ rebounds \+ assists|PRA|points|rebounds|assists|threes)$", t) or re.match(r"(.+?) (double-double|triple-double)$", t)
    assert m, p
    k = nm(m.group(1)); b = BOX.get(k)
    if b is None: return 'V', 'did not play'
    if m.group(2) in ('double-double', 'triple-double') and m.lastindex == 2:
        c = sum(v >= 10 for v in (b['points'], b['rebounds'], b['assists']))
        need = 2 if m.group(2) == 'double-double' else 3
        return ('W' if c >= need else 'L'), f"{int(b['points'])}/{int(b['rebounds'])}/{int(b['assists'])}"
    stat = m.group(4); v = b['points'] + b['rebounds'] + b['assists'] if stat in ('PRA', 'points + rebounds + assists') else b[stat]
    if m.group(2): return ('W' if v >= int(m.group(2)) else 'L'), str(int(v))
    return ('W' if v < int(m.group(3)) else 'L'), str(int(v))
