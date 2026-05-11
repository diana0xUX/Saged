# Saged.club — Project Context

## What this is
A real client project: **Saged.club**, a ceramic and cultural workshop space in Valencia old city, marketing to **Russian-speaking and Ukrainian-speaking residents** of Valencia.

Phase 1 product: a single bilingual (RU/UA) landing page promoting **"Ceramics with Koritsya"** — a two-day pottery workshop.

## Owner
**Diana Sage**, UX designer. Plain-language explanations, design-world analogies preferred over engineering jargon.

## Status (as of 2026-05-11)
- Audit of past €105 of ads: ✅ complete (see `AUDIT.md`)
- GitHub repo: ✅ created — https://github.com/diana0xUX/Saged
- Vanilla JS landing page (RU + UA): ✅ v0 built
- GitHub Pages: ✅ enabled, custom domain `saged.club` set
- DNS: ⏳ pending Diana
- Real images: ⏳ pending Diana
- Booking integration: ⏳ pending Cal.com setup
- Meta Pixel: ⏳ pending creation
- New ad campaign: ⏳ blocked by all of the above

## File map
- `index.html` — Russian landing
- `uk/index.html` — Ukrainian landing
- `assets/style.css`, `assets/script.js`, `assets/images/` — front-end assets
- `privacy.html`, `cookies.html` — legal stubs (need real text before launch)
- `CNAME` — `saged.club`
- `AUDIT.md` — findings from the Phase 0 ad-account audit
- `PLAN.md` — phased roadmap (still relevant; small-business scope)
- `research.md` — broader reference (Meta API, A/B, audience, tools)
- `REPORT.md` — plain-language status report for Diana
- `audit-prompt.md` — browser-Claude prompt to re-run the ad audit later
- `data/raw/` — cached Meta API responses (gitignored)
- `.env` — Meta access token, ad account ID (gitignored)

## Stack decisions
- **Hosting**: GitHub Pages, custom domain `saged.club`
- **Front-end**: Vanilla HTML/CSS/JS — no framework, no build step. Designed for "edit a file and push."
- **Typography**: Cormorant Garamond (display) + Inter (text), via Google Fonts.
- **Palette**: warm clay neutrals + terracotta + sage accent. Tokens in `:root` in `style.css`.
- **Booking**: Cal.com (planned) — open source, GDPR-friendly, Stripe-integrated.
- **Tracking**: Meta Pixel + Conversions API, gated by EU-compliant consent banner.

## Hard constraints
- **EU compliance** (Spain): explicit opt-in before Pixel fires. Consent banner already implemented in `script.js`.
- **RU + UA audiences separated**: never merge into one ad set. Localized creative per language.
- **Ad spend reality**: €150/month total. No statistical A/B testing until volume grows. Doing creative iteration instead.
- **Meta Marketing API v25.0** pinned. v26.0 expected ~Sept 2026.

## What we are NOT doing
- React/Next.js/any build tool — vanilla, deployable from `main`
- Programmatic Advantage+ Shopping campaigns (Meta blocks API access after 2026-05-19; not relevant for workshops anyway)
- MMM / Robyn / data warehouses / Prefect — premature at this scale
- Merging RU + UA ad sets

## Working preferences for Claude

**🔁 BILINGUAL MIRROR (non-negotiable)**: every content edit to `index.html` (RU) MUST be mirrored in `uk/index.html` (UA), and vice versa. Same sections, same structure, same images, same number of testimonials/IG embeds/FAQ items/etc. A diff in `<section>` count or `<h2>` count between the two files is a bug. Always edit both before committing.

Other preferences:
- Read `REPORT.md` for the plain-English current state before suggesting changes
- Diana is a UX designer — use plain language, design analogies
- One step at a time; don't batch big decisions
- Always reference the relevant GitHub issue when proposing work
- Russian/Ukrainian audience separation is non-negotiable
- Don't recommend tooling beyond what's justified at €150/month spend
