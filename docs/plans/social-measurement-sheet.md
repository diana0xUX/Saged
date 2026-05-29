# Social media measurement scaffold

**Epic:** [#111 Social media mediaplan](https://github.com/diana0xUX/Saged/issues/111)
**Related:** [#113 Lena trial · Reel concept research + shoot brief](https://github.com/diana0xUX/Saged/issues/113)
**Purpose:** make organic social efforts measurable BEFORE Lena's paid shoot day, so the 4-week pilot has a real comparison baseline.

---

## What we're measuring

Saged today has no per-post measurement. We post, things happen, no causal link between posts and bookings. This scaffold fixes that with **5 metrics tracked per Reel/carousel** and one intake question that closes the attribution loop.

This isn't "tracking for tracking's sake." It's the only way to know whether **paying Lena** drives more bookings than barter-only content. The decision rule from the audit:

> Pay Lena monthly if her posts drive **≥1.5× bookings per post vs amateur baseline**.

To compute that ratio honestly we need both sides of the equation. That's what this sheet is for.

---

## The 5 metrics per post

| Metric | Source | Why it matters | How to log |
|---|---|---|---|
| **Reach** | IG Insights (post-level) | Did Meta show this post to anyone? Baseline for everything else. | Note value 7d after posting |
| **Saves** | IG Insights (post-level) | Strongest organic intent signal — more predictive than likes. Someone saving a Reel is bookmarking it for later, often for booking. | Note value 7d after posting |
| **Profile visits (24h)** | IG Insights (post-level) | How many of the people who saw the post went to look at @saged.club. Bridges from "scroll" to "consider." | Note value 24h after posting |
| **DMs received (7d)** | Manual count | How many new DM conversations started in the 7 days after this post went live, where the person mentions or alludes to recent content. | Daily tally in WhatsApp + IG inbox |
| **Bookings ascribed** | Manual log | How many bookings happened where the customer said "I saw your [Reel / story / post]." | At intake — "where did you see us?" question |

Why these 5 specifically:
- **Reach** is the denominator for everything else
- **Saves** is the leading indicator that compounds — high-save posts tend to drive bookings days/weeks later
- **Profile visits** is the bridge between awareness and consideration
- **DMs** is Saged's actual funnel entry — Diana's classes book via DM, not Cal.com (KNOWLEDGE.md "high-touch DM-first booking")
- **Bookings** is the only number that actually pays the rent

---

## The intake question (the unlock)

This is the highest-leverage change in the whole scaffold. Without it, the entire stack of metrics floats unattributed.

### Where to add it

**1. WhatsApp first-reply template** (priority — that's where most leads land)

Current Diana flow: lead DMs → Diana responds with a warm message. Add ONE line:

> *"How did you find us?"* (RU/UA: *Как вы нас нашли? / Як ви нас знайшли?* · EN: *Where did you hear about us?*)

Place it after Diana's greeting, before logistics. Make it feel like genuine interest, not a survey.

**Example RU full template (for reference, adjust to Diana's voice):**

> Привет! Спасибо, что написали. Я Диана, основательница Saged.
>
> Можно небольшой вопрос — как вы нас нашли? (Инстаграм / Reels / друг / Гугл / еще что-то?) Это правда помогает понять, что работает 🌿
>
> Сейчас расскажу про класс/коворкинг/…

**2. Cal.com booking form** (secondary — captures self-serve bookings)

Add a custom field to the Cal.com booking event: dropdown "Where did you hear about us?" with options:
- Instagram (Reel)
- Instagram (Story)
- Instagram (Post)
- TikTok
- Friend / referral
- Google
- Other

Cal.com supports custom questions on the booking flow — settings → event type → questions.

**3. In-class casual ask** (validation)

When a new student starts their first class, Korytsia / Vita / Diana ask casually: "where did you find us?" — log answer in the tracking sheet within 24h.

### Tagging answers back to posts

If someone says "your Reel about [thing]" — match to the post in the sheet. If they say "Instagram" generically, log as `IG-untagged`. Over time the untagged percentage drops as Diana learns to probe ("which post specifically?").

---

## The tracking sheet

A simple Google Sheet is sufficient. No fancy tooling at this scale.

### Sheet 1: "Post log"

| Date posted | Account | Format | Topic | Producer | Reach (7d) | Saves (7d) | Profile visits (24h) | DMs ascribed (7d) | Bookings ascribed | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-30 | @saged.club | Reel | Korytsia hands wheel | Korytsia | | | | | | |
| 2026-05-31 | @saged.club | Story | Thursday class | Korytsia | n/a | n/a | n/a | | | Stories logged minimally |
| 2026-06-02 | @saged.club | Reel | Diana founder face | Diana | | | | | | |
| 2026-06-15 | @saged.club | Reel | Lena hero #1 | Lena (PAID) | | | | | | Mark Lena posts clearly |

**Conventions:**
- "Producer" is who made it — matters for ROAS comparison
- "Lena (PAID)" rows go in a different color/tab so the comparison is one-click
- "Reach" updated 7d after post (close enough to final, IG keeps updating slowly)
- "Bookings ascribed" updated as they come in over the post's lifetime
- Stories logged minimally (date + account + topic) since IG doesn't show per-Story analytics easily

### Sheet 2: "Booking log"

Already partially exists in Diana's head. Make it explicit:

| Booking date | Product | Channel of first contact | Where they saw us | Tied to post (if known) | Revenue | Notes |
|---|---|---|---|---|---|---|
| 2026-06-10 | Adult Thursday | WhatsApp | "Your Reel about Korytsia" | Reel 2026-06-02 | €60 | |
| 2026-06-12 | Kids trial | WhatsApp | "Instagram" | IG-untagged | €25 | |

### Sheet 3: "Weekly summary" (auto-computed)

| Week ending | Posts | Avg reach | Avg saves | Total DMs | Total bookings | Bookings/post | Bookings/post (Lena only) | Bookings/post (amateur only) |
|---|---|---|---|---|---|---|---|---|

The last two columns are the **decision rule input** — Lena's ratio vs amateur baseline.

---

## The 4-week pilot flow

| Week | Status | Action |
|---|---|---|
| **Week 1** | Baseline 1 | Korytsia + Diana + Vita post normally. Log all 5 metrics. Intake question live in WhatsApp + Cal.com. |
| **Week 2** | Baseline 2 | Same. Build the baseline dataset. Aim for at least 4-6 amateur posts in the log by end of week. |
| **Week 3** | Lena pilot 1 | Lena's first 2 hero Reels ship. Diana + Korytsia + Vita also continue normal posting. |
| **Week 4** | Lena pilot 2 | Lena's remaining 2 hero Reels ship. Continue baseline posting. |
| **End of week 4** | Decision | Compute "bookings per post (Lena)" vs "bookings per post (amateur)". Apply 1.5× rule. |

If sample sizes are too small for confidence (fewer than 3 bookings on either side), extend the pilot 2 weeks rather than deciding on noise.

---

## What we are NOT measuring (yet)

Out of scope for the trial — add later only if needed:

- Per-Story analytics (IG makes this painful, low signal)
- Follower growth attribution (lagging indicator, useful at scale not at our size)
- Cross-platform attribution (TikTok / YT Shorts) — defer until cross-post pipeline exists
- Brand search lift — too small scale to read
- Customer lifetime value per acquisition channel — premature

---

## Implementation checklist

- [ ] Create the Google Sheet with 3 tabs (Post log / Booking log / Weekly summary)
- [ ] Diana shares sheet with Korytsia + Vita (read for them, write for Diana)
- [ ] Add "How did you find us?" line to WhatsApp first-reply template (RU + UA + EN versions)
- [ ] Add custom question to Cal.com adult-workshop event
- [ ] Brief Korytsia + Vita on the in-class ask (one sentence in passing)
- [ ] Test by logging 1 amateur Reel through the full flow before Lena's pilot starts
- [ ] Tab 3 ("Weekly summary") gets one row at end of each week

Total setup time: ~2 hours. Most of it is the sheet structure + writing the WhatsApp template variants.

---

## What success looks like at end of week 4

| Outcome | Decision | Then |
|---|---|---|
| Lena ≥1.5× bookings/post vs amateur | Pay her monthly retainer for 1 shoot day/month | Schedule recurring shoot day, refine brief |
| Lena 1.0-1.5× | Keep barter only | Lena still produces 1 hero Reel/month via barter, no paid retainer yet |
| Lena <1.0× | Barter only AND adjust brief | Likely wrong concept type. Re-run trial with different concepts in 4 more weeks |
| Sample size too small | Extend pilot 2 weeks | Don't decide on <3 bookings either side |

---

## Open questions

- ~~**Existing Diana booking log**~~ ✅ **Resolved 2026-05-29** — Diana keeps it in WhatsApp threads. Booking sheet starts fresh as part of this scaffold.
- ~~**WhatsApp first-reply template ownership**~~ ✅ **Resolved 2026-05-29** — drafted by Fergie, see [`intake-templates.md`](intake-templates.md). Diana to review for voice fit and paste into her saved replies.
- ~~**Cal.com permissions**~~ ✅ **Resolved 2026-05-29** — no API key in `.env` yet; UI path (~2 min in Cal.com dashboard) is the recommendation. API path optional with key added to `.env`. See [`intake-templates.md`](intake-templates.md) for both paths.
