#!/usr/bin/env python3
"""
boost-post-DewNEQwOSxe.py

Boost Instagram post DewNEQwOSxe as an awareness campaign.
Objective: OUTCOME_AWARENESS (reach/impressions — people see it, not likes)
Audience:  RU women 25-45 + UA women 25-45, Valencia 17km, home only
Budget:    €1/day per ad set (€2/day total)
Created PAUSED — Diana activates.
"""
from __future__ import annotations
import time
from pathlib import Path
import requests

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
env: dict[str, str] = {}
for line in ENV_FILE.read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("="); env[k.strip()] = v.strip()

TOKEN      = env["META_ACCESS_TOKEN"]
AD_ACCOUNT = env["META_AD_ACCOUNT_ID"]
API_V      = env["META_API_VERSION"]
BASE       = f"https://graph.facebook.com/{API_V}"
PARAMS     = {"access_token": TOKEN}
PAGE_ID    = "373458682506494"
IG_ACTOR   = "17841428554040839"

VALENCIA_KEY  = 699854
RU_LOCALE     = 17
UA_LOCALE     = 52
MEDIA_ID      = "4012764735458585694"  # decoded from shortcode DewNEQwOSxe
TODAY         = "2026-10-21"


def api_get(path, params=None):
    r = requests.get(f"{BASE}{path}", params={**PARAMS, **(params or {})})
    if not r.ok:
        print(f"  GET {path} FAILED: {r.text[:400]}")
        r.raise_for_status()
    return r.json()

def api_post(path, data):
    r = requests.post(f"{BASE}{path}", params=PARAMS, json=data)
    if not r.ok:
        print(f"  POST {path} FAILED: {r.text[:600]}")
        r.raise_for_status()
    return r.json()

def verify_locale(name, expected_id):
    res = api_get("/search", {"type": "adlocale", "q": name, "limit": 5})
    found = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == name), None)
    assert found == expected_id, f"{name} locale = {found}, expected {expected_id} — STOP"
    return found

def verify_city():
    res = api_get("/search", {"type": "adgeolocation", "q": "Valencia", "location_types": '["city"]', "limit": 5})
    found = next((int(x["key"]) for x in res.get("data", []) if "Valencia" in x.get("name","") and x.get("country_code") == "ES"), None)
    assert found == VALENCIA_KEY, f"Valencia key = {found}, expected {VALENCIA_KEY} — STOP"
    return found

def targeting(locale_id):
    return {
        "geo_locations": {
            "cities": [{"key": VALENCIA_KEY, "radius": 17, "distance_unit": "kilometer"}],
            "location_types": ["home"],
        },
        "locales": [locale_id],
        "genders": [2],       # women only
        "age_min": 25,
        "age_max": 45,
        "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
        "targeting_automation": {"advantage_audience": 0},
    }


def main():
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid — STOP"
    print("   ✓ Token valid")

    print("2. Verifying locale and city IDs at runtime...")
    ru = verify_locale("Russian", RU_LOCALE)
    ua = verify_locale("Ukrainian", UA_LOCALE)
    vc = verify_city()
    print(f"   ✓ Russian={ru}  Ukrainian={ua}  Valencia={vc}")

    print("3. Creating ad creative from existing post...")
    creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
        "name":                    f"Post boost · DewNEQwOSxe · {TODAY}",
        "instagram_actor_id":      IG_ACTOR,
        "object_id":               PAGE_ID,
        "source_instagram_media_id": MEDIA_ID,
    })
    creative_id = creative["id"]
    print(f"   ✓ Creative: {creative_id}")

    print("4. Creating OUTCOME_AWARENESS campaign...")
    campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name":      f"Saged · Post boost · DewNEQwOSxe · awareness · {TODAY}",
        "objective": "OUTCOME_AWARENESS",
        "status":    "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    })
    campaign_id = campaign["id"]
    print(f"   ✓ Campaign: {campaign_id}")

    ad_ids = []
    for lang, locale_id in [("RU", RU_LOCALE), ("UA", UA_LOCALE)]:
        print(f"\n5. Creating {lang} ad set...")
        adset = api_post(f"/{AD_ACCOUNT}/adsets", {
            "name":              f"Post boost · {lang} · women 25-45 · Valencia · {TODAY}",
            "campaign_id":       campaign_id,
            "status":            "PAUSED",
            "billing_event":     "IMPRESSIONS",
            "optimization_goal": "REACH",
            "bid_strategy":      "LOWEST_COST_WITHOUT_CAP",
            "daily_budget":      100,   # €1/day
            "targeting":         targeting(locale_id),
            "promoted_object":   {"page_id": PAGE_ID},
        })
        adset_id = adset["id"]
        print(f"   ✓ Ad set: {adset_id}")

        ad = api_post(f"/{AD_ACCOUNT}/ads", {
            "name":     f"Post boost · {lang} · DewNEQwOSxe · {TODAY}",
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status":   "PAUSED",
        })
        ad_ids.append(ad["id"])
        print(f"   ✓ Ad: {ad['id']}")
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("DONE — created PAUSED")
    print(f"\nCampaign: {campaign_id}")
    print(f"Creative: {creative_id}")
    print(f"Ads: {', '.join(ad_ids)}")
    print("\nActivate in Ads Manager when ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
