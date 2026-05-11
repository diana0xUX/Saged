# Saged.club — Project Knowledge

The canonical source of truth for everything about the studio. Update this file as facts change; future Claude sessions read it for context.

Last updated: **2026-05-11**

---

## The Studio

| | |
|---|---|
| **Brand name** | Saged.club |
| **Business portfolio (Meta BM)** | Saged.design |
| **Domain** | saged.club (bought, DNS pending) |
| **Address** | C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia, Spain |
| **Google Maps** | https://maps.app.goo.gl/RqsReEo929aeUAPN9 |
| **Type** | Ceramic + cultural workshop space ("art community platform") |
| **Existing tagline** | "A place to slow down, create, and connect through art, music, and hands-on making." |
| **Languages served** | Russian, Ukrainian (primary); English (some); Spanish (some) |

## The People

### Diana Sage — Founder / operator
- Role: UX designer, runs the business + marketing
- Email: alisheryakupov@gmail.com
- Telegram: @dvoroneca
- GitHub: diana0xUX

### Korincia Gasikóvska ("Кориця" RU / "Кориця" UA / "Korytsia" EN) — Ceramic instructor
- Ukrainian ceramic artist based in Valencia
- Runs her own studio: @korytsia_studio (Instagram)
- Telegram: @ko_hasi
- Speaks: Ukrainian, Russian
- Aesthetic: minimalist ceramic art, slow tactile process

## Contact Channels (all working as of 2026-05-11)

| Channel | Handle / URL | For |
|---|---|---|
| WhatsApp | +34 605 54 33 00 | Primary booking + general |
| Email | hello@saged.club | Formal inquiries, sertificates |
| Studio Instagram | @saged.club | Brand presence + DM bookings |
| Koritsa Instagram | @korytsia_studio | Bookings directly with instructor |
| Studio Telegram | @dvoroneca (Diana's personal) | RU/UA-speaking audience |
| Koritsa Telegram | @ko_hasi | Direct with instructor |
| Facebook page | https://www.facebook.com/share/1BUsmYHLdW/ | Older audience, less active |

## The Audience

- **Primary**: Russian-speaking + Ukrainian-speaking residents of Valencia. Many post-2022 displacement context (Ukrainian community especially).
- **Secondary**: English-speaking expats and digital nomads in Valencia.
- **Tertiary**: Spanish locals interested in handcraft / slow living.
- **Treat RU and UA as separate audiences** in advertising — never lump them in one ad set. Cultural sensitivity is non-negotiable.

## The Workshop (current primary offering)

### "Керамика с Корицей" / "Кераміка з Корицею" / "Ceramics with Koritsya"

- **Format**: Two 2-hour sessions, one week apart
  - Session 1: hand-form a piece (cup / bowl / small plate)
  - Session 2 (a week later): glaze + decorate; studio handles final firing
- **Schedule**: Every Thursday, 3 time slots
  - 12:00–14:00
  - 15:00–17:00
  - 19:00–21:00
- **Booking rule**: Book 2 consecutive Thursdays in the same slot
- **First cohort**: 14 + 21 May 2026
- **Price**: €60 for both sessions (everything included)
- **Group size**: up to 6 people per slot
- **What's included**: clay (~1kg), tools, two firings (bisque + glaze), tea/water, finished piece delivered ~2 weeks after session 2

### Why two sessions
Clay must dry + go through first (bisque) firing before glazing. That cycle takes a week. This isn't a workaround — it's the actual ceramic process.

## Brand Voice & Tone

Cues borrowed from the existing saged.club site + Koritsa's Instagram:

- **"Slow down"** — recurring motif (English: "slow down, create, connect" / Russian: "замедлиться, создавать, соединяться")
- **Anti-rush** — explicitly frames patience and process as values
- **Warm, inclusive** — not corporate, not LinkedIn
- **Community-first** — focuses on the space + people, not just product
- **Hand-made / tactile** — emphasizes physicality of materials
- **Minimalist visual style** — let imagery breathe; warm clay neutrals, no neon

Words that work: тихо, без спешки, замедлиться, руками, своими, маленькая группа, через две недели, тактильный.

Words to avoid: "premium", "luxury", "exclusive", "limited", "hurry", urgent CTAs.

## Other Saged.club Offerings (from past Meta ads)

Beyond ceramics, the studio has hosted:
- **Neuroclay** — clay as self-discovery / therapy (Yaroslav co-led?)
- **Tea ceremony + sound meditation** (Роман Тизенберг × АнандаГири)
- **Kirtan** — call-and-response chanting evening
- **Gua sha self-massage** workshop
- **Saged.club community gatherings** (Eastern European / post-Soviet diaspora)

Future scope: same landing structure can serve any of these. Current focus = ceramics only.

## Meta Ads Context

### What we found (audit 2026-05-11)
- Ad account: `act_484884320671439`
- Lifetime spend: €143.43, status **UNSETTLED** (needs payment)
- 9 prior boosted Instagram posts, all optimizing for wrong objectives (MESSAGES, LINK_CLICKS)
- No Pixel installed
- No Custom Audiences
- No language targeting despite Russian-language creative
- Result: 0 workshop bookings from €105 spent

See `AUDIT.md` for the full breakdown.

### What we're rebuilding (post-launch)
1. ~~Settle invoice + pause old boosts~~ ✅ done 2026-05-11 — Diana paid invoice (€143.43 cleared), deleted all 9 old campaigns. Account back to status=1 (ACTIVE).
2. Install Meta Pixel + Conversions API on saged.club — pending Diana to create Pixel (#20)
3. Build proper Sales-objective campaign with RU + UA separate ad sets — pending Pixel + DNS
4. Target Valencia + 25km, language-filtered
5. Reuse "Saged.club is for…" copy structure (had 4% CTR — best performer). Now also embedded as a pinned-style block on the landing page.

## Tech Stack

- **Hosting**: GitHub Pages (`diana0xUX/Saged` repo, `main` branch)
- **Domain**: saged.club (CNAME set, DNS pending)
- **Front-end**: Vanilla HTML/CSS/JS — no framework, no build step
- **Booking**: Multi-channel (manual via WhatsApp/Telegram/IG) for now. Cal.com + Stripe is the future plan.
- **Tracking**: Meta Pixel + CAPI (planned, EU-consent-gated)
- **Repo collaborator**: xAlisher (admin)

## Decision Log

| Date | Decision | Why |
|---|---|---|
| 2026-05-11 | Vanilla HTML/CSS/JS, no framework | Diana is a UX designer; editable in any editor, deployable from main, no build complexity |
| 2026-05-11 | Multi-channel manual booking (not Cal.com yet) | €60 workshop, small studio, manual handling fine until volume justifies automation |
| 2026-05-11 | RU + UA always separate ad sets | Cultural sensitivity (post-2022 displacement context) + statistical clarity |
| 2026-05-11 | System User "claude" gets read-only on ad account | Security: keep write power off until clear automation workflow defined |
| 2026-05-11 | Course frame as "every Thursday" not "May 14 one-off" | Reflects actual recurring schedule + lets page stay relevant past first cohort |
| 2026-05-11 | Cookie consent banner enforced; no Pixel until accept | GDPR + DMA compliance for EU audience |

## Open Questions

- Will the Meta App require App Review for production traffic? (Likely yes if we scale spend; not blocking at current scale.)
- What's the cancellation/refund policy beyond "48h notice"?
- Are gift certificates real or aspirational? (Mentioned in FAQ but not yet operationalized.)
- Studio capacity per Thursday: 6×3 slots = 18 people/Thursday × 2 weeks = €1,080 weekly ceiling. Worth understanding for scaling decisions.

## Useful Links

- Live preview: https://diana0xUX.github.io/Saged/
- Repo: https://github.com/diana0xUX/Saged
- Issues: https://github.com/diana0xUX/Saged/issues
- Existing saged.club site (English, Squarespace): https://saged.club (pre-DNS-change)
- Koritsa's IG: https://www.instagram.com/korytsia_studio
- Studio IG: https://www.instagram.com/saged.club
- Studio FB: https://www.facebook.com/share/1BUsmYHLdW/
- Studio Maps: https://maps.app.goo.gl/RqsReEo929aeUAPN9
