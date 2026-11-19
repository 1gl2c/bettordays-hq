import json,re
P=[
("00:00","faith","The LORD is my shepherd; I shall not want.\n\nPsalm 23:1"),
("00:30","grind","Midnight check. Tuesday's graded, the jar is 84% green, and tomorrow's board is already on the way. bettordays.xyz"),
("01:00","gratitude","Grateful for everyone who tailed, faded, or just watched this week. You're part of it."),
("01:30","process","We don't grade on vibes. Every leg gets a hit %, and every hit % gets checked against the box score."),
("02:00","faith","Rejoicing in hope; patient in tribulation; continuing instant in prayer.\n\nRomans 12:12"),
("02:30","motivation","Small edges, every single day. That's the whole game."),
("03:00","engagement","Night owls, real question: what's the one leg you always add and always regret? 👇"),
("03:30","grind","Up late or up early, the work's the same. Grade it. Build it. Track it."),
("04:00","faith","Wait on the LORD: be of good courage, and he shall strengthen thine heart.\n\nPsalm 27:14"),
("04:30","process","Rule we learned this week: a coin flip doesn't belong on a 2x ticket. Lotto only."),
("05:00","motivation","East coast is up. Coffee, box scores, discipline. ☕"),
("05:30","gratitude","Thankful for a green Tuesday and a Family that shows up. Receipts drop at 9 AM PT."),
("06:00","faith","Delight thyself also in the LORD; and he shall give thee the desires of thine heart.\n\nPsalm 37:4"),
("06:30","engagement","Good morning BettorDays Family ☀️ Drop a 🟢 if you cashed yesterday."),
("07:00","grind","Picks drop at 2 PM PT. The countdown is live on the site. ⏳ bettordays.xyz"),
("07:30","process","Before you build today: is every leg 70%+? Does each leg bump the payout 10%? If not, cut it."),
("08:00","motivation","Yesterday: 19 of 21 legs at 70%+ hit. Today we run it back. Smarter. 🟢"),
("08:30","engagement","Quick poll. Which ticket do you play most?\n🔨 Hammer\n2️⃣ The 2x\n🎰 Lotto\n⚡ All of em"),
("09:00","results","TUESDAY RECEIPTS 🧾\n\n✅ 9-leg cashed 5.34x ($534)\n✅ 3-leg cashed 2.29x ($229)\n❌ Hammer: 5 of 6, Brown came up short\n\n70%+ legs: 19/21\nNet: +$186\n7-day: +$2,218\n\nbettordays.xyz"),
("09:30","faith","The LORD shall fight for you, and ye shall hold your peace.\n\nExodus 14:14"),
("10:00","process","Why'd an extra 90% leg DROP your payout? Kalshi takes a cut per leg. If the cut beats the bump, you lose. Free leg checker: bettordays.xyz"),
("10:30","grind","Lost 3 tickets by one leg yesterday. We don't cry about it. We study it. New rules are up on the site."),
("11:00","gratitude","To everyone who made an account this week: welcome to the Family. It's free and it stays free. bettordays.xyz"),
("11:30","engagement","10 NBA games tonight. Watching first: Knicks-Cavs, Lakers-Bucks, or Spurs-Bulls? 👇"),
("12:00","slate","WEDNESDAY SLATE 🏀 (PT)\n\n4:00 CLE@NYK · BOS@TOR · WAS@IND\n5:00 DEN@MEM · LAL@MIL · SAS@CHI · BKN@NOP\n6:00 ORL@UTA\n6:30 GSW@HOU\n7:00 OKC@POR\n\nBoard drops 2 PM. Graded by 3."),
("12:30","faith","For with God nothing shall be impossible.\n\nLuke 1:37"),
("13:00","bestplays","Capper board lands in 1 hour. Every pick graded with a real hit %. Best Plays card right after. ⏳\n\nbettordays.xyz"),
("13:30","motivation","Patience is a position. We don't bet until the board is graded."),
("14:00","engagement","Board just dropped. 🚨 Grading every pick now. Turn on the 🔔 at bettordays.xyz so you get pinged when tickets land."),
("14:30","process","Today's build rules:\n• Coin flips go in the lotto only\n• No leg on more than 2 tickets\n• Every leg bumps the payout 10%+"),
("15:00","75club","THE 75% CLUB 🟢\n\n[FILL AT 3 PM: today's 70%+ legs with grades]\n\nOur 70%+ tier since Nov 4: 87 of 104 (84%).\nbettordays.xyz"),
("15:30","faith","Let your light so shine before men, that they may see your good works.\n\nMatthew 5:16"),
("16:00","ticket","TICKET OF THE DAY 🔨\n\n[FILL AT 3 PM: legs + Kalshi price]\n\nEvery leg 70%+. Pays 2x or more.\nbettordays.xyz"),
("16:30","hype","FIRST TIPS ARE UP 🔥 3 games live, 7 more coming. Sweat it with the Family in the room. bettordays.xyz"),
("17:00","grind","5 PM wave tipping now: Nuggets, Lakers, Spurs, Nets. Every leg tracked live."),
("17:30","engagement","Halftime in the East. How's your ticket looking? 🟢 or 😬"),
("18:00","gratitude","Win or lose tonight, grateful to build this with you. The process stays the same."),
("18:30","faith","I have fought a good fight, I have finished my course, I have kept the faith.\n\n2 Timothy 4:7"),
("19:00","motivation","Late games decide tickets. Stay focused, stay calm, let it play out."),
("19:30","process","Win or lose, every leg gets graded by 9 AM. That's how the model gets sharper every day."),
("20:00","sweat","SWEAT CHECK 💦\n\n[FILL: ✓ legs hit / ⏳ legs live]\n\nRoom is open: bettordays.xyz"),
("20:30","engagement","Thunder at Blazers again, one night after Portland won by 20. Revenge or repeat? 👇"),
("21:00","faith","Weeping may endure for a night, but joy cometh in the morning.\n\nPsalm 30:5"),
("21:30","grind","Grading starts the second the last buzzer hits. Misses get posted too."),
("22:00","gratitude","Thank you for riding with us today. Family over everything. 🤝"),
("22:30","recap","WEDNESDAY RECAP 🧾\n\n[FILL: tickets ✓/✗ and net]\n\nFull receipts 9 AM PT.\nbettordays.xyz"),
("23:00","motivation","Tomorrow's board drops at 2 PM PT. The countdown is already running. ⏳ bettordays.xyz"),
("23:30","faith","I will both lay me down in peace, and sleep: for thou, LORD, only makest me dwell in safety.\n\nPsalm 4:8"),
]
assert len(P)==48 and len({t for t,_,_ in P})==48
FIX={'results','slate','bestplays','75club','ticket','hype','sweat','recap'}
for t,ty,x in P:
  assert '—' not in x and '–' not in x, t
  assert not re.search(r'\b(know|knew|lock|guarantee|can\'t lose|no miss)',x,re.I),t
  if ty not in FIX: assert len(x)<200,(t,len(x))
assert len({x for _,_,x in P})==48
print('faith',sum(ty=='faith' for _,ty,_ in P))
d={"date":"2026-11-11","posts":[{"time":t,"type":ty,"text":x,"posted":False} for t,ty,x in P]}
json.dump(d,open('xposts-2026-11-11.json','w'),ensure_ascii=False)
