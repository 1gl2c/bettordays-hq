**BettorDays’ desktop slip passes the arithmetic test. The biggest remaining trust issue is the phrase “our true chance.”** On the three-leg slip I built, the market prices implied about **72%** under independence. BettorDays raised that to **79%**. That adjustment turned an estimated **2¢ loss** into an estimated **8¢ profit per $1**. There is encouraging historical evidence for the adjustment on favorites, but the published tracker had **zero forward-tested legs** under the new rule.

The site has improved since the first audit. The season ROI, Friday recap, same-game warning, slip persistence and iPhone clipping all passed this retest. **My first product change now would be a timestamped receipt for each published ticket** showing exactly what the user could see before the games, the price needed, and how it settled. That would improve Board, Research, Proof and your social posts at once.

## Desktop navigation and the iPhone retest

I tested signed out at **1440 × 900 CSS pixels**, with an additional check at **1872 px wide**. I checked 20 public pages and Research views. I briefly used 390 px to open Me because the site hides it at desktop width, then inspected its destinations at 1440 px. Signed-in results, exchange fills and physical iPhone Safari remain unverified.

| Area | What happened |
|---|---|
| **Desktop navigation** | Board, Grader and Proof worked from **19 of 20** tested views, **57 successful transitions**. Terms and privacy had none of those three controls. The main header had eight controls. Grader and Sign-up Offers had five, dropping Past nights, Pick & post and Tour. **Me was absent at full width.** |
| **Every Me item** | Full Board and Top 25, Research Lab, Past Nights, Older Recaps, How It Works, Sign-up Offers and Founders opened. Profile and invites, Pick & post, Leaderboard, Feed and Chat each opened the signup dialog. All five now say **“account.”** Talk to Ace, Tour and Add to Home Screen opened. Grader’s version of Me also exposed Terms and privacy, but omitted Tour and Add to Home Screen. |
| **Board → Grader → Board** | All three selected legs survived the round trip. Grader accepted the guest interaction, explained the account requirement and retained the pasted legs. Its upload notice now names OpenRouter and tells users what to crop. I did not submit a personal slip. |
| **iPhone-width slip** | At 390 px, the expanded summary ran from **x=52 to x=338**. The clipping I found in the first audit is fixed in the tested layout. At 1440 px, the summary had **1,084 px** of usable width. |
| **Settled Board** | Copying was disabled correctly. The page still paired a settled Friday ticket and “Pregame closed” with an instruction to **lock at this price or better**. A settled card should show the forecast, result and price assumptions in past tense. |



BettorDays-desktop-slip.jpg



## Three-leg slip and Friday’s proof

I selected **Trae Young 10+ points** at 92¢, **Tyrese Proctor 1+ three** at 85¢, and **Isaiah Hartenstein 2+ assists** at 92¢. Each played in a different game.

| Metric | Displayed | Independent calculation | Verdict |
|---|---:|---:|---|
| Estimated payout after fees | 1.36× | 1.360249× | Correct under the site’s pricing formula |
| Win rate needed | 74% | 73.5159% | Correct rounding |
| “Our true chance” | 79% | 79.3453% | Correct output of the fitted favorite model, assuming independence |
| Expected per $1 | +$0.08 | +$0.07929 net profit | Correct. Expected **total** return is $1.07929 including stake |

The engine multiplies each leg’s price plus its estimated fee, yielding an all-in cost of **$0.735159**. The payout is the reciprocal of that cost. The model chance divided by cost, less one, gives expected profit. The collapsed slip now labels the payout **estimated**. Kalshi prices a real combo through a live request for quote, so a user entering their actual all-in price could get a materially different answer. [Kalshi Help Center](https://help.kalshi.com/en/articles/13823820-combos?utm_source=chatgpt.com)

I replaced Proctor with **Thunder moneyline**, putting two legs in the same game. The app correctly removed the chance and EV. It still showed **1.38×** and **73% needed** from multiplied leg prices. Those numbers deserve the same caution when the price of the correlated combo is unknown. This test also exposed a stale error message describing a **3–5 leg** Hammer, while the eligible-slip message correctly says **2–5**.

**Friday’s corrected figures now reconcile.** The public rows give **29/32** for 70+ picks, **+10.8987%** on the 31 priced picks at equal $1 stakes, and **72/108** across published decisions. The recap now says **96 priced legs**, with Brier scores of **0.192 for BD and 0.190 for Kalshi**. The beta result is labeled **Top 15, 11–4**. The season headline of **+0.2%** rounds correctly from **+0.1725%** across 375 priced 70+ picks. Friday’s five winning Hammer legs are described on Proof as an estimated **2.04× before fees**. [Friday Proof](https://bettordays.xyz/record) · [Public result rows](https://github.com/1gl2c/bettordays-hq/blob/main/record.json)

## Research Lab, Past nights and Method

| Page | What works | What still needs attention |
|---|---|---|
| **Research Lab** | I opened the full grade sheet, Beta Test Mode, Perfect Parlays, category hit rates, grade bands, both nightly views, sport and line types, parlay clues, and the linked Record Explorer. Beta labels the simulation as experimental. Perfect Parlays explicitly says the Nov 20 rebuild was never posted. | The category table puts **9/9 receptions** first, without the small-sample label shown on **6/6 totals**. Parlay Clues calls **PRA at 22/28, or 78.6%**, the weakest main basketball stat, while the category table shows **rebounds at 56/77, or 72.7%**. The removed Kevin Durant row still shows a dash for its result even though Proof says he scored 16 and missed. [Research Lab](https://bettordays.xyz/research) |
| **Past nights** | The archive preserves contemporary explanations, losing tickets and unresolved results. That is valuable evidence of what BettorDays believed at the time. | The page opens with a Nov 19 AI review, then a Nov 11 recap, then the Nov 19 board. Expanding **“Show 14 older nights”** made the document **40,578 px tall**. More importantly, the Nov 13 archive headline says **42/58** at 70+, while Research and the public rows say **41/57**. Keep the original entry and attach a dated correction identifying the affected pick. [Past nights](https://bettordays.xyz/history) |
| **Method** | The current panel explains the 1.50× Hammer and 1.35× fallback. Its worked example now correctly explains why a ticket winning roughly 47% at 1.6–1.8× loses money. It also identifies the early 211-leg study as historical. | Farther down, the page still calls old guidance **“current rules,”** describes building 14–16-leg lottos, and displays a rule limiting Kalshi lottos to 6–8 legs. Proof says lottos were retired at **0/22**. Its example also switches from **1.0 🍪** to **$131** without giving a dollar conversion alongside the calculation. Use one stake unit and put retired rules behind a version selector. [Method](https://bettordays.xyz/method) |

Two details matter to a serious bettor. First, the archive calls a three-leg ticket made of **74–82% legs** “about a 60% shot.” Even three independent 82% legs reach only **55.1%**. A different probability model might justify 60%, but the archive needs to identify it. Second, Research links to an explorer labeled **1,219 graded legs**. The explorer describes **1,303 records**, including eight pushes, and displays **1,295 decisions**. The site identifies the smaller sample as capper picks elsewhere. Carry that definition onto the link so readers can reconcile the totals.

## What the three Python files establish

**Ticket rules.** The current engine requires **at least +2% estimated EV**. Hammer searches 2–5 distinct-game, distinct-player legs, requires **1.50× payout** and at least **45%** modeled chance. If that fails, Safe Hammer searches 2–4 legs, requires **1.35×** and at least **60%** chance. The search considers only the **first 14 eligible candidates**, so its pass message can overstate what was searched. Also, the forward shutdown watches a cohort of **singles**. Its equal-dollar staking calculation is now correct, but that cohort cannot tell users what the actual published Hammer **tickets** returned. [Ticket engine](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/v7/v7lib.py#L106) · [Forward tracker](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/calib.py)

**Calibration.** I replayed the price-only favorite model used by the slip, refitting on earlier nights before scoring the next night. Lower Brier is better.

| Historical replay | Legs | Raw market | Favorite model |
|---|---:|---:|---:|
| All priced walk-forward observations | 797 | **0.19446** | 0.19484 |
| 80–92¢ favorites, grade ≥75, grade less than 8 points above market | 126 | 0.08507 | **0.08045** |

That second row is the most promising result in this audit. It gives you a specific hypothesis worth tracking. The favorite filter was chosen after studying this history, the 126 observations are singles, and the saved tracker had **zero legs since its Nov 21 start**. Freeze the rule now, publish both benchmarks daily, and score the tickets separately. The existing published Brier report evaluates the raw grade, calibrated grade and blend, but omits this price-only curve that actually drives the slip. [Calibration code](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/calib.py) · [Published scores and weights](https://github.com/1gl2c/bettordays-hq/blob/main/calib.json)

**Sportsbook fair chance.** `book_ev.py` takes a supplied no-vig main line and infers alternate-rung probabilities using Poisson distributions for threes, rebounds and assists, and a normal approximation for points. It prefers the line with the most books. The matching function checks normalized player name and market, leaving event identity and quote freshness to the caller. Show the source line, book count, timestamp and distance to the requested rung. Whole-number lines also need explicit push treatment. The Hammer path reviewed here uses the favorite curve, so sportsbook-derived probabilities should have their own label. [Sportsbook rung model](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/book_ev.py#L45)

## Legal exposure and the business opportunity

- **Verify data rights before scaling distribution.** Kalshi’s standard developer agreement limits API collection and sharing and calls for prior written authorization to share covered data. Check the agreement that applies to your feed against three actual uses: public Board prices, archived repository data, and social cards. A separate license could cover them. I did not inspect your contracts. [kalshi-public-docs.s3.amazonaws.com](https://kalshi-public-docs.s3.amazonaws.com/Kalshi-Developer-Agreement.pdf?utm_source=chatgpt.com)
- **Keep promotional claims as precise as Proof.** “29 of 32 published 70+ picks won Friday” is reproducible. “One of the sharpest,” a guaranteed edge, or a claim about what customers earned requires evidence specific to that claim. The site-wide ticker still compresses the result to “Hammer hit 2.04x,” dropping Proof’s before-fee qualification. Put the qualification on anything people can screenshot or share. The FTC requires a reasonable basis for objective advertising claims before publication. [Federal Trade Commission](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation?utm_source=chatgpt.com)
- **Update the California venue link.** The Offers page uses Gambling.com and FOX Sports for state status. The November 4 preliminary injunction concerning Kalshi sports contracts on the lands of **Blue Lake Rancheria and Chicken Ranch Rancheria** is more specific than the page’s general litigation warning. Scope it to those lands and link the governing source. If BettorDays moves into paid personalized contract advice or transaction-linked compensation, have counsel review that business model before launch. [cdn.ca9.uscourts.gov](https://cdn.ca9.uscourts.gov/datastore/opinions/2026/09/16/25-7504.pdf?utm_source=chatgpt.com)

**What I’d market today:** “Build a slip, see the price it needs, then check every pick after the game.” Friday gives you an unusually good example: all five Hammer legs won, and your own pregame grades still said the price was poor. Showing both facts on one shareable card teaches people what BettorDays does. I’d measure how many first-time visitors come back to check settlement before optimizing the founders signup.

The first ten rows are my ranked product priorities. Effort is estimated person-days and excludes external legal review or licensing turnaround.

```text
BD_AUDIT_START
rank,area,change,why_it_matters,effort_days
1,Published tickets,Freeze each pregame forecast and issue a permanent settlement receipt,Users can verify what was known before a win or loss,4
2,Model validation,Publish daily forward scores for the deployed favorite curve and actual tickets,The adjustment supplies the entire positive edge on the tested slip,3
3,Combo pricing,Accept an actual all-in combo quote and recalculate payout and EV,The exchange quote can change whether a ticket clears break-even,2
4,Archive integrity,Generate corrected totals from row IDs and link each historical revision,The Nov 13 archive says 42/58 while the public rows say 41/57,3
5,Navigation,Use one responsive header and Me menu across core pages Grader Offers and Legal,Desktop users lose destinations when they change pages,3
6,Past nights,Replace the expanded archive with a newest-first date picker and one page per night,Opening older nights currently creates a 40578-pixel page,3
7,Method,Separate active rules from dated retired versions and use one stake unit,Readers encounter conflicting lotto instructions and ambiguous dollar examples,2
8,Research evidence,Generate category claims and sample warnings from their underlying rows,The weakest-stat claim conflicts with the category table,2
9,Data licensing,Verify rights for public display archived prices and social redistribution,The research and acquisition channels depend on those permissions,2
10,Slip language,Show model-estimated chance and expected net profit per dollar with the model date,Visitors can distinguish a forecast from a payout or a verified return,1
11,Correlated slips,Require a combo quote before showing actionable same-game break-even,The current warning hides EV but still shows synthetic price-based metrics,1
12,Rule consistency,Generate success failure and pass messages from the active ticket configuration,A same-game failure still describes the obsolete three-leg minimum,1.5
13,Research settlements,Populate removed-leg outcomes from the same settlement feed as Proof,Durant is graded in Proof while the lab result is blank,1.5
14,Record Explorer,Name each sample and show a count of inclusions pushes and exclusions,Readers can reconcile 1219 capper picks with 1295 explorer decisions,1.5
15,Sportsbook rungs,Verify event and timestamp and display source line book count and push treatment,An inferred alternate-line probability needs a traceable input,3
16,Eligibility,Use dated regulator and court sources adjacent to venue links,California availability can depend on the specific territory,2
17,Social sharing,Generate cards from the original ticket receipt with fee label and full-night link,Shared wins and losses retain the evidence visible on Proof,2
18,Grader,Offer a worked guest example with one weak leg and its required price,Visitors can judge the result before creating an account,2
19,Settled Board,Replace closed-ticket lock instructions with a dated recap and next-board status,The current action copy addresses a price users can no longer obtain,0.5
20,Founders offer,Publish the price and eligibility terms or offer a launch notification,Visitors can tell exactly what joining the list secures,0.5
BD_AUDIT_END
```