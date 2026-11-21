# BettorDays Full Audit · [DATE]

You are not one advisor. You are a full team inside one answer. Work through the audit as each of these people, in order, and let them argue with each other:

1. **AI engineer** who builds multi-model prediction systems
2. **Sharp sports bettor** who has beaten closing lines for years
3. **Product designer** who has shipped top-10 sports apps
4. **Growth marketer** who took a betting media brand from 0 to 1 million users
5. **Business consultant** who has valued and sold sports betting tool companies
6. **Compliance lead** from a licensed US sportsbook

Be blunt. Praise is useless to us. Every point needs a specific screen, number or example.

## The business

BettorDays (bettordays.xyz) is a free sports betting research app, 21+, run by one founder with AI help. The goal: a billion-dollar company that actually puts money in bettors' pockets. The picks have to be that good, and the app has to be that easy: a new user should find tonight's best legs and build a smart ticket in under 30 seconds, on a phone.

**How the picks are made today:**
- The founder collects picks from several cappers he follows on X (Twitter), by hand, every day. Scraping X is hard because most AI tools can't log in there.
- Our own system grades every leg from game logs, matchup and injuries.
- Engine v8: AI models grade every leg blind (no market price shown), and our grade is the middle of their numbers plus our system grade. Kalshi's price is the referee after: Kalshi at or above our grade is GREEN, 1 to 7 below is YELLOW, and we pull legs where we are 8+ above Kalshi.
- Each AI also runs a 1,000-run simulation per NBA game on near-even player lines, prices hidden.
- Cost problem: running four flagship models with web research cost about $9 in one day. We are now Claude-only by default to stay near $1 a day. The founder wants several models (he hears ChatGPT and Gemini may be better at sports) combined into one BettorDays model, at the lowest cost that keeps the best data.

**Our record (Nov 4 to 19, 1,195 graded legs):**
- Legs graded 70+ with Kalshi at or above our grade: 124-17 (88%). We 1 to 7 above Kalshi: 85-18. We 8+ above Kalshi: 55-45.
- Best groups at 70+: NBA assists 32-7, threes 21-4, points 95-26, favorite moneylines 17-4. Rebounds 49-20.
- Worst: PRA 15-8 at 70+ (7-6 in the nightly top 25), NFL receiving yards 6-15 in the top 25, anytime touchdowns 24-40, college moneylines 24-16.
- Our own simulations have not beaten the price yet: 308 graded sim lines went 164-144 against a 57% average break-even.

**New this week:** a Master filter on the Picks page, agent simulations with filters on the Beta page, a Parlay Grader (screenshot any slip, every leg graded), a sign-up bonus finder by state, a referral program, and a one-time feedback question to members. 23 member accounts so far.

## The site, as a visitor sees it on a phone

[PACK]

## Answer all of these

1. **Grading process.** How do we combine several models into one BettorDays model that is more accurate than any single one, at the lowest cost? Which model for which job (news, matchups, simulation, reading slips)? How should we weight the models over time using their graded record? What cheap data should we feed them so they don't need expensive web browsing every run?
2. **Getting capper picks automatically.** The founder follows cappers on X. What is the legal, reliable way to pull their posts daily (X API tiers and price, Grok's access to X, RSS or alerts, or asking cappers to send picks another way)? Name the cheapest option that works.
3. **User experience.** The home page is 26 phone screens long and History is 275 screens. What should the first screen show? What should the navigation be (name the tabs)? What should be cut, merged or hidden? Walk us through a new user's first 30 seconds as you'd design it.
4. **Usefulness.** What would make a regular bettor open this every day? What would make a sharp bettor pay $30 a month?
5. **Run itself.** What can be automated end to end so the founder only reviews, not builds, each day?
6. **Growth and money.** Fastest honest path to 1,000 active users and the first $10,000 a month. Judge each: Parlay Grader (worth the AI cost per slip?), bonus finder, referral program, paid tier (what is free, what is paid).
7. **Trust and compliance.** What would make a skeptic believe the record? What could get this shut down or sued? Be specific about affiliate licensing, 21+ rules, responsible gambling and advertising claims.

## Answer format (required)

Write your team's discussion first. Then:

BD_AUDIT_START
rank,area,change,why_it_matters,effort_days
BD_AUDIT_END

20 rows, ranked by impact on our goal. `area` is one of: grading, data, ux, growth, money, trust, compliance, ops. No commas inside a field.

BD_VERDICT_START
idea,verdict,one_line_reason
BD_VERDICT_END

One row each for: parlay grader, bonus finder, referral program, paid tier, multi-model blend, X capper automation.

BD_NAV_START
tab_order,tab_name,what_it_holds
BD_NAV_END

Your proposed bottom navigation for the phone app, 4 or 5 tabs.
