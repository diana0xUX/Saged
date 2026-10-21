#!/usr/bin/env python3
"""
Launch 4-language workshop video ads: RU, UA, EN, ES.

Uploads videos → creates campaign → 4 ad sets → 4 ads, all PAUSED.
Diana flips to ACTIVE in Ads Manager after review.

Usage:
    python3 scripts/launch-workshop-video-ads.py --dry-run
    python3 scripts/launch-workshop-video-ads.py
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
IDS_PATH = ROOT / ".campaign-ids"

# ---------- config ----------

CAMPAIGN_NAME = "Saged · Workshops · All Languages · Jul 2026"
PAGE_ID       = "373458682506494"
IG_USER_ID    = "17841428554040839"
ACCOUNT       = "act_484884320671439"
API_VERSION   = "v25.0"
GRAPH         = f"https://graph.facebook.com/{API_VERSION}"
GRAPH_VIDEO   = f"https://graph-video.facebook.com/{API_VERSION}"

VALENCIA = {
    "key": "668776",
    "country": "ES",
    "radius": 17,
    "distance_unit": "kilometer",
}

VIDEOS = {
    "ru": Path("/Users/diana/Downloads/IMG_0625.MOV"),
    "ua": Path("/Users/diana/Downloads/IMG_0622.MOV"),
    "en": Path("/Users/diana/Downloads/IMG_0623.MOV"),
    "es": Path("/Users/diana/Downloads/IMG_0624.MOV"),
}

AD_SETS = {
    "ru": {
        "name":               "Workshops · RU · Valencia 17km",
        "locale_name":        "Russian",
        "locale_expected_id": 17,
        "daily_budget_cents": 150,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Керамика каждый четверг в Валенсии. Маленькая группа — до 6 человек. Все материалы включены. Запись — в директ.",
        "headline":      "Керамика в Saged.club",
        "link":          "https://saged.club",
    },
    "ua": {
        "name":               "Workshops · UA · Valencia 17km",
        "locale_name":        "Ukrainian",
        "locale_expected_id": 52,
        "daily_budget_cents": 200,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Кераміка щочетверга у Валенсії. Мала група — до 6 осіб. Усі матеріали включені. Запис — у директ.",
        "headline":      "Кераміка у Saged.club",
        "link":          "https://saged.club/ua/",
    },
    "en": {
        "name":               "Workshops · EN · Valencia 17km",
        "locale_name":        "English (UK)",
        "locale_expected_id": 24,
        "daily_budget_cents": 80,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Ceramics every Thursday in Valencia. Small group, up to 6 people. All materials included. Book via DM.",
        "headline":      "Ceramics at Saged.club",
        "link":          "https://saged.club/en/",
    },
    "es": {
        "name":               "Workshops · ES · Valencia 17km",
        "locale_name":        "Spanish (Spain)",
        "locale_expected_id": 23,
        "daily_budget_cents": 80,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Cerámica todos los jueves en Valencia. Grupo pequeño, hasta 6 personas. Todos los materiales incluidos. Reserva por DM.",
        "headline":      "Cerámica en Saged.club",
        "link":          "https://saged.club",
    },
}

# ---------- helpers ----------

def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env

def api_get(token, path, **params):
    params["access_token"] = token
    url = f"{GRAPH}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())

def api_post(token, path, data, dry_run=False):
    data["access_token"] = token
    print(f"  POST /{path}")
    if dry_run:
        print(f"  payload: {json.dumps({k:v for k,v in data.items() if k!='access_token'}, ensure_ascii=False, indent=2)}")
        return {"id": f"DRY_{path}_{uuid.uuid4().hex[:6]}"}
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(f"{GRAPH}/{path}", data=encoded, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR {e.code}: {body[:600]}", file=sys.stderr)
        sys.exit(1)

def verify_locale(token, locale_name, expected_id):
    """Mandatory: verify locale ID against Meta API. Exits if mismatch."""
    print(f"  verifying locale '{locale_name}' → expected id {expected_id} …")
    data = api_get(token, "search", type="adlocale", q=locale_name.split("(")[0].strip(), limit=20)
    for item in data.get("data", []):
        if str(item.get("key")) == str(expected_id):
            print(f"  ✓ confirmed: '{item['name']}' = {expected_id}")
            return expected_id
    print(f"  ERROR: locale id {expected_id} not found for '{locale_name}'", file=sys.stderr)
    print(f"  API returned: {json.dumps(data.get('data', [])[:5])}", file=sys.stderr)
    sys.exit(1)

def upload_video(token, file_path, name, dry_run=False):
    """Upload a video file to Meta ad videos. Returns video_id."""
    print(f"  uploading {file_path.name} ({file_path.stat().st_size // 1024 // 1024}MB) …")
    if dry_run:
        fake_id = f"DRY_VIDEO_{uuid.uuid4().hex[:8]}"
        print(f"  [dry-run] would upload → {fake_id}")
        return fake_id

    boundary = uuid.uuid4().hex
    with open(file_path, "rb") as f:
        video_bytes = f.read()

    parts = []
    # name field
    parts.append((
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f"{name}\r\n"
    ).encode())
    # file field
    parts.append((
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="source"; filename="{file_path.name}"\r\n'
        f"Content-Type: video/quicktime\r\n\r\n"
    ).encode())
    parts.append(video_bytes)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    # access_token field (inject before closing)
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="access_token"\r\n\r\n'
        f"{token}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="name"\r\n\r\n'
        f"{name}\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="source"; filename="{file_path.name}"\r\n'
        f"Content-Type: video/quicktime\r\n\r\n"
    ).encode() + video_bytes + f"\r\n--{boundary}--\r\n".encode()

    url = f"{GRAPH_VIDEO}/{ACCOUNT}/advideos"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            result = json.loads(r.read())
            video_id = result.get("id")
            print(f"  ✓ uploaded → video_id {video_id}")
            return video_id
    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR uploading video: {e.code} {body_err[:600]}", file=sys.stderr)
        sys.exit(1)

# ---------- main ----------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dry = args.dry_run

    if dry:
        print("=== DRY RUN — no API writes ===\n")

    env = load_env()
    token = env["META_ACCESS_TOKEN"]

    # 1. Verify all locales first (mandatory project rule)
    print("── Step 1: Verify locales ──")
    verified_locales = {}
    for lang, cfg in AD_SETS.items():
        verified_locales[lang] = verify_locale(token, cfg["locale_name"], cfg["locale_expected_id"])
    print()

    # 2. Upload videos
    print("── Step 2: Upload videos ──")
    video_ids = {}
    for lang, path in VIDEOS.items():
        video_ids[lang] = upload_video(token, path, f"Saged Workshop {lang.upper()} Jul 2026", dry_run=dry)
        if not dry:
            time.sleep(2)  # be gentle with the API
    print()

    # 3. Create campaign
    print("── Step 3: Create campaign ──")
    campaign = api_post(token, f"{ACCOUNT}/campaigns", {
        "name":      CAMPAIGN_NAME,
        "objective": "OUTCOME_TRAFFIC",
        "status":    "PAUSED",
        "special_ad_categories": "[]",
        "is_adset_budget_sharing_enabled": "false",
    }, dry_run=dry)
    campaign_id = campaign["id"]
    print(f"  ✓ campaign → {campaign_id}\n")

    # 4. Create ad sets
    print("── Step 4: Create ad sets ──")
    adset_ids = {}
    for lang, cfg in AD_SETS.items():
        locale_id = verified_locales[lang]
        targeting = {
            "geo_locations": {
                "cities": [VALENCIA],
                "location_types": ["home"],
            },
            "locales": [locale_id],
            "age_min": cfg["age_min"],
            "age_max": cfg["age_max"],
        }
        adset = api_post(token, f"{ACCOUNT}/adsets", {
            "name":               cfg["name"],
            "campaign_id":        campaign_id,
            "daily_budget":       str(cfg["daily_budget_cents"]),
            "billing_event":      "IMPRESSIONS",
            "optimization_goal":  "LINK_CLICKS",
            "targeting":          json.dumps(targeting),
            "status":             "PAUSED",
            "destination_type":   "WEBSITE",
        }, dry_run=dry)
        adset_ids[lang] = adset["id"]
        print(f"  ✓ {lang.upper()} ad set → {adset['id']}")
    print()

    # 5. Create ad creatives + ads
    print("── Step 5: Create ads ──")
    ad_ids = {}
    for lang, cfg in AD_SETS.items():
        # Creative
        creative_spec = {
            "video_data": {
                "video_id":    video_ids[lang],
                "title":       cfg["headline"],
                "message":     cfg["primary_text"],
                "call_to_action": json.dumps({
                    "type":  "LEARN_MORE",
                    "value": {"link": cfg["link"]},
                }),
            },
        }
        object_story_spec = {
            "page_id":            PAGE_ID,
            "instagram_user_id":  IG_USER_ID,
            "video_data": {
                "video_id":    video_ids[lang],
                "title":       cfg["headline"],
                "message":     cfg["primary_text"],
                "call_to_action": {
                    "type":  "LEARN_MORE",
                    "value": {"link": cfg["link"]},
                },
            },
        }
        creative = api_post(token, f"{ACCOUNT}/adcreatives", {
            "name":               f"Saged Workshop Video {lang.upper()}",
            "object_story_spec":  json.dumps(object_story_spec),
        }, dry_run=dry)
        creative_id = creative["id"]

        # Ad
        ad = api_post(token, f"{ACCOUNT}/ads", {
            "name":       f"Workshops · {lang.upper()} · Video Jul 2026",
            "adset_id":   adset_ids[lang],
            "creative":   json.dumps({"creative_id": creative_id}),
            "status":     "PAUSED",
        }, dry_run=dry)
        ad_ids[lang] = ad["id"]
        print(f"  ✓ {lang.upper()} ad → {ad['id']}")
    print()

    # 6. Summary
    print("── Done ──")
    print(f"Campaign: {campaign_id}")
    for lang in AD_SETS:
        budget_eur = AD_SETS[lang]["daily_budget_cents"] / 100
        print(f"  {lang.upper()}: ad set {adset_ids[lang]} · ad {ad_ids[lang]} · €{budget_eur:.2f}/day")
    print()
    print("All created as PAUSED. Review in Ads Manager, then flip to ACTIVE.")
    print(f"Total budget when active: €5.00/day")

    if not dry:
        # Save IDs
        existing = IDS_PATH.read_text() if IDS_PATH.exists() else ""
        lines = [
            f"\n# Workshop Video Ads · Jul 2026",
            f"WORKSHOP_VIDEO_CAMPAIGN_ID={campaign_id}",
        ]
        for lang in AD_SETS:
            lines.append(f"WORKSHOP_ADSET_{lang.upper()}_ID={adset_ids[lang]}")
            lines.append(f"WORKSHOP_AD_{lang.upper()}_ID={ad_ids[lang]}")
        IDS_PATH.write_text(existing + "\n".join(lines) + "\n")
        print(f"\nIDs saved to .campaign-ids")

if __name__ == "__main__":
    main()
