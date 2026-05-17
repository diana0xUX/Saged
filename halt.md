# Halt — 2026-05-17

## Where we stopped

Five days into the Meta campaign. Diagnosed why "leads/contacts felt lower than before" — performance was actually *improving* (CTR rising, CPC falling, UA ad set at 5.25% CTR), but the strict-consent Pixel gating was making 95-99% of ad-driven traffic invisible to Meta. Built the fix: Meta Consent Mode v2 (Pixel fires PageView on every visit in limited-data mode regardless of consent state). Also added a Contact event on WhatsApp/Telegram clicks, softened the consent banner UX, created a Contact Custom Conversion in Meta, and added UTM tags at the ad level. Booking section rebalanced earlier in the day to equal-weight DM + Stripe paths after observation that real conversions are coming via Telegram/Instagram DMs, not the cold checkout funnel. Lead-handling playbook now lives at `docs/lead-handling.md`. Vera testimonial added as social proof above the booking CTAs.

## Current state (2026-05-17)

- **Branch**: `main`
- **Last commit**: `35b67df` (Vera testimonial in booking section)
- **Build status**: GitHub Pages auto-deploys, no failures
- **Live URLs**: https://saged.club/ (RU) · https://saged.club/uk/ (UA) · https://saged.club/coworking/ (+ /uk/coworking/ + /en/coworking/)
- **Meta campaign**: 🟢 ACTIVE, 5 days in. €44.37 spent of €50 expected. CTR 3-4% (climbing). UA outperforming RU ~2-3×.
- **Tracking infrastructure**: Pixel fires on every visit via Consent Mode v2. Contact event live on DM CTAs. Two Custom Conversions: `980444324695740` (Schedule → Purchase €60) and `1016380434145553` (Contact → Lead €30).
- **Reporting**: daily + weekly GitHub Actions workflows auto-commit reports to `reports/daily/` and `reports/weekly/`. Secrets in GH. Last successful run: today's daily.
- **First real booking**: 1 (came via Telegram DM after Diana shared the Cal.com link, not ad-attributed). Workshop ran 2026-05-14.

## Tracking architecture (current)

```
Visitor lands on saged.club
  ↓
Pixel script loads (always)
  ├─ fbq('consent', 'revoke')      ← if user hasn't accepted yet
  ├─ fbq('init', PIXEL_ID)
  └─ fbq('track', 'PageView')      ← fires regardless; Meta sees the visit
  ↓
Banner shown (softened: "Помогите нам понять..." with Accept dominant)
  ↓
If user accepts → fbq('consent', 'grant')  ← unlocks full tracking
  ↓
User clicks WhatsApp/Telegram in #book → fbq('track', 'Contact')
  → maps to Custom Conversion 1016380434145553 (Lead, €30)
  ↓
OR user clicks Cal.com → completes payment → Cal.com fires Schedule
  → maps to Custom Conversion 980444324695740 (Purchase, €60)
```

## Issues closed this session arc (2026-05-14 → 2026-05-17)

- **#5, #7, #11, #28, #34, #35, #37, #61, #83, #84, #87** — shipped + verified

## Issues opened this session arc

- **#85** — Test Message-CTA ads (waiting for Day 8 baseline)
- **#86** — Contact event tracking (partially shipped today: click handler + Custom Conversion live; remaining: report-template update to show Contact column)
- **#87** ✅ closed today
- **#88** — Koritsa retro-camera invitation video (needs Alisher to shoot)
- **#89** — Adopt lead playbook, train operators (Diana)

## Next steps (in order — when Diana resumes)

1. **Watch tomorrow's daily report (auto-fires at 09:00 Madrid)**. Check that PageView count now ~matches Meta's click count. If yes — Consent Mode fix worked. If still 5-10× discrepancy — investigate further (maybe Pixel script error in production; test in incognito).
2. **Day 8 review (2026-05-20)** — `python3 scripts/audit-weekly.py` or just check `reports/weekly/`. First real read with proper attribution data. Decisions to make:
   - Shift budget toward UA (still ahead) if pattern holds?
   - Trigger #85 (Message-CTA experiment)?
   - Pause anything underperforming?
3. **#86 finish** — extend `scripts/audit-daily.py` to show Contact event count alongside Schedule. ~20 min change.
4. **#88** — schedule the Koritsa retro-camera shoot with Alisher (Thursday is the natural day, when the studio is "on").
5. **#89** — Diana reads `docs/lead-handling.md`, confirms accuracy, and starts using the templates when DMs come in.
6. **Optional cleanup** — delete old v1 ad sets `120244368150280513` (RU) and `120244368151220513` (UA). Still paused, harmless, just clutter.

## Blockers

- None. Everything is shipped or queued. Day 8 review is the next decision point.

## Context that's hard to re-derive

- **Meta Consent Mode v2 is the key unlock**: `fbq('consent', 'revoke')` BEFORE `fbq('init')` keeps tracking on without cookies/PII. Meta still gets PageView signal for ad optimization. EU-compliant. Documented at developers.facebook.com but easy to miss because the simpler "load Pixel only on accept" pattern is what most tutorials show — and it kills tracking.
- **UTM url_tags work at the ad level, not the creative level**: `POST /{ad-id}` with `url_tags=...` succeeds where `POST /{creative-id}` with `url_tags` fails (subcode 1815573). Meta internally creates a new creative pointing to the tagged URL. The published creative ID changes silently — verify by reading back the ad's `creative.id`.
- **The "high-touch over high-velocity" insight is real**: for €60 community workshops, the first booking came via DM after Diana sent the link, not via cold Stripe checkout from an ad. The funnel is now equal-weight WhatsApp + Cal.com paths, not Cal.com-only. Lead playbook (`docs/lead-handling.md`) operationalizes this — without it, DM response quality decays as bandwidth gets stretched.
- **Three v1 ad sets** (`120244368150280513`, `120244368151220513`) still PAUSED in the live campaign — leftover from the Purchase→Schedule optimization rebuild. Safe to delete after Day 8.
- **Untracked PNGs** still sitting in `assets/images/` (`1.png`, `2.png`, `3.png`) — flagged across multiple sessions, never committed or deleted, status unknown. Worth one explicit ask + cleanup.
- **Flyer is at v5** (`flyer/index.html`) — Bricolage Grotesque, #FF7A23 brand color, organic-blob photo mask, bare QR. v1-v4 preserved as fallback. Open in browser then Cmd+P to print A5.
- **Coworking offering lives at `/coworking/`** (RU/UA/EN, three pages) with master rules at `docs/coworking-rules.md`. Footer of main page cross-promotes it.

## Skills + knowledge persisted this session

- New cross-session memory: `reference_meta_consent_mode_v2.md` (the EU-compliant tracking pattern)
- New cross-session memory: `feedback_high_touch_community_offers.md` (when DM-first beats click-to-pay-first)
- Updated: `project_saged_club_campaign_live.md` with mid-campaign state
- New docs in repo: `docs/lead-handling.md` (operational playbook), `docs/coworking-rules.md` (pricing canon)
- Reporting scripts: `scripts/_meta.py` (shared helpers), `scripts/audit-daily.py`, `scripts/audit-weekly.py`, plus `docs/templates/report-*.md`

## Open issues snapshot (most relevant)

- 🟢 **Live & humming**: campaign `120244368076410513` — auto-monitored daily
- 🔴 **Next decision point**: Day 8 review 2026-05-20 ([#62](https://github.com/diana0xUX/Saged/issues/62)), Day 14 2026-05-26 ([#63](https://github.com/diana0xUX/Saged/issues/63))
- 🟡 **DM-strategy follow-up**: [#85](https://github.com/diana0xUX/Saged/issues/85) (Message-CTA test), [#88](https://github.com/diana0xUX/Saged/issues/88) (Koritsa video), [#89](https://github.com/diana0xUX/Saged/issues/89) (playbook adoption)
- 🟡 **Small dev wrap-ups**: [#86](https://github.com/diana0xUX/Saged/issues/86) (add Contact column to daily report)
- 🟡 **Diana quick wins still open**: [#36](https://github.com/diana0xUX/Saged/issues/36), [#38](https://github.com/diana0xUX/Saged/issues/38), [#41](https://github.com/diana0xUX/Saged/issues/41), [#47](https://github.com/diana0xUX/Saged/issues/47)
- 🟡 **Content for ad rotation**: [#54](https://github.com/diana0xUX/Saged/issues/54), [#53](https://github.com/diana0xUX/Saged/issues/53), [#55](https://github.com/diana0xUX/Saged/issues/55), [#58](https://github.com/diana0xUX/Saged/issues/58), [#64](https://github.com/diana0xUX/Saged/issues/64)
