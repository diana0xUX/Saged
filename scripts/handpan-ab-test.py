#!/usr/bin/env python3
"""
Handpan School A/B Test — Russian audience, Valencia
Campaign A: Click-to-WhatsApp  (OUTCOME_ENGAGEMENT → conversations)
Campaign B: Traffic to landing  (OUTCOME_TRAFFIC → landing page views)

Same video, same audience, same budget, different CTA.
All entities created PAUSED — activate both at the same time.

Run:  python3 scripts/handpan-ab-test.py
      python3 scripts/handpan-ab-test.py --dry-run  (verify + skip API writes)
"""

import json, sys, time, argparse
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

# ── Geo / locale (verified at runtime — never trust these without the API check)
VALENCIA_KEY = 699854   # Valencia, Spain — verified below
RU_LOCALE    = 17       # Russian — verified below

# ── Budget: €2/day each = €4/day total = ~€120/month
DAILY_BUDGET_CENTS = 350  # 350 = €3.50 (Meta minimum is ~€2.68)

# ── Video
VIDEO_PATH = "/Users/diana/Downloads/handpan_school_captions.MP4"

# ── Copy
BODY_A = (
    "Хочешь научиться играть на хэндпане? 🎶\n\n"
    "Занятия каждое воскресенье в Saged Club, старый город Валенсии. "
    "Инструменты — наши. Опыт — не нужен. Группа до 5 человек.\n\n"
    "Напиши нам — расскажем подробнее и запишем ↓"
)
HEADLINE_A = "Handpan School — напиши нам"

BODY_B = (
    "Хочешь научиться играть на хэндпане? 🎶\n\n"
    "Занятия каждое воскресенье в Saged Club, старый город Валенсии. "
    "Инструменты — наши. Опыт — не нужен. Группа до 5 человек.\n\n"
    "Первое занятие €25 — запись онлайн за минуту ↓"
)
HEADLINE_B = "Handpan School — записаться онлайн"
LANDING_URL = "https://saged.club/handpan/"

WELCOME_MSG = json.dumps({
    "type": "VISUAL_EDITOR",
    "version": 2,
    "landing_screen_type": "welcome_message",
    "media_type": "text",
    "text_format": {
        "customer_action_type": "ice_breakers",
        "message": {
            "autofill_message": {"content": "Привет! Хочу узнать о занятиях по хэндпану"},
            "text": "Привет! Чем можем помочь?",
            "ice_breakers": [
                {"title": "Когда ближайшее занятие?", "response": None},
                {"title": "Нужен ли свой инструмент?", "response": None},
                {"title": "Сколько стоит занятие?", "response": None},
            ],
        },
    },
    "user_edit": True,
    "surface": "visual_editor_new",
}, ensure_ascii=False)

TARGETING = {
    "geo_locations": {
        "cities": [{"key": VALENCIA_KEY, "radius": 17, "distance_unit": "kilometer"}],
        "location_types": ["home"],
    },
    "locales": [RU_LOCALE],
    "age_min": 22,
    "age_max": 52,
    "targeting_automation": {"advantage_audience": 0},
}


# ── Helpers ───────────────────────────────────────────────────────────────────
def api_get(path, params=None):
    r = requests.get(f"{BASE}{path}", params={**PARAMS, **(params or {})})
    r.raise_for_status()
    return r.json()


def api_post(path, data, dry_run=False):
    if dry_run:
        print(f"    [dry-run] POST {path}")
        return {"id": "DRY_RUN"}
    r = requests.post(f"{BASE}{path}", params=PARAMS, json=data)
    if not r.ok:
        print(f"  POST {path} FAILED:\n{r.text[:800]}")
        r.raise_for_status()
    return r.json()


def verify_locale(name: str, expected_id: int):
    res = api_get("/search", {"type": "adlocale", "q": name, "limit": 10})
    actual = next((int(x["key"]) for x in res.get("data", []) if x["name"].lower() == name.lower()), None)
    if actual != expected_id:
        sys.exit(f"FATAL: locale '{name}' → {actual}, expected {expected_id}. Fix before re-running.")
    print(f"   ✓ {name} locale = {actual}")


def verify_city_key(city: str, country: str, expected_key: int):
    res = api_get("/search", {"type": "adgeolocation", "q": city,
                              "location_types": '["city"]', "limit": 20})
    match = next(
        (x for x in res.get("data", [])
         if x["name"].lower() == city.lower() and x.get("country_code") == country),
        None,
    )
    if not match:
        sys.exit(f"FATAL: city '{city}, {country}' not found via Meta API.")
    actual_key = int(match["key"])
    if actual_key != expected_key:
        sys.exit(f"FATAL: city key for '{city}, {country}' = {actual_key}, expected {expected_key}.")
    print(f"   ✓ {city}, {country} city key = {actual_key}")


def upload_video(path: str, dry_run=False) -> str:
    if dry_run:
        print("   [dry-run] skipping video upload")
        return "DRY_RUN_VIDEO_ID"
    print(f"   Uploading {path} ...")
    with open(path, "rb") as f:
        r = requests.post(
            f"{BASE}/{AD_ACCOUNT}/advideos",
            params=PARAMS,
            files={"source": (Path(path).name, f, "video/mp4")},
            data={"name": "Handpan School A/B — captions video"},
        )
    if not r.ok:
        sys.exit(f"Video upload failed: {r.text[:600]}")
    video_id = r.json()["id"]
    print(f"   ✓ Uploaded → video_id: {video_id}")
    return video_id


def poll_video_ready(video_id: str, dry_run=False):
    if dry_run or video_id == "DRY_RUN_VIDEO_ID":
        return
    print(f"   Waiting for video {video_id} to finish processing...")
    for _ in range(24):  # up to 2 min
        data = api_get(f"/{video_id}", {"fields": "status"})
        status = data.get("status", {}).get("video_status", "unknown")
        if status == "ready":
            print("   ✓ Video ready")
            return
        print(f"     status: {status} — retrying in 5s")
        time.sleep(5)
    sys.exit("FATAL: video not ready after 2 minutes.")


def make_campaign(name: str, objective: str, dry_run=False) -> str:
    result = api_post(f"/{AD_ACCOUNT}/campaigns", {
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": [],
        "is_adset_budget_sharing_enabled": False,
    }, dry_run)
    return result["id"]


def make_adset(name: str, campaign_id: str, destination_type: str,
               optimization_goal: str, dry_run=False) -> str:
    result = api_post(f"/{AD_ACCOUNT}/adsets", {
        "name": name,
        "campaign_id": campaign_id,
        "status": "PAUSED",
        "billing_event": "IMPRESSIONS",
        "optimization_goal": optimization_goal,
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "destination_type": destination_type,
        "daily_budget": DAILY_BUDGET_CENTS,
        "targeting": TARGETING,
        "promoted_object": {"page_id": PAGE_ID},
    }, dry_run)
    return result["id"]


THUMBNAIL_URL = "https://saged.club/oct/saged-handpan-school-hero.png"


def make_video_creative(name: str, video_id: str, headline: str,
                        body: str, cta: dict, dry_run=False) -> str:
    result = api_post(f"/{AD_ACCOUNT}/adcreatives", {
        "name": name,
        "object_story_spec": {
            "page_id": PAGE_ID,
            "video_data": {
                "video_id": video_id,
                "image_url": THUMBNAIL_URL,
                "title": headline,
                "message": body,
                "call_to_action": cta,
                **({"page_welcome_message": WELCOME_MSG}
                   if cta["type"] == "WHATSAPP_MESSAGE" else {}),
            },
        },
    }, dry_run)
    return result["id"]


def make_ad(name: str, adset_id: str, creative_id: str, dry_run=False) -> str:
    result = api_post(f"/{AD_ACCOUNT}/ads", {
        "name": name,
        "adset_id": adset_id,
        "creative": {"creative_id": creative_id},
        "status": "PAUSED",
    }, dry_run)
    return result["id"]


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dry = args.dry_run

    print("=" * 60)
    print("Handpan School A/B Test — creating 2 campaigns PAUSED")
    if dry:
        print("DRY-RUN MODE — no changes will be written")
    print("=" * 60)

    # 1. Verify token
    print("\n1. Verifying token...")
    info = api_get("/debug_token", {"input_token": TOKEN})
    assert info.get("data", {}).get("is_valid"), "Token is invalid — refresh in Meta Business Suite"
    print("   ✓ Token valid")

    # 2. Verify locale + city key
    print("\n2. Verifying locale and geo...")
    verify_locale("Russian", RU_LOCALE)
    verify_city_key("Valencia", "ES", VALENCIA_KEY)

    # 3. Upload video (single upload — 23 MB is well within the 1 GB limit)
    print("\n3. Uploading video...")
    video_id = upload_video(VIDEO_PATH, dry)
    poll_video_ready(video_id, dry)

    # ── Campaign A: WhatsApp messages ─────────────────────────────────────────
    print("\n4. Building Campaign A — Click to WhatsApp (OUTCOME_ENGAGEMENT)...")
    # NOTE: OUTCOME_ENGAGEMENT is correct here — it optimises for message conversations,
    # not likes. The CLAUDE.md rule against OUTCOME_ENGAGEMENT targets the "page engagement"
    # variant (reactions/shares), not click-to-message campaigns.
    camp_a = make_campaign("Saged · Handpan · RU · A — Message", "OUTCOME_ENGAGEMENT", dry)
    print(f"   Campaign A: {camp_a}")

    adset_a = make_adset(
        "Handpan · RU · Valencia · A — WhatsApp",
        camp_a,
        destination_type="WHATSAPP",
        optimization_goal="CONVERSATIONS",
        dry_run=dry,
    )
    print(f"   Ad set A:   {adset_a}")

    creative_a = make_video_creative(
        "Handpan · RU · A — Message creative",
        video_id, HEADLINE_A, BODY_A,
        cta={"type": "WHATSAPP_MESSAGE", "value": {"app_destination": "WHATSAPP"}},
        dry_run=dry,
    )
    print(f"   Creative A: {creative_a}")

    ad_a = make_ad("Handpan · RU · A — Message ad", adset_a, creative_a, dry)
    print(f"   Ad A:       {ad_a}")

    # ── Campaign B: Traffic to landing page ───────────────────────────────────
    print("\n5. Building Campaign B — Traffic to landing page (OUTCOME_TRAFFIC)...")
    camp_b = make_campaign("Saged · Handpan · RU · B — Traffic", "OUTCOME_TRAFFIC", dry)
    print(f"   Campaign B: {camp_b}")

    adset_b = make_adset(
        "Handpan · RU · Valencia · B — Website",
        camp_b,
        destination_type="WEBSITE",
        optimization_goal="LANDING_PAGE_VIEWS",
        dry_run=dry,
    )
    print(f"   Ad set B:   {adset_b}")

    creative_b = make_video_creative(
        "Handpan · RU · B — Traffic creative",
        video_id, HEADLINE_B, BODY_B,
        cta={"type": "LEARN_MORE", "value": {"link": LANDING_URL}},
        dry_run=dry,
    )
    print(f"   Creative B: {creative_b}")

    ad_b = make_ad("Handpan · RU · B — Traffic ad", adset_b, creative_b, dry)
    print(f"   Ad B:       {ad_b}")

    # ── Save IDs ──────────────────────────────────────────────────────────────
    ids_path = Path(__file__).resolve().parent.parent / ".handpan-ab-ids"
    if not dry:
        ids_path.write_text(
            f"VIDEO_ID={video_id}\n"
            f"CAMP_A={camp_a}\n"
            f"ADSET_A={adset_a}\n"
            f"CREATIVE_A={creative_a}\n"
            f"AD_A={ad_a}\n"
            f"CAMP_B={camp_b}\n"
            f"ADSET_B={adset_b}\n"
            f"CREATIVE_B={creative_b}\n"
            f"AD_B={ad_b}\n"
        )
        print(f"\n   IDs saved → {ids_path.name} (gitignored)")

    print("\n" + "=" * 60)
    print("DONE — all entities PAUSED")
    print()
    print("Next:")
    print("  1. Open Ads Manager and preview both ads")
    print("  2. Activate BOTH at the same time (fair test)")
    print(f"  3. Budget: €{DAILY_BUDGET_CENTS/100:.2f}/day each = €{DAILY_BUDGET_CENTS*2/100:.2f}/day total")
    print("  4. Check after 7 days: WhatsApp chats vs landing page visits")
    print("     Winner = whichever led to more actual bookings (check manually)")
    print("=" * 60)


if __name__ == "__main__":
    main()
