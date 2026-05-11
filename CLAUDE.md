# Meta Marketing Automation — Ceramic Studio (Valencia)

## What this project is

A real client project: **a ceramic studio in Valencia old city**, marketing pottery workshops to **Russian-speaking and Ukrainian-speaking residents** of Valencia via Meta (Facebook + Instagram) ads.

Goal: turn ad spend into workshop bookings — currently zero conversions on €150 spent.

The owner is **Diana**, a UX designer. Explanations and docs favor plain language + design analogies over engineering jargon. No code is written yet; we're in foundations-first mode.

## Current status

**Audit phase.** Diagnosing why the existing campaign produced no bookings.

## Hard facts about this account

| Thing | Value |
|---|---|
| Studio location | Valencia old city, Spain |
| Customers | Russian-speaking + Ukrainian-speaking, primarily Valencia residents |
| Conversion goal | Workshop / class booking (with payment) |
| Spend so far | €65 Meta ads (3 ads) + €60 Telegram sponsored post = €125 total, zero bookings |
| Remaining this month | €150 |
| Telegram channel | One-off, not in scope for automation |
| Website | Outdated; will build a new minimal landing page |
| Account scale | Small — too small for statistical A/B testing yet |

## The plan in one sentence

**Audit → fix foundations (landing page + tracking + offer) → run one well-structured campaign → review weekly → iterate. Automate later, only when there's volume worth automating.**

## What we are NOT doing (yet)

- Python pipelines, data warehouses, scheduled jobs — premature at this spend level.
- A/B testing — at <€300/month total spend split across two language segments, statistical significance is unreachable. We'll do *creative iteration* (judgment-based) instead.
- Conversions API Gateway, MMM, Robyn, Madgicx — far overkill.
- Combining Russian + Ukrainian audiences into one ad set — separate ad sets with localized creative is mandatory.

## Strategic constraints

- **RU and UA audiences get separate ad sets and creative.** Same offer, same landing page (with language toggle), but each language has its own ad copy, voice, and where appropriate, separate visuals. This is partly statistical (we want to see which segment converts) and partly ethical/respectful given war-displacement context.
- **Tracking-first.** Without Meta Pixel + Conversions API installed correctly, Meta is optimizing blind and the "no results" outcome is almost guaranteed. Step one of any fix is making sure conversions are being tracked.
- **One conversion event matters.** "Workshop booking confirmed" (form submit + payment). Everything else is a leading indicator, not the goal.
- **GDPR + DSA** apply (Spain = EU). The landing page needs a real consent banner before tracking fires.

## Tech stack (final decisions for this scale)

- **Landing page**: Framer or Webflow or Carrd. Single page, two language versions. Free/cheap tier.
- **Booking**: Calendly, Cal.com, or Tally form → Stripe link. (Skip building auth/CMS.)
- **Tracking**: Meta Pixel (browser) + Meta Conversions API one-click setup (server-side mirror).
- **Consent**: Cookiebot free tier or a hand-rolled banner — must block tracking until consent.
- **Reporting**: Manual review in Meta Ads Manager for the first 4 weeks. Optional weekly summary via a Google Sheet or simple Python script later.
- **Automation**: Deferred until there's enough data to automate against (60–90 days of clean tracked data, minimum).

## Key external references

- Meta Marketing API docs: https://developers.facebook.com/docs/marketing-apis
- Meta Pixel + CAPI guide: https://developers.facebook.com/docs/marketing-api/conversions-api/
- Meta Events Manager (where Pixel lives): https://business.facebook.com/events_manager2
- Meta Ads Manager (where campaigns live): https://adsmanager.facebook.com/

## File map

- `CLAUDE.md` — this file. Project context.
- `PLAN.md` — phased small-business roadmap (current scope).
- `AUDIT.md` — findings from the Phase 0 audit (filled in as we go).
- `research.md` — broader research reference (May 2026) — kept for later, not directly relevant to Phase 0–2.

## Working preferences for Claude

- Diana is a UX designer. Use plain language and design analogies; explain technical concepts in terms of patterns she already knows (browser cookies, design tokens, prototype testing).
- Walk through each step; don't batch big decisions.
- Don't recommend tooling beyond what's justified by the current spend level.
- Always reference the relevant Meta deadline if architecture choices touch Advantage+, Audience Insights, or compliance.
- Russian + Ukrainian audience separation is non-negotiable — never propose merging the ad sets to "increase sample size."
