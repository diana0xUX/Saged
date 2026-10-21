# Skill — Meta geo city key verification

_Last used: 2026-07-25 (added verify_city_key() to build-meta-campaign.sh after geo incident)._

## Problem

Meta city keys are opaque integers — `699854` looks like "Valencia" because a comment says so, but the API is the only authority. On 2026-07-20, all 7 active ad sets were built with key `668776`, which the API resolves to **Shubra Tana, Egypt**. €95.46 spent, 0 possible bookings. Combined with the locale incident (€141.89), total wasted to targeting ID bugs: **€237.35**.

Same failure mode as the locale incident: the ID came from memory / an older run, nobody verified it against the live API.

## Recipe

**Always verify at runtime — never trust a hardcoded key.**

```bash
source .env
curl -s "https://graph.facebook.com/${META_API_VERSION}/search?type=adgeolocation&q=Valencia&location_types=%5B%22city%22%5D&access_token=${META_ACCESS_TOKEN}" | python3 -m json.tool
```

Confirm the result includes `"name": "Valencia"` and `"country_code": "ES"` before using that `key` value.

## Reference implementation

`scripts/local/build-meta-campaign.sh` → `verify_city_key()` function. Called as:

```bash
verify_city_key "Valencia" "ES" "$VALENCIA_KEY"
```

The function exits non-zero if the API returns a different key or a different country — same pattern as `verify_locale()`. The script refuses to build any ad sets until both locale and city key checks pass.

## Anti-patterns

- Using a key from a previous session's output, a comment, or this file — they all rot
- Verifying the city name but not the country code — `Valencia, VE` (Venezuela) is a different city
- Skipping verification because "we just ran this last week" — Meta can reassign or deprecate keys

## Canonical IDs as of 2026-07-25

| City | Country | Key |
|------|---------|-----|
| Valencia | ES | 699854 |

**Do not trust this table.** Verify via API before every campaign build.
