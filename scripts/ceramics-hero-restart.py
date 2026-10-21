#!/usr/bin/env python3
"""
Restart: Керамика с Корицей — Hero RU + UA videos
Same creatives as the May 2026 campaign (video IDs, copy, links preserved exactly).
OUTCOME_TRAFFIC at €3/day each — original used OUTCOME_SALES which needs
25+ conversions/week to exit learning phase; traffic works at low budget.
"""

import json, sys
from pathlib import Path
import requests

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

VALENCIA_KEY = 699854
RU_LOCALE    = 17
UA_LOCALE    = 52

# Original winning creatives — preserved exactly
ADS = [
    {
        "lang":    "UA",
        "locale":  UA_LOCALE,
        "link":    "https://saged.club/uk/",
        "video_id": "1542298757583243",
        "image_hash": "4d0158305e5551b89cc8461d29d05b44",
        "title":   "Кераміка з Корицею · Saged.club",
        "message": (
            "Сповільнитися, попрацювати руками з глиною та забрати додому свою кераміку. "
            "Курс із двох 2-годинних занять, щочетверга у старій Валенсії. "
            "€60 за обидві зустрічі. До 6 осіб."
        ),
    },
    {
        "lang":    "RU",
        "locale":  RU_LOCALE,
        "link":    "https://saged.club/",
        "video_id": "959536350220678",
        "image_hash": "4d0158305e5551b89cc8461d29d05b44",
        "title":   "Керамика с Корицей · Saged.club",
        "message": (
            "Замедлиться, поработать руками с глиной и забрать домой свою керамику. "
            "Курс из двух 2-часовых занятий, каждый четверг в старой Валенсии. "
            "€60 за обе встречи. До 6 человек."
        ),
    },
]


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


def activate(eid, label):
    r = requests.post(f"{BASE}/{eid}", params=PARAMS, json={"status": "ACTIVE"})
    print(f"  {'✓' if r.ok else '✗'} ACTIVE: {label}")


def verify_locale(name, expected_id):
    res = api_get("/search", {"type": "adlocale", "q": name, "limit": 5})
    found = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == name), None)
    assert found == expected_id, f"{name} locale = {found}, expected {expected_id}"
    return found


def main():
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid"
    print("   ✓ Token valid")

    print("2. Verifying locales...")
    verify_locale("Russian", RU_LOCALE)
    verify_locale("Ukrainian", UA_LOCALE)
    print(f"   ✓ RU={RU_LOCALE}, UA={UA_LOCALE}")

    print("3. Creating campaign...")
    campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name":      "Saged · Керамика с Корицей · v2 · Oct 2026",
        "objective": "OUTCOME_TRAFFIC",
        "status":    "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    })
    campaign_id = campaign["id"]
    print(f"   ✓ Campaign: {campaign_id}")

    ad_ids = []
    for ad_cfg in ADS:
        lang = ad_cfg["lang"]
        print(f"\n4. Creating {lang} ad set...")
        adset = api_post(f"/{AD_ACCOUNT}/adsets", {
            "name":              f"Керамика · {lang} · Valencia · Oct 2026",
            "campaign_id":       campaign_id,
            "status":            "PAUSED",
            "billing_event":     "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "bid_strategy":      "LOWEST_COST_WITHOUT_CAP",
            "destination_type":  "WEBSITE",
            "daily_budget":      300,  # €3/day
            "targeting": {
                "geo_locations": {
                    "cities": [{"key": VALENCIA_KEY, "radius": 17, "distance_unit": "kilometer"}],
                    "location_types": ["home"],
                },
                "locales": [ad_cfg["locale"]],
                "age_min": 25,
                "age_max": 54,
                "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
                "targeting_automation": {"advantage_audience": 0},
            },
            "promoted_object": {"page_id": PAGE_ID},
        })
        adset_id = adset["id"]
        print(f"   ✓ Ad set: {adset_id}")

        print(f"   Creating creative ({lang})...")
        creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
            "name": f"Керамика Hero · {lang} · v2 rerun",
            "object_story_spec": {
                "page_id": PAGE_ID,
                "video_data": {
                    "video_id":   ad_cfg["video_id"],
                    "image_hash": ad_cfg["image_hash"],
                    "title":      ad_cfg["title"],
                    "message":    ad_cfg["message"],
                    "call_to_action": {
                        "type":  "LEARN_MORE",
                        "value": {"link": ad_cfg["link"]},
                    },
                },
            },
        })
        creative_id = creative["id"]
        print(f"   ✓ Creative: {creative_id}")

        ad = api_post(f"/{AD_ACCOUNT}/ads", {
            "name":     f"Керамика Hero · {lang} · v2 rerun",
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status":   "PAUSED",
        })
        ad_id = ad["id"]
        print(f"   ✓ Ad: {ad_id}")
        ad_ids.append((campaign_id, adset_id, ad_id, lang))

    print("\n5. Activating everything...")
    activate(campaign_id, "campaign")
    for cid, asid, aid, lang in ad_ids:
        activate(asid, f"ad set {lang}")
        activate(aid,  f"ad {lang}")

    print("\n" + "=" * 55)
    print("DONE — live")
    print(f"Campaign: {campaign_id}")
    print("=" * 55)


if __name__ == "__main__":
    main()
