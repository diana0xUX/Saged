# Codex Handoff — Saged.club Redesign
**Agent:** Read this entire file before writing any code.
**Working directory:** `/Users/diana/Documents/saged.club/`
**Reference docs:** `docs/ux-audit.md` · `docs/sitemap.md` · `docs/ia-redesign.md`
**Source of truth:** `creative/SAGED-SOURCE-OF-TRUTH.md`

---

## Context

Saged.club is a ceramic and cultural workshop space in the old city of Valencia. Owner: Diana Sage — product designer and ceramicist. Primary audiences: Russian and Ukrainian-speaking residents (RU/UA), English-speaking expats (EN).

The site is vanilla HTML/CSS/JS. No framework, no build step. Hosted on GitHub Pages. Edit files and push — that's the deploy.

The UX audit identified two critical gaps and several high-priority fixes. This handoff specifies exactly what to build and how.

---

## Tech stack — do not deviate

- **HTML/CSS/JS only.** No React, no Vue, no Tailwind, no build tool.
- **CSS custom properties** (design tokens) defined in `assets/style.css :root`. Use them — don't hardcode hex values.
- **Fonts:** Saged Cyrillic (Cyrillic display) + Costa Light (Latin display) + Inter (body/UI). Self-hosted from `assets/fonts/`. Do not add new fonts.
- **Google Maps embed** via `<iframe>` with `loading="lazy"`. No Maps JS API.
- **WhatsApp links** via `wa.me` deep links. Use anchor-click pattern for JS-triggered opens (see constraint below).
- **Cal.com booking** via direct link: `https://cal.com/saged-club/ceramics`
- **Analytics:** Plausible via CDN (`<script defer data-domain="saged.club" src="https://plausible.io/js/script.js">`). Meta Pixel loaded by `assets/script.js` after consent — do NOT add Pixel script tags directly in HTML.
- **Consent banner:** `<div id="consent" class="consent" hidden>` + `<script src="[path-to]/assets/script.js">` at bottom of every page. Never remove.

---

## Design tokens — from `assets/style.css`

```css
:root {
  --bg:       #FAF7F2;   /* page background — warm off-white */
  --bg-sand:  #F1E9DA;   /* section background — sand */
  --ink:      #2A2520;   /* primary text, dark UI */
  --muted:    #6B5F54;   /* secondary text, captions */
  --terracotta: #9F4D2D; /* links, CTAs, accent (web only) */
  --sage:     #6E7F5A;   /* nature/wellness accent (rarely used) */
  --line:     #E1D6C5;   /* dividers, borders */
  --max:      1100px;    /* max content width */
  --gutter:   clamp(1.25rem, 3vw, 2.5rem); /* horizontal padding */
}
```

**Never use `#FF7A23` (logo orange) in web CSS.** That colour is print/ads only. Web accent is `--terracotta: #9F4D2D`.

---

## CSS classes reference — copy patterns, don't reinvent

All classes are defined in `assets/style.css`. Use them.

```
Layout:
  .band               4rem padding, max-width 1100px, centred
  .band--sand         band with bg-sand background (full-bleed)
  .three              3-column grid (responsive → 1col mobile)
  .hero               2-column grid: media left, copy right (responsive → stacked)
  .about              2-column grid: photo left, copy right

Typography:
  .eyebrow            0.8rem, uppercase, letter-spaced, muted — section label
  .lead               1.15rem body intro text
  .muted              color: var(--muted)
  .small              font-size: 0.85rem
  .center             text-align: center
  .label              0.75rem, uppercase, letter-spaced, muted — used in schedule

Interactive:
  .cta                pill button — terracotta fill (primary action)
  .cta--secondary     pill button — terracotta outline (secondary action, equal weight)
  .channel            contact card (icon + name + handle)
  .channels           grid of .channel cards

Content:
  .testimonial        quote card with terracotta left border
  .testimonial-grid   3-column grid of testimonials
  .includes           2-column bullet list for "what's included"
  .gallery__grid      4-column image grid
  .schedule__grid     4-column info grid
  .faq                accordion using <details>/<summary>
  .book               booking section — centred, max-width 36rem
  .book__paths        side-by-side CTA pair (DM + pay)
  .book__path         individual path (CTA + description)
  .book__embed        background sand box around booking content

Carousel:
  .carousel / .carousel__track / .carousel__slide / .carousel__dots
  JS is in assets/script.js — no new carousel code needed
```

---

## Hard constraints

1. **GDPR consent banner** — `<div id="consent" class="consent" hidden>` must be present on every page. `<script src="assets/script.js">` fires Pixel after consent. Never remove or bypass.

2. **Bilingual mirror rule** — every structural change to `index.html` (RU) must be mirrored in `ua/index.html` (UA). Same sections, same structure, same block count. Content is translated, not restructured.

3. **WhatsApp deep link from JS** — use anchor-click pattern, NOT `window.open()`:
   ```js
   const a = document.createElement('a');
   a.href = `https://wa.me/34605543300?text=${msg}`;
   a.target = '_blank';
   a.rel = 'noopener';
   document.body.appendChild(a);
   a.click();
   a.remove();
   ```
   `window.open()` drops the `text=` parameter on mobile Safari.

4. **WhatsApp number:** `+34 605 54 33 00` / `34605543300`. Use this everywhere. (Source of truth currently has a different number — the site number is canonical.)

5. **Address:** `C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia` — use this exact format everywhere. Match what's in the Google Maps embed and schema.org.

6. **Do not commit** `.env`, `finances/`, `data/raw/`, `inbox/`, `*.MOV` — these are gitignored for good reason.

7. **No `--` inside HTML comment bodies.** `<!-- --- SECTION --- -->` is invalid HTML. Use `<!-- SECTION -->`.

---

## Build order — priority 1 first

---

### TASK 1 — Create `/en/studio/index.html` 🔴 CRITICAL

**Why first:** The EN ceramics ad (best-performing: CTR 5.17%, CPC €0.01) currently has no landing page. Every ad euro spent without this page is partially wasted.

**Template to copy:** `studio/index.html` — copy the full file, translate to English, adapt where noted below.

**Path:** `en/studio/index.html`
**Asset path prefix:** `../../` (two levels up from `en/studio/`)

#### Head
```html
<html lang="en">
<title>Ceramics with Koritsia · Every Thursday · Saged.club Valencia</title>
<meta name="description" content="A 2-day pottery class in English. Every Thursday in Saged.club, old city Valencia. €60 for two sessions. Shape, glaze, take your piece home. Groups up to 6.">
<link rel="canonical" href="https://saged.club/en/studio/">
<link rel="alternate" hreflang="en" href="https://saged.club/en/studio/">
<link rel="alternate" hreflang="ru" href="https://saged.club/studio/">
<link rel="alternate" hreflang="uk" href="https://saged.club/ua/studio/">
```

#### Schema.org (in `<head>`)
Same Course schema as RU version. Change:
```json
"inLanguage": ["en"]
"name": "Ceramics with Koritsia"
"description": "A 2-day pottery class in English, every Thursday in Valencia old city. Shape, glaze, take your piece home."
```

#### Header/nav
```html
<header class="topbar">
  <a class="brand" href="../../" aria-label="Saged.club home">
    <img src="../../assets/images/logo-saged-club.svg" alt="Saged.club" width="88" height="40">
  </a>
  <nav class="topnav" aria-label="Sections">
    <span class="topnav__current">Ceramics</span>
    <a href="../../en/kids/">Kids</a>
    <a href="../../events/">Events</a>
    <a href="../../gifts/">Gifts</a>
  </nav>
  <nav class="lang" aria-label="Language">
    <span class="lang__current">EN</span>
    <a href="../../studio/" class="lang__alt">RU</a>
    <a href="../../ua/studio/" class="lang__alt">UA</a>
  </nav>
</header>
```

#### BLOCK 1 — Hero
Copy `.hero` structure from `studio/index.html`. Changes:
- Same carousel (video + 3 photos, same image paths via `../../assets/images/`)
- Eyebrow: `Every Thursday · Old City · Valencia`
- H1: `Ceramics with Koritsia`
- Lead: `A 2-session pottery class in English. Shape your piece, glaze it, take it home. Small group — up to 6 people.`
- Price line: `€60 · two sessions · everything included`
- CTA: `<a href="#book" class="cta">Book your spot</a>`

**ADD** immediately after the hero copy div, before or alongside the price line — an "IN ENGLISH" badge:
```html
<span class="lang-badge">Taught in English</span>
```
Style inline or add to page `<style>`:
```css
.lang-badge {
  display: inline-block;
  background: var(--ink);
  color: var(--bg);
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
  margin-bottom: 1rem;
}
```

#### BLOCK 2 — 3-step process (`.band.band--sand > .three`)
```
Session 1 — Shape
  Two hours with clay. Build your piece by hand — a bowl, a vase, a mug, beads, whatever you want. Koritsia guides every step.

Session 2 — Glaze
  A week later, your piece comes back from the first firing. You choose colours, apply glaze, decorate. The studio does the final firing.

What you take home
  Your piece — fired, glazed, finished. Ready to live with you. Two weeks after the second session.
```

#### BLOCK 3 — Instructor (`.about`)
```html
<p class="eyebrow">Your instructor</p>
<h2>Koritsia <span class="muted small">/ Корица</span></h2>
<p>A Ukrainian ceramic artist based in Valencia, Koritsia works as the ceramic resident at Saged.club. For her, clay is a slow, tactile material — it doesn't tolerate rushing, and that's the point.</p>
<p>She hand-builds ceramics of every kind — bowls, vases, candleholders, beads, small sculptures. Each course is two sessions with a week in between, because the clay needs time: it must dry and go through its first firing before you can glaze it. Groups stay small — up to 6 — so everyone gets her full attention.</p>
<p class="muted small">Koritsia teaches in English, Ukrainian, and Russian. Sessions happen in whatever language the group prefers.</p>
```
Photo: `../../assets/images/koritsya.jpg`

#### BLOCK 4 — What's included (`.band > .includes`)
```
Two sessions (2 hours each)
Clay (~1 kg)
All tools and workspace
Glaze and colour choice
Both firings (bisque + glaze)
Tea and water
Your finished piece (ready in 2 weeks)
```

**ADD a booking CTA directly after the includes list — before the schedule section:**
```html
<div style="text-align:center; margin-top:2rem;">
  <a href="#book" class="cta">Book your spot →</a>
</div>
```

#### BLOCK 5 — Schedule (`.schedule`)
```
When:       Every Thursday
Sessions:   Two consecutive Thursdays — same time slot both weeks
Time slots: 12:00–14:00 / 15:00–17:00 / 19:00–21:00
Start:      Any Thursday — join any week
Group:      Up to 6 people
```
Map iframe: same as RU version. Caption: `C/ de les Cuines, 8 · Ciutat Vella · 46001 Valencia`

#### BLOCK 6 — Gallery (`.gallery`)
H2: `How it feels`
Caption: `Small group, warm light, your hands in clay. No rush.`
Same 4 images as RU version.

#### BLOCK 7 — Testimonials (`.band.testimonials`)
H2: `What people say`
Use same quotes from RU version if no EN-specific quotes exist yet. Add `— Google review` attribution.

#### BLOCK 8 — Instagram embed (`.band.band--sand.instagram-band`)
H2: `On Instagram`
Same 2 blockquotes. Caption: `Follow us — @saged.club`

#### BLOCK 9 — Booking `id="book"` (`.book`)
```html
<h2 class="center">Book your spot</h2>
<p class="center muted">Not sure? Message us — we'll answer your questions and book you in manually. Ready to go — book and pay directly.</p>
<p class="center muted small">Confirmed after payment. Free cancellation up to 48 hours before.</p>

<div class="book__embed">
  <div class="book__paths">
    <div class="book__path">
      <a class="cta cta--secondary"
         href="https://wa.me/34605543300?text=Hi!%20I%27d%20like%20to%20book%20a%20ceramics%20class%20with%20Koritsia.%0A%0AName%3A%20%0ADate%20(any%20Thursday)%3A%20%0ATime%20slot%20(12%3A00%20%2F%2015%3A00%20%2F%2019%3A00)%3A%20%0A%0AQuestions%3F%20Ask%20me%20here%20%3A)"
         target="_blank" rel="noopener">
        Message on WhatsApp
      </a>
      <p class="muted">Reply within a few hours · we'll confirm your spot</p>
    </div>
    <div class="book__path">
      <a class="cta" href="https://cal.com/saged-club/ceramics" target="_blank" rel="noopener">
        Pick a date and pay
      </a>
      <p class="muted">Instant confirmation · card payment via Stripe</p>
    </div>
  </div>
  <p class="muted small center" style="margin-top:2rem;margin-bottom:1rem">or find us on:</p>
  <div class="channels">
    <a class="channel" href="https://wa.me/34605543300?text=Hi%2C%20I%27d%20like%20to%20know%20about%20ceramics">
      <span class="channel__name">WhatsApp</span>
      <span class="channel__handle">+34 605 54 33 00</span>
    </a>
    <a class="channel" href="https://instagram.com/saged.club">
      <span class="channel__name">Instagram</span>
      <span class="channel__handle">@saged.club</span>
    </a>
  </div>
  <p class="muted small center" style="margin-top:1.5rem">or email: <a href="mailto:hello@saged.club?subject=Booking%20—%20Ceramics%20with%20Koritsia">hello@saged.club</a></p>
</div>
```

#### BLOCK 10 — FAQ (`.band.band--sand > .faq`)
```
Do I need experience?
  None. We start from zero and go at your pace. Koritsia helps everyone.

Why two sessions, not one?
  The clay needs a week to dry and go through the first firing before you can glaze it. That's just how ceramics works — we don't rush it.

Can I start any Thursday?
  Yes. The course runs every Thursday. Book two consecutive Thursdays (e.g. the 14th + 21st) in whichever time slot works for you.

What should I wear?
  Anything you don't mind getting dirty. Clay washes out but can leave marks. Aprons are provided.

What if I miss the second session?
  The studio can glaze for you — but it's worth coming. Choosing the colour and decoration is the best part. You can also reschedule your second session to the following Thursday.

When do I get my piece?
  Two weeks after your second session. Pick it up at the studio, or we can arrange delivery within Valencia.

Can I bring a friend?
  Yes — book two spots on the same Thursday and let us know. Message us on WhatsApp and we'll confirm both together.

Is there a gift certificate?
  Yes. Message or email us and we'll send a named certificate within the day. <a href="../../gifts/">See gift options →</a>
```

#### Footer
```html
<footer class="footer">
  <p><strong>Saged.club</strong></p>
  <p class="muted">A studio for making things with your hands — ceramics, sound, tea, and community in the old city of Valencia.</p>
  <p class="muted">C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia</p>
  <p class="muted">WhatsApp <a href="https://wa.me/34605543300">+34 605 54 33 00</a> · <a href="mailto:hello@saged.club">hello@saged.club</a> · <a href="https://instagram.com/saged.club">@saged.club</a></p>
  <p class="muted">Also: <a href="../../en/kids/">Kids ceramics</a> · <a href="../../coworking/">Studio coworking</a></p>
  <p class="muted small">© 2026 Saged.club · <a href="../../privacy.html">Privacy</a> · <a href="../../cookies.html">Cookies</a></p>
</footer>
```

#### Consent banner + script (bottom of body — same as all pages)
```html
<div id="consent" class="consent" hidden>
  <p>Help us understand what's working — allow analytics? Visit stats only, no ad tracking.</p>
  <div class="consent__buttons">
    <button id="consent-accept" class="btn-solid">Allow</button>
    <button id="consent-decline" class="btn-text">Not now</button>
  </div>
</div>
<script src="../../assets/script.js"></script>
```

#### ViewContent — add to script.js path map
After creating this file, add `/en/studio` to the ViewContent map in `assets/script.js`:
```js
'/en/studio': 'studio-adult',
```
The map is at line 32–35 of `assets/script.js`.

---

### TASK 2 — Create `/en/index.html` 🔴 CRITICAL

**Why:** English-speaking visitors who click through to `saged.club/en/` currently get a 404. This page is the entry point for the EN audience.

**This is a shorter page than `/en/studio/`.** It orients, then routes to `/en/studio/`. It is not a full product page.

**Path:** `en/index.html`
**Asset path prefix:** `../`

#### Head
```html
<html lang="en">
<title>Saged.club · Ceramics studio and cultural space · Valencia</title>
<meta name="description" content="Pottery classes, sound ceremonies, and community events in the old city of Valencia. Small groups, real people, made by hand.">
<link rel="canonical" href="https://saged.club/en/">
<link rel="alternate" hreflang="en" href="https://saged.club/en/">
<link rel="alternate" hreflang="ru" href="https://saged.club/">
<link rel="alternate" hreflang="uk" href="https://saged.club/ua/">
```

#### Nav
```html
<nav class="topnav">
  <a href="studio/">Ceramics</a>
  <a href="../en/kids/">Kids</a>
  <a href="../events/">Events</a>
  <a href="../gifts/">Gifts</a>
</nav>
<nav class="lang">
  <span class="lang__current">EN</span>
  <a href="../" class="lang__alt">RU</a>
  <a href="../ua/" class="lang__alt">UA</a>
</nav>
```

#### Hero section
Use `.home-hero` class structure (copy from `index.html` home hero block):
```
Eyebrow:  Saged.club · Valencia
H1:       A studio where you make things with your hands
Lead:     Pottery classes, sound ceremonies, and slow community in the old city of Valencia. Small groups. Real people. No rush.
CTA:      Join a ceramics class → (href="studio/")
Image:    ../assets/images/workshop-1.jpg
```

#### Trust strip (`.trust-strip`)
```
50+ participants     since May 2026
Small groups        up to 6 people · no rush
Old City Valencia   C/ de les Cuines, 8
```

#### Three offerings (`.band > .three` or 3 cards)
Card 1 — Ceramics:
```
Label: Ceramics studio
Title: Taught in English
Body:  A 2-session wheel class with Koritsia, a Ukrainian ceramic artist. Every Thursday. Take your piece home.
Price: €60 · 2 sessions · all materials included
CTA:   Learn more → (href="studio/")
```
Card 2 — Events:
```
Label: Cultural programme
Title: Gather with people
Body:  Sound ceremonies, breathwork, tea gatherings, slow friending. Small groups, real encounters.
CTA:   See events → (href="../events/")
```
Card 3 — For ceramicists:
```
Label: Studio coworking
Title: Workspace for potters
Body:  Hot desk in a working ceramic studio in the old city. 5 spots. Ask about availability.
CTA:   Find out more → (href="../coworking/")
```

#### Find us block
```html
<section class="band">
  <h2 class="center">Find us</h2>
  <div class="map">
    <iframe title="Saged.club on the map"
      src="https://maps.google.com/maps?q=Saged,%20C%2F%20de%20les%20Cuines,%208,%2046001%20Val%C3%A8ncia&output=embed"
      width="100%" height="320" loading="lazy" allowfullscreen
      referrerpolicy="no-referrer-when-downgrade"></iframe>
    <p class="map__caption">
      <strong>C/ de les Cuines, 8</strong> · Ciutat Vella · 46001 Valencia<br>
      WhatsApp <a href="https://wa.me/34605543300">+34 605 54 33 00</a> ·
      <a href="https://instagram.com/saged.club">@saged.club</a><br>
      <a href="https://maps.app.goo.gl/RqsReEo929aeUAPN9">Open in Google Maps →</a>
    </p>
  </div>
</section>
```

#### Footer + consent — same pattern as `/en/studio/`

---

### TASK 3 — Fix home page CTA `index.html` 🟠 HIGH

**File:** `index.html` (RU home)
**Also mirror:** `ua/index.html` (UA home)

Change the primary hero CTA from events to ceramics:

```html
<!-- BEFORE -->
<a href="events/" class="home-hero__cta">Ближайшие события →</a>

<!-- AFTER -->
<a href="studio/" class="home-hero__cta">Записаться на керамику →</a>
```

Add a secondary link below it:
```html
<a href="events/" style="font-size:0.9rem;color:var(--muted);border-bottom:1px solid var(--line);margin-top:0.75rem;display:inline-block;">Ближайшие события →</a>
```

Mirror the same change in `ua/index.html`:
```html
<a href="studio/" class="home-hero__cta">Записатись на кераміку →</a>
<a href="events/" ...>Найближчі події →</a>
```

---

### TASK 4 — Add mid-page booking CTA to `/studio/index.html` 🟠 HIGH

**File:** `studio/index.html` (and mirror `ua/studio/index.html`)

After the "What's included" section (`.band > .includes` list), before the `.schedule` section, insert:

```html
<div class="center" style="margin-top:2.5rem;">
  <a href="#book" class="cta">Выбрать дату и записаться →</a>
  <p class="muted small" style="margin-top:0.75rem;">Или напишите в WhatsApp — ответим и забронируем вручную</p>
</div>
```

UA mirror:
```html
<div class="center" style="margin-top:2.5rem;">
  <a href="#book" class="cta">Обрати дату і записатися →</a>
  <p class="muted small" style="margin-top:0.75rem;">Або напишіть у WhatsApp — відповімо і забронюємо вручну</p>
</div>
```

---

### TASK 5 — Fix nav language consistency `studio/index.html` 🟡 MEDIUM

**File:** `studio/index.html` nav (and `ua/studio/index.html`)

Current nav has "Events" in English inside a Russian nav. Change:
```html
<!-- BEFORE -->
<a href="../events/">Events</a>

<!-- AFTER -->
<a href="../events/">События</a>
```

UA version: `<a href="../ua/events/">Події</a>`

Also add EN link to language switcher on RU/UA pages:
```html
<nav class="lang" aria-label="Language">
  <span class="lang__current">RU</span>
  <a href="../ua/studio/" class="lang__alt">UA</a>
  <a href="../en/studio/" class="lang__alt">EN</a>
</nav>
```

---

### TASK 6 — Add ViewContent path for new EN pages 🟡 MEDIUM

**File:** `assets/script.js`

Add to the ViewContent map at lines 32–35:
```js
'/en/studio': 'studio-adult',
'/en': 'home-en',
```

Full updated map:
```js
const vc = {
  '/studio': 'studio-adult', '/ua/studio': 'studio-adult', '/en/studio': 'studio-adult',
  '/kids': 'studio-kids',   '/ua/kids': 'studio-kids',
  '/coworking': 'coworking', '/ua/coworking': 'coworking',
  '/en': 'home-en',
}[path];
```

---

## Self-evaluation checklist

Run every item before committing.

**New pages (`/en/studio/`, `/en/`)**
- [ ] `<html lang="en">` on both pages
- [ ] `<link rel="canonical">` present and correct
- [ ] `hreflang` alternates: en, ru, uk on both pages
- [ ] Asset paths use `../../` prefix from `en/studio/`, `../` from `en/`
- [ ] Consent banner present (`<div id="consent">` + script tag at end of body)
- [ ] "Taught in English" badge visible in `/en/studio/` hero
- [ ] WhatsApp number `34605543300` in all `wa.me` links
- [ ] Pre-filled WhatsApp message text is URL-encoded (no raw spaces)
- [ ] Booking section has both WhatsApp path (`.cta--secondary`) and Cal.com path (`.cta`) at equal visual weight
- [ ] Mid-page booking CTA present after "What's included" on `/en/studio/`
- [ ] Map embed present with correct address caption
- [ ] Script tag path correct: `../../assets/script.js` from `en/studio/`, `../assets/script.js` from `en/`
- [ ] Plausible script present: `<script defer data-domain="saged.club" src="https://plausible.io/js/script.js">`

**Existing page fixes**
- [ ] `index.html` hero CTA: now points to `studio/`, not `events/`
- [ ] `ua/index.html` hero CTA: now points to `studio/` (UA), not `events/`
- [ ] `studio/index.html`: mid-page booking CTA added after includes list
- [ ] `ua/studio/index.html`: same mid-page CTA added (in Ukrainian)
- [ ] Nav "Events" renamed to "События" in RU pages / "Події" in UA pages
- [ ] Language switcher on studio pages includes EN link

**Code quality**
- [ ] No `--` inside HTML comment bodies (breaks HTML parser)
- [ ] No inline `style` tags with hardcoded hex colours — use CSS custom properties
- [ ] All images have descriptive `alt` attributes
- [ ] All external links have `target="_blank" rel="noopener"`
- [ ] `assets/script.js` ViewContent map updated with new EN paths
- [ ] No new fonts or CDN dependencies introduced

---

## What NOT to do

- Do not use `window.open()` for WhatsApp links — use anchor-click pattern
- Do not remove the consent banner from any page
- Do not add framework dependencies (React, Tailwind, etc.)
- Do not hardcode `#FF7A23` anywhere in CSS — that's ads-only orange
- Do not use `#9F4D2D` in inline styles — use `var(--terracotta)`
- Do not add new font families
- Do not merge RU and UA pages or redirect one to the other
- Do not restructure `ua/index.html` independently from `index.html` — they must mirror

---

## Files to create or edit

| Action | File |
|---|---|
| **Create** | `en/studio/index.html` |
| **Create** | `en/index.html` |
| **Edit** | `index.html` (hero CTA) |
| **Edit** | `ua/index.html` (hero CTA mirror) |
| **Edit** | `studio/index.html` (mid-page CTA + nav fix) |
| **Edit** | `ua/studio/index.html` (mid-page CTA mirror + nav fix) |
| **Edit** | `assets/script.js` (ViewContent map) |

---

_Handoff written: 2026-08-30_
_Cross-reference: `docs/ux-audit.md` · `docs/sitemap.md` · `docs/ia-redesign.md`_
_For questions on brand/design decisions: `creative/SAGED-SOURCE-OF-TRUTH.md` · `creative/DESIGNER.md`_
