```python
import os
import pandas as pd

print("Files in current dir:", os.listdir('.'))

for f in ['BD_DAILY_PICKS_BLIND_2026-11-19.csv', 'BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv', 'picks_history_1.csv']:
    if os.path.exists(f):
        df = pd.read_csv(f)
        print(f"\n=== {f} === (rows: {len(df)}, cols: {len(df.columns)})")
        print("Columns:", list(df.columns))
        print(df.head(5).to_string())
    else:
        print(f"MISSING: {f}")


```

```text
Files in current dir: ['picks_history_1.csv', 'BD_DAILY_PICKS_BLIND_2026-11-19.csv', 'BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv']

=== BD_DAILY_PICKS_BLIND_2026-11-19.csv === (rows: 50, cols: 11)
Columns: ['pick_no', 'pick_as_submitted', 'sport', 'game', 'tip_time_pt', 'market', 'capper', 'sportsbook', 'odds_american', 'line_captured_at', 'status_note']
   pick_no                      pick_as_submitted sport     game tip_time_pt market  capper  sportsbook  odds_american  line_captured_at status_note
0        1             CJ Stroud 5+ rushing yards   NFL  IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN         NaN
1        2      Dalton Schultz 25 receiving yards   NFL  IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN         NaN
2        3  Xavier hutchinson 30+ receiving yards   NFL  IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN         NaN
3        4   Laquon Treadwell 20+ receiving yards   NFL  IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN         NaN
4        5       Tyler Warren 30+ receiving yards   NFL  IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN         NaN

=== BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv === (rows: 91, cols: 11)
Columns: ['player', 'team', 'game', 'tip_time_pt', 'line', 'kalshi_ticker', 'kalshi_ask', 'kalshi_bid', 'american_odds_from_ask', 'breakeven_pct', 'price_at']
               player team    game tip_time_pt                         line                              kalshi_ticker  kalshi_ask  kalshi_bid  american_odds_from_ask  breakeven_pct              price_at
0          Al Horford   GS  GS@MEM        5:00                  4+ rebounds     KXNBAREB-26NOV19GSWMEM-GSWAHORFORD20-4        0.56        0.54                    -127           57.7  2026-11-20T00:13:18Z
1  Brandin Podziemski   GS  GS@MEM        5:00  25+ points+rebounds+assists  KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25        0.59        0.57                    -144           60.7  2026-11-20T00:13:18Z
2      Cameron Boozer  MEM  GS@MEM        5:00                    2+ threes      KXNBA3PT-26NOV19GSWMEM-MEMCBOOZER27-2        0.60        0.59                    -150           61.7  2026-11-20T00:13:18Z
3       Cedric Coward  MEM  GS@MEM        5:00                   15+ points     KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15        0.56        0.54                    -127           57.7  2026-11-20T00:13:18Z
4       Cedric Coward  MEM  GS@MEM        5:00                    2+ threes      KXNBA3PT-26NOV19GSWMEM-MEMCCOWARD23-2        0.60        0.59                    -150           61.7  2026-11-20T00:13:18Z

=== picks_history_1.csv === (rows: 1322, cols: 45)
Columns: ['pick_key', 'slate_date', 'game_time_text', 'sport', 'event', 'player', 'market', 'stat', 'direction', 'line', 'line_style', 'pick_text', 'capper_line', 'moved', 'grade', 'grade_version', 'b2b', 'matchup', 'kalshi_ticker', 'kalshi_price_grade', 'kalshi_price_grade_ts', 'kalshi_price_close', 'kalshi_price_close_ts', 'kalshi_result', 'result', 'actual', 'status', 'data_source', 'data_gaps', 'notes', 'd_record_status', 'd_unresolved_reason', 'd_in_win_loss_record', 'd_game_key', 'd_ladder_key', 'd_real_line_move', 'd_kalshi_tip_observed', 'd_kalshi_tip_estimated', 'd_kalshi_tip_ts', 'd_kalshi_grade_observed', 'd_kalshi_grade_estimated', 'd_kalshi_grade_ts', 'd_grade_uses_market', 'd_grade_uses_market_reason', 'd_head_to_head_eligible']
                     pick_key  slate_date game_time_text sport       event     player market stat direction  line line_style          pick_text capper_line moved  grade      grade_version  b2b matchup                             kalshi_ticker  kalshi_price_grade kalshi_price_grade_ts  kalshi_price_close      kalshi_price_close_ts kalshi_result result  actual  status         data_source                                    data_gaps notes d_record_status d_unresolved_reason  d_in_win_loss_record             d_game_key                d_ladder_key d_real_line_move  d_kalshi_tip_observed  d_kalshi_tip_estimated            d_kalshi_tip_ts  d_kalshi_grade_observed  d_kalshi_grade_estimated d_kalshi_grade_ts  d_grade_uses_market d_grade_uses_market_reason  d_head_to_head_eligible
0      2026-11-04|herro15+pts  2026-11-04            NaN   NBA  MIL (team)      Herro   prop  pts         o  15.0        alt      Herro 15+ PTS         NaN   NaN     85  v1-v7 (pre-audit)  NaN     NaN     KXNBAPTS-26NOV04MILBOS-MILTHERRO11-15                 NaN                   NaN                74.0  2026-11-05T00:00:00+00:00           yes      W    25.0  graded  Nov 4 recap ledger  game time; grading notes; grading timestamp   NaN     settled_win                 NaN                  True  2026-11-04|MIL (team)      2026-11-04|herro|pts|o              NaN                   74.0                     NaN  2026-11-05T00:00:00+00:00                      NaN                       NaN               NaN                False                        NaN                    False
1      2026-11-04|lebron4+ast  2026-11-04            NaN   NBA  PHI (team)     LeBron   prop  ast         o   4.0        alt      LeBron 4+ AST         NaN   NaN     80  v1-v7 (pre-audit)  NaN     NaN      KXNBAAST-26NOV04PHIDET-PHILJAMES23-4                 NaN                   NaN                81.0  2026-11-05T00:00:00+00:00           yes      W     8.0  graded  Nov 4 recap ledger  game time; grading notes; grading timestamp   NaN     settled_win                 NaN                  True  2026-11-04|PHI (team)     2026-11-04|lebron|ast|o              NaN                   81.0                     NaN  2026-11-05T00:00:00+00:00                      NaN                       NaN               NaN                False                        NaN                    False
2  2026-11-04|mcdaniels10+pts  2026-11-04            NaN   NBA  MIN (team)  McDaniels   prop  pts         o  10.0        alt  McDaniels 10+ PTS         NaN   NaN     78  v1-v7 (pre-audit)  NaN     NaN  KXNBAPTS-26NOV04MINHOU-MINJMCDANIELS3-10                 NaN                   NaN                84.0  2026-11-05T01:00:00+00:00           yes      W    14.0  graded  Nov 4 recap ledger  game time; grading notes; grading timestamp   NaN     settled_win                 NaN                  True  2026-11-04|MIN (team)  2026-11-04|mcdaniels|pts|o              NaN                   84.0                     NaN  2026-11-05T01:00:00+00:00                      NaN                       NaN               NaN                False                        NaN                    False
3     2026-11-04|huerter2+reb  2026-11-04            NaN   NBA  DET (team)    Huerter   prop  reb         o   2.0        alt     Huerter 2+ REB         NaN   NaN     78  v1-v7 (pre-audit)  NaN     NaN    KXNBAREB-26NOV04PHIDET-DETKHUERTERSF-2                 NaN                   NaN                64.0  2026-11-05T00:00:00+00:00            no      L     1.0  graded  Nov 4 recap ledger  game time; grading notes; grading timestamp   NaN    settled_loss                 NaN                  True  2026-11-04|DET (team)    2026-11-04|huerter|reb|o              NaN                   64.0                     NaN  2026-11-05T00:00:00+00:00                      NaN                       NaN               NaN                False                        NaN                    False
4       2026-11-04|luka30+pts  2026-11-04            NaN   NBA  LAL (team)       Luka   prop  pts         o  30.0        alt       Luka 30+ PTS         NaN   NaN     74  v1-v7 (pre-audit)  NaN     NaN    KXNBAPTS-26NOV04LALSAC-LALLDONCIC77-30                 NaN                   NaN                70.0  2026-11-05T03:00:00+00:00           yes      W    40.0  graded  Nov 4 recap ledger  game time; grading notes; grading timestamp   NaN     settled_win                 NaN                  True  2026-11-04|LAL (team)       2026-11-04|luka|pts|o              NaN                   70.0                     NaN  2026-11-05T03:00:00+00:00                      NaN                       NaN               NaN                False                        NaN                    False


```

```python
import pandas as pd

picks = pd.read_csv('BD_DAILY_PICKS_BLIND_2026-11-19.csv')
print("=== ALL 50 PICKS ===")
print(picks.to_string(index=False))

beta = pd.read_csv('BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv')
print("\n=== ALL 91 BETA LINES ===")
print(beta.to_string(index=False))


```

```text
=== ALL 50 PICKS ===
 pick_no                                     pick_as_submitted sport       game tip_time_pt market  capper  sportsbook  odds_american  line_captured_at                             status_note
       1                            CJ Stroud 5+ rushing yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       2                     Dalton Schultz 25 receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       3                 Xavier hutchinson 30+ receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       4                  Laquon Treadwell 20+ receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       5                      Tyler Warren 30+ receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       6                     Jonathan Taylor 50+ rushing yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       7                   David Montgomery any time touchdown   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
       8                                 Charleston ML @ Drake   CBB  COFC@DRKE  4:30 PM PT     ml     NaN         NaN            NaN               NaN                                     NaN
       9                           St. Thomas ML v SE Missouri   CBB  SEMO@STMN  5:00 PM PT     ml     NaN         NaN            NaN               NaN                                     NaN
      10                             Wisconsin ML v Seton Hall   CBB HALL v WIS  5:30 PM PT     ml     NaN         NaN            NaN               NaN                                     NaN
      11                                        St Thomas -6.5   CBB  SEMO@STMN  5:00 PM PT spread     NaN         NaN            NaN               NaN                                     NaN
      12                                        Wisconsin -4.5   CBB HALL v WIS  5:30 PM PT spread     NaN         NaN            NaN               NaN                                     NaN
      13                    Pepperdine +4.5 v UC Santa Barbara   CBB  UCSB@PEPP  6:00 PM PT spread     NaN         NaN            NaN               NaN                                     NaN
      14    Sacramento State @ Stanford under 150 total points   CBB   SAC@STAN  7:00 PM PT  total     NaN         NaN            NaN               NaN                                     NaN
      15                      Nico Collins 60+ receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      16        David Montgomery 60+ rushing + receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      17                     Jonathan Taylor 50+ rushing yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                        Duplicate of #6.
      18                            Tyler Warren 5+ receptions   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      19                                  David Montgomery ATD   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                        Duplicate of #7.
      20                             CJ Stroud o9.5 Rush Yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      21                   Jonathan Taylor o12.5 Rush Attempts   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      22                           Minnesota Timberwolves +2.5   NBA     NY@MIN  5:00 PM PT spread     NaN         NaN            NaN               NaN                                     NaN
      23                                Washington Capitals ML   NHL    BUF@WSH  4:00 PM PT     ml     NaN         NaN            NaN               NaN                                     NaN
      24 Anaheim Ducks / Colorado Avalanche over 6 total goals   NHL    ANA@COL  6:00 PM PT  total     NaN         NaN            NaN               NaN                                     NaN
      25                          Tank Dell any time touchdown   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      26     Amari Demercado over 30 rushing + receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      27                         Anthony Gould receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                          No line given.
      28                                Lamelo Ball 20+ points   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      29                               Lamelo Ball 4+ rebounds   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      30                                Lamelo Ball 15+ points   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      31                     Dalton Schultz any time touchdown   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      32                        Seth McGowan anytime touchdown   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      33                            Donovan Clingan 10+ points   NBA    POR@MIL  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      34                            Donovan Clingan 15+ points   NBA    POR@MIL  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      35                                  Jalen Brunson 6+ AST   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      36                               Brook Lopez 6+ rebounds   NBA     LAC@SA  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      37                               Brook Lopez 4+ rebounds   NBA     LAC@SA  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      38                              De'Aaron Fox 4+ rebounds   NBA     LAC@SA  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      39                           Jaden McDaniels 4+ rebounds   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      40                         Tank Dell 40+ receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      41                     Texans to win by over 9.5+ points   NFL    IND@HOU  5:15 PM PT spread     NaN         NaN            NaN               NaN                                     NaN
      42                   David Montogmery any time touchdown   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                        Duplicate of #7.
      43                     Jonathan Taylor 50+ rushing yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                        Duplicate of #6.
      44                                             Texans ML   NFL    IND@HOU  5:15 PM PT     ml     NaN         NaN            NaN               NaN                                     NaN
      45                          Myles Turner under 3 assists   NBA    POR@MIL  5:00 PM PT   prop     NaN         NaN            NaN               NaN Player ruled out before grading (void).
      46                          Myles Turner under 4 assists   NBA    POR@MIL  5:00 PM PT   prop     NaN         NaN            NaN               NaN Player ruled out before grading (void).
      47                     Victor Wembanyama under 30 points   NBA     LAC@SA  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      48                         Jalen Brunson under 30 points   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      49                             Mikal Bridges over 15 PRA   NBA     NY@MIN  5:00 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN
      50             David Montgomery over 9.5 receiving yards   NFL    IND@HOU  5:15 PM PT   prop     NaN         NaN            NaN               NaN                                     NaN

=== ALL 91 BETA LINES ===
            player team    game tip_time_pt                        line                              kalshi_ticker  kalshi_ask  kalshi_bid  american_odds_from_ask  breakeven_pct             price_at
        Al Horford   GS  GS@MEM        5:00                 4+ rebounds     KXNBAREB-26NOV19GSWMEM-GSWAHORFORD20-4        0.56        0.54                    -127           57.7 2026-11-20T00:13:18Z
Brandin Podziemski   GS  GS@MEM        5:00 25+ points+rebounds+assists  KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
    Cameron Boozer  MEM  GS@MEM        5:00                   2+ threes      KXNBA3PT-26NOV19GSWMEM-MEMCBOOZER27-2        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
     Cedric Coward  MEM  GS@MEM        5:00                  15+ points     KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15        0.56        0.54                    -127           57.7 2026-11-20T00:13:18Z
     Cedric Coward  MEM  GS@MEM        5:00                   2+ threes      KXNBA3PT-26NOV19GSWMEM-MEMCCOWARD23-2        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
     Cedric Coward  MEM  GS@MEM        5:00                  4+ assists      KXNBAAST-26NOV19GSWMEM-MEMCCOWARD23-4        0.50        0.49                     100           51.7 2026-11-20T00:13:18Z
     Cedric Coward  MEM  GS@MEM        5:00                 8+ rebounds      KXNBAREB-26NOV19GSWMEM-MEMCCOWARD23-8        0.50        0.49                     100           51.7 2026-11-20T00:13:18Z
 De'Anthony Melton   GS  GS@MEM        5:00                  10+ points      KXNBAPTS-26NOV19GSWMEM-GSWDMELTON8-10        0.60        0.56                    -150           61.7 2026-11-20T00:13:18Z
 De'Anthony Melton   GS  GS@MEM        5:00                   2+ threes       KXNBA3PT-26NOV19GSWMEM-GSWDMELTON8-2        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
        Gui Santos   GS  GS@MEM        5:00                   1+ threes      KXNBA3PT-26NOV19GSWMEM-GSWGSANTOS15-1        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
        Gui Santos   GS  GS@MEM        5:00 15+ points+rebounds+assists     KXNBAPRA-26NOV19GSWMEM-GSWGSANTOS15-15        0.52        0.51                    -108           53.7 2026-11-20T00:13:18Z
        Gui Santos   GS  GS@MEM        5:00                 4+ rebounds      KXNBAREB-26NOV19GSWMEM-GSWGSANTOS15-4        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
      Jaylen Wells  MEM  GS@MEM        5:00                  10+ points       KXNBAPTS-26NOV19GSWMEM-MEMJWELLS0-10        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
      Jaylen Wells  MEM  GS@MEM        5:00 15+ points+rebounds+assists       KXNBAPRA-26NOV19GSWMEM-MEMJWELLS0-15        0.54        0.53                    -117           55.7 2026-11-20T00:13:18Z
      Jaylen Wells  MEM  GS@MEM        5:00                  2+ assists        KXNBAAST-26NOV19GSWMEM-MEMJWELLS0-2        0.50        0.49                     100           51.7 2026-11-20T00:13:18Z
      Jaylen Wells  MEM  GS@MEM        5:00                   2+ threes        KXNBA3PT-26NOV19GSWMEM-MEMJWELLS0-2        0.56        0.54                    -127           57.7 2026-11-20T00:13:18Z
      Jerami Grant  MEM  GS@MEM        5:00 15+ points+rebounds+assists       KXNBAPRA-26NOV19GSWMEM-MEMJGRANT9-15        0.54        0.50                    -117           55.7 2026-11-20T00:13:18Z
      Jerami Grant  MEM  GS@MEM        5:00                   2+ threes        KXNBA3PT-26NOV19GSWMEM-MEMJGRANT9-2        0.51        0.49                    -104           52.7 2026-11-20T00:13:18Z
  Taylor Hendricks  MEM  GS@MEM        5:00                 4+ rebounds   KXNBAREB-26NOV19GSWMEM-MEMTHENDRICKS22-4        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
    Darius Garland  LAC  LAC@SA        5:00                  6+ assists     KXNBAAST-26NOV19LACSAS-LACDGARLAND10-6        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
      De'Aaron Fox   SA  LAC@SA        5:00                  15+ points         KXNBAPTS-26NOV19LACSAS-SASDFOX4-15        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
      De'Aaron Fox   SA  LAC@SA        5:00 25+ points+rebounds+assists         KXNBAPRA-26NOV19LACSAS-SASDFOX4-25        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
      De'Aaron Fox   SA  LAC@SA        5:00                 4+ rebounds          KXNBAREB-26NOV19LACSAS-SASDFOX4-4        0.58        0.57                    -138           59.7 2026-11-20T00:13:18Z
      De'Aaron Fox   SA  LAC@SA        5:00                  6+ assists          KXNBAAST-26NOV19LACSAS-SASDFOX4-6        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
 Derrick Jones Jr.  LAC  LAC@SA        5:00                 4+ rebounds        KXNBAREB-26NOV19LACSAS-LACDJONES5-4        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
     Devin Vassell   SA  LAC@SA        5:00                   2+ threes     KXNBA3PT-26NOV19LACSAS-SASDVASSELL24-2        0.55        0.53                    -122           56.7 2026-11-20T00:13:18Z
     Devin Vassell   SA  LAC@SA        5:00                 4+ rebounds     KXNBAREB-26NOV19LACSAS-SASDVASSELL24-4        0.56        0.55                    -127           57.7 2026-11-20T00:13:18Z
 Julian Champagnie   SA  LAC@SA        5:00                  10+ points KXNBAPTS-26NOV19LACSAS-SASJCHAMPAGNIE30-10        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
 Julian Champagnie   SA  LAC@SA        5:00                   3+ threes  KXNBA3PT-26NOV19LACSAS-SASJCHAMPAGNIE30-3        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
     Keaton Wagler  LAC  LAC@SA        5:00                  10+ points      KXNBAPTS-26NOV19LACSAS-LACKWAGLER1-10        0.54        0.53                    -117           55.7 2026-11-20T00:13:18Z
     Keaton Wagler  LAC  LAC@SA        5:00 15+ points+rebounds+assists      KXNBAPRA-26NOV19LACSAS-LACKWAGLER1-15        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
    Keldon Johnson   SA  LAC@SA        5:00                   1+ threes      KXNBA3PT-26NOV19LACSAS-SASKJOHNSON3-1        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
    Keldon Johnson   SA  LAC@SA        5:00                  2+ assists      KXNBAAST-26NOV19LACSAS-SASKJOHNSON3-2        0.58        0.57                    -138           59.7 2026-11-20T00:13:18Z
         Kris Dunn  LAC  LAC@SA        5:00                   5+ points         KXNBAPTS-26NOV19LACSAS-LACKDUNN8-5        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
     Rui Hachimura  LAC  LAC@SA        5:00                   2+ threes   KXNBA3PT-26NOV19LACSAS-LACRHACHIMURA28-2        0.53        0.51                    -113           54.7 2026-11-20T00:13:18Z
    Stephon Castle   SA  LAC@SA        5:00                   2+ threes       KXNBA3PT-26NOV19LACSAS-SASSCASTLE5-2        0.52        0.51                    -108           53.7 2026-11-20T00:13:18Z
    Stephon Castle   SA  LAC@SA        5:00 30+ points+rebounds+assists      KXNBAPRA-26NOV19LACSAS-SASSCASTLE5-30        0.52        0.51                    -108           53.7 2026-11-20T00:13:18Z
 Victor Wembanyama   SA  LAC@SA        5:00                12+ rebounds  KXNBAREB-26NOV19LACSAS-SASVWEMBANYAMA1-12        0.51        0.50                    -104           52.7 2026-11-20T00:13:18Z
       Ayo Dosunmu  MIN  NY@MIN        5:00                   2+ threes     KXNBA3PT-26NOV19NYKMIN-MINADOSUNMU13-2        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
       Ayo Dosunmu  MIN  NY@MIN        5:00 25+ points+rebounds+assists    KXNBAPRA-26NOV19NYKMIN-MINADOSUNMU13-25        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
       Ayo Dosunmu  MIN  NY@MIN        5:00                  4+ assists     KXNBAAST-26NOV19NYKMIN-MINADOSUNMU13-4        0.58        0.57                    -138           59.7 2026-11-20T00:13:18Z
       Ayo Dosunmu  MIN  NY@MIN        5:00                 4+ rebounds     KXNBAREB-26NOV19NYKMIN-MINADOSUNMU13-4        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
      Bones Hyland  MIN  NY@MIN        5:00                 2+ rebounds      KXNBAREB-26NOV19NYKMIN-MINBHYLANDPG-2        0.50        0.46                     100           51.7 2026-11-20T00:13:18Z
      Bones Hyland  MIN  NY@MIN        5:00                   2+ threes      KXNBA3PT-26NOV19NYKMIN-MINBHYLANDPG-2        0.51        0.49                    -104           52.7 2026-11-20T00:13:18Z
   Jaden McDaniels  MIN  NY@MIN        5:00 25+ points+rebounds+assists   KXNBAPRA-26NOV19NYKMIN-MINJMCDANIELS3-25        0.52        0.50                    -108           53.7 2026-11-20T00:13:18Z
     Jalen Brunson   NY  NY@MIN        5:00                  25+ points    KXNBAPTS-26NOV19NYKMIN-NYKJBRUNSON11-25        0.58        0.56                    -138           59.7 2026-11-20T00:13:18Z
     Jalen Brunson   NY  NY@MIN        5:00 35+ points+rebounds+assists    KXNBAPRA-26NOV19NYKMIN-NYKJBRUNSON11-35        0.52        0.50                    -108           53.7 2026-11-20T00:13:18Z
     Jalen Brunson   NY  NY@MIN        5:00                  6+ assists     KXNBAAST-26NOV19NYKMIN-NYKJBRUNSON11-6        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
     Joan Beringer  MIN  NY@MIN        5:00                   5+ points    KXNBAPTS-26NOV19NYKMIN-MINJBERINGER19-5        0.50        0.47                     100           51.7 2026-11-20T00:13:18Z
  Jonathan Kuminga  MIN  NY@MIN        5:00 20+ points+rebounds+assists     KXNBAPRA-26NOV19NYKMIN-MINJKUMINGA0-20        0.55        0.53                    -122           56.7 2026-11-20T00:13:18Z
         Josh Hart   NY  NY@MIN        5:00                 6+ rebounds         KXNBAREB-26NOV19NYKMIN-NYKJHART3-6        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
Karl-Anthony Towns   NY  NY@MIN        5:00                   2+ threes       KXNBA3PT-26NOV19NYKMIN-NYKKTOWNS32-2        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
Karl-Anthony Towns   NY  NY@MIN        5:00                  20+ points      KXNBAPTS-26NOV19NYKMIN-NYKKTOWNS32-20        0.56        0.55                    -127           57.7 2026-11-20T00:13:18Z
Karl-Anthony Towns   NY  NY@MIN        5:00                  4+ assists       KXNBAAST-26NOV19NYKMIN-NYKKTOWNS32-4        0.51        0.50                    -104           52.7 2026-11-20T00:13:18Z
       LaMelo Ball  MIN  NY@MIN        5:00                   4+ threes         KXNBA3PT-26NOV19NYKMIN-MINLBALL1-4        0.50        0.48                     100           51.7 2026-11-20T00:13:18Z
       LaMelo Ball  MIN  NY@MIN        5:00                  6+ assists         KXNBAAST-26NOV19NYKMIN-MINLBALL1-6        0.56        0.55                    -127           57.7 2026-11-20T00:13:18Z
     Landry Shamet   NY  NY@MIN        5:00                 2+ rebounds      KXNBAREB-26NOV19NYKMIN-NYKLSHAMET44-2        0.55        0.53                    -122           56.7 2026-11-20T00:13:18Z
     Landry Shamet   NY  NY@MIN        5:00                   2+ threes      KXNBA3PT-26NOV19NYKMIN-NYKLSHAMET44-2        0.56        0.55                    -127           57.7 2026-11-20T00:13:18Z
     Mikal Bridges   NY  NY@MIN        5:00                  10+ points    KXNBAPTS-26NOV19NYKMIN-NYKMBRIDGES25-10        0.50        0.48                     100           51.7 2026-11-20T00:13:18Z
     Mikal Bridges   NY  NY@MIN        5:00 15+ points+rebounds+assists    KXNBAPRA-26NOV19NYKMIN-NYKMBRIDGES25-15        0.56        0.54                    -127           57.7 2026-11-20T00:13:18Z
     Miles McBride   NY  NY@MIN        5:00                   5+ points      KXNBAPTS-26NOV19NYKMIN-NYKMMCBRIDE2-5        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
        OG Anunoby   NY  NY@MIN        5:00                  15+ points     KXNBAPTS-26NOV19NYKMIN-NYKOANUNOBY8-15        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
        OG Anunoby   NY  NY@MIN        5:00                  2+ assists      KXNBAAST-26NOV19NYKMIN-NYKOANUNOBY8-2        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
       Rudy Gobert  MIN  NY@MIN        5:00                10+ rebounds     KXNBAREB-26NOV19NYKMIN-MINRGOBERT27-10        0.55        0.53                    -122           56.7 2026-11-20T00:13:18Z
       Rudy Gobert  MIN  NY@MIN        5:00                  2+ assists      KXNBAAST-26NOV19NYKMIN-MINRGOBERT27-2        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
       Rudy Gobert  MIN  NY@MIN        5:00 20+ points+rebounds+assists     KXNBAPRA-26NOV19NYKMIN-MINRGOBERT27-20        0.54        0.51                    -117           55.7 2026-11-20T00:13:18Z
        Trey Lyles  MIN  NY@MIN        5:00                 4+ rebounds       KXNBAREB-26NOV19NYKMIN-MINTLYLES41-4        0.60        0.57                    -150           61.7 2026-11-20T00:13:18Z
   Brayden Burries  MIL POR@MIL        5:00 20+ points+rebounds+assists     KXNBAPRA-26NOV19PORMIL-MILBBURRIES0-20        0.57        0.55                    -133           58.7 2026-11-20T00:13:18Z
   Brayden Burries  MIL POR@MIL        5:00                 6+ rebounds      KXNBAREB-26NOV19PORMIL-MILBBURRIES0-6        0.51        0.50                    -104           52.7 2026-11-20T00:13:18Z
    Damian Lillard  POR POR@MIL        5:00 30+ points+rebounds+assists     KXNBAPRA-26NOV19PORMIL-PORDLILLARD0-30        0.57        0.53                    -133           58.7 2026-11-20T00:13:18Z
       Deni Avdija  POR POR@MIL        5:00                   2+ threes       KXNBA3PT-26NOV19PORMIL-PORDAVDIJA8-2        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
       Deni Avdija  POR POR@MIL        5:00                  6+ assists       KXNBAAST-26NOV19PORMIL-PORDAVDIJA8-6        0.53        0.52                    -113           54.7 2026-11-20T00:13:18Z
   Donovan Clingan  POR POR@MIL        5:00                12+ rebounds    KXNBAREB-26NOV19PORMIL-PORDCLINGAN23-12        0.60        0.59                    -150           61.7 2026-11-20T00:13:18Z
  Jaime Jaquez Jr.  MIL POR@MIL        5:00                  15+ points     KXNBAPTS-26NOV19PORMIL-MILJJAQUEZ24-15        0.53        0.51                    -113           54.7 2026-11-20T00:13:18Z
      Jrue Holiday  POR POR@MIL        5:00                 4+ rebounds      KXNBAREB-26NOV19PORMIL-PORJHOLIDAY5-4        0.58        0.57                    -138           59.7 2026-11-20T00:13:18Z
       Kel'el Ware  MIL POR@MIL        5:00                  10+ points        KXNBAPTS-26NOV19PORMIL-MILKWARE9-10        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
       Kel'el Ware  MIL POR@MIL        5:00                 8+ rebounds         KXNBAREB-26NOV19PORMIL-MILKWARE9-8        0.55        0.54                    -122           56.7 2026-11-20T00:13:18Z
        Nate Ament  MIL POR@MIL        5:00                  2+ assists       KXNBAAST-26NOV19PORMIL-MILNAMENT15-2        0.59        0.55                    -144           60.7 2026-11-20T00:13:18Z
        Nate Ament  MIL POR@MIL        5:00                 4+ rebounds       KXNBAREB-26NOV19PORMIL-MILNAMENT15-4        0.52        0.50                    -108           53.7 2026-11-20T00:13:18Z
      Ryan Rollins  MIL POR@MIL        5:00                   2+ threes     KXNBA3PT-26NOV19PORMIL-MILRROLLINS13-2        0.52        0.50                    -108           53.7 2026-11-20T00:13:18Z
      Ryan Rollins  MIL POR@MIL        5:00 20+ points+rebounds+assists    KXNBAPRA-26NOV19PORMIL-MILRROLLINS13-20        0.52        0.51                    -108           53.7 2026-11-20T00:13:18Z
      Ryan Rollins  MIL POR@MIL        5:00                  4+ assists     KXNBAAST-26NOV19PORMIL-MILRROLLINS13-4        0.60        0.57                    -150           61.7 2026-11-20T00:13:18Z
      Ryan Rollins  MIL POR@MIL        5:00                 4+ rebounds     KXNBAREB-26NOV19PORMIL-MILRROLLINS13-4        0.57        0.56                    -133           58.7 2026-11-20T00:13:18Z
      Sidy Cissoko  POR POR@MIL        5:00                  2+ assists     KXNBAAST-26NOV19PORMIL-PORSCISSOKO91-2        0.59        0.57                    -144           60.7 2026-11-20T00:13:18Z
      Sidy Cissoko  POR POR@MIL        5:00                   2+ threes     KXNBA3PT-26NOV19PORMIL-PORSCISSOKO91-2        0.50        0.49                     100           51.7 2026-11-20T00:13:18Z
      Sidy Cissoko  POR POR@MIL        5:00                 4+ rebounds     KXNBAREB-26NOV19PORMIL-PORSCISSOKO91-4        0.52        0.51                    -108           53.7 2026-11-20T00:13:18Z
    Toumani Camara  POR POR@MIL        5:00                  2+ assists      KXNBAAST-26NOV19PORMIL-PORTCAMARA33-2        0.53        0.50                    -113           54.7 2026-11-20T00:13:18Z
    Toumani Camara  POR POR@MIL        5:00 20+ points+rebounds+assists     KXNBAPRA-26NOV19PORMIL-PORTCAMARA33-20        0.51        0.50                    -104           52.7 2026-11-20T00:13:18Z
       Tyler Herro  MIL POR@MIL        5:00                  20+ points      KXNBAPTS-26NOV19PORMIL-MILTHERRO11-20        0.56        0.55                    -127           57.7 2026-11-20T00:13:18Z
       Tyler Herro  MIL POR@MIL        5:00                  4+ assists       KXNBAAST-26NOV19PORMIL-MILTHERRO11-4        0.59        0.58                    -144           60.7 2026-11-20T00:13:18Z
       Tyler Herro  MIL POR@MIL        5:00                 4+ rebounds       KXNBAREB-26NOV19PORMIL-MILTHERRO11-4        0.58        0.57                    -138           59.7 2026-11-20T00:13:18Z


```

```python
import pandas as pd
import numpy as np

hist = pd.read_csv('picks_history_1.csv')
print("Total rows:", len(hist))
print("Date range:", hist['slate_date'].min(), "to", hist['slate_date'].max())

wl = hist[hist['d_in_win_loss_record'] == True].copy()
print("d_in_win_loss_record == True:", len(wl), "Date range:", wl['slate_date'].min(), "to", wl['slate_date'].max())
print("Overall win rate:", (wl['result'] == 'W').mean(), "W:", (wl['result'] == 'W').sum(), "L:", (wl['result'] == 'L').sum())

print("\n--- By sport ---")
print(wl.groupby('sport')['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))

print("\n--- By line_style ---")
print(wl.groupby('line_style', dropna=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))

print("\n--- By market ---")
print(wl.groupby('market', dropna=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))

print("\n--- By stat (top 12) ---")
print(wl.groupby('stat', dropna=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()).sort_values('n', ascending=False).head(12))

print("\n--- By direction ---")
print(wl.groupby('direction', dropna=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))

print("\n--- By grade bucket ---")
wl['grade_num'] = pd.to_numeric(wl['grade'], errors='coerce')
wl['grade_bin'] = pd.cut(wl['grade_num'], bins=[0, 59, 69, 79, 89, 100], labels=['<60', '60-69', '70-79', '80-89', '90+'])
print(wl.groupby('grade_bin', observed=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))

print("\n--- Head-to-head eligible ---")
h2h = wl[wl['d_head_to_head_eligible'] == True].copy()
print("H2H rows:", len(h2h), "Date range:", h2h['slate_date'].min() if len(h2h) else None, "to", h2h['slate_date'].max() if len(h2h) else None)
if len(h2h) > 0:
    h2h['k_price'] = pd.to_numeric(h2h['d_kalshi_grade_observed'], errors='coerce')
    h2h['gap'] = h2h['grade_num'] - h2h['k_price']
    h2h['gap_bin'] = pd.cut(h2h['gap'], bins=[-100, -1, 7.99, 100], labels=['grade<kalshi', '0_to_7', '8+above'])
    print(h2h.groupby('gap_bin', observed=False)['result'].agg(n='count', wins=lambda s: (s=='W').sum(), wr=lambda s: (s=='W').mean()))


```

```text
Total rows: 1322
Date range: 2026-11-04 to 2026-11-18
d_in_win_loss_record == True: 1146 Date range: 2026-11-04 to 2026-11-18
Overall win rate: 0.6483420593368238 W: 743 L: 403

--- By sport ---
         n  wins        wr
sport                     
CBB     18    11  0.611111
CFB     39    27  0.692308
NBA    727   487  0.669876
NCAAB    9     4  0.444444
NCAAF    2     2  1.000000
NFL    307   185  0.602606
NHL     10     7  0.700000
UFC     34    20  0.588235

--- By line_style ---
              n  wins        wr
line_style                     
alt         558   398  0.713262
ceil         30    18  0.600000
move          4     4  1.000000
reg         554   323  0.583032

--- By market ---
          n  wins        wr
market                     
atd      49    20  0.408163
method    5     3  0.600000
ml      138    90  0.652174
prop    885   583  0.658757
spread   44    29  0.659091
total    25    18  0.720000

--- By stat (top 12) ---
          n  wins        wr
stat                       
pts     271   183  0.675277
reb     156   102  0.653846
ml      138    90  0.652174
ast     114    74  0.649123
recyds   65    38  0.584615
rush     60    40  0.666667
3pm      56    42  0.750000
atd      53    20  0.377358
pra      43    23  0.534884
spread   41    28  0.682927
pass     25    17  0.680000
total    25    18  0.720000

--- By direction ---
              n  wins        wr
direction                      
o          1044   676  0.647510
u            99    64  0.646465
NaN           3     3  1.000000

--- By grade bucket ---
             n  wins        wr
grade_bin                     
<60        483   249  0.515528
60-69      221   151  0.683258
70-79      231   180  0.779221
80-89      182   141  0.774725
90+         29    22  0.758621

--- Head-to-head eligible ---
H2H rows: 184 Date range: 2026-11-16 to 2026-11-18
               n  wins        wr
gap_bin                         
grade<kalshi  89    63  0.707865
0_to_7        58    38  0.655172
8+above       37    18  0.486486


```

```python
import pandas as pd
import numpy as np

# Verify ticket math
def calc_ticket(legs):
    # legs: list of (pick_no, name, grade, market_price_pct)
    prices = [x[3] for x in legs]
    grades = [x[2] for x in legs]
    if any(p is None for p in prices):
        payout = None
    else:
        prod_p = np.prod([p/100.0 for p in prices])
        payout = 1.0 / prod_p
    comb_hit = np.prod([g/100.0 for g in grades]) * 100.0
    weakest = min(legs, key=lambda x: x[2])
    return payout, comb_hit, weakest

# Main parlay: #44, #9, #10, #29, #35 (5 legs)
main_legs = [
    (44, "Texans ML", 85, 84.0),
    (9, "St. Thomas ML", 76, 75.9),
    (10, "Wisconsin ML", 66, 68.8),
    (29, "LaMelo Ball 4+ reb", 64, 61.5),
    (35, "Jalen Brunson 6+ AST", 61, 56.3),
]
p, ch, w = calc_ticket(main_legs)
print(f"Main (5-leg): payout={p:.2f}x, combined_hit={ch:.2f}%, weakest=#{w[0]} ({w[2]})")

# Regular-lines parlay: #44, #9, #10, #35 (4 legs)
reg_legs = [
    (44, "Texans ML", 85, 84.0),
    (9, "St. Thomas ML", 76, 75.9),
    (10, "Wisconsin ML", 66, 68.8),
    (35, "Jalen Brunson 6+ AST", 61, 56.3),
]
p, ch, w = calc_ticket(reg_legs)
print(f"Regular (4-leg): payout={p:.2f}x, combined_hit={ch:.2f}%, weakest=#{w[0]} ({w[2]})")

# 20-leg long shot: let's check eligible non-duplicate, non-same-player legs!
# Remember: NEVER same player twice on one ticket!
# Let's check all 50 picks and see how many unique-player eligible picks exist!
picks_meta = [
    # (pick_no, player_or_team_key, game, grade, mkt_price, reg_line, ticket_ok)
    (44, "HOU_ML", "IND@HOU", 85, 84.0, "yes", "yes"),
    (1, "CJ_Stroud", "IND@HOU", 82, None, "no", "yes"),
    (30, "LaMelo_Ball", "NY@MIN", 77, None, "no", "yes"),
    (9, "STMN_ML", "SEMO@STMN", 76, 75.9, "yes", "yes"),
    (39, "Jaden_McDaniels", "NY@MIN", 75, None, "no", "yes"),
    (33, "Donovan_Clingan", "POR@MIL", 73, None, "no", "yes"),
    (15, "Nico_Collins", "IND@HOU", 70, None, "no", "yes"),
    (3, "Xavier_Hutchinson", "IND@HOU", 68, None, "no", "yes"),
    (10, "WIS_ML", "HALL v WIS", 66, 68.8, "yes", "yes"),
    (2, "Dalton_Schultz", "IND@HOU", 66, None, "no", "yes"),
    (37, "Brook_Lopez", "LAC@SA", 65, None, "yes", "yes"),
    (5, "Tyler_Warren", "IND@HOU", 65, None, "no", "yes"),
    (48, "Jalen_Brunson", "NY@MIN", 65, None, "no", "yes"),
    (29, "LaMelo_Ball", "NY@MIN", 64, 61.5, "no", "yes"),
    (4, "Laquon_Treadwell", "IND@HOU", 64, None, "no", "yes"),
    (24, "ANA_COL_O6", "ANA@COL", 63, None, "no", "yes"),
    (13, "PEPP_+4.5", "UCSB@PEPP", 62, None, "no", "yes"),
    (35, "Jalen_Brunson", "NY@MIN", 61, 56.3, "yes", "yes"),
    (41, "HOU_-9.5", "IND@HOU", 60, None, "no", "yes"),
    (20, "CJ_Stroud", "IND@HOU", 58, None, "yes", "yes"),
    (16, "David_Montgomery", "IND@HOU", 57, None, "no", "yes"),
    (22, "MIN_+2.5", "NY@MIN", 57, None, "yes", "yes"),
    (6, "Jonathan_Taylor", "IND@HOU", 56, None, "yes", "yes"),
    (49, "Mikal_Bridges", "NY@MIN", 56, None, "yes", "yes"),
    (11, "STMN_-6.5", "SEMO@STMN", 55, 53.5, "yes", "yes"),
    (50, "David_Montgomery", "IND@HOU", 55, None, "yes", "yes"),
    (26, "Emari_Demercado", "IND@HOU", 55, None, "yes", "yes"),
    (38, "DeAaron_Fox", "LAC@SA", 54, None, "yes", "yes"),
    (12, "WIS_-4.5", "HALL v WIS", 54, 54.5, "yes", "yes"),
    (21, "Jonathan_Taylor", "IND@HOU", 54, None, "yes", "yes"),
    (7, "David_Montgomery", "IND@HOU", 52, 53.0, "yes", "yes"),
    (28, "LaMelo_Ball", "NY@MIN", 52, 51.7, "yes", "yes"),
    (40, "Tank_Dell", "IND@HOU", 52, None, "yes", "yes"),
    (18, "Tyler_Warren", "IND@HOU", 51, None, "yes", "yes"),
    (14, "SAC_STAN_U150", "SAC@STAN", 46, None, "no", "yes"),
    (34, "Donovan_Clingan", "POR@MIL", 43, None, "no", "yes"),
    (36, "Brook_Lopez", "LAC@SA", 38, None, "no", "yes"),
    (31, "Dalton_Schultz", "IND@HOU", 32, 33.3, "yes", "yes"),
    (25, "Tank_Dell", "IND@HOU", 29, 27.8, "yes", "yes"),
    (32, "Seth_McGowan", "IND@HOU", 21, 21.0, "yes", "yes"),
]

# Select top 20 unique players/teams for Long20
seen_players = set()
long20 = []
for row in picks_meta:
    pno, pkey, game, gr, mp, rl, tok = row
    if pkey not in seen_players:
        seen_players.add(pkey)
        long20.append(row)
    if len(long20) == 20:
        break

print(f"\nLong20 count: {len(long20)}")
for r in long20:
    print(f"  #{r[0]:2d} {r[1]:20s} ({r[2]:10s}) grade={r[3]} mkt={r[4]}")

comb_long20 = np.prod([r[3]/100.0 for r in long20]) * 100.0
weak_long20 = min(long20, key=lambda x: x[3])
print(f"Long20 combined hit chance (assuming independence): {comb_long20:.4f}%, weakest=#{weak_long20[0]} ({weak_long20[3]})")


```

```text
Main (5-leg): payout=6.58x, combined_hit=16.65%, weakest=#35 (61)
Regular (4-leg): payout=4.05x, combined_hit=26.01%, weakest=#35 (61)

Long20 count: 20
  #44 HOU_ML               (IND@HOU   ) grade=85 mkt=84.0
  # 1 CJ_Stroud            (IND@HOU   ) grade=82 mkt=None
  #30 LaMelo_Ball          (NY@MIN    ) grade=77 mkt=None
  # 9 STMN_ML              (SEMO@STMN ) grade=76 mkt=75.9
  #39 Jaden_McDaniels      (NY@MIN    ) grade=75 mkt=None
  #33 Donovan_Clingan      (POR@MIL   ) grade=73 mkt=None
  #15 Nico_Collins         (IND@HOU   ) grade=70 mkt=None
  # 3 Xavier_Hutchinson    (IND@HOU   ) grade=68 mkt=None
  #10 WIS_ML               (HALL v WIS) grade=66 mkt=68.8
  # 2 Dalton_Schultz       (IND@HOU   ) grade=66 mkt=None
  #37 Brook_Lopez          (LAC@SA    ) grade=65 mkt=None
  # 5 Tyler_Warren         (IND@HOU   ) grade=65 mkt=None
  #48 Jalen_Brunson        (NY@MIN    ) grade=65 mkt=None
  # 4 Laquon_Treadwell     (IND@HOU   ) grade=64 mkt=None
  #24 ANA_COL_O6           (ANA@COL   ) grade=63 mkt=None
  #13 PEPP_+4.5            (UCSB@PEPP ) grade=62 mkt=None
  #41 HOU_-9.5             (IND@HOU   ) grade=60 mkt=None
  #16 David_Montgomery     (IND@HOU   ) grade=57 mkt=None
  #22 MIN_+2.5             (NY@MIN    ) grade=57 mkt=None
  # 6 Jonathan_Taylor      (IND@HOU   ) grade=56 mkt=None
Long20 combined hit chance (assuming independence): 0.0347%, weakest=#6 (56)


```

```python
import numpy as np

# Check counts of regular lines among eligible picks
reg_eligible = [
    (44, "Texans ML", 85),
    (9, "St. Thomas ML v SE Missouri", 76),
    (10, "Wisconsin ML v Seton Hall", 66),
    (37, "Brook Lopez 4+ rebounds", 65),
    (35, "Jalen Brunson 6+ AST", 61),
    (20, "CJ Stroud o9.5 Rush Yards", 58),
    (22, "Minnesota Timberwolves +2.5", 57),
    (6, "Jonathan Taylor 50+ rushing yards", 56),
    (49, "Mikal Bridges over 15 PRA", 56),
    (11, "St Thomas -6.5", 55),
    (50, "David Montgomery over 9.5 receiving yards", 55),
    (26, "Amari Demercado over 30 rushing + receiving yards", 55),
    (38, "De'Aaron Fox 4+ rebounds", 54),
    (12, "Wisconsin -4.5", 54),
    (21, "Jonathan Taylor o12.5 Rush Attempts", 54),
    (7, "David Montgomery any time touchdown", 52),
    (28, "Lamelo Ball 20+ points", 52),
    (40, "Tank Dell 40+ receiving yards", 52),
    (18, "Tyler Warren 5+ receptions", 51),
    (31, "Dalton Schultz any time touchdown", 32),
    (25, "Tank Dell any time touchdown", 29),
    (32, "Seth McGowan anytime touchdown", 21),
]
print("Total eligible regular lines:", len(reg_eligible))

# Recalc Long20 with #49 instead of #41
long20_grades = [85, 82, 77, 76, 75, 73, 70, 68, 66, 66, 65, 65, 65, 64, 63, 62, 57, 57, 56, 56]
print("Long20 (swapped #41->#49) combined hit chance:", f"{np.prod([g/100 for g in long20_grades])*100:.4f}%")


```

```text
Total eligible regular lines: 22
Long20 (swapped #41->#49) combined hit chance: 0.0324%


```

```python
import pandas as pd

beta = pd.read_csv('BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv')
tickers = [
    'KXNBAREB-26NOV19PORMIL-PORDCLINGAN23-12',
    'KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25',
    'KXNBAPTS-26NOV19PORMIL-MILJJAQUEZ24-15',
    'KXNBAREB-26NOV19LACSAS-SASVWEMBANYAMA1-12',
    'KXNBAPTS-26NOV19NYKMIN-NYKKTOWNS32-20',
    'KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15',
    'KXNBAPTS-26NOV19NYKMIN-NYKOANUNOBY8-15',
    'KXNBA3PT-26NOV19LACSAS-SASDVASSELL24-2',
]
sub = beta[beta['kalshi_ticker'].isin(tickers)][['player', 'team', 'game', 'line', 'kalshi_ticker', 'kalshi_ask', 'breakeven_pct']]
print(sub.to_string(index=False))
print("Matched:", len(sub))


```

```text
            player team    game                        line                             kalshi_ticker  kalshi_ask  breakeven_pct
Brandin Podziemski   GS  GS@MEM 25+ points+rebounds+assists KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25        0.59           60.7
     Cedric Coward  MEM  GS@MEM                  15+ points    KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15        0.56           57.7
     Devin Vassell   SA  LAC@SA                   2+ threes    KXNBA3PT-26NOV19LACSAS-SASDVASSELL24-2        0.55           56.7
 Victor Wembanyama   SA  LAC@SA                12+ rebounds KXNBAREB-26NOV19LACSAS-SASVWEMBANYAMA1-12        0.51           52.7
Karl-Anthony Towns   NY  NY@MIN                  20+ points     KXNBAPTS-26NOV19NYKMIN-NYKKTOWNS32-20        0.56           57.7
        OG Anunoby   NY  NY@MIN                  15+ points    KXNBAPTS-26NOV19NYKMIN-NYKOANUNOBY8-15        0.55           56.7
   Donovan Clingan  POR POR@MIL                12+ rebounds   KXNBAREB-26NOV19PORMIL-PORDCLINGAN23-12        0.60           61.7
  Jaime Jaquez Jr.  MIL POR@MIL                  15+ points    KXNBAPTS-26NOV19PORMIL-MILJJAQUEZ24-15        0.53           54.7
Matched: 8


```

## 1. Header

* **Date & Time:** Thursday, November 19, 2026, 4:35 PM PT
* **Live Web Access:** Yes
* **Files Read:**
* `BD_DAILY_PICKS_BLIND_2026-11-19.csv`: **50** rows
* `BD_DAILY_BETA_LINES_BLIND_2026-11-19.csv`: **91** rows
* `picks_history_1.csv`: **1,322** rows



---

## 2. Every Pick Graded and Ranked

*All 50 submitted picks ranked highest to lowest by independent grade. Market prices were checked at 4:35 PM PT on Nov 19, 2026, using sportsbooks and Kalshi outside the Beta file. Where no exact market price was found for the submitted threshold, value is marked "cannot assess: no price".*

| Rank | # | Pick | Your grade (basis) | Market price found (source, time) | Value | Key news (source, time) | Strongest for | Strongest against |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 44 | Texans ML | **85** (12.5-pt home favorite; IND missing both starting OTs and both outside CBs; Google Sports Data gives HOU 85.4%) | 84.0% (Kalshi via Covers, 4:35 PM PT) | fair | IND inactive: Sauce Gardner, Charvarius Ward, Bernhard Raimann, Jalen Travis, Jerry Tillery (Colts.com, 4:35 PM PT); HOU inactive: Woody Marks, MHJ, Danielle Hunter (Texans.com, 4:35 PM PT) | Massive talent/health mismatch at home vs 3-7 IND | Divisional TNF variance; IND won Week 3 meeting 19-17 |
| 2 | 1 | CJ Stroud 5+ rushing yards | **82** (Hit 5+ in 8 of 9 games this season, incl. 10 vs IND in Wk 3 and 20 in each of last 2; main line 10.5) | none | cannot assess: no price | Active; HOU missing C Jake Andrews, G Wyatt Teller, T Nate Thomas (Texans.com, 4:35 PM PT) | 8/9 season hit rate; depleted O-line can force scrambles | Kneel-downs late if HOU wins by double digits |
| 3 | 30 | Lamelo Ball 15+ points | **77** (Averages 17.7 PPG; main line 18.5–19.5; Edwards & DiVincenzo out boosts usage) | none | cannot assess: no price | Active, starting PG for MIN; Anthony Edwards & Donte DiVincenzo out (Google Sports Data / SBD, 4:35 PM PT) | Primary creator for depleted MIN; bought down 4 pts off main | Inefficient 41.8% FG shooting; NYK tough perimeter defense |
| 4 | 9 | St. Thomas ML v SE Missouri | **76** (Home favorite by 6.5–7.5 pts; coming off 79-70 road win at LIU) | 75.9% (-315, Bleacher Nation, 4:35 PM PT) | fair | No major injuries verified (not verified) | Strong home court edge at Lee & Penny Anderson Arena | Early-season CBB variance; 3-3 record |
| 5 | 39 | Jaden McDaniels 4+ rebounds | **75** (Averages 6.2 RPG; consensus line 5.5, BetMGM O4.5 -155; extra frontcourt minutes if Kuminga sits) | none | cannot assess: no price | Active, starting for MIN; Edwards/DiVincenzo out, Kuminga status monitored (Google Sports Data / SBD, 4:35 PM PT) | Bought down 1.5 boards below consensus; high minute floor | Gobert and KAT dominate paint glass |
| 6 | 33 | Donovan Clingan 10+ points | **73** (Avg 11.0 PPG, 10+ in 3 straight; main line 12.5; MIL missing Turner & Kuzma) | none | cannot assess: no price | Active for POR; MIL centers/forwards Myles Turner & Kyle Kuzma both OUT (shoulder) (Action Network, 4:35 PM PT) | Thin MIL interior (Ware/Sims); bought down 2.5 pts off main | Blowout risk (POR -10.5) could trim 4Q minutes |
| 7 | 15 | Nico Collins 60+ receiving yards | **70** (WR1 coming off 16 targets/94 yds; main line 71.5; MHJ out; IND missing both starting CBs) | none | cannot assess: no price | Active; HOU WR Marvin Harrison Jr. OUT; IND CBs Sauce Gardner & Charvarius Ward OUT (Texans.com / Colts.com, 4:35 PM PT) | Target funnel vs backup outside corners | Heavy favorite script (-12.5) could reduce 2H pass volume |
| 8 | 3 | Xavier hutchinson 30+ receiving yards | **68** (Had 51 yds vs IND in Wk 3; main line 36.5; MHJ out; IND missing top 2 CBs) | none | cannot assess: no price | Active; MHJ, Higgins, Noel all out/IR for HOU; IND CBs Gardner & Ward out (DK Network / Texans.com / Colts.com, 4:35 PM PT) | Elevated snap share vs depleted IND secondary | Competes with Collins, Dell, Schultz; blowout script risk |
| 9 | 10 | Wisconsin ML v Seton Hall | **66** (4-0 straight up, favored by 4.5–5.5 pts on neutral floor in Bahamas) | 68.8% (-220, BetMGM, 4:35 PM PT) | poor | Neutral site (Baha Mar Championship); injuries not verified | Unbeaten 4-0 start; market favorite | Seton Hall 3-1 ATS with tougher schedule; BetMGM model favors Hall |
| 10 | 2 | Dalton Schultz 25 receiving yards | **66** *(Read as 25+ rec yds)* (Had 30 yds vs IND in Wk 3; main line 29.5; Brevin Jordan & MHJ out) | none | cannot assess: no price | Active; HOU TE Brevin Jordan & WR MHJ OUT (Texans.com, 4:35 PM PT) | Bought down 4.5 yds below main line; steady safety valve | Route share ≤70% in 5 straight games |
| 11 | 37 | Brook Lopez 4+ rebounds | **65** (Avg 5.4 RPG; consensus line 4.5; plays regular starting C minutes for LAC) | none | cannot assess: no price | Active for LAC (Google Sports Data, 4:35 PM PT) | 1.4 RPG above threshold; slightly under 4.5 consensus | Spurs -15.5 blowout risk; Wembanyama limits road OREBs |
| 12 | 5 | Tyler Warren 30+ receiving yards | **65** (IND's top pass-catcher; had 55 yds vs HOU in Wk 3; main line 37.5; trailing script) | none | cannot assess: no price | Active; IND OTs Raimann & Travis OUT, TE Will Mallory OUT (Colts.com, 4:35 PM PT) | Quick-throw TE role behind beat-up O-line; trailing script | Only 1 rec yd last week vs MIA; 63 yds total in last 3 games |
| 13 | 48 | Jalen Brunson under 30 points | **65** (Main line 26.5–27.5; FD 30+ is +186; slow-paced 215.5 total vs Gobert/McDaniels) | none | cannot assess: no price | Active, starting PG for NYK (Google Sports Data, 4:35 PM PT) | 2.5–3.5 pts above main line in low-total (215.5) game | Scored 31 in last game; high-usage closer |
| 14 | 29 | Lamelo Ball 4+ rebounds | **64** (Avg 4.1 RPG; consensus line 4.5, WinDaily proj 4.38; BetMGM O3.5 -160) | 61.5% (O3.5 -160, BetMGM via WinDailySports, 4:35 PM PT) | good | Active, starting PG for MIN; Edwards & DiVincenzo out (SBD, 4:35 PM PT) | Heavy minutes with Edwards out; priced below consensus 4.5 | Gobert/McDaniels/KAT limit guard rebound ceiling |
| 15 | 4 | Laquon Treadwell 20+ receiving yards | **64** (IND's busiest WR post-deadline; main line 27.5; had 20 yds vs HOU in Wk 3) | none | cannot assess: no price | Active; IND OTs Raimann & Travis OUT (Colts.com, 4:35 PM PT) | Bought down 7.5 yds off main; trailing pass script | Poor IND passing offense (166.7 YPG) & Daniel Jones pressure |
| 16 | 24 | Anaheim Ducks / Colorado Avalanche over 6 total goals | **63** (Main total is 6.5 shaded to Over -125/-128; push protection at 6) | none | cannot assess: no price | Scheduled 6:00 PM PT at Ball Arena; goalies not verified | Market heavily favors Over 6.5 (-128 FanDuel) | Goalie hot-streak variance; push on 6 returns no profit |
| 17 | 13 | Pepperdine +4.5 v UC Santa Barbara | **62** (Current consensus moved to +2.5; +4.5 gives 2 pts of CLV at home) | none *(opened -110, current alt price not found)* | cannot assess: no price | Home game at Firestone Fieldhouse; injuries not verified | +2 pts better than current market (+2.5) | UCSB is 4-0 and stronger offensively/defensively |
| 18 | 35 | Jalen Brunson 6+ AST | **61** (Main line 5.5 shaded Over -129; KAT/Anunoby/Bridges healthy; revenge game feed to KAT) | 56.3% (O5.5 -129, BetMGM via SBD, 4:35 PM PT) | good | Active, starting PG for NYK (Google Sports Data, 4:35 PM PT) | Market shaded Over 5.5; MIN missing perimeter defenders | Low game total (215.5) caps possession volume |
| 19 | 41 | Texans to win by over 9.5+ points | **60** (Main spread is -10.5 to -12.5; bought down 1–3 pts past key number 10) | none | cannot assess: no price | IND missing both OTs and both starting CBs; HOU missing Hunter & Al-Shaair (IR) (Colts.com / Texans.com / Covers, 4:35 PM PT) | Clear edge over current -12.5 consensus | HOU is 0-6 ATS in last 6 home games; IND 17-3 ATS +12.5 on road |
| 20 | 20 | CJ Stroud o9.5 Rush Yards | **58** (Hit 10+ in 6 of 9 games; main line is 10.5 on DK) | none | cannot assess: no price | Active; 3 HOU O-linemen inactive (Texans.com, 4:35 PM PT) | 1 yd better than DK 10.5; 20 yds in each of last 2 games | Selective game script as 12.5-pt favorite; kneel-down risk |
| 21 | 16 | David Montgomery 60+ rushing + receiving yards | **57** (Woody Marks out; DK rush line 56.5 + rec line 9.5; IND missing DT Tillery) | none | cannot assess: no price | Active, returning from 4-game groin absence; Woody Marks OUT (Texans.com / TOI, 4:35 PM PT) | Lead RB role in positive script vs weakened IND interior | Averaged just 2.5 YPC this season; workload management risk |
| 22 | 22 | Minnesota Timberwolves +2.5 | **57** (Main spread is MIN +1.5; 11-4 overall, 6-3 ATS at home; numberFire projects MIN 51.8% SU) | none | cannot assess: no price | Edwards & DiVincenzo OUT; LaMelo Ball, Gobert, McDaniels, Dosunmu starting (Google Sports Data / SBD, 4:35 PM PT) | +1 pt better than current +1.5 market; strong home record | Depleted wing depth vs defending champion NYK |
| 23 | 6 | Jonathan Taylor 50+ rushing yards | **56** (739 rush yds on season, 68 vs HOU in Wk 3; main line dropped 51.5 to 49.5; HOU missing Hunter & Al-Shaair) | none | cannot assess: no price | Active; IND OTs Raimann & Travis OUT; HOU DE Danielle Hunter & LB Azeez Al-Shaair OUT (Colts.com / Texans.com / Covers, 4:35 PM PT) | HOU missing top tackler & edge rusher; Taylor focal point | Both IND tackles out; 12.5-pt dog negative game script |
| 24 | 17 | Jonathan Taylor 50+ rushing yards *(Duplicate of #6)* | **56** (Duplicate of #6 — ineligible for tickets) | none | cannot assess: no price | Same as #6 | Same as #6 | Duplicate leg |
| 25 | 43 | Jonathan Taylor 50+ rushing yards *(Duplicate of #6)* | **56** (Duplicate of #6 — ineligible for tickets) | none | cannot assess: no price | Same as #6 | Same as #6 | Duplicate leg |
| 26 | 49 | Mikal Bridges over 15 PRA | **56** (Main lines: 9.5 pts, 3.5 reb, 2.5 ast = 15.5; plays heavy starter minutes) | none *(Beta file excluded)* | cannot assess: no price | Active, starting for NYK (Google Sports Data, 4:35 PM PT) | Slightly below sum of main lines (15.5) | Low-usage 4th option; 9.5 pts line shaded Under (-130) |
| 27 | 23 | Washington Capitals ML *(Game started)* | **55** (Dimers projects 54.3% win prob at home vs BUF; ineligible — started 4:00 PM PT) | 56.0% (56¢ Kalshi / -127, Dimers, 4:35 PM PT) | fair | Game already started (4:00 PM PT) — ineligible | Home favorite with slight analytical edge | Already in progress; coin-flip NHL variance |
| 28 | 11 | St Thomas -6.5 | **55** (Current spread -6.5 to -7.5; 3-2 ATS this season) | 53.5% (-115, BetMGM, 4:35 PM PT) | fair | Injuries not verified | Better number than -7.5 at some books | Bleacher Nation projects tight 2-pt game |
| 29 | 50 | David Montgomery over 9.5 receiving yards | **55** (7 catches for 67 yds in 5 games, 15 yds vs IND in Wk 3; Woody Marks out; SportsGambler O8.5 -114) | none *(exact O9.5 odds not found; O8.5 is -114)* | cannot assess: no price | Active; Woody Marks OUT (Texans.com, 4:35 PM PT) | 100% catch rate (7/7) this season; expanded backfield share | Returning from groin injury; 1-catch variance |
| 30 | 26 | Amari Demercado over 30 rushing + receiving yards | **55** *(Spelled Emari Demercado, HOU RB)* (Projected 42.0 rush+rec yds for Wk 11; Woody Marks out; DK rush line 20.5) | none | cannot assess: no price | Active for HOU; Woody Marks OUT (Texans.com, 4:35 PM PT) | Clear RB2 behind Montgomery returning from groin injury; blowout carries | Limited touches if Montgomery handles full early-down load |
| 31 | 38 | De'Aaron Fox 4+ rebounds | **54** (Hit 4+ in 3 of last 8 active games: 2, 5, 4, 9, 3, 2, 3, 2; Statz AI lists U3.5 at 2.25) | none *(Beta file excluded)* | cannot assess: no price | Active for SAS (Google Sports Data, 4:35 PM PT) | Market leans Over 3.5; high-scoring Spurs side | Only 3/8 hit rate recently; -15.5 blowout risk cuts 4Q mins |
| 32 | 12 | Wisconsin -4.5 | **54** (Current spread -4.5 to -5.5; 4-0 SU) | 54.5% (-120, FanDuel via Action Network, 4:35 PM PT) | fair | Neutral site (Nassau, Bahamas); injuries not verified | 1 pt better than BetMGM -5.5 | Wisconsin 1-3 ATS; Seton Hall 3-1 ATS & Action Network best bet |
| 33 | 21 | Jonathan Taylor o12.5 Rush Attempts | **54** (Had 23 carries vs HOU in Wk 3; IND lean run game, though Seth McGowan taking ~7 carries) | none | cannot assess: no price | Active; IND missing both starting OTs (Colts.com, 4:35 PM PT) | Low threshold for bell-cow RB; HOU missing Hunter & Al-Shaair | Trailing by 12.5+ pts could abandon the run early |
| 34 | 7 | David Montgomery any time touchdown | **52** (Lead goal-line back with Marks out; 9 RZ carries; Covers fair estimate 48–52%) | 53.0% (Kalshi via Covers, 4:35 PM PT; -130 SportsGambler) | fair | Active, full participant all week; Woody Marks OUT (Texans.com / TOI, 4:35 PM PT) | Clear finishing role on 28-pt implied total team | HOU hasn't scored a rushing TD in 32 days; workload cap risk |
| 35 | 19 | David Montgomery ATD *(Duplicate of #7)* | **52** (Duplicate of #7 — ineligible for tickets) | 53.0% (Kalshi via Covers, 4:35 PM PT) | fair | Same as #7 | Same as #7 | Duplicate leg |
| 36 | 42 | David Montogmery any time touchdown *(Duplicate of #7)* | **52** *(Typo for Montgomery; duplicate of #7 — ineligible)* | 53.0% (Kalshi via Covers, 4:35 PM PT) | fair | Same as #7 | Same as #7 | Duplicate leg |
| 37 | 28 | Lamelo Ball 20+ points | **52** (Avg 17.7 PPG; main line 18.5–19.5; WinDaily proj 18.2; extra usage with Edwards out) | 51.7% (O19.5 -107, BetMGM via SBD, 4:35 PM PT) | fair | Active, starting PG for MIN; Edwards & DiVincenzo out (SBD, 4:35 PM PT) | High-volume scoring role with Edwards sidelined | 41.8% FG efficiency; WinDaily projects under 18.5 |
| 38 | 40 | Tank Dell 40+ receiving yards | **52** (Projected 44.6 yds; main line 38.5; MHJ out & IND missing top 2 CBs) | none | cannot assess: no price | Active (full practice Tue, hand/shoulder); MHJ OUT; IND CBs Gardner & Ward OUT (Covers / Texans.com / Colts.com, 4:35 PM PT) | Big-play upside vs backup IND corners | Hand/shoulder issue; blowout script may cap pass attempts |
| 39 | 18 | Tyler Warren 5+ receptions | **51** (Projected 4.78 rec; 9 rec vs HOU in Wk 3, but only 10 rec in last 3 games combined) | none | cannot assess: no price | Active; IND OTs Raimann & Travis OUT (Colts.com, 4:35 PM PT) | Top IND target in likely trailing script | Just 2 catches last week; struggling Daniel Jones offense |
| 40 | 8 | Charleston ML @ Drake *(Game started)* | **50** (Tight -1.5 underdog at Drake; ineligible — started 4:30 PM PT) | 50.5% (-102, Fox Sports Radio 1400, 4:35 PM PT) | fair | Game already started (4:30 PM PT) — ineligible | Nearly coin-flip matchup; solid FG% defense | Road underdog; game already underway |
| 41 | 14 | Sacramento State @ Stanford under 150 total points | **46** (Current total 154.5; both teams trending Under early, but 4.5 pts below market) | none | cannot assess: no price | Injuries not verified | Sac State 2-0 to Under, Stanford 4-1 to Under this season | Giving up 4.5 pts of value vs 154.5 market total |
| 42 | 34 | Donovan Clingan 15+ points | **43** (Avg 11.0 PPG; main line 12.5; hit 15+ in only 3 of last 9 games) | none | cannot assess: no price | Active; MIL missing Turner & Kuzma (Action Network, 4:35 PM PT) | Soft MIL interior defense without Turner | 2.5 pts above main line; blowout risk limits minutes |
| 43 | 47 | Victor Wembanyama under 30 points *(Rule-ineligible)* | **48** (Covers projects 27.89 pts; BetMGM O29.5 +105; ineligible per no-Wemby-unders rule) | none *(O29.5 +105 cited; exact U29.5 not found)* | cannot assess: no price | Active for SAS (not verified on injury report) | -15.5 blowout script could sit him in 4Q | LAC allows 117.7 PPG & 49.1% FG; violates ticket rule |
| 44 | 36 | Brook Lopez 6+ rebounds | **38** (Avg 5.4 RPG; Kalshi U5.5 is -150; consensus 4.5; only 1.0 road OREB/gm) | none *(U5.5 -150 cited; exact O5.5 not found)* | cannot assess: no price | Active for LAC (Google Sports Data, 4:35 PM PT) | Starting center minutes if game stays close | Facing Wembanyama; blowout risk; market heavily favors Under |
| 45 | 31 | Dalton Schultz any time touchdown | **32** (Projected 0.22 rec TD; +200 implied 33.3%; Brevin Jordan out) | 33.3% (+200, SportsGambler, 4:35 PM PT) | fair | Active; TE Brevin Jordan & WR MHJ OUT (Texans.com, 4:35 PM PT) | IND allowed 17 passing TDs; red-zone TE role | Reduced route share (≤70% last 5); TD variance |
| 46 | 25 | Tank Dell any time touchdown | **29** (Projected 0.30 rec TD; +260 implied 27.8%; IND missing top 2 CBs) | 27.8% (+260, SportsGambler, 4:35 PM PT) | good | Active; MHJ OUT; IND CBs Gardner & Ward OUT (Texans.com / Colts.com, 4:35 PM PT) | Explosive playmaker vs backup corners; slight positive edge | Hand/shoulder wear; behind Collins & Montgomery in RZ |
| 47 | 32 | Seth McGowan anytime touchdown | **21** (IND RB2; scored in back-to-back games; projected 0.19 total TDs) | 21.0% (Kalshi via FantasyLabs, 4:35 PM PT; +390 SBD) | fair | Active for IND; both starting OTs out (Colts.com, 4:35 PM PT) | Recent red-zone involvement (2 straight games with TD) | Backup behind Taylor on 12.5-pt underdog with depleted O-line |
| 48 | 27 | Anthony Gould receiving yards | **insufficient** (No line given in `status_note`) | none | cannot assess: no price | Active (limited with toe injury; not on IND inactive list) (Covers / Colts.com, 4:35 PM PT) | N/A (no line) | No line given — ineligible |
| 49 | 45 | Myles Turner under 3 assists | **insufficient** (Void — player ruled out before grading) | none | cannot assess: no price | OUT (shoulder) (Action Network, 4:35 PM PT) | N/A (void) | Player ruled out — void |
| 50 | 46 | Myles Turner under 4 assists | **insufficient** (Void — player ruled out before grading) | none | cannot assess: no price | OUT (shoulder) (Action Network, 4:35 PM PT) | N/A (void) | Player ruled out — void |

---

## 3. Top 25, Any Line (Eligible Picks Only)

*Excludes started games (#8, #23), duplicates (#17, #19, #42, #43), no-line (#27), voids (#45, #46), and Wemby under (#47).*

1. **#44** Texans ML — **85**
2. **#1** CJ Stroud 5+ rushing yards — **82**
3. **#30** Lamelo Ball 15+ points — **77**
4. **#9** St. Thomas ML v SE Missouri — **76**
5. **#39** Jaden McDaniels 4+ rebounds — **75**
6. **#33** Donovan Clingan 10+ points — **73**
7. **#15** Nico Collins 60+ receiving yards — **70**
8. **#3** Xavier hutchinson 30+ receiving yards — **68**
9. **#10** Wisconsin ML v Seton Hall — **66**
10. **#2** Dalton Schultz 25 receiving yards — **66**
11. **#37** Brook Lopez 4+ rebounds — **65**
12. **#5** Tyler Warren 30+ receiving yards — **65**
13. **#48** Jalen Brunson under 30 points — **65**
14. **#29** Lamelo Ball 4+ rebounds — **64**
15. **#4** Laquon Treadwell 20+ receiving yards — **64**
16. **#24** Anaheim Ducks / Colorado Avalanche over 6 total goals — **63**
17. **#13** Pepperdine +4.5 v UC Santa Barbara — **62**
18. **#35** Jalen Brunson 6+ AST — **61**
19. **#41** Texans to win by over 9.5+ points — **60**
20. **#20** CJ Stroud o9.5 Rush Yards — **58**
21. **#16** David Montgomery 60+ rushing + receiving yards — **57**
22. **#22** Minnesota Timberwolves +2.5 — **57**
23. **#6** Jonathan Taylor 50+ rushing yards — **56**
24. **#49** Mikal Bridges over 15 PRA — **56**
25. **#11** St Thomas -6.5 — **55**

---

## 4. Top 25, Regular Lines Only (Eligible Picks Only)

*Only 22 eligible regular-line picks (at or near main sportsbook consensus) exist on today's slate:*

1. **#44** Texans ML — **85**
2. **#9** St. Thomas ML v SE Missouri — **76**
3. **#10** Wisconsin ML v Seton Hall — **66**
4. **#37** Brook Lopez 4+ rebounds — **65**
5. **#35** Jalen Brunson 6+ AST — **61**
6. **#20** CJ Stroud o9.5 Rush Yards — **58**
7. **#22** Minnesota Timberwolves +2.5 — **57**
8. **#6** Jonathan Taylor 50+ rushing yards — **56**
9. **#49** Mikal Bridges over 15 PRA — **56**
10. **#11** St Thomas -6.5 — **55**
11. **#50** David Montgomery over 9.5 receiving yards — **55**
12. **#26** Amari Demercado over 30 rushing + receiving yards — **55**
13. **#38** De'Aaron Fox 4+ rebounds — **54**
14. **#12** Wisconsin -4.5 — **54**
15. **#21** Jonathan Taylor o12.5 Rush Attempts — **54**
16. **#7** David Montgomery any time touchdown — **52**
17. **#28** Lamelo Ball 20+ points — **52**
18. **#40** Tank Dell 40+ receiving yards — **52**
19. **#18** Tyler Warren 5+ receptions — **51**
20. **#31** Dalton Schultz any time touchdown — **32**
21. **#25** Tank Dell any time touchdown — **29**
22. **#32** Seth McGowan anytime touchdown — **21**

---

## 5. Tickets

### Hammer

**No Hammer today.** Only one eligible leg graded 80+ has a verified market price (**#44 Texans ML**, Grade 85, Market 84.0%), which pays 1.19x — below the 2x minimum. (#1 CJ Stroud 5+ rushing yards is graded 82 but lacks a verified market price.)

---

### Main Parlay (5 Legs)

* **Legs & why:**
1. **#44 Texans ML** (Grade 85, Market 84.0%, Kalshi/Covers) — Strongest anchor on the board vs an IND team missing both starting tackles and both outside corners.
2. **#9 St. Thomas ML** (Grade 76, Market 75.9%, -315 Bleacher Nation) — Solid home favorite in Summit League play.
3. **#10 Wisconsin ML** (Grade 66, Market 68.8%, -220 BetMGM) — 4-0 neutral-site favorite.
4. **#29 LaMelo Ball 4+ rebounds** (Grade 64, Market 61.5%, O3.5 -160 BetMGM) — Positive edge (+2.5%) with Edwards/DiVincenzo out.
5. **#35 Jalen Brunson 6+ AST** (Grade 61, Market 56.3%, O5.5 -129 BetMGM) — Positive edge (+4.7%); market shaded Over 5.5.


* **Correlation check:** Two legs come from **NY@MIN** (#29 LaMelo Ball 4+ rebounds and #35 Jalen Brunson 6+ AST). They are on opposite teams and have slight negative-to-neutral correlation (more Knicks made shots assisted by Brunson means fewer defensive rebounds for Ball, though higher pace helps both). All other legs are in separate games.
* **Payout:** **6.58x** before fees — `1 ÷ (0.840 × 0.759 × 0.688 × 0.615 × 0.563)`.
* **Combined hit chance:** **16.65%** (independent product of grades: `0.85 × 0.76 × 0.66 × 0.64 × 0.61`). Parlays multiply risk.
* **Weakest leg:** **#35 Jalen Brunson 6+ AST** (Grade 61).

---

### Regular-Lines Parlay (4 Legs)

* **Legs & why (with regular-line judgment):**
1. **#44 Texans ML** (Grade 85, Market 84.0%, Kalshi/Covers) — Standard moneyline market.
2. **#9 St. Thomas ML** (Grade 76, Market 75.9%, -315 Bleacher Nation) — Standard moneyline market.
3. **#10 Wisconsin ML** (Grade 66, Market 68.8%, -220 BetMGM) — Standard moneyline market.
4. **#35 Jalen Brunson 6+ AST** (Grade 61, Market 56.3%, O5.5 -129 BetMGM) — Exact main consensus assists line (5.5).


* **Correlation check:** Zero same-game overlap (4 separate games across NFL, CBB, and NBA).
* **Payout:** **4.05x** before fees — `1 ÷ (0.840 × 0.759 × 0.688 × 0.563)`.
* **Combined hit chance:** **26.01%** (independent product of grades: `0.85 × 0.76 × 0.66 × 0.61`).
* **Weakest leg:** **#35 Jalen Brunson 6+ AST** (Grade 61).

---

### 20-Leg Long Shot (Experimental — Small Stake Only)

*Uses top 20 eligible unique-player/team legs (avoiding redundant HOU -9.5 alongside HOU ML).*

* **Legs:** #44 Texans ML (85), #1 CJ Stroud 5+ rush yds (82), #30 LaMelo Ball 15+ pts (77), #9 St. Thomas ML (76), #39 Jaden McDaniels 4+ reb (75), #33 Donovan Clingan 10+ pts (73), #15 Nico Collins 60+ rec yds (70), #3 Xavier Hutchinson 30+ rec yds (68), #10 Wisconsin ML (66), #2 Dalton Schultz 25+ rec yds (66), #37 Brook Lopez 4+ reb (65), #5 Tyler Warren 30+ rec yds (65), #48 Jalen Brunson under 30 pts (65), #4 Laquon Treadwell 20+ rec yds (64), #24 ANA/COL over 6 goals (63), #13 Pepperdine +4.5 (62), #16 David Montgomery 60+ rush+rec yds (57), #22 Timberwolves +2.5 (57), #6 Jonathan Taylor 50+ rush yds (56), #49 Mikal Bridges over 15 PRA (56).
* **Correlation check:** Heavy same-game clustering in **IND@HOU** (9 legs: HOU ML, Stroud, Collins, Hutchinson, Schultz, Montgomery, plus IND's Warren, Treadwell, Taylor — positive pass-game correlation for HOU receivers with Stroud/HOU win, mixed negative script tension between HOU blowout and Taylor rushing) and **NY@MIN** (5 legs: Ball, McDaniels, MIN +2.5 positively correlated with Brunson Under 30; Bridges PRA neutral).
* **Payout:** **Cannot calculate** (17 of 20 legs have no verified exact market price).
* **Combined hit chance:** **0.0324%** (~1 in 3,086, assuming independence across grades). Experimental, small stake only.
* **Weakest leg:** **#6 Jonathan Taylor 50+ rushing yards** / **#49 Mikal Bridges over 15 PRA** (tied at Grade 56; #6 carries higher negative game-script risk).

---

### Long-Shot Picks (Experimental — Small Stake Only)

1. **#25 Tank Dell any time touchdown** — Market **27.8%** (+260, SportsGambler) vs Grade **29** (+1.2% edge). Marvin Harrison Jr. is out and IND is missing both starting outside CBs.
2. **#31 Dalton Schultz any time touchdown** — Market **33.3%** (+200, SportsGambler) vs Grade **32**. Brevin Jordan is out and IND has surrendered 17 passing TDs.
3. **#32 Seth McGowan anytime touchdown** — Market **21.0%** (Kalshi/FantasyLabs) vs Grade **21**. Scored in two straight games as IND's RB2.
4. **#34 Donovan Clingan 15+ points** — Grade **43** (no exact price). Upside ceiling play against a MIL frontcourt missing both Myles Turner and Kyle Kuzma.

---

## 6. Perfect Parlays Attempt (Experimental)

**Nothing qualifies for Beta 3 or Beta 10x today.**

* Only **2** eligible legs meet the criteria (Grade 70–86, verified market price within 7 of grade, no PRA, no spreads, game not started): **#44 Texans ML** (Grade 85, Market 84.0%) and **#9 St. Thomas ML** (Grade 76, Market 75.9%).
* Beta 3 requires 3 qualifying legs across 3 games, and Beta 10x requires ~10x combined payout, so neither ticket can be constructed.

---

## 7. Beta Top List (Experimental)

**Simulation not run.** Full 2026-27 player game logs for all 91 Beta lines across 4 NBA games could not be programmatically pulled into the execution environment. Per ground rules, no numbers below are presented as simulated; the ranking below is **judgment, not simulated**, capped at 8 lines (max 1 per player, max 2 per game across 4 games) and skipping questionable/day-to-day players (Deni Avdija, Toumani Camara, Jonathan Kuminga).

| Rank | Player (Team) | Game | Line | Kalshi Ticker | Breakeven % | Judgment Hit % | Est. Edge | Key Risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Donovan Clingan (POR) | POR@MIL | 12+ rebounds | `KXNBAREB-26NOV19PORMIL-PORDCLINGAN23-12` | 61.7% | 66% | +4.3% | Blowout risk (POR -10.5) trims 4Q minutes |
| 2 | Brandin Podziemski (GS) | GS@MEM | 25+ PRA | `KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25` | 60.7% | 64% | +3.3% | Shooting variance as primary option w/ Curry & Green out |
| 3 | Jaime Jaquez Jr. (MIL) | POR@MIL | 15+ points | `KXNBAPTS-26NOV19PORMIL-MILJJAQUEZ24-15` | 54.7% | 58% | +3.3% | Blowout risk; POR length on wing |
| 4 | Victor Wembanyama (SA) | LAC@SA | 12+ rebounds | `KXNBAREB-26NOV19LACSAS-SASVWEMBANYAMA1-12` | 52.7% | 56% | +3.3% | Heavy -15.5 favorite blowout could cap minutes |
| 5 | Karl-Anthony Towns (NY) | NY@MIN | 20+ points | `KXNBAPTS-26NOV19NYKMIN-NYKKTOWNS32-20` | 57.7% | 60% | +2.3% | Foul trouble vs Gobert in low-total (215.5) game |
| 6 | Cedric Coward (MEM) | GS@MEM | 15+ points | `KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15` | 57.7% | 60% | +2.3% | Usage split with Cameron Boozer & Jaylen Wells |
| 7 | OG Anunoby (NY) | NY@MIN | 15+ points | `KXNBAPTS-26NOV19NYKMIN-NYKOANUNOBY8-15` | 56.7% | 59% | +2.3% | Low-possession environment; 3rd scoring option |
| 8 | Devin Vassell (SA) | LAC@SA | 2+ threes | `KXNBA3PT-26NOV19LACSAS-SASDVASSELL24-2` | 56.7% | 59% | +2.3% | 3PT variance and blowout rest risk |

---

## 8. Summary

* **Verified injuries drove major adjustments:** IND is without both starting tackles (Raimann, Travis) and both starting outside CBs (Gardner, Ward); HOU is without Woody Marks, Marvin Harrison Jr., Danielle Hunter, and Azeez Al-Shaair (IR); MIL is without Myles Turner and Kyle Kuzma; MIN is without Anthony Edwards and Donte DiVincenzo.
* **Ineligible slate legs removed:** #8 (COFC@DRKE, started 4:30 PM PT), #23 (BUF@WSH, started 4:00 PM PT), #17/#19/#42/#43 (duplicates), #27 (no line), #45/#46 (Myles Turner void), and #47 (Wembanyama under).
* **Ticket discipline held:** No Hammer qualified (only one priced 80+ leg, #44 Texans ML) and no Perfect Parlays qualified (only two priced 70–86 legs). Both the 5-leg Main Parlay (6.58x) and 4-leg Regular-Lines Parlay (4.05x) clear the 2x floor using verified prices.
* **What could not be verified:** Exact market prices for 36 of the 50 picks (mostly bought-down alt props and secondary NFL/NBA markets), CBB injury reports (#8–#14), NHL starting goalies (#24), and full 2026-27 NBA player game logs for Beta simulation.

---

## 9. Research Notes (from `picks_history_1.csv`)

*All findings filtered strictly to `d_in_win_loss_record == TRUE` (n = 1,146; dates 2026-11-04 to 2026-11-18; overall 743-403, 64.8%).*

1. **Bought-down alt lines vs. regular lines (observed, small sample):** Across 2026-11-04 to 2026-11-18, `alt` lines hit **71.3%** (398/558) compared to `reg` lines at **58.3%** (323/554). *Idea to test:* track ROI after accounting for heavier alt juice rather than raw hit rate alone.
2. **Stat-type dispersion (observed, small sample):** Over the same 15-day window, `3pm` props hit **75.0%** (42/56) and `pts` props hit **67.5%** (183/271), whereas `pra` hit **53.5%** (23/43) and `atd` hit **37.7%** (20/53). *Idea to test:* keeping `pra` out of Perfect Parlays and restricting `atd` to small-stake long-shots aligns with observed hit rates.
3. **Grade vs. Kalshi divergence (`d_head_to_head_eligible == TRUE`, n = 184; dates 2026-11-16 to 2026-11-18; observed, small sample):** When our grade was **8+ points above** the observed Kalshi price, picks hit just **48.6%** (18/37), compared to **65.5%** (38/58) when 0–7 points above Kalshi and **70.8%** (63/89) when below Kalshi. *Idea to test:* continue enforcing the `<8 above market` filter on core tickets.

---

## 10. Result Blocks

```
BD_PICKS_START
pick_no,your_rank,your_grade,market_price,price_source,value_verdict,ticket_ok,regular_line,key_risk,sources_checked_at
44,1,85,84.0,Kalshi via Covers,fair,yes,yes,Divisional TNF variance,2026-11-19 16:35 PT
1,2,82,,,cannot assess,yes,no,Late kneel-downs in blowout,2026-11-19 16:35 PT
30,3,77,,,cannot assess,yes,no,Shooting efficiency vs NYK defense,2026-11-19 16:35 PT
9,4,76,75.9,Bleacher Nation,fair,yes,yes,Early-season CBB variance,2026-11-19 16:35 PT
39,5,75,,,cannot assess,yes,no,Gobert and KAT paint rebounding,2026-11-19 16:35 PT
33,6,73,,,cannot assess,yes,no,Blowout trims 4Q minutes,2026-11-19 16:35 PT
15,7,70,,,cannot assess,yes,no,Run-heavy 2H script,2026-11-19 16:35 PT
3,8,68,,,cannot assess,yes,no,Target competition and blowout script,2026-11-19 16:35 PT
10,9,66,68.8,BetMGM,poor,yes,yes,Seton Hall 3-1 ATS toughness,2026-11-19 16:35 PT
2,10,66,,,cannot assess,yes,no,Route share under 70 pct last 5,2026-11-19 16:35 PT
37,11,65,,,cannot assess,yes,yes,Blowout risk and Wemby glass,2026-11-19 16:35 PT
5,12,65,,,cannot assess,yes,no,Only 1 rec yd last week,2026-11-19 16:35 PT
48,13,65,,,cannot assess,yes,no,High-usage scorer (31 last game),2026-11-19 16:35 PT
29,14,64,61.5,BetMGM via WinDailySports,good,yes,no,Frontcourt rebound competition,2026-11-19 16:35 PT
4,15,64,,,cannot assess,yes,no,Weak IND pass offense behind backup OTs,2026-11-19 16:35 PT
24,16,63,,,cannot assess,yes,no,Goalie variance and push at 6,2026-11-19 16:35 PT
13,17,62,,,cannot assess,yes,no,UCSB 4-0 efficiency edge,2026-11-19 16:35 PT
35,18,61,56.3,BetMGM via SBD,good,yes,yes,Low 215.5 game total,2026-11-19 16:35 PT
41,19,60,,,cannot assess,yes,no,HOU 0-6 ATS last 6 at home,2026-11-19 16:35 PT
20,20,58,,,cannot assess,yes,yes,Blowout script and kneel-downs,2026-11-19 16:35 PT
16,21,57,,,cannot assess,yes,no,Groin return workload cap,2026-11-19 16:35 PT
22,22,57,,,cannot assess,yes,yes,Missing Edwards and DiVincenzo,2026-11-19 16:35 PT
6,23,56,,,cannot assess,yes,yes,Missing both OTs and trailing script,2026-11-19 16:35 PT
17,24,56,,,cannot assess,no,yes,Duplicate of pick 6,2026-11-19 16:35 PT
43,25,56,,,cannot assess,no,yes,Duplicate of pick 6,2026-11-19 16:35 PT
49,26,56,,,cannot assess,yes,yes,Low-usage 4th option,2026-11-19 16:35 PT
23,27,55,56.0,Kalshi via Dimers,fair,no,yes,Game already started,2026-11-19 16:35 PT
11,28,55,53.5,BetMGM,fair,yes,yes,Early CBB margin variance,2026-11-19 16:35 PT
50,29,55,,,cannot assess,yes,yes,Low target volume variance,2026-11-19 16:35 PT
26,30,55,,,cannot assess,yes,yes,Backup RB touch share,2026-11-19 16:35 PT
38,31,54,,,cannot assess,yes,yes,3 of 8 recent hit rate and blowout,2026-11-19 16:35 PT
12,32,54,54.5,FanDuel via Action Network,fair,yes,yes,Wisconsin 1-3 ATS,2026-11-19 16:35 PT
21,33,54,,,cannot assess,yes,yes,Negative game script as 12.5-pt dog,2026-11-19 16:35 PT
7,34,52,53.0,Kalshi via Covers,fair,yes,yes,No HOU rush TD in 32 days,2026-11-19 16:35 PT
19,35,52,53.0,Kalshi via Covers,fair,no,yes,Duplicate of pick 7,2026-11-19 16:35 PT
42,36,52,53.0,Kalshi via Covers,fair,no,yes,Duplicate of pick 7,2026-11-19 16:35 PT
28,37,52,51.7,BetMGM via SBD,fair,yes,yes,41.8 pct FG efficiency,2026-11-19 16:35 PT
40,38,52,,,cannot assess,yes,yes,Hand/shoulder wear and blowout script,2026-11-19 16:35 PT
18,39,51,,,cannot assess,yes,yes,Poor IND passing attack,2026-11-19 16:35 PT
8,40,50,50.5,Fox Sports Radio 1400,fair,no,yes,Game already started,2026-11-19 16:35 PT
14,41,46,,,cannot assess,yes,no,4.5 pts below 154.5 market total,2026-11-19 16:35 PT
34,42,43,,,cannot assess,yes,no,2.5 pts above main line,2026-11-19 16:35 PT
47,43,48,,,cannot assess,no,yes,No Wemby unders rule violation,2026-11-19 16:35 PT
36,44,38,,,cannot assess,yes,no,Market favors U5.5 vs Wemby,2026-11-19 16:35 PT
31,45,32,33.3,SportsGambler,fair,yes,yes,Reduced route share and TD variance,2026-11-19 16:35 PT
25,46,29,27.8,SportsGambler,good,yes,yes,TD variance behind Collins/Montgomery,2026-11-19 16:35 PT
32,47,21,21.0,Kalshi via FantasyLabs,fair,yes,yes,Backup RB on 12.5-pt underdog,2026-11-19 16:35 PT
27,48,insufficient,,,cannot assess,no,no,No line given,2026-11-19 16:35 PT
45,49,insufficient,,,cannot assess,no,no,Player ruled out (void),2026-11-19 16:35 PT
46,50,insufficient,,,cannot assess,no,no,Player ruled out (void),2026-11-19 16:35 PT
BD_PICKS_END
BD_TICKETS_START
ticket_name,leg_pick_no,price_used,price_source
Main,44,84.0,Kalshi via Covers
Main,9,75.9,Bleacher Nation
Main,10,68.8,BetMGM
Main,29,61.5,BetMGM via WinDailySports
Main,35,56.3,BetMGM via SBD
Regular,44,84.0,Kalshi via Covers
Regular,9,75.9,Bleacher Nation
Regular,10,68.8,BetMGM
Regular,35,56.3,BetMGM via SBD
Long20,44,84.0,Kalshi via Covers
Long20,1,,
Long20,30,,
Long20,9,75.9,Bleacher Nation
Long20,39,,
Long20,33,,
Long20,15,,
Long20,3,,
Long20,10,68.8,BetMGM
Long20,2,,
Long20,37,,
Long20,5,,
Long20,48,,
Long20,4,,
Long20,24,,
Long20,13,,
Long20,16,,
Long20,22,,
Long20,6,,
Long20,49,,
BD_TICKETS_END
BD_TICKET_SUMMARY_START
ticket_name,payout_estimate,combined_hit_chance,weakest_leg_pick_no
Main,6.58x,16.65%,35
Regular,4.05x,26.01%,35
Long20,cannot calculate,0.0324%,6
BD_TICKET_SUMMARY_END
BD_BETA_START
your_rank,kalshi_ticker,your_hit_pct,edge_pct,sample_games,simulated_yes_no,runs,key_risk
1,KXNBAREB-26NOV19PORMIL-PORDCLINGAN23-12,66.0,4.3,0,no,0,Blowout trims 4Q minutes
2,KXNBAPRA-26NOV19GSWMEM-GSWBPODZIEMSKI2-25,64.0,3.3,0,no,0,Shooting variance as primary creator
3,KXNBAPTS-26NOV19PORMIL-MILJJAQUEZ24-15,58.0,3.3,0,no,0,Blowout risk vs POR
4,KXNBAREB-26NOV19LACSAS-SASVWEMBANYAMA1-12,56.0,3.3,0,no,0,Blowout rest risk (-15.5)
5,KXNBAPTS-26NOV19NYKMIN-NYKKTOWNS32-20,60.0,2.3,0,no,0,Foul trouble vs Gobert
6,KXNBAPTS-26NOV19GSWMEM-MEMCCOWARD23-15,60.0,2.3,0,no,0,Usage split with Boozer and Wells
7,KXNBAPTS-26NOV19NYKMIN-NYKOANUNOBY8-15,59.0,2.3,0,no,0,Low-possession game environment
8,KXNBA3PT-26NOV19LACSAS-SASDVASSELL24-2,59.0,2.3,0,no,0,3PT variance and blowout rest
BD_BETA_END

```