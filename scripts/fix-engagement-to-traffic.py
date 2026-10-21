#!/usr/bin/env python3
"""
fix-engagement-to-traffic.py

Pauses the OUTCOME_ENGAGEMENT handpan + art-classes campaigns
launched 2026-10-20, then rebuilds them as OUTCOME_TRAFFIC.

Existing campaigns are PAUSED (not deleted — spend history preserved).
New campaigns created PAUSED — Diana activates.

Campaigns fixed:
  Saged · Handpan School · RU · music · claude · 2026-10-20
    120250085902350513  →  ENGAGEMENT  (wrong)
  Saged · Art Classes · RU+UA · art · claude · 2026-10-20
    120250085874070513  →  ENGAGEMENT  (wrong)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

# ── Credentials ───────────────────────────────────────────────────────────────
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
env: dict[str, str] = {}
for line in ENV_FILE.read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()

TOKEN      = env["META_ACCESS_TOKEN"]
AD_ACCOUNT = env["META_AD_ACCOUNT_ID"]
API_V      = env["META_API_VERSION"]
BASE       = f"https://graph.facebook.com/{API_V}"
PARAMS     = {"access_token": TOKEN}
PAGE_ID    = "373458682506494"
IG_ACTOR   = "17841428554040839"

VALENCIA_KEY = 699854
RU_LOCALE    = 17
UA_LOCALE    = 52

# IDs to pause
OLD_HANDPAN_CAMPAIGN  = "120250085902350513"
OLD_ARTCLASS_CAMPAIGN = "120250085874070513"


def api_get(path: str, params: dict | None = None) -> dict:
    r = requests.get(f"{BASE}{path}", params={**PARAMS, **(params or {})})
    if not r.ok:
        print(f"  GET {path} FAILED: {r.text[:400]}")
        r.raise_for_status()
    return r.json()


def api_post(path: str, data: dict) -> dict:
    r = requests.post(f"{BASE}{path}", params=PARAMS, json=data)
    if not r.ok:
        print(f"  POST {path} FAILED: {r.text[:600]}")
        r.raise_for_status()
    return r.json()


def api_patch(object_id: str, data: dict) -> dict:
    r = requests.post(f"{BASE}/{object_id}", params=PARAMS, json=data)
    if not r.ok:
        print(f"  PATCH {object_id} FAILED: {r.text[:400]}")
        r.raise_for_status()
    return r.json()


def verify_locale(name: str, expected_id: int) -> int:
    res = api_get("/search", {"type": "adlocale", "q": name, "limit": 5})
    found = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == name), None)
    assert found == expected_id, f"{name} locale ID is {found}, expected {expected_id} — STOP"
    return found


def verify_city(name: str, expected_key: int) -> int:
    res = api_get("/search", {"type": "adgeolocation", "q": name, "location_types": '["city"]', "limit": 5})
    found = next((int(x["key"]) for x in res.get("data", []) if "Valencia" in x.get("name", "") and x.get("country_code") == "ES"), None)
    assert found == expected_key, f"Valencia city key is {found}, expected {expected_key} — STOP"
    return found


def get_creative_ids(campaign_id: str) -> list[tuple[str, str]]:
    """Return [(ad_name, creative_id), ...] for all ads in a campaign."""
    res = api_get(f"/{campaign_id}/ads", {"fields": "id,name,creative{id}", "limit": 50})
    out = []
    for ad in res.get("data", []):
        cid = (ad.get("creative") or {}).get("id")
        if cid:
            out.append((ad["name"], cid))
    return out


def targeting(locale_id: int) -> dict:
    return {
        "geo_locations": {
            "cities": [{"key": VALENCIA_KEY, "radius": 17, "distance_unit": "kilometer"}],
            "location_types": ["home"],
        },
        "locales": [locale_id],
        "age_min": 20,
        "age_max": 54,
        "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
        "targeting_automation": {"advantage_audience": 0},
    }


def main() -> None:
    today = "2026-10-21"

    # 1. Token
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid — STOP"
    print("   ✓ Token valid")

    # 2. Locales + city
    print("2. Verifying locale and city IDs at runtime...")
    ru = verify_locale("Russian", RU_LOCALE)
    ua = verify_locale("Ukrainian", UA_LOCALE)
    valencia = verify_city("Valencia", VALENCIA_KEY)
    print(f"   ✓ Russian={ru}  Ukrainian={ua}  Valencia city={valencia}")

    # 3. Fetch existing creatives before pausing
    print("3. Reading existing creatives from ENGAGEMENT campaigns...")
    handpan_creatives  = get_creative_ids(OLD_HANDPAN_CAMPAIGN)
    artclass_creatives = get_creative_ids(OLD_ARTCLASS_CAMPAIGN)
    print(f"   Handpan creatives:  {handpan_creatives}")
    print(f"   Art class creatives: {artclass_creatives}")
    assert handpan_creatives,  "No ads found in handpan campaign — STOP"
    assert artclass_creatives, "No ads found in art classes campaign — STOP"

    # 4. Pause old campaigns (already done on first run — confirm status)
    print("4. Confirming old ENGAGEMENT campaigns are paused...")
    for cid, label in [(OLD_HANDPAN_CAMPAIGN, "Handpan"), (OLD_ARTCLASS_CAMPAIGN, "Art Classes")]:
        r = api_get(f"/{cid}", {"fields": "status,effective_status"})
        status = r.get("status", "?")
        if status != "PAUSED":
            api_patch(cid, {"status": "PAUSED"})
            print(f"   ✓ {label} {cid} → PAUSED now")
        else:
            print(f"   ✓ {label} {cid} already PAUSED")

    # ── Handpan School rebuild ─────────────────────────────────────────────────
    # Campaign already created on previous run — reuse it
    hp_campaign_id = "120250108388860513"
    print(f"\n5. Rebuilding Handpan School as OUTCOME_TRAFFIC (reusing campaign {hp_campaign_id})...")

    # Creative has both WA + IG CTAs (asset_feed_spec) — needs MESSAGING_INSTAGRAM_DIRECT_WHATSAPP
    hp_adset = api_post(f"/{AD_ACCOUNT}/adsets", {
        "name":              f"Handpan School · RU · Valencia 17km · traffic · {today}",
        "campaign_id":       hp_campaign_id,
        "status":            "PAUSED",
        "billing_event":     "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy":      "LOWEST_COST_WITHOUT_CAP",
        "destination_type":  "MESSAGING_INSTAGRAM_DIRECT_WHATSAPP",
        "daily_budget":      300,
        "targeting":         targeting(RU_LOCALE),
        "promoted_object":   {"page_id": PAGE_ID},
    })
    hp_adset_id = hp_adset["id"]
    print(f"   ✓ Ad set: {hp_adset_id}")

    for ad_name, creative_id in handpan_creatives:
        ad = api_post(f"/{AD_ACCOUNT}/ads", {
            "name":     ad_name.replace("claude", "traffic"),
            "adset_id": hp_adset_id,
            "creative": {"creative_id": creative_id},
            "status":   "PAUSED",
        })
        print(f"   ✓ Ad: {ad['id']}  (creative {creative_id})")
        time.sleep(0.3)

    # ── Art Classes rebuild ────────────────────────────────────────────────────
    print("\n6. Rebuilding Art Classes as OUTCOME_TRAFFIC...")
    ac_campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name":     f"Saged · Art Classes · RU+UA · traffic · {today}",
        "objective": "OUTCOME_TRAFFIC",
        "status":    "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    })
    ac_campaign_id = ac_campaign["id"]
    print(f"   ✓ Campaign: {ac_campaign_id}")

    # Separate creatives by language (ad name contains RU / UA)
    ru_creatives = [(n, c) for n, c in artclass_creatives if "· RU ·" in n or n.endswith("· RU")]
    ua_creatives = [(n, c) for n, c in artclass_creatives if "· UA ·" in n or n.endswith("· UA")]

    # Fallback: split evenly if naming doesn't match
    if not ru_creatives and not ua_creatives:
        half = len(artclass_creatives) // 2 or 1
        ru_creatives = artclass_creatives[:half]
        ua_creatives = artclass_creatives[half:]

    for lang, locale_id, creatives in [
        ("RU", RU_LOCALE, ru_creatives or artclass_creatives),
        ("UA", UA_LOCALE, ua_creatives or artclass_creatives),
    ]:
        adset = api_post(f"/{AD_ACCOUNT}/adsets", {
            "name":              f"Art Classes · {lang} · Valencia 17km · traffic · {today}",
            "campaign_id":       ac_campaign_id,
            "status":            "PAUSED",
            "billing_event":     "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "bid_strategy":      "LOWEST_COST_WITHOUT_CAP",
            "destination_type":  "INSTAGRAM_DIRECT",
            "daily_budget":      300,
            "targeting":         targeting(locale_id),
            "promoted_object":   {"page_id": PAGE_ID},
        })
        adset_id = adset["id"]
        print(f"   ✓ {lang} ad set: {adset_id}")

        for ad_name, creative_id in creatives:
            ad = api_post(f"/{AD_ACCOUNT}/ads", {
                "name":     ad_name.replace("claude", "traffic"),
                "adset_id": adset_id,
                "creative": {"creative_id": creative_id},
                "status":   "PAUSED",
            })
            print(f"   ✓ Ad: {ad['id']}  (creative {creative_id})")
            time.sleep(0.3)

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("DONE")
    print(f"\nPAUSED (old, ENGAGEMENT):")
    print(f"  {OLD_HANDPAN_CAMPAIGN}  Handpan School")
    print(f"  {OLD_ARTCLASS_CAMPAIGN}  Art Classes")
    print(f"\nCREATED PAUSED (new, OUTCOME_TRAFFIC):")
    print(f"  {hp_campaign_id}  Handpan School · RU · traffic")
    print(f"  {ac_campaign_id}  Art Classes · RU+UA · traffic")
    print("\nActivate the two new campaigns in Ads Manager when ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
