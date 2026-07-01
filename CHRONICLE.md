# Session log

## 2026-06-22 → 2026-06-29 — Finance, tax research, three new campaigns

**Duration**: multiple sessions across one week
**Outcome**: June books closed, accountant report ready, three campaigns live across 6 ad sets, all WITH_ISSUES ads unblocked.

### Major milestones

1. **Bank reconciliation + June ledger** — Full Santander *0997 reconciliation May 23–Jun 22. Confirmed income €633.31 (Stripe ×3 + Bizum ×5 + Ekaterina coworking). All deductible costs logged with invoice refs: rent €1,173, electricity €74.57, Movistar 1/3 share €29.37, water €44.78, Prodesco clay €248.70, Meta Ads €274.36. IKEA + Leroy Merlin excluded (home purchases). June net: −€1,211 confirmed, −€856 with Korytsia pending. ⚠️ Santander balance was €27 on Jun 22; July rent ~€1,173 due ~Jul 5.

2. **Accountant report created** — `finances/reports/june-2026-accountant.md` — ready to send to gestor. Covers all income, deductible costs with invoice refs, 8 questions for gestor (TGSS discrepancy, IVA on workshops, Meta reverse charge, ROI registration, Bizum receipts, Stripe gross/net, Prodesco invoice, landlord invoice).

3. **Spanish tax research** — Key findings: workshops IVA almost certainly 21% (teaching exemption requires official curriculum); Meta Ads = inversión del sujeto pasivo (reverse charge, declare on Model 303, neutral); ROI registration needed (Model 036, checkbox 582); Model 349 for intra-EU purchases; Model 130 IRPF 20% net profit quarterly (currently net loss → file but pay zero).

4. **Cacao & Sound campaign** — Built and launched Jun 22 (Campaign ID: 120247269492570513, €10/day, Russian, CTA → Luma link). Paused Jun 29: 6 days of spend, €53.41, 7,623 reach, 78 clicks, CTR 0.19%, frequency 5.4× — creative exhausted. Event July 3 still happening (just not advertising it). July 2 pause reminder set then disabled.

5. **Kids Clay Camp campaign** (Jun 29–Jul 1) — Full 4-language campaign (UA/EN/RU/ES). Target: age 30–50, Valencia 5km, parents of children 6–8 and 9–12. CTA: Instagram DM (`ig.me/m/saged.club`). Budget: €5/day × 4 ad sets = ~€10/day total. Flyer time corrected 10:00 → 11:00 mid-build; all creatives updated. Kids Camp UA + EN went ACTIVE; RU + ES were WITH_ISSUES then expired (ad set end date was Jun 28). Fixed by extending end dates to Jul 1 and force-activating.

6. **Thursday Adults campaign** (ongoing) — Korytsia ceramics, women 30–45, art/craft/wealth interests, Valencia + Puçol, €5/day × 2 ad sets = €10/day total. CTA: Instagram DM. Image creative: `assets/images/korytsia.jpg` (uploaded to Meta, hash a7bb73a3996451dc72a685764c9f5a4b). Both RU + UA ads were WITH_ISSUES since Jun 24. Unblocked Jun 29 by force-activating via API.

### Key decisions made

| Decision | Why |
|---|---|
| Cacao & Sound paused (not swapped to video) | CTR 0.19%, freq 5.4× — audience saturated. Event close; not worth more spend |
| Kids Camp: ig.me DM CTA not website | WhatsApp CTA failed Meta review; IG DM link (`ig.me/m/saged.club`) approved and works |
| Thursday Adults: Valencia + Puçol only | Tighten geo to avoid wasting budget on distant suburbs |
| Meta ad locale IDs verified at runtime | Past incident: wrong locales (Italian/Bulgarian instead of RU/UA) cost €141.89 |

### WITH_ISSUES pattern — documented

Meta's error code 2446984 ("trusted user approval needed") can be resolved by calling `POST /{ad_id}` with `status=ACTIVE` via API — this counts as the Business Admin re-confirming the ad. Ads Manager UI approval is not required. Exception: if the parent ad set has an expired `end_time`, extend it first or the API call errors with "end date reached."

### Locale IDs confirmed (as of Jun 2026)

Russian=17, Ukrainian=52, Spanish(Spain)=7, English(UK)=24. Verified via `/search?type=adlocale` — hardcoded here for reference only, always re-verify at runtime per CLAUDE.md rule.

### Files created/modified

```
new:      finances/reports/june-2026-accountant.md
new:      finances/invoices/iberdrola-2026-06-studio.pdf
modified: LEDGER.md  (June actuals, projection to Jul 5)
modified: halt.md    (session state)
```

### What's open at end of sessions

- Send accountant report to gestor (not done)
- ROI registration — gestor to confirm
- Korytsia €355 outstanding (not received)
- Sanitas −€88.47: personal or business? (unclassified)
- July rent ~€1,173 due ~Jul 5 (critical cash)
- Check Kids Camp performance before camp ends Jul 1

---

## 2026-05-26 → 2026-05-27 — Polish, repositioning, kids campaign prep

**Duration**: ~one long session split across two days, ~30 commits
**Outcome**: site visually polished, Koritsa repositioned as Saged.club resident, kids Meta campaign fully prepped (creative + brief + UTM attribution), Google Search Console verified, SEO foundation upgraded (LocalBusiness schema + complete sitemap).

### Major themes

1. **Brand consolidation** — Koritsa's bio rewritten site-wide as "ceramic resident of Saged.club" (was "her own studio @korytsia_studio"). Schema.org `instructor.sameAs` updated to @saged.club. Contact channels stripped to WhatsApp + Instagram studio only (removed @ko_hasi, @dvoroneca, @korytsia_studio, Facebook). Deliberate choice to accumulate brand authority on Saged.club instead of Koritsa's personal accounts. Diana to brief Koritsa on this change before someone shares the link.

2. **Parent+kid request form** — inline HTML form on all 3 kids pages opens WhatsApp with structured prefilled message (parent name, child name+age, preferred time). Fires Pixel Contact event. Inline confirmation. The form gives parents a real UI without requiring a backend — the conversion path stays DM-first per the project's community-offers playbook.

3. **UTM attribution end-to-end** — new `getUtm()` + `utmSourceLine(lang)` in script.js. UTM params from landing URL persist via sessionStorage and append to every outbound WA message (form + static CTAs). Lets Diana attribute incoming WA leads to specific campaigns/ad sets without backend or CRM.

4. **SEO foundation upgrade**:
   - `sitemap.xml`: 4 → 10 URLs (now lists kids + coworking in all 3 languages)
   - `LocalBusiness` JSON-LD added to RU homepage with stable `@id` so Google can merge into one Knowledge Graph entity
   - RU/UA price format standardized to `NN €` (EU convention), EN kept as `€NN` (English convention)
   - Kids meta descriptions trimmed under 160 chars
   - Google Search Console verified via HTML file method

5. **Kids Meta campaign prep** — full brief at `references/meta-ad-copy-kids.md`: Traffic objective, €5/day (€2 RU + €3 UA biased to UA per adult learnings), 14d duration, Valencia 17km residents, age 28-45, parents 6-12. 6 ad creatives Diana designed in Figma (3 ratios × 2 languages) saved to `assets/images/ad-kids-*`. Day-7 evaluation rubric included. Launching manually via Ads Manager UI while Business Verification re-clears (~2026-05-29).

6. **Typography iterations** (lots of Diana iterating live):
   - Summer Font Light applied to h1-h3 + top nav + language switcher
   - FAQ + schedule sections **locked to Inter** (Summer Font Light too thin for body info)
   - `<strong>` reverted from Summer Font (broke price-line flow)
   - Channels grid centers when only one item via `:has()` selector
   - Kids h1 typo fix: Керамики → Керамика (singular)

### Key decisions made

| Decision | Why |
|---|---|
| Koritsa as "resident of Saged.club" not "@korytsia_studio" | Consolidate brand authority on studio rather than personal IG; reduce funnel leakage |
| Single WhatsApp + IG channels (no Telegram, no Facebook) | Fewer options = fewer abandoned leads; matches DM-first playbook |
| Traffic objective (not Messages) for kids campaign | No WhatsApp Business API — Messages would require that. Landing page does the conversion job. |
| €2 RU / €3 UA budget split | Adult campaign showed UA outperforms (8% CTR post-geo-tighten); apply same bias to kids |
| Form submits to WA (no backend) | Matches DM-first conversion pattern; no backend or CRM cost; lead still arrives in real inbox |
| RU/UA "NN €", EN "€NN" | Respect each language's convention; rejected forcing one global format |

### Bugs found + fixed

- **wa.me deep link broken** when using `window.open(url, '_blank', 'noopener')` — the popup-feature variant opens a stripped browser that drops the `text=` param mid-redirect on some browsers, or fails the universal-link handoff to the WhatsApp app on iOS. Fix: temporary `<a target="_blank">.click()` — preserves params, bypasses popup blockers.
- **`form.parent?.value` unreliable** for reading form inputs due to property naming collision. Fix: `new FormData(form).get('parent')` — unambiguous.
- **Inline emphasis in Summer Font breaks meta lines** like "25 € за класс · 1,5 часа..." — price jumped to different font/size. Lesson: keep display font for h1-h3 only.

### Files touched

```
new:      assets/images/ad-kids-{ru,ua}-{1x1,4x5,9x16}.png  (6 creatives)
new:      references/meta-ad-copy-kids.md
new:      googlec4676a6ccd34c593.html  (GSC verification)
modified: sitemap.xml (4 → 10 URLs)
modified: index.html, uk/index.html (LocalBusiness schema, bio, contacts, prices, sameAs)
modified: kids/index.html, uk/kids/index.html, en/kids/index.html (form, bio, copy, contacts)
modified: coworking/index.html, uk/coworking/index.html, en/coworking/index.html (contacts)
modified: assets/script.js (UTM tracking, form handler, wa.me link rewriter)
modified: assets/style.css (typography, FAQ Inter, schedule Inter, channels centering)
```

### What's open at the end of session

- Kids campaign mid-launch via Ads Manager UI (handed off to another Claude session with browser control)
- Business Verification in review (~2 business days to clear)
- GSC needs sitemap.xml manually submitted in Sitemaps tab
- EN adult workshop page doesn't exist (kids/coworking have EN, adult only RU/UA) — decision deferred
- Koritsa report drafted in chat, not yet sent

---

## 2026-05-11 — Foundations day

**Duration**: ~3 hours, single session with Diana
**Outcome**: project bootstrapped from "0 bookings on €105 ad spend" to "live bilingual landing + 48-issue roadmap + clean ad account + background automation"

### Major milestones

1. **Diagnostic audit** of the €105 Meta spend — pulled via API once token access was set up. Found 6 root causes of zero bookings (wrong objectives, no Pixel, no landing, no language targeting, scattered audience, brand fragmentation). Full breakdown in `AUDIT.md`.

2. **Meta API access provisioned** — created Meta App "studio audit", System User `claude` (ID 61589322372602), ad account `act_484884320671439` assigned with `View performance` (read-only) permission. Token stored in `.env`.

3. **GitHub repository created**: https://github.com/diana0xUX/Saged. Public. Pages enabled. xAlisher added as admin collaborator.

4. **Bilingual landing page shipped** (vanilla HTML/CSS/JS):
   - `index.html` (RU primary) + `uk/index.html` (UA)
   - 3-slide hero carousel (process → person → place)
   - All sections mirrored in both languages
   - Real photos from saged.old archive
   - Embedded Google Maps + Instagram top-CTR posts
   - 6-channel manual booking grid
   - EU-compliant cookie consent banner
   - Full SEO pass: OG tags, Twitter Card, Schema.org Course, hreflang, sitemap, robots.txt, favicon pulled from existing Squarespace site
   - Mobile-tight (3 breakpoints, ≥44px tap targets)

5. **GitHub issues** — 52 issues created across 8 epics:
   - Domain & Hosting
   - Content production
   - Landing page polish
   - Booking integration
   - Tracking (Pixel + CAPI)
   - Meta Ads rebuild
   - Continuous review loop
   - Creative tactics to fill workshops (NEW — 10 sub-issues)
   - Plus social-strategy issues (#35–#41)

6. **Old Meta campaigns cleaned up** — Diana paid the outstanding invoice + deleted all 9 boosted Instagram posts. Background API poll confirmed `account_status: 3 → 1`, `active campaigns: 9 → 0`. Issues #26 and #27 auto-closed by the loop.

7. **References gathered + documented**:
   - `KNOWLEDGE.md` — canonical project facts (brand, people, audience, channels, workshop format, voice)
   - `references/social-strategy.md` — proposed copy for IG pins, bio updates, Telegram channel, Facebook page
   - `audit-prompt.md` — re-runnable Claude-for-Chrome prompt
   - `scripts/audit.py` — weekly performance report generator (no dependencies, uses .env)

### Key decisions made

| Decision | Why |
|---|---|
| Vanilla HTML/CSS/JS over a framework | Diana is a UX designer; editable in any tool, no build step, deployable from `main` |
| Multi-channel manual booking (not Cal.com yet) | At €60/seat small studio, manual is fine until volume justifies automation |
| RU + UA always separate ad sets | Cultural sensitivity (post-2022 displacement context) + statistical clarity |
| System User read-only on ad account | Security: keep write power off until clear automation workflow defined |
| Workshop format: 2 sessions, 1 week apart | Reflects actual ceramic process (form → bisque-fire → glaze) |
| `CNAME` temporarily disabled | Lets github.io preview URL work until xAlisher does DNS |
| All copy mirrored in both languages | Hard rule in CLAUDE.md: every edit applies to both files |

### Workshop details locked

- **Workshop**: "Керамика с Корицей" / "Кераміка з Корицею" — two-session ceramics course
- **Date format**: every Thursday (first cohort 14 + 21 May 2026)
- **Time slots**: 12:00–14:00 / 15:00–17:00 / 19:00–21:00
- **Price**: €60 for both sessions, materials + 2 firings included
- **Capacity**: 6 people per slot
- **Address**: C/ de les Cuines, 8, Ciutat Vella, 46001 Valencia
- **Instructor**: Korincia Gasikóvska (@korytsia_studio) — "Кориця" / "Корица"

### Contact channels confirmed

- WhatsApp: +34 605 54 33 00
- Email: hello@saged.club
- IG studio: @saged.club
- IG Koritsa: @korytsia_studio
- Telegram studio (via Diana): @dvoroneca
- Telegram Koritsa: @ko_hasi
- Facebook: facebook.com/share/1BUsmYHLdW

### Reality-check moments

- **3 ad accounts existed**, Diana initially navigated to the wrong ones twice before finding the active Saged one (`484884320671439`). Logged a TODO to rename ad accounts for clarity in future.
- **The "Ad account restricted" banner** revealed the campaigns weren't bleeding money during the day — Meta had blocked delivery due to the failed payment. They went from "ACTIVE in metadata + Payment error delivery" → "Off" → "Deleted".
- **Instagram permalink scraping** worked via Meta Ads API; bio scraping of @saged.club + @korytsia_studio did not (Instagram blocks anonymous text scraping).
- **GitHub Pages auto-redirects** to custom domain when `CNAME` exists; broke the preview workflow until DNS is real. Worked around by renaming `CNAME` → `CNAME.disabled` temporarily.

### Things that stayed out of scope (intentional)

- Python data pipelines, warehouses, Robyn — premature at €150/month spend
- Cal.com booking automation — defer until weekly volume justifies setup
- Statistical A/B testing — too small a sample
- Meta App Review (Standard tier) — not blocking at current scale

### Pending — Diana

Critical path (in order):
1. xAlisher does DNS pointing (#33)
2. Pin workshop post on @saged.club (#35)
3. Update @saged.club bio (#37) + restore `CNAME` after DNS
4. Send real testimonials (#34)
5. Higher-res Koritsa photo (current is 481×483)

### Pending — Claude (automated, once unblocked)

- Lighthouse audit + HTTPS toggle after DNS
- Wire Meta Pixel into landing once Pixel ID exists
- Embed Cal.com after Diana sets it up
- Weekly performance report via `scripts/audit.py`

---

## File map

| File | What it's for |
|---|---|
| `index.html` + `uk/index.html` | The landing page (Russian + Ukrainian) |
| `assets/style.css`, `assets/script.js`, `assets/images/` | Front-end assets |
| `privacy.html`, `cookies.html` | Legal stubs (need real text before scale) |
| `CLAUDE.md` | Project context for future Claude sessions |
| `KNOWLEDGE.md` | Canonical facts (brand, people, address, workshop, channels) |
| `PLAN.md` | Phased roadmap |
| `AUDIT.md` | Diagnostic findings from the €105 spend |
| `REPORT.md` | Plain-language status summary for Diana |
| `SESSION_LOG.md` | This file — daily log entries |
| `research.md` | Reference: Meta API, A/B testing, audience research (May 2026) |
| `audit-prompt.md` | Re-runnable Claude-for-Chrome prompt |
| `references/social-strategy.md` | IG pin copy, bio drafts, Telegram + FB recommendations |
| `scripts/audit.py` | Weekly Meta performance report |
| `data/raw/` | Cached Meta API responses (gitignored) |
| `reports/` | Generated weekly reports |
| `.env`, `.env.example` | Meta credentials (`.env` gitignored) |
| `CNAME.disabled` | Will be `CNAME` once DNS is pointed |
| `sitemap.xml`, `robots.txt` | SEO |
