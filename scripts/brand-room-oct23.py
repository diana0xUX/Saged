#!/usr/bin/env python3
"""
Brand Room — Жінка. Видимість. Гроші.
Event: 23 Oct 2026 @ Saged.club
Audience: Ukrainian-speaking women 25–45, Valencia Spain
Budget: €40 lifetime, Oct 20–22 2026
3 image creatives in one ad set, all created PAUSED.
"""

import json, os, sys, time
from datetime import datetime, timezone
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
UA_LOCALE    = 52

IMAGES = [
    "/tmp/br_6.png",
    "/tmp/br_5.png",
    "/tmp/br_4.png",
]

BODY = (
    "Жінка. Видимість. Гроші.\n\n"
    "Камерна зустріч у Валенсії про особистий бренд, Instagram та монетизацію.\n"
    "Розбираємо ваші профілі та ідеї наживо з бренд-стратегом.\n\n"
    "📍 Saged.club, C/ de les Cuines, 8\n"
    "🗓 23 жовтня · 12:00\n"
    "💫 40 € · Місць обмаль"
)
HEADLINE = "Brand Room — Валенсія, 23.10"

WELCOME_MSG = json.dumps({
    "type": "VISUAL_EDITOR",
    "version": 2,
    "landing_screen_type": "welcome_message",
    "media_type": "text",
    "text_format": {
        "customer_action_type": "ice_breakers",
        "message": {
            "autofill_message": {"content": "Привіт! Можна дізнатися більше про Brand Room?"},
            "text": "Привіт! Чим можемо допомогти?",
            "ice_breakers": [
                {"title": "Скільки коштує участь?", "response": None},
                {"title": "Чи ще є вільні місця?", "response": None},
                {"title": "Як зареєструватися?", "response": None},
            ],
        },
    },
    "ai_generated_icebreaker_toggle_enabled": True,
    "user_edit": True,
    "surface": "visual_editor_new",
}, ensure_ascii=False)

ASSET_FEED = {
    "optimization_type": "DOF_MESSAGING_DESTINATION",
    "call_to_actions": [
        {
            "type": "WHATSAPP_MESSAGE",
            "value": {
                "app_destination": "WHATSAPP",
                "link": "https://api.whatsapp.com/send",
            },
        },
        {
            "type": "INSTAGRAM_MESSAGE",
            "value": {
                "app_destination": "INSTAGRAM_DIRECT",
                "app_link": "instagram://direct?userid=28406719801",
                "link": "https://www.instagram.com/",
            },
        },
    ],
    "additional_data": {
        "multi_share_end_card": False,
        "is_click_to_message": True,
    },
}

# Oct 22 2026, 23:59 CET = 21:59 UTC
END_TS   = int(datetime(2026, 10, 22, 21, 59, tzinfo=timezone.utc).timestamp())
START_TS = int(datetime.now(timezone.utc).timestamp())


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
        filename = Path(image_path).name
        r = requests.post(
            f"{BASE}/{AD_ACCOUNT}/adimages",
            params=PARAMS,
            files={"filename": (filename, f, "image/png")},
        )
    if not r.ok:
        print(f"  Image upload FAILED: {r.text[:400]}")
        r.raise_for_status()
    data = r.json()
    for key, val in data.get("images", {}).items():
        return val["hash"]
    raise ValueError(f"No hash in response: {data}")


def main():
    # 1. Verify token
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    if not info.get("data", {}).get("is_valid"):
        sys.exit("Token invalid.")
    print(f"   ✓ Token valid")

    # 2. Verify UA locale
    print("2. Verifying Ukrainian locale ID...")
    res = api_get("/search", {"type": "adlocale", "q": "Ukrainian", "limit": 5})
    ua_id = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == "Ukrainian"), None)
    assert ua_id == UA_LOCALE, f"Ukrainian locale = {ua_id}, expected {UA_LOCALE}"
    print(f"   ✓ Ukrainian locale = {ua_id}")

    # 3. Upload images
    print("3. Uploading images...")
    hashes = []
    for img in IMAGES:
        h = upload_image(img)
        hashes.append(h)
        print(f"   ✓ {Path(img).name} → {h}")

    # 4. Campaign
    print("4. Creating campaign...")
    campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name":      "Saged · Brand Room · Oct 2026",
        "objective": "OUTCOME_ENGAGEMENT",
        "status":    "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    })
    campaign_id = campaign["id"]
    print(f"   ✓ Campaign: {campaign_id}")

    # 5. Ad set
    print("5. Creating ad set...")
    adset = api_post(f"/{AD_ACCOUNT}/adsets", {
        "name":            "Brand Room · UA · Women 25–45",
        "campaign_id":     campaign_id,
        "status":          "PAUSED",
        "billing_event":   "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy":    "LOWEST_COST_WITHOUT_CAP",
        "destination_type": "MESSAGING_INSTAGRAM_DIRECT_WHATSAPP",
        "lifetime_budget": 4000,  # €40 in cents
        "start_time":      START_TS,
        "end_time":        END_TS,
        "targeting": {
            "geo_locations": {
                "cities": [{"key": VALENCIA_KEY, "radius": 20, "distance_unit": "kilometer"}],
                "location_types": ["frequently_in", "home", "recent"],
            },
            "locales": [UA_LOCALE],
            "age_min": 25,
            "age_max": 45,
            "genders": [2],  # women
            "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
            "targeting_automation": {
                "advantage_audience": 0,
                "individual_setting": {"geo": 0},
            },
        },
        "promoted_object": {"page_id": PAGE_ID},
    })
    adset_id = adset["id"]
    print(f"   ✓ Ad set: {adset_id}")

    # 6. Creatives + ads
    print("6. Creating creatives and ads...")
    for i, (img_path, img_hash) in enumerate(zip(IMAGES, hashes), 1):
        name = Path(img_path).stem

        creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
            "name": f"Brand Room · {name}",
            "object_story_spec": {
                "page_id":           PAGE_ID,
                "instagram_user_id": IG_ACTOR,
                "link_data": {
                    "link":                  "https://api.whatsapp.com/send",
                    "message":               BODY,
                    "name":                  HEADLINE,
                    "description":           "Особистий бренд / Instagram / Монетизація",
                    "image_hash":            img_hash,
                    "page_welcome_message":  WELCOME_MSG,
                    "call_to_action": {
                        "type":  "WHATSAPP_MESSAGE",
                        "value": {"app_destination": "WHATSAPP"},
                    },
                },
            },
            "asset_feed_spec": ASSET_FEED,
        })
        creative_id = creative["id"]
        print(f"   ✓ Creative {i} ({name}): {creative_id}")

        ad = api_post(f"/{AD_ACCOUNT}/ads", {
            "name":      f"Brand Room · {name}",
            "adset_id":  adset_id,
            "creative":  {"creative_id": creative_id},
            "status":    "PAUSED",
        })
        print(f"   ✓ Ad {i}: {ad['id']}")
        time.sleep(0.5)

    print("\n" + "=" * 55)
    print("DONE — all created PAUSED")
    print(f"Campaign:  {campaign_id}")
    print(f"Ad set:    {adset_id}")
    print("Go to Ads Manager and ACTIVATE the campaign.")
    print("=" * 55)


if __name__ == "__main__":
    main()
