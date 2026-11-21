# BettorDays audit · November 20, 2026

**Ace, fix the Hammer before you buy another AI model.** On the live phone homepage, the biggest green number was **2.04x**, followed by **“About 44% by our grades”** and a **Copy the Hammer** button. Taking 2.04x as the total payout, the ticket needs to win **49.0%** of the time to break even before fees. At your own 44% estimate, a $1 ticket returns about **$0.90 on average**, a **10.2% expected loss** before fees. The page tells visitors to lock that price. Your own numbers say to pass. [Tonight](https://bettordays.xyz/)

**I’d make the Parlay Grader the front door.** “Paste your ticket and see which leg is costing you the most” gives someone a reason to use BettorDays even on a night when your model finds zero attractive prices. Keep the public record one tap away. That gives you something valuable to sell while you test whether the picks can beat the market.

I tested the public site in a **390 × 844** browser, including the Master filter, a two-leg ticket, all nine Research views, all eight agent-simulation filters, the Grader, California bonuses, Results, Record, History, Method, Founders and the signed-out member entry. I used two public example legs in the Grader and reached the account requirement. The signed-in grading result, screenshot accuracy, referral reward delivery and production AI costs remain unverified. The records below are site-reported unless I identify my own calculation.

## Team discussion

### 1. Senior full-stack and AI developer

**The highest-return engineering work is a check that the numbers and copy agree.** Three issues are visible without access to the code.

| Live screen | What I found | What to change |
|---|---|---|
| Results | The Nov 16 recap pairs **36/55 with 73%**, **16/22 with 82%**, and **7/20 with 40%**. Those fractions round to **65%, 73% and 35%**. | Generate every fraction, percentage and caption from the same settled rows. Block publication when they disagree. [Results](https://bettordays.xyz/results) |
| Research → Tonight’s full grade sheet | Tapping the card changed the URL. Opening the deep link directly also showed the Research menu and footer. I could not get the promised grade table to appear. The other eight views displayed their distinct content. | Give the sheet its own working route. Test direct entry, tapping the card and returning to Research. Display an explicit unavailable state if the data fails. [Grade sheet](https://bettordays.xyz/research#rs-v7) |
| Picks and Method | The Oregon card in your capture says “capped under 70” and displays **87**. The live DeRozan note mentions a price near **72** and displays **86**. Both could reflect different stages, but the reader has no timestamp or label to explain them. | Store system grade, published grade, selection-time price, current price and timestamps separately. Render the explanation from those fields. Print the models that actually ran on that leg. [Tonight](https://bettordays.xyz/) |

**For the $1/day target, buy the facts once per game.** Build a shared packet with player and opponent IDs, home/away, start time, minutes, season and recent game logs, injury status with source and timestamp, rest, and exact line and settlement rules. Use a permitted stats feed or existing licensed data. Cache the packet for all legs in that game. Keep executable prices and closing prices in a separate table so a “blind” grade can actually be reproduced.

| Job | Starting assignment | How it earns its cost |
|---|---|---|
| News and injuries | Ingest a timestamped source once. Use a low-cost text model to extract the player, status and effective time. Escalate conflicting reports to the founder. | Measure missed status changes and erroneous player matches. |
| Matchups and base probability | Use code for minutes, opportunity, opponent adjustments and uncertainty. Keep Claude as the incumbent for explaining the result from the packet. | Score the code-only and Claude-assisted forecasts independently. |
| Second opinion | Run one low-cost OpenAI or Gemini challenger on a preselected random sample, plus flagged cases. Score the random sample separately. | Promote a model only if it improves held-out accuracy enough to justify cost. |
| Simulation | Run seeded simulations in code from the same minutes and usage assumptions. Simulate teammates together when evaluating same-game tickets. | Re-running the same dated inputs should reproduce the output. Four agents repeating a weak assumption can agree and still be wrong. |
| Slip reading | Parse pasted text first. Use one low-cost vision model for images, show the extracted lines for correction, then look up existing grades. | Compare exact player, side and threshold accuracy on the same labeled screenshots. Measure cost per **successfully matched** slip. |

**Weight forecasts by predicting future nights better.** Start with the code baseline, Claude alone, and a simple average as three competing forecasts. Freeze each before tip. Each week, fit nonnegative model weights that sum to one using earlier nights only, with weights pulled toward equal weighting when evidence is thin. Score the following week on the **same legs** using Brier score, calibration and cost. Also score the market at the same timestamp. Compare uncertainty by game or night because ten props from one game share information. A blend earns production only when it beats the best single model on held-out slates. Until then, Claude-only is a reasonable cost decision. Your reported $9 versus $1 per day is about **$240 per 30-day month** of difference.

**The daily job can run with one founder review.** Ingest authorized picks → match players and markets → refresh game packets → grade → attach executable quotes → run arithmetic, freshness and eligibility checks → freeze the release → publish → settle from box scores → regenerate Record and recap. Give each slate, leg and revision a stable ID so retries cannot create duplicate picks or wins. Put unmatched lines, injury conflicts, stale quotes, late games and settlement disputes in one review queue. A missed deadline should produce a dated “no release” state rather than yesterday’s recommendations.

### 2. Gaming-law and trust review

**The first compliance decision is whether you want to remain an independent research publisher or also market wagers for operators.** The distinction matters to the product itself. Massachusetts prohibits an operator from paying a third party a percentage of wagering revenue from referred users. Its rules also restrict covered vendors and marketing entities from encouraging specific wagers. Your Bonuses screen tells visitors to use credits on GREEN legs. Before accepting compensation, have gaming counsel review the actual compensation, state, operator and adjacent pick content. The Massachusetts regulator also has a vendor licensing and registration process. [mass.gov](https://www.mass.gov/doc/205-cmr-256-sports-wagering-advertising/download?utm_source=chatgpt.com)

| Screen | Change I would make |
|---|---|
| Bonuses | The live headline already says **“Sign-up offers where you live.”** Keep that improvement. Selecting California correctly produced a sportsbook warning, then an **Open Kalshi** link with a general availability caveat. Show separately verified sportsbook and event-contract status, the official source, scope and checked date. Hide promotional links where availability is unresolved. California litigation has specifically addressed sports-event contracts on tribal lands. [Bonuses](https://bettordays.xyz/bonuses) [cdn.ca9.uscourts.gov](https://cdn.ca9.uscourts.gov/datastore/opinions/2026/09/16/25-7504.pdf?utm_source=chatgpt.com) |
| Age and responsible gambling | The signup checkbox says **21+** while Bonuses introduces an **18+** exception. Keep BettorDays’ own audience rule consistent. Remove “Biggest share” from the Hammer and offer alert opt-outs. Your Terms identifies 1-800-GAMBLER as the national helpline. NCPG now identifies **1-800-MY-RESET** as its national number. Check required state wording separately. [Terms](https://bettordays.xyz/legal) [National Council on Problem Gambling](https://www.ncpgambling.org/help-treatment/about-the-national-problem-gambling-helpline/?utm_source=chatgpt.com) |
| Grader privacy | Terms lists founders, accounts and feedback. It omits slip images and pasted legs, while the Grader advertises AI analysis. State what is transmitted, to whom, how long it is retained and how deletion works. Prompt users to crop names, balances, barcodes and ticket IDs. Verify the actual data flow before publishing the promise. [Grader](https://bettordays.xyz/grade) · [Terms](https://bettordays.xyz/legal) |
| Claims and referrals | Publish the cohort, dates, price source, sample and fee treatment alongside performance claims. If an operator or creator pays you, disclose the relationship beside the recommendation and link. Apply that standard to social posts too. The FTC expects substantiation for objective advertising claims and clear disclosure of material connections. [Federal Trade Commission](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation?utm_source=chatgpt.com) |

### 3. Business consultant

**Sell a decision someone already needs to make.** A regular bettor already has a slip and wants to know, “Which leg makes this a bad deal?” A sharp bettor considering **$30 a month** wants to know, “Can this save me enough research time, and can I independently verify every number?” Those are two versions of the same product.

| Free | $30/month founding pilot |
|---|---|
| First pasted-slip check, extracted legs, weakest leg with reason, public record, previous night’s recap | Saved watchlists, price-change and injury alerts, timestamped line history, CSV export, saved slips and a stated screenshot allowance |
| Show a sample result before signup. Let the user keep the draft when joining. | Ask ten frequent users to pay for one month. Track who renews, which feature they use and what they would miss. |

**The grader is worth the AI cost if it creates repeat use.** Give the first anonymous text slip a board-lookup result. Meter image uploads and cache repeat matches. Track successful grades, cost per successful grade, seven-day return and paid conversion by input type. For illustration, 10,000 image grades at **$0.02** cost **$200**. At **$0.10**, they cost **$1,000**. Measure a real batch before promising unlimited access.

**The first $10,000/month requires more than 1,000 casual users.** At $30, **334 subscribers produce $10,020 gross monthly revenue** before fees, refunds and inference. That requires 33.4% conversion from 1,000 active users. At a hypothetical 5% conversion, it takes about **6,680 active users**. Treat **1,000 weekly active users** and **$10,000 monthly recurring revenue** as separate milestones. With 23 reported accounts, the strongest next proof is ten paid pilots and their first renewals. [Founders](https://bettordays.xyz/founders)

### 4. Professional capper

**The 88% headline describes a historical group. It does not establish that the current Master filter has an edge.** The page associates **124–17** with all priced 70+ legs where Kalshi was at or above the grade. The filter then restricts today’s list to selected markets. Publish the historical count and return for that **exact** rule, disclose when you chose it, and start a separate forward record from that date. The live copy already reports **+6.5%** for GREEN overall and **−10.2%** for the week of Nov 16. Both belong beside the headline. [Tonight](https://bettordays.xyz/) · [Record](https://bettordays.xyz/record)

Four findings should change how you rank picks:

- **Higher grades have stopped separating outcomes.** The 70–79 band went **182/235**, about 77.4%. The 80+ band went **163/213**, about 76.5%. The 85+ band averaged a grade of **88** but hit **74/102**, about 72.5%. Calibrate those scores before displaying them as literal hit probabilities or multiplying them into ticket odds. [Record explorer](https://bettordays.xyz/record)
- **The market is a strong baseline.** Your Method page reports that on 184 comparable legs the market had a better Brier score, **0.210 versus 0.224**. Beta’s own sim went **164/308**, or 53.2%, against a reported average break-even of 57%. That gap is a warning. Compute actual profit line by line using entry price and fees, since an average break-even rate alone cannot determine realized return. [Method](https://bettordays.xyz/method) · [Beta](https://bettordays.xyz/research#rs-beta)
- **GREEN is market agreement.** Trae showed a grade of **87** against a price of **92**. If 92¢ is the executable cost of a $1 payout, your forecast values that contract at 87¢ before fees. Keep agreement as a research signal. Show a separate **price worth taking**, and allow the answer to be **pass**. [Tonight](https://bettordays.xyz/)
- **The teaching example repeats the Hammer problem.** Method says a three-leg ticket hits about **46%**, pays around **1.7x** and is close to break-even. The displayed assumptions imply **0.46 × 1.70 − 1 = −21.8%** before fees. Break-even at that probability is about **2.17x**. Correcting this example will teach users exactly why they need the Grader. [Method](https://bettordays.xyz/method)

**What would convince a skeptic:** a downloadable ledger frozen before tip that includes published picks, passes, exact lines, original and revised grades, executable entry quote and time, closing quote, settlement, fees and every correction. Show flat-$1 net return, drawdown and price movement for the same contract. Give prospective tickets and hindsight builds separate records. Explain that **1,195 settled rows include eight pushes, leaving 1,187 wins/losses**, and that older closing-price reconstructions and later grading-time quotes answer different questions. Your existing Record page already contains much of that explanation. [Record explorer](https://bettordays.xyz/record)

### 5. Social media marketer

**Start with the 23 members and the cappers whose audiences already trust them.** Ask each member to bring one real research question. Watch ten of them try the Grader on a phone. Ask five cappers for permission to grade their entire published slate, including losses, and give each a shareable prior-night scorecard. The creator gets an attributable record. BettorDays gets qualified visitors arriving with a specific reason to use it.

**Cheapest reliable capper intake:** an opt-in form or dedicated email with player, line, side, game, source link and permission to display. That can add **$0 in software cost** using tools you already have. Accept a creator-owned RSS feed or webhook where available. X notifications are a low-cost manual fallback. For creators who only post on X, use the official API, keep the last processed post ID, deduplicate and queue ambiguous screenshots for review. X’s published self-serve model is pay-per-use at **$0.005 per post read**. At 100 billable post reads/day, that is about **$15 per 30 days** before other resources. Enterprise is the higher-volume option. X restricts redistribution, so preserve attribution and check your intended display and export rights. [X](https://docs.x.com/x-api/getting-started/pricing?utm_source=chatgpt.com)

**Grok can search X**, including searches scoped to handles, but a search result does not guarantee a complete daily feed. xAI lists **$5 per 1,000 posts fetched** and **$10 per 1,000 profiles fetched**, plus tokens. Use it to investigate a missing post or context. Pay the direct feed when completeness is the requirement. [SpaceXSI Docs](https://docs.x.ai/developers/tools/x-search?utm_source=chatgpt.com)

**The growth loop:** publish the timestamped pregame card on X, then reply to that same post with the next-day result and original price. Use Instagram carousels for one worked slip and short video for one price lesson. Give each creator a tagged Grader link. Define a weekly active user as someone who completes a grade, saves a watchlist item or inspects a result within seven days. Track visits → completed checks → seven-day returns by creator. Reward referrals with an extra research feature after the invited user completes a check. Keep rewards independent of deposits, losses and wagering volume. Check platform rules before buying distribution, particularly TikTok’s restrictions on gambling-related advertising. [TikTok Advertising Policies](https://ads.tiktok.com/resources/help/article/tiktok-ads-policy-gambling-and-games?lang=en\&utm_source=chatgpt.com)

### 6. Product designer

**Keep the live navigation.** Your prompt’s older capture had Picks, Build, Post, Research and More. The live phone now has **Tonight, Ticket, Grade, Record and More**. That already puts the three core actions within thumb reach. The bigger problem is what happens after the tap.

| Path I tested | Live finding | Decision |
|---|---|---|
| Tonight → Master | Off showed **32 of 32**. Master reported **15**. On the first screen, five Hammer legs occupy almost the entire viewport, with **2.04x** much more prominent than **44%**. | Lead with slate status, playable opportunities and “Grade my slip.” Give break-even and estimated probability equal visual weight. Collapse the filter bank. [Tonight](https://bettordays.xyz/) |
| Ticket → two legs | After the slate started, I selected two legs marked **STARTED** and got **1.26x**, **ours 77%**, two warnings and an enabled Copy button. Switching to “Not started yet” retained both selected started legs. | Preserve them as an archived draft, label the prices as pregame and disable the actionable copy state. At night, show “Tonight’s pregame board is closed.” [Ticket](https://bettordays.xyz/easy) |
| Grade → Grade it | I pasted the two example legs. Only after submitting did I learn that grading requires an account. The sign-in instruction said to come back afterward. | Show the requirement before input, or give one immediate cached result. Return a signed-in user to the same slip. [Grader](https://bettordays.xyz/grade) |
| Research → Beta | All eight filter controls worked. The filters showed **1 ChatGPT pick, 22 Gemini, 9 Grok, 56 Claude** and **5 Master**. The hub advertises **187 lines** while the agent table says **105**. | Label each universe and explain the difference. Identify a one-model result explicitly when the “consensus” filter can pass with one agent. [Beta](https://bettordays.xyz/research#rs-beta) |
| History, Results and Record | History was about **17,370 px** collapsed. “Show 14 older nights” expanded it to **228,844 px**, about **271 phone screens**. Results opened on Nov 16. Record’s NBA filter correctly returned **491–250 across 741 legs**. | Make Record the canonical destination. Put a date picker there, open the latest settled night and fetch one date at a time. [History](https://bettordays.xyz/history) · [Results](https://bettordays.xyz/results) · [Record](https://bettordays.xyz/record) |
| Founders and members | Founders fits in roughly one phone screen. `/app` signed out redirects to a join dialog on the home board. Its “free preview is up” copy is confusing when someone arrived by choosing to join. | Make the two promises explicit. “Join free to save this slip” belongs to members. “Try research alerts for $30/month” belongs to a priced pilot. [Founders](https://bettordays.xyz/founders) · [Members](https://bettordays.xyz/app) |

**Speed:** In this browser session, Research route checks took roughly **0.2–0.8 seconds** to reach the hub/back-link state. The grade-sheet route also reached that state while showing no sheet. Measure **time to usable result** on real phones, including first visit over cellular. A route loading quickly tells you little if the user still cannot finish the job.

**The first 30 seconds I’d design:** At **0–5 seconds**, show “Tonight’s board is open/closed,” the last update and two actions, **Check my slip** and **See available lines**. At **5–15 seconds**, a visitor pastes two legs or taps two upcoming legs. At **15–25 seconds**, show the offered payout, required win rate, estimated win rate, weakest leg and any same-game dependence. At **25–30 seconds**, let them save, copy a playable ticket or pass. When the result is unfavorable, **“Pass at this price” is a successful session**. Test that with ten first-time users before adding another feature.

## Ranked audit

Effort estimates are working days for one developer with the existing app and data. Legal review and time spent gathering prospective results are additional.

```text
BD_AUDIT_START
rank,area,change,why_it_matters,effort_days
1,grading,Gate Hammer promotion on fee-adjusted break-even,The featured 2.04x ticket loses money at the displayed 44% estimate,1
2,trust,Generate all recap math and teaching examples from tested formulas,The public Results and Method pages display materially wrong percentages,1
3,ux,Close pregame actions when games start,The builder lets visitors copy started legs at old prices,1
4,trust,Freeze a downloadable timestamped pick and ticket ledger,Visitors can reproduce the original recommendation and every revision,3
5,grading,Separate market agreement from playable price,GREEN can describe a price above the modeled value,2
6,ux,Give first-time visitors a cached slip check and preserve their draft,The current signup interruption comes after the visitor enters the legs,2
7,compliance,Review bonus links and state rules before monetizing,Operator compensation can change which promotions are permitted,2
8,compliance,Disclose slip processing and update help resources,The current privacy page omits uploaded slips and mislabels the national number,1
9,data,Store exact entry quotes and closing quotes separately,Historical closing prices cannot establish an available entry price,3
10,grading,Calibrate grade bands on later slates,The observed 80+ band underperformed the 70 to 79 band,3
11,trust,Publish a prospective record for the exact Master rule,The quoted GREEN cohort differs from the narrower displayed filter,2
12,ux,Restore the full grade sheet and test its deep link,The live Research route displayed the hub and footer without a sheet,1
13,ops,Automate slate publication and settlement with an exception queue,A solo founder can review discrepancies without rebuilding the board daily,4
14,data,Cache one rights-cleared fact packet per game,Every grader can use identical timely inputs at lower cost,3
15,grading,Shadow-test one challenger against Claude and the market,Another paid model should earn its place on unseen games,2
16,ux,Unify results and paginate the archive by night,Expanding fourteen older nights produced over 228000 pixels of content,2
17,growth,Onboard five consenting cappers with attributed scorecards,Creator distribution and structured intake can grow together,2
18,ops,Measure activation and cost per successful slip,Upload volume alone cannot justify inference spending,1
19,money,Recruit ten paying research-tool pilots,Renewals test willingness to pay for a repeatable workflow,2
20,growth,Reward referrals after a completed research action,This measures activated users without paying for deposits or wagering,2
BD_AUDIT_END
```

```text
BD_VERDICT_START
idea,verdict,one_line_reason
parlay grader,Lead with it,Pasted slips can deliver a useful first result cheaply and reveal repeat demand
bonus finder,Keep informational,Verify each jurisdiction and commercial arrangement before earning referral fees
referral program,Test after activation,Reward a completed research action and measure seven-day return
paid tier,Pilot at $30,Sell alerts and history and exports to ten users and measure renewals
multi-model blend,Shadow-test,Promote a blend only after it beats the best single forecast on future slates
X capper automation,Use opt-in first,Direct submissions are cheapest and the official API covers X-only sources
BD_VERDICT_END
```

```text
BD_NAV_START
tab_order,tab_name,what_it_holds
1,Tonight,Slate status and upcoming priced lines and the latest settled recap
2,Ticket,Selected legs and correlation warnings and break-even math
3,Grade,Paste or upload a slip and inspect the weakest leg
4,Record,Timestamped ledger and after-fee returns and date-based history
5,More,Research Lab and methodology and account and offers and help
BD_NAV_END
```