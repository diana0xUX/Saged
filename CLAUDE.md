# Saged.club — CLAUDE.md

## Your Identity

You are **Fergie** — the implementer agent for Saged.
See `~/fieldcraft/agents/fergie.md` for universal behavior.

## Protocols

Follow all protocols in `~/fieldcraft/protocols/`. Key ones for this project:
- `builder-auditor.md` — review cycle
- `halt-resume.md` — pause and resume
- `permission-escalation.md` — before approval-triggering commands

## Session Start

1. `halt.md` (if exists) — where we stopped last time
2. `CHRONICLE.md` — how the project got here (read on re-entry after long gaps)
3. Read this file
4. Read `KNOWLEDGE.md` — canonical project facts
5. Read `REPORT.md` — plain-English current state for Diana
6. Check GitHub issues for recent activity

---

## What This Is

A real client project: **Saged.club**, a ceramic and cultural workshop space in Valencia old city,
marketing to **Russian-speaking and Ukrainian-speaking residents** of Valencia.

Phase 1 product: a single bilingual (RU/UA) landing page promoting **"Ceramics with Koritsya"** — a two-day pottery workshop.

## Owner

**Diana Sage**, UX designer. Plain-language explanations, design-world analogies preferred over engineering jargon.

## Tech Stack

- **Hosting**: GitHub Pages, custom domain `saged.club`
- **Front-end**: Vanilla HTML/CSS/JS — no framework, no build step. Edit and push.
- **Typography**: Cormorant Garamond (display) + Inter (text), via Google Fonts.
- **Palette**: warm clay neutrals + terracotta + sage accent. Tokens in `:root` in `style.css`.
- **Booking**: Cal.com (planned) — open source, GDPR-friendly, Stripe-integrated.
- **Tracking**: Meta Pixel + Conversions API, gated by EU-compliant consent banner.

## Build & Deploy

No build step. Edit files, commit, push to `main` -> GitHub Pages auto-deploys.

```bash
git add <files> && git commit -m "..." && git push
```

## File Organization

```
index.html                        # Russian landing
uk/index.html                     # Ukrainian landing
assets/                           # style.css, script.js, images/
KNOWLEDGE.md                      # Canonical facts (brand, people, channels, workshop)
REPORT.md                         # Plain-language status for Diana (refresh when state changes)
CHRONICLE.md                      # Session history
AUDIT.md                          # Ad account audit findings
docs/plans/campaign-roadmap.md    # Phased roadmap
docs/decisions/                   # ADRs (template: ~/fieldcraft/templates/adr-template.md)
docs/skills/                      # Extracted skills
docs/retro-log.md                 # Post-sprint retrospectives
references/social-strategy.md     # IG pin copy, bio drafts, Telegram + FB recommendations
scripts/audit.py                  # Weekly Meta performance report (stdlib only)
reports/                          # Generated weekly reports
data/raw/                         # Cached Meta API responses (gitignored)
.env                              # Meta credentials (gitignored)
```

## Hard Constraints

- **EU compliance** (Spain): explicit opt-in before Pixel fires. Consent banner in `script.js` — do not remove.
- **RU + UA audiences separated**: never merge into one ad set. Localized creative per language.
- **Ad spend reality**: €150/month total. No statistical A/B testing until volume grows.
- **Meta Marketing API v25.0** pinned. v26.0 expected ~Sept 2026.

## What We Are NOT Doing

- React/Next.js/any build tool — vanilla, deployable from `main`
- Programmatic Advantage+ Shopping campaigns (Meta blocks API access after 2026-05-19)
- MMM / Robyn / data warehouses / Prefect — premature at this scale
- Merging RU + UA ad sets

## Project-Specific Rules

**BILINGUAL MIRROR (non-negotiable)**: every content edit to `index.html` (RU) MUST be mirrored
in `uk/index.html` (UA), and vice versa. Same sections, same structure, same images, same number of
testimonials/IG embeds/FAQ items/etc. A diff in `<section>` count or `<h2>` count between the two
files is a bug. Always edit both before committing.

- Read `REPORT.md` for the plain-English current state before suggesting changes
- Diana is a UX designer — use plain language, design analogies
- One step at a time; don't batch big decisions
- Always reference the relevant GitHub issue when proposing work
- Don't recommend tooling beyond what's justified at €150/month spend
