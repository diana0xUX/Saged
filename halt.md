# Halt — 2026-05-11

## Where we stopped

Long, productive session. Shipped 9 PRs (#74–#82) tonight covering: hero video aspect fix,
4 new Koritsa photos wired in, UA-captioned hero loop, 3 real testimonials (Vera DM +
2 Google reviews), proper 1200×630 OG card, real past-event gallery from Diana's Boosi +
Vaamos shoots, click-to-advance carousel, and the retro itself. Site is in launch-ready
shape. Halt is voluntary — no failure state, just end of working day.

## Current state

- **Branch**: `main` (clean, in sync with origin)
- **Last commit**: `99d9933` chore: retro for 2026-05-11 session (PRs #74–#81) (#82)
- **Build status**: GitHub Pages deploys auto-run; latest ones successful
- **Open review**: none
- **Live URLs**: https://saged.club/ (RU) and https://saged.club/uk/ (UA)
- **Meta account**: ACTIVE, balance 0, no disable reasons
- **Meta campaign**: built, PAUSED. Toggle ACTIVE via `bash scripts/local/toggle-campaign.sh ACTIVE` once below blockers clear.

## Next steps (in order — tomorrow's first sitting)

1. **Check Stripe approval email** — Diana submitted for review yesterday-ish; approval typically ~24h.
2. **Smoke-test booking flow end-to-end** with test card `4242 4242 4242 4242` — issue [#61](https://github.com/diana0xUX/Saged/issues/61). Verify: Cal.com event picker → Stripe checkout → confirmation email → Pixel `Purchase` event in Events Manager.
3. **Flip campaign to ACTIVE** — `bash scripts/local/toggle-campaign.sh ACTIVE`. Fergie can run this; Diana approves.
4. **Diana's IG/FB quick wins** (parallel, ~30 min total): pin workshop post on @saged.club + @korytsia_studio ([#36](https://github.com/diana0xUX/Saged/issues/36)), update both IG bios ([#37](https://github.com/diana0xUX/Saged/issues/37), [#38](https://github.com/diana0xUX/Saged/issues/38)), refresh FB page ([#41](https://github.com/diana0xUX/Saged/issues/41)).

## Blockers

- **Stripe approval** — external, just waiting on Stripe's review.
- Nothing else blocking on Fergie's side.

## Context that's hard to re-derive

- **Vera Baykovskaya consent** — Diana said "we requested confirmation / all will be good" (her message tonight). Don't re-flag this; treat as approved.
- **Andrii + Elizaveta** (Google reviewers, slots #1 and #2) — no separate consent ping done; Google reviews are public + attributed under their own names, so reusing the quote with attribution is generally accepted. If Diana wants to be extra-careful, ping is optional.
- **PR #74 image cross-wiring quirk**: file `gallery-1.jpg` had identical bytes to `koritsa-village.jpg` (same file, two names). After #80 it's now the candles+linen shot from Boosi. The `koritsa-*.jpg` duplicates from PR #74 are still in `assets/images/` but unreferenced — safe to leave or clean later, no rush.
- **Inbox photos not yet used** (still in `inbox/`): `IMG_5070.JPG` (beads close-up), `IMG_8695.JPG` (exhibition), `photo_3` (thistle editorial). Held back for Instagram or a second drop. Hero videos (RU + UA originals + landing-page loop) are processed and in `assets/video/`.
- **Past-event photo archive lives outside repo** at `~/Documents/saged.old/Boosi photos/` (66 photos, beads workshop) and `~/Documents/saged.old/Vaamos Photos/Fotos/` (58 photos, clay workshop). All Diana's, OK to use. KNOWLEDGE.md has the table.
- **OG image cache**: Facebook + Telegram may still serve the old broken 1286×1600 card from their caches. After Pages finishes deploying, force-refresh via the [FB Sharing Debugger](https://developers.facebook.com/tools/debug/) for both `https://saged.club/` and `https://saged.club/uk/`.
- **Loop task from earlier** (poll Meta account for settlement + campaign paused): account confirmed ACTIVE balance=0 + 0 active campaigns at last check. Issues #26 and #27 should be closeable if not already — verify on resume.

## Skills + knowledge persisted this session

- `CLAUDE.md` gained **TESTIMONIAL INTEGRITY** non-negotiable rule
- `KNOWLEDGE.md` gained Asset Archive table, social-share card spec, bilingual parity one-liner
- `docs/retro-log.md` has the full structured retro entry for 2026-05-11
- Reusable shell scripts in `scripts/local/` (gitignored): `build-meta-campaign.sh`, `toggle-campaign.sh`, `upload-video-to-meta.sh`

## Open issues snapshot (most relevant)

- 🔴 Blocking launch: [#61](https://github.com/diana0xUX/Saged/issues/61) (booking smoke-test)
- 🟡 Diana quick wins: [#36](https://github.com/diana0xUX/Saged/issues/36), [#37](https://github.com/diana0xUX/Saged/issues/37), [#38](https://github.com/diana0xUX/Saged/issues/38), [#41](https://github.com/diana0xUX/Saged/issues/41), [#47](https://github.com/diana0xUX/Saged/issues/47)
- 🟡 Content: [#54](https://github.com/diana0xUX/Saged/issues/54), [#53](https://github.com/diana0xUX/Saged/issues/53), [#55](https://github.com/diana0xUX/Saged/issues/55), [#58](https://github.com/diana0xUX/Saged/issues/58), [#64](https://github.com/diana0xUX/Saged/issues/64)
- 🟡 Post-launch reviews: [#62](https://github.com/diana0xUX/Saged/issues/62) (Day 8), [#63](https://github.com/diana0xUX/Saged/issues/63) (Day 14)
