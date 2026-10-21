# UX Audit — Saged.club
**Date:** 2026-08-29
**Auditor:** Fergie (AI agent)
**Method:** Full HTML read of all live pages + cross-reference with SAGED-SOURCE-OF-TRUTH.md and analytics data

---

## Executive summary

The studio page (`/studio/`) is well-built — it answers every user question in the right order and has both DM and online booking paths. The home page and English section are where the biggest gaps are. The most critical issue is a missing English landing page: the best-performing ad in the studio's history (5.17% CTR) sends English-speaking traffic to a dead end.

**Severity key:** 🔴 Critical · 🟠 High · 🟡 Medium · 🟢 Low

---

## Critical issues (fix before next ad spend)

### 🔴 No English landing page — `/en/` returns 404
The English ceramics ad campaign (the studio's best-performing ad, CTR 5.17%, CPC €0.01) has no destination. `/en/index.html` does not exist. Someone clicking the ad in English arrives at either the Russian homepage or a 404, depending on where the ad links. This is the highest-priority fix in the project.

**What exists:** `/en/kids/` and `/en/coworking/` subpages only.
**What's missing:** `/en/` (English home or landing) and `/en/studio/` (English ceramics class page).
**Impact:** Every euro spent on the EN ceramics campaign has an impaired landing experience.

### 🔴 No English ceramics page — `/en/studio/` missing
The primary English audience (expats, arriving via paid ads) has no page that says "ceramics class, in English, €60, every Thursday, book here." The studio page (`/studio/`) is Russian-only.

---

## High priority issues

### 🟠 Home page primary CTA goes to Events, not Ceramics
The main call-to-action on the Russian home page (`/index.html`) is:
```
<a href="events/" class="home-hero__cta">Ближайшие события →</a>
```
Events are the secondary offering. Ceramics with Koritsia is the primary revenue source (~57% of income). The primary CTA should direct users to the ceramics booking page, not events.

### 🟠 Booking section is buried at the bottom of the studio page
The booking form (`#book`) is the 9th section from the top on `/studio/`. A user who is ready to book after reading the hero section has to scroll through: 3-step process, instructor bio, gift promo, photo gallery, what's included, schedule, gallery, testimonials, Instagram embeds — before reaching the book button. There should be a booking anchor CTA immediately after the "What's included in €60" section (or a sticky CTA on mobile).

### 🟠 WhatsApp number inconsistency
- `SAGED-SOURCE-OF-TRUTH.md` lists: `+34 695 73 19 00`
- Website (`/studio/`, `/index.html`, etc.) uses: `+34 605 54 33 00`

These are different numbers. The KNOWLEDGE.md notes a known conflict (bot vs. Diana's personal WhatsApp). Needs resolution — one canonical number across all surfaces.

### 🟠 Nav mixes languages
Russian nav includes "Events" in English and "Приватно" in Russian. Inconsistent. User whose language is Russian should see all items in Russian.

### 🟠 No schedule widget — users can't see real availability
The `/studio/` page shows the schedule structure (Thursday, 3 slots: 12:00, 15:00, 19:00) but no live availability. A user who wants to book a specific Thursday has to DM to ask if it's available, then get sent a Cal.com link. The Cal.com widget should be embedded inline, or at minimum, there should be a "check availability" link that goes directly to the Cal.com booking page.

---

## Medium priority issues

### 🟡 Address inconsistency between source of truth and site
- `SAGED-SOURCE-OF-TRUTH.md`: `C/ de la Correu, 8`
- Website HTML + schema.org: `C/ de les Cuines, 8`

These may be the same street with different transliterations, or different streets. Needs verification. Google Maps embed and schema.org LocalBusiness use `C/ de les Cuines, 8` — if that's wrong, it affects search discoverability.

### 🟡 Coworking in primary nav dilutes focus
The primary nav includes Коворкинг (Coworking), which targets a completely different audience (professional potters wanting studio access). It occupies the same weight as Детям (Kids) and Студия (Adults), which are the studio's revenue-generating offerings. Coworking should be deprioritised — footer link or a secondary nav tier.

### 🟡 No price visible on Events page from home
The home page events section lists event names but no prices. A user browsing events can't tell if they're free, €5, or €50 without clicking through. Price transparency reduces drop-off.

### 🟡 Gallery images lack descriptive alt text quality
Several gallery images use alt text that describes the scene ("Свечи и лён на столе") rather than the experience ("Занятие с Корицей — первая встреча с глиной"). Alt text is both accessibility and SEO.

### 🟡 Testimonials are too short and not linked to verifiable source
"Уютное место, приятная атмосфера, чудесные люди." — this is generic and could apply to any cafe. Testimonials should mention the specific experience (what they made, how it felt), and link to the Google review for trust.

### 🟡 No back-navigation from studio/ to home
The studio page header shows "Взрослым" as the current page marker (no link), but there's no explicit breadcrumb or home link beyond the logo. Mobile users navigating back rely entirely on browser back button.

---

## Low priority issues

### 🟢 Schema.org instructor sameAs links to @saged.club, not Koritsia's own profile
The Course schema has `"sameAs": "https://instagram.com/saged.club"` for the instructor. Koritsia has her own Instagram — `@korytsia_studio`. This should point to the instructor's profile, not the studio's.

### 🟢 `kids summer` images not served from the site
The kids summer programme PNG files (eng/esp/ukr) were sitting loose in the project root. Now moved to `creative/library/04-social/`. If they were ever embedded in a page, those image hrefs need updating.

### 🟢 Private page linked from nav without explanation
`/private/` appears in the nav but the page has no visible explanation of what "private" means in this context until you visit it. A tooltip or subtitle ("Private events") would help.

### 🟢 Footer address format inconsistent with address in body
Body text uses: "C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia"
Footer should match exactly, including postcode and city.

### 🟢 No canonical URL on index.html `<meta property="og:url">`
The home page OG tag says `"https://saged.club/"` which is correct, but the studio page OG tag has both `og:url` and a separate `link rel="canonical"` — inconsistency across pages.

---

## What's working well (don't break)

- **Studio page content structure** — hero → what you learn → instructor → includes → schedule → gallery → testimonials → book → FAQ is the right order and covers every user question.
- **Dual booking paths** — WhatsApp DM + Cal.com/Stripe side by side, with the DM option clearly not marked as "lesser" than online booking. This matches how the RU/UA audience actually books.
- **WhatsApp pre-filled message** — the `wa.me` deep link includes pre-filled text (name, date, slot) which reduces friction dramatically. Keep and extend to all booking CTAs.
- **FAQ section** — 9 questions, covers the actual questions people ask. "Can I start any Thursday?" and "What should I wear?" are exactly right.
- **Consent-gated Pixel** — GDPR compliant. Do not remove.
- **Schema.org markup** — LocalBusiness, Course, Event structured data gives search visibility. Well-implemented.
- **Plausible + Meta Pixel dual analytics** — privacy-respecting analytics without compromising Meta event tracking.

---

## Pages audited

| Page | Status | Main issue |
|---|---|---|
| `/index.html` | Exists | CTA points to events not ceramics |
| `/studio/index.html` | Exists, good | Booking buried, no inline calendar |
| `/kids/index.html` | Exists | Not reviewed in detail |
| `/events/index.html` | Exists | No prices shown |
| `/coworking/index.html` | Exists | Wrong audience in primary nav |
| `/gifts/index.html` | Exists | Not reviewed in detail |
| `/ua/index.html` | Exists | Mirror of RU |
| `/en/index.html` | **MISSING** | Critical gap |
| `/en/studio/index.html` | **MISSING** | Critical gap |

---

_Last updated: 2026-08-29_
