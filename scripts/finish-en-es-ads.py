#!/usr/bin/env python3
"""
Finish creating EN and ES ad sets + ads.
Campaign, RU, and UA are already created.

Run:
    python3 scripts/finish-en-es-ads.py --dry-run
    python3 scripts/finish-en-es-ads.py
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
IDS_PATH = ROOT / ".campaign-ids"

ACCOUNT     = "act_484884320671439"
PAGE_ID     = "373458682506494"
IG_USER_ID  = "17841428554040839"
API_VERSION = "v25.0"
GRAPH       = f"https://graph.facebook.com/{API_VERSION}"

CAMPAIGN_ID = "120248011297180513"

VALENCIA = {
    "key": "668776",
    "country": "ES",
    "radius": 17,
    "distance_unit": "kilometer",
}

VIDEO_IDS = {
    "en": "1730819618045834",
    "es": "1574793734274290",
}

AD_SETS = {
    "en": {
        "name":               "Workshops · EN · Valencia 17km",
        "locale_id":          24,
        "daily_budget_cents": 90,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Ceramics every Thursday in Valencia. Small group, up to 6 people. All materials included. Book via DM.",
        "headline":      "Ceramics at Saged.club",
        "link":          "https://saged.club/en/",
    },
    "es": {
        "name":               "Workshops · ES · Valencia 17km",
        "locale_id":          23,
        "daily_budget_cents": 90,
        "age_min": 24, "age_max": 55,
        "primary_text":  "Cerámica todos los jueves en Valencia. Grupo pequeño, hasta 6 personas. Todos los materiales incluidos. Reserva por DM.",
        "headline":      "Cerámica en Saged.club",
        "link":          "https://saged.club",
    },
}

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

def fetch_thumbnail(token, video_id):
    print(f"  fetching thumbnail for video {video_id} …")
    data = api_get(token, video_id, fields="thumbnails")
    thumbs = data.get("thumbnails", {}).get("data", [])
    if not thumbs:
        print("  ERROR: no thumbnails returned", file=sys.stderr)
        sys.exit(1)
    url = thumbs[0]["uri"]
    print(f"  ✓ thumbnail: {url[:80]}…")
    return url

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    dry = args.dry_run

    if dry:
        print("=== DRY RUN — no API writes ===\n")

    env = load_env()
    token = env["META_ACCESS_TOKEN"]

    adset_ids = {}
    ad_ids = {}

    for lang, cfg in AD_SETS.items():
        print(f"\n── {lang.upper()} ──")

        # 1. Fetch thumbnail
        thumb_url = fetch_thumbnail(token, VIDEO_IDS[lang]) if not dry else "https://example.com/thumb.jpg"

        # 2. Ad set
        targeting = {
            "geo_locations": {
                "cities": [VALENCIA],
                "location_types": ["home"],
            },
            "locales":  [cfg["locale_id"]],
            "age_min":  cfg["age_min"],
            "age_max":  cfg["age_max"],
            "targeting_automation": {"advantage_audience": 0},
        }
        adset = api_post(token, f"{ACCOUNT}/adsets", {
            "name":               cfg["name"],
            "campaign_id":        CAMPAIGN_ID,
            "daily_budget":       str(cfg["daily_budget_cents"]),
            "billing_event":      "IMPRESSIONS",
            "optimization_goal":  "LINK_CLICKS",
            "bid_strategy":       "LOWEST_COST_WITHOUT_CAP",
            "targeting":          json.dumps(targeting),
            "status":             "PAUSED",
            "destination_type":   "WEBSITE",
        }, dry_run=dry)
        adset_ids[lang] = adset["id"]
        print(f"  ✓ ad set → {adset['id']}")

        # 3. Creative
        object_story_spec = {
            "page_id":           PAGE_ID,
            "instagram_user_id": IG_USER_ID,
            "video_data": {
                "video_id":  VIDEO_IDS[lang],
                "title":     cfg["headline"],
                "message":   cfg["primary_text"],
                "image_url": thumb_url,
                "call_to_action": {
                    "type":  "LEARN_MORE",
                    "value": {"link": cfg["link"]},
                },
            },
        }
        creative = api_post(token, f"{ACCOUNT}/adcreatives", {
            "name":              f"Saged Workshop Video {lang.upper()}",
            "object_story_spec": json.dumps(object_story_spec),
        }, dry_run=dry)
        creative_id = creative["id"]
        print(f"  ✓ creative → {creative_id}")

        # 4. Ad
        ad = api_post(token, f"{ACCOUNT}/ads", {
            "name":     f"Workshops · {lang.upper()} · Video Jul 2026",
            "adset_id": adset_ids[lang],
            "creative": json.dumps({"creative_id": creative_id}),
            "status":   "PAUSED",
        }, dry_run=dry)
        ad_ids[lang] = ad["id"]
        print(f"  ✓ ad → {ad['id']}")

    print("\n── Done ──")
    for lang in AD_SETS:
        budget_eur = AD_SETS[lang]["daily_budget_cents"] / 100
        print(f"  {lang.upper()}: ad set {adset_ids[lang]} · ad {ad_ids[lang]} · €{budget_eur:.2f}/day")

    print("\nAll created as PAUSED. Review in Ads Manager, then flip to ACTIVE.")

    if not dry:
        existing = IDS_PATH.read_text() if IDS_PATH.exists() else ""
        lines = []
        for lang in AD_SETS:
            lines.append(f"WORKSHOP_ADSET_{lang.upper()}_ID={adset_ids[lang]}")
            lines.append(f"WORKSHOP_AD_{lang.upper()}_ID={ad_ids[lang]}")
        IDS_PATH.write_text(existing + "\n".join(lines) + "\n")
        print(f"IDs appended to .campaign-ids")

if __name__ == "__main__":
    main()
