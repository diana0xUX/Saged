# Halt — 2026-05-20 (Day 8 review)

## Where we stopped

Day 8 of the Meta campaign. Made the budget rebalance decision after seeing UA ad set explode to 8% CTR / €0.03 CPC following the May 18 geo tighten. Budget shifted from €5/€5 to €3 RU / €7 UA (same €10/day total). Campaign ends 2026-05-26 — six days left. Real diagnostic of the tracking gap shipped over May 17-18: Consent Mode v2 in the Pixel script + WhatsApp/Telegram Contact event handlers + Custom Conversion for Contact + UTM url_tags on ads. PageView fire rate jumped from ~2/day to 32 on May 18 (proof the Pixel fix worked). Logo migrated from PNG to SVG on every page (main, coworking RU/UA/EN, flyer). Flyer is at v6 (most basic editorial design). Lead-handling playbook + coworking pages all live.

## Current state (2026-05-20)

- **Branch**: `main`, last commit `d90f4db` (logo migration)
- **Meta campaign**: 🟢 ACTIVE, Day 8. €70 spent of expected €80. Ends 2026-05-26.
- **Daily budget**: **€3 RU / €7 UA** (rebalanced today after Day 8 review)
- **UA ad set**: dramatically outperforming — 8.33% CTR today (partial), €0.03 CPC. Post-geo-tighten resonance is real.
- **RU ad set**: wobbled May 18-19 (re-learning), recovering today (3.28% CTR / €0.17 CPC).
- **Pixel tracking**: 32 PageView events fired May 18 (vs ~2/day previously) — Consent Mode v2 working. 1 Contact event May 19 (first DM-click tracked).
- **Conversions**: 0 ad-attributed via Schedule. The DM-led conversions (real bookings) remain invisible to Meta attribution.
- **Account balance**: €7.62. Lifetime spend: €220.05.
- **First real booking**: 1 (via Telegram, pre-campaign tracking), workshop ran 2026-05-14.

## Tracking architecture (current, fully wired)

```
Visitor → saged.club
  ↓
Pixel loads in revoked mode (Consent Mode v2)
  ├─ fbq('init', PIXEL_ID)
  └─ fbq('track', 'PageView')        ← Meta sees the visit either way
  ↓
Banner: Accept dominant (terracotta pill) / Decline muted text
  ↓
Accept → fbq('consent', 'grant')     ← full tracking unlocked
  ↓
WhatsApp/Telegram click in #book → fbq('track', 'Contact')
  → Custom Conversion 1016380434145553 (Lead, €30)
  ↓
Cal.com checkout → Schedule event
  → Custom Conversion 980444324695740 (Purchase, €60)
```

## Issues closed/shipped since last halt (2026-05-17 → 2026-05-20)

- **#87** Vera testimonial moved near booking CTAs (closed 2026-05-17)
- **#90** Instagram + Messenger auto-replies — filed for Diana to set up in Business Suite UI
- Flyer iteration cycle: v4 → v5 (Bricolage Grotesque editorial) → v6 (most basic). All preserved as fallbacks.
- Logo migration: 6 PNG references → single SVG (`logo-saged-club.svg`) across main pages + coworking (3 languages) + flyer
- Tracking fixes shipped:
  - Meta Consent Mode v2 (Pixel always fires; revoke→grant flow on accept)
  - Banner UX softened (Accept dominant, Decline as muted text link)
  - WhatsApp/Telegram click → Pixel Contact event handler (#86 mostly done)
  - Custom Conversion 1016380434145553 created (Contact → Lead €30)
  - UTM tags via ad-level url_tags (`utm_source=meta&utm_medium=cpc&utm_campaign=ceramics-thursday&utm_content=hero-{ru,ua}-v2`)
- Targeting tightened (2026-05-18):
  - Geo radius 25km → 17km (Meta's minimum for city target)
  - Location types: `["home", "recent"]` → `["home"]` (residents only, no tourists)
  - Ad sets renamed `… v3` with "17km residents" tag
- Budget rebalanced (2026-05-20): €5/€5 → €3 RU / €7 UA

## Next steps (in order)

1. **Tomorrow morning (2026-05-21)**: read the auto-generated daily report — first day with new budget split. Verify UA can absorb €7 without efficiency degrading.
2. **Day 14 (2026-05-26)**: campaign auto-ends. **Decision point**. Three paths:
   a. Extend at current setup (UA just hitting stride)
   b. Launch Message-CTA experiment (#85) instead
   c. Both — keep current + add a Message-CTA variant ad set
3. **#86 finish**: extend `scripts/audit-daily.py` to surface Contact event count alongside Schedule (~20 min). Useful for Day 14 read.
4. **#88 Koritsa video** — schedule the retro-camera shoot with Alisher. Best on a Thursday (workshop day). Would unlock creative refresh + warmer ad-content rotation.
5. **#89 lead playbook adoption** — Diana confirms accuracy of `docs/lead-handling.md`, starts using templates in DMs.
6. **#90 IG/Messenger auto-replies** — Diana sets up Instant Reply + FAQs + Away Message via Meta Business Suite app (~10 min, no code).

## Blockers

- None on the dev side.
- Real-life: scheduling the Koritsa video shoot (#88), and Diana finding time to do the auto-reply setup in Meta Business Suite (#90).

## Context that's hard to re-derive

- **Geo tightening on small local campaigns produces dramatic effects within ~48h.** UA CTR went from 4.20% → 8.33% in 2 days after dropping 25km → 17km + removing "recent" location type. Worth remembering for any future hyperlocal campaign — Meta's algorithm finds its quality audience faster when given a tighter pool.
- **The Consent Mode v2 fix is harder to verify than to ship**: even after the script is deployed, Pixel stats endpoint has hours-to-days of lag, and many visits still don't fire (Safari ITP, ad-blockers). The proof point on May 18 (32 PageViews vs typical 2) only became visible 24-48h later. Patience required.
- **RU ad set re-learning takes 24-48h** after targeting changes. CTR drops to ~half before recovering. Don't panic-pause during this window.
- **Budget rebalances should be incremental** (max 20-30% shift per change) to avoid resetting Meta's learning. €5→€7 on UA is a 40% increase — borderline. Watch tomorrow's data for any wobble.
- **First Contact event fired 2026-05-19** — someone clicked WhatsApp on the booking section, the new handler captured it. That's the first signal we've ever gotten that the DM-led funnel exists at scale.
- **Logo SVG asset**: `assets/images/logo-saged-club.svg` — 12.7KB, color #FF7A23 baked in, viewBox 712×322. Use this everywhere. Old PNGs (`logo-saged-orange.png`, `logo-saged-club.png`) still in repo but unreferenced — safe to delete.
- **Flyer is at v6** (most basic editorial). v1-v5 preserved as fallback iterations. Bricolage Grotesque single font, #FF7A23 single accent, clean rounded photo rectangle, bare QR.

## Skills + memory persisted

- New cross-session memory: `feedback_a5_print_overflow.md` — A5 HTML flyers silently clip past 210mm
- Updated: `project_saged_club_campaign_live.md` previously with mid-campaign state; could update again with Day 8 numbers but the trend is captured here in halt.md

## Open issues snapshot (most relevant)

- 🟢 **Live**: campaign — auto-monitored daily reports
- 🔴 **Next decision point**: Day 14 (2026-05-26) — campaign auto-ends
- 🟡 **DM strategy follow-ups**: [#85](https://github.com/diana0xUX/Saged/issues/85), [#86](https://github.com/diana0xUX/Saged/issues/86), [#88](https://github.com/diana0xUX/Saged/issues/88), [#89](https://github.com/diana0xUX/Saged/issues/89), [#90](https://github.com/diana0xUX/Saged/issues/90)
- 🟡 **Diana quick wins still open**: [#36](https://github.com/diana0xUX/Saged/issues/36), [#38](https://github.com/diana0xUX/Saged/issues/38), [#41](https://github.com/diana0xUX/Saged/issues/41), [#47](https://github.com/diana0xUX/Saged/issues/47)
- 🟡 **Content for ad rotation**: [#54](https://github.com/diana0xUX/Saged/issues/54), [#53](https://github.com/diana0xUX/Saged/issues/53), [#55](https://github.com/diana0xUX/Saged/issues/55), [#58](https://github.com/diana0xUX/Saged/issues/58), [#64](https://github.com/diana0xUX/Saged/issues/64)
