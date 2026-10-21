# Saged — Design Identity for AI Agent

This file is loaded at the start of every design session. It tells me who Saged is visually, what rules I follow, and how I work. It is the machine-readable equivalent of a brand guide + design brief + process doc in one.

---

## Who I Am Designing For

**Saged.club** — a ceramic and cultural workshop space in the old city of Valencia.
Owner: **Diana Sage**, product designer and ceramicist.
Primary audiences: Russian-speaking and Ukrainian-speaking residents of Valencia (RU/UA), plus English-speaking expats (EN).

**Feeling to communicate:** warm, handmade, community-rooted, a little playful — not corporate, not minimalist-cold, not tourist-y. Think: a real person's studio, not a brand agency's idea of one.

---

## Brand Personality

| Attribute     | Expression                                                    |
|---------------|---------------------------------------------------------------|
| Warm          | Cream backgrounds, clay tones, no pure whites or cold grays   |
| Handmade      | Brand figures, organic blob shapes, hand-drawn energy         |
| Playful       | Scattered decorative elements, arrows pointing at things      |
| Honest        | Real photos of real people, not stock                         |
| Community     | Names on figures, personal tone in copy                       |

---

## Colour System

Always use these exact values. Do not approximate.

| Token           | Hex       | Use                                              |
|-----------------|-----------|--------------------------------------------------|
| Background      | `#F9F4ED` | Page/canvas background (warmer than pure white)  |
| Sand            | `#F1E9DA` | Secondary backgrounds, photo zones, pill fills   |
| Ink             | `#2A2520` | Primary text, headlines on light                 |
| Muted           | `#6B5F54` | Secondary text, captions, labels                 |
| Terracotta (UI) | `#9F4D2D` | Web UI accents, links, arrows                    |
| Logo orange     | `#FF7A23` | **Primary brand accent in print/ads.** Badges, price blobs, headline accents, CTA buttons |
| Sage            | `#6E7F5A` | Tertiary accent, nature/wellness events          |
| Line / border   | `#E1D6C5` | Dividers, card borders, subtle separators        |

**Critical distinction:** `#FF7A23` (logo orange) is the primary accent in ads and print. `#9F4D2D` (terracotta) is for web UI only. Never swap them.

### Colour combinations that work
- Ink on Background: body text
- Logo orange on Background: badges, price, CTA
- White on Logo orange: reversed badge text
- Logo orange on Ink: inverted hero
- Sand as photo background: figures, product shots

---

## Typography

### Font stack (in priority order)

| Font            | Weight | File path                                      | Use                          |
|-----------------|--------|------------------------------------------------|------------------------------|
| Costa           | Light  | `assets/fonts/costa-light.otf`                 | Latin display / all headings |
| Saged Cyrillic  | 400    | `assets/fonts/saged-display-cyrillic-v1.396.woff` | Cyrillic display / headings |
| Inter           | 400/500| Google Fonts                                   | All body copy, UI, labels    |

### Type hierarchy for ads (1080×1350)

| Level      | Font    | Size   | Weight | Colour   | Use                     |
|------------|---------|--------|--------|----------|-------------------------|
| Display    | Costa   | 120–180px | Light | Ink or Orange | Main headline — readable in 0.25s |
| Sub-display| Costa   | 36–60px | Light | Muted or Orange | Location, name, day |
| Body       | Inter   | 24–28px | 400   | Muted    | Course details (24px minimum) |
| Label/pill | Inter   | 18–20px | 500   | Ink or White | Tags, small info (never below 16px) |

**Mathematical type scale (Perfect Fifth, ×1.5):** 24 → 36 → 54 → 81 → 121px. Use these steps, not arbitrary sizes. Our Costa display at 120–180px lands at the top two stops.

### Type rules
- Language rule for the website: Russian and Ukrainian use Saged Cyrillic for display; English and Spanish use Costa as the accent/display font. Inter remains the body and UI font in every language.
- Costa dominates. One or two words max per line at display size.
- Never use more than 2 font families in one piece.
- Letter-spacing: Costa large display: −0.02 to −0.05em (tighter). All-caps labels: +0.04 to +0.08em (looser).
- Line height: body copy 1.4–1.6×. Headlines 1.1–1.3×.
- Max line length for image text: 7–8 words per line.
- Text on orange: always white (`#FAF7F2`), never ink.
- Minimum contrast: 4.5:1 for body text. 3:1 for large display. CTA contrast target: 6:1–8:1 (delivers ~17% better performance).
- Never place text directly over a busy photo — use a colour overlay or crop to a clear zone.

---

## Logo & Brand Marks

| File                                          | Use                                           |
|-----------------------------------------------|-----------------------------------------------|
| `assets/images/logo-saged-club.svg`           | Primary SVG — use on all digital              |
| `creative/library/01-brand/logos/logo-white.png`  | On dark or coloured backgrounds           |
| `creative/library/01-brand/logos/logo-black.png`  | On light backgrounds when SVG unavailable |
| `creative/library/01-brand/logos/logo-orange.png` | Alternate brand expression                |
| `assets/images/saged-symbols.svg`             | Decorative strip / texture element            |

**Logo placement in ads:** top-right corner, ~80–100px tall, with 28–40px margin. Always logo-white on coloured backgrounds, SVG/logo-black on cream/sand.

---

## Brand Figures

41 character illustrations at `creative/library/02-figures/`.

**Named characters** (use when the person is relevant):
- `Diana.png` — Diana (studio owner)
- `koritsa.png` — Koritsia (ceramics instructor)
- `helena.png` — Helena (English/Spanish classes)
- `Vlada.png`, `liza.png`, `zhenya.png` — community figures

**Numbered figures** (use as decorative elements, scattered):
- `figure 1.png`, `figure 4.png`, `figure 6.png` — active/dancing poses
- `figure 22.png`, `figure 26.png`, `figure 27.png` — standing/gesture poses
- `figure 19.png`, `figure 24.png` — calm, seated or still

### Figure placement rules
- Always scatter at edges/corners — never centred, never inline with text.
- Opacity: 0.45–0.60. They are texture, not focal points.
- Scale: 100–180px tall. Larger = more prominent. Use sparingly.
- Minimum 3, maximum 6 per composition. The Koritsia ad uses 4–5.
- Mix active and still poses. Don't repeat the same figure twice in one piece.

---

## Layout Principles

### Named layout principles (use these when making decisions)

**60-30-10 colour rule:** 60% dominant (background/cream), 30% secondary (ink text, photo), 10% accent (orange badges, price, highlights). Saged's warm cream IS the 60%.

**3-Element Rule:** maximum 3 primary focal points per frame. Human working memory holds 3–4 chunks. More than 3 competing elements = nothing reads. Our three: headline / photo / price blob.

**Z-Pattern:** the default eye path in Western reading — top-left → top-right → diagonal → bottom-right. Map: `SAGED CLUB` top-left → logo mark top-right → diagonal across photo → price blob bottom-right.

**The squint test:** half-close your eyes and look at the composition. What do you see first? It must be the headline or the instructor's face — not the figures, not the address block.

**Isolation creates attention:** an element surrounded by empty space draws up to 100% more attention than one in a crowded layout. The cream background earns its keep.

### Ad anatomy (learned from Koritsia ceramics ad — the reference standard)
```
┌─────────────────────────────────┐
│ SAGED CLUB (small caps)  [LOGO] │  ← header row, 60px tall
│                                 │
│  HUGE                           │  ← Costa display, dominates top 35%
│  HEADLINE                       │
│  IN ORANGE                      │
│                                 │
│  [PHOTO]      [BADGE pill]      │  ← photo left, info right, middle zone
│  NAME→        Day · Location    │
│               Details block     │
│               ✦                 │
│─────────────────────────────────│  ← divider line
│ Address       [€XX price blob]  │  ← bottom info strip
│ WhatsApp                        │
│─────────────────────────────────│
│ saged.club          @handle     │  ← footer, 40px
└─────────────────────────────────┘
```

### Card & frame rules (UI — non-negotiable)

**Words must never be clipped by a card edge.** If a word is cut off, the padding is wrong or the font is too large — fix it, don't work around it.

**Padding inside frames must be strict:**
- Cards (`.pillar`, `.assoc__card`, `.team__card`): minimum `24px` horizontal padding at any viewport width. Use `clamp(24px, 3.5vw, 44px)` — never drop below 24px.
- Content must always have room to wrap before it hits the edge. If it can't wrap, reduce the font size.

**Grid items that contain text must have `min-width: 0`** to prevent CSS grid from letting content overflow the column.

**Long display words in grid cells:**
- Always set `overflow-wrap: break-word; word-break: break-word` on large Costa titles inside card grids.
- Test with the longest expected word at minimum viewport (375px). If it clips, reduce font size before publishing.
- Font size for pillar titles in 3-column grids: max `clamp(22px, 2.6vw, 38px)`.

**The rule in one sentence:** a card that clips a word is a broken card — just like a button that clips its label.

---

### Visual hierarchy rules
1. **One thing first.** The headline should be readable in 1 second, without reading anything else.
2. **Photo and headline share the top half.** Don't crowd the bottom.
3. **Price is always visible without scrolling.** Bottom-right, inside an orange blob.
4. **Figures live at edges.** They frame, they don't compete.
5. **Whitespace is warm.** The cream background IS the breathing room — don't fill it.

### Composition ratios that work
- Display text: ~40% of canvas height
- Photo zone: ~35–40% of canvas height
- Info + footer: ~20–25% of canvas height
- Left margin: 60px. Right margin: 60px. Consistent.

---

## Photo Usage

### Available photos by use case

| Need                  | Use this                                                  |
|-----------------------|-----------------------------------------------------------|
| Instructor portrait   | `koritsa-editorial.jpg`, `koritsya-portrait.png`         |
| Hands at work         | `workshop-teaching.jpg`, `workshop-1.jpg`                |
| Studio atmosphere     | `hero-1.jpg`, `hero-2.jpg`, `gallery-1.jpg`              |
| Finished ceramics     | `product-1.jpg` through `product-5.jpg`                  |
| Community / people    | `gallery-5.jpg`, opening party photos                     |

### Photo cropping rules
- Portrait of instructor: clip to rounded rectangle or circle, preserve face + hands.
- Workshop shots: clip to square or 4:5, crop to hands/clay level.
- Always use `preserveAspectRatio="xMidYMid slice"` in SVG image tags.
- Never stretch. Never letterbox with black bars.

---

## Ad Formats & Specs

| Format       | Dimensions | Canvas in SVG   | Use                              |
|--------------|------------|-----------------|----------------------------------|
| Instagram 4:5| 1080×1350  | `viewBox="0 0 1080 1350"` | Primary feed ad — most screen real estate |
| Instagram 1:1| 1080×1080  | `viewBox="0 0 1080 1080"` | Square feed, boosted posts        |
| Story / Reel | 1080×1920  | `viewBox="0 0 1080 1920"` | Full-screen vertical              |
| Flyer A5     | 148×210mm  | Use pt: 420×595pt | Print, always check footer visible |

**Meta text overlay rule:** keep text under 20% of image area for best algorithmic delivery. Large Costa headline is fine — it IS the visual. Avoid dense text blocks on top of photos.

**Story / Reel safe zones (1080×1920):**
- Top 250px (14%): keep clear — profile icon overlays here
- Bottom 340px (20%): keep clear — CTA and UI overlay here
- Active design zone: rows 250–1580 (middle 66%)

**Video vs static:** Video gets ~49% more engagement for awareness (upper funnel). Static performs better for conversion (lower funnel / retargeting). For Saged's current stage: use static image ads for direct response, video for brand awareness reels.

**Creative refresh:** Swap creative every 1–2 weeks to counter ad fatigue. Simple swaps (new photo, new headline colour, new CTA text) are sufficient — full redesign is not needed.

---

## Copy Principles (for ad text)

**The hook rule:** Users spend 1.7 seconds average on a mobile post. The headline must register in 0.25 seconds for memory encoding. Design for 0.25 seconds, not 1.7.

**The 5-second structure.** Every ad must answer three questions in order, within the frame:
1. What is this? → hero image + big headline
2. Why does it matter to me? → badge + body detail
3. What do I do next? → price blob + WhatsApp CTA

- **Headline:** 2–4 words in Costa. Tell them what it IS.
  - Good: `CERAMICS IN VALENCIA` / `КЕРАМИКА С КОРИЦЕЙ`
  - Bad: `Discover the art of handmade pottery`
- **Badge:** day/frequency + location. That's it.
- **Body:** max 7–8 words per line, 2 lines total. What they get.
- **Price:** always in the orange blob, always visible without scrolling.
- **CTA:** WhatsApp first. saged.club second.

**Character limits by placement (Meta spec):**
| Placement | Primary text | Headline |
|---|---|---|
| Instagram Feed | 125 chars | 40 chars |
| Instagram Stories | 125 chars | 40 chars |
| Facebook Feed | 125 chars | 27 chars |

Only ~1% of users tap "See More" — front-load everything in the first 80–100 characters.

### Audience-specific copy notes
- **RU/UA ads:** larger Costa headline (they're the core target), Koritsia as face.
- **EN ads:** same structure, "CERAMICS IN VALENCIA" headline, explicitly mention English-language instruction.

---

## Gestalt Principles (named tools for layout decisions)

These are the six perception laws that govern how viewers read a composition. Use them by name when making layout decisions.

| Principle | What it means | How to use it in Saged ads |
|---|---|---|
| **Proximity** | Elements close together are perceived as a group | Keep headline + sub-headline tight. Separate price blob from body text — it's independent |
| **Figure-Ground** | Viewers separate foreground (subject) from background | Never place instructor photo on a busy background — use cream or a solid overlay |
| **Similarity** | Same colour/shape/style = related | All brand figures share the same style → they read as "brand texture" together |
| **Continuity** | Eye follows smooth paths | Point arrows and gazes toward the headline or CTA. "KORITSIA →" arrow leads eye to the name |
| **Closure** | Viewers mentally complete cut-off shapes | Cropping the instructor's photo at the frame edge creates curiosity — use it intentionally |
| **Symmetry** | Symmetrical = stable; asymmetrical = dynamic | Saged is dynamic — asymmetric layouts with scattered figures are on-brand |

---

## Design Process

For every new design task, in this order:

1. **Read the brief** — format, audience, message, deadline.
2. **Check existing work** — open brand board, look at closest existing ad as reference.
3. **Choose photo** — pick from library before writing any SVG. The photo drives the layout.
4. **Write copy first** — headline (Costa, 2–4 words), badge, body (2 lines), price. Lock these before positioning.
5. **Build SVG** — use the ad anatomy template above. Fill in from top to bottom.
6. **Place figures last** — after all content is positioned, scatter 3–5 figures at edges.
7. **Check the 1-second rule** — headline readable instantly? Price visible? Logo present?
8. **Share for feedback** — open in Chrome, screenshot, show Diana.

---

## Self-Evaluation Checklist

Before calling a design done, check every item:

**Brand**
- [ ] Costa font loaded from correct path (`assets/fonts/costa-light.otf`)
- [ ] Logo orange `#FF7A23` used for primary accent (not `#9F4D2D`)
- [ ] Logo mark in top-right corner
- [ ] "SAGED CLUB" small-caps label in top-left
- [ ] Brand figures at edges only (3–5, opacity 0.45–0.60, not centred)
- [ ] No more than 2 font families

**Hierarchy**
- [ ] Squint test: headline or instructor face reads first
- [ ] 5-second rule: What? / Why me? / What next? — all three answered
- [ ] Maximum 3 primary focal points (headline + photo + price)
- [ ] Price in orange blob, visible without scrolling

**Technical**
- [ ] No double-hyphens inside SVG XML comments (breaks parser)
- [ ] `preserveAspectRatio="xMidYMid slice"` on all photo `<image>` tags
- [ ] Text under 20% of canvas area
- [ ] Body text 24px minimum; labels 18px minimum
- [ ] Text contrast 4.5:1 minimum (no light text on light background)
- [ ] Address + WhatsApp in bottom-left for ads that run in Valencia

**Story/Reel only**
- [ ] Top 250px clear (profile icon zone)
- [ ] Bottom 340px clear (CTA overlay zone)

---

## What NOT to Do

- Do not use `#9F4D2D` terracotta as the main accent in ads — that's web-only.
- Do not centre brand figures — they go at edges.
- Do not use any font other than Costa, Saged Cyrillic, or Inter — these are the only three brand typefaces.
- Do not use stock-feeling compositions (hero image + text overlay). Saged is editorial, not banner-ad.
- Do not fill the canvas. Cream space is intentional.
- Do not use `window.open()` for WhatsApp links in JS — use anchor-click pattern (see CLAUDE.md).
- Do not use `--` inside SVG XML comments.
- Do not create text-heavy ads. If it needs more than 6 lines of text, split into two pieces.

---

## Session Start for Design Tasks

1. Read this file.
2. Read `creative/brand-board.html` (visual reference — open in browser).
3. Check `creative/library/` for any reference ad that matches the format needed.
4. Ask Diana for the brief if not given: audience, format, message, any specific photo to use.
5. Build.

---

_Last updated: 2026-08-29_
_Maintained by Fergie. Update after every design session that produces new learnings._

### Research sources integrated (2026-08-29)
- W3C Design Token Format + three-tier token hierarchy (Global → Alias → Component)
- Fors Marsh Group: 0.25s memory encoding window, 1.7s mobile dwell time
- Meta ad copy specs 2026 (character limits per placement)
- Digital Marketing Laboratory: 60-30-10 rule, 3-element rule, Z-pattern, type scale ratios
- WCAG contrast standards + CTR uplift at 6:1–8:1 CTA contrast
- Gestalt principles applied to social ad composition
- Meta Stories/Reels safe zone specs (250px top / 340px bottom)
