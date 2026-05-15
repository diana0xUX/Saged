# Thursday-class flyer

Two-sided A5 flyer for the **Керамика с Корицей** / **Кераміка з Корицею** Thursday workshop.

- **Side 1**: Ukrainian (front)
- **Side 2**: Russian (back)
- Identical layout, mirrored content
- Size: A5 portrait (148 × 210 mm)
- Includes QR code linking to `https://cal.com/saged-club/ceramics`

## How to print

1. Open `flyer/index.html` in Chrome (or any modern browser)
2. **Cmd + P** → choose **Save as PDF** as the destination
3. In *More settings*, set:
   - Paper size: **A5**
   - Margins: **None** (the flyer has its own internal margins)
   - Scale: **100%** (no shrink-to-fit)
   - Background graphics: **ON** (so the cream + terracotta colors print)
4. Save → you get a 2-page PDF
5. Send to a print shop, or print at home double-sided (flip on long edge)

## How to share digitally

Just send the saved PDF, or share `saged.club/flyer/` after deploy (won't deploy by default — flyer is gitignored from GitHub Pages indexing; share directly).

## To edit

- **Copy / wording**: edit `index.html` directly. Each side is a `<section class="side" lang="...">` — RU and UA are clearly delimited.
- **Photo**: change the `src` on both `<img class="photo">` tags. Default is `../assets/images/hero-1.jpg` (Koritsa teaching at table).
- **QR code**: regenerate via:
  ```bash
  python3 -c "import segno; segno.make('https://cal.com/saged-club/ceramics', error='h').save('qr-booking.svg', scale=10, border=2, dark='#3a2615', light=None)"
  ```
  Change the URL inside the parens to retarget. (Requires `pip3 install segno` once.)
- **Colors / fonts**: tokens live in the `<style>` block. Color values:
  - `#faf6f0` — cream background
  - `#b85c38` — terracotta accent
  - `#2a1b10` — body text
  - `#f1e9dd` — sand block

## Bilingual mirror note

Both sides MUST stay synchronized. If you edit one, edit the other. Same as the main site's `index.html` / `uk/index.html` rule.
