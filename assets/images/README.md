# Images

Drop image files here matching these names — the HTML references them directly:

| Filename | Purpose | Recommended | Notes |
|---|---|---|---|
| `hero-placeholder.jpg` | Hero (right column) — hands-on-clay or finished piece | 4:5 ratio, ~1200×1500px, <300KB | Will become a short looping video later (`hero.mp4`); see GitHub issues |
| `koritsya-placeholder.jpg` | Portrait of Koritsya in the studio | 1:1, ~1000×1000px | Natural light, working, not posed |
| `gallery-1.jpg` ... `gallery-4.jpg` | Past workshop moments | 1:1, ~800×800px | Real participants + finished pieces |
| `og-cover.jpg` | Social-share preview (Open Graph) | 1200×630px | One strong image — used when someone shares the link |

## Format guidance
- Prefer **WebP** (smaller files); JPG works too.
- Compress before committing — TinyPNG or Squoosh.app.
- No raw RAW/HEIC files; convert first.

## Until Diana provides real images
The site references the placeholders by name. If a file doesn't exist, the browser shows a broken image icon — that's fine for local preview but should be fixed before launch. The CSS gives `<img>` slots a sandy background tint so empty boxes still look intentional.
