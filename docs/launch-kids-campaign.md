# Launch the Kids Trial Class Meta campaign — step by step

> **⚠️ Superseded 2026-05-28.** The campaign was launched via API instead of clicking through Ads Manager (`scripts/launch-kids-campaign.py`). The current plan + spec is in [`docs/plans/kids-campaign.md`](plans/kids-campaign.md). This doc is preserved as a reference for the manual click path in case API access is ever lost or a fresh BM needs a quick start. Budgets here are launch-day numbers; current budgets are in the plan doc.

**Time needed**: ~15 minutes of clicking.
**Pre-loaded brief**: `references/meta-ad-copy-kids.md` — keep this open in another tab; you'll copy from it.

---

## Phase A · Pre-flight (1 min)

- [ ] Open the right ad account in Ads Manager: **Diana Voronec's ad account** (not "Saged.club" if there's a second one — the wrong one has zero campaigns visible)
- [ ] Open `https://saged.club/kids/` in another tab — confirm the form near the bottom loads
- [ ] Open `references/meta-ad-copy-kids.md` in your editor — you'll paste from here

---

## Phase B · Create the campaign (2 min)

- [ ] Click the green **+ Create** button at the top-left of the campaigns table
- [ ] In the popup: **Buying type** = `Auction` (leave default)
- [ ] **Choose a campaign objective** → tick **Traffic** (second from top)
- [ ] Click **Continue**
- [ ] On the campaign settings screen, in the **Campaign name** field paste:
  ```
  Saged - Kids Trial Class - 2026-05
  ```
- [ ] **Budget strategy** → select **Ad set budget** (the second radio — not "Campaign budget")
- [ ] Leave Live video ad: Off, A/B test: Off
- [ ] Click **Next** (bottom right)

---

## Phase C · Build the RU ad set (4 min)

You're now on the ad set screen. Top left should auto-name something like "New Traffic ad set". Rename it.

- [ ] **Ad set name**:
  ```
  Kids · RU · Valencia 17km
  ```
- [ ] **Conversion location**: select **Website**
- [ ] **Performance goal**: select **Maximize number of landing page views**
- [ ] **Daily budget**: `2.00 EUR`
- [ ] **Schedule** → **Start date**: tomorrow's date. **End date**: tomorrow + 14 days
- [ ] **Audience** section:
  - [ ] **Locations** → click ✕ to remove any default. Add **València, Spain**. Below it, set radius to **+17 km**.
  - [ ] **Location type**: switch from "People living in or recently in this location" → **People living in this location** (residents only)
  - [ ] **Age**: `28` to `45`
  - [ ] **Gender**: All
  - [ ] **Languages**: type and add **Russian**
  - [ ] **Detailed targeting** → click "Add demographics, interests or behaviours" → search and add:
    - Demographics > Parents > **Parents (with children 6–12 years)**
    - Then click **Narrow audience** (the "AND" link) → search and add interests, any of: **Arts and crafts**, **Pottery**, **Family-friendly activities**, **Children's activities**
- [ ] **Placements** → select **Advantage+ placements** (recommended; auto-distributes to feed/stories/reels)
- [ ] Click **Next** (bottom right)

---

## Phase D · Build the RU ad (3 min)

You're now on the ad creation screen.

- [ ] **Ad name**:
  ```
  Kids · RU · v1
  ```
- [ ] **Identity**:
  - Facebook Page: **Saged.club** (should auto-select)
  - Instagram account: **@saged.club** (should auto-select)
- [ ] **Ad setup** → Format: **Single image or video**
- [ ] **Ad creative** → **Media** → click **Add media** → **Add image**
  - Upload from your Mac: `~/Documents/saged.club/assets/images/ad-kids-ru-4x5.png`
  - (Optional but better) click **+ Add image** twice more to add the 1:1 and 9:16 variants for placement-specific delivery: `ad-kids-ru-1x1.png` and `ad-kids-ru-9x16.png`
- [ ] **Primary text** (paste from `references/meta-ad-copy-kids.md` § Russian):
  ```
  Полуторачасовой класс лепки для детей 6–10 лет с украинской керамисткой Корицей. Ребёнок уйдёт с готовой керамикой в тот же день. Маленькая группа в старой Валенсии. 25 €.
  ```
- [ ] **Headline**:
  ```
  Керамика для детей · 25 €
  ```
- [ ] **Description**:
  ```
  Старая Валенсия · 1,5 часа
  ```
- [ ] **Destination** → **Website URL**:
  ```
  https://saged.club/kids/?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=ru
  ```
- [ ] **Call to action** button: select **Learn More**
- [ ] Scroll up — preview should show the ad in feed + stories. Looks right? Click **Next** (bottom right) OR find the "Save draft" / outline button.

---

## Phase E · Duplicate for Ukrainian (3 min)

In the left sidebar you now see: Campaign > Ad set "Kids · RU · Valencia 17km" > Ad "Kids · RU · v1".

- [ ] Right-click on **Kids · RU · Valencia 17km** ad set → **Duplicate**
  (or use the "..." menu next to the ad set name → Duplicate)
- [ ] On the duplicated ad set, change:
  - [ ] **Name** → `Kids · UA · Valencia 17km`
  - [ ] **Daily budget** → `3.00 EUR`
  - [ ] **Languages** → remove Russian, add **Ukrainian**
- [ ] Click into the ad inside the duplicated set:
  - [ ] **Ad name** → `Kids · UA · v1`
  - [ ] **Media** → remove the RU images, upload `ad-kids-ua-4x5.png` (plus `ad-kids-ua-1x1.png` + `ad-kids-ua-9x16.png` if doing placement-specific)
  - [ ] **Primary text** (paste UA version from brief):
    ```
    Півторагодинний клас ліплення для дітей 6–10 років з українською керамісткою Корицею. Дитина забере готову кераміку додому того ж дня. Маленька група у старій Валенсії. 25 €.
    ```
  - [ ] **Headline**:
    ```
    Кераміка для дітей · 25 €
    ```
  - [ ] **Description**:
    ```
    Стара Валенсія · 1,5 години
    ```
  - [ ] **Destination URL**:
    ```
    https://saged.club/uk/kids/?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=uk
    ```
  - [ ] **CTA**: Learn More (already set from duplicate, verify)

---

## Phase F · Review + publish (2 min)

- [ ] Top right → click **Review and publish** (button has a count, like "Review and publish (3)")
- [ ] Sanity check the summary screen:
  - 1 campaign: **Saged - Kids Trial Class - 2026-05**
  - 2 ad sets: RU (€2/day) + UA (€3/day) = **€5/day total**
  - 2 ads: 1 RU + 1 UA
  - 14 days = €70 max spend
- [ ] Click **Publish**
- [ ] Meta will say "In Review" — normal. Approval usually takes **30 min to 24 hours**.

---

## After launch

- [ ] **Day 1**: check Meta Ads Manager next morning. If both ads show "Active" (not "Rejected") and impressions > 0, you're live.
- [ ] **Day 3**: check WhatsApp inbox for first parent leads. Look for `— Источник: meta / kids-trial / ru` (or `uk`) at the end of the message — that's the UTM attribution we wired.
- [ ] **Day 7**: read the daily report (`reports/daily/*.md`). If CPC < €0.50 and Contact events > 0, keep running. If CTR < 1% on either ad set, pause that side.
- [ ] **Day 14**: campaign auto-ends. Decision: extend / kill / iterate creative.

Full Day-7 evaluation rubric is in `references/meta-ad-copy-kids.md`.

---

## If you get stuck

Screenshot the screen you're on and send it to me — I'll tell you the next click. The most common stumbles:

- **"Ad rejected"** after publish → click the ad, read Meta's reason. Usually a copy or image issue, easy fix.
- **"Budget too low"** error → bump RU to €3, UA to €4 (Meta sometimes requires €3 minimum per ad set in EUR).
- **Audience too narrow** warning → loosen detailed targeting (remove one interest at a time).
- **Image rejected for too much text** → unlikely with your creatives (they're light on text), but if so, use a version with less type overlay.
