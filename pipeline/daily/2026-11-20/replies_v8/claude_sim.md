Ran the code (seed 20, 1,000 runs per game), with one change: I used 105 inputs drawn from my own prior knowledge of roles, minutes and rates. I did not web-search tonight's injury report, beat-reporter news or game logs, and I left matchup and pace multipliers at 1.00 (no adjustment). Treat the numbers as rough, and check for late scratches before using any of them. Rosters for some players (Durant, Trae Young, Anthony Davis, McCain, DeRozan) were taken from the line list, not verified.

BD_SIM_START
line_no,sim_hit_pct,minutes_used,key_input
1,82.3,30,Gordon ast rate 0.12/min
2,52.5,33,Sengun PRA rate 1.10/min
3,49.6,33,Sengun pts rate 0.60/min
4,77.8,33,Amen ast rate 0.17/min
5,82.5,33,Amen PRA rate 0.97/min
6,73.0,33,Amen pts rate 0.55/min
7,74.9,30,CJohnson 3PM rate 0.10/min
8,86.0,30,CJohnson ast rate 0.13/min
9,92.3,30,CJohnson PRA rate 0.80/min
10,85.4,30,CJohnson pts rate 0.50/min
11,67.9,30,Braun reb rate 0.17/min
12,74.3,26,DeRozan pts rate 0.50/min
13,56.5,32,VanVleet 3PM rate 0.10/min
14,77.6,32,VanVleet PRA rate 0.77/min
15,52.7,31,Jabari ast rate 0.06/min
16,53.8,31,Jabari pts rate 0.50/min
17,50.8,33,Murray 3PM rate 0.09/min
18,71.5,33,Murray ast rate 0.24/min
19,55.2,33,Murray reb rate 0.12/min
20,77.1,34,Durant 3PM rate 0.09/min
21,65.6,34,Durant PRA rate 0.98/min
22,73.0,22,Smart reb rate 0.13/min
23,75.3,35,Jokic PRA rate 1.50/min
24,64.6,35,Jokic pts rate 0.80/min
25,58.0,24,Eason pts rate 0.45/min
26,52.3,24,Eason reb rate 0.25/min
27,33.8,18,Mara PRA with only 18 min
28,38.6,18,Mara pts with only 18 min
29,75.2,28,Mitchell ast rate 0.20/min
30,51.6,28,Mitchell PRA rate 0.90/min
31,57.9,26,Hartenstein ast rate 0.17/min
32,44.4,26,Hartenstein PRA rate 0.92/min
33,54.9,24,McCain 3PM rate 0.13/min
34,42.9,24,McCain PRA rate 0.78/min
35,36.7,24,McCain pts rate 0.55/min
36,56.3,18,JaylinW ast with only 18 min
37,58.6,32,Fears ast rate 0.20/min
38,59.5,32,Fears pts rate 0.50/min
39,49.7,15,KenrichW ast with only 15 min
40,46.9,15,KenrichW reb with only 15 min
41,67.1,33,SGA reb rate 0.15/min
42,66.7,30,Zion reb rate 0.24/min
43,74.2,30,Bailey 3PM rate 0.10/min
44,62.1,24,Sensabaugh 3PM rate 0.10/min
45,75.2,28,Gillespie ast rate 0.20/min
46,61.2,28,Gillespie pts rate 0.40/min
47,65.5,32,Peterson ast rate 0.15/min
48,70.0,32,Peterson PRA rate 0.90/min
49,67.8,34,Booker PRA rate 1.13/min
50,83.4,31,Brooks 3PM rate 0.12/min
51,76.8,31,Brooks ast rate 0.10/min
52,74.1,31,Brooks PRA rate 0.78/min
53,62.6,31,Brooks pts rate 0.55/min
54,52.4,31,Brooks reb rate 0.13/min
55,81.3,30,JGreen PRA rate 0.85/min
56,62.3,30,JGreen reb rate 0.15/min
57,37.5,18,Hayes ast with only 18 min
58,42.6,18,Hayes reb with only 18 min
59,64.4,22,Goodwin reb rate 0.22/min
60,69.9,22,JoshGreen pts low line of 5
61,45.8,33,KeyonteGeorge PRA rate 1.03/min
62,59.0,33,KeyonteGeorge reb rate 0.13/min
63,70.8,31,Bridges 3PM rate 0.09/min
64,54.2,31,Bridges reb rate 0.20/min
65,77.5,24,Ighodaro PRA rate 0.82/min
66,62.8,24,Ighodaro reb rate 0.30/min
67,67.6,26,Sexton reb rate 0.10/min
68,57.9,29,Hunter 3PM rate 0.07/min
69,66.2,29,Hunter ast rate 0.08/min
70,66.0,29,Hunter reb rate 0.17/min
71,92.7,34,Sabonis PRA rate 1.25/min
72,65.2,34,Sabonis reb rate 0.40/min
73,82.9,27,LaRavia 1+ three is a low bar
74,52.4,27,LaRavia reb rate 0.15/min
75,75.9,35,Doncic ast rate 0.30/min
76,41.7,35,Doncic PRA rate 1.37/min
77,23.4,35,Doncic pts rate 0.85/min
78,86.7,28,Monk ast rate 0.25/min
79,80.8,28,Monk pts rate 0.50/min
80,61.9,22,Thybulle PRA rate 0.53/min
81,49.6,28,Grimes reb rate 0.13/min
82,52.5,18,Mamukelashvili ast with only 18 min
83,32.4,18,Mamukelashvili pts with only 18 min
84,27.0,24,Kessler PRA with only 24 min
85,69.9,31,LaVine PRA rate 0.93/min
86,68.2,30,Sarr ast rate 0.09/min
87,81.8,30,Sarr PRA rate 0.86/min
88,55.1,30,ADavis PRA rate 1.20/min
89,80.1,28,Coulibaly 1+ three is a low bar
90,57.1,28,Coulibaly reb rate 0.15/min
91,66.7,26,Okoro ast rate 0.10/min
92,40.3,26,Okoro PRA rate 0.53/min
93,28.2,26,Okoro pts rate 0.30/min
94,50.9,24,JalenSmith 3PM rate 0.08/min
95,39.4,24,JalenSmith ast rate 0.06/min
96,37.3,24,JalenSmith PRA rate 0.96/min
97,66.9,24,JalenSmith reb rate 0.40/min
98,61.5,32,Giddey PRA rate 1.02/min
99,33.0,30,KyshawnGeorge PRA rate 0.75/min
100,47.7,29,Buzelis PRA rate 0.85/min
101,69.1,29,Buzelis reb rate 0.25/min
102,62.8,29,Powell 3PM rate 0.12/min
103,78.4,33,TraeYoung ast rate 0.40/min
104,81.9,33,TraeYoung PRA rate 1.15/min
105,72.5,28,TreJones ast rate 0.20/min
BD_SIM_END

BD_SIMTOP_START
rank,line_no,why
1,71,Sabonis 30+ PRA at 34 min and about 1.25 PRA/min
2,9,C Johnson 15+ PRA is a low bar at 30 min
3,78,Monk 4+ ast with a primary-creator role
4,8,C Johnson 2+ ast at 30 min
5,50,Brooks 2+ threes at about 31 min
6,55,J Green 20+ PRA with heavy PHX usage
7,104,Trae Young 30+ PRA with 0.40 ast/min
8,87,Sarr 20+ PRA as a starting big
9,29,Mitchell 4+ ast with a starter role
10,41,SGA 4+ reb needs only about 33 min
BD_SIMTOP_END
