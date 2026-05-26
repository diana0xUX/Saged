# Halt — 2026-05-27 (Kids campaign launch in progress)

## Where we stopped

End of a long session (2026-05-26 → 2026-05-27, ~30+ commits). Two big tracks completed in parallel: (a) a deep site polish + brand repositioning of Koritsa from "her own studio @korytsia_studio" → "ceramic resident of @saged.club", and (b) full prep of the **kids trial class Meta campaign** — copy, creatives, audience spec, UTM attribution, launch checklist. Diana is mid-launch through Ads Manager UI (manual path, because Business Verification is in review again — submitted additional docs 2026-05-26, ~2 business days to clear). Campaign is at the campaign-setup screen of the Ads Manager wizard — name `Saged - Kids Trial Class - 2026-05`, Traffic objective, Ad set budget mode. Diana asked another Claude (Sonnet 4.6 with browser control) to finish the click-through from `references/meta-ad-copy-kids.md`.

## Current state (2026-05-27)

- **Branch**: `main`, last commit `8380f91` (UTM attribution on WhatsApp messages)
- **Adult campaign**: 🟢 still active (€147.58 spent, 51,556 impressions, 13,373 reach in last 30d per Ads Manager view)
- **Kids campaign**: 🟡 mid-launch via Ads Manager UI, Diana clicking through
- **Business Verification**: 🟡 in review — additional docs submitted 2026-05-26, ~2 business days (~2026-05-29)
- **Google Search Console**: ✅ verified (HTML file method, `googlec4676a6ccd34c593.html` at root)
- **Site state**: significantly polished — see Chronicle for detailed change log

## What shipped this session

### Brand repositioning
- Koritsa now described site-wide as **"keramic resident of Saged.club"** (not "her own studio @korytsia_studio")
- Contact channels simplified to **WhatsApp + Instagram @saged.club only** — removed @ko_hasi, @dvoroneca, @korytsia_studio, Facebook
- Schema.org `instructor.sameAs` updated to `@saged.club` (was @korytsia_studio) — fixes branding leak in Google Knowledge Graph

### Parent+kid request form
- Inline HTML form on all 3 kids pages (RU/UA/EN) → opens WhatsApp with structured prefilled message
- 3 fields: parent name, child name+age, preferred time
- Fires `Contact` Pixel event on submit
- Inline confirmation message (works even if popup blocker fires)
- Bug fix: changed `window.open(url, '_blank', 'noopener')` → temp `<a>.click()` (the noopener-feature variant was dropping the `text=` param mid-redirect on some browsers)

### UTM attribution on all outbound WhatsApp
- New `getUtm()` + `utmSourceLine(lang)` in `assets/script.js`
- Captures `utm_source/medium/campaign/content` on landing, stores in sessionStorage
- Appends localized source line ("— Источник: meta / kids-trial / ru") to BOTH the form submission AND every static wa.me link on the page
- Organic visits (no UTM) get no source line — clean

### SEO + schema
- `sitemap.xml` rebuilt: 4 URLs → 10 URLs (adds /kids/, /uk/kids/, /en/kids/, /coworking/, /uk/coworking/, /en/coworking/); each page-group declares full hreflang inline
- `LocalBusiness` JSON-LD added to RU homepage with `@id "https://saged.club/#localbusiness"` (stable Knowledge Graph anchor)
- Includes: full PostalAddress, telephone +34605543300, email, sameAs IG, priceRange €€, knowsLanguage ru/uk/en/es
- Price format standardized across RU/UA pages: `NN €` (EU convention) — fixed where meta had `€NN` while body had `60 €`
- Kids meta descriptions trimmed under 160 chars (was 162-164)

### Typography iterations (lots — Diana iterated live)
- Summer Font Light applied to h1/h2/h3 globally
- Top nav at 1.6rem Summer Font Light
- Language switcher restyled to match nav (terracotta underline for current, dropped button-block bg)
- Schedule + FAQ sections **locked to Inter** for legibility (Summer Font Light too thin for body-style info)
- `.three h3` (subhead labels) → Summer Font (was Inter bold caps)
- `<strong>/<b>` reverted to body Inter (Summer Font on inline emphasis broke "25 € за класс" line flow)
- Channels grid centers when only one item left (`.channels:has(.channel:only-child)`)
- Kids h1 typo fix: Керамики → Керамика (singular, mirrors adult page)

### Kids Meta campaign — fully prepped
- Brief at `references/meta-ad-copy-kids.md` — campaign settings, audience spec, copy, UTM scheme, Day-7 evaluation rubric, launch checklist
- 6 ad creatives saved: `assets/images/ad-kids-{ru,ua}-{1x1,4x5,9x16}.png` (Diana designed all in Figma)
- Configuration: Traffic objective, €5/day (€2 RU + €3 UA — biased to UA per adult campaign learning), 14d duration, Valencia 17km residents, age 28-45, parents 6-12

### Google Search Console
- Verified via HTML file method (`googlec4676a6ccd34c593.html`)
- Diana to submit `sitemap.xml` next time she opens GSC

## Next steps (in order)

1. **Diana finishes the kids campaign launch** in Ads Manager UI (in progress — handed off to another Claude session). Stuck at campaign-setup screen; remaining work documented in `references/meta-ad-copy-kids.md`.
2. **Submit `sitemap.xml`** in GSC → Sitemaps tab (one-line input, hit Submit)
3. **Day 7 of kids campaign** — read the data, decide if budget split is right or rebalance
4. **Business Verification clearance** (~2026-05-29) — unlocks API write ops again. Plan A: nothing changes, the manual UI campaign continues running. Plan B: re-prep WhatsApp Business API workflow once available.
5. **Koritsa report** — drafted in chat, not yet sent. Diana can copy from session transcript or ask me to save to `reports/koritsa-2026-05-27.md`
6. **Open SEO finding still open**: no EN adult workshop page. EN traffic landing on `/en/` (kids/coworking only) has no main product. Decision when ready.

## Blockers

- **Business Verification in review** — blocks API-driven campaign creation. Workaround: manual UI launch (in progress).
- **WhatsApp Business API not set up** — chose Traffic objective for kids campaign instead of Messages (Messages requires WA Business API). Acceptable trade-off; landing page does the conversion job.

## Context hard to re-derive

- **The wa.me deep link bug**: `window.open(url, '_blank', 'noopener')` works on desktop but on mobile (iOS especially) opens a stripped popup that drops the `text=` param during the wa.me → web.whatsapp.com redirect, OR fails to trigger the universal-link handoff to the WhatsApp app. The fix: temporary `<a target="_blank">.click()` — preserves params, triggers universal-link, bypasses popup blockers. Document this pattern for any future wa.me work.
- **`form.parent?.value` is unreliable for reading form inputs**. `parent` collides with browser-context properties in some envs. Use `new FormData(form).get('parent')` instead — unambiguous, FormData is the canonical pattern.
- **Summer Font Light glyph gaps**: missing uppercase Ukrainian `І` (U+0406), `Ґ`/`ґ`. Diana avoided this by sentence-casing UA headers instead of uppercase. The Cormorant Garamond fallback chain handles missing glyphs gracefully.
- **`<strong>` in Summer Font breaks meta lines**: Diana noticed "25 € за класс · 1,5 часа..." had the price jumping into a different font/size. Lesson: keep display font for h1-h3 only, not inline emphasis. Body emphasis stays in Inter.
- **GSC verification file is dead simple to create**: filename is `google<HASH>.html`, content is one line `google-site-verification: google<HASH>.html`. No need to download from GSC — create directly with Write tool.
- **`:has()` CSS selector**: used for FAQ-h2 → Inter (`section:has(.faq) h2`) and 1-item channels centering. Supported in all modern browsers (Safari 15.4+, Chrome 105+).
- **UTM attribution architecture**: every wa.me link on the page gets dynamically rewritten with the source line at JS load — no per-link href changes needed in HTML. Means future wa.me links work automatically.

## Open issues snapshot

- 🟢 **Live**: adult campaign (4th week)
- 🟡 **Mid-launch**: kids campaign — Diana clicking through Ads Manager
- 🟡 **Awaiting**: Business Verification, then GSC sitemap submit
- 🔴 **Decision queue**: EN adult page (yes/no), Koritsa report (send/save), Day-7 kids campaign decision

## Files added/touched this session

```
new:    assets/images/ad-kids-{ru,ua}-{1x1,4x5,9x16}.png  (6 creatives)
new:    references/meta-ad-copy-kids.md
new:    googlec4676a6ccd34c593.html  (GSC verification)
modified: sitemap.xml (4 → 10 URLs)
modified: index.html, uk/index.html (LocalBusiness schema, bio, contacts, prices, sameAs)
modified: kids/index.html, uk/kids/index.html, en/kids/index.html (form, bio, copy, contacts)
modified: coworking/index.html, uk/coworking/index.html, en/coworking/index.html (contacts)
modified: assets/script.js (UTM tracking, form handler, wa.me link rewriter)
modified: assets/style.css (typography, FAQ Inter, schedule Inter, channels centering)
```
