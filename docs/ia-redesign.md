# Information Architecture — Saged.club Redesign
**Date:** 2026-08-29
**Purpose:** User scenarios, content blocks per page, redesign specification

---

## User scenarios

### Provided by Diana
1. I want to understand what the studio offers
2. I want to know how to find it
3. I want to contact the studio
4. I want to book and pay online
5. I want to know who my instructor is
6. I want to see the schedule
7. I want to understand what I can make

### Additional scenarios (suggested)
8. I'm an English speaker — is this for me too?
9. I want to give this as a gift
10. I've never done ceramics — am I good enough?
11. I want to try it once before committing
12. I want to bring a friend and come together
13. I want to bring my child
14. I'm a working ceramicist and need studio access
15. I want to host a private celebration or team event
16. I want to attend a cultural event (not ceramics)
17. I'm new to Valencia and want to meet people
18. I saw the ad on Instagram — is this legit?
19. I missed the first session — can I still come?
20. I want to know the cancellation/refund policy
21. I want to see what other people have made
22. I want to follow the studio on social media

---

## Scenario → page mapping

| Scenario | Primary page | Currently answered? |
|---|---|---|
| Understand what studio offers | `/index.html`, `/studio/` | Partially — home page too vague |
| Find the studio | `/studio/` (map + address) | Yes — buried in bottom third |
| Contact the studio | `/studio/` (booking section) | Yes — but too far down |
| Book and pay online | `/studio/` (Cal.com link) | Yes — but buried |
| Know the instructor | `/studio/` (Koritsia section) | Yes — well done |
| See the schedule | `/studio/` (schedule section) | Partially — no live availability |
| Understand what I can make | `/studio/` body copy | Partially — gallery helps |
| English speaker — is this for me? | **No page** | ❌ Missing |
| Gift certificate | `/gifts/` | Yes |
| Never done ceramics — am I good enough? | `/studio/` FAQ | Yes |
| Try once before committing | Not addressed | ❌ Missing (gift cert could serve this) |
| Come with a friend | Not addressed | ❌ Missing |
| Bring my child | `/kids/` | Yes |
| Ceramicist needing workspace | `/coworking/` | Yes |
| Private event | `/private/` | Yes |
| Cultural event (not ceramics) | `/events/` | Yes |
| New to Valencia, meet people | `/index.html` about section | Partially |
| Is this legit? | Testimonials + Google link | Yes |
| Missed a session | `/studio/` FAQ | Yes |
| Cancellation policy | `/studio/` FAQ | Yes |
| See what others made | `/studio/` gallery | Partially |
| Follow on social | Footer + Instagram embed | Yes |

---

## Content blocks — by page

---

### Home page `/index.html` (and `/ua/index.html` mirror)

**Objective:** Orient new visitors in 5 seconds. Route them to the right sub-page.

```
BLOCK 1 — Hero
  Content:  Studio name · one-line position statement · hero image/video
  CTA:      Primary → "Записаться на керамику" (→ /studio/)
            Secondary → "Ближайшие события" (→ /events/)
  Image:    workshop-teaching.jpg or hero-1.jpg

BLOCK 2 — Proof strip (trust signals, no CTA)
  Content:  3 items horizontal:
            "50+ участников с мая 2026"
            "Группы до 6 человек"
            "Старая Валенсия · C/ de les Cuines, 8"

BLOCK 3 — Primary offering card (Ceramics)
  Content:  Label: "Керамическая студия"
            Headline: "Каждый четверг — за столом с глиной"
            Body: 2 sentences max — what you do, what you take home
            Price: €60 · 2 встречи · всё включено
            Instructor: "С Корицей" + photo thumbnail
  CTA:      "Узнать о курсе →" (→ /studio/)

BLOCK 4 — Secondary offering card (Events)
  Content:  Label: "События"
            Headline: "Собираем хороших людей"
            Body: upcoming events list (3 items max, with date + price)
  CTA:      "Смотреть события →" (→ /events/)

BLOCK 5 — Kids card (if space)
  Content:  "Детская керамика · €25 · 1.5 часа"
  CTA:      "→ Детям"

BLOCK 6 — About / Why we exist
  Content:  2 paragraphs — origin story, community angle
            Sign-off line

BLOCK 7 — Testimonials
  Content:  2–3 quotes with name, source, star rating

BLOCK 8 — Find us (map + contact)
  Content:  Address · Google Maps embed · WhatsApp · Instagram
  Note:     This block answers "how do I find it" and "how do I contact"

FOOTER
  Content:  Full address · WhatsApp · email · Instagram
            Links: Studio · Kids · Events · Coworking · Gifts · Private
            Legal: Privacy · Cookies
```

---

### Studio page `/studio/index.html` (and `/ua/studio/`)

**Objective:** Convert a curious visitor into a booking. Every section should move toward that outcome.

```
BLOCK 1 — Hero
  Content:  Photo/video carousel (existing: video + 3 photos)
            Eyebrow: "Каждый четверг · Старая Валенсия"
            H1: "Керамика с Корицей"
            Lead: what you do + what you take home (2 sentences)
            Price callout: "60 € · две встречи · всё включено"
  CTA:      "Выбрать дату" (anchor → #book)

BLOCK 2 — 3-step process
  Content:  Встреча 1 — лепка (2 hours, hands in clay)
            Встреча 2 — глазурь (glazing, colour choice)
            Что заберёте (your piece, fired, glazed, 2 weeks later)

BLOCK 3 — Instructor
  Content:  Photo of Koritsia
            Name, short bio (3–4 sentences)
            Language: Ukrainian / Russian
            Instagram link: @korytsia_studio

BLOCK 4 — What's included
  Content:  7-item list (as current)
  CTA:      [ADD] Booking CTA button here — "Забронировать место" (→ #book)
            This is the earliest logical booking moment after all key info is presented.

BLOCK 5 — Schedule
  Content:  Days: Thursday + Thursday (two consecutive)
            3 time slots: 12:00, 15:00, 19:00
            Any Thursday start
  [ADD]     Live availability: embed Cal.com inline or link "Проверить даты →"

BLOCK 6 — Gallery (how it feels)
  Content:  4 photos — hands working, group atmosphere, finished pieces
            Caption: "Маленькая группа, тёплый свет, ваши руки в глине."

BLOCK 7 — Testimonials
  Content:  3 quotes, each linked to Google review

BLOCK 8 — Instagram embed
  Content:  2 posts (existing)
  CTA:      "Подписаться → @saged.club"

BLOCK 9 — Booking  id="book"
  Content:  H2: "Забронировать место"
            Lead: "Не уверены? Напишите..."
            Path A: WhatsApp (pre-filled message — keep existing wa.me deep link)
            Path B: Cal.com / Stripe (online payment)
            Other channels: Instagram, email
  Note:     Both paths stay equal weight — DM is how this audience books

BLOCK 10 — FAQ
  Content:  9 questions (as current — they're correct)
  [ADD]     "Можно ли прийти вдвоём?" (group booking scenario)
  [ADD]     "Есть ли сертификаты в подарок?" (link to /gifts/)

BLOCK 11 — Map + address
  Content:  Google Maps embed
            Full address, "Open in Google Maps →"

FOOTER (same as all pages)
```

---

### English ceramics page `/en/studio/` [NEW — to be built]

**Objective:** Convert English-speaking expats arriving from Meta ads into WhatsApp bookings. This is the missing landing page for the best-performing ad campaign.

```
BLOCK 1 — Hero
  Eyebrow:  "Every Thursday · Old City · Valencia"
  H1:       "Ceramics with Koritsia"
  Lead:     "A 2-day pottery class in English. Small group. All materials. Take your piece home."
  Badge:    "TAUGHT IN ENGLISH" — prominent, can't be missed
  Price:    "€60 · 2 sessions · everything included"
  CTA:      "Check availability" (→ Cal.com) OR "Message us" (→ WhatsApp)
  Image:    workshop-teaching.jpg

BLOCK 2 — 3-step process
  Session 1 — shape (hand-build your piece, 2 hours)
  Session 2 — glaze (colour, decoration, finish)
  Take home (fired, glazed, yours — 2 weeks after session 2)

BLOCK 3 — Instructor
  Photo of Koritsia
  "Koritsia is a Ukrainian ceramic artist based in Valencia. She teaches in English, Russian, and Ukrainian."
  Group size: up to 6 — "she knows your name by the end of the first session"

BLOCK 4 — What's included
  €60 covers: 2 sessions (2h each) · clay (~1kg) · all tools · glaze · 
              both firings (bisque + glaze) · tea and water · your finished piece

BLOCK 5 — Schedule
  Every Thursday · 3 slots: 12:00 / 15:00 / 19:00
  "Start any Thursday — book two consecutive Thursdays"
  Link to Cal.com for live availability

BLOCK 6 — Gallery
  4 photos showing the experience

BLOCK 7 — Testimonials
  English-language quotes from participants

BLOCK 8 — Booking  id="book"
  H2:       "Book your spot"
  Path A:   WhatsApp +34 605 54 33 00 (pre-filled: "Hi, I'd like to book ceramics with Koritsia...")
  Path B:   Cal.com / Stripe online payment

BLOCK 9 — FAQ (in English)
  Do I need experience? (No)
  Why 2 sessions? (clay needs a week to dry + fire)
  Can I start any Thursday? (Yes)
  What should I wear? (Something you don't mind getting dirty)
  When do I get my piece? (2 weeks after session 2)
  Is it really in English? (Yes — Koritsia teaches in English, Russian, and Ukrainian)

BLOCK 10 — Map
  Google Maps embed + address + "Open in Google Maps →"

FOOTER
  Address · WhatsApp · Instagram @saged.club
  Language links: EN · RU · UA
```

---

### English home page `/en/` [NEW — to be built]

**Objective:** One-page English landing. Orient EN-speaking visitors. Route to ceramics or events.

```
BLOCK 1 — Hero
  H1:       "A studio where you make things with your hands"
  Lead:     "Ceramics classes, cultural events, and a small community in the old city of Valencia."
  CTA:      "Join a ceramics class →" (→ /en/studio/)

BLOCK 2 — What's here
  3 cards:
  - Ceramics: "Every Thursday with Koritsia · €60 · taught in English"
  - Events: "Sound healing, breathwork, tea ceremonies, slow friending"
  - For potters: "Hot desk & studio access"

BLOCK 3 — Find us
  Address · WhatsApp · Instagram · Google Maps

FOOTER
```

---

## Information hierarchy per user scenario

### Scenario: "I want to book and pay online" — optimal path
```
Ad → /en/studio/ → see price in hero → scroll to BLOCK 4 → click Cal.com → Stripe payment
                 → OR: see WhatsApp in hero → tap → send message → Diana sends Cal.com link
```
Current friction: Cal.com link is only at the bottom of the page. Fix: add to hero block.

### Scenario: "I want to understand what I can make"
```
/studio/ BLOCK 1 (lead copy: "забрать домой свою керамику")
       → BLOCK 2 (3-step: shape → glaze → take home)
       → BLOCK 6 (gallery: finished pieces)
```
Currently answered, but gallery should show more finished pieces, not just process shots.

### Scenario: "I'm an English speaker — is this for me too?"
```
Currently: NO ANSWER — /en/ doesn't exist.
Fix: /en/studio/ hero with "TAUGHT IN ENGLISH" badge answers this in 2 seconds.
```

### Scenario: "I want to give this as a gift"
```
/studio/ BLOCK 4 → gift promo block → /gifts/
Cross-link should also appear in the booking block: "Want to give this as a gift? →"
```

### Scenario: "I'm new to Valencia and want to meet people"
```
/index.html BLOCK 6 (about) → /events/
The community angle is currently undersold. The about section should more explicitly 
name this: "a place for people who've just arrived and are looking for theirs."
```

### Scenario: "I want to come with a friend"
```
Not currently addressed. Add to FAQ: "Can I book for two?"
Answer: "Yes — book two spots on the same Thursday. WhatsApp us and we'll confirm 
both spots together."
```

---

## Content gaps to fill

| Gap | Where it belongs | Priority |
|---|---|---|
| English ceramics page | `/en/studio/` | 🔴 Critical |
| English home page | `/en/` | 🔴 Critical |
| Group booking info | Studio page FAQ | 🟠 High |
| Event prices on home page | Home page events block | 🟠 High |
| Inline Cal.com widget | Studio page BLOCK 5 | 🟠 High |
| More finished-piece photos | Studio gallery | 🟡 Medium |
| English testimonials | `/en/studio/` | 🟡 Medium |
| "Come with a friend" copy | Studio page FAQ | 🟡 Medium |
| Gift certificate cross-link in booking block | Studio page BLOCK 9 | 🟡 Medium |
| Koritsia's own Instagram link | Studio instructor block | 🟢 Low |

---

## Redesign principles (for the designer)

1. **Ceramics first.** Every page's primary CTA points toward ceramics booking. Events are secondary. Coworking is tertiary.

2. **Book early, book often.** Booking CTAs should appear: in the hero, after "what's included", and in the dedicated booking section. Three opportunities minimum on any product page.

3. **One WhatsApp number everywhere.** Resolve the 695 vs 605 conflict and apply consistently.

4. **English section is a first-class citizen.** `/en/` should have the same quality and depth as `/` and `/ua/`. It's the paid acquisition channel — it can't be an afterthought.

5. **Price is never hidden.** Price in the hero, price in the nav or eyebrow, price in the booking section. €60 is fair — never make someone dig for it.

6. **The instructor is the trust signal.** Koritsia's name, face, and bio should appear on every page that mentions ceramics — including the home page.

7. **Contact at the top and bottom.** WhatsApp number in both header area (or sticky bar) and footer. Don't make mobile users scroll to the bottom to find the number.

---

_Last updated: 2026-08-29_
_Cross-reference: `docs/ux-audit.md`, `docs/sitemap.md`, `creative/SAGED-SOURCE-OF-TRUTH.md`_
