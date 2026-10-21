#!/usr/bin/env python3
"""
Handpan School — Denis Balykin @ Saged Club
Every Sunday 12:00, €50/session
Russian-speaking audience, Valencia
€3/day, open-ended, Instagram + WhatsApp messages
All created PAUSED.
"""

import json, sys, time
from pathlib import Path
from PIL import Image
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

SOURCE_IMAGE = "/Users/diana/Documents/saged.club/oct/Codex Image 9 Oct 2026, 14_14_43.png"
RESIZED      = "/tmp/handpan_school.png"

BODY = (
    "Хочешь научиться играть на хэнпане?\n\n"
    "Еженедельные занятия с Денисом Балыкиным в Saged Club — "
    "для начинающих, без опыта и своего инструмента.\n\n"
    "🎵 Каждое воскресенье в 12:00\n"
    "📍 C/ de les Cuines, 8, Valencia\n"
    "💰 50€ за занятие\n\n"
    "Напиши нам — расскажем подробнее и запишем ↓"
)
HEADLINE = "Handpan School — каждое воскресенье"

WELCOME_MSG = json.dumps({
    "type": "VISUAL_EDITOR",
    "version": 2,
    "landing_screen_type": "welcome_message",
    "media_type": "text",
    "text_format": {
        "customer_action_type": "ice_breakers",
        "message": {
            "autofill_message": {"content": "Привет! Хочу узнать о занятиях по хэнпану"},
            "text": "Привет! Чем можем помочь?",
            "ice_breakers": [
                {"title": "Когда ближайшее занятие?", "response": None},
                {"title": "Нужен ли свой инструмент?", "response": None},
                {"title": "Как записаться?", "response": None},
            ],
        },
    },
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
        r = requests.post(
            f"{BASE}/{AD_ACCOUNT}/adimages",
            params=PARAMS,
            files={"filename": (Path(image_path).name, f, "image/png")},
        )
    if not r.ok:
        print(f"  Image upload FAILED: {r.text[:400]}")
        r.raise_for_status()
    data = r.json()
    for key, val in data.get("images", {}).items():
        return val["hash"]
    raise ValueError(f"No hash in response: {data}")


def main():
    # 1. Token
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid"
    print("   ✓ Token valid")

    # 2. Verify Russian locale
    print("2. Verifying Russian locale ID...")
    res = api_get("/search", {"type": "adlocale", "q": "Russian", "limit": 5})
    ru_id = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == "Russian"), None)
    assert ru_id == RU_LOCALE, f"Russian locale = {ru_id}, expected {RU_LOCALE}"
    print(f"   ✓ Russian locale = {ru_id}")

    # 3. Resize + upload image
    print("3. Resizing image to 1080×1350...")
    img = Image.open(SOURCE_IMAGE).convert("RGB")
    img = img.resize((1080, 1350), Image.LANCZOS)
    img.save(RESIZED, "PNG", optimize=True)
    print(f"   Saved to {RESIZED}")

    print("   Uploading...")
    img_hash = upload_image(RESIZED)
    print(f"   ✓ Hash: {img_hash}")

    # 4. Campaign
    print("4. Creating campaign...")
    campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name":      "Saged · Handpan School · RU",
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
        "name":            "Handpan School · RU · Valencia",
        "campaign_id":     campaign_id,
        "status":          "PAUSED",
        "billing_event":   "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy":    "LOWEST_COST_WITHOUT_CAP",
        "destination_type": "MESSAGING_INSTAGRAM_DIRECT_WHATSAPP",
        "daily_budget":    300,  # €3/day
        "targeting": {
            "geo_locations": {
                "cities": [{"key": VALENCIA_KEY, "radius": 20, "distance_unit": "kilometer"}],
                "location_types": ["home"],
            },
            "locales": [RU_LOCALE],
            "age_min": 20,
            "age_max": 50,
            "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
            "targeting_automation": {"advantage_audience": 0},
        },
        "promoted_object": {"page_id": PAGE_ID},
    })
    adset_id = adset["id"]
    print(f"   ✓ Ad set: {adset_id}")

    # 6. Creative + ad
    print("6. Creating creative and ad...")
    creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
        "name": "Handpan School · RU · poster",
        "object_story_spec": {
            "page_id":           PAGE_ID,
            "instagram_user_id": IG_ACTOR,
            "link_data": {
                "link":                 "https://api.whatsapp.com/send",
                "message":              BODY,
                "name":                 HEADLINE,
                "description":          "Хэнпан · Saged Club · Валенсия",
                "image_hash":           img_hash,
                "page_welcome_message": WELCOME_MSG,
                "call_to_action": {
                    "type":  "WHATSAPP_MESSAGE",
                    "value": {"app_destination": "WHATSAPP"},
                },
            },
        },
        "asset_feed_spec": ASSET_FEED,
    })
    creative_id = creative["id"]
    print(f"   ✓ Creative: {creative_id}")

    ad = api_post(f"/{AD_ACCOUNT}/ads", {
        "name":     "Handpan School · RU · poster",
        "adset_id": adset_id,
        "creative": {"creative_id": creative_id},
        "status":   "PAUSED",
    })
    print(f"   ✓ Ad: {ad['id']}")

    print("\n" + "=" * 55)
    print("DONE — created PAUSED")
    print(f"Campaign:  {campaign_id}")
    print(f"Ad set:    {adset_id}")
    print("Go to Ads Manager and ACTIVATE the campaign.")
    print("=" * 55)


if __name__ == "__main__":
    main()
