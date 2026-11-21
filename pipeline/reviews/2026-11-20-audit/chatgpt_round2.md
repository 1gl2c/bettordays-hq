**The first thing I’d fix is the slip. At iPhone width, the four numbers that make BettorDays useful are clipped off the right side of the screen.** The second fix is the public record. Proof says a flat $1 on each priced 70+ pick returned **+0.8%**. Replaying the 375 public picks gives **+0.17%**. I could reproduce +0.8% only by buying one contract per pick, which puts a different amount of money on each outcome.

I tested the live site signed out at **390 × 844 CSS pixels**, tapped all four bottom controls from **20 public pages and research views**, opened every item in Me, tested the guest Grader, and read Friday’s recap. I also read all three requested Python files and replayed the public results. This was an iPhone-size browser test. Signed-in screens, actual exchange fills, and physical iPhone Safari remain unverified.

## What happened on the phone

| Surface | What I found |
|---|---|
| **Board slip** | With three legs selected, the expanded numbers started at **x=346** and extended to **x=632** on a **390 px** screen. The panel clipped them. The page had no horizontal scroll to recover them. The screenshot below shows what a visitor actually sees. |
| **Bottom tabs** | Board, Grader and Proof reached their destinations, and Me opened, from all 20 tested origins. The order and sizing were consistent across the main screens, approximately **95 × 58 px per control**. Board, Grader and Proof highlighted correctly on their landing pages. Full Board and the other secondary pages had no active tab. The active controls also lacked `aria-current`. |
| **Me** | The menus differ. Board offers **Tour** and **Add to Home Screen**. Grader and Sign-up Offers substitute **Terms and privacy** and route **Talk to Ace** through Board. Feedback opened, all five tour steps worked, and installation instructions opened. |
| **Menu destinations** | Full Board, Research Lab, Past Nights, Older Recaps, How It Works, Sign-up Offers, Founders and Terms opened. **Profile and invites, Pick & post, Leaderboard, Feed and Chat** all sent a guest to the same signup dialog on Board. “Keep browsing” left me on Board. None of those five labels warned me an account was required. |
| **Continuity** | **Board → Proof → Board** kept my three legs. **Board → Grader → Board** erased all three. This is especially frustrating because Grader is the natural next stop after building a slip. |
| **Grader and onboarding** | Grader accepted three pasted legs and explained its free-account requirement on submission. I could verify the guest flow only. On Board, a signup dialog appeared on entry and a separate feedback dialog interrupted the first slip test. Both asked for something before I could read my result. |







## Does the three-leg math work?

I selected **Trae Young 10+ points** at 92¢, **Tyrese Proctor 1+ threes** at 85¢, and **Isaiah Hartenstein 2+ assists** at 92¢. They were in three different games. Friday had settled, and the app correctly disabled copying the pregame slip.

| Metric | Board showed | Independent calculation | Finding |
|---|---:|---:|---|
| Payout after fees | 1.36× | 1.36025× | Matches the app’s estimated price |
| Win rate needed | 74% | 73.5159% | Correct rounding |
| “Our true chance” | 79% | 79.345% | Matches the fitted favorite model under independence |
| Expected per $1 | +$0.08 | +$0.0793 net profit | Correct rounding. Expected total returned is $1.0793 including stake |

**The arithmetic works. The uncertainty is in the price and the probability.** The engine multiplies three fee-adjusted leg prices to estimate a 73.516¢ ticket cost. Kalshi gives each combo its own order book and live request-for-quote price. Fees can also depend on the market and execution. The app does acknowledge the estimate inside Details. Put **“Estimated payout”** on the collapsed slip and offer a field for the user’s actual all-in quote. [Kalshi Help Center](https://help.kalshi.com/en/articles/13823820-combos?utm_source=chatgpt.com)

The distinction changes the decision. The three raw grades multiply to **62.86%**, the three market prices multiply to **71.94%**, and the favorite model raises that to **79.35%**. At this payout, the market product implies about **−2.1¢ per $1** and the favorite model implies **+7.9¢**. The adjustment supplies the entire positive edge.

I also tried **Hartenstein assists + Thunder moneyline + Trae points**. The first two share a game. The slip still displayed **78% chance and +8% EV** while its own warning explained that multiplying those probabilities was inappropriate. Suppress those two numbers whenever the app lacks a joint model for the selected legs.

## What the code and Friday’s Proof establish

| Area | Finding |
|---|---|
| **Hammer rules** | The code enforces estimated EV **≥ +2%** for both tickets. Hammer requires **2–5 legs, ≥1.50× payout, ≥45% modeled hit chance**. Its fallback Safe Hammer requires **2–4 legs, ≥1.35×, ≥60%**. Both require distinct games and players. The slip still describes **3–5 legs**, and Method describes an older **2×** rule. The search also considers only the first 14 eligible legs, so a pass does not establish that the whole slate lacked a qualifying ticket. [Ticket engine](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/v7/v7lib.py#L106) |
| **Calibration and Brier** | The saved walk-forward report covers **797 priced legs** from Nov 8–20. Lower is better. Raw BD grades scored **0.2126**, the calibrated grade **0.2127**, the blend **0.1955**, and Kalshi **0.1945**. The report omits the price-only favorite curve actually used by the slip. I refit that curve on prior nights and scored the same 797 later observations. It scored **0.19484** against the market’s **0.19446**. That small difference does not establish a winner. It gives you no basis yet to advertise the adjustment as more accurate. The saved forward tracker contained **zero legs**. [Calibration code](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/calib.py#L119) · [Published weights and scores](https://github.com/1gl2c/bettordays-hq/blob/main/calib.json) |
| **Historical replay** | The settled Friday builder uses weights fitted **through Friday**, including that night’s outcomes. Fitting through Thursday gives **78.91%** for my ticket, versus **79.35%** on the recap build. Both display as 79%, but a historical receipt should preserve exactly what a visitor could know before tip. |
| **Sportsbook fair chance** | `book_ev.py` takes a supplied no-vig main line and estimates alternate rungs using a Poisson distribution for assists, rebounds and threes, and a normal approximation for points. That is a **model-derived alternate-line probability**. The function matches on normalized player name and market without checking game or quote time itself, so callers must supply properly scoped rows. A whole-number book line can also push and needs separate handling if the supplied fair probability is conditional on no push. The Hammer path I reviewed uses the favorite curve, not this sportsbook estimate. [Sportsbook rung model](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/book_ev.py#L45) |
| **Flat-stake ROI** | The 70+ record **374/480** checks out. Of those picks, **375** had prices. Equal $1 stakes produce **+0.1725%**. One contract per pick produces **+0.7503%**, displayed as +0.8%. Friday’s own headline similarly says **+11.1%** where equal stakes produce **+10.90%** across 31 priced picks. The GREEN subgroup’s **+6.9%** does reproduce under equal stakes. The same staking mismatch appears in the forward pass-mode code, where it can affect whether the engine keeps publishing. [Public results](https://github.com/1gl2c/bettordays-hq/blob/main/record.json) · [Forward ROI calculation](https://github.com/1gl2c/bettordays-hq/blob/main/pipeline/calib.py#L130) |

**Friday’s recap is worth keeping.** It names all three 70+ losses, shows Thursday’s bad night immediately below Friday’s good one, and admits the winning five-leg Hammer had negative estimated value before the game. I reproduced **29/32** and all three named losses. The advertised **2.04×** matches the product of the five fee-free prices. Applying the builder’s fee approximation gives **1.95×**. Without a fill receipt, “estimated 2.04× before fees” is more defensible than “paid about 2.04×.” [Friday Proof](https://bettordays.xyz/record)

Two other figures need a receipt. Friday says **72/109 overall** and **0.192 vs 0.192 on 97 priced legs**. The public Friday rows I could replay contain **72 wins from 108 decisions** and **96 priced decisions**, scoring **0.1916 for BD vs 0.1900 for Kalshi**. A missing or differently classified row could explain the discrepancy. Likewise, Friday’s “Beta Top 8” says **11–4**, while Research describes a **Top 15**. A reader should be able to tap either headline and see exactly which rows it counts.

## Legal and business exposure

- **Market-data rights are the first legal check.** The Board displays exchange prices, the public repository archives them, and share cards would distribute them again. Kalshi’s public developer agreement restricts API data collection and third-party sharing without written authorization. Verify the actual feed agreement covers public display, archives and social distribution. I did not inspect a signed agreement. [kalshi-public-docs.s3.amazonaws.com](https://kalshi-public-docs.s3.amazonaws.com/Kalshi-Developer-Agreement.pdf?utm_source=chatgpt.com)
- **Performance claims need evidence that matches the wording.** “One of the sharpest,” “our true chance,” and promoting a simulated payout as money a bettor received create avoidable exposure. The FTC requires a reasonable basis for objective advertising claims before publication. The Offers page says sportsbooks do not pay for those links. If a referral or creator arrangement changes, disclose the relationship beside the endorsement. [Federal Trade Commission](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation?utm_source=chatgpt.com)
- **The California Offers page needs primary sources.** It distinguishes sportsbooks from prediction markets, acknowledges litigation, and dates its check. Its cited authorities are Gambling.com and FOX Sports. Use regulator and court sources for eligibility, especially beside a venue link. California’s attorney general was still contesting these issues in November, and the Ninth Circuit’s September preliminary-injunction ruling specifically addressed tribal lands. Before charging for personalized contract recommendations or accepting transaction-linked compensation, have gaming and derivatives counsel review the proposed activity. [Office of the Attorney General](https://www.oag.ca.gov/news/press-releases/attorney-general-bonta-defends-state-gambling-laws-against-kalshi-again?utm_source=chatgpt.com)
- **Make the privacy promise match the form.** Signup asks for an optional phone number and preselects marketing email. The privacy page’s account-data list omits the phone field. Grader tells users to crop their slips, but the explanation that screenshots go to OpenRouter and a downstream model is on the legal page. Put that disclosure at upload, verify provider retention before promising deletion, and make marketing an affirmative choice. [Grader](https://bettordays.xyz/grade) · [Terms and privacy](https://bettordays.xyz/legal)

**The strongest business offer is something you can already demonstrate: “See what price a pick needs, then come back and check how it settled.”** Give each published pick one shareable link that starts as a timestamped forecast and becomes a receipt, including when it loses. Let a new visitor see one of those receipts before asking them to join. That gives friends a concrete reason to share the app and a concrete reason to return tomorrow.

The first ten rows below are my ranked launch priorities. Effort is estimated person-days and excludes external licensing or counsel turnaround.

```text
BD_AUDIT_START
rank,area,change,why_it_matters,effort_days
1,iPhone slip,Stack slip controls and metrics vertically and test at 375 and 390 px,The core result is clipped offscreen at iPhone width,1
2,Public ROI,Use equal-dollar returns for flat-stake claims and regenerate the historical and forward reports,The advertised season return changes from +0.8% to +0.17%,2
3,Combo pricing,Label synthetic payouts and accept an actual all-in combo quote,Only the quoted ticket price can support an actionable break-even figure,2
4,Probability,Suppress chance and EV for dependent legs until a joint model exists,The current slip shows positive EV while warning its probability formula is invalid,1
5,Model validation,Walk-forward score the deployed favorite curve and publish it beside the market benchmark,The adjustment creates the entire edge on the tested slip,3
6,Historical proof,Freeze inputs and weights before each game and attach a settlement receipt to each ticket,Friday can currently be replayed using information learned on Friday night,4
7,Record integrity,Generate every recap headline from a linked list of settled rows,Readers can resolve the 96 versus 97 priced legs and Top 8 versus 15 results,3
8,Data rights,Verify and document permission for price display archives and redistribution,The public product depends on rights beyond personal API use,2
9,Ticket rules,Generate eligibility copy and pass reasons from the same configuration as the engine,The app currently describes conflicting leg counts and payout floors,2
10,Navigation,Share one tab bar and Me menu and preserve draft slips across routes,Visiting Grader erases selections and changes available menu actions,3
11,Slip language,Show modeled win chance and net profit per dollar beside break-even,Users can distinguish an estimate from a verified edge or a total payout,1
12,Sportsbook model,Verify event identity timestamp push treatment and alternate-rung accuracy,A mismatched main line or poor tail estimate can manufacture value,4
13,Onboarding,Delay signup and feedback until after the first useful result,New visitors can experience the research before two interruptions,1
14,Guest experience,Mark member-only items and return users to their intended screen after signup,Five different menu choices currently lead guests to the same Board dialog,2
15,Privacy,Disclose image processing at upload and align phone and marketing disclosures with signup,Users can make an informed choice before sharing personal data,1.5
16,Offers,Use primary jurisdiction sources and date eligibility and compensation disclosures,The venue link sits next to guidance that can change with court decisions,2
17,Social proof,Publish one timestamped pick link that updates with settlement and the full night,Shared wins and losses become independently checkable,3
18,Grader,Provide a worked guest example showing the weakest leg and the price needed,Visitors can judge the grader before opening an account,2
19,Accessibility,Expose active tabs to screen readers and test focus and tab labels on physical iPhone Safari,The active route is currently conveyed visually on the main screens,2
20,Founders offer,State the founders price and terms or change the promise to a pricing notification,Visitors can understand what joining actually secures,0.5
BD_AUDIT_END
```