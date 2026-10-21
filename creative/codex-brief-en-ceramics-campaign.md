# Codex Brief — EN Ceramics Ad Campaign
## Saged.club · Meta Ads · 3-format SVG set

**Agent:** Read this entire file before writing any code. Do not skim.
**Working directory:** `/Users/diana/Documents/saged.club/`
**Existing reference:** `creative/ad-en-ceramics-v4.svg` — this is Format 1 at v4. Your job is to produce the full 3-format set, using v4 as the structural template.

---

## Task Summary

Produce three SVG ad files for a Meta (Facebook + Instagram) campaign targeting English-speaking expats in Valencia. Each file is a standalone SVG at the specified canvas size. All three share the same visual system — colour tokens, fonts, brand figures, copy — adapted per canvas.

Output files (write to `creative/`):
```
creative/ad-en-ceramics-feed-4x5.svg      1080 × 1350px  (Instagram 4:5 feed — iterate from v4)
creative/ad-en-ceramics-feed-1x1.svg      1080 × 1080px  (Facebook + Instagram square)
creative/ad-en-ceramics-story-9x16.svg    1080 × 1920px  (Stories + Reels)
```

---

## Design Tokens — Use these exact values everywhere

```
Background  #F9F4ED   canvas fill, page base
Sand        #F1E9DA   secondary bg (not used in ads)
Ink         #2A2520   primary text, dark badges, WhatsApp CTA bar
Muted       #6B5F54   body copy, address, secondary text
Orange      #FF7A23   price blob, schedule badge, headline accent line, sparkle
Line        #E1D6C5   dividers, footer rule
```

**Fonts:**
```
Costa Light   src: ../assets/fonts/costa-light.otf   display headlines, sub-labels, footer domain
Inter         system/Google Fonts                    body copy, badge labels, CTA, handle
```

**Font stack fallback for SVG:**
```
font-family: 'Costa', Georgia, serif
font-family: Inter, sans-serif
```

---

## Assets — File Paths

All paths are relative to the SVG file location in `creative/`.

```
Photo (primary):         ../assets/images/workshop-teaching.jpg
Logo SVG:                ../assets/images/logo-saged-club.svg
Symbols strip:           ../assets/images/saged-symbols.svg
Figure 1  (left edge):   ../assets/images/figures/figure%201.png
Figure 6  (lower-left):  ../assets/images/figures/figure%206.png
Figure 22 (right edge):  ../assets/images/figures/figure%2022.png
Figure 23 (lower-right): ../assets/images/figures/figure%2023.png
Figure 27 (right-low):   ../assets/images/figures/figure%2027.png
```

**Encoding rule:** All figure filenames have spaces. Always encode as `%20` in `href` attributes. Never use raw spaces in SVG `href` values — they break image loading silently.

**Photo crop rule:** All photo `<image>` elements must use `preserveAspectRatio="xMidYMid slice"` and be clipped with a `<clipPath>` containing a `<rect rx="24">` for rounded corners.

---

## Copy — Verbatim. Do Not Change.

```
Header label:       SAGED CLUB                  (Costa, small-caps weight, letter-spacing 6)
Headline line 1:    CERAMICS                     (Costa, fill #2A2520)
Headline line 2:    IN VALENCIA                  (Costa, fill #FF7A23)
Positioning pill:   IN ENGLISH                   (Inter 500, fill #F9F4ED, bg #2A2520, pill shape)
Schedule badge:     EVERY THURSDAY               (Costa, fill #F9F4ED, bg #FF7A23, pill shape)
Schedule sub:       OLD CITY · VALENCIA          (Inter, fill #F9F4ED, opacity 0.9)
Course title:       2-day pottery course         (Costa, fill #2A2520)
Body line 1:        Throw · glaze · take your piece home    (Inter, fill #6B5F54)
Body line 2:        Small group · all materials included    (Inter, fill #6B5F54)
Price:              €60                          (Costa, fill #F9F4ED, inside orange ellipse)
Price sub:          2 sessions · 2h each · up to 6         (Inter, fill #F9F4ED)
Photo label:        KORITSIA →                   (Costa, fill #9F4D2D)
Address:            C/ de la Correu, 8 · Casco Antiguo, Valencia  (Inter, fill #6B5F54)
CTA:                WhatsApp +34 695 73 19 00 →  (Inter 500, fill #F9F4ED, bg #2A2520)
Footer domain:      saged.club                   (Costa, fill #2A2520, letter-spacing 1)
Footer handle:      @saged_diana                 (Inter, fill #6B5F54, text-anchor end)
Sparkle:            ✦                            (Unicode U+2726, Inter, fill #FF7A23)
```

---

## SVG Technical Rules

1. **No `--` inside XML comment bodies.** `<!-- --- SECTION --- -->` is illegal XML. Chrome parses `--` as comment close and throws a parse error. Use `<!-- SECTION -->` only.
2. **Document render order = z-order.** Elements later in the document render on top. Background first, figures last. The "IN ENGLISH" pill and photo label must appear AFTER the `<image>` photo element in document order, or the photo renders over them.
3. **No raw spaces in href.** `href="../assets/images/figures/figure 1.png"` breaks. Use `figure%201.png`.
4. **Font face declaration** goes in `<defs><style>`. Load Costa only — Inter is a system font, no `@font-face` needed.
5. **ClipPath IDs** must be unique per file. Use `id="photo-clip-4x5"`, `id="photo-clip-1x1"`, `id="photo-clip-9x16"` respectively.

---

## Format 1 — 4:5 Feed `1080 × 1350`

**File:** `creative/ad-en-ceramics-feed-4x5.svg`
**Base:** `creative/ad-en-ceramics-v4.svg` — copy this and apply any improvements. The layout is already correct.

Exact layout from v4 (all coordinates verified):

```
Canvas:           1080 × 1350
Margin:           60px left/right

HEADER ROW (y ≈ 28–88)
  "SAGED CLUB"    x=60, y=66, font-size=22, letter-spacing=6
  Logo SVG        x=892, y=28, width=132, height=60

HEADLINE (y ≈ 100–380)
  "CERAMICS"      x=60, y=208, font-size=172, letter-spacing=-5, fill=#2A2520
  "IN VALENCIA"   x=60, y=378, font-size=172, letter-spacing=-5, fill=#FF7A23

PHOTO ZONE (left column)
  ClipPath rect:  x=60, y=330, width=480, height=540, rx=24
  <image>:        x=60, y=330, width=480, height=540
  preserveAspectRatio="xMidYMid slice"

IN ENGLISH pill (rendered AFTER photo element)
  <rect>:         x=60, y=396, width=248, height=44, rx=22, fill=#2A2520
  <text>:         x=184, y=424, text-anchor=middle, font-size=19, font-weight=500, letter-spacing=2

KORITSIA label (rendered AFTER photo element)
  x=220, y=325, text-anchor=middle, font-size=22, fill=#9F4D2D

RIGHT COLUMN (x starts at 576)
  Thursday badge: rect x=576, y=500, width=448, height=84, rx=42, fill=#FF7A23
    "EVERY THURSDAY"  x=800, y=549, text-anchor=middle, font-size=30, letter-spacing=1
    "OLD CITY · VALENCIA" x=800, y=572, text-anchor=middle, font-size=15, letter-spacing=1, opacity=0.9

  Course title:   x=576, y=648, font-size=32
  Body line 1:    x=576, y=698, font-size=23
  Body line 2:    x=576, y=730, font-size=23

  Sparkle ✦:      x=560, y=800, font-size=28, fill=#FF7A23

  Price ellipse:  cx=790, cy=860, rx=190, ry=98, fill=#FF7A23
    "€60":        x=790, y=842, text-anchor=middle, font-size=68
    price sub:    x=790, y=876, text-anchor=middle, font-size=17

DIVIDER
  <line>:         x1=60, y1=1004, x2=1020, y2=1004, stroke=#E1D6C5, stroke-width=1.5

BOTTOM STRIP (y 1004–1274)
  Address:        x=60, y=1046, font-size=19
  WhatsApp rect:  x=60, y=1064, width=580, height=72, rx=10, fill=#2A2520
  WhatsApp text:  x=350, y=1109, text-anchor=middle, font-size=22, font-weight=500
  Symbols strip:  x=60, y=1164, width=440, height=68, opacity=0.16

FOOTER (y 1274–1350)
  Rule:           x1=60, y1=1274, x2=1020, y2=1274, stroke=#E1D6C5, stroke-width=1
  "saged.club":   x=60, y=1314, font-size=28, letter-spacing=1
  "@saged_diana": x=1020, y=1314, text-anchor=end, font-size=20

FIGURES (document-final, render on top of background/behind text)
  figure%201.png  x=-15,  y=100,  width=130, height=165, opacity=0.48
  figure%2022.png x=928,  y=140,  width=120, height=155, opacity=0.46
  figure%2027.png x=932,  y=900,  width=115, height=148, opacity=0.46
  figure%206.png  x=24,   y=1060, width=108, height=140, opacity=0.44
  figure%2023.png x=640,  y=1120, width=100, height=128, opacity=0.40
```

---

## Format 2 — Square Feed `1080 × 1080`

**File:** `creative/ad-en-ceramics-feed-1x1.svg`
**Rule:** 270px shorter than 4:5. Compress the layout — headline + photo share the top half, info block in the bottom half. Price blob must remain visible without scrolling.

Layout target:

```
Canvas:           1080 × 1080
Margin:           60px left/right

HEADER ROW  y=28–72
  "SAGED CLUB"    x=60, y=60, font-size=20, letter-spacing=6
  Logo SVG        x=892, y=24, width=120, height=54

HEADLINE  (condensed — font-size 130 fits both words on canvas)
  "CERAMICS"      x=60, y=160, font-size=130, letter-spacing=-4, fill=#2A2520
  "IN VALENCIA"   x=60, y=300, font-size=130, letter-spacing=-4, fill=#FF7A23

PHOTO ZONE (left column, shorter)
  ClipPath rect:  x=60, y=272, width=440, height=400, rx=20
  <image>:        x=60, y=272, width=440, height=400
  preserveAspectRatio="xMidYMid slice"

IN ENGLISH pill (AFTER photo element)
  <rect>:         x=60, y=332, width=220, height=40, rx=20, fill=#2A2520
  <text>:         x=170, y=357, text-anchor=middle, font-size=17, font-weight=500, letter-spacing=2

KORITSIA label (AFTER photo element)
  x=200, y=268, text-anchor=middle, font-size=18, fill=#9F4D2D

RIGHT COLUMN (x=532, width=488)
  Thursday badge: rect x=532, y=330, width=492, height=72, rx=36, fill=#FF7A23
    "EVERY THURSDAY"  x=778, y=375, text-anchor=middle, font-size=26, letter-spacing=1
    "OLD CITY · VALENCIA" x=778, y=395, text-anchor=middle, font-size=13, opacity=0.9

  Course title:   x=532, y=502, font-size=26
  Body line 1:    x=532, y=540, font-size=20
  Body line 2:    x=532, y=566, font-size=20

  Price ellipse:  cx=760, cy=670, rx=170, ry=86, fill=#FF7A23
    "€60":        x=760, y=652, text-anchor=middle, font-size=58
    price sub:    x=760, y=684, text-anchor=middle, font-size=14

DIVIDER         x1=60, y1=778, x2=1020, y2=778, stroke=#E1D6C5, stroke-width=1.5

BOTTOM STRIP  y=778–1080
  Address:        x=60, y=814, font-size=16
  WhatsApp rect:  x=60, y=832, width=580, height=64, rx=10, fill=#2A2520
  WhatsApp text:  x=350, y=871, text-anchor=middle, font-size=20, font-weight=500
  Symbols strip:  x=60, y=918, width=380, height=56, opacity=0.14

FOOTER
  Rule:           x1=60, y1=1032, x2=1020, y2=1032, stroke=#E1D6C5, stroke-width=1
  "saged.club":   x=60, y=1066, font-size=24, letter-spacing=1
  "@saged_diana": x=1020, y=1066, text-anchor=end, font-size=17

FIGURES
  figure%201.png  x=-12, y=80,  width=110, height=140, opacity=0.48
  figure%2022.png x=938, y=110, width=105, height=135, opacity=0.46
  figure%2027.png x=940, y=730, width=100, height=128, opacity=0.44
  figure%206.png  x=20,  y=848, width=92,  height=118, opacity=0.42
```

---

## Format 3 — Story / Reels `1080 × 1920`

**File:** `creative/ad-en-ceramics-story-9x16.svg`
**Rule:** Full-screen vertical. Keep top 250px and bottom 340px empty — Meta UI overlays this zone. Active design runs rows 250–1580. Simpler than the feed formats — the photo dominates, copy is minimal.

Layout target:

```
Canvas:           1080 × 1920
Safe zone top:    0–250px     (keep empty — Meta profile icon overlay)
Safe zone bottom: 1580–1920px (keep empty — Meta CTA button overlay)
Active zone:      250–1580px  (all design lives here)
Margin:           60px left/right

HEADER (inside safe zone — keep minimal, logo only)
  Logo SVG:       x=892, y=30, width=120, height=54
  "SAGED CLUB":   x=60, y=56, font-size=18, letter-spacing=6, fill=#2A2520

HEADLINE (top of active zone)
  "CERAMICS"      x=60, y=380, font-size=160, letter-spacing=-5, fill=#2A2520
  "IN VALENCIA"   x=60, y=550, font-size=160, letter-spacing=-5, fill=#FF7A23

PHOTO (large, full-width, centre of canvas)
  ClipPath rect:  x=0, y=560, width=1080, height=720, rx=0   (full bleed, no radius)
  <image>:        x=0, y=560, width=1080, height=720
  preserveAspectRatio="xMidYMid slice"

IN ENGLISH pill (AFTER photo element)
  <rect>:         x=60, y=618, width=260, height=52, rx=26, fill=#2A2520
  <text>:         x=190, y=650, text-anchor=middle, font-size=22, font-weight=500, letter-spacing=2

KORITSIA label (AFTER photo element)
  x=240, y=608, text-anchor=middle, font-size=22, fill=#9F4D2D

INFO BLOCK (below photo)
  Thursday badge: rect x=60, y=1316, width=450, height=70, rx=35, fill=#FF7A23
    "EVERY THURSDAY"   x=285, y=1358, text-anchor=middle, font-size=28, letter-spacing=1
    "OLD CITY · VALENCIA" x=285, y=1376, text-anchor=middle, font-size=13, opacity=0.9

  Body line 1:    x=60, y=1430, font-size=26, fill=#6B5F54
  Body line 2:    x=60, y=1462, font-size=26, fill=#6B5F54

PRICE (bottom-right of active zone)
  Price ellipse:  cx=880, cy=1430, rx=160, ry=80, fill=#FF7A23
    "€60":        x=880, y=1413, text-anchor=middle, font-size=62
    price sub:    x=880, y=1447, text-anchor=middle, font-size=14

DIVIDER (top of safe zone floor)
  <line>:         x1=60, y1=1530, x2=1020, y2=1530, stroke=#E1D6C5, stroke-width=1.5

BOTTOM STRIP (inside safe zone — only WhatsApp, nothing else)
  WhatsApp rect:  x=60, y=1548, width=700, height=68, rx=10, fill=#2A2520
  WhatsApp text:  x=410, y=1590, text-anchor=middle, font-size=24, font-weight=500

FIGURES (scattered at edges, inside active zone only)
  figure%201.png  x=-18, y=280,  width=140, height=180, opacity=0.46
  figure%2022.png x=940, y=320,  width=125, height=160, opacity=0.44
  figure%2027.png x=940, y=1200, width=120, height=154, opacity=0.44
  figure%206.png  x=24,  y=1310, width=110, height=140, opacity=0.40
```

Note: no footer line or `@saged_diana` handle in the story format — that zone is covered by Meta UI.

---

## Document Structure (all 3 formats)

Write elements in this exact order (top of file = bottom of z-stack):

```
1. <defs>  — @font-face, clipPath
2. Background <rect>
3. Right-column content (badges, body, price) — before photo so photo renders on top in overlap zone
4. <image> photo element — renders on top of headline overlap zone
5. "IN ENGLISH" pill — AFTER photo, so it renders on top of the photo
6. "KORITSIA →" label — AFTER photo
7. Header "SAGED CLUB" text and logo
8. Headline lines
9. Sparkle ✦
10. Divider line
11. Bottom strip (address, WhatsApp bar)
12. Symbols strip
13. Footer rule + text
14. Brand figures — LAST in document (renders over background, under text elements above it)
```

Wait — re-evaluate: header, headline, and body text must render OVER the figures. Figures must appear BEFORE text elements in the document. Correct final order:

```
1. <defs>
2. Background <rect>
3. Brand figures (appear early = render behind everything else)
4. Header "SAGED CLUB" + logo
5. Headline lines
6. Right-column content (badges, body, price ellipse)
7. <image> photo
8. "IN ENGLISH" pill (AFTER photo)
9. "KORITSIA →" label (AFTER photo)
10. Sparkle ✦
11. Divider line
12. Bottom strip
13. Symbols strip
14. Footer
```

---

## Self-Evaluation Checklist

Run through every item before writing output files.

**Brand**
- [ ] Costa font loaded via `@font-face` in `<defs><style>`, path `../assets/fonts/costa-light.otf`
- [ ] Accent colour is `#FF7A23` (orange). `#9F4D2D` is used only on "KORITSIA →" label.
- [ ] Logo SVG in top-right corner on all 3 formats
- [ ] "SAGED CLUB" small-caps label in top-left on all 3 formats
- [ ] Brand figures at edges only — not centred, not over text
- [ ] Only 2 font families: Costa and Inter

**Copy**
- [ ] "IN ENGLISH" pill present on all 3 formats, rendered after photo element
- [ ] "EVERY THURSDAY" badge present on all 3 formats
- [ ] Price blob `€60` visible on all 3 formats without needing to scroll
- [ ] WhatsApp CTA `+34 695 73 19 00` present on all 3 formats
- [ ] "KORITSIA →" label present, fill `#9F4D2D` (this is the one allowed use of terracotta)

**Technical**
- [ ] No `--` inside any SVG XML comment body
- [ ] All figure hrefs use `%20` not raw spaces
- [ ] All photo `<image>` elements have `preserveAspectRatio="xMidYMid slice"`
- [ ] All photo `<image>` elements use a `<clipPath>` with `<rect rx="…">`
- [ ] ClipPath IDs are unique across files (`photo-clip-4x5`, `photo-clip-1x1`, `photo-clip-9x16`)
- [ ] Story format: no design elements in top 250px or bottom 340px (beyond header logo/label)
- [ ] Background fill `#F9F4ED` on all 3 (not white `#FFFFFF`, not `#FFF`)

**Layout**
- [ ] Squint test: headline and price blob are the two dominant reads
- [ ] "IN ENGLISH" pill visually prominent — not buried
- [ ] WhatsApp CTA is the single CTA — no website link in the main CTA zone

---

## What Not to Do

- Do not use `#9F4D2D` for badges, blobs, or CTAs — that hex is web-only and only appears once in ads (the KORITSIA label)
- Do not place `--` inside XML comment bodies
- Do not use raw spaces in `href` attribute values for figure images
- Do not place the "IN ENGLISH" pill before the `<image>` element in document order — it will be hidden behind the photo
- Do not add fonts beyond Costa and Inter
- Do not put any design elements in the story safe zones (top 250px / bottom 340px)
- Do not hardcode `width` and `height` on the SVG root without a matching `viewBox`

---

_This brief targets an AI coding agent. Every value is specified. If a value is missing or ambiguous, derive it from the v4 reference at `creative/ad-en-ceramics-v4.svg` — that file is ground truth for the 4:5 format._
