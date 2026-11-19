# day, pick, est, hit, sport, market, stat, dir, style, boost, star, acefav
# market: prop/ml/spread/total/method ; stat: pts reb ast 3pm pra combo yds rec att ml spread total ko dec sog blk td
# dir: o/u ; style: reg (posted .5 line or ML) / alt (X+ ladder below avg) / ceil (above avg)
R=[]
def a(*x): R.append(x)
# ---- Nov 4 (from recap ledger) ----
N4=[["Herro 15+ PTS",85,1,"pts","o","alt",0,0],["LeBron 4+ AST",80,1,"ast","o","alt",0,1],["McDaniels 10+ PTS",78,1,"pts","o","alt",0,1],["Huerter 2+ REB",78,0,"reb","o","alt",0,0],
["Luka 30+ PTS",74,1,"pts","o","alt",1,1],["KD 20+ PTS",72,1,"pts","o","alt",1,1],["Markkanen o5.5 REB",72,1,"reb","o","reg",0,0],["Brunson o4.5 AST",68,0,"ast","o","reg",1,0],
["Bam U20 PTS",68,0,"pts","u","reg",0,0],["Herro 20+ PTS",67,1,"pts","o","alt",0,0],["Sherwood o1.5 SOG",66,1,"sog","o","reg",0,0],["Brown o19.5 PTS",65,1,"pts","o","reg",1,0],
["KD o21.5 PTS",65,0,"pts","o","reg",1,0],["Flagg 20+ PTS",64,0,"pts","o","alt",1,1],["Mobley U20 PTS",64,1,"pts","u","reg",0,0],["Nuggets ML",62,1,"ml","o","reg",0,1],
["MPJ o20.5 PTS",60,1,"pts","o","reg",0,1],["Brown o5.5 REB",60,1,"reb","o","reg",1,1],["Scheierman 4+ REB",60,1,"reb","o","alt",0,1],["Blazers ML",60,1,"ml","o","reg",0,1],
["Ighodaro U6 REB",60,0,"reb","u","reg",0,0],["Camara U15 PTS",60,1,"pts","u","reg",0,0],["Huerter 3+ REB",60,0,"reb","o","alt",0,1],["Giddey o7.5 AST",58,0,"ast","o","reg",0,0],
["LeBron o5.5 REB",58,1,"reb","o","reg",1,0],["Miller U6 REB",58,1,"reb","u","reg",0,0],["Green U20 PTS",58,0,"pts","u","reg",0,0],["Acuff 20+ PTS",58,1,"pts","o","alt",0,1],
["Trae o9.5 AST",57,0,"ast","o","reg",1,0],["Kings ML",57,1,"ml","o","reg",0,0],["Murray o5.5 AST",55,1,"ast","o","reg",0,0],["McDaniels 15+ PTS",55,0,"pts","o","alt",0,1],
["Herro U25 PTS",55,0,"pts","u","reg",0,0],["Hartenstein 20+ PRA",55,0,"pra","o","alt",0,0],["Giannis o0.5 BLK",55,1,"blk","o","reg",1,0],["Scheierman o13.5 P+R",52,1,"combo","o","reg",0,0],
["Scheierman 10+ PTS",52,0,"pts","o","alt",0,0],["Dunn o16.5 PRA",52,0,"pra","o","reg",0,0],["LeBron 6+ AST",52,1,"ast","o","alt",1,1],["Avdija o1.5 3PM",52,0,"3pm","o","reg",0,0],
["76ers ML",50,1,"ml","o","reg",0,1],["Daniels o11.5 PTS",50,0,"pts","o","reg",0,0],["Dunn U5 AST",50,1,"ast","u","reg",0,0],["Flagg U8 REB",48,0,"reb","u","reg",1,0],
["Jabari U25 PRA",45,1,"pra","u","reg",0,0],["Powell U20 PTS",45,1,"pts","u","reg",0,0],["Wiggins o0.5 BLK",45,1,"blk","o","reg",0,0],["Maluach U6.5 REB",45,1,"reb","u","reg",0,0],
["Kessler o12.5 PTS",42,1,"pts","o","reg",0,0],["Flagg 25+ PTS",42,0,"pts","o","ceil",1,1],["Acuff 25+ PTS",38,0,"pts","o","ceil",0,1],["McCain 3+ REB",38,0,"reb","o","alt",0,0],
["Flagg U7 REB",38,0,"reb","u","reg",1,0],["Dame U6 AST",38,1,"ast","u","reg",1,0],["Hartenstein 25+ PRA",33,0,"pra","o","ceil",0,0],["Herb Jones U3 REB",30,0,"reb","u","reg",0,0],
["McDaniels 20+ PTS",28,0,"pts","o","ceil",0,1],["LeBron 8+ AST",25,1,"ast","o","ceil",1,1],["Dame U5 AST",25,0,"ast","u","reg",1,0],["Flagg 30+ PTS",20,0,"pts","o","ceil",1,1],
["Scheierman DD",10,0,"combo","o","ceil",0,1]]
for p,e,h,st,d,sty,star,fav in N4: a("Nov 4",p,e,h,"NBA" if st!="sog" else "NHL","ml" if st=="ml" else "prop",st,d,sty,0,star,fav)
# ---- Nov 5 ----
N5=[("Lawrence 150+ pass",86,1,"NFL","yds","o","alt",0,1),("Curry 20+",86,1,"NBA","pts","o","alt",0,1),("Curry o28.5 PRA",85,1,"NBA","pra","o","reg",0,1),
("Black 10+",84,1,"NBA","pts","o","alt",1,0),("Henry 30+ rush+rec",84,1,"NFL","yds","o","alt",0,1),("Giannis 20+",84,1,"NBA","pts","o","alt",0,1),
("Jaguars ML",83,1,"NFL","ml","o","reg",0,0),("Giannis 8+ reb",82,1,"NBA","reb","o","alt",0,1),("Lendeborg 15+",76,1,"NBA","pts","o","alt",0,0),
("Lawrence 175+ pass",75,1,"NFL","yds","o","alt",0,1),("Henry 40+ rush",75,1,"NFL","yds","o","alt",0,1),("Fagnano 100+ pass",74,0,"NFL","yds","o","alt",0,0),
("Warriors ML",74,1,"NBA","ml","o","reg",0,0),("Lendeborg 20+ P+A",72,1,"NBA","combo","o","alt",0,0),("Bane 15+",70,1,"NBA","pts","o","alt",0,0),
("Henry U21 att",70,1,"NFL","att","u","alt",0,1),("Franz 20+",68,0,"NBA","pts","o","alt",1,0),("Curry 25+",68,1,"NBA","pts","o","alt",0,1),
("WCJ 6+ reb",68,1,"NBA","reb","o","alt",0,0),("Brooks U6 reb",68,1,"NBA","reb","u","alt",0,0),("UTSA ML",66,0,"CFB","ml","o","reg",0,0),
("Flowers 15+ yds",66,0,"NFL","yds","o","alt",0,1),("Lendeborg 6+ reb",60,1,"NBA","reb","o","alt",0,0),("Lendeborg o22.5 P+A",60,1,"NBA","combo","o","reg",0,0),
("Brooks U5 reb",60,1,"NBA","reb","u","reg",0,0),("Black o14.5",60,0,"NBA","pts","o","reg",1,0),("Bam 15+",60,1,"NBA","pts","o","alt",0,0),
("Lawrence 200+ pass",58,1,"NFL","yds","o","reg",0,1),("Wiggins 15+ PRA",58,0,"NBA","pra","o","alt",0,0),("Podz o3.5 ast",55,0,"NBA","ast","o","reg",0,0),
("Booker o3.5 reb",55,0,"NBA","reb","o","reg",0,1),("Bridges 6+ reb",55,1,"NBA","reb","o","reg",0,0),("P.Washington 50+ yds",55,1,"NFL","yds","o","reg",0,0),
("Henry U17.5 att",55,1,"NFL","att","u","reg",0,1),("Suns ML",52,1,"NBA","ml","o","reg",0,0),("WCJ 10+ pts",52,1,"NBA","pts","o","reg",0,0),
("Henry 50+ rush",52,1,"NFL","yds","o","reg",0,1),("Franz o5.5 reb",50,1,"NBA","reb","o","reg",1,0),("Over 35 total",50,1,"NFL","total","o","alt",0,0),
("Over 36.5 total",45,1,"NFL","total","o","alt",0,0),("Black 6+ ast",45,1,"NBA","ast","o","ceil",1,0),("da Silva 2+ 3PM",45,1,"NBA","3pm","o","reg",0,0),
("Flowers 5+ rec",44,0,"NFL","rec","o","ceil",0,1),("Giannis U11.5 reb",42,0,"NBA","reb","u","reg",0,1),("WCJ o11.5 pts",42,1,"NBA","pts","o","reg",0,0),
("Giannis o29.5",40,0,"NBA","pts","o","ceil",0,1),("Black 6+ reb",40,1,"NBA","reb","o","ceil",1,0),("Franz o6 ast",38,1,"NBA","ast","o","ceil",1,0),
("P.Washington ATD",35,1,"NFL","td","o","ceil",0,0),("Podz 6+ reb",35,1,"NBA","reb","o","ceil",0,0),("Henry ATD",28,0,"NFL","td","o","ceil",0,1),
("Podz 6+ ast",28,0,"NBA","ast","o","ceil",0,0),("Tuten ATD",22,1,"NFL","td","o","ceil",0,0),("J.Hill ATD",12,1,"NFL","td","o","ceil",0,0)]
for p,e,h,sp,st,d,sty,boost,star in N5: a("Nov 5",p,e,h,sp,"ml" if st=="ml" else ("total" if st=="total" else "prop"),st,d,sty,boost,star,0)
# ---- Nov 6 ----
N6=[("PJ o0.5 3PM",84,1,"3pm","o","alt",0,0),("Jerome 15+",82,1,"pts","o","alt",0,0),("Luka 30+",82,1,"pts","o","alt",0,1),("Brown 15+",80,1,"pts","o","alt",0,1),
("SGA 25+",78,1,"pts","o","alt",0,1),("SGA U6.5 ast",78,1,"ast","u","reg",0,1),("Castle 4+ reb",76,0,"reb","o","alt",0,0),("Acuff o1.5 3PM",75,1,"3pm","o","alt",0,0),
("Coward 10+",74,1,"pts","o","alt",0,0),("Coward o1.5 3PM",72,1,"3pm","o","reg",0,0),("Flagg 20+",70,1,"pts","o","alt",0,1),("Peterson 10+",68,1,"pts","o","alt",0,0),
("Avdija 20+",66,1,"pts","o","alt",0,0),("Lillard o16.5",66,1,"pts","o","reg",0,1),("Luka o6.5 ast",66,0,"ast","o","reg",0,1),("Jaquez U3.5 ast",65,1,"ast","u","reg",0,0),
("LaMelo 15+",64,1,"pts","o","alt",1,1),("Markkanen 15+",64,1,"pts","o","alt",0,0),("Ajay Mitchell 15+",64,1,"pts","o","alt",1,0),("Dosunmu 15+",63,1,"pts","o","alt",1,0),
("Naz Reid 15+",62,0,"pts","o","alt",1,0),("McDaniels 15+",62,1,"pts","o","alt",1,0),("Coward 12+",62,0,"pts","o","alt",0,0),("Zion 20+",60,0,"pts","o","alt",0,1),
("Tatum 7+ ast",60,1,"ast","o","reg",0,1),("Fears 4+ reb",60,1,"reb","o","reg",0,0),("Luka 35+",58,1,"pts","o","ceil",0,1),("LeBron 7+ ast",58,0,"ast","o","reg",0,1),
("PJ o1.5 3PM",58,1,"3pm","o","reg",0,0),("LaVine o2.5 reb",58,1,"reb","o","reg",0,1),("J.Hayes 4+ reb",58,1,"reb","o","reg",0,0),("LeBron o13.5 R+A",57,0,"combo","o","reg",0,1),
("LeBron 7+ reb",56,1,"reb","o","reg",0,1),("Peterson 12+",55,1,"pts","o","reg",0,0),("Barrett 20+",55,1,"pts","o","reg",1,1),("Clingan U11.5",52,0,"pts","u","reg",0,0),
("Shead 4+ ast",50,1,"ast","o","reg",1,0),("R.Williams o12.5 P+R",48,1,"combo","o","reg",0,0),("D.Mitchell o24.5",42,0,"pts","o","ceil",0,1),("Tatum 7+ reb",40,1,"reb","o","ceil",0,1),
("Shead 6+ ast",30,1,"ast","o","ceil",1,0),("Barrett 25+",28,1,"pts","o","ceil",1,1)]
for p,e,h,st,d,sty,boost,star in N6: a("Nov 6",p,e,h,"NBA","prop",st,d,sty,boost,star,0)
# ---- Nov 7 ----
N7=[("Michigan ML",84,0,"CFB","ml","o","reg",0,0),("Houston ML",78,1,"CFB","ml","o","reg",0,0),("Miami +10.5",74,1,"CFB","spread","o","alt",0,0),
("Ohio State ML",73,0,"CFB","ml","o","reg",0,0),("McCollum 10+",72,0,"NBA","pts","o","alt",1,0),("Utah -4 (live)",72,1,"CFB","spread","o","reg",0,0),
("Notre Dame ML",71,1,"CFB","ml","o","reg",0,0),("Shamet 6+",70,1,"NBA","pts","o","alt",1,0),("South Carolina ML",69,1,"CFB","ml","o","reg",0,0),
("Oklahoma St ML",69,1,"CFB","ml","o","reg",0,0),("LSU ML",67,0,"CFB","ml","o","reg",0,0),("Florida ML",66,0,"CFB","ml","o","reg",0,0),
("Shamet o6.5",66,1,"NBA","pts","o","reg",1,0),("Purdue ML",65,0,"CFB","ml","o","reg",0,0),("Avdija 20+",63,0,"NBA","pts","o","alt",0,0),
("Nembhard 2+ reb",62,0,"NBA","reb","o","alt",1,0),("Georgia ML",61,1,"CFB","ml","o","reg",0,0),("MPJ 20+",58,1,"NBA","pts","o","alt",0,0),
("Holiday 20+ PRA",56,0,"NBA","pra","o","alt",0,0),("Baylor ML (live)",55,1,"CFB","ml","o","reg",0,0),("UConn +7.5",52,0,"CFB","spread","o","reg",0,0),
("McCollum o13.5",52,0,"NBA","pts","o","reg",1,0),("Harper o4.5 ast",50,0,"NBA","ast","o","reg",0,0),("MPJ o21.5",48,1,"NBA","pts","o","reg",0,0),
("Avdija o23.5",47,0,"NBA","pts","o","reg",0,0),("Holiday o21.5 PRA",47,0,"NBA","pra","o","reg",0,0),("Utah ML + u57.5",45,1,"CFB","total","u","reg",0,0),
("Syracuse +1.5",45,0,"CFB","spread","o","reg",0,0),("FSU ML (live)",40,1,"CFB","ml","o","reg",0,0),("Nembhard o2.5 reb",40,0,"NBA","reb","o","reg",1,0),
("BYU/Utah u49.5",38,1,"CFB","total","u","reg",0,0),("FSU -5.5 (live)",30,1,"CFB","spread","o","reg",0,0),
("Avdija 15+",85,1,"NBA","pts","o","alt",0,0),("Harden 10+",86,0,"NBA","pts","o","alt",1,0),("MPJ 15+",80,1,"NBA","pts","o","alt",0,0),("Shamet 5+",78,1,"NBA","pts","o","alt",1,0),
("Avdija 18+",72,0,"NBA","pts","o","alt",0,0),("Harden o16.5",52,0,"NBA","pts","o","reg",1,0),
("Bashi ML",85,1,"UFC","ml","o","reg",0,0),("Milosevic ML",81,1,"UFC","ml","o","reg",0,0),("Fernando ML",75,1,"UFC","ml","o","reg",0,0),("Smith ML",74,1,"UFC","ml","o","reg",0,0),
("Kondratavicius ML",74,0,"UFC","ml","o","reg",0,0),("Degli ML",68,0,"UFC","ml","o","reg",0,0),("Cortes-Acosta ML",68,0,"UFC","ml","o","reg",0,0),("Silva ML",67,1,"UFC","ml","o","reg",0,0),
("Petersen ML",61,1,"UFC","ml","o","reg",0,0),("Bashi KO/Sub",50,1,"UFC","method","o","reg",0,0),("Magomedov ML",48,1,"UFC","ml","o","reg",0,0),("Fernando KO",45,0,"UFC","method","o","reg",0,0),
("Kondratavicius KO",42,0,"UFC","method","o","reg",0,0),("Milosevic KO",38,1,"UFC","method","o","reg",0,0),("Parsons ML",34,0,"UFC","ml","o","reg",0,0),("Silva by dec",32,1,"UFC","method","o","reg",0,0)]
for p,e,h,sp,st,d,sty,boost,star in N7: a("Nov 7",p,e,h,sp,"ml" if st=="ml" else ("spread" if st=="spread" else ("total" if st=="total" else ("method" if st=="method" else "prop"))),st,d,sty,boost,star,0)
