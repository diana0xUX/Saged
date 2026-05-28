# Meta ad copy — Kids Trial Class (RU + UA)

> **Update 2026-05-28**: campaign was launched via API (`scripts/launch-kids-campaign.py`), not Ads Manager UI. Same copy + targeting. Budgets in this brief are launch-day numbers (€2 RU / €3 UA); current budgets are €4 RU / €6 UA (doubled before any delivery). See `docs/plans/kids-campaign.md` for live spec.

Campaign for the €25 single-class kids' product. DM-first conversion (WhatsApp interest list — no Cal.com booking for kids).

Character limits Meta enforces:
- **Primary text**: 125 chars before "see more" truncation (max 2,200)
- **Headline**: 27 chars before truncation (max 40)
- **Description**: 27 chars before truncation (max 30)
- **CTA**: Pre-defined list (LEARN_MORE, SEND_MESSAGE, SIGN_UP, etc.)

---

## Campaign-level

| Setting | Value |
|---|---|
| Campaign name | `Saged - Kids Trial Class - 2026-05` |
| Objective | Traffic (optimize for Landing Page Views) |
| Daily budget | €5/day total |
| Duration | 14 days, evaluate Day 7 |
| Conversion pattern | Landing page → on-page form (fires Pixel `Contact`) OR WA CTA click |
| Languages | RU + UA only (no EN — Diana's decision 2026-05-26) |
| Budget split | RU €2 · UA €3 (biased to UA, mirrors adult campaign learning where UA hit 8% CTR) |

---

## 🇷🇺 Russian — Ad Set A

**Ad Set name:** `Kids · RU · Valencia 17km`
**Daily budget:** €2
**Language targeting:** Russian

### Ad 1A — Primary

**Primary text** (~120 chars):
```
Полуторачасовой класс лепки для детей 6–10 лет с украинской керамисткой Корицей. Ребёнок уйдёт с готовой керамикой в тот же день. Маленькая группа в старой Валенсии. 25 €.
```

**Headline** (24 chars):
```
Керамика для детей · 25 €
```

**Description** (26 chars):
```
Старая Валенсия · 1,5 часа
```

**CTA:** `LEARN_MORE` (Узнать больше)
**Destination URL:** `https://saged.club/kids/`
**URL parameters:** `utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=ru`

**Creative:**
- Feed (1:1 + 4:5): `assets/images/ad-kids-ru-4x5.png`
- Stories / Reels (9:16): `assets/images/ad-kids-ru-9x16.png`

---

## 🇺🇦 Ukrainian — Ad Set B

**Ad Set name:** `Kids · UA · Valencia 17km`
**Daily budget:** €3
**Language targeting:** Ukrainian

### Ad 1B — Primary

**Primary text** (~118 chars):
```
Півторагодинний клас ліплення для дітей 6–10 років з українською керамісткою Корицею. Дитина забере готову кераміку додому того ж дня. Маленька група у старій Валенсії. 25 €.
```

**Headline** (24 chars):
```
Кераміка для дітей · 25 €
```

**Description** (28 chars):
```
Стара Валенсія · 1,5 години
```

**CTA:** `LEARN_MORE` (Дізнатися більше)
**Destination URL:** `https://saged.club/uk/kids/`
**URL parameters:** `utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=uk`

**Creative:**
- Feed (1:1 + 4:5): `assets/images/ad-kids-ua-4x5.png`
- Stories / Reels (9:16): `assets/images/ad-kids-ua-9x16.png`

---

## Audience spec (same per ad set, only language differs)

| Field | Value |
|---|---|
| Location | València, Spain — 17km radius |
| Location type | People **living** in this location (residents only) |
| Age | 28 – 45 |
| Gender | All |
| Languages | RU set → Russian · UA set → Ukrainian |
| Detailed targeting | Demographics > Parents (children 6–12) AND any of: Arts and crafts · Family-friendly activities · Pottery · Children's activities |
| Placements | Advantage+ (auto) — FB + IG feed + stories + reels |

---

## Pre-launch checklist

- [x] Pixel `Contact` event fires on parent+kid form submit (wired in `assets/script.js`, commit `ebe11d2`)
- [ ] Confirm Pixel `Contact` also fires on the kids hero "Записаться" → WhatsApp CTA click
- [ ] Creative ready: 4:5 + 9:16 PNGs in repo at `assets/images/ad-kids-{ru,ua}-{4x5,9x16}.png` ✅
- [ ] UTM tracking added to landing page form so WA messages identify ad source (5-min code change)
- [ ] Business Verification cleared (in review 2026-05-26, ~2 business days)

---

## Launch checklist — Ads Manager UI

1. Ads Manager → **+ Create** → **Traffic** objective → Continue
2. Campaign name: `Saged - Kids Trial Class - 2026-05`
3. Budget: **Campaign budget optimization OFF** (per-ad-set control)
4. **Ad Set 1 (RU):**
   - Name: `Kids · RU · Valencia 17km`
   - Daily budget: **€2**
   - Conversion location: **Website**
   - Performance goal: **Maximize landing page views**
   - Audience: paste from above
   - Placements: **Advantage+ Placements**
   - Schedule: start tomorrow, end +14 days
5. **Ad inside Ad Set 1:**
   - Format: **Single image**
   - Placement assets:
     - Feed → upload `ad-kids-ru-4x5.png`
     - Stories/Reels → upload `ad-kids-ru-9x16.png`
   - Paste copy from § Ad 1A above
   - URL: `https://saged.club/kids/?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=ru`
6. **Duplicate Ad Set** → name `Kids · UA · Valencia 17km`, set budget €3, switch language to Ukrainian, swap images to `ad-kids-ua-*.png`, swap copy to UA, change URL to `/uk/kids/` with `utm_content=uk`
7. Review, Publish

---

## Day 7 evaluation rubric

Pause / adjust if any of these:

| Metric | Threshold | Action if hit |
|---|---|---|
| CTR < 1% | Creative or audience mismatch | Test alternate headline |
| CPC > €1.50 | Audience too narrow or competitive | Loosen interests, widen age |
| Landing page views / spend ratio low | Mobile drop-off | Check page load, form UX |
| Contact events = 0 | Funnel broken | Check Pixel + form JS |
| Contact events earned · CAC > €15 | Unprofitable at €25 product | Pause, rebuild |

Keep / scale if any:

| Metric | Threshold | Action |
|---|---|---|
| CTR > 3% | Strong creative-audience fit | Hold, let it run full 14d |
| CPC < €0.50 | Healthy reach | Consider bumping budget +€1/day |
| Contact events earned at < €5 each | Strong intent | Scale UA or RU side that's winning |
