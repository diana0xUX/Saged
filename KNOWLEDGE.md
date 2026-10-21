# Saged.club — Project Knowledge

The canonical source of truth for everything about the studio. Update this file as facts change; future Claude sessions read it for context.

Last updated: **2026-10-21**

---

## The Studio

| | |
|---|---|
| **Brand name** | Saged.club |
| **Legal name** | Asociación Cultural Saged |
| **Legal status** | Registered non-profit cultural association — *careciendo de ánimo de lucro* |
| **Registration** | Conselleria de Justícia, Transparència i Participació, Generalitat Valenciana |
| **File number** | ASINS/46/2026/0756 |
| **Tax regime** | IS partial exemption (Art. 9.3 LIS); IVA exempt for cultural classes (Art. 20 LIVA) |
| **Business portfolio (Meta BM)** | Saged.design |
| **Domain** | saged.club (bought, DNS pending) |
| **Address** | C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia, Spain |
| **Google Maps** | https://maps.app.goo.gl/RqsReEo929aeUAPN9 |
| **Type** | Multidisciplinary creative club / cultural association |
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
- Runs her own studio: @korytsia_studio (Instagram brand, not a physical studio)
- Telegram: @ko_hasi
- Speaks: Ukrainian, Russian
- Aesthetic: minimalist ceramic art, slow tactile process
- **Studio shifts**: Thursdays + weekends (Korytsia leads the adult Thursday cohort + weekend events)
- Also responsible for kiln shelf repair (in progress as of 2026-06-08)
- **Partnership terms (as of 2026-09-30)**: 50/50 revenue split on all studio income. Korytsia's side covers: teaching/running classes, all studio operations (kiln, supplies, cleanliness, member access). Studio (Diana's side) covers: material costs for classes, bills, rent, water, tea/coffee for studio members. Split is of net revenue after studio expenses.
- **Stated vision (Sep 2026)**: Wants to contribute 3 days/week to classes (Thu + Sat + Sun) and work on her own craft after. Identity is artist first, teacher second. @korytsia_studio is her personal brand — separate from Saged.
- **Schedule at full capacity**: 13 classes/week across 3 days. Monthly gross potential: €8,880 (6 people/class) to €11,840 (8 people/class).
- **Open question (as of Sep 30, 2026)**: Builder or instructor? Has not been asked directly. Diana needs to have this conversation before proposing any partnership restructure. Key signal to listen for: does she say "we" about Saged's future, or does she talk about her own craft/time/brand as the real thing?
- **Financial stakes of the choice**: As resident (current model) at full capacity she earns €4,440–€5,920/month. As equal partner she'd earn €3,585–€5,065/month (€855 less — the cost of shared expenses including mom's salary). She gains co-ownership upside (events, coworking, future instructors) in exchange. Whether that trade makes sense to her depends on whether she wants to build Saged or just teach at Saged.
- **August 2026 outstanding**: €287.50 she collected in cash and hasn't passed to Diana. Resolve before any new structure starts.

## Team schedule (as of October 2026)

| Day | Lead | Format |
|---|---|---|
| Tuesday–Friday | Diana | Adult ceramics (EN/ES) |
| Thursday | Korytsia | Adult cohort (3 slots) |
| Weekends | Korytsia | Events / birthdays / weekend bookings |

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
- **Price**: €60 for the full 2-session cohort (everything included). **€30 single-class drop-in** also available — same Thursday slot, no commitment to come back. Drop-in is the lower-friction entry point; first observed sale 2026-06-11 (3 drop-ins, €90 gross).
- **Group size**: up to 6 people per slot
- **What's included**: clay (~1kg), tools, two firings (bisque + glaze), tea/water, finished piece delivered ~2 weeks after session 2

### Why two sessions
Clay must dry + go through first (bisque) firing before glazing. That cycle takes a week. This isn't a workaround — it's the actual ceramic process.

## Typography rule — Euro sign (hard rule, non-negotiable)

The Costa font does not include a proper € glyph. **Never type `€` inside a Costa font element.**

Use the custom SVG glyph instead:
```html
<img class="euro-sign" src="/assets/images/euro-sign.svg" alt="€">
```
With this CSS (copy into every page that uses Costa + prices):
```css
img.euro-sign{height:.72em;width:auto;vertical-align:baseline;position:relative;top:.04em;display:inline}
```
Source file: `/design/saged font/euro sign.svg` (canonical), copied to `/assets/images/euro-sign.svg` (web path).

This applies to ALL large price displays in Costa font — hero prices, pricing cards, any display-size number. Small prices in Inter body text (event cards, host profiles) may use the regular `€` character since they are in Inter, not Costa.

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

Historical website focus was ceramics. As of 2026-09-30, the new direction is a multidisciplinary creative club; ceramics remains a core program alongside recurring art classes and handpan lessons.

## Creative club direction (added 2026-09-30)

- Saged.club should be positioned and designed as a multidisciplinary creative club, not primarily as a ceramic studio.
- Ceramics remains a core, fully documented program but should share homepage prominence with other recurring creative practices.
- New recurring program: art classes, 4 sessions per week. Exact schedule, teacher, languages, age range, prices and materials still need confirmation.
- New recurring program: handpan music lesson, once per week. **Price confirmed: €50 flat per session (total, not per person).** Exact schedule, teacher, language, duration, group size and instrument requirements still need confirmation.
- Saged also hosts one-off events, birthdays and private group celebrations. These should be visible as distinct ways to use the club.
- Website inspiration: Creative Lunch Club (https://www.creativelunchclub.com/) — adapt its community-first positioning, recurring rhythm, real-member stories and simple joining path without copying its brand.
- Draft redesign proposal: `docs/creative-club-redesign-proposal.md`.

## Product Lines (active as of 2026-05-26)

| Product | Price | Format | Page | Booking | Notes |
|---|---:|---|---|---|---|
| **Ceramics with Korytsia (adult)** | €60 | 2 sessions × 2h, every Thursday | `/` + `/uk/` | Cal.com + DM | Original product. 6 customers acquired in first 14 days. |
| **Coworking** | €200/month | Monthly studio access, daily 10:00-22:00 | `/coworking/`, `/uk/coworking/`, `/en/coworking/` | DM only | 5 spots. Pricing not advertised publicly. 1 active resident: Ekaterina Sharova (pays €200/month via Bizum). Master rules in `docs/coworking-rules.md`. Launched 2026-05-14. |
| **Intro course** | €120 | 4 classes for studio-newcomers, prep for coworking | Section on `/coworking/#intro` | DM only | Pathway product into coworking. |
| **Kids' ceramic class** | €25 | Single 1.5h class, ages 6-10, group 4-6 | `/kids/`, `/uk/kids/`, `/en/kids/` | DM only · interest list · Stripe link sent in chat | **Launched 2026-05-26 as trial.** No fixed dates — schedule once 4-6 parents express interest. Validates demand before scaling. Pivoted away from full summer camp after honest critique (school-conflict timing, 2h too short for "camp", launching 3rd product line while first still proving out). **Per-class format (confirmed 2026-06-08):** each session has a single subject ("today everyone makes a mug" / "today everyone makes an animal"). Kids get a stencil + descriptive process so they have creative freedom within boundaries. Subject rotates each class. |
| **Parent + kid class** (planned) | €50 pair | 2h weekend, parent + child work together | Phase 2 of kids product | DM only | Launch only after kid-only class validates. Same warm audience. |

**Operational principle for all DM-led products**: parents/customers DM via WhatsApp with structured pre-fill → Saged/Koritsa qualify → Stripe payment link sent in chat → confirmed. No Cal.com for kids/coworking/intro. Cal.com used only for the recurring adult Thursday workshop where the calendar widget makes sense.

## Finances

All financial files live in `finances/` (gitignored — never commit).

| File | What it is |
|---|---|
| `finances/marketing-report.html` | Full Meta ads performance report — open in browser |
| `finances/financial-model.html` | Studio P&L model: 3 scenarios, break-even analysis |
| `finances/income/pnl-chart.html` | Visual income vs expenses chart (Feb–Nov 2026) |
| `finances/income/pnl-by-month.md` | Income + expense table by month |
| `finances/ad-budget-decisions.md` | Ad budget history and decisions |

**⚠ Remind Diana to check finances on session start.**

### P&L snapshot (as of 2026-07-23)

| Month | Income | Expenses | Net |
|---|---|---|---|
| Feb | €80 | €1,614 | −€1,534 |
| Mar | €982 | €1,727 | −€745 |
| Apr | €716 | €1,674 | −€959 |
| May | €494 | €1,826 | −€1,332 |
| Jun | €1,123 | €2,043 | −€920 |
| Jul (partial to 23rd) | €913 | ~€1,570 | −€657 |
| **Total** | **€4,308** | **€10,454** | **−€6,146** |

July income breakdown (after July 9 update: +€553):
- Coworking: €200
- Jul 11: €87.50 · Jul 12: €60 · Jul 16: €37.50
- Jul 18: €50 · Jul 19: €25 · Jul 21: €50
- Kiln: €43 (€30 + €13)

- Fixed monthly costs (no ads, from Sep 2026): ~€1,273 (rent + electricity + water + GWS + Notion + Anthropic + GitHub). TGSS, Vuka, Artlist all discontinued Sep 2026.
- Fixed monthly costs (with ~€45/month ads): ~€1,318
- Break-even income needed: ~€1,318
- Best month: June €1,123 (first month of correct RU+UA locale targeting)

### Active ad spend (as of 2026-07-09)

**€11.80/day = ~€366/month**

| Campaign | Budget/day | Audience |
|---|---|---|
| Workshops RU | €1.50 | Russian speakers, Valencia 17km |
| Workshops UA | €2.00 | Ukrainian speakers, Valencia 17km |
| Workshops EN | €0.90 | English speakers, Valencia 17km |
| Workshops ES | €0.90 | Spanish speakers, Valencia 17km |
| Kids · RU | €3.00 | Russian-speaking parents 28–45, Valencia 17km |
| Kids · UA | €2.00 | Ukrainian-speaking parents 28–45, Valencia 17km |
| Coworking | €1.50 | All languages, Valencia 17km |

### Meta safety audit and October drafts (2026-09-30)

- Live audit found two Instagram-created campaigns active with unsafe targeting: `Sept` (`120249679890510513`) and `Sept – Site` (`120249745435670513`). Both targeted Castellón, Gandía, Paterna and Sagunto rather than Valencia, combined RU+UA, included recent/frequent visitors, used Advantage+ expansion, and allowed age 65. Both were paused on 2026-09-30; preserve their history.
- Spend before pause: €35.10 from 24–30 Sep, 474 link clicks, 0 attributed bookings, 0 Pixel events in the latest 24h.
- Prepared two replacement campaign structures, all paused: Adult Ceramics `120249772446440513` and Kids Ceramics `120249772447210513`. Each has separate RU/UA ad sets, age 25–54, Valencia key `699854`, 17km, Advantage+ off, landing-page-view optimization, €1.25/day per ad set (€5/day total if all four are activated).
- Launch blocker: Meta automatically saves `location_types` as `home` + `frequently_in` even when the API explicitly sends `home` only. A second explicit update produced the same result. Do not activate until this is accepted as a platform limitation or a stricter supported targeting method is found.
- The drafts contain no ads yet. Approved RU/UA copy, images, destination URLs and UTM parameters must be added before launch.

### Campaign IDs (active, also in .campaign-ids)

- **Workshop** campaign: `120248011297180513`
  - Ad sets: RU=`120248011301760513`, UA=`120248011306620513`, EN=`120248011326580513`, ES=`120248011327440513`
  - Video IDs: RU=`1731122627885947`, UA=`27948590351415835`, EN=`1730819618045834`, ES=`1574793734274290`
- **Kids** campaign: `120248011753470513`
  - Ad sets: RU=`120248011753590513`, UA=`120248011754180513`
- **Coworking** campaign: `120248011726860513`
  - Ad set: `120248011728250513`

### Pending actions (Meta)
- Custom conversion (Schedule → Purchase, ID `980444324695740`) — still unverified, flagged every weekly report
- Old broken campaigns not yet deleted (Sales v1, Messages v1, WhatsApp v1, Kids Trial 2026-05, old IG posts)

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
| ~~2026-05-11~~ → **superseded** | System User "claude" now has full-write scope | Verified 2026-05-28 via `debug_token`: scopes include `ads_management`, `pages_manage_ads`, `business_management`. See Meta API section below. |
| 2026-05-11 | Course frame as "every Thursday" not "May 14 one-off" | Reflects actual recurring schedule + lets page stay relevant past first cohort |
| 2026-05-11 | Cookie consent banner enforced; no Pixel until accept | GDPR + DMA compliance for EU audience |
| 2026-05-28 | Rebuilt kids campaign via API after IG "Suggested Ads" quick-create produced malformed structure | Spain-wide geo, no language filter, 0 ads — wouldn't deliver. Replaced with proper Valencia 17km × RU/UA split via `scripts/launch-kids-campaign.py`. |
| 2026-05-28 | Kids ad sets ship with `advantage_audience: 0` (Advantage+ off) | Strict 28-45 age range conflicted with Advantage+ requirement (age_min ≤ 25, error 1870188). Honors the plan's age band; trade-off is no algorithm-driven audience expansion. Reconsider at Day 7 if reach is starved. |
| 2026-05-28 | Doubled kids ad-set budgets pre-delivery: RU €2→€4, UA €3→€6 (total €5→€10/day, 14-day cap €70→€140) | Both ads ACTIVE but zero delivery yet — no "learning phase" to reset. Doubling gives Meta more room to find the tight Valencia-17km × RU/UA parents audience. 1.5× UA-over-RU ratio preserved. |
| 2026-06-09 | Paused adult Thursday campaign (Sales v1, `120244368076410513`). Kids Trial stays ACTIVE at €10/day combined. | 6 days of delivery (€97 spent) produced 0 campaign-attributed bookings; the two weekend bookings came through DM, not ads. Decision: stop paying for adult-campaign exposure that isn't converting, keep kids campaign live through its launch weekend. Saves ~€20/day = ~€600/month. Re-evaluate after kids weekend (Sat 13 + Sun 14 June). |
| 2026-06-09 | Adult campaign cool-down 14 days, relaunch 2026-06-23 with new creative + EN ad set added (Valencia 17km × English). Full plan: `docs/plans/adult-campaign-relaunch-2026-06-23.md`. | Lifetime data showed frequency 5.0 / CTR halved week-over-week / CPM rising — classic audience saturation + creative fatigue. Cool-down lets audience "forget" before fresh creative. EN ad set expands beyond RU/UA diaspora to English-speaking expats and digital nomads, who are a documented secondary audience in Valencia. Diana to decide before relaunch: keep Sales objective or pivot to Messages objective (project pattern says DM-first converts better for €60 community offers). |
| 2026-06-09 | **Locale-targeting bug found + fixed.** Adult RU ad set (`120244412141780513`) was `locale: [10]` (Italian, not Russian). Adult UA ad set (`120244412143130513`) was `locale: [37]` (Bulgarian, not Ukrainian). Both corrected to RU=17, UA=52 today. Root cause: `scripts/local/build-meta-campaign.sh` shipped with wrong hardcoded IDs + wrong comment on 2026-05-11. Script now has runtime `verify_locale` guard that refuses to run if API disagrees with hardcoded values. New project rule added to `CLAUDE.md`. | 30 days of misfire — adult campaign showed Russian/Ukrainian creative to Italians and Bulgarians in Valencia. €141.89 spent, 891 clicks (warm visuals), 0 bookings (couldn't read copy). Kids campaign was correctly configured (May 28 setup verified locale IDs). Fix is no-op while campaign is paused; takes effect at relaunch 2026-06-23 when ad sets reactivate. |

## Launch Milestones

| Date | Milestone | Notes |
|---|---|---|
| 2026-05-12 | Stripe live mode confirmed | `pk_live_*` keys + EUR bank account added 11 May; no celebratory email — verified via dashboard |
| 2026-05-12 | First end-to-end smoke test passed | Cal.com → Stripe (€60 charge + auto-refund) → confirmation email → Pixel Schedule event in Meta — full funnel verified |
| 2026-05-12 | First Meta campaign live | Campaign `120244368076410513`, €10/day (RU+UA), end 2026-05-26. Custom Conversion `980444324695740` maps Schedule→Purchase €60 |
| 2026-05-13 / -14 | **First real paid booking** | Came via **Telegram DM** (direct booking link Diana shared), NOT from Meta campaign. €60 in. Workshop ran 2026-05-14 |
| 2026-05-14 | **First workshop run with paying customer** | Diana confirmed booking, class delivered |
| 2026-05-28 | **Kids Trial Class campaign built via API** | Campaign `Saged · Kids Trial · 2026-05` (`120245456772570513`), 2 ad sets RU€2/UA€3, all PAUSED. Diana flips ACTIVE after review. |

## Channel attribution learnings

- **Telegram DM with direct Cal.com link works** as a sales channel — Diana sent a booking link and it converted. The Pixel still fires Schedule on the success page regardless of how the user got there, so Telegram bookings show up in Meta's Pixel stats but NOT in the campaign-attributed conversions.
- For accurate campaign attribution, separate "Pixel total Schedule events" from "campaign-attributed Schedule events" when reading reports. The audit script + Ads Manager show the campaign-attributed number; the Pixel stats endpoint shows the raw total.
- Day 8 review (#62): if Telegram keeps converting and Meta hasn't, that's an important signal — Telegram is a better channel for this audience and may deserve its own attention (e.g., building the @sagedclub public channel from #39).

## Studio operations — open work (from 2026-06-08 meeting)

- **Kiln shelves**: need repair. Korytsia is on it.
- **Storage room under stairs**: cleaned out 2026-06-08. Plan: move existing shelves into this storage room; buy nicer shelves for the main studio space.
- **Kids class supplies**: need to buy more materials + create reusable stencils for the rotating subject-of-the-day format.

## Meta weekly content plan (active as of 2026-06-09)

Meta's Business Suite "Weekly plan" target — complete 4 of 6 tasks per week to satisfy the algorithm. 5 days left as of 2026-06-09.

| Task | Status (06-09) |
|---|---|
| Publish one ad | 0/1 |
| Publish 10 stories on Instagram | 8/10 |
| Publish one post on Facebook | 0/1 |
| Publish 4 posts on Instagram | 0/4 |
| Publish one story on Facebook | 0/1 |
| Always share posts to stories on Facebook | 0/1 (one-time toggle) |

Cheapest path to 4/6 this week: finish 2 more IG stories → toggle FB cross-share → publish 1 FB story → publish 1 FB post. Skips the heavier "4 IG posts" and "1 ad" lifts. The active Thursday adult campaign already counts as an ad in spirit, but Meta's task counts paid campaigns separately from organic posts — confirm in-app before assuming it ticks the "ad" box.

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


## Asset Archive (outside repo)

Photo + video originals live in `~/Documents/saged.old/`, not in the repo (large files).
Treat as the canonical source when filling galleries or generating new derivatives.

| Folder | Content | Use for |
|---|---|---|
| `Boosi photos/` | 66 photos, ~1 GB. Professional shoot of the **beads workshop**. | Past-event gallery, social proof imagery |
| `Vaamos Photos/Fotos/` | 58 photos, ~207 MB. Professional shoot of the **clay/ceramics workshop**. | Past-event gallery, workshop-in-action shots |
| `design/` | 93 designed graphics (IG posts, posters, logos) | Reference for brand voice; not raw photos |
| `inbox/` (in saged.club) | Current-drop raw photos + videos from Koritsa | Active campaign assets before processing |

All photos are Diana's (commissioned shoots). OK to use on saged.club + ad creatives.

## Social-share card spec

- **Dimensions**: 1200×630 JPEG (1.91:1 horizontal)
- **Declared in HTML must match actual file** — `og:image:width` and `og:image:height` were
  previously lying (2880×800 declared, file was 1286×1600). Verify on every update.
- **Source photo**: `assets/images/workshop-1.jpg` (Koritsa teaching with candles) is the strongest
  social card source — horizontal-friendly, warm, narrative.
- **Cache busting**: after deploying a new OG image, Facebook caches the old one. Use the
  [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) to force refresh.

## Bilingual mirror parity check

After any edit that touches structural HTML, verify RU/UA parity in seconds:

```bash
diff <(grep -oE '<section[^>]*class="[^"]+"|<h2[^>]*>[^<]+' index.html) \
     <(grep -oE '<section[^>]*class="[^"]+"|<h2[^>]*>[^<]+' uk/index.html)
# Expected: only RU↔UA text differences inside <h2>, identical section classes in identical positions.

echo "RU: $(grep -c '<section' index.html) sections / $(grep -c '<h2' index.html) h2"
echo "UA: $(grep -c '<section' uk/index.html) sections / $(grep -c '<h2' uk/index.html) h2"
# Counts must match exactly.
```

## CAPI access (resolved 2026-05-11)

Discovery: the **existing System User token** (in `.env` as `META_ACCESS_TOKEN`) works as the Conversions API access token. No separate CAPI token needed.

- Scope `ads_management` covers both Marketing API and Conversions API
- Verified by sending a test PageView event to `/1533639615120579/events` — Meta returned `events_received: 1`
- When Cal.com / Stripe webhooks land, server forwarder uses same token to send `Purchase` events

The Events Manager UI flow for dedicated tokens is blocked behind a "business email required" rule that we sidestepped. Optional cleanup: set a business email in Business Settings → Business Info to unblock the UI path too.

---

## Meta API & Tracking Reference

Hard-won knowledge about how Meta's Marketing API, Pixel, and Cal.com integration actually behave. Read this before touching campaigns, ad sets, or tracking code.

### Token scope (System User "claude")

The `META_ACCESS_TOKEN` in `.env` is a System User token with **full write scope**. Confirmed scopes via `debug_token`:

- `ads_management` — create/edit campaigns, ad sets, creatives, ads
- `pages_manage_ads` — page-level ad operations
- `business_management` — business-level write
- `ads_read`, `pages_read_engagement`, `catalog_management`, `pages_show_list`, `threads_business_basic`, `public_profile`

Token type: **SYSTEM_USER**, `expires_at: 0` (no expiry). App is named "studio audit" — misleading; do NOT assume read-only based on the name.

Verify scope anytime:
```bash
source .env
curl -s "https://graph.facebook.com/v25.0/debug_token?input_token=${META_ACCESS_TOKEN}&access_token=${META_ACCESS_TOKEN}" | python3 -m json.tool
```

**When to use API vs Ads Manager UI:**
- API: launching a new campaign from scratch, batch-creating ad variants, mirroring RU→UA, rebuilding after an edit-lock forces a recreate.
- UI: editing a single field, anything Diana is already mid-form on.
- Always create paid entities in `status: PAUSED`. Diana flips to `ACTIVE` herself in Ads Manager — she stays the one spending money.

### Edit locks (the "after publish" gotchas)

The Meta Marketing API blocks certain edits after entities are published. These aren't obvious until you hit them:

- **Campaign objective is locked** once any ad set exists. Error 1885073: `"Cannot update the objective of a campaign that has at least one advert set."` To change objective, rebuild the campaign.
- **Ad set optimization** (pixel, conversion event, custom conversion) is locked after first publish. Error 3260011. Workaround: create new ad sets inside the same campaign, leave old ones paused.
- **Ad creative** is locked on a published ad. Create a new ad to swap creative. Creatives can be reused by reference (`creative: {"creative_id": "..."}`) — no need to re-upload assets.

**Recovery pattern when a lock bites**: "create a new entity, leave old one paused, point scripts/IDs at the new one." Don't delete — pause is safer (can copy targeting back).

**Custom Conversion API quirk**: `POST /act_<id>/customconversions` uses `event_source_id`, not `pixel_id` (despite the rest of the API using `pixel_id`).

**Pixel stats lag**: `GET /<pixel-id>/stats?aggregation=event` has a ~30 min aggregation lag. Don't conclude an event didn't fire until 30+ min past the event timestamp. Test Events UI requires `test_event_code` in the event payload — production Cal.com events won't appear there.

### Cal.com Meta Pixel app — what it does and doesn't do

Cal.com's "Meta Pixel" app (slug `metapixel`) supports exactly 4 event types: `Lead`, `CompleteRegistration`, `Schedule`, `PageView`. **It cannot fire `Purchase` events**, and there's no value/currency parameter.

Source confirmed in `packages/app-store/metapixel/zod.ts` in the calcom/cal.com repo. The `trackingEvent` enum is `["Lead", "CompleteRegistration", "Schedule", "PageView"]`.

**Implication**: Sales-objective Meta campaigns need `Purchase` as the optimization event. Cal.com can't supply it directly. Workaround (working setup for Saged):
- **Custom Conversion** in Meta Events Manager: rule `event_name = Schedule`, category `PURCHASE`, default value €60
- Ad sets target via `promoted_object: {"custom_conversion_id": "<id>"}`
- Saged's live IDs: `980444324695740` (Schedule → Purchase €60), `1016380434145553` (Contact → Lead €30)
- Current IDs always in `.campaign-ids` (gitignored)

**Cal.com app install is per-event-type, not account-level.** Each event type needs its own Apps tab configured. Stripe must also be enabled per event type.

### Pixel-total vs campaign-attributed (don't confuse them)

Two different endpoints give different conversion counts:

- **`/<pixel-id>/stats?aggregation=event`** — raw total of events on the Pixel, regardless of source (ad, direct, organic, anywhere).
- **`/<campaign-id>/insights` with `actions`** — only conversions Meta could attribute to the campaign (saw/clicked ad within attribution window, then converted).

These can diverge meaningfully. Example from 2026-05-14 (48h after launch): Pixel total Schedule = 3, campaign-attributed = 0. The 3 were 2 smoke tests + 1 Telegram-DM booking. Reading Pixel-total alone would have suggested the campaign was working.

**Rules:**
- "Campaign performance" reports → use campaign insights, NOT Pixel stats
- "Is the Pixel firing at all" → use Pixel stats, source-agnostic
- Day 8 / Day 14 / weekly readouts → campaign-attributed is the relevant number
- Cal.com Schedule = total bookings (any source); campaign-attributed Schedule = ad-driven only. Subtract to estimate organic + direct.
- **Always tell Diana which one she's seeing** in any report.

### Consent Mode v2 — EU-compliant Pixel that still attributes

The "load Pixel only after Accept" pattern that most EU tutorials show **destroys ad attribution** — most ad-click visitors never accept, so Meta sees clicks but no visits.

Meta's documented fix: **Consent Mode v2**. Pixel loads on every page, but `fbq('consent', 'revoke')` is called *before* `fbq('init')`. In revoked state:
- Does NOT set tracking cookies (`_fbp`, etc.)
- Does NOT collect PII
- DOES fire `PageView` / `track()` events with Pixel ID + page URL + `fbclid` only

Enough for Meta to attribute ad click → site visit and optimize delivery, without identifying the visitor.

```js
!function(f,b,e,v,n,t,s){...}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

const consent = localStorage.getItem('saged_consent_v1');
if (consent !== 'accepted') fbq('consent', 'revoke');

fbq('init', PIXEL_ID);
fbq('track', 'PageView');

// On accept click:
fbq('consent', 'grant');
```

**Implemented on Saged 2026-05-17**. Before: ~80 PageView per 247 ad clicks (32% loss). After: expected ~95% fire rate.

**Compliance basis (Spain/EU)**: AEPD permits "necessary" analytics under legitimate-interest; revoked-state Pixel doesn't process PII (GDPR Recital 47). Banner still asks for elevated consent (cookies + PII). One-line revert if legal pushes back: change `if (consent !== 'accepted')` to `if (true)`.

### Hyperlocal geo tightening (counter-intuitive lever)

For hyperlocal Meta campaigns that aren't converting despite decent delivery, the highest-leverage targeting change is often **tightening** geo, not broadening.

**Evidence from Saged 2026-05-18 → 2026-05-20:**
- Before: Valencia + 25km radius, `location_types: ["home", "recent"]`
- After: Valencia + 17km radius (Meta's minimum), `location_types: ["home"]`

UA ad set, 48h after:
- CTR: 4.20% → **8.33%** (2×)
- CPC: €0.12 → **€0.03** (4× cheaper)
- Same budget, same creative

RU ad set: brief re-learning wobble (CTR dropped to 1.65% day 1) → recovered to 3.28% within 48h. **Don't panic-pause during the wobble.**

**Mechanism**: removing `"recent"` drops tourists; tightening radius drops 25-35km commuters who won't drive in for Thursday evening. Smaller pool, ~3× higher quality, algorithm converges faster.

**API constraints:**
- City radius minimum is **17km** (lower returns error 1487110)
- With `targeting_automation.advantage_audience: 1`, age max must be ≥65 (error 1870189)
- Updating targeting on existing ad set works fine — doesn't require recreating

**When to apply**: hyperlocal services where customers physically attend. After 5-7 days of delivery, frequency >2.5.
**When NOT**: e-commerce shipping nationally, services with broad area, brand-awareness campaigns.

### Audit findings from prior €105 spent (2026-05-11)

Why prior spend produced 0 bookings:
- Wrong objectives: MESSAGES / LINK_CLICKS, never SALES
- No Pixel installed
- No landing page
- No language targeting despite Russian-language creative
- All 9 ads were boosted IG posts (naming pattern: `Instagram post: ...`)
- Scattered targeting, no audience segmentation

Account state: lifetime spend €143.43, status UNSETTLED (cleared 2026-05-11). All 9 old campaigns deleted. Account back to status=1.

### Resources & IDs

- Ad account: `act_484884320671439` (in Saged.design BM, EUR, was wrongly Atlantic/Canary tz)
- System User: name "claude", ID `61589322372602`
- Marketing API version pinned: **v25.0** (v26.0 expected ~Sept 2026; v<24.0 retired 2026-06-09)
- Pixel ID + active campaign IDs: in `.campaign-ids` (gitignored)
- Lead-handling playbook: `docs/lead-handling.md`
- IG FAQ menu copy: `docs/instagram-faq.md`
- Locale IDs (verified via `/search?type=adlocale` on 2026-06-09): Russian = `17`, Ukrainian = `52`, English (UK) = `24`, English (US) = `6`, Spanish = `23`. **DO NOT trust hardcoded locale IDs** — past incidents shipped `5`/`120` (wrong) and later `10`/`37` (Italian/Bulgarian, also wrong). Project rule in CLAUDE.md mandates runtime verification via `verify_locale()` (reference: `scripts/local/build-meta-campaign.sh`).
- **Valencia Spain city key = `699854`**. Key `668776` = Shubra Tana, Egypt — do NOT use. Bug found 2026-07-20: all 7 active ad sets (Workshops RU/UA/EN/ES, Kids RU/UA, Coworking) were targeting Egypt. Fixed same day. Always verify via `/search?type=adgeolocation&q=Valencia&location_types=["city"]` — never hardcode from memory.
- Instagram business account ID linked to FB page: `17841428554040839` (needed in `object_story_spec.instagram_user_id`)
- Kids campaign launch script: `scripts/launch-kids-campaign.py` — idempotent (refuses if `KIDS_CAMPAIGN_ID` already set), supports `--dry-run`

## Website language strategy (2026-09-21)

- Russian is now the canonical and only public working language for the redesign.
- Finish and approve the complete Russian website before translating it.
- Ukrainian, English, and Spanish pages must not be maintained in parallel while the Russian structure is changing.
- Existing translated URLs should redirect to their matching Russian page to prevent dead ends.
- The header language dropdown shows Russian as active and UA/EN/ES as coming soon until their translations are rebuilt from the approved Russian site.
- The shared 2026 navigation uses a warm floating-glass bar, Inter UI labels, a terracotta contextual CTA, a compact mobile menu, and the language dropdown across every Russian page.

## October 2026 events and programme launches

- 3 October: Handpan School opening.
- October launch: Story Therapy.
- October launch: beginner ceramics in Spanish and English.
- 17 October at 13:00: Creative Lunch Club × Saged.club collaboration, with vinyl by Alisher. This is the confirmed date/time shown in the current event creative.
- 17 October at 16:00: mantra singing and meditation with Suma and Laura of Terapia Sonora.
- Lono Project event: date TBC.
- Tea Club: recurring October programme; dates not yet confirmed.
- Painting classes with Katerina: recurring October programme; dates not yet confirmed.

### Fairy Tale Therapy / Story Therapy format

- Participants build clay characters and miniature settings inspired by popular fairy tales and stories.
- Visual language: imaginative handmade story worlds rather than a conventional ceramics class.

---

## Korica (Lena) — Madeira trip

Korica is in Madeira from Thursday 9 October (temporary, not a departure from the studio).

---

## Studio finances — September 2026 summary

| Period | Amount | Type | Notes |
|--------|--------|------|-------|
| Sep 1–21 | €235.90 | Stripe | Clients direct |
| Sep 1–21 | €130 | Cash | Max collected |
| Sep 21 balance | €52.90 | Reconciliation | Studio 50% of €235.90 = €117.95; €65 cash on hand; difference = €52.90 |
| Sep 22 | €60 | Stripe | Gift certificate |
| Sep 25 | €60 | Cash | Collected |
| Sep 28 | €50 | Stripe | Class payment |
| Oct 5 | Pending | Stripe | Children's class — mum said she would pay |

---

## Active Stripe links (as of Sep 2026)

| Link | Amount | Notes |
|------|--------|-------|
| https://buy.stripe.com/4gMeVfcgmboi3PUcqqffy08 | €60 | Couple |
| https://buy.stripe.com/bJe9AVa8eboi1HM8aaffy09 | €30/person × 2 | Two people |
| https://book.stripe.com/aFa00l94a8c6bimduuffy0a | Variable | Booking link |
| https://buy.stripe.com/6oU6oJ806dwq3PU9eeffy07 | Variable | General payment |

## Handpan school Stripe links (added Oct 2026)

| Link | Amount | Notes |
|------|--------|-------|
| https://book.stripe.com/28E28t806gIC5Y21LMffy0o | €25 / €30 | One lesson (€25 first class, €30 drop-in) |
| https://buy.stripe.com/5kQcN794a9ga86a2PQffy0p | €100 | Monthly pass (4 Sundays) |

## Handpan school Stripe promo codes (Oct 2026)

| Promo code ID | Code | Use |
|---------------|------|-----|
| `promo_1UT7qIQuDZY27kuF6RusUQtx` | FRIENDS20 | Monthly subscription discount — shown on pricing card |
| `promo_1UT7ogQuDZY27kuFBdDrWJQB` | *(coupon, updated/replaced by above)* | Previous coupon — superseded |

---

## Tourist ceramic painting concept (on website, Sep 2026)

Diana confirmed that a "tourist tile painting" concept is already on the saged.club website:
- Tourist visits → paints a tile or ceramic piece at the studio
- Studio fires it → ships the finished piece to the client's home address
- Mentioned Airbnb and Groupon as potential distribution channels
- Spanish classic tile painting techniques (easy ones) are part of the planned tourist session offering

---

## Other studio contacts (Oct 2026)

- **Sandro**: finishing work at the studio in the evening (30 Sep). Likely a coworking member.

## October Instagram handpan announcement — 2026-10-09

- Diana requested a text-free hero background using the actual handpan session screenshot `~/Downloads/Screenshot 2026-10-09 at 14.03.08.png`.
- Match the supplied October feed references in `oct/Instagram post opening 56.png`, `61.png`, and `63.png`–`66.png`: periwinkle/lavender, pink, and warm coral-orange photographic grading.
- Announcement: Handpan School is open; schedule will be supplied in text separately. Do not infer a schedule from older graphics.

## Halloween event artwork — 2026-10-21

- Supplied `oct/Frame 98.png` announces Saged Club Halloween Witch Party, Friday 30 October 2026 at 16:00.
- No price, booking requirement, or programme details supplied with this artwork.

## Helena tea photo editing preference — 2026-10-21

- Diana rejected harsh cinematic facial shadows and dark grading on Helena's tea portrait. Use soft peach tones and preserve Helena's appearance.
- Requested removal of wall cords and extension of the photograph on both left and right sides.
- Revised asset: `oct/saged-helena-tea-peach-wide.png`.

## «Через огонь» franchise proposal — read 2026-10-21

Source: `Ritual/Франшиза «Через огонь».pdf`, dated 15 October 2026, 5 pages. Treat as a proposal, not approved commercial terms.
- Two-day Saged amulet ritual: intuitive selection, intention, symbol story, underglaze painting, firing, collective kiln opening. Symbols: Lotus (opening), Koi (movement toward a goal), Hamsa (protection).
- Diana supplies bisque amulets, symbol cards and cords; facilitator provides venue, group facilitation, approved pigments/glaze and firing. Molds stay with Diana. Proposed first facilitator: Koritsa.
- Suggested group 6–10; facilitator training and assisting Diana required; consistent script and brand.
- Proposed model: €15 participant kit including license. Suggested retail €55 early / €65 standard / €120 for two. These are discussion figures, not finalized prices. Entry fee, ordering lead time, territory and license terms remain open.
- Document states day one about 3 hours, but listed stages total 195 minutes (3h15); day two about 40 minutes. Next-morning opening depends on kiln cooling, not a guaranteed timing.

## «Через огонь» marketing drafts — received 2026-10-21

Source: `Ritual/Анонс «Через огонь».pdf`, 10 pages; Diana identifies these as marketing drafts, not approved publication-ready copy.
- Includes main announcement; Lotus, Koi and Hamsa symbol posts; compact promotional creative; teaser, process and remaining-spaces stories; landing-page draft with pricing and FAQ.
- Positioning: intuitive amulet choice, intention for a new phase, painting, firing and collective kiln opening. No drawing experience needed; relief guides painting.
- Draft pricing repeats €55 early / €65 standard / €120 for two. Date, time, capacity, early-booking deadline, refund terms and Instagram remain placeholders.
- Draft CTAs vary between direct message, profile link and payment. Gift certificates are offered in draft; operational availability not confirmed by this document.
- Editorial issue to resolve: public symbol explanations reveal the meanings before the promised intuitive choice without knowing meanings. Next-morning kiln opening remains an operational dependency, not verified by these drafts.

## Saged font 1.399 — 2026-10-21

- Diana supplied updated € and Ы SVGs, `Vector.svg` (Ю), and `Group 441.png` (Й).
- New local font package: `design/saged font/v1.399/`, includes TTF, WOFF, editable sources, build script and proof.
- Based on editable 1.398 source found in `~/Downloads/codex-design-studio/projects/saged-display-cyrillic/src/`. Only €, Ы, Ю, Й outlines changed; lowercase shares uppercase designs; vertical metrics retained.
- Й traced from supplied 105×148 PNG; needs Diana's visual review. No live website font replacement or system installation performed.

## Font cleanup — 2026-10-21

- At Diana's request, moved 293 old Saged font-work files to macOS Trash: previous development/output folders, older installed v1.396, duplicate supplied letter artwork, obsolete proofs and unreferenced web exports.
- Canonical retained package: `design/saged font/v1.399/`; v1.399 remains installed in `~/Library/Fonts/`.
- Pruned unused glyph-source revisions; 31 required glyph source files remain alongside the current supplied artwork and rebuild sources. Rebuild succeeded after cleanup without the old development folders.
- Older web fonts still referenced by existing pages were retained to avoid breaking them. No site deployment or replacement performed.
- Detailed move manifest: `design/saged font/v1.399/cleanup-record.json`.

## Logo motion study — 2026-10-22

- Diana requested animation between the supplied SPIRIT (green), MUSIC (purple), and ART (orange) PNG logos, exploring flips, turns, merging and warping.
- Local study in `design/logo-motion/`: 12-second square loop, 800×800 MP4 at 30 fps, GIF preview, HTML player, and editable `render.py`.
- Sequence: SPIRIT → MUSIC turning flip, MUSIC → ART liquid merge, ART → SPIRIT twisting warp. Original PNG lettering and colours retained at rest; dark background. This is a local creative study, not a website deployment.
