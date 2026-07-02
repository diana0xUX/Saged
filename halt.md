# Halt — 2026-07-02

## Where we stopped

Reviewed live site (both RU and UA confirmed healthy). Pulled Meta ads stats for June 5–July 2.

---

## What was done this session

1. **Live site check** — fetched saged.club and saged.club/ua/ and saged.club/uk/ (redirect stub). All healthy. Nav, hero, trust strip, offerings, about all present and correct on both language versions. /uk/ redirects to /ua/ as expected.

2. **Meta ads stats — June 5 to June 29:**
   - Total spend: **€372**
   - Total clicks: **1,653**
   - Impressions: ~223,000
   - Campaign-attributed conversions: **0** (every week, all month)
   - Best creative: Instagram post "Дитячі майстер-класи..." — 4.8–5.4% CTR at €0.08/click
   - Worst: Cacao & Sound RU campaign — 0.19% CTR, frequency 6.16, €62 spent with 0 result
   - Weekly reports flag "Verify Custom Conversion is still active in Events Manager" — never confirmed fixed

---

## Current state

- Branch: main
- Last commit: `636a6e1` — halt notes
- Build status: live and healthy
- Open review: none

---

## Next steps (in order)

1. **Check Custom Conversion in Meta Events Manager** — weekly reports have flagged this every week. If it's broken, Meta has no signal and is spending blind. Go to Events Manager → Custom Conversions and confirm it's active.
2. **Add real testimonials** — trust strip uses stats. One real student quote near the CTA is the highest-leverage conversion improvement still pending.
3. **Google Business Profile** — Diana to do at business.google.com. #1 SEO priority, still pending.
4. **Cacao & Sound campaign** — 0.19% CTR, freq 6.16. Either kill it or refresh creative before spending more.
5. **Cigun price** — never confirmed, not shown on events card.
6. **Spanish page** (`/es/`) — to catch "taller cerámica Valencia" searches.

## Context hard to re-derive

- Coworking price (€200/month) is intentionally hidden from all public pages — Diana's decision.
- `hreflang="uk"` stays as-is — ISO language code for Ukrainian is correct. Only the URL path was changed to `/ua/`.
- Sensitive local files (leeds/ WhatsApp exports, data/customers.csv) should NEVER be committed to GitHub.
- The 0 conversion problem persists all month. Clicks are happening (1,653 total) but Pixel PageViews in daily reports are nearly zero (2–25/day). Likely cause: people decline consent so Pixel can't fire, or they bounce before page loads. Custom Conversion check is the first diagnostic step.

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
