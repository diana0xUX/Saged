# Plan — Launch Kids Trial Class Meta campaign

_Status_: drafted 2026-05-28 (Fergie). Tracks issue **Epic — Launch Kids Trial Class Meta campaign**.

## Goal

Launch a properly-targeted Meta Traffic campaign for the €25 kids ceramic class to Valencia parents who speak RU or UA, ending in measurable WhatsApp leads (UTM `meta / kids-trial / ru|uk`) to the `/kids/` interest list.

## Why this campaign exists

- Kids product launched 2026-05-26 as a demand-validation trial (no fixed dates — waitlist model).
- Adult campaign (`120244368076410513`) ended 2026-05-26; the kids campaign was meant to follow.
- Diana tried to set it up today via Instagram's "Suggested Ads" quick-create — the result is malformed (see Findings below).

## Findings — current Meta state (2026-05-28)

The kids campaign Diana started today is **ACTIVE but won't deliver**, and two other ACTIVE campaigns are stale.

| Campaign ID | Name | Objective | Status | Issue |
|---|---|---|---|---|
| `120245448073800513` | Traffic campaign for Instagram advertisers 5/28/2026 | OUTCOME_TRAFFIC | ACTIVE | Spain-wide geo, age 35-50, no language, IG DM destination, **0 ads** → won't deliver, won't spend, but blocks a clean launch |
| `120244368076410513` | Saged · Керамика с Корицей · Sales · v1 | OUTCOME_SALES | ACTIVE | Adult campaign — `stop_time` 2026-05-26, should be PAUSED |
| `120244806078280513` | Instagram post: We're opening a coworking space... | OUTCOME_ENGAGEMENT | ACTIVE | Coworking boost — `stop_time` 2026-05-25, should be PAUSED |

Other state:
- Landing pages live: `/kids/`, `/uk/kids/`, `/en/kids/` (RU primary, UA mirror, EN courtesy)
- 6 ad creatives ready: `assets/images/ad-kids-{ru,ua}-{1x1,4x5,9x16}.png`
- Copy brief: `references/meta-ad-copy-kids.md`
- Launch playbook (manual): `docs/launch-kids-campaign.md` — superseded by this API plan
- System User token has full write scope — campaign creation can be API-driven

## Approach

**Rebuild from scratch via API.** The broken quick-create cannot be edited cleanly because the non-negotiable rule "RU + UA separate ad sets" requires two ad sets, not one re-targeted ad set.

Pattern (per `CLAUDE.md`):
- All entities created via API in `status: PAUSED`
- Diana reviews in Ads Manager and flips to ACTIVE — she stays the one spending money

### Campaign-level config

| Field | Value |
|---|---|
| Name | `Saged · Kids Trial · 2026-05` |
| Objective | `OUTCOME_TRAFFIC` |
| Buying type | `AUCTION` |
| Budget strategy | Ad-set budget (not CBO) |
| Status | `PAUSED` |

### Ad set — RU

| Field | Value |
|---|---|
| Name | `Kids · RU · Valencia 17km` |
| Optimization goal | `LANDING_PAGE_VIEWS` |
| Destination | Website (`saged.club/kids/`) |
| Daily budget | €4.00 (400 cents) — doubled from launch-day €2 on 2026-05-28 before any delivery |
| Schedule | Start tomorrow, run 14 days |
| Geo | Valencia city, +17km, **residents only** (`location_types: ["home"]`) |
| Age | 28–45 |
| Languages | Russian (locale `17`) |
| Targeting | Parents (6–12 yrs) AND interests: Arts and crafts / Pottery / Family-friendly activities / Children's activities |
| Placements | Advantage+ placements (auto) |
| Advantage+ audience | **OFF** (`advantage_audience: 0`) — required because age_min < 26 triggers error 1870188 when Advantage+ is on; revisit at Day 7 if reach is starved |

### Ad set — UA

Identical to RU except:
- Name: `Kids · UA · Valencia 17km`
- Daily budget: **€6.00** — doubled from launch-day €3 on 2026-05-28. UA audience is smaller but converted better on the adult campaign; biased budget reflects that. Maintains 1.5× ratio vs RU.
- Languages: Ukrainian (locale `52`)

### Ads

- **`Kids · RU · v1`** — single image (`ad-kids-ru-4x5.png` + 1x1 + 9x16 placement variants), Primary Text from `references/meta-ad-copy-kids.md` § Russian, CTA `LEARN_MORE`, URL `https://saged.club/kids/?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=ru`
- **`Kids · UA · v1`** — same shape with UA assets + copy + `/uk/kids/?utm_content=uk`

## Phased breakdown

### Phase 1 · Clean slate (urgent)
Pause every ACTIVE campaign that's broken or past its end date so the account is in a known state before launch.

### Phase 2 · Build the kids campaign (PAUSED) via API
Create campaign + 2 ad sets + 2 ads, all in PAUSED status. Persist new IDs to `.campaign-ids`.

### Phase 3 · Diana flips ACTIVE
Diana opens Ads Manager, sanity-checks the structure, flips both ad sets to ACTIVE.

### Phase 4 · Watch (Day 3 / 7 / 14)
- Day 3: confirm delivery + first leads
- Day 7: pause underperforming ad set if CTR < 1%
- Day 14: decision — extend / kill / iterate

### Phase 5 · Parity polish
- IG FAQ chips routing: kids parents landing in IG DM see chips that answer for adult class (€60). Fix: either keep ad destination at website (current plan), or add a kids-aware chip variant.
- Update `KNOWLEDGE.md` with new campaign IDs post-launch
- Mirror any creative learnings back into the next iteration

## Risk register

| Risk | Mitigation |
|---|---|
| Diana accidentally flips ACTIVE before Day 3 inbox is monitored | Schedule it so start_time = tomorrow 09:00; she'll see WhatsApp pings within hours |
| Edit lock hits mid-build (e.g., ad set optimization lock after first publish) | Build in one shot — campaign → both ad sets → both ads → done. Don't ship half. |
| Kids waitlist model creates "what's the date?" friction in DMs | Already addressed in `docs/lead-handling.md` — operators say "first to know when we set the date" |
| IG FAQ chip routing confuses parent leads with adult-class answer | Mitigated by routing to website (not IG DM). Parents who DM anyway hit operator triage. |

## Success criteria (Day 14)

- Delivery: > 200 landing-page views across both ad sets
- CPC: < €0.50
- WhatsApp parent leads: ≥ 4 (the "set a date" threshold)
- Cost per lead: < €15

## Files this plan touches

- `docs/plans/kids-campaign.md` — this file
- `scripts/launch-kids-campaign.py` — new (Phase 2 API script)
- `.campaign-ids` — new IDs appended (gitignored)
- `KNOWLEDGE.md` § Resources & IDs — refresh after launch
- `REPORT.md` — refresh after Day 14 decision
