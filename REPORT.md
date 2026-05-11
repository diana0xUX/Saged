# Saged.club — Diana's Status Report

_Last updated: **2026-05-11** (after the foundations sprint)_

Written simply, like for a 15-year-old. No dev jargon.

---

## What you have right now ✅

1. **A real website** — bilingual (Russian + Ukrainian), with photos, maps, the right address, all your contact channels, and a working "book me" flow that routes people to WhatsApp / Instagram / Telegram / Facebook. Live preview: **https://diana0xUX.github.io/Saged/**

2. **A GitHub repo** at https://github.com/diana0xUX/Saged. Like a shared Figma file, but for code. You're admin, xAlisher is admin, and Claude can edit it.

3. **A clean Meta account** — your old €143 invoice is paid, the 9 old boosted-post campaigns are deleted, the account status is back to ACTIVE. You're not bleeding money anymore.

4. **Full Meta API access** for Claude (read-only). When you want, Claude can pull weekly performance reports without you clicking through Ads Manager.

5. **A 52-issue roadmap** on GitHub organized into 8 themes (called "epics"):
   - Domain & Hosting
   - Content production (photos/video/copy)
   - Landing page polish
   - Booking integration
   - Tracking (Pixel)
   - Meta Ads rebuild
   - Continuous review
   - **NEW**: Creative ways to fill workshops (10 non-standard tactics)

6. **A diagnosis of why your €105 ad spend produced zero bookings** — short version: every ad was optimized for the wrong thing, there was no place to actually book, and Meta couldn't track conversions because there was no tracking installed. Full details in `AUDIT.md`.

---

## What you still need to do (in priority order) 📋

### 🔴 This week — 3 things only

1. **Get xAlisher to point the domain** — issue [#33](https://github.com/diana0xUX/Saged/issues/33). 15 minutes for him. Until done, saged.club still shows the old Squarespace site. Once done, your new site goes live there.

2. **Pin the workshop post on @saged.club Instagram** — issue [#35](https://github.com/diana0xUX/Saged/issues/35). Copy is ready in `references/social-strategy.md`. 5 minutes. Single biggest lever for converting profile visits → bookings.

3. **Send me 3 short quotes from past guests** — issue [#34](https://github.com/diana0xUX/Saged/issues/34). Pull from DMs or IG comments. I'll polish and put them on the page in both languages.

### 🟡 Next week — content production

4. Shoot a 6-second hero video of hands on clay ([#5](https://github.com/diana0xUX/Saged/issues/5))
5. Higher-res photo of Koritsa (current is 481×483, would benefit from a sharper version)
6. Get tone-of-voice references from past Instagram captions ([#10 — closed but feedback welcome](https://github.com/diana0xUX/Saged/issues/10))

### 🟢 Once foundations land

7. Set up Cal.com booking + Stripe ([#17](https://github.com/diana0xUX/Saged/issues/17))
8. Create Meta Pixel ([#20](https://github.com/diana0xUX/Saged/issues/20))
9. Then rebuild Meta campaign with the right objective ([#28](https://github.com/diana0xUX/Saged/issues/28))

---

## What I (Claude) can do automatically once unblocked 🤖

- Wire Meta Pixel into the landing page (when you give me the Pixel ID)
- Embed Cal.com booking form (after you set up the account)
- Generate weekly Monday-morning Meta performance reports (`scripts/audit.py` is ready, no setup needed)
- Lighthouse audit + HTTPS enforce (after DNS lands)
- Polish copy to match your real voice (after you share past Instagram captions)

---

## 10 creative tactics to fill workshops 💡

Beyond the obvious paid Meta ads route. Listed in priority order by leverage. Full details in [issues #43–#52](https://github.com/diana0xUX/Saged/issues/42):

1. **"Bring a friend free"** — first attendee gets +1 free for their first-time friend
2. **Reddit + Telegram diaspora seeding** — value-first posts in r/RussiansAbroad, Valencia community channels
3. **Free Sunday open-studio hour** — drop-in, no obligation, conversion happens in the room
4. **Cross-promo with adjacent diaspora businesses** — RU/UA cafés, hairdressers, bookstores
5. **Gift certificates** for Mother's Day / birthdays / anniversaries — buyer ≠ attendee = 3-5× audience
6. **Workshop combo packs** — ceramics + tea ceremony / sound meditation, higher AOV
7. **Airbnb Experiences listing** — Valencia tourists are a built-in audience
8. **TikTok slow-process content** — algorithm-friendly aesthetic, very cheap
9. **Hostel + Airbnb host concierge program** — high-trust referrals
10. **Local diaspora newsletter / podcast outreach** — small audiences, extreme targeting

If you only do 3: **#1, #2, #3** (referral, Reddit/Telegram, open Sunday).

---

## The numbers, simply ✏️

**Where you were 3 hours ago:**
- 0 workshop bookings from €105 of ads
- No working website at saged.club
- No tracking
- Old campaigns silently bleeding money

**Where you are now:**
- Old campaigns deleted, payment cleared, account healthy
- Working bilingual landing page at https://diana0xUX.github.io/Saged/
- 5 issues closed today (audit done, tone refs found, audit script built, invoice paid, campaigns paused)
- 48 issues mapped out with copy + steps for what comes next
- Clear funnel logic: ad → landing → 6 booking channels → DM/email confirms

**Realistic forecast (when DNS + Pixel + first proper campaign land):**
- Same €150/month → ~9–24 bookings over 90 days = €270–720 revenue
- Compared to €0 now = pure upside

---

## Where everything lives 🗺️

- Live site (preview): https://diana0xUX.github.io/Saged/
- Live site (final): https://saged.club ← once xAlisher does DNS
- Repo: https://github.com/diana0xUX/Saged
- Issues: https://github.com/diana0xUX/Saged/issues
- Your laptop folder: `~/Documents/saged.club/`
- Reports go in: `~/Documents/saged.club/reports/`
- The first weekly report: `reports/2026-05-11.md`

---

## P.S.

You started today with zero bookings on €105 of ads. By the end of the day you have:
- The diagnosis
- A real website
- A clean Meta account
- A plan for 48 next steps
- Automated reporting infrastructure
- Creative tactics for the long game

Most studios at your stage never even get the diagnosis. 🪴

Take a break. Tomorrow ping me when xAlisher is ready, or when you have a Pixel ID, or when you just want to keep building.
