#!/usr/bin/env python3
"""
Create 3 August event ads for Saged.club via Meta Marketing API v25.0.
All entities created PAUSED — Diana activates in Ads Manager.

Events:
  1. Gardens of Flavor     — 17 Aug, €40
  2. Tea Club Friending    — 26 Aug, €15
  3. The Art of Dashi      — 30 Aug, €40

Budget: €2.50/day per ad set (RU + UA = €5/day total per event)
Duration: 3 days ending on event day
Targeting: Valencia, Spain (17km, home only) | RU locale=17, UA locale=52
"""

import requests, json, sys, time
from datetime import datetime, timezone, timedelta

TOKEN      = "EAAS5i1HnFAYBRS7EZCOxmRHviIkLr3x41QZAfxzPeh3a1zdPJ8NpZBgtu3Wj34xQtIq4oXTnzIVPkDwEZCbBZBz440myL1j3yYFxIp7LHuITsG4pdoFlbE0vObSZCj45SjtBTrbwY7r1ZBFSlhwIo0ZABBRZBDgnlRSuMc021zlqoHvP3FIyFCeQUxGtcDfL6dwZDZD"
AD_ACCOUNT = "act_484884320671439"
IG_ACTOR   = "17841428554040839"
API_V      = "v25.0"
BASE       = f"https://graph.facebook.com/{API_V}"
PARAMS     = {"access_token": TOKEN}

LINK = "https://saged.club"

EVENTS = [
    {
        "slug":       "gardens-of-flavor",
        "name":       "Gardens of Flavor",
        "event_date": datetime(2026, 8, 17, tzinfo=timezone.utc),
        "image":      "/Users/diana/Downloads/Instagram post opening 28.png",
        "ru": {
            "headline": "Gardens of Flavor · Дегустация чая",
            "body": (
                "Три ферментированных украинских чая — груша, малина, вишня.\n"
                "Пробуем, сравниваем, ищем свой вкус.\n\n"
                "17 августа · 18:30–20:30 · Saged Club · €40\n\n"
                "Запись — в DM 🌿"
            ),
        },
        "ua": {
            "headline": "Gardens of Flavor · Дегустація чаю",
            "body": (
                "Три ферментованих українських чаї — груша, малина, вишня.\n"
                "Пробуємо, порівнюємо, шукаємо свій смак.\n\n"
                "17 серпня · 18:30–20:30 · Saged Club · €40\n\n"
                "Запис — у DM 🌿"
            ),
        },
    },
    {
        "slug":       "tea-club-friending",
        "name":       "Tea Club · Friending",
        "event_date": datetime(2026, 8, 26, tzinfo=timezone.utc),
        "image":      "/Users/diana/Downloads/Instagram post opening 26.png",
        "ru": {
            "headline": "Tea Club · Вечер знакомств",
            "body": (
                "Вечер для тех, кто хочет познакомиться, пообщаться "
                "и просто провести время вместе за хорошим чаем.\n\n"
                "26 августа · 18:30–20:00 · Saged Club · €15\n\n"
                "Запись — в DM 🌿"
            ),
        },
        "ua": {
            "headline": "Tea Club · Вечір знайомств",
            "body": (
                "Вечір для тих, хто хоче познайомитися, поспілкуватися "
                "і просто провести час разом за хорошим чаєм.\n\n"
                "26 серпня · 18:30–20:00 · Saged Club · €15\n\n"
                "Запис — у DM 🌿"
            ),
        },
    },
    {
        "slug":       "art-of-dashi",
        "name":       "The Art of Dashi",
        "event_date": datetime(2026, 8, 30, tzinfo=timezone.utc),
        "image":      "/Users/diana/Downloads/Instagram post opening 27.png",
        "ru": {
            "headline": "The Art of Dashi · Чайная церемония",
            "body": (
                "Kōridashi · Mizudashi · Ōyudashi\n"
                "Три температуры воды, один чай — совершенно разный вкус.\n\n"
                "30 августа · 14:00 · 2 часа · Saged Club · €40\n\n"
                "Запись — в DM 🌿"
            ),
        },
        "ua": {
            "headline": "The Art of Dashi · Чайна церемонія",
            "body": (
                "Kōridashi · Mizudashi · Ōyudashi\n"
                "Три температури води, один чай — зовсім різний смак.\n\n"
                "30 серпня · 14:00 · 2 години · Saged Club · €40\n\n"
                "Запис — у DM 🌿"
            ),
        },
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

def upload_image(image_path):
    with open(image_path, "rb") as f:
        filename = image_path.split("/")[-1]
        r = requests.post(
            f"{BASE}/{AD_ACCOUNT}/adimages",
            params=PARAMS,
            files={"filename": (filename, f, "image/png")},
        )
    if not r.ok:
        print(f"  Image upload FAILED: {r.text[:400]}")
        r.raise_for_status()
    data = r.json()
    images = data.get("images", {})
    for key, val in images.items():
        return val["hash"]
    raise ValueError(f"No hash in response: {data}")

def dt_to_unix(dt):
    return int(dt.timestamp())

def main():
    # ── 1. Verify token ──────────────────────────────────────────────────────
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    if not info.get("data", {}).get("is_valid"):
        sys.exit("Token is invalid. Re-generate at developers.facebook.com/tools/explorer")
    scopes = info["data"].get("scopes", [])
    assert "ads_management" in scopes, f"Missing ads_management scope. Scopes: {scopes}"
    print(f"   ✓ Token valid. Scopes include ads_management.")

    # ── 2. Verify locale IDs ─────────────────────────────────────────────────
    print("2. Verifying locale IDs via API...")
    ru_res = api_get("/search", {"type": "adlocale", "q": "Russian", "limit": 20})
    ua_res = api_get("/search", {"type": "adlocale", "q": "Ukrainian", "limit": 20})
    ru_id = next((int(x["key"]) for x in ru_res.get("data", []) if x.get("name") == "Russian"), None)
    ua_id = next((int(x["key"]) for x in ua_res.get("data", []) if x.get("name") == "Ukrainian"), None)
    assert ru_id == 17, f"Russian locale ID = {ru_id}, expected 17. Abort."
    assert ua_id == 52, f"Ukrainian locale ID = {ua_id}, expected 52. Abort."
    print(f"   ✓ Russian={ru_id}, Ukrainian={ua_id}")

    # ── 3. Verify Valencia city key ──────────────────────────────────────────
    print("3. Verifying Valencia, Spain city key via API...")
    geo_res = api_get("/search", {
        "type": "adgeolocation",
        "q": "Valencia",
        "location_types": '["city"]',
        "country_code": "ES",
        "limit": 20,
    })
    valencia_key = None
    for item in geo_res.get("data", []):
        if item.get("name") == "Valencia" and item.get("country_code") == "ES":
            valencia_key = int(item["key"])
            break
    assert valencia_key == 699854, f"Valencia key = {valencia_key}, expected 699854. Abort."
    print(f"   ✓ Valencia, ES city key = {valencia_key}")

    # ── 4. Get Facebook Page ID ──────────────────────────────────────────────
    print("4. Fetching Facebook Page ID...")
    accounts = api_get("/me/accounts", {"limit": 10})
    page_id = None
    page_name = None
    for page in accounts.get("data", []):
        page_id = page["id"]
        page_name = page.get("name", "")
        print(f"   Found page: {page_name} ({page_id})")
        break
    if not page_id:
        sys.exit("No Facebook page found for this token. Cannot create ads.")
    print(f"   ✓ Using page: {page_name} ({page_id})")

    # ── 5. Upload images ─────────────────────────────────────────────────────
    print("5. Uploading images...")
    image_hashes = {}
    for event in EVENTS:
        print(f"   Uploading {event['name']}...")
        h = upload_image(event["image"])
        image_hashes[event["slug"]] = h
        print(f"   ✓ Hash: {h}")

    # ── 6. Create campaigns + ad sets + ads ──────────────────────────────────
    created = []

    for event in EVENTS:
        slug = event["slug"]
        print(f"\n6. Creating campaign: {event['name']}...")

        # Campaign runs from 3 days before event to event day
        end_ts   = dt_to_unix(event["event_date"] + timedelta(hours=23, minutes=59))
        start_ts = dt_to_unix(event["event_date"] - timedelta(days=2))
        now_ts   = dt_to_unix(datetime.now(timezone.utc))
        if start_ts < now_ts:
            start_ts = now_ts  # don't schedule in the past

        # -- Campaign --
        campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
            "name":      f"Saged · {event['name']} · Aug 2026",
            "objective": "OUTCOME_TRAFFIC",
            "status":    "PAUSED",
            "special_ad_categories": [],
            "is_adset_budget_sharing_enabled": False,
        })
        campaign_id = campaign["id"]
        print(f"   ✓ Campaign: {campaign_id}")

        campaign_entry = {
            "event":       event["name"],
            "campaign_id": campaign_id,
            "ad_sets":     [],
        }

        for lang, locale_id, label in [("ru", 17, "RU"), ("ua", 52, "UA")]:
            copy = event[lang]

            # -- Ad Set --
            adset = api_post(f"/{AD_ACCOUNT}/adsets", {
                "name":            f"Saged · {event['name']} · {label}",
                "campaign_id":     campaign_id,
                "status":          "PAUSED",
                "billing_event":   "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy":    "LOWEST_COST_WITHOUT_CAP",
                "daily_budget":    250,  # €2.50 in cents
                "start_time":      start_ts,
                "end_time":        end_ts,
                "targeting": {
                    "geo_locations": {
                        "cities": [{"key": 699854, "radius": 17, "distance_unit": "kilometer"}],
                        "location_types": ["home"],
                    },
                    "locales": [locale_id],
                    "age_min": 18,
                    "age_max": 55,
                    "targeting_automation": {"advantage_audience": 0},
                },
                "promoted_object": {"page_id": page_id},
            })
            adset_id = adset["id"]
            print(f"   ✓ Ad set {label}: {adset_id}")

            # -- Creative --
            creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
                "name": f"Saged · {event['name']} · {label} · Creative",
                "object_story_spec": {
                    "page_id": page_id,
                    "link_data": {
                        "image_hash":  image_hashes[slug],
                        "link":        LINK,
                        "message":     copy["body"],
                        "name":        copy["headline"],
                        "call_to_action": {
                            "type":  "LEARN_MORE",
                            "value": {"link": LINK},
                        },
                    },
                },
            })
            creative_id = creative["id"]
            print(f"   ✓ Creative {label}: {creative_id}")

            # -- Ad --
            ad = api_post(f"/{AD_ACCOUNT}/ads", {
                "name":        f"Saged · {event['name']} · {label} · Ad",
                "adset_id":    adset_id,
                "creative":    {"creative_id": creative_id},
                "status":      "PAUSED",
            })
            ad_id = ad["id"]
            print(f"   ✓ Ad {label}: {ad_id}")

            campaign_entry["ad_sets"].append({
                "lang":        label,
                "adset_id":    adset_id,
                "creative_id": creative_id,
                "ad_id":       ad_id,
            })

        created.append(campaign_entry)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("ALL DONE — all entities created PAUSED")
    print("Activate in Ads Manager: business.facebook.com/adsmanager")
    print("="*60)
    for c in created:
        print(f"\n{c['event']}")
        print(f"  Campaign: {c['campaign_id']}")
        for ads in c["ad_sets"]:
            print(f"  {ads['lang']}: adset={ads['adset_id']}  ad={ads['ad_id']}")

if __name__ == "__main__":
    main()
