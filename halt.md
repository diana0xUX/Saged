# Halt — 2026-07-01

## Where we stopped

Ukrainian URL rename shipped (`/uk/` → `/ua/`), RU/UA home pages synced. Site is live.

---

## What was done this session

1. **`/uk/` → `/ua/` URL rename — fully shipped:**
   - `git mv uk ua` — directory renamed, all content preserved
   - Batch `sed` replaced all URL references across every HTML file
   - Backward-compat redirect stubs created at all old `/uk/` paths (meta refresh → `/ua/`)
   - `hreflang="uk"` language attribute left unchanged (ISO 639-1 correct, only URL path changed)
   - Committed and pushed as `f53b163`

2. **UA home page inconsistency fixed:**
   - Added missing `LocalBusiness` JSON-LD schema block (was in RU, missing from UA)
   - Removed stray blank line in UA lang nav (leftover from EN link removal)
   - Committed and pushed as `afb7eb6`

3. **Sensitive files kept out of git:**
   - `leeds/` WhatsApp chat exports — NOT committed, still local only
   - `data/customers.csv` — NOT committed, still local only
   - `hand building templates/`, `kids summer *.png` — NOT committed

## Current state

- Branch: main
- Last commit: `afb7eb6` — ua/index.html: add missing JSON-LD schema, fix nav whitespace
- Build status: pushed, GitHub Pages deploying
- Open review: none
- Live URLs: saged.club (RU) and saged.club/ua/ (UA)

---

## Next steps (in order)

1. **Review the live site** — check saged.club and saged.club/ua/ on both desktop and mobile.
2. **Add real testimonials** — trust strip uses stats. One real student quote near the CTA is the highest-leverage conversion improvement still not done.
3. **Google Business Profile** — Diana to do at business.google.com. #1 SEO priority still pending.
4. **Cigun price** — never confirmed, not shown on events card.
5. **Spanish page** (`/es/`) — to catch "taller cerámica Valencia" searches.

## Context hard to re-derive

- Coworking price (€200/month) is intentionally hidden from all public pages — Diana's decision.
- `workshop-1.jpg` chosen for hero because KNOWLEDGE.md flags it as strongest social card source.
- `hreflang="uk"` stays as-is — that's the ISO language code for Ukrainian and is correct for SEO. Only the URL path was changed from `/uk/` to `/ua/`.
- Sensitive local files (leeds/ WhatsApp exports, data/customers.csv) should NEVER be committed to GitHub.

---

## Carry-over from previous halts

- **Google Business Profile** — Diana to do at business.google.com. Requires postcard verification.
- **Spanish page** (`/es/`) — to catch "taller cerámica Valencia" searches
- **Cigun price** — never confirmed, no price shown on event card
- **Send accountant report to gestor** — `finances/reports/june-2026-accountant.md`
- **ROI registration** — gestor to confirm; file Model 036 if not registered
- **Korytsia €355** — still outstanding (€267.50 + €87.50)
- **July rent ~€1,173** — due ~Jul 5. Critical.

---

## What to read first on resume

1. This file
2. CLAUDE.md
3. KNOWLEDGE.md
