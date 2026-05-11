# Execution Plan — Ceramic Studio Workshops, Valencia

A small-business roadmap sized for **€150/month spend**, **RU + UA audience**, **workshop bookings**.

Read `CLAUDE.md` first for context. This plan is intentionally lightweight — no automation until there's volume worth automating.

## Plan at a glance

| Phase | Calendar | Goal | Deliverable | Status |
|---|---|---|---|---|
| **0 — Audit** | Day 1 | Diagnose why the first €150 made zero bookings | `AUDIT.md` filled with findings | ✅ **done 2026-05-11** |
| **1 — Foundations** | Week 1–2 | Working landing page, tracking, consent banner | One-page bilingual site live, Pixel+CAPI verified | 🟡 landing live, tracking pending |
| **2 — Campaign rebuild** | Week 2 | Two ad sets (RU, UA) with localized creative + offer | Live campaign with proper objective + tracking | ⏳ blocked by Phase 1 tracking |
| **3 — Manual review loop** | Weeks 3–6 | Weekly read + creative iteration | 4 weekly reviews logged | ⏳ |
| **4 — Decide what to scale** | Week 7 | Make a real decision about budget + automation | Go/no-go on next investment | ⏳ |
| **5 — (Conditional) light automation** | Later | Only if Phase 4 says yes | Scheduled report + simple data pull | 🟢 `scripts/audit.py` ready (stdlib only) |

---

## Phase 0 — Audit (Week 1, ~1 hour)

**Goal**: write down what the existing setup looked like and which of the five usual suspects broke it.

Do this **in Meta Ads Manager UI**, no code. Five things to check:

### 0.1 Campaign objective
Open Ads Manager → find the existing campaign that spent €150. Note its **objective**.
- If it's **Engagement**, **Reach**, **Traffic**, or **Awareness** → that's the bug. Meta won't optimize for bookings if you didn't ask it to. Need **Sales** (Conversions) or **Leads**.
- If it's **Sales / Conversions** but the conversion event isn't tracked → same outcome, different cause.

### 0.2 Pixel + tracking
Open Events Manager (business.facebook.com/events_manager2) → find the Pixel for your business.
- Does a Pixel exist? Is it firing? (Green checkmark on `PageView` is the minimum.)
- Is there a `Lead`, `Purchase`, or `CompleteRegistration` event firing? If no → Meta is blind.
- Is Conversions API connected? Probably not — note it.

### 0.3 Funnel destination
What URL did the ad link to?
- IG profile → dead end; people scroll, then leave. ~zero conversions expected.
- Outdated website → if the site doesn't have a clear "book a workshop" button above the fold, same outcome.
- Calendly / form direct → check if it loads fast and looks trustworthy.

Count the **clicks from ad to "I have paid"**. If > 3, that's friction worth fixing.

### 0.4 Creative
Look at the ads themselves.
- **First 3 seconds**: is there a hook (face, hands working clay, finished piece reveal)? Or is it product-photography flat?
- **Language**: Russian-only, Ukrainian-only, Spanish, English? If only one — what about the other audience?
- **CTA**: explicit ("Book your first class — €X off") or vague ("Visit our studio")?
- **Format**: image, carousel, video, Reel? Video and Reels generally win for small businesses in 2026.

### 0.5 Audience
Look at the ad set's targeting.
- Location: Valencia + how big a radius?
- Language: is "Russian" or "Ukrainian" set? Or unset (= Meta serves everyone)?
- Detailed interests: anything specific? (Note: as of Jan 2026, most granular interests were removed — Advantage+ Audience is now the default.)
- Custom Audiences: any built? (Probably not yet.)

### Deliverable
Create `AUDIT.md` in the project folder with one paragraph per check, marking ✅ or 🚩. I'll help you write it once you've poked around.

---

## Phase 1 — Foundations (Week 1–2)

Before any new spend, fix what was broken.

### 1.1 Landing page (1 day)
A single page, two languages (RU and UA, with a toggle), with **one** primary action: book a workshop.

Structure:
- **Hero**: 5-second hook — photo or 6-second clip of hands on clay, a finished piece, the studio. One headline in the visitor's language.
- **Offer**: clear price + duration + what's included. *"€35 — 2 hours — leave with your own piece."*
- **Why book this specific workshop**: 3 bullets (atmosphere, language fit, what you'll learn).
- **Trust signals**: 2-3 photos of past workshops with real people, 1-2 short testimonials in the visitor's language.
- **Booking**: Calendly/Cal.com/Tally form → confirm + redirect to a thank-you page.
- **Cookie consent banner**: explicit opt-in (EU requirement) — Pixel doesn't fire until consent given.

Recommended tools:
- **Framer** or **Carrd** for the page (under €15/month, no developer needed).
- **Cal.com** (free) or **Calendly** (free tier) for booking.
- **Cookiebot** free tier for consent.
- **Stripe Payment Link** for paid bookings (€0 setup, ~3% per transaction).

### 1.2 Tracking install (half a day)
- Add **Meta Pixel** to the landing page (one snippet in `<head>`).
- Configure events: `PageView`, `Lead` (form submit), `Purchase` (Stripe success page).
- Connect **Conversions API** via Meta's one-click setup (April 2026 update made this trivial for most stacks).
- Verify in Events Manager: dedup ID matches between Pixel and CAPI.

### 1.3 Bilingual setup
- Both language versions live on the same site at e.g. `/ru` and `/ua`.
- The page accessed determines which Meta Pixel content variant fires (use `content_name` parameter).
- This lets us see which language converts better without splitting the technical stack.

### Deliverable
Live landing page; Pixel + CAPI verified with at least one test conversion firing.

---

## Phase 2 — Campaign rebuild (Week 2)

**Budget**: split your €150 → ~€75 to each of two ad sets, 14-day run.

### 2.1 Campaign structure
- **Campaign objective**: Sales (Conversions), optimizing for `Lead` or `Purchase` event.
- **Two ad sets**:
  - **Ad Set A — Russian speakers in Valencia**: targeting language = Russian, location = Valencia + 25 km, age 25–55.
  - **Ad Set B — Ukrainian speakers in Valencia**: targeting language = Ukrainian, location = Valencia + 25 km, age 25–55.
- Detailed targeting: leave open (Advantage+ Audience will expand from the language + location signal).
- Daily budget: ~€5/day per ad set.

### 2.2 Creative (per ad set)
Make **2 ads per ad set** — different angles, same offer:
- **Ad 1**: hook = hands on the wheel, clay forming. Copy = the experience.
- **Ad 2**: hook = finished piece reveal. Copy = what you take home.

Each ad in the matching language. Use **vertical 9:16 video** if possible (Reels), 15–30 seconds. Add subtitles. End with the offer + the "Book your spot" button.

### 2.3 Quality checks before launch
- Click the ad preview yourself. Does the page load in <3s? Is it in the right language?
- Submit a test booking. Does Stripe show "succeeded"? Does Meta Events Manager see the `Purchase` event?
- Open the page on mobile — small business ads convert almost exclusively on mobile.

### 2.4 Launch
- Schedule the campaign to run **14 days minimum**. Don't touch it for the first 7 days (learning phase).
- Daily glance: spend pacing, no comments/policy issues. **Do not change anything** in the first week.

---

## Phase 3 — Manual review loop (Weeks 3–6)

Weekly cadence, 30 min each.

### 3.1 Weekly review template
Every Monday, in Ads Manager, write 4 lines:
- Spend last 7d / 7-day total
- Bookings (from Stripe) — confirm match with Meta `Purchase` events
- Cost per booking (€spend / bookings)
- Which ad set + which creative won?

### 3.2 Decision rules
- If an ad has spent >€30 with zero conversions and the rest of the ad set is converting → **pause that ad**.
- If a creative looks fatigued (frequency > 2.5 in 7 days, CTR dropping) → **swap in a new creative**.
- If one language clearly outperforms (>2× the other) and you don't have appetite to fix the loser → **reallocate budget**.
- **Don't change everything at once.** One change per week max — otherwise you can't tell what worked.

### 3.3 Creative refresh
Keep a list of 3–5 new creative ideas in a doc. Refresh one ad per week.

### Deliverable
4 weekly review notes in `AUDIT.md` (or a new `REVIEWS.md`); a clear sense of which language + which creative angle works.

---

## Phase 4 — Decide what to scale (Week 7)

Pause and answer honestly:

1. **Is the math working?** Cost per booking < workshop price - cost of materials - studio time?
2. **Is one segment clearly viable?** If RU works and UA doesn't (or vice versa), commit to the winner.
3. **What's the bottleneck now?**
   - Creative? → keep iterating manually, no automation needed.
   - Volume / consistency? → budget bump (€500–1,000/month is the next realistic step).
   - Reporting fatigue? → that's when light automation justifies itself.

**If the answer is "math doesn't work yet"**: do not add automation. Loop back to Phase 1.3 / 2.2 (landing page, creative). Most small-business ad failures are creative + offer problems, not measurement problems.

---

## Phase 5 — (Conditional) light automation

**Only enter this phase if Phase 4 says the foundations work AND budget is climbing past €500/month.**

At that point, light automation pays off:

1. **Scheduled report** — a Python script that pulls the last 7 days of campaign data via Meta Marketing API and emails / Slacks you a 1-page summary. The Phase 5 spec from the original (now archived) plan is a useful reference; we don't need MMM or Robyn at this scale.
2. **Creative tagging via vision LLM** — when you have 20+ ads run, tag what's in each, join to performance, find patterns. This is the "design research" layer where your UX brain has the most leverage.
3. **Custom Audience pipeline** — upload past customers + email list as a hashed Custom Audience, build a 5% Lookalike. Cheap, high-impact when first-party data is meaningful.

Code-level details live in the original (enterprise-flavored) plan, archived in `research.md`. We'll pick from it when relevant — but only when relevant.

---

## Critical Meta deadlines that affect this project

- **June 9, 2026** — Marketing API versions < v24.0 retired. Not a problem if we don't write code in Phases 0–4.
- **EU consent (DMA, in effect Jan 2026)** — Spanish users must opt-in before tracking. The landing page consent banner is non-negotiable.
- **GPC honoring** — not directly relevant in EU (consent model is stricter), but worth knowing if we ever expand.

## Effort sizing (realistic, evenings + weekends pace)

| Phase | Calendar | Effort |
|---|---|---|
| 0 — Audit | 1 hour | sitting with Ads Manager |
| 1 — Foundations | 3–5 evenings | landing page + tracking |
| 2 — Campaign rebuild | 2 evenings | creative + launch |
| 3 — Review loop | 30 min/week × 4 | weekly review |
| 4 — Decide | 1 hour | honest reflection |

**Total to a decision point**: ~6 weeks, very part-time.
