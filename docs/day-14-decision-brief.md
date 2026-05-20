# Day 14 Decision Brief — Meta Campaign

**Prepared**: 2026-05-20 (Day 8 of 14)
**Decision date**: 2026-05-26 (campaign auto-ends Tuesday)
**Audience for this doc**: Saged.club team (Diana, Koritsa, anyone weighing in)

---

## TL;DR

We've been running a Meta ad campaign for 8 days. By Day 14 (Tuesday May 26), it stops automatically and we need to decide what's next. Three plausible paths. **Our recommendation is path B — pivot to a DM-driven campaign — but the team should weigh in.**

---

## Where we are after 8 days

**The ads themselves are working unusually well.**

- **CTR**: 4% account-wide (industry average for local ads: ~1.5%)
- **Ukrainian ad**: **8% CTR**, **€0.03 per click** — 5× cheaper than typical
- **Russian ad**: 3% CTR, €0.17 per click — solid but not exceptional
- **€70 spent** so far across 8 days
- **600+ people** clicked through to the website

**But we have zero bookings traceable to the campaign.**

- 0 Stripe checkouts attributable to ad traffic
- 1 real €60 booking happened *during* the campaign — but it came via Telegram DM after Diana shared the link personally, not from someone clicking the ad
- 9 new Instagram followers gained
- Most ad-driven visitors are invisible to our tracking (iPhone Safari blocks Meta's pixel; even with our fixes, we capture maybe 10% of visits)

---

## What we learned (the important stuff)

1. **The creative resonates.** People stop on the ad and click — especially the Ukrainian-speaking audience. The CTR data is unambiguous.
2. **The funnel is broken at the wrong step.** People click → land on the website → leave without booking through Stripe.
3. **Real conversions happen in DM, not checkout.** The one real €60 booking proves the funnel CAN convert — just not the Stripe-checkout part.
4. **The Ukrainian audience is significantly more engaged** than Russian-speaking. 2-3× the click rate, 5× cheaper per click.

---

## Three options for Day 14

### Option A — Extend the current campaign as-is

**What it means**: keep running the same ads, same budget (€3 RU / €7 UA), for another 14 days.

**Cost**: ~€140 over 14 days.

**Pros**:
- The Ukrainian ad is *just* hitting its stride — cutting it now is throwing away momentum
- No new work required from anyone
- Continues building the Instagram following

**Cons**:
- Doesn't fix the conversion problem (people clicking but not booking)
- Same creative for 22 days total will fatigue — clicks will likely drop
- We'd still have ~0 trackable bookings at Day 28

### Option B — Pivot to a "Message us" campaign ⭐ recommended

**What it means**: stop the current ads. Replace with ads that have a "Send Message" button instead of "Visit Website". When someone clicks, it opens a WhatsApp/Instagram DM with us pre-filled.

**Cost**: ~€140 over 14 days (same budget).

**Pros**:
- **Matches how this audience actually converts** — we know real bookings come via DM, not Stripe
- Every click becomes a real conversation, not a website bounce
- Bypasses the entire tracking problem (DMs are visible to us, attribution clean)
- Builds direct relationships, not just impressions
- The Ukrainian audience is primed and engaged — they're ready to talk

**Cons**:
- Higher response burden on Diana/Koritsa — every DM needs a human reply within a few hours
- Requires the IG/Messenger auto-replies to be set up first ([#90](https://github.com/diana0xUX/Saged/issues/90))
- Loses some delivery momentum during the switch (~2 days of re-learning)

### Option C — Both: extend current + add a Message variant

**What it means**: Keep the Ukrainian ad running at lower budget (€3/day). Add a new "Send Message" Ukrainian ad at €5/day. Pause the Russian.

**Cost**: ~€110 over 14 days.

**Pros**:
- A/B comparison: which actually books more workshops?
- Hedges the bet — if Message doesn't work, current keeps running
- Same total budget as now

**Cons**:
- Two campaigns to manage instead of one
- Smaller budget per variant → slower learning for both
- Decision deferred to Day 28 anyway

---

## Recommendation

**Option B — pivot to Message campaign.**

The data we have says people click but don't checkout. The audience clearly responds to the ads. The one real booking happened via DM. Pointing the ads at DM directly closes the loop the way the audience actually converts.

The risk is the response burden. If Diana/Koritsa can't keep up with DMs, the campaign loses its edge — slow responses convert worse than no campaign at all.

**Decision question for the team**: Can someone reliably reply to DMs within ~4 hours during the day, and within 12 hours always, for the next 14 days?
- If **yes** → Option B.
- If **maybe** → Option C (smaller risk).
- If **no** → Option A, but set up the auto-replies first to buy response time.

---

## What's needed to execute (per option)

### Option A
- Nothing. Campaign continues automatically until May 26, then we extend it on Day 14.
- Time required: 0 minutes.

### Option B (the recommended one)
1. **Diana**: set up IG + Messenger auto-replies via Meta Business Suite ([#90](https://github.com/diana0xUX/Saged/issues/90), ~15 min)
2. **Diana + Koritsa**: agree on DM-shift coverage (who replies when?)
3. **Claude/dev**: build new "Send Message" ad sets via API (~30 min), launch on May 26
4. **Test**: trigger a few of your own DMs to verify auto-replies fire correctly
- Time required: ~1 hour spread over a few days.

### Option C
- Combine Option A + B work above.
- Time required: ~1 hour.

---

## Tracking note (separate from the decision)

Regardless of which option we pick, the tracking gap (iPhone Safari blocking) won't fully close without server-side Conversions API integration. That's a ~1-2 hour engineering build. **It's worth doing for Option B** because each new DM should fire an attributable event. Not worth doing for Option A alone.

---

## Backup data (for the curious)

- Full daily reports: `reports/daily/`
- Weekly report: `reports/weekly/2026-W20.md`
- Lead-handling playbook (what to do once a DM arrives): `docs/lead-handling.md`
- Current Meta campaign + ad set IDs: `.campaign-ids` (gitignored)
