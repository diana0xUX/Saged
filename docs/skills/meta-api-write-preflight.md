# Skill — Meta Marketing API write pre-flight

_Last used: 2026-05-28 (kids campaign launch). Saved 3 round-trips by reading existing state._

## Problem

The Meta Marketing API moves underneath you. Across the last 6 months on this project, every write attempt has hit at least one of:

- A newly required field (e.g., `is_adset_budget_sharing_enabled`, error 4834011)
- A newly deprecated field (e.g., `degrees_of_freedom_spec.standard_enhancements`, error 3858504)
- A coupling rule that's not in the official docs (e.g., `advantage_audience: 1` requires `age_min ≤ 25`, error 1870188)
- Edit locks after publish (campaign objective, ad set optimization, ad creative — KNOWLEDGE.md § Edit locks)
- Wrong enum IDs propagated from memory (locales `5/120` instead of `17/52`)
- Stale ACTIVE campaigns past `stop_time` still bleeding budget

Each landmine produces a failed POST. Multi-step builds (campaign → ad sets → ads) leave orphan state on failure.

## Recipe

Run this checklist before writing any new campaign / ad set / ad / creative.

**1. GET a reference object of the same kind.**
```bash
source .env
# Pick a recent working ad set as reference
curl -s "https://graph.facebook.com/${META_API_VERSION}/${REF_ADSET_ID}?fields=name,targeting,promoted_object,destination_type,optimization_goal,billing_event,bid_strategy,daily_budget,start_time,end_time&access_token=${META_ACCESS_TOKEN}" | python3 -m json.tool
```
Diff the response against your intended payload. Newly required fields appear here. Deprecated fields don't. This catches 2 of the 3 landmines above for free.

**2. Verify every enum ID against the live API.**
```bash
# Locales
curl -s "https://graph.facebook.com/${META_API_VERSION}/search?type=adlocale&q=russian&access_token=${META_ACCESS_TOKEN}"
# Interests / family statuses / behaviours
curl -s "https://graph.facebook.com/${META_API_VERSION}/search?type=adinterest&q=pottery&access_token=${META_ACCESS_TOKEN}"
```
Never trust enum IDs from memory or older docs. Past-session "5 for Russian" was wrong; live API says `17`. Verification cost: 1 round-trip per language.

**3. Audit account clean state.**
```bash
curl -s "https://graph.facebook.com/${META_API_VERSION}/${META_AD_ACCOUNT_ID}/campaigns?fields=name,effective_status,stop_time&limit=50&access_token=${META_ACCESS_TOKEN}" | python3 -m json.tool
```
Pause any campaign that is `effective_status: ACTIVE` past `stop_time`, plus any malformed quick-create (Spain-wide geo, no language, zero ads). Today three campaigns needed this; 5 seconds total.

**4. Check existing entity for known edit locks** (KNOWLEDGE.md § Edit locks).
- Campaign objective locked once any ad set exists → rebuild campaign, don't try to PATCH
- Ad set optimization locked after first publish → create new ad set, leave old PAUSED
- Ad creative locked on published ad → create new ad

**5. Dry-run the write script** (see [`idempotent-build-script.md`](idempotent-build-script.md)) before the real run. Print URLs + payloads; verify visually.

## Anti-patterns

- Trusting your mental model of "I've done this before" — Meta v25.0 still ships breaking changes mid-version
- Copying the entire `targeting` object from a reference and changing one field — Advantage+ Audience and Advantage+ Placements are independent toggles; treat each as a separate decision
- Skipping the GET because "the docs say what fields to send" — the docs are 6 months behind production
