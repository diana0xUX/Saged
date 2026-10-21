# Skill — Instagram carousel: HTML → uploadable PNGs

_Last used: 2026-09-09 (september-carousel.html → Instagram slides)._

## Problem

Designing a carousel in HTML gives pixel-perfect control and brand consistency, but Instagram only accepts images — not HTML files. Going from `carousel.html` to uploadable slide PNGs requires a screenshot-per-slide pipeline. Doing it manually (browser screenshot, crop, repeat) is slow and loses quality.

Two landmines when skipping this:
- Screenshot at wrong resolution → slides look blurry on Retina / mobile
- Screenshotting the whole page (with nav dots, browser chrome) instead of the canvas only

## Specs to know before building

| Format | Dimensions | Aspect ratio | When to use |
|---|---|---|---|
| Square | 1080×1080 px | 1:1 | Older convention; less feed real-estate |
| **Portrait (recommended)** | **1080×1350 px** | **4:5** | More vertical space = more visible in feed |
| Story / Reel | 1080×1920 px | 9:16 | Full-screen stories |

Build at 1080×1350 by default. Saged carousels should use this unless there's a specific reason to go square.

## Recipe A — Python script (fastest, works on existing HTML)

**Tool:** [html-to-Instagram-carousel](https://github.com/DJ-vekariya/html-to-Instagram-carousel)

Zero config. Auto-installs Playwright + Chromium on first run.

**Requirements on the HTML:**
- Each slide must be a `.slide` element inside `.carousel-track` inside `.carousel-viewport` inside `.ig-frame`
- Nav dots, arrows, counter labels will be auto-hidden during export
- Fonts must load before screenshot — use local `@font-face` paths, not CDN (CDN may time out)

**Steps:**
```bash
# 1. Clone once
git clone https://github.com/DJ-vekariya/html-to-Instagram-carousel ~/tools/html-to-ig-carousel
cd ~/tools/html-to-ig-carousel
pip install -r requirements.txt   # installs playwright
playwright install chromium

# 2. Run on your carousel
python export.py --input /path/to/carousel.html --output /path/to/output-folder/

# 3. Output: slide-01.png, slide-02.png, … ready for Instagram
```

**How the resolution works:**
The script renders at a small viewport (420×525 px) then sets `device_scale_factor = 2.571` (1080÷420). The browser treats this like a Retina display — identical layout, full 1080 px output. No layout reflow or blurry upscaling.

## Recipe B — open-carrusel (full design app, more powerful)

**Tool:** [open-carrusel](https://github.com/Hainrixz/open-carrusel)

A local Next.js app: chat panel + live preview + filmstrip. You describe slides conversationally to Claude, watch them render live, drag-reorder, then export via Puppeteer. Supports 1:1, 4:5, 9:16 in one click.

Best for: designing new carousels from scratch with iterative chat. Overkill if you already have HTML.

```bash
git clone https://github.com/Hainrixz/open-carrusel ~/tools/open-carrusel
cd ~/tools/open-carrusel
npm install
npm run dev   # opens at localhost:3000
```

Set your brand config once (colors, fonts, tone); Claude reads it on every slide generation.

## Adapting september-carousel.html for export

Current carousel (`creative/september-carousel.html`) is 1080×1080 and uses custom nav. To make it compatible with Recipe A:

1. Change canvas to 1080×1350 (update `#canvasWrap` width/height and `.track` height)
2. Wrap the `.track` in `.ig-frame > .carousel-viewport > .carousel-track`
3. Add class `slide` to each existing `.slide` element
4. The script will hide the nav dots + arrows automatically

## Anti-patterns

- Screenshotting in a browser at display resolution — you get 144 px/inch on Retina but the PNG dimensions depend on your zoom level. Use the script.
- Building at 1080×1080 when 1080×1350 is available — you leave 25% of feed height on the table
- Hosting fonts on Google Fonts CDN in export HTML — Playwright may time out waiting; always use local `@font-face` paths
- Running export before checking that all `.slide` elements have a fixed height set — slides without explicit height may capture as 0 px
