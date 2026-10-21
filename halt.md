# Halt — 2026-10-21

## Where we stopped

Completed the full Cal.com → NocoDB handpan booking pipeline. Netlify webhook is live.
Context limit hit right after confirming the deployment.

## Current state

### Handpan booking pipeline — COMPLETE ✅
- Landing page: `/handpan/index.html` — 5 spots, €25/€30/€100 pricing, Denys Balykhin teacher, SVG euro sign
- Cal.com event: `saged-club/handpan` (Sunday 12:00, 5 spots)
- Webhook: `https://reliable-kulfi-f7d3f9.netlify.app/api/calcom-webhook` (live on Netlify)
- Cal.com webhook ID: `3a440ff8-9c01-4582-937d-c7b0a43221c8` (trigger: BOOKING_CREATED)
- NocoDB table: "Booking Handpan School" (`mzerh9imrwgjmuf`)

### Manual steps Diana still needs to do
1. **Stripe on Cal.com**: Cal.com → Event Types → Handpan → Apps tab → Stripe → Enable → €30 → ON_BOOKING → tick "Allow promotion codes" → Save
2. **Promo code in Stripe**: Create coupon for first-class €25 in Stripe Dashboard
3. **NocoDB Clients link**: Booking Handpan School → + Add field → Link → Clients table
4. **Denys photo**: Save his photo to `/assets/images/denys-balykhin.jpg`, update `/handpan/index.html` teacher img src

### Meta ads
- **Ceramics DM campaign** `120250092222100513` — ACTIVE
  - UA ad `120250092223630513` — ACTIVE (live)
  - RU ad `120250092222990513` — WITH_ISSUES (needs manual approval in Ads Manager)
- **Handpan School** `120250085902350513` — ACTIVE, €3/day, LINK_CLICKS
  - ⚠️ No destination URL — needs to point to `https://saged.club/handpan/`
- **Art Classes** `120250085874070513` — PAUSED
- **Old ceramics TRAFFIC** `120250086001120513` — PAUSED
- Total active daily budget: ~€9/day

### Materials Lab page
- Live at `https://saged.club/materials-lab/` — sent to Katya for review
- Yellow note boxes mark what she needs to fill in

### Association registration
- **ASINS/46/2026/0756** — Solicitud phase, no issues, expected Nov 2026 – Feb 2027

### Todo list (pinned doc)
- https://claude.ai/code/artifact/aa99256d-0a2a-441a-9972-0c81deef7298

## Next steps (in order)
1. **Diana**: Approve RU ceramics ad in Ads Manager — campaign `120250092222100513`, ad `120250092222990513`
2. **Diana**: Enable Stripe on Cal.com handpan event (see above)
3. **Fix handpan Meta campaign**: update ad destination URL to `https://saged.club/handpan/`
4. **Wait for Katya**: materials-lab → remove yellow boxes after her feedback

## Blockers
- RU ceramics ad needs Diana's manual approval click in Ads Manager
- Stripe + promo code need Diana's action in Cal.com and Stripe dashboards
