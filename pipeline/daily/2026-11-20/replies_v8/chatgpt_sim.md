I ran the supplied Python for 1,000 simulations per game across all five NBA games, using pregame box scores weighted 70% to the last 10 games; Q rows are conditional on playing under the 6:30 PM ET NBA injury report and are excluded from the top 10.

BD_SIM_START
line_no,sim_hit_pct,minutes_used,key_input
1,58.4,29,2.3 AST per 36 weighted
2,49.4,32,Q eye - if active
3,43.2,32,Q eye - if active
4,31.2,32,3.5 AST per 36 weighted
5,37.1,32,27.2 PRA per 36 weighted
6,36.1,32,16.3 PTS per 36 weighted
7,47.2,29,2.2 3PM per 36 weighted
8,48.2,29,2.2 AST per 36 weighted
9,63.6,29,21.4 PRA per 36 weighted
10,62.1,29,14.5 PTS per 36 weighted
11,50.6,33,4.3 REB per 36 weighted
12,34.8,20,20-minute bench projection
13,52.8,29,3.7 3PM per 36 weighted
14,54.2,29,27.8 PRA per 36 weighted
15,47.8,29,2.2 AST per 36 weighted
16,34.6,29,15.9 PTS per 36 weighted
17,61.4,36,3.2 3PM per 36 weighted
18,43.1,36,5.7 AST per 36 weighted
19,60.5,36,5.0 REB per 36 weighted
20,43.0,31,1.7 3PM per 36 weighted
21,46.5,31,32.2 PRA per 36 weighted
22,53.7,17,4.3 REB per 36 weighted
23,50.3,38,43.8 PRA per 36 weighted
24,52.9,38,24.2 PTS per 36 weighted
25,54.6,26,15.4 PTS per 36 weighted
26,56.6,26,8.4 REB per 36 weighted
27,55.9,25,Holmgren out and Mara starts
28,62.9,25,Holmgren out and Mara starts
29,45.4,27,Caruso and Wallace out
30,41.4,27,Caruso and Wallace out
31,60.9,25,6.2 AST per 36 weighted
32,51.8,25,33.9 PRA per 36 weighted
33,41.8,30,3.0 3PM per 36 weighted
34,61.3,30,25.6 PRA per 36 weighted
35,60.4,30,18.6 PTS per 36 weighted
36,38.8,18,18-minute return-to-rotation projection
37,44.7,30,6.7 AST per 36 weighted
38,50.8,30,19.1 PTS per 36 weighted
39,47.3,23,Reserve role limits minutes
40,55.2,23,Reserve role limits minutes
41,45.1,33,4.3 REB per 36 weighted
42,47.2,29,6.6 REB per 36 weighted
43,39.4,29,1.9 3PM per 36 weighted
44,51.0,24,24 bench minutes with Markkanen out
45,35.6,23,4.9 AST per 36 weighted
46,49.7,23,14.2 PTS per 36 weighted
47,52.9,31,4.6 AST per 36 weighted
48,61.0,31,30.1 PRA per 36 weighted
49,47.0,32,36.0 PRA per 36 weighted
50,53.5,27,2.6 3PM per 36 weighted
51,48.3,27,2.6 AST per 36 weighted
52,37.5,27,25.1 PRA per 36 weighted
53,33.5,27,17.8 PTS per 36 weighted
54,42.8,27,4.7 REB per 36 weighted
55,42.7,24,26.8 PRA per 36 weighted
56,48.5,24,5.3 REB per 36 weighted
57,47.6,25,25 minutes with Utah short on bigs
58,57.1,25,25 minutes with Utah short on bigs
59,53.9,20,7.7 REB per 36 weighted
60,50.1,20,9.1 PTS per 36 weighted
61,43.3,35,34.3 PRA per 36 weighted
62,59.4,35,4.4 REB per 36 weighted
63,47.5,25,2.3 3PM per 36 weighted
64,48.3,25,8.7 REB per 36 weighted
65,49.9,25,25 minutes with Mark Williams out
66,40.2,25,25 minutes with Mark Williams out
67,50.7,21,3.1 REB per 36 weighted
68,56.3,34,Q hip - if active
69,49.5,34,Q hip - if active
70,54.0,34,Q hip - if active
71,21.2,27,33.5 PRA per 36 weighted
72,32.9,27,13.5 REB per 36 weighted
73,55.5,25,25 minutes with starting role uncertain
74,52.1,25,25 minutes with starting role uncertain
75,43.1,34,7.4 AST per 36 weighted
76,54.3,34,52.3 PRA per 36 weighted
77,56.0,34,38.0 PTS per 36 weighted
78,51.4,19,7.7 AST per 36 weighted
79,46.0,19,18.6 PTS per 36 weighted
80,41.6,22,14.5 PRA per 36 weighted
81,46.8,32,Reaves out keeps Grimes in the starting five
82,38.5,23,2.6 AST per 36 weighted
83,50.7,23,15.2 PTS per 36 weighted
84,45.6,28,32.4 PRA per 36 weighted
85,40.0,30,28.7 PRA per 36 weighted
86,38.5,29,1.8 AST per 36 weighted
87,61.0,29,27.4 PRA per 36 weighted
88,60.1,34,39.3 PRA per 36 weighted
89,20.0,21,0.5 3PM per 36 weighted
90,58.6,21,6.7 REB per 36 weighted
91,64.0,30,2.9 AST per 36 weighted
92,54.2,30,18.8 PRA per 36 weighted
93,45.1,30,11.9 PTS per 36 weighted
94,50.8,26,Q illness - if active
95,60.8,26,Q illness - if active
96,45.0,26,Q illness - if active
97,58.0,26,Q illness - if active
98,32.6,29,33.0 PRA per 36 weighted
99,67.2,34,28.8 PRA per 36 weighted
100,48.3,30,28.7 PRA per 36 weighted
101,40.2,30,6.2 REB per 36 weighted
102,36.2,29,3.0 3PM per 36 weighted
103,32.2,33,8.7 AST per 36 weighted
104,27.9,33,28.1 PRA per 36 weighted
105,53.3,21,6.7 AST per 36 weighted
BD_SIM_END

BD_SIMTOP_START
rank,line_no,why
1,99,Kyshawn George: 28.8 PRA per 36 with 34 minutes projected
2,91,Isaac Okoro: 2.9 AST per 36 with 30 minutes projected
3,9,Cameron Johnson: 21.4 PRA per 36 against a 15 PRA threshold
4,28,Aday Mara: Holmgren out and Mara projected to start
5,10,Cameron Johnson: 14.5 PTS per 36 with 29 minutes projected
6,34,Jared McCain: 30-minute starting role with Wallace and Caruso out
7,48,Darryn Peterson: 30.1 PRA per 36 with 31 minutes projected
8,62,Keyonte George: 35-minute role supports 4+ rebounds
9,77,Luka Dončić: 38.0 PTS per 36 even with a blowout discount to minutes
10,73,Jake LaRavia: 25 projected minutes without assuming a start
BD_SIMTOP_END
