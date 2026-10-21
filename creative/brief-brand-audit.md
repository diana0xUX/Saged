# Brand Audit Brief — Saged.club
**For:** Freelance UI/brand designer
**Deliverable:** Audit report + proposed design changes
**Reference:** `creative/SAGED-SOURCE-OF-TRUTH.md` — read this first, it covers the business, audience, and full asset inventory

---

## What is Saged

A ceramic and cultural workshop space in the old city of Valencia, Spain. Real physical studio, owner-operated. People come to the address, make pottery, and leave with something they created. The studio also runs cultural events (sound healing, breathwork, tea ceremonies). Opens 2026.

Owner: Diana Sage — product designer and ceramicist (working with clay since COVID). Built this from scratch, handles brand and marketing herself.

Primary audience: Russian and Ukrainian-speaking women, 25–45, long-term Valencia residents.
Secondary: English-speaking expats (discovered via paid Meta ads).

**Website:** [saged.club](https://saged.club) — live, in production.

---

## Scope of Audit

You are auditing the visual brand as it exists across two surfaces:

### Surface 1 — Website (saged.club)
A live site built in vanilla HTML/CSS/JS, no framework, no build step. Hosted on GitHub Pages.

Pages:
- `/` — Russian landing (primary)
- `/uk/` — Ukrainian landing (must stay identical structure to RU)
- `/en/` — English section
- `/kids/` — kids ceramics
- `/coworking/` — hot desk page
- `/events/` — events
- `/studio/` — studio page
- `/gifts/` — gift certificates

### Surface 2 — Ad Creative
Instagram feed ads (1080×1350 px), built as SVG files.

Reference creative at `creative/library/05-ads/`:
- `koritsia-ceramics/` — the reference standard, the design to beat
- `en-ceramics/ad-en-ceramics-v4.svg` — current in-progress English version
- `kids-ceramics/` — 6 format variants

---

## Brand Assets Available

Everything is at `creative/library/`. Start with the visual reference:

```
creative/brand-board.html        Open in Chrome — shows all colours, type, logos, figures, photos side by side
creative/library/01-brand/       Colours (PNG swatches), fonts, logo variants
creative/library/02-figures/     41 illustrated character figures
creative/library/03-photos/      All photography (hero, workshop, instructor, gallery, products, opening party)
creative/library/04-social/      Instagram post and story exports
creative/library/05-ads/         All ad creative (SVG source + previews)
creative/DESIGNER.md             Machine-readable brand system — colour rules, type hierarchy, layout principles
```

---

## Known Issues to Investigate

These are documented problems. Your audit should confirm, quantify severity, and propose resolution for each.

### 1. Two accent colours doing the same job
- `#FF7A23` (logo orange) — used in ads, print, all SVG creative
- `#9F4D2D` (terracotta) — used on website for links, CTAs, buttons

These are visually distinct. They've never been reconciled. Someone landing from an ad sees orange; on the website they see terracotta. Not a two-tone system — an unresolved collision.

**Question to answer:** Should they merge into one accent, or be formalised as distinct contexts (print vs web)? If merged, which wins?

### 2. Costa font on website ✅ resolved
Costa Light is now the Latin display font on the website. Saged Cyrillic handles Cyrillic headings. Summer Font and Cormorant Garamond have been removed from all files.

### 3. Logo on dark backgrounds uses CSS invert
The website applies `filter: invert(1)` to produce a white version of the logo. This is a workaround — not a real white-on-dark asset.

A proper white SVG logo exists at `creative/library/01-brand/logos/logo-white.png`. The SVG file at `assets/images/logo-saged-club.svg` uses fill `#FF7A23` and is not designed for dark surfaces.

**Question to answer:** Is the current invert approach acceptable, or does the site need a properly rendered dark-mode logo implementation?

### 4. No brand guidelines document
Rules exist scattered across:
- `creative/DESIGNER.md` — machine-readable, for AI agents
- `creative/SAGED-SOURCE-OF-TRUTH.md` — business reference
- `CLAUDE.md` — project-level behavior rules

There is no single designed brand guide a human freelancer can open and trust. Each collaborator (Koritsia, Helena, Vita, future event organizers) has to be briefed verbally or by trial and error.

**Deliverable needed:** A usable one-page brand reference — colour values, font names, logo rules, do/don't examples. PDF or HTML, not just a markdown file.

### 5. Photo categorization error
`creative/library/03-photos/koritsia/koritsa-editorial.jpg` is a fashion editorial photo — woman with elaborate beaded necklace and feathers. It is labeled as an instructor photo and was accidentally used in early ad creative. Should be quarantined or relabeled so it's not used in ceramics ads.

### 6. No RU/UA adult ceramics ad
The only RU/UA ceramics ad that exists is the original Koritsia ad (`.ai` source only — not easily editable). There is no reproducible SVG workflow for producing RU/UA variants at different sizes. English ad has SVG v1–v4. Russian doesn't.

This is a creative gap, not a pure brand audit item — but flag it if you see it blocking campaign consistency.

---

## Constraints

**Technical (do not propose solutions that break these):**
- Website is vanilla HTML/CSS/JS — no React, no Tailwind, no build step. Changes must be plain CSS/HTML.
- Hosted on GitHub Pages — no server-side rendering, no backend.
- Font files must be self-hosted (no Adobe Fonts / Typekit — GDPR consent complexity). Google Fonts are fine.
- GDPR consent banner must fire before any Meta Pixel tracking. Do not touch or propose removing `consent` logic in `script.js`.
- RU landing (`index.html`) and UA landing (`uk/index.html`) must stay structurally identical — any layout change on one must be mirrored in the other.

**Creative:**
- Brand personality must stay: warm, handmade, playful, honest. Not minimalist-cold, not corporate, not tourist-brochure.
- Cream background (`#F9F4ED`) is load-bearing — it IS the warmth. Don't replace it with white.
- Costa font is non-negotiable for print/ad creative. If it comes onto the website, it comes at full weight — not as a supplementary accent.
- Brand figures (illustrated characters) stay — they are the texture of the brand.
- This is not a rebrand. It's a brand audit. Propose refinements, not replacement.

**Business:**
- Owner is one person with no design budget for a full system rebuild. Prioritise high-impact, low-effort fixes.
- The best-performing ad on record used English-language video + "Saged.club is for..." positioning. Whatever you propose should be compatible with that creative direction.
- Events are promoted organically only — never via paid ads. Any event-specific design changes don't need to be optimized for ad performance.

---

## What Good Looks Like

At the end of this audit, there should be:

1. **Audit report** — each of the 6 known issues assessed with a severity rating (critical / notable / minor) and a concrete recommendation. New issues you spot that aren't listed above are welcome — add them.

2. **Proposed changes document** — specific, implementable changes. Not "improve type hierarchy" — instead "Costa Light at 72px, letter-spacing −0.04em, colour `#2A2520`". Enough detail that a developer or Claude Code session can implement each change without further design input.

3. **One-page brand reference** — a designed PDF or HTML file showing: colour swatches with hex values, font names and weights, logo rules, do/don't examples. Should be something Diana can send to a new collaborator without needing to explain anything verbally.

4. **Priority order** — which changes should Diana do first? Ordered by: user-facing impact × implementation effort. The top 3 should be doable in a single working session.

---

## Tone and Process Notes

Diana is a product designer — she thinks in systems, components, and design tokens. You can use that language. She doesn't want to be walked through basics.

She doesn't speak Spanish and doesn't make phone calls. All communication should be written (email, DM, document comments).

She built this project herself. Be direct about problems — she'd rather know something is broken than have it softened. Don't oversell fixes; she'll know if the recommendation is bloated for the problem.

---

_Brief written: 2026-08-29_
_Contact: Diana Sage — WhatsApp +34 695 73 19 00 · @saged_diana_
