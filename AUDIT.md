# Phase 0 Audit — Findings

**Date**: 2026-05-11
**Source**: Meta Marketing API v25.0, ad account `act_484884320671439`, last 90 days
**Auditor**: Claude (System User on Saged.design BM)

---

## TL;DR

The €105 spent on Meta over 90 days (across 9 boosted Instagram posts) produced **zero workshop bookings** because the ads were structurally incapable of producing them — there is no conversion event being tracked, no landing page to convert on, no language filter on the targeting, and every campaign was optimized for something *other than* bookings (messages, profile visits, or link clicks).

This isn't a creative or budget problem. It's a **funnel problem at every layer**. The good news: now that we can see the data clearly, the fixes are concrete.

---

## 0.0 Spend channels

- **Meta (Facebook + Instagram)**: €105.38 across 9 boosted posts over 90 days (Feb 10 – May 10, 2026). Lifetime account spend: €143.43.
- **Telegram channel sponsorship**: €60 (one-off, outside Meta — not in scope for automation).
- **Account status**: ⚠️ **UNSETTLED** (status code 3). There's an unpaid invoice on the ad account — Meta may restrict new ad delivery until paid. Check Ads Manager → Billing.
- **Timezone**: `Atlantic/Canary` — wrong for Valencia. Should be `Europe/Madrid`. Affects how spend is bucketed in reports. Worth fixing.

## 0.1 Campaign objectives — 🚩 ROOT CAUSE #1

| Objective | Count | What it tells Meta to do | What we actually want |
|---|---|---|---|
| `MESSAGES` | 5 | "Get people to start a DM with us" | Get them to *book a workshop* |
| `LINK_CLICKS` | 4 | "Get clicks on a URL" | (no quality filter) |
| `OUTCOME_SALES` / `OUTCOME_LEADS` | **0** | Get conversions | ✅ this is what we need |

🚩 **No campaign has the right objective for bookings.** Even if everything else were perfect, Meta literally isn't trying to drive bookings — it's trying to drive DMs and clicks.

## 0.2 Pixel + tracking — 🚩 ROOT CAUSE #2

- **Pixels on this ad account**: **0** (confirmed: `pixels` endpoint returned `{"data":[]}`).
- **Conversions API**: not connected (no Pixel to connect it to).
- **Conversion events in last 90 days**: `link_click`, `page_engagement`, `video_view`, `post_reaction`, `messaging_block`, `post_save` — all on-platform "soft" actions. **No `lead`, `purchase`, `complete_registration`, or any booking-related conversion event exists**.

🚩 **Meta is optimizing blind.** Even if someone booked a workshop via DM, Meta has no way to know — so the algorithm can't find more people like them.

## 0.3 Funnel destination — 🚩 ROOT CAUSE #3

**Confirmed**: no landing page anywhere in the funnel.

Of the 9 ads:
- **6** send people to an Instagram profile or DM (`VIEW_INSTAGRAM_PROFILE`, `MESSAGE_PAGE`, `CHECK_AVAILABILITY`, `CONTACT_US` CTAs).
- **1** sends to `https://fb.com/messenger_doc/` — a Messenger document (still no booking flow).
- **2** show `LEARN_MORE` or `SHOP_NOW` CTAs but have no link attached.
- **0** point to an actual landing page with a booking action.

The funnel for every ad ends in: **Instagram profile** or **DM thread**, where the visitor has to figure out how to book on their own.

Of the 190+ conversation attempts started, **23 people *blocked* the messaging** — 12% block rate. Meta sees these as a negative quality signal.

## 0.4 Creative

The 9 ads are all **boosted Instagram posts** (not built-for-ads campaigns). Naming pattern `"Instagram post: ..."` confirms it.

**Languages used in creative**:
- Russian: 5 ads (the most spent on — including "Дорогие девочки!" with €28 spend, 10,302 reach)
- English: 3 ads (Saged.club intro posts, Kirtan event)
- Spanish: 1 ad

**Brand identities mixed in the copy**:
- **Saged.design** (parent business name in BM)
- **Saged.club** (described as a Valencia community space for people with Eastern European / post-Soviet roots)
- **Neuroclay** (clay-as-therapy workshop product)
- Plus individual events: tea ceremony + sound meditation, Kirtan, gua sha self-massage

🚩 This isn't a clear "ceramic studio." It's a multidisciplinary cultural/wellness club whose offerings cross categories. The current messaging is too fragmented for Meta's algorithm to pattern-match.

**Top-performing creative by CTR** (note: CTR ≠ bookings, but signals what catches attention):
- "Saged.club is for..." — **4.0% CTR**, €19.75 spent, 3,059 reach, 174 link clicks (English, positioning the audience clearly)
- "Saged.club is now open." — **4.0% CTR**, €19.73 spent (English, soft launch announcement)
- "Звук, рождённый в Тишине" (Sound born in silence — RU sound meditation) — 1.5% CTR

**Worst performing** (by CTR + negative signals):
- "[4/29/2026] Promoting messenger_doc" — €32 spent, **15 messaging_blocks** (highest negative signal)
- "Дорогие девочки!" — €28 spent, 6 messaging_blocks, only 0.82% CTR despite 10k reach

**Two ads have `WITH_ISSUES` status** — Meta flagged "Neuroclay" and "Kirtan" posts (likely policy or asset quality). Worth checking in Ads Manager.

## 0.5 Audience targeting — 🚩 ROOT CAUSE #4

| What the user wanted | What the data shows |
|---|---|
| Russian + Ukrainian speakers in Valencia | **Language targeting: empty on every ad set.** Russian creative serves to anyone in the geo. |
| Valencia specifically | 3 ad sets target only Valencia city; 5 target all of Spain (`ES`); 1 targets Madrid + Barcelona + Alicante + Ibiza + Málaga + Germany; 1 targets NL + ES + BE + DE |
| Workshop-relevant audience | **No interest targeting on any ad set.** All rely on Advantage+ auto-expansion, but with no Pixel + no Custom Audiences, the algorithm has no seed signal to expand from |

**Custom Audiences in account**: **0**.
**Lookalike Audiences**: **0**.

🚩 The targeting is **scattered**, inconsistent across ad sets, and missing the one filter (language) that would actually deliver the intended audience.

## 🚩 Root-cause hypothesis (final)

In order of impact:

1. **Wrong campaign objectives** — every campaign optimized for engagement/clicks/messages, never for bookings. Even fixing everything else, this alone would prevent meaningful conversion learning.
2. **No conversion tracking** — no Pixel, no CAPI, no booking event. Meta cannot optimize for what it cannot see.
3. **No landing page / no booking destination** — every funnel ends in IG profile or DM, where booking is a manual conversation.
4. **No language targeting** — Russian-language creative serves to general Spanish residents; signal is lost in noise.
5. **Scattered targeting + no audience pool** — no Custom Audiences, no Pixel data, inconsistent geo/age/gender; algorithm has nothing to learn from.
6. **Brand identity fragmentation** — Saged.design / Saged.club / Neuroclay / various events — Meta can't pattern-match what the studio actually sells.

## Decisions for Phase 1

Before spending the remaining €150, fix in this exact order:

1. **Settle the unpaid Meta invoice** — until account is out of UNSETTLED status, new ads may be throttled. ~5 min in Billing.
2. **Pick ONE primary conversion goal** to design around. Recommendation: **workshop booking (pottery, since "Neuroclay" seems to be the most differentiated offering)**. The other offerings (sound meditation, gua sha, kirtan) can run later with the same infrastructure.
3. **Build a one-page bilingual (RU/UA) landing page** with:
   - Hero: 5-second video of clay being formed + headline in user's language
   - One offer: a specific workshop with date, price, what's included
   - A booking widget (Calendly / Cal.com / Tally) → Stripe payment link
   - Cookie consent banner (EU mandatory)
4. **Install Meta Pixel + Conversions API** on the landing page. Define the conversion event `Purchase` (workshop paid) and `Lead` (form started but not paid).
5. **Verify in Events Manager**: a test booking fires both Pixel and CAPI, dedup ID matches.
6. **Rebuild the campaign in Ads Manager** (not Boost Post):
   - Objective: **Sales (Conversions)** optimizing for `Purchase`
   - 2 ad sets: one targeting `Russian` language + Valencia, one targeting `Ukrainian` language + Valencia
   - Daily budget ~€5/ad set for 14 days
   - 2 creatives per ad set: hands-on-clay + finished-piece-reveal, both vertical 9:16 with subtitles, CTA `BOOK_NOW`
7. **Fix timezone** to `Europe/Madrid` in Ads Manager → Account settings (one-time, cosmetic but useful for reporting).
8. **Pause the 9 existing boosted posts** that are still ACTIVE. They're spending money without producing bookings. Keep "Saged.club is for..." paused-but-saved as creative inspiration (it had the best CTR — the *audience positioning* of that copy works).

## What's NOT a problem

Worth naming for confidence:
- **CTR (1.97% account-wide)** is fine. Industry average is 1–2%.
- **CPC (€0.17)** is excellent. Audience-fit is not the limiting factor.
- **Reach (22,564 people for €105)** is healthy. Meta is delivering — we just don't have anywhere good to send them.
- **Frequency (1.4)** is low — no audience fatigue.

The creative attention works. The funnel doesn't.

## Estimated impact of fixes

Conservative back-of-envelope:
- 22,564 people reached at current spend
- 473 link clicks (2.1% click-through)
- If we add a real landing page with a clear offer, **typical small-business landing-page conversion** is 2–5% of link clicks for workshop signups.
- Expected bookings from same spend, post-fixes: **9–24 workshop signups over 90 days**
- At even a €30 workshop price: **€270–720 revenue** vs. current €0. Worth fixing.

This assumes language targeting + landing page + tracking + conversion-optimized campaign. Doing only one of those won't move the needle much.
