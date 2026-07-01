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

**TESTIMONIAL INTEGRITY (non-negotiable)**: testimonial content must come from a real, user-supplied
source — Google review, IG comment, DM, email. NEVER fabricate a quote, even as "plausible filler."
Placeholder slots must clearly self-label (e.g., `[Тестимониал — ждём из Instagram]`). If asked
for N testimonials, write exactly N — pattern-completion bias has produced phantom slots before
(see retro 2026-05-11).

**META LOCALE VERIFICATION (non-negotiable)**: NEVER create or modify a Meta ad set's `locales`
targeting using hardcoded IDs from memory, comments, or older docs. Always query Meta's
`/search?type=adlocale` endpoint at runtime and verify each ID against the canonical name before
sending the targeting payload. Any script that hardcodes locale IDs must include a runtime
`verify_locale` guard that exits non-zero on mismatch.

**Past incident (2026-05-11)**: the adult campaign launched with `locale 10` labeled as Russian
(actually Italian) and `locale 37` labeled as Ukrainian (actually Bulgarian). 30 days of misfire,
€141.89 spent, 0 bookings — the Russian/Ukrainian ad creative was shown to Italians and Bulgarians
in Valencia. Reference implementation: the `verify_locale()` function in
`scripts/local/build-meta-campaign.sh`. Canonical IDs as of 2026-06-09: Russian=17, Ukrainian=52,
English (UK)=24, English (US)=6, Spanish=23. Verify every time — don't trust this list either.

- Read `REPORT.md` for the plain-English current state before suggesting changes
- Diana is a UX designer — use plain language, design analogies
- One step at a time; don't batch big decisions
- Always reference the relevant GitHub issue when proposing work
- Don't recommend tooling beyond what's justified at €150/month spend

**PERSISTENCE RULE**: do NOT save project knowledge to Claude's auto-memory folder. Save facts to `KNOWLEDGE.md`, behavior rules to this file, cross-project user prefs to `~/.claude/CLAUDE.md`. See `~/.claude/CLAUDE.md` for the full rule. Diana wants visibility and version control over what's known about her work.

**NO REVIEWER on this project**: there is no Senty / Codex reviewer wired up for saged.club. Skip the builder-auditor review step from `~/fieldcraft/protocols/builder-auditor.md` — do NOT offer to run `/codex:review`, `/codex:rescue`, or any external review command. Diana reviews changes directly via the GitHub PR diff or by running the result. When the protocol says "trigger Senty review", substitute: post a handoff comment and ask Diana to review the PR.

---

## Behavioral patterns learned on this project

### High-touch DM-first booking (for ≤€100 offers)

For small-ticket community-flavored purchases (workshops ≤€100) to RU/UA/ES messaging-dominant audiences, "message first → pay later" converts higher than "click → checkout instantly."

**Why:** Evidence from Saged.club 2026-05-12 → 2026-05-17 — 247 ad-driven visits produced 0 attributed Stripe checkouts; first €60 booking came via Telegram DM with a Cal.com link sent 1:1. Audience treats €60 as "worth a 30-min DM" and wants to feel they know the host.

**How to apply:**
- Booking sections: equal-weight DM and direct-pay CTAs side-by-side. Don't make DM look like a fallback.
- Permission framing: "Не уверены? Напишите — расскажем больше, забронируем вручную. Уверены — бронируйте сразу."
- WhatsApp pre-fills: structured (Имя, Дата, Слот) + "Если есть вопросы — спрошу здесь :)" — lowers activation energy.
- Ad CTA: prefer `MESSAGE_PAGE` / WhatsApp deep link over website link for these offers.
- Keep `docs/lead-handling.md` up to date — it's the human side of this conversion path.

**When this doesn't apply:** self-serve / SaaS / commodity bookings, US/UK markets, €200+ ticket size.

### wa.me deep-link from JavaScript

When triggering a `wa.me/<phone>?text=<encoded>` link from JS (form submit, button handler), use a temporary `<a target="_blank">.click()` pattern, NOT `window.open(url, '_blank', 'noopener')`.

```js
// WRONG — drops text= param on mobile Safari, breaks iOS universal-link
window.open(`https://wa.me/${phone}?text=${msg}`, '_blank', 'noopener');

// RIGHT — preserves params, triggers iOS/Android universal link
const a = document.createElement('a');
a.href = `https://wa.me/${phone}?text=${msg}`;
a.target = '_blank';
a.rel = 'noopener';
document.body.appendChild(a);
a.click();
a.remove();
```

**Why:** The feature-string variant opens a stripped popup; somewhere in wa.me's redirect the `text=` param gets dropped, and WhatsApp opens with an empty message. Diana caught this 2026-05-26 on the kids form — looked like the form was broken.

**How to apply:** any dynamic wa.me / tel: / mailto: deep link triggered from JS — use the anchor-click pattern.

### A5 print HTML — overflow clips silently

When designing a printable HTML flyer at A5 (148×210mm) with `overflow: hidden` on the page container, content past 210mm gets clipped with **no visible warning**. Browser, CSS, and print preview all stay silent. The QR or footer just disappears.

Bitten twice on the Thursday-class flyer (v5 and v6). Felt fine eyeballed; user noticed the QR was missing.

**How to apply after ANY structural change to a print flyer:**
1. Sum expected heights of every direct child of the page container in mm. Treat as a back-of-envelope budget. 1pt ≈ 0.35mm.
2. CSS guards: `.footer { flex-shrink: 0 }` (footer never squeezes), photo `flex-shrink: 1` (it compresses first), avoid `overflow: hidden` during dev.
3. Verify: `python3 -m http.server`, open the file, check footer is fully visible. If unsure, set `body { background: red }` so clipping is obvious.

Active flyer at `flyer/index.html`, iterations v1–v6 alongside. v6 is the "most basic" reference.
