#!/usr/bin/env python3
"""
Art Classes — Saged Studio
Two languages: RU + UA, €2/day each (€4/day total)
Two videos per ad set (IMG_9370, IMG_9371)
Destination: Instagram Direct messages
All created PAUSED.
"""

import json, os, sys, time
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

VIDEOS = [
    "/Users/diana/Documents/saged.club/art classes/IMG_9370.MOV",
    "/Users/diana/Documents/saged.club/art classes/IMG_9371.MOV",
]

VALENCIA_KEY = 699854
RU_LOCALE    = 17
UA_LOCALE    = 52

BODY_RU = (
    "Рисование. Кисть. Краски. Тишина.\n\n"
    "Небольшие занятия по искусству в Saged Studio — "
    "для тех, кто хочет замедлиться и создавать руками.\n\n"
    "📍 Валенсия, C/ de les Cuines, 8\n"
    "✉️ Напишите в Direct — расскажем о ближайших занятиях"
)
HEADLINE_RU = "Занятия по искусству — Saged Studio"

BODY_UA = (
    "Малювання. Пензель. Фарби. Тиша.\n\n"
    "Невеликі заняття з мистецтва в Saged Studio — "
    "для тих, хто хоче сповільнитися і творити руками.\n\n"
    "📍 Валенсія, C/ de les Cuines, 8\n"
    "✉️ Напишіть у Direct — розкажемо про найближчі заняття"
)
HEADLINE_UA = "Заняття з мистецтва — Saged Studio"

WELCOME_RU = json.dumps({
    "type": "VISUAL_EDITOR",
    "version": 2,
    "landing_screen_type": "welcome_message",
    "media_type": "text",
    "text_format": {
        "customer_action_type": "ice_breakers",
        "message": {
            "autofill_message": {"content": "Привет! Хочу узнать о занятиях по искусству"},
            "text": "Привет! Чем можем помочь?",
            "ice_breakers": [
                {"title": "Когда ближайшее занятие?", "response": None},
                {"title": "Сколько стоит занятие?", "response": None},
                {"title": "Как записаться?", "response": None},
            ],
        },
    },
    "user_edit": True,
    "surface": "visual_editor_new",
}, ensure_ascii=False)

WELCOME_UA = json.dumps({
    "type": "VISUAL_EDITOR",
    "version": 2,
    "landing_screen_type": "welcome_message",
    "media_type": "text",
    "text_format": {
        "customer_action_type": "ice_breakers",
        "message": {
            "autofill_message": {"content": "Привіт! Хочу дізнатися про заняття з мистецтва"},
            "text": "Привіт! Чим можемо допомогти?",
            "ice_breakers": [
                {"title": "Коли найближче заняття?", "response": None},
                {"title": "Скільки коштує заняття?", "response": None},
                {"title": "Як записатися?", "response": None},
            ],
        },
    },
    "user_edit": True,
    "surface": "visual_editor_new",
}, ensure_ascii=False)


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
    assert found == expected_id, f"{name} locale = {found}, expected {expected_id}"
    return found


def upload_video(video_path):
    name = Path(video_path).name
    print(f"   Uploading {name} ({Path(video_path).stat().st_size // 1024}KB)...")
    with open(video_path, "rb") as f:
        r = requests.post(
            f"{BASE}/{AD_ACCOUNT}/advideos",
            params=PARAMS,
            files={"source": (name, f, "video/quicktime")},
            data={"name": name},
        )
    if not r.ok:
        print(f"  Video upload FAILED: {r.text[:400]}")
        r.raise_for_status()
    video_id = r.json()["id"]
    print(f"   Uploaded → id {video_id}, waiting for processing...")

    # Poll until ready (max ~3 min)
    for _ in range(36):
        time.sleep(5)
        status = api_get(f"/{video_id}", {"fields": "status"})
        vs = status.get("status", {})
        if vs.get("video_status") == "ready":
            print(f"   ✓ {name} ready")
            return video_id
        if vs.get("video_status") == "error":
            raise ValueError(f"Video processing error: {vs}")
        prog = vs.get("processing_progress", "?")
        print(f"     … {prog}% processed")

    raise TimeoutError(f"Video {name} did not finish processing in 3 minutes")


def main():
    # 1. Token
    print("1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid"
    print("   ✓ Token valid")

    # 2. Locales
    print("2. Verifying locale IDs...")
    ru = verify_locale("Russian", RU_LOCALE)
    ua = verify_locale("Ukrainian", UA_LOCALE)
    print(f"   ✓ Russian={ru}, Ukrainian={ua}")

    # 3. Videos already uploaded — reuse IDs
    video_ids = ["1463318399056128", "1120763570489161"]
    print(f"3. Reusing uploaded videos: {video_ids}")

    # 3b. Upload thumbnails
    print("3b. Uploading video thumbnails...")
    thumb_paths = ["/tmp/thumb_9370.png", "/tmp/thumb_9371.png"]
    thumb_hashes = []
    for tp in thumb_paths:
        with open(tp, "rb") as f:
            r = requests.post(
                f"{BASE}/{AD_ACCOUNT}/adimages",
                params=PARAMS,
                files={"filename": (Path(tp).name, f, "image/png")},
            )
        if not r.ok:
            print(f"  Thumbnail upload FAILED: {r.text[:400]}")
            r.raise_for_status()
        data = r.json()
        for key, val in data.get("images", {}).items():
            h = val["hash"]
            thumb_hashes.append(h)
            print(f"   ✓ {Path(tp).name} → {h}")
            break

    # 4. Campaign (already created — reuse to avoid duplicates)
    campaign_id = "120250085874070513"
    print(f"4. Reusing existing campaign: {campaign_id}")

    TARGETING_BASE = {
        "geo_locations": {
            "cities": [{"key": VALENCIA_KEY, "radius": 20, "distance_unit": "kilometer"}],
            "location_types": ["home"],
        },
        "age_min": 25,
        "age_max": 54,
        "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
        "targeting_automation": {"advantage_audience": 0},
    }

    # RU ad set already created in previous run — reuse
    existing_adsets = {"RU": "120250085878380513"}

    for lang, locale_id, body, headline, welcome in [
        ("RU", RU_LOCALE, BODY_RU, HEADLINE_RU, WELCOME_RU),
        ("UA", UA_LOCALE, BODY_UA, HEADLINE_UA, WELCOME_UA),
    ]:
        if lang in existing_adsets:
            adset_id = existing_adsets[lang]
            print(f"\n5. Reusing {lang} ad set: {adset_id}")
        else:
            print(f"\n5. Creating {lang} ad set...")
        if lang not in existing_adsets:
            adset = api_post(f"/{AD_ACCOUNT}/adsets", {
                "name":              f"Art Classes · {lang} · Valencia",
                "campaign_id":       campaign_id,
                "status":            "PAUSED",
                "billing_event":     "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy":      "LOWEST_COST_WITHOUT_CAP",
                "destination_type":  "INSTAGRAM_DIRECT",
                "daily_budget":      300,  # €3/day (Meta floor is €2.68)
                "targeting": {**TARGETING_BASE, "locales": [locale_id]},
                "promoted_object":   {"page_id": PAGE_ID},
            })
            adset_id = adset["id"]
            print(f"   ✓ Ad set: {adset_id}")

        for i, (vid_path, vid_id, thumb_hash) in enumerate(zip(VIDEOS, video_ids, thumb_hashes), 1):
            vname = Path(vid_path).stem
            print(f"   Creating creative+ad {i} ({vname})...")
            creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
                "name": f"Art Classes · {lang} · {vname}",
                "object_story_spec": {
                    "page_id":           PAGE_ID,
                    "instagram_user_id": IG_ACTOR,
                    "video_data": {
                        "video_id":           vid_id,
                        "image_hash":         thumb_hash,
                        "message":            body,
                        "title":              headline,
                        "call_to_action": {
                            "type":  "INSTAGRAM_MESSAGE",
                            "value": {
                                "app_destination": "INSTAGRAM_DIRECT",
                                "app_link": "instagram://direct?userid=28406719801",
                                "link":     "https://www.instagram.com/",
                            },
                        },
                        "page_welcome_message": welcome,
                    },
                },
            })
            creative_id = creative["id"]

            ad = api_post(f"/{AD_ACCOUNT}/ads", {
                "name":     f"Art Classes · {lang} · {vname}",
                "adset_id": adset_id,
                "creative": {"creative_id": creative_id},
                "status":   "PAUSED",
            })
            print(f"   ✓ Creative {creative_id} → Ad {ad['id']}")
            time.sleep(0.5)

    print("\n" + "=" * 55)
    print("DONE — all created PAUSED")
    print(f"Campaign:  {campaign_id}")
    print("Go to Ads Manager and ACTIVATE all three campaigns.")
    print("=" * 55)


if __name__ == "__main__":
    main()
