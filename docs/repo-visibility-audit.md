# Repository visibility audit — 2026-05-28

Audit triggered by Diana's question: "is anything secret exposed publicly, and can the repo be made private while keeping saged.club live?"

## TL;DR

- **No technical secrets are exposed.** `.env`, `.campaign-ids`, raw Meta dumps, and inbox photos are all gitignored. Git history was checked back to first commit — no token, key, or credential was ever committed. Workflows use GitHub Actions secrets (encrypted server-side), not hardcoded values.
- **Business strategy is visible** to anyone who reads the repo: `KNOWLEDGE.md`, `REPORT.md`, `AUDIT.md`, `docs/plans/`, `docs/decisions/`, and 100+ GitHub Issues describe audience, targeting, budgets, prior failures, decision log, and operator playbooks. This is a design / strategy disclosure, not a security incident.
- **Making the repo private while keeping `saged.club` live requires upgrading the GitHub plan** (Diana is on Free). Cheapest path: GitHub Pro at **$4/month**. Alternative without upgrading: move static hosting off GitHub Pages (Cloudflare Pages or Netlify connect to a private GitHub repo and serve publicly on their free tiers).

## What was checked

### Technical secrets
| Check | Result |
|---|---|
| `.env` present locally | ✅ exists, gitignored |
| `.env` ever committed | ✅ no — `git log --all -- .env` empty |
| `.campaign-ids` present locally | ✅ exists, gitignored |
| `.campaign-ids` ever committed | ✅ no |
| `EAA*` Meta token pattern in tree | ✅ none |
| `sk_live_*` / `sk_test_*` Stripe pattern | ✅ none |
| `AIza*` Google API pattern | ✅ none |
| `ghp_*` / `github_pat_*` GitHub PAT | ✅ none |
| Files matching `*.token`, `credentials.json`, `*.key` in tree | ✅ none |
| Workflow secret handling | ✅ proper — uses `${{ secrets.META_* }}` |
| Repo Actions secrets (named correctly) | ✅ 5 named secrets set 2026-05-15 |

### Intentionally public (not leaks)
| Item | Why it's OK |
|---|---|
| Meta Pixel ID `1533639615120579` | Pixel IDs always live in client-side JS for tracking. Public by Meta's design. |
| WhatsApp `+34 605 54 33 00` | Studio's booking number, meant to be visible. |
| Instagram, Telegram, FB handles | Marketing contact channels. |
| Cal.com URLs (when added) | Public booking widget. |
| Studio address, hours, instructor name | Marketing copy. |

### Business strategy currently visible
Anyone with the repo URL can read:
- `KNOWLEDGE.md` — audience cohorts, post-2022 displacement context, financial ceiling (€1,080/week per cohort track), prior spend (€143.43 wasted on misconfigured ads), targeting decisions, edit-lock workarounds
- `AUDIT.md` — full diagnosis of why €105 produced zero bookings
- `REPORT.md` — current campaign state, plans, retrospectives
- `docs/plans/` — campaign roadmaps with budgets and timelines
- `docs/decisions/` — ADRs (why certain calls were made)
- `docs/lead-handling.md` — operator playbook for WhatsApp DM conversion
- `docs/instagram-faq.md` — IG auto-reply scripts
- GitHub Issues — ad copy iterations, day-N reviews, tactic experiments

Whether this matters is a business question, not a security one:
- It tells competitors how the studio is positioning + what's working
- It exposes thresholds (Day 7 pause rules, CPC targets) that a hostile reader could use to interpret ad performance
- It documents operator-level conversion patterns — fine for transparency, awkward for sales

## Making the repo private — options

GitHub Pages from a **private repo** requires a paid plan. The current free-tier setup only allows Pages from public repos.

### Option 1 — GitHub Pro ($4/month) · simplest
- Upgrade Diana's account: `github.com/settings/billing` → Pro
- Then flip repo to private: `github.com/diana0xUX/Saged/settings` → Change visibility → Private
- Pages keeps working at `saged.club` with zero further changes
- All existing workflows, secrets, and DNS stay as-is
- **Trade-off**: $48/year recurring

### Option 2 — Cloudflare Pages or Netlify (free) · more setup
- Repo can stay private on GitHub Free
- Create a Cloudflare Pages / Netlify account, connect to the (now-private) GitHub repo, point them at `main` branch
- Move DNS for `saged.club` from GitHub Pages to the new host (one CNAME change)
- Turn off GitHub Pages
- **Trade-off**: 30–60 min one-time DNS work; learning a second platform; some Meta domain-verification record may need re-checking

### Option 3 — Split-repo (private source → public deploy) · complex
- Keep `diana0xUX/Saged` private with all strategy docs
- Create a second public `diana0xUX/Saged-deploy` repo
- GitHub Action in private repo pushes only the rendered HTML/CSS/JS/images to the public deploy repo
- Public repo serves Pages
- **Trade-off**: more moving parts, two repos to maintain, GitHub Actions minutes consumed

### Option 4 — Stay public, redact business docs · zero-cost
- Move `KNOWLEDGE.md`, `AUDIT.md`, `REPORT.md`, `docs/plans/`, `docs/decisions/`, `docs/lead-handling.md` out of the repo and into a private location (Notion, Drive, a separate private GitHub repo)
- Keep only the website source + readme in the public repo
- **Trade-off**: loses the colocation that makes the agent workflow work — Claude can't read docs that aren't in the project folder

## Recommendation

Option 1 (**GitHub Pro $4/month**) if the strategy disclosure feels uncomfortable AND the colocated-docs workflow is valuable (it is — most of Claude's effectiveness here comes from reading `KNOWLEDGE.md` + `REPORT.md` next to the code).

Option 4 (**redact + stay public**) if $48/year feels wrong for what is, after all, a single landing page.

Either way: nothing currently in the repo qualifies as a credential leak. The audit is clean.
