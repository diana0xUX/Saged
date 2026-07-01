# Adult campaign relaunch plan

**Decision date**: 2026-06-09
**Cool-down period**: 2026-06-09 → 2026-06-23 (14 days, campaign PAUSED)
**Relaunch target**: 2026-06-23 (Tuesday)

## Why we're doing this

The current adult campaign (`Saged · Керамика с Корицей · Sales · v1`, ID `120244368076410513`) was paused 2026-06-09 because:

- 30 days lifetime, €141.89 spent, 891 clicks, **0 attributed bookings**
- Frequency 5.0 across 5,156 unique people reached — audience near saturation
- CTR halved week-over-week (5.20% → 1.99%) — classic creative fatigue
- CPM rose (€4.95 → €6.38) — Meta charging more to find anyone new
- All bookings to date came through DM, not click-to-checkout

The 2-week cool-down lets the audience "forget" before fresh creative gets a second look.

## What changes at relaunch

### Three ad sets, not two

| Ad set | Locale | Geo | Status today | Notes |
|---|---|---|---|---|
| RU | 17 (Russian) | Valencia 17km | exists, currently broken | **Locale check needed — see below** |
| UA | 52 (Ukrainian) | Valencia 17km | exists | verify locale ID at relaunch |
| **EN (new)** | 6 (English UK) or 1 (English US) | Valencia 17km | to be created | English-speaking expats / digital nomads in Valencia |

**EN ad set details:**
- Same campaign (`120244368076410513`) — reuses the Sales objective and Custom Conversion setup
- Geo: Valencia + 17km radius, `location_types: ["home"]` (same as RU/UA — hyperlocal tightening proven 2026-05-20)
- Age: 25-65 (mirror RU/UA)
- Locale: English. Verify which Meta locale ID — historically Meta uses 1 (en_US) and 6 (en_GB). Use `/search?type=adlocale&q=english` to confirm before creating.
- Budget: €5/day to start (lower than €10 RU/UA — English audience may be a smaller intent pool for ceramic-with-Korytsia; ramp if CTR ≥ 2%)
- Creative: needs English version of new copy + visuals

### Locale-targeting bug (FIXED 2026-06-09)

While planning the relaunch we discovered the adult campaign had wrong locale IDs the whole time:
- RU ad set was `locale: [10]` → Italian
- UA ad set was `locale: [37]` → Bulgarian

Both fixed today (RU=17 / UA=52, verified against Meta's `/search?type=adlocale`). The campaign is paused, so the fix is silent until relaunch. Root cause was hardcoded IDs in `scripts/local/build-meta-campaign.sh`; that script now has a runtime `verify_locale` guard.

**English ad set at relaunch**: use locale 24 (English UK) for Valencia expats. Or 6 (English US). Both verified. Decide on UK vs US at relaunch.

## Decision Diana needs to make: campaign objective

Bigger question for the relaunch. The current campaign uses **Sales objective + Custom Conversion** (Schedule → Purchase €60). That's "click → land on saged.club → book via Cal.com → fire Pixel Schedule event."

But the project knowledge says: **for €60 community workshops to RU/UA audiences, "message first → pay later" converts better than "click → checkout."** Evidence: 247 ad-driven visits in May → 0 attributed Stripe checkouts; first €60 booking came through a Telegram DM link, not a click on the ad.

Two paths at relaunch:

| | Option A: Keep Sales objective | Option B: Switch to Messages objective |
|---|---|---|
| What it does | Click ad → land on saged.club → book via Cal.com | Click ad → opens WhatsApp/Messenger DM with Saged |
| Pro | Less rebuild work, keeps existing Pixel + conversion setup | Aligns with the channel that actually converts |
| Con | Same conversion pattern that produced 0 bookings in May | Have to rebuild the campaign (campaign objective is locked once ad sets exist) |
| Effort | Low — new creative + EN ad set | Medium — new campaign + new ad sets + WhatsApp/IG message setup |

**Recommendation**: Option B (Messages). The data is asking for it. But this needs Diana's call before I build it.

## New creative brief

The relaunch needs fresh visuals + fresh copy in 3 languages. The audience has seen the current ad ~5 times each — same images, same words won't work.

### What to change

- **New angle**: not "ceramics with Korytsia" (positioning Korytsia as the teacher). Try the **format** as the hook: "two Thursdays, one piece" or "you make it, we fire it, you take it home." Shifts emphasis from instructor to ritual.
- **Image**: avoid reusing the existing Korytsia-at-wheel shots. Pull from the `Vaamos Photos/Fotos/` archive (58 pro shots of the ceramics workshop) for unseen frames. Strong candidates: hands working clay, finished pieces on shelf, the candle-lit studio aesthetic.
- **CTA**: if Option B (Messages) → "Напишите, чтобы записаться" / "Напишіть, щоб записатися" / "Message us to book." If Option A → "Забронировать четверг" / "Забронювати четвер" / "Book your Thursday."
- **Length**: short. Single-image static ads — the prior CTR peak (5.2%) was on a static ad set, not video.

### Three hooks to test if budget allows separate ads in each ad set

1. **The ritual hook**: "Замедлиться на два четверга." Emphasis on the slowdown/anti-rush angle.
2. **The product hook**: "Чашка, которую вы сделали сами." Emphasis on the take-home object.
3. **The community hook**: "Маленькая группа, ваш язык, тёплая мастерская." Emphasis on belonging.

EN versions:
1. "Slow down for two Thursdays."
2. "A cup you made with your hands."
3. "Small group, warm studio, your pace."

### What stays

- Warm clay neutrals, no neon, no urgent CTAs (brand voice rules — see KNOWLEDGE.md)
- Saged.club branding subtle, not loud
- Valencia 17km geo lock (proven 2026-05-20)

## Pre-launch checklist (for me to run on 2026-06-23)

- [ ] Verify all locale IDs via `/search?type=adlocale` — fix RU ad set if locale 10 is indeed English
- [ ] Confirm Diana's decision on Sales vs Messages objective
- [ ] If Messages: build new campaign, archive old one
- [ ] Upload new creative assets (RU + UA + EN)
- [ ] Create EN ad set under the active campaign
- [ ] Re-activate RU + UA ad sets with new creative attached
- [ ] All ad sets ship PAUSED — Diana flips ACTIVE in Ads Manager
- [ ] Update `.campaign-ids` if new campaign/ad set IDs
- [ ] Update `KNOWLEDGE.md` decision log

## What Diana needs to provide before relaunch

1. **Decision: Sales objective or Messages objective?** (one question, I can implement either)
2. **New creative assets** — 3 images (RU, UA, EN) or 1 image + 3 copy variants. Photos from existing archive are fine if unused on Saged ads before.
3. **Confirm budget**: €10 RU + €10 UA + €5 EN = **€25/day combined** at relaunch. Or different split.

## Success criteria — what makes us NOT pause again

After 14 days of relaunch (so by 2026-07-07):

- At least 1 attributed booking (either Schedule via Pixel OR a DM that mentions seeing the ad)
- Frequency stays below 3.0 (means audience is still growing, not just re-seeing)
- CTR holds above 2.0% in week 2 (not just initial novelty)

If none of these hit by 2026-07-07: stop spending on cold acquisition for the adult workshop entirely. Channel the budget into IG content + retargeting + the kids campaign instead.
