# Sitemap — Saged.club
**Date:** 2026-08-29
**Status:** Current state + proposed changes

---

## Current sitemap (as-built)

```
saged.club/
├── index.html                    RU home
├── studio/                       RU ceramics with Koritsia
├── kids/                         RU kids ceramics
├── events/                       Events (RU — mixed language)
├── coworking/                    Coworking (RU)
├── gifts/                        Gift certificates (RU)
├── private/                      Private events (RU)
├── kundoglini/                   Specific event page (RU)
├── cookies.html
├── privacy.html
│
├── ua/                           UA full mirror
│   ├── index.html
│   ├── studio/
│   ├── kids/
│   ├── events/
│   ├── coworking/
│   ├── gifts/
│   ├── private/
│   └── kundoglini/
│
├── uk/                           Redirect stubs → /ua/
│   ├── index.html  → /ua/
│   ├── coworking/  → /ua/coworking/
│   ├── events/     → /ua/events/
│   ├── kids/       → /ua/kids/
│   └── studio/     → /ua/studio/
│
└── en/                           ⚠️ INCOMPLETE
    ├── (no index.html)           ← MISSING
    ├── kids/                     EN kids (exists)
    └── coworking/                EN coworking (exists)
```

**Critical gaps in current sitemap:**
- `/en/` — no English home or landing page
- `/en/studio/` — no English ceramics page

---

## Proposed sitemap (redesign target)

Changes from current are marked **[NEW]**, **[MOVE]**, **[MERGE]**, or **[FIX]**.

```
saged.club/
│
├── index.html                    RU home
│   Sections: hero · offerings · events strip · instructor · 
│             testimonials · map · contact
│
├── studio/                       RU ceramics — Koritsia
│   Sections: hero · process (3-step) · instructor · 
│             what's included · schedule · gallery · 
│             testimonials · booking [book CTA earlier] · FAQ
│
├── kids/                         RU kids ceramics
│
├── events/                       Events (RU)
│   [FIX] Add prices to each event listing
│
├── coworking/                    Coworking (RU)
│   [MOVE] Demote from primary nav to footer only
│
├── gifts/                        Gift certificates (RU)
│
├── private/                      Private events (RU)
│
│
├── ua/                           UA full mirror (keep identical structure to RU)
│   ├── index.html
│   ├── studio/
│   ├── kids/
│   ├── events/
│   ├── coworking/
│   ├── gifts/
│   └── private/
│
├── uk/ → /ua/                    Redirect stubs (keep, don't remove)
│
└── en/                           English section
    ├── index.html                [NEW] English home / landing
    │   Sections: hero (EN) · ceramics offer · instructor · 
    │             booking · map
    │
    ├── studio/                   [NEW] English ceramics page
    │   Same structure as RU /studio/ but in English
    │   Explicitly states: "Taught in English"
    │
    ├── kids/                     EN kids (exists, keep)
    └── coworking/                EN coworking (exists, keep)
```

---

## Navigation redesign

### Current nav (RU)
```
[Logo]  Взрослым  Детям  Коворкинг  Events  Подарки  Приватно  [RU | UA]
```
Problems: "Events" in English breaks language consistency. "Коворкинг" in primary nav wrong audience.

### Proposed nav (RU)
```
[Logo]  Студия  Детям  События  Подарки  [RU | UA | EN]
```
- "Коворкинг" moved to footer
- "Приватно" moved to footer (secondary audience)
- "Events" renamed to "События" (consistent Russian)
- Language switcher adds EN option

### Proposed nav (EN)
```
[Logo]  Ceramics  Kids  Events  Gifts  [EN | RU | UA]
```

---

## Page priority for redesign (build order)

| Priority | Page | Why |
|---|---|---|
| 1 | `/en/studio/` | Missing landing for best-performing ad campaign |
| 2 | `/en/` | English home — needed for EN audience entry point |
| 3 | `/studio/` | Move booking CTA higher, embed Cal.com inline |
| 4 | `/index.html` | Fix primary CTA (events → ceramics) |
| 5 | `/ua/studio/` | Mirror changes from RU studio page |
| 6 | All pages | Fix WhatsApp number consistency |
| 7 | `/events/` | Add prices to each event |

---

## URL structure decisions

**Keep `/ua/` as canonical Ukrainian path.** The `/uk/` stubs exist as redirects for any old links that use the ISO code. Do not delete the `/uk/` redirects — they're lean (13 lines each) and harmless.

**English path is `/en/`**, not `/en-gb/` or `/english/`. Already used for kids and coworking, keep consistent.

**No language subdomain.** Current path-based structure (`/ua/`, `/en/`) is correct for a small site. Subdomains (`ua.saged.club`) would complicate GitHub Pages hosting and cookie/consent logic.

---

_Last updated: 2026-08-29_
