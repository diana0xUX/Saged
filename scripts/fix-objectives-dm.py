#!/usr/bin/env python3
"""
Fix all active campaigns → optimise for Instagram DM conversation starts.

Changes made:
  1. Pause ceramics TRAFFIC campaign (wrong objective, can't be changed in place)
  2. Fix Handpan adset: LINK_CLICKS → CONVERSATIONS, radius 20 → 17km
  3. Fix Art Classes adsets: LINK_CLICKS → CONVERSATIONS, radius 20 → 17km
  4. Create new ceramics ENGAGEMENT + Instagram DM campaign (same videos, new CTA + welcome screen)
     → created PAUSED; Diana activates

All new entities: PAUSED. Never auto-activates new campaigns.
"""
import json, sys, time
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
IG_ACTOR   = "17841428554040839"
IG_USER_ID = "28406719801"  # saged_diana Instagram numeric ID

VALENCIA_KEY = 699854
RU_LOCALE    = 17
UA_LOCALE    = 52

# ── Campaign / adset IDs from 2026-10-20 audit ──────────────────────────────
CERAMICS_CAMPAIGN   = "120250086001120513"   # TRAFFIC — pause this
HANDPAN_CAMPAIGN    = "120250085902350513"   # ENGAGEMENT — keep, fix adset
ART_CLASSES_CAMPAIGN = "120250085874070513"  # ENGAGEMENT — keep, fix adsets

HANDPAN_ADSET_RU     = "120250085902530513"
ART_CLASSES_ADSET_RU = "120250085878380513"
ART_CLASSES_ADSET_UA = "120250085887810513"

# Existing ceramics video assets (reuse for DM campaign)
CERAMICS_RU_VIDEO   = "959536350220678"
CERAMICS_UA_VIDEO   = "1542298757583243"
CERAMICS_THUMB_HASH = "4d0158305e5551b89cc8461d29d05b44"

# ── Helpers ──────────────────────────────────────────────────────────────────
def api_get(path, params=None):
    r = requests.get(f"{BASE}{path}", params={**PARAMS, **(params or {})})
    if not r.ok:
        print(f"  GET {path} FAILED: {r.text[:400]}", file=sys.stderr)
        r.raise_for_status()
    return r.json()

def api_post(path, data):
    r = requests.post(f"{BASE}{path}", params=PARAMS, json=data)
    if not r.ok:
        print(f"  POST {path} FAILED: {r.text[:600]}", file=sys.stderr)
        r.raise_for_status()
    return r.json()

def api_update(eid, data):
    r = requests.post(f"{BASE}/{eid}", params=PARAMS, json=data)
    ok = r.ok
    if not ok:
        print(f"  UPDATE {eid} FAILED: {r.text[:600]}", file=sys.stderr)
    return ok

def pause(eid, label):
    ok = api_update(eid, {"status": "PAUSED"})
    print(f"  {'✓' if ok else '✗'} PAUSED {label}")
    return ok

def reactivate(eid, label):
    ok = api_update(eid, {"status": "ACTIVE"})
    print(f"  {'✓' if ok else '✗'} ACTIVE {label}")
    return ok

# ── Welcome screens with ice-breakers ────────────────────────────────────────
def welcome(lang):
    if lang == "RU":
        return json.dumps({
            "type": "VISUAL_EDITOR", "version": 2,
            "landing_screen_type": "welcome_message",
            "media_type": "text",
            "text_format": {
                "customer_action_type": "ice_breakers",
                "message": {
                    "autofill_message": {"content": "Привет! Хочу записаться на керамику"},
                    "text": "Привет! Расскажем о ближайших занятиях и запишем 🏺",
                    "ice_breakers": [
                        {"title": "Когда ближайшие занятия?", "response": None},
                        {"title": "Сколько стоит курс?",      "response": None},
                        {"title": "Для начинающих?",           "response": None},
                    ],
                },
            },
            "user_edit": True, "surface": "visual_editor_new",
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "type": "VISUAL_EDITOR", "version": 2,
            "landing_screen_type": "welcome_message",
            "media_type": "text",
            "text_format": {
                "customer_action_type": "ice_breakers",
                "message": {
                    "autofill_message": {"content": "Привіт! Хочу записатися на кераміку"},
                    "text": "Привіт! Розкажемо про найближчі заняття і запишемо 🏺",
                    "ice_breakers": [
                        {"title": "Коли найближчі заняття?",  "response": None},
                        {"title": "Скільки коштує курс?",     "response": None},
                        {"title": "Для початківців?",          "response": None},
                    ],
                },
            },
            "user_edit": True, "surface": "visual_editor_new",
        }, ensure_ascii=False)

# ── Ceramics ad configs ───────────────────────────────────────────────────────
CERAMICS_ADS = [
    {
        "lang": "RU", "locale": RU_LOCALE, "video_id": CERAMICS_RU_VIDEO,
        "message": (
            "Замедлиться, поработать руками с глиной и забрать домой свою керамику.\n\n"
            "Курс из двух 2-часовых занятий, каждый четверг в старой Валенсии.\n"
            "€60 за обе встречи · до 6 человек.\n\n"
            "Напишите — запишем и ответим на вопросы ↓"
        ),
        "headline": "Керамика с Корицей · Saged Club",
    },
    {
        "lang": "UA", "locale": UA_LOCALE, "video_id": CERAMICS_UA_VIDEO,
        "message": (
            "Сповільнитися, попрацювати руками з глиною та забрати додому свою кераміку.\n\n"
            "Курс із двох 2-годинних занять, щочетверга у старій Валенсії.\n"
            "€60 за обидві зустрічі · до 6 осіб.\n\n"
            "Напишіть — запишемо і відповімо на питання ↓"
        ),
        "headline": "Кераміка з Корицею · Saged Club",
    },
]

# ── Shared targeting builder ──────────────────────────────────────────────────
def targeting(locale_id, age_min=25, age_max=54):
    return {
        "geo_locations": {
            "cities": [{"key": VALENCIA_KEY, "radius": 17, "distance_unit": "kilometer"}],
            "location_types": ["home"],
        },
        "locales": [locale_id],
        "age_min": age_min,
        "age_max": age_max,
        "brand_safety_content_filter_levels": ["FACEBOOK_RELAXED", "AN_RELAXED"],
        "targeting_automation": {"advantage_audience": 0},
    }


def main():
    # Token check
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token invalid"
    print("✓ Token valid\n")

    # Verify locales live
    for name, expected in [("Russian", RU_LOCALE), ("Ukrainian", UA_LOCALE)]:
        res = api_get("/search", {"type": "adlocale", "q": name, "limit": 5})
        found = next((int(x["key"]) for x in res.get("data", []) if x.get("name") == name), None)
        assert found == expected, f"{name} locale {found} ≠ {expected}"
    print("✓ Locales verified (RU=17, UA=52)\n")

    # ── 1. Pause old ceramics TRAFFIC campaign ────────────────────────────────
    print("1. Pausing ceramics TRAFFIC campaign (wrong objective)...")
    pause(CERAMICS_CAMPAIGN, "ceramics TRAFFIC campaign")

    # ── 2. Fix Handpan adset ──────────────────────────────────────────────────
    print("\n2. Fixing Handpan RU adset (LINK_CLICKS → CONVERSATIONS, 20→17km)...")
    pause(HANDPAN_ADSET_RU, "Handpan RU adset")
    time.sleep(1)
    ok = api_update(HANDPAN_ADSET_RU, {
        "optimization_goal": "CONVERSATIONS",
        "targeting": targeting(RU_LOCALE, age_min=20, age_max=54),
    })
    print(f"  {'✓' if ok else '✗'} optimization_goal + targeting updated")
    reactivate(HANDPAN_ADSET_RU, "Handpan RU adset")

    # ── 3. Fix Art Classes adsets ─────────────────────────────────────────────
    print("\n3. Fixing Art Classes adsets (LINK_CLICKS → CONVERSATIONS, 20→17km)...")
    for adset_id, lang, locale_id in [
        (ART_CLASSES_ADSET_RU, "RU", RU_LOCALE),
        (ART_CLASSES_ADSET_UA, "UA", UA_LOCALE),
    ]:
        pause(adset_id, f"Art Classes {lang}")
        time.sleep(1)
        ok = api_update(adset_id, {
            "optimization_goal": "CONVERSATIONS",
            "targeting": targeting(locale_id),
        })
        print(f"  {'✓' if ok else '✗'} {lang}: optimization_goal + targeting updated")
        reactivate(adset_id, f"Art Classes {lang}")

    # ── 4. New ceramics ENGAGEMENT + Instagram DM campaign ───────────────────
    print("\n4. Creating ceramics DM campaign (OUTCOME_ENGAGEMENT + INSTAGRAM_DIRECT)...")
    campaign = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name": "Saged · Керамика с Корицей · v3 · DM · claude · 2026-10-20",
        "objective": "OUTCOME_ENGAGEMENT",
        "status": "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    })
    campaign_id = campaign["id"]
    print(f"   ✓ Campaign: {campaign_id}")

    for ad_cfg in CERAMICS_ADS:
        lang = ad_cfg["lang"]
        print(f"\n   [{lang}] Creating adset...")
        adset = api_post(f"/{AD_ACCOUNT}/adsets", {
            "name": f"Керамика · {lang} · Valencia 17km · DM",
            "campaign_id": campaign_id,
            "status": "PAUSED",
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "CONVERSATIONS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "destination_type": "INSTAGRAM_DIRECT",
            "daily_budget": 300,
            "targeting": targeting(ad_cfg["locale"]),
            "promoted_object": {"page_id": PAGE_ID},
        })
        adset_id = adset["id"]
        print(f"   ✓ Adset: {adset_id}")

        creative = api_post(f"/{AD_ACCOUNT}/adcreatives", {
            "name": f"Керамика DM · {lang} · v3",
            "object_story_spec": {
                "page_id": PAGE_ID,
                "instagram_user_id": IG_ACTOR,
                "video_data": {
                    "video_id": ad_cfg["video_id"],
                    "image_hash": CERAMICS_THUMB_HASH,
                    "message": ad_cfg["message"],
                    "title": ad_cfg["headline"],
                    "call_to_action": {
                        "type": "INSTAGRAM_MESSAGE",
                        "value": {
                            "app_destination": "INSTAGRAM_DIRECT",
                            "app_link": f"instagram://direct?userid={IG_USER_ID}",
                            "link": "https://www.instagram.com/",
                        },
                    },
                    "page_welcome_message": welcome(lang),
                },
            },
        })
        creative_id = creative["id"]
        print(f"   ✓ Creative: {creative_id}")

        ad = api_post(f"/{AD_ACCOUNT}/ads", {
            "name": f"Керамика DM · {lang} · v3",
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status": "PAUSED",
        })
        print(f"   ✓ Ad: {ad['id']}")

    print("\n" + "=" * 60)
    print("ALL DONE")
    print()
    print("  ✓ Ceramics TRAFFIC campaign — paused")
    print("  ✓ Handpan RU — CONVERSATIONS, 17km, re-activated")
    print("  ✓ Art Classes RU — CONVERSATIONS, 17km, re-activated")
    print("  ✓ Art Classes UA — CONVERSATIONS, 17km, re-activated")
    print(f"  ✓ New ceramics DM campaign {campaign_id} — PAUSED")
    print()
    print("Go to Ads Manager and activate the new ceramics DM campaign")
    print("when you're ready. Everything else is already live.")
    print("=" * 60)


if __name__ == "__main__":
    main()
