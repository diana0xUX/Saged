# Saged.club — Website Strategy
### Business · Design · Marketing

_September 2026 — working document for Diana and the team_

---

## What we're building and why

**Saged.club** is a ceramic and cultural workshop space in Valencia old city. The website has one job: turn strangers who find us (via Instagram, ads, or word of mouth) into paying customers who show up to the studio.

We are not trying to be everything. The website is a booking machine, not a magazine.

**Break-even target:** €1,935/month. Best month so far: €1,123 (June 2026). The gap is closed by filling more ceramics slots and kids classes — not by adding more pages.

---

## Our customers — who they are and what they need

### Persona 1 — The Russian or Ukrainian speaker
> *"I moved to Valencia and I'm looking for something that feels like home — a place with people like me, something to do with my hands."*

- Arrived post-2022 in many cases. Socially isolated, looking for community.
- Discovers us via Instagram, Telegram groups, or word of mouth.
- Books via WhatsApp — never via a checkout form on first visit.
- Speaks: Russian or Ukrainian (treat as separate — never lump together).

**What the website must do for them:**
Immediately feel warm and familiar. Show the instructor's face and name. Make WhatsApp the easiest path.

---

### Persona 2 — The English-speaking expat or digital nomad
> *"I want to try ceramics while I'm living in Valencia. I googled it and found you — but is the class actually in English?"*

- Discovered via Meta ads or Google search.
- Skeptical. Needs to see "TAUGHT IN ENGLISH" within 3 seconds or they leave.
- More likely to book online (Cal.com/Stripe) than to DM first.
- Currently: **we have no English ceramics page. This is our biggest gap.**

**What the website must do for them:**
A dedicated English page (`/en/studio/`) that makes the language question irrelevant in the first sentence.

---

### Persona 3 — The parent
> *"My child is 8 years old and I'm looking for an after-school activity that isn't a screen."*

- Finds us via Instagram or parent WhatsApp groups.
- Needs: clear age groups, schedule, price, and what the child actually makes.
- Wants to know if it's safe and supervised.
- Decides fast — if the page doesn't answer the basics, she messages someone else.

**What the website must do for them:**
A dedicated kids page with age groups, days, times, price, and a WhatsApp button that pre-fills a message so she doesn't have to think.

---

### Persona 4 — The gift buyer
> *"Her birthday is in two weeks and I want to give her something she'd actually remember."*

- Often comes from someone who attended and loved it.
- Not looking for information — looking for a fast purchase with minimal friction.
- Price sensitivity: low (it's a gift).

**What the website must do for them:**
A gift certificate page that explains what's included and has one clear button to buy or enquire.

---

### Persona 5 — The working ceramicist
> *"I need studio access and a kiln. I don't want to teach — I just want to make my own work."*

- Small audience but high-value: €200/month recurring.
- Comes from ceramics community word of mouth.
- Needs to know: can I fire my own work? what are the rules? how do I start?

**What the website must do for them:**
A coworking page that answers the practical questions and makes the intro course pathway clear.

---

## Business objectives — ranked by revenue impact

| # | Objective | How website supports it |
|---|---|---|
| 1 | Fill adult ceramics slots (Thu 3×/day, 6 people/slot) | `/studio/` and `/en/studio/` convert visitors into WhatsApp/Cal.com bookings |
| 2 | Fill kids classes (Wed+Fri solo, Thu+Sat+Sun parent+child) | `/kids/` drives WhatsApp enquiries from parents |
| 3 | Sell gift certificates | `/gifts/` is fast and frictionless |
| 4 | Fill coworking spots (5 total, €200/month each) | `/coworking/` explains the offer and intake path |
| 5 | Drive event attendance (tea club, workshops, ceremonies) | `/events/` lists what's coming with prices and booking |
| 6 | Build community (retention + word of mouth) | Every page has social links; events foster return visits |

---

## Website structure

### The pages we have — and what each one does

---

**`/` — Home (Russian)**
**`/ua/` — Home (Ukrainian mirror)**

_Role: Orient. Route. Don't try to sell everything._

Every visitor lands here first. In 5 seconds they need to know:
- This is a ceramics studio in Valencia
- It feels warm and human
- Here's where to go next

CTA hierarchy:
1. Ceramics → `/studio/`
2. Upcoming events → `/events/`
3. Kids → `/kids/`

What's NOT the homepage's job: closing the sale. The homepage routes people. The studio page sells.

---

**`/studio/` — Adult ceramics (Russian)**
**`/ua/studio/` — Ukrainian mirror**

_Role: Convert. This is the most important page on the site._

The visitor already knows they want ceramics. The page needs to remove every doubt and make booking feel easy.

Content flow (in this order):
1. What it is + price in the first sentence (€60, 2 sessions, everything included)
2. How it works (3 steps: shape → glaze → take home)
3. Who teaches it (Koritsia — face, name, bio)
4. What's included (no hidden costs)
5. **Booking CTA** — appears here, not just at the bottom
6. Schedule (every Thursday, 3 time slots)
7. Gallery (what the experience looks like)
8. Testimonials (real quotes only)
9. FAQ (9 common questions)
10. Map + address

Booking paths (equal weight — both matter):
- WhatsApp: pre-filled message, one tap on mobile
- Cal.com: online booking with Stripe payment

---

**`/en/studio/` — English ceramics page**
**`/en/` — English home**

_Role: Serve the English-speaking audience. Currently missing. This is our biggest gap._

The English ad campaign is running. People click, arrive, and find no English page. This is costing us bookings every day.

`/en/studio/` must do one thing above all else: answer "is this actually in English?" in the first sentence.

Hero copy: *"Ceramics with Koritsia — taught in English. Every Thursday, old city Valencia. €60 · 2 sessions · everything included."*

Badge in the hero: **TAUGHT IN ENGLISH** — large, impossible to miss.

---

**`/kids/` — Kids ceramics (Russian)**
**`/ua/kids/` — Ukrainian mirror**
**`/en/kids/` — English (exists)**

_Role: Answer the parent's questions and get her to WhatsApp._

Three questions every parent has:
1. What age? (7–14 solo / 4.5–7 with parent)
2. When and how much? (Wed+Fri 16:30 / €25 solo · Thu+Sat+Sun / €50 parent+child)
3. What does the child make? (one subject per session — a mug, an animal, etc.)

WhatsApp pre-fill for this page:
*"Привет! Хочу записать ребёнка [имя, возраст] на керамику. Свободные места?"*

---

**`/events/` — Events listing**
**`/ua/events/`, `/en/events/`**

_Role: Show what's coming. Drive one-off attendance. Build community._

Each event listed with: name, date, time, price, and a booking button.
Past events marked as completed (cannot be booked).

Current September events:
- 27 Sep — Tea Club with Helena, €15
- Ring workshop (TBD) — blocked
- Vase workshop (TBD) — blocked
- Big Mother workshop (TBD) — blocked

Rule: events are never paid-promoted. Organic only — Instagram + Telegram.

---

**`/gifts/` — Gift certificates**
**`/ua/gifts/`**

_Role: Make the gift purchase feel easy and special._

One certificate covers one full ceramics course (€60 / 2 sessions).
Buyer pays → recipient books their own Thursday.

Page needs: what's included, price, how it works, and a buy/enquire button.

---

**`/coworking/` — Studio access**
**`/ua/coworking/`, `/en/coworking/`**

_Role: Attract working ceramicists. Secondary audience, high recurring value._

€200/month, 5 spots, daily 10:00–22:00.
Intro course (€120 / 4 classes) is the entry path for newcomers.

This page is NOT in primary navigation — it's in the footer. Not our main audience.

---

**`/private/` — Private events**
**`/ua/private/`**

_Role: Capture enquiries for birthdays, team events, private groups._

Footer only. Enquiry by DM.

---

**`/es/` — Spanish home**

_Role: Serve Spanish-speaking locals. Exists as of September 2026._

---

### Pages we still need to build

| Page | Priority | Reason |
|---|---|---|
| `/en/studio/` | 🔴 Critical | Paid EN campaign sends traffic here. Page doesn't exist. |
| `/en/` | 🔴 Critical | No English entry point |

---

## Navigation

### What visitors see (Russian)
```
Студия · Детям · События · Подарки   [RU · UA · EN]
```

### What visitors see (English)
```
Ceramics · Kids · Events · Gifts   [EN · RU · UA]
```

**Not in the main nav** (footer only):
- Coworking
- Private events

**Why:** These are secondary offers for specific audiences. Putting them in the nav alongside ceramics confuses the primary message.

---

## Content rules — non-negotiable

**1. Every Russian page has a Ukrainian mirror.**
Same sections, same structure, same number of items. Any structural difference between `/` and `/ua/` is a bug.

**2. Price is never hidden.**
€60 is in the hero, in the booking section, and in the FAQ. Nobody should have to dig.

**3. Testimonials are real.**
Only real quotes from real people (Google reviews, DMs, Instagram comments). No placeholder text pretending to be a review.

**4. One WhatsApp number everywhere.**
`+34 605 54 33 00` — this is the correct number. No other number should appear on the site.

**5. Koritsia's name and face appear on every ceramics page.**
She is the product. Her face builds trust faster than any copy.

**6. Booking CTA appears at least 3 times on the studio page.**
In the hero, after "what's included", and in the booking section.

---

## How bookings actually happen

Based on everything we know from real bookings so far:

1. Person sees an Instagram post or ad
2. They visit the website (or go directly to Instagram)
3. They send a WhatsApp message (not a checkout — a message)
4. Diana or Koritsia responds, confirms the slot, sends a Stripe payment link
5. Customer pays, booking confirmed

**The website's job in this flow:** make step 3 as easy as possible. One tap. Pre-filled message. No form to fill out.

Cal.com (online booking without a DM) works too — especially for English speakers. Both paths must be equally visible.

---

## What to build next

In this order:

1. **`/en/studio/`** — English ceramics page. One page, all content in English, "TAUGHT IN ENGLISH" in the hero.
2. **`/en/`** — English home. Simple, routes to ceramics and events.
3. **Fix the WhatsApp number** — audit every page, make it `+34 605 54 33 00` everywhere.
4. **Add Cal.com inline on `/studio/`** — booking widget in the schedule section, not just a link at the bottom.
5. **Add event prices to home page** — the events block on the home page should show prices.

---

_This document is the single source of truth for website decisions. Update it when strategy changes — don't let it go stale._
_Cross-reference: `KNOWLEDGE.md` (business facts), `docs/sitemap.md` (page structure), `docs/ia-redesign.md` (content blocks)_
