# Saged.club

Landing page for Saged.club, a ceramic and cultural workshop space in Valencia, Spain. Targeted at Russian- and Ukrainian-speaking residents.

**Live site**: https://saged.club (once DNS is pointed)
**Stack**: vanilla HTML/CSS/JS, GitHub Pages hosting, custom domain.

## Structure

```
/
├── index.html          # Russian-language landing (default)
├── uk/index.html       # Ukrainian-language landing
├── assets/
│   ├── style.css
│   ├── script.js
│   └── images/         # all imagery — see issues for upload list
├── CNAME               # saged.club
├── CLAUDE.md           # context for Claude sessions
├── PLAN.md             # phased roadmap
├── AUDIT.md            # findings from the Phase 0 ad-account audit
├── research.md         # broader research reference (Meta ads, A/B, audience, automation)
├── audit-prompt.md     # browser-Claude prompt for repeating the ad-account audit
└── data/raw/           # cached API responses (ignored from git for now)
```

## Local preview

```sh
cd ~/Documents/saged.club
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

Push to `main`. GitHub Pages is enabled on the repository — it builds automatically. Custom domain `saged.club` is wired via the `CNAME` file in repo root; DNS configuration happens at the domain registrar (see issue **#DNS**).

## What's NOT in the repo

- `.env` — Meta access token, ad account ID. Local only.
- `data/raw/` — cached audit data; can be regenerated from API.

## Working with Claude on this project

Read `CLAUDE.md` first for project context. The current phase, hard constraints, and working preferences are documented there. Tone: plain language, no unexplained jargon. Diana is a UX designer, not a developer.
