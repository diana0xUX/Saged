# Skill — Idempotent multi-step build script

_Last used: 2026-05-28 (`scripts/launch-kids-campaign.py`)._

## Problem

Building a hierarchical resource via API — campaign → ad sets → ads → creatives, or any similar fan-out — has three failure modes:

1. **Mid-build failure**: any one POST fails after parents were already created → orphan empty entities accumulate
2. **Accidental double-run**: re-running the script after a successful build creates duplicates that bleed budget
3. **Tactile-pattern errors**: typos in payloads only surface when the live API rejects them, after partial state has been written

Solution: bake idempotency + dry-run + clear failure recovery into the script's spine.

## Recipe

**Spine of the script:**

```python
ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
IDS_PATH = ROOT / ".campaign-ids"   # gitignored persistent state

def main():
    args = parse_args()              # --dry-run flag
    env = load_env()                 # parse .env (stdlib only)
    existing = load_campaign_ids()   # parse .campaign-ids

    # Idempotency gate — refuse if already built
    if "KIDS_CAMPAIGN_ID" in existing and not args.dry_run:
        sys.stderr.write(f"Refusing: KIDS_CAMPAIGN_ID={existing['KIDS_CAMPAIGN_ID']} already set.\n")
        return 2

    # Validate inputs (images exist, copy is non-empty, etc.) BEFORE first POST
    for spec in AD_SETS.values():
        if not spec["image_path"].exists():
            sys.stderr.write(f"Missing: {spec['image_path']}\n")
            return 3

    # Build top-down, persist IDs at end
    new_ids = {}
    campaign_id = create_campaign(...)
    new_ids["KIDS_CAMPAIGN_ID"] = campaign_id
    for lang, spec in AD_SETS.items():
        adset_id = create_ad_set(...)
        image_hash = upload_image(...)
        creative_id = create_creative(...)
        ad_id = create_ad(...)
        new_ids[f"KIDS_{lang.upper()}_ADSET_ID"] = adset_id
        # ...

    if not args.dry_run:
        append_campaign_ids(new_ids)   # all-or-nothing persist
    return 0
```

**Dry-run mode** (the cheapest insurance):

```python
def api_post(url, payload, token, dry_run):
    if dry_run:
        print(f"[DRY] POST {url}")
        print(f"      payload: {json.dumps(payload, ensure_ascii=False)[:500]}")
        return {"id": f"DRY_{uuid.uuid4().hex[:12]}"}  # fake ID so downstream steps render
    # ...real POST
```

The fake DRY ID lets downstream calls render their payloads with real-looking parent IDs. Today's dry-run caught a `act_act_484884320671439` double-prefix bug in 12 seconds.

**Recovery from partial state** (when the dry-run misses something):

If a real run fails mid-build, the higher levels exist but the children don't. Recovery:

```bash
# Pause + delete the orphan campaign (safe only if it has no ad sets yet)
curl -s -X POST "${URL}/${PARTIAL_ID}" -d "status=PAUSED&access_token=${TOKEN}"
curl -s -X DELETE "${URL}/${PARTIAL_ID}?access_token=${TOKEN}"
# Both return {"success":true}. Re-run script.
```

If the orphan has children (ad sets with no ads), use **pause-only**, not delete — per the project rule "pause is safer than delete." Diana sees the noise in Ads Manager; minor cost.

## Anti-patterns

- Persisting IDs incrementally to `.campaign-ids` — feels safer but makes the idempotency gate ambiguous (was the previous run complete or partial?). Persist once at the end.
- Skipping dry-run on the "small fix" — every Meta API change ships at least one surprise per quarter
- Stdlib + urllib feels primitive but is the right call: zero deps, runs on any GitHub Actions runner without `pip install`. Match `scripts/audit-daily.py` style.
