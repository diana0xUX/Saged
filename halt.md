# Halt — 2026-05-14 (first workshop day)

## Where we stopped

Brief check-in 48 h after Tuesday's campaign launch. Pulled a health-check report — campaign serving cleanly on both ad sets (CTR 2.95%, CPC €0.18, €15 spent of expected €20). 3 Schedule events in Pixel = 2 smoke tests + **1 real paid booking that came via Telegram DM, not the Meta ad**. Diana sent the booking link to someone on Telegram, they paid €60, and **the class ran today (Thursday 2026-05-14)** — first actual workshop delivered through the new booking infrastructure. Voluntary halt; nothing actionable until Day 8 (2026-05-20).

## Prior session summary (preserved)

Resumed 2026-05-12 from earlier halt. Stripe approval came through silently (no celebratory email — just `pk_live_*` keys and the EUR bank account confirmation on 11 May). Worked through the booking smoke-test (#61) end-to-end, hit two infrastructure gaps Diana fixed in Cal.com, and shipped the campaign live. **Campaign is ACTIVE as of ~11:42 UTC 2026-05-12.**

## Current state (2026-05-14)

- **Branch**: `main` (no code commits this session or last)
- **Last commit**: `99d9933` (unchanged)
- **Build status**: Pages live, no code changes
- **Open review**: none
- **Live URLs**: https://saged.club/ (RU) and https://saged.club/uk/ (UA)
- **Meta campaign**: 🟢 **ACTIVE, 48 h in** — €15.06 spent of €20 expected. CTR 2.95%, CPC €0.18, link clicks 66, video views 784. UA outperforming RU (CTR 3.79% vs 2.0%; CPC €0.13 vs €0.29). **0 campaign-attributed conversions** so far (normal for early days). Ends 2026-05-26.
- **First real paying customer**: 1 booking via Telegram (direct link, not ad). €60 cleared. Class ran 2026-05-14. Diana confirmed customer + class delivered.
- **Stripe**: APPROVED, live mode. Production payment cleared (the Telegram booking).
- **Cal.com**: All configured correctly; Meta Pixel app firing Schedule events on every paid booking regardless of source.

## Smoke-test scorecard (#61 — CLOSED)

- ✅ Cal.com event picker loads with right price/details
- ✅ Stripe checkout completes (after Diana enabled Stripe on the event type mid-session — Stripe-on-account is not enough, must be enabled per event type)
- ✅ €60 charge succeeded in dashboard, refunded on cancel
- ✅ Confirmation email + calendar invite delivered
- ✅ **Pixel `Schedule` event fires** — verified via Meta Graph API stats endpoint (2 Schedule + 4 CalcomView events in 10:00 UTC 2026-05-12 bucket). NOT visible in the Test Events UI in real time due to Meta's ~30 min aggregation lag.
- ✅ Custom Conversion (id `980444324695740`) maps Schedule → Purchase €60 — required because Cal.com's Meta Pixel app can't fire Purchase directly.

## Issues closed this session

- **#5** Hero video shot — shipped in prior sessions
- **#7** Gallery photos — shipped in prior sessions
- **#11** OG image — shipped in PR #80
- **#28** Build sales campaign — campaign was built and PAUSED
- **#34** 3 real testimonials — shipped in PR #77
- **#35** Pin workshop post on @saged.club — Diana confirmed pinned
- **#61** Smoke-test booking flow — full funnel verified end-to-end
- **#83** Install Cal.com Meta Pixel app — Diana installed and configured

## Issues opened this session

- **#83** (then closed) — Install Cal.com Meta Pixel app

## Next steps (in order — Diana's next sitting)

1. **No action until Day 8** (2026-05-20). Campaign is healthy, 0 attributed conversions is normal at 48 h, do not touch.
2. **Day 8 review** ([#62](https://github.com/diana0xUX/Saged/issues/62), 2026-05-20) — pause losers, scale winners. Run `python3 scripts/audit.py` for the first real report. Specific things to look at:
   - Is UA still outperforming RU? If yes, consider shifting budget split.
   - Did any campaign-attributed Schedule events fire? (NOT Pixel-total — that includes Telegram and direct.)
   - Frequency creep — if >3.0, audience may be saturating.
3. **Day 14 review** ([#63](https://github.com/diana0xUX/Saged/issues/63), 2026-05-26) — decide budget for next 14 days. Campaign ends naturally on this date.
4. **Optional cleanup** — delete old v1 ad sets `120244368150280513` (RU) and `120244368151220513` (UA). They're PAUSED with stale PURCHASE optimization. Safe to delete after v2 proves out. IDs preserved in `.campaign-ids` comments.
5. **Quick wins still open** — [#36](https://github.com/diana0xUX/Saged/issues/36) (Koritsa account pin — needs her), [#38](https://github.com/diana0xUX/Saged/issues/38) (Koritsa IG bio), [#41](https://github.com/diana0xUX/Saged/issues/41) (FB page refresh). #37 closed 2026-05-14.
6. **Worth considering after Day 8 data lands**: if Telegram keeps being the converting channel, build out [#39](https://github.com/diana0xUX/Saged/issues/39) (public @sagedclub Telegram channel) — it's currently low-priority but real revenue suggests it deserves promotion.

## Blockers

- None. Campaign is live, infrastructure verified, money flowing on Meta's side.

## Context that's hard to re-derive

- **Cal.com's Meta Pixel app cannot fire Purchase events.** Only `Lead`, `CompleteRegistration`, `Schedule`, `PageView`. Confirmed by reading their source (`packages/app-store/metapixel/zod.ts`). If you need Purchase optimization, the fix is a Meta **Custom Conversion** mapping Schedule → Purchase with €60 value.
- **Meta API gotcha**: can't change campaign objective once it has ad sets (error code 1885073). Can't change optimization event on a published ad set (error code 3260011). Workaround: create new ad sets with the desired optimization in the same campaign, leave old ones paused.
- **Meta Custom Conversion API uses `event_source_id`, not `pixel_id`** as the parameter name (despite the rest of the API using pixel_id). Cost me a minute earlier.
- **Meta Graph API `/{pixel}/stats?aggregation=event` has ~30 min aggregation lag.** Don't trust real-time absence of events as proof they didn't fire. The Test Events UI has its own quirks (requires sending the `test_event_code` param — Cal.com doesn't, so test bookings won't show up there at all even when working).
- **Stripe approval is silent now** — no celebratory email, just `pk_live_*` keys appearing in the dashboard + bank account confirmation. The "did Stripe approve us?" question is answered by checking the dashboard, not the inbox.
- **Cal.com bookings without a name show "Nameless"** as the customer — there's no required-name validation in the booking form. Low-priority quirk but could cause attribution chaos at scale. Worth verifying the booking form actually requires a name field for real customers.
- **The Cal.com app store install is per-event-type, not account-level.** Stripe being connected at account level is NOT enough; each event type has its own Apps tab where Stripe (and Meta Pixel) must be explicitly enabled with config (price + currency for Stripe; Pixel ID + event type for Meta Pixel).
- **All v1 ad sets (the original PURCHASE-optimized ones) remain PAUSED in the same campaign.** Don't accidentally toggle them — `.campaign-ids` only references the v2 IDs but Meta's UI will show all of them. Comments in `.campaign-ids` mark which are old.

## Skills + knowledge to persist

- Add to KNOWLEDGE.md: Custom Conversion `980444324695740` exists and maps Schedule→Purchase €60. v2 ad set IDs are the live ones. Cal.com per-event-type config requirement.
- Already updated: `.campaign-ids` (now points at v2 + has CUSTOM_CONVERSION_ID + commented OLD_*).
- Cross-session memory updated separately (Cal.com app event-type limitation, Meta API edit-locks).

## Open issues snapshot (most relevant)

- 🟢 **Live**: campaign 120244368076410513 — monitor via Ads Manager + scripts/audit.py
- 🟡 Diana quick wins still open: [#36](https://github.com/diana0xUX/Saged/issues/36), [#37](https://github.com/diana0xUX/Saged/issues/37) (maybe done), [#38](https://github.com/diana0xUX/Saged/issues/38), [#41](https://github.com/diana0xUX/Saged/issues/41), [#47](https://github.com/diana0xUX/Saged/issues/47)
- 🟡 Content for ad rotation: [#54](https://github.com/diana0xUX/Saged/issues/54), [#53](https://github.com/diana0xUX/Saged/issues/53), [#55](https://github.com/diana0xUX/Saged/issues/55), [#58](https://github.com/diana0xUX/Saged/issues/58), [#64](https://github.com/diana0xUX/Saged/issues/64)
- 🔵 Reviews scheduled: [#62](https://github.com/diana0xUX/Saged/issues/62) Day 8, [#63](https://github.com/diana0xUX/Saged/issues/63) Day 14
- 🟡 Other tactics: [#42](https://github.com/diana0xUX/Saged/issues/42) epic with 10 non-standard tactics ([#43](https://github.com/diana0xUX/Saged/issues/43)–[#52](https://github.com/diana0xUX/Saged/issues/52))
