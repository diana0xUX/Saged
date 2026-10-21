# Saged.club — Website Overview
_Last updated: September 2026. Based on sitemap.md, ia-redesign.md, and README.md._

---

## What the website is

A multilingual landing site for **Saged.club** — a ceramic and cultural workshop space in Valencia old city. Built in plain HTML/CSS/JS, hosted on GitHub Pages, deployed by pushing to `main`.

**Live site:** https://saged.club

---

## Current page structure

```
saged.club/
│
├── / (Russian)              Home
├── /studio/                 Ceramics with Koritsia — main booking page
├── /kids/                   Kids ceramics
├── /events/                 Events listing
├── /coworking/              Studio coworking / hot desk
├── /gifts/                  Gift certificates
├── /private/                Private events
│
├── /ua/ (Ukrainian mirror)  Full copy of all RU pages in Ukrainian
│
├── /uk/ → /ua/              Old redirect stubs — keep, don't delete
│
└── /en/ (English)           ⚠️ INCOMPLETE
    ├── /en/kids/            ✅ exists
    ├── /en/coworking/       ✅ exists
    ├── /en/                 ❌ missing — no English home
    └── /en/studio/          ❌ missing — no English ceramics page
```

---

## What's missing (priority order)

| # | What | Why it matters |
|---|---|---|
| 1 | `/en/studio/` | The best-performing ad campaign sends English speakers here — page doesn't exist |
| 2 | `/en/` | English home — entry point for EN audience |
| 3 | Cal.com inline on `/studio/` | Booking CTA is buried at the bottom — needs to appear earlier |
| 4 | Event prices on home page | Events block shows events but not prices |
| 5 | Group booking info in FAQ | No answer to "can I come with a friend?" |

---

## Languages

| Path | Language | Status |
|---|---|---|
| `/` | Russian | ✅ Live |
| `/ua/` | Ukrainian | ✅ Live (full mirror of RU) |
| `/uk/` | — | Redirects to `/ua/` — keep as-is |
| `/en/` | English | ⚠️ Partially built |

**Rule:** every change to RU pages must be mirrored in UA pages. Same sections, same structure.

---

## Navigation (current vs. planned)

**Current:**
```
Logo · Взрослым · Детям · Коворкинг · Events · Подарки · Приватно · [RU | UA]
```
Problems: "Events" in English breaks consistency. "Коворкинг" shouldn't be in primary nav.

**Planned:**
```
Logo · Студия · Детям · События · Подарки · [RU | UA | EN]
```
Coworking and Private move to footer. Language switcher adds EN.

---

## Key design rules

- **Price is never hidden** — €60 shown in hero, not buried
- **Booking CTA appears 3 times** on studio page: hero, after what's included, and at the booking section
- **WhatsApp and direct pay are equal weight** — DM is how this audience actually books
- **Koritsia's name and photo** appear on every page that mentions ceramics
- **Contact at top and bottom** — WhatsApp number in both header area and footer

---

## Known issues

**⚠️ WhatsApp number conflict** — two different numbers appear across the site: `+34 695 XX XX XX` and `+34 605 54 33 00`. One number must be chosen and applied consistently everywhere.

---

## Tech

- No build step — edit HTML, commit, push to `main`, site updates automatically
- Fonts: Saged Cyrillic (Cyrillic display) + Costa Light (Latin display) + Inter (body/UI). Self-hosted from `assets/fonts/`. No Cormorant Garamond, no Summer Font.
- Colors: clay neutrals, terracotta, sage — defined as CSS variables in `assets/style.css`
- Booking: WhatsApp DM (live) + Cal.com with Stripe (planned)
- Tracking: Meta Pixel, gated by EU cookie consent banner

---

## Conflicts found between documents

| Conflict | Detail |
|---|---|
| README is outdated | README shows only `index.html` and `uk/index.html` — misses studio/, kids/, events/, coworking/, gifts/, private/, ua/, en/ |
| README says `/uk/` is Ukrainian landing | Wrong — `/uk/` are redirects. `/ua/` is the canonical Ukrainian path |
| README references `PLAN.md` | That file no longer exists — replaced by `REPORT.md` and `CHRONICLE.md` |
| README says "once DNS is pointed" | DNS is live — saged.club is the active domain |

**Sitemap and IA redesign are fully aligned** — no conflicts between those two.

---

## What to build next (agreed priority)

1. `/en/studio/` — English ceramics page with "TAUGHT IN ENGLISH" badge, price in hero, WhatsApp booking
2. `/en/` — English home, routes to ceramics and events
3. Update README to reflect current reality
