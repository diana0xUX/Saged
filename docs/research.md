# Research Notes — May 2026

Consolidated findings from four parallel research passes. Each section is self-contained; jump to whichever is relevant. All citations linked at the end of each section.

---

## 1. Meta Marketing API — State of the Union

### Version & deprecation cadence
- **Latest stable: Marketing API v25.0** (released Feb 18, 2026). v26.0 expected ~September 2026.
- Meta ships a new version every 4–6 months; each version is supported ~2 years.
- **Key deadlines**:
  - **June 9, 2026** — all versions prior to v24.0 are retired.
  - **May 19, 2026** — creation/update of Advantage+ Shopping (ASC) and Advantage+ App (AAC) campaigns disabled across all versions.
  - **Sept 2026 (v26.0)** — remaining ASC/AAC campaigns auto-paused.
  - **June 2026** — legacy reach/impressions/video-impressions/story-impressions metrics deprecated; replaced by new Page Viewer / media-view metrics.

### Auth
- **System User access tokens** are standard for server-to-server. Generate from Business Manager → Business Settings → System Users.
- Tokens can be made never-expiring when generated correctly (otherwise 60 days).
- **Required scopes**: `ads_management` (write), `ads_read`, `business_management`, plus `pages_read_engagement` / `instagram_basic` / `pages_manage_ads` for asset-tied creatives.
- **App Review** required for Advanced Access — plan 2–4 weeks.
- **Tiers**: Development (300 calls/hour/account) → Standard (100,000 base + 40 × active ads).

### Key endpoints
- **Insights**: `GET /{campaign|adset|ad|act_<id>}/insights` — supports `level`, `breakdowns`, `action_breakdowns`, `time_range`, `time_increment`, attribution windows. 70+ metrics.
- **Hierarchy**: `/act_<id>/campaigns`, `/adsets`, `/ads`, `/adcreatives`.
- **A/B testing**: `POST /act_<id>/ad_studies` (Experiments endpoint — canonical). The older `split_test` field on ad sets is still present but deprecated path.
- **Custom Audiences**: `POST /act_<id>/customaudiences` (CUSTOM, WEBSITE, CUSTOMER_FILE, ENGAGEMENT). Hashed PII uploads via `users` endpoint (SHA-256). Sensitive-category audiences blocked (error 471) since Sept 2025.
- **Lookalikes**: `customaudiences` with `subtype=LOOKALIKE` + `origin_audience_id` + `lookalike_spec`.
- **Audience Insights replacement**: legacy tool sunset 2021. **No direct API replacement.** Substitutes: Meta Foresight (qualitative, no API), Advantage+ Audience for expansion, your own Custom Audience analytics. For programmatic discovery: `targetingsearch`, `targetingsuggestions`, `targetingbrowse`, `reachestimate`, `delivery_estimate`.

### Rate limits
- **Business Use Case (BUC)** model — per ad account per BUC (`ads_management`, `ads_insights`, `custom_audience`). Check `X-Business-Use-Case-Usage` response header.
- **Ads Management**: 100,000 (Standard) or 300 (Dev) + 40 × active ads per hour.
- **Insights async**: `POST /<obj>/insights?async=true` → returns `report_run_id` → poll `async_status`. Required for breakdowns + backfill > 13 months. ~10 async jobs/account/day for expensive queries.
- **Batch**: `POST /` with `batch` array, up to 50 sub-requests. Each still counts for BUC.

### SDKs
- **Python `facebook-business`**: v25.0.0 (Mar 10, 2026). Most active. Version-locked to MAPI.
- **Node `facebook-nodejs-business-sdk`**: tracks MAPI versions; less frequent commits than Python.
- PHP / Java / Ruby SDKs also auto-generated.

### 2026 gotchas
- **iOS ATT** still drives 15–30% pixel signal loss. AEM mandatory for iOS conversion measurement.
- **AEM 8-event cap removed** (June 2025) — all eligible standard/custom events auto-process. Domain verification still required.
- **CAPI no longer optional** — one-click setup (April 2026) lowered the bar. Use `event_id` dedup with Pixel.
- **Privacy Sandbox / Chrome** — cookie deprecation softened but signal degradation continues; EU DMA adds consent friction.
- **Data delays** — insights stabilize over 24–72 hours; don't trust same-day numbers.
- **Webhooks** — Meta CA cert change March 31, 2026; update trust stores.

### Sources
- https://developers.facebook.com/docs/marketing-api/marketing-api-changelog/versions/
- https://developers.facebook.com/docs/marketing-api/overview/versioning/
- https://developers.facebook.com/blog/post/2026/02/18/introducing-graph-api-v25-and-marketing-api-v25/
- https://developers.facebook.com/docs/marketing-api/insights/best-practices/
- https://developers.facebook.com/docs/marketing-api/overview/rate-limiting/
- https://developers.facebook.com/docs/marketing-api/get-started/authentication/
- https://developers.facebook.com/docs/marketing-api/guides/split-testing/
- https://developers.facebook.com/docs/marketing-api/reference/custom-audience/
- https://github.com/facebook/facebook-python-business-sdk
- https://www.facebook.com/business/foresight

---

## 2. Existing automation landscape (build vs buy)

### Commercial all-in-one
| Tool | Strength | Rough price | Main gap |
|---|---|---|---|
| **Smartly.io** | Enterprise dynamic creative at scale | $5k–$10k+/mo | Overkill < $100k/mo spend; weak rules |
| **Madgicx** | "AI Marketer" autonomous mode; cross-account UI | $49–$499/mo | Black-box decisions |
| **Revealbot** | Most flexible rule engine; operator-friendly | $99–$499/mo | Rules-only; no creative/attribution layer |
| **AdEspresso** | Easy A/B + clean reporting | $49+/mo | Stagnant since 2017 Hootsuite acquisition |
| **Triple Whale** | Shopify-native blended ROAS; "Moby" AI | from $129/mo | Shopify-centric |
| **Northbeam** | Sophisticated MTA + MMM + incrementality; new Clicks+Views model (late 2025) | ~$1,000+/mo | Expensive; needs analyst |
| **Motion** | Auto-tags creative elements; visual creative reporting | from $250/mo | Reporting-only, no execution |
| **Pencil** (Brandtech) | End-to-end creative gen with brand-guideline enforcement | Enterprise | Slow onboarding |
| **AdCreative.ai** | Trained on 450M ads; cheap entry | $39–$249/mo | Output quality varies |

### Data connectors
- **Supermetrics** — 176+ connectors, fastest to Sheets/Looker. From €29/mo. SMB.
- **Funnel.io** — 590+ connectors, strong normalization. From ~$400/mo.
- **Fivetran** — 600+ connectors, generic ELT. From $500/mo.
- **Improvado** — 500+ connectors, enterprise marketing ops.
- **Windsor.ai** — 325+ connectors, all tiers, free tier. Acquired by team.blue Jan 2026.

All read-only. None *write back* to Meta.

### Meta's native automation (don't rebuild)
- **Advantage+ Shopping / App** — API creation/update **disabled May 19, 2026**.
- **Advantage+ Audience** — only min age + location are hard constraints.
- **Enhanced Automated Rules** — factor in Meta's predicted outcomes.
- **Experiments tool** — A/B, holdout, brand lift, conversion lift. Solid.
- **REA (Ranking Engineer Agent)** — autonomous ML improving auction ranking (March 2026).

### Open source
- `facebook/facebook-python-business-sdk` — v25.0.1 (Mar 2026). Canonical.
- `facebook/facebook-nodejs-business-sdk` — active.
- `pipeboard-co/meta-ads-mcp` — MCP server exposing Meta Ads to LLM agents.
- `gomarble-ai/facebook-ads-mcp-server` — alternative.
- **No mature open-source "platform"** exists. Greenfield.

### AI tools — real vs hype
- **Real**: Motion's creative element auto-tagging; Triple Whale Moby (NL analytics); Northbeam's clicks+views.
- **Mixed**: AdCreative.ai / Pencil / Omneky — speed up generation; quality inconsistent.
- **Hype**: most "AI Marketer" autonomous-mode claims are LLM-wrapped rule engines.

### Build-vs-buy verdict
**Don't rebuild**: Advantage+, Meta Experiments, the SDKs, basic data extraction.
**Buy/integrate**: Motion ($250/mo) for creative analytics; Windsor.ai/Supermetrics for cheap reads; Triple Whale only if Shopify DTC.
**Custom system adds value in**:
1. Decision layer over warehouse data (Revealbot-killer)
2. Cross-account portfolio logic
3. Custom attribution opinion
4. Creative-tagging → brief-generation feedback loop
5. MCP-style agent control with audit trails

**Practical stack**: `facebook-business` SDK (writes) + Windsor/Supermetrics (reads) + your own rules/LLM layer + Motion (creative) — or build creative tagging with vision LLMs.

### Sources
- https://adlibrary.com/posts/facebook-ads-automation-platforms-reviewed-2026
- https://www.adstellar.ai/blog/best-facebook-ad-automation-platforms
- https://segwise.ai/blog/top-10-ai-tools-meta-ads-management-2026
- https://www.triplewhale.com/blog/triple-whale-vs-northbeam
- https://windsor.ai/supermetrics-vs-funnel-io-vs-windsor-ai-vs-fivetran-vs-improvado/
- https://www.facebook.com/business/ads/meta-advantage/advantage-plus-shopping-ads
- https://alexneiman.com/ai-agents-meta-ads-manager/
- https://github.com/facebook/facebook-python-business-sdk
- https://github.com/pipeboard-co/meta-ads-mcp
- https://motionapp.com/

---

## 3. A/B testing & experimentation

### Meta Experiments tool
- Available in Ads Manager + dedicated Experiments tool.
- Tests up to **5 variants** of: creative, audience, placement, delivery optimization, bidding, custom audience, or whole-campaign strategy.
- Traffic split by **user** (not impression) — Meta deduplicates users across cells, eliminating overlap bias.
- Recommended **5–7 day minimum** to clear learning phase. Auto-computes ~95% confidence reading.
- Marketing API access: `adstudy` and `adstudy_objective` endpoints. `SPLIT_TEST` for A/B, `LIFT` for Conversion Lift.

### Statistical foundations
- **Frequentist** (p-value, power, MDE): defensible, requires pre-committed sample size. Peeking inflates false positives.
- **Bayesian** (posterior P(B>A)): supports continuous monitoring, intuitive for marketers, works with small samples.
- **Sequential testing** (mSPRT, always-valid p-values — Optimizely/Eppo style): increasingly default; lets you stop early without false-positive inflation.
- Typical e-com CVR 1–3% with 10% relative MDE @ 80% power → ~30k–100k users/arm.
- Pitfalls: peeking, novelty/primacy effects, attribution-window mismatch (Meta 7d-click vs your warehouse), Simpson's paradox across placements, learning-phase contamination.

### Incrementality / lift
- A/B tests compare variants of ads that all run; can't measure ad cannibalization of organic.
- **Meta Conversion Lift**: user-level RCT with PSA/ghost-ad holdout. Typically requires **$50k+ over 2–4 weeks** and high conversion volume.
- **GeoLift** (Meta open-source, synthetic-control): market-level holdout, no min-spend gate, ~4 weeks on 3–5 matched DMAs.
- Use lift tests for **whether to spend at all**; A/B for **how to spend within**.

### MMM renaissance
- Post-ATT signal loss revived MMM.
- **Meta Robyn** (R + Python; ridge regression + Nevergrad; adstock + saturation; budget allocator) — open-source standard.
- **Google LightweightMMM / Meridian** — alternatives.
- Modern stack = "triangulation": MMM for strategic allocation, lift to calibrate MMM coefficients, A/B for tactical execution.

### Practical automation
- Min duration **7 days** (covers weekly seasonality + learning phase); 14 days preferred.
- Stopping rule: precommit either sample size (frequentist) or posterior threshold (e.g., P(B>A) > 95% AND expected loss < ε).
- **Multi-armed bandits** (Thompson sampling, ε-greedy) for creative rotation when you don't need a clean causal estimate. Meta's Advantage+ uses bandit logic internally. Typical hybrid: 20% explore / 80% exploit.
- Creative fatigue: retire ads at frequency ~2.5–3 in a 7-day window.

### Tooling
- **General experiment platforms**: GrowthBook (OSS, CUPED, sequential, Bayesian + frequentist), Statsig (OpenAI-owned), Eppo (sequential focus).
- **Ad-specific incrementality**: Haus, Measured, INCRMNTAL, Triple Whale, Northbeam, Cometly.
- **Open source**: Robyn (MMM), GeoLift (geo experiments), Meridian (Google MMM), CausalImpact.
- For in-house: Bayesian beta-binomial over warehouse data is sufficient for A/B; reserve GeoLift/Robyn for incrementality + allocation.

### Sources
- https://www.facebook.com/business/help/1738164643098669
- https://www.facebook.com/business/measurement/ab-testing
- https://extuitive.com/articles/a-b-testing-meta-ads
- https://www.triplewhale.com/blog/meta-conversion-lift-test
- https://www.triplewhale.com/blog/geolift-geo-based-incrementality-testing
- https://facebookincubator.github.io/GeoLift/docs/Methodology/
- https://www.haus.io/article/meta-incrementality-testing
- https://www.geteppo.com/blog/comparing-frequentist-vs-bayesian-approaches
- https://github.com/facebookexperimental/Robyn
- https://research.facebook.com/blog/2021/4/auto-placement-of-ad-campaigns-using-multi-armed-bandits/
- https://www.growthbook.io/compare/growthbook-vs-statsig
- https://www.statsig.com/experimentation

---

## 4. Audience research approaches

### Meta Audience Insights status
- Audience Insights **deprecated July 2021** → folded into Meta Business Suite Insights + Ads Manager reporting (shallower).
- **January 15, 2026**: Meta removed dozens of detailed targeting interest categories — granular interest stacking is largely dead for most advertisers.
- Marketing API still exposes: age/gender/geo breakdowns, life events, broad interest forecasts (audience-size estimates), behaviors, owned-audience metrics.
- Treat Meta-native research as a *validation* layer, not discovery.

### First-party data post-ATT
- ATT cut pixel-measurable events 15–30%.
- Still effective:
  - **Customer-list Custom Audiences** (hashed email/phone) — unaffected by ATT.
  - **Website Custom Audiences** via Pixel + CAPI (CAPI essential).
  - **Engagement Custom Audiences** (video viewers, FB/IG engagers, lead-form openers).
  - **Lookalikes** still work; testing 3–5% LAL (vs 1%) is now standard.

### Advantage+ Audience
- Meta's AI replacement for manual targeting.
- You provide a *suggestion* (custom audience, interest, demo); AI expands using pixel/CAPI signals, creative engagement, on-platform behavior, similar-advertiser patterns.
- **Hard constraints**: min age, location, language, custom-audience exclusions. Everything else is a hint.
- Requires ~**50 conversions/week** for stable learning.
- **Creative is now the primary targeting lever.**

### Conversions API (CAPI)
- Essentially mandatory in 2026.
- Browser pixel alone misses >50% of conversions (ATT + ad blockers + ITP + consent walls).
- Send server-side: Purchase, AddToCart, InitiateCheckout, Lead, CompleteRegistration + offline + CRM-stage events.
- **Dedup**: Pixel `eventID` = CAPI `event_id`; Meta dedupes pairs within 48h.
- Keep Pixel running alongside CAPI — Pixel provides pre-conversion behavioral context.
- One-click setup (April 2026) handles standard web events; custom/offline/multi-platform still need custom work.

### Third-party enrichment
- **SparkToro** — where audiences actually consume content (sites, podcasts, accounts, hashtags). Channel discovery + seed-interest validation.
- **Similarweb** — competitive digital traffic, audience overlap, referral patterns.
- **Brandwatch / Sprinklr Insights / Pulsar** — enterprise social listening, historical depth, sentiment.
- **GWI / YouGov Profiles / Audiense** — psychographics SparkToro lacks.
- **TikTok Research API** + 2026 Creator Search Insights API — creator-level demos, hashtag breakdowns, growth velocity (academic/approved use).
- **Reddit public API** — free social listening for subreddit/topic affinity.

Pattern: enrich outside Meta → hash & upload as Custom Audience seed → let Advantage+ expand.

### Privacy / regulatory
- **GDPR (EU)** — opt-in consent before any pixel/CAPI fire; document lawful basis; honor data-subject rights.
- **DSA (EU)** — ad-transparency obligations; one-click opt-out from personalized ads; no profiling minors.
- **DMA / Meta-specific (Jan 2026)** — EU users can choose "less personalized ads"; replaces prior consent-or-pay model. Expect partially degraded EU conversion signals.
- **CCPA/CPRA (Jan 1, 2026)** — mandatory GPC signal honoring; visible opt-out confirmations; bans on dark-pattern consent UIs.
- **ATT (Apple)** — iOS users who decline tracking generate aggregated/modeled conversions only; SKAdNetwork/AEM limits depth.

**Operational rules**: gate every event on region-specific consent state; store only hashed PII (SHA-256); respect GPC/DNT; deletion pipeline; never log raw third-party PII; document lawful basis per source.

### Sources
- https://www.facebook.com/business/help/531965364451139
- https://www.jonloomer.com/yes-facebook-audience-insights-still-exists/
- https://www.metacto.com/blogs/facebook-analytics-competitors-the-ultimate-guide-to-the-top-alternatives
- https://www.facebook.com/business/help/273363992030035
- https://alexneiman.com/meta-advantage-plus-audience-targeting-2026/
- https://adligator.com/blog/meta-broad-targeting-advantage-plus-audiences-2026
- https://www.admove.ai/blog/meta-capi-guide
- https://blog.funnelfox.com/meta-pixel-and-conversions-api/
- https://www.triplewhale.com/blog/facebook-capi
- https://www.upstackdata.com/blog/facebook-custom-audiences-without-third-party-cookies
- https://sparktoro.com/
- https://www.brandwatch.com/blog/social-listening-tools/
- https://developers.tiktok.com/products/research-api/
- https://www.techradar.com/pro/meta-promises-to-reduce-data-sharing-for-eu-users-by-2026-to-avoid-eu-gdpr-fines
- https://usercentrics.com/knowledge-hub/gdpr-vs-ccpa-compliance/
