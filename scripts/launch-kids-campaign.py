#!/usr/bin/env python3
"""Launch the Kids Trial Class Meta campaign via API.

Builds: 1 campaign (OUTCOME_TRAFFIC) + 2 ad sets (RU/UA) + 2 ads, all PAUSED.
Diana flips to ACTIVE in Ads Manager after review.

Idempotent: refuses to run if KIDS_CAMPAIGN_ID already in .campaign-ids.

Usage:
    python3 scripts/launch-kids-campaign.py --dry-run    # print payloads, no POST
    python3 scripts/launch-kids-campaign.py              # actually create
"""

import argparse
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
IDS_PATH = ROOT / ".campaign-ids"

CAMPAIGN_NAME = "Saged · Kids Trial · 2026-05"
PAGE_ID = "373458682506494"
INSTAGRAM_USER_ID = "17841428554040839"

START_TIME = "2026-05-29T09:00:00+0200"
END_TIME = "2026-06-12T09:00:00+0200"

VALENCIA_CITY = {
    "key": "699854",
    "country": "ES",
    "radius": 17,
    "distance_unit": "kilometer",
}

PARENT_FAMILY_STATUSES = [
    {"id": "6023005570783", "name": "Parents with early school-age children (06-08 years)"},
    {"id": "6023080302983", "name": "Parents with preteens (09-12 years)"},
]

LOCALE_RU = 17
LOCALE_UA = 52

AD_SETS = {
    "ru": {
        "name": "Kids · RU · Valencia 17km",
        "locale": LOCALE_RU,
        "daily_budget_cents": 200,
        "image_path": ROOT / "assets/images/ad-kids-ru-4x5.png",
        "primary_text": (
            "Полуторачасовой класс лепки для детей 6–10 лет с украинской "
            "керамисткой Корицей. Ребёнок уйдёт с готовой керамикой в тот же "
            "день. Маленькая группа в старой Валенсии. 25 €."
        ),
        "headline": "Керамика для детей · 25 €",
        "description": "Старая Валенсия · 1,5 часа",
        "link": (
            "https://saged.club/kids/"
            "?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=ru"
        ),
        "ad_name": "Kids · RU · v1",
    },
    "ua": {
        "name": "Kids · UA · Valencia 17km",
        "locale": LOCALE_UA,
        "daily_budget_cents": 300,
        "image_path": ROOT / "assets/images/ad-kids-ua-4x5.png",
        "primary_text": (
            "Півторагодинний клас ліплення для дітей 6–10 років з українською "
            "керамісткою Корицею. Дитина забере готову кераміку додому того ж "
            "дня. Маленька група у старій Валенсії. 25 €."
        ),
        "headline": "Кераміка для дітей · 25 €",
        "description": "Стара Валенсія · 1,5 години",
        "link": (
            "https://saged.club/uk/kids/"
            "?utm_source=meta&utm_medium=paid&utm_campaign=kids-trial&utm_content=uk"
        ),
        "ad_name": "Kids · UA · v1",
    },
}


def load_env() -> dict:
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def load_campaign_ids() -> dict:
    if not IDS_PATH.exists():
        return {}
    out = {}
    for line in IDS_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    return out


def append_campaign_ids(new_ids: dict) -> None:
    with IDS_PATH.open("a") as fh:
        fh.write("\n# Kids campaign launched 2026-05-28\n")
        for k, v in new_ids.items():
            fh.write(f"{k}={v}\n")


def graph_url(version: str, path: str) -> str:
    return f"https://graph.facebook.com/{version}/{path.lstrip('/')}"


def api_post(url: str, payload: dict, token: str, dry_run: bool) -> dict:
    body = dict(payload)
    body["access_token"] = token
    if dry_run:
        print(f"[DRY] POST {url}")
        print(f"      payload: {json.dumps({k: v for k, v in payload.items() if k != 'access_token'}, ensure_ascii=False)[:500]}")
        return {"id": f"DRY_{uuid.uuid4().hex[:12]}"}
    data = urllib.parse.urlencode(body, doseq=True).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"\nHTTP {e.code} from POST {url}\n{body_text}\n")
        raise


def api_post_multipart(url: str, fields: dict, file_field: str, file_path: Path, token: str, dry_run: bool) -> dict:
    if dry_run:
        print(f"[DRY] POST {url} (multipart, file={file_path.name})")
        return {"images": {file_path.name: {"hash": f"DRY_HASH_{uuid.uuid4().hex[:16]}"}}}
    boundary = f"----saged{uuid.uuid4().hex}"
    body = bytearray()
    for k, v in {**fields, "access_token": token}.items():
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'.encode()
    body += f"Content-Type: {mime}\r\n\r\n".encode()
    body += file_path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=bytes(body), method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"\nHTTP {e.code} from POST {url}\n{body_text}\n")
        raise


def create_campaign(version: str, ad_account: str, token: str, dry_run: bool) -> str:
    url = graph_url(version, f"act_{ad_account}/campaigns")
    payload = {
        "name": CAMPAIGN_NAME,
        "objective": "OUTCOME_TRAFFIC",
        "status": "PAUSED",
        "buying_type": "AUCTION",
        "special_ad_categories": json.dumps([]),
        "is_adset_budget_sharing_enabled": "false",
    }
    resp = api_post(url, payload, token, dry_run)
    return resp["id"]


def create_ad_set(version: str, ad_account: str, token: str, campaign_id: str, spec: dict, dry_run: bool) -> str:
    url = graph_url(version, f"act_{ad_account}/adsets")
    targeting = {
        "age_min": 28,
        "age_max": 45,
        "geo_locations": {
            "cities": [VALENCIA_CITY],
            "location_types": ["home"],
        },
        "locales": [spec["locale"]],
        "flexible_spec": [{"family_statuses": PARENT_FAMILY_STATUSES}],
        "targeting_automation": {"advantage_audience": 0},
    }
    payload = {
        "name": spec["name"],
        "campaign_id": campaign_id,
        "status": "PAUSED",
        "daily_budget": spec["daily_budget_cents"],
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LANDING_PAGE_VIEWS",
        "destination_type": "WEBSITE",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "start_time": START_TIME,
        "end_time": END_TIME,
        "targeting": json.dumps(targeting),
    }
    resp = api_post(url, payload, token, dry_run)
    return resp["id"]


def upload_image(version: str, ad_account: str, token: str, image_path: Path, dry_run: bool) -> str:
    url = graph_url(version, f"act_{ad_account}/adimages")
    resp = api_post_multipart(url, {}, image_path.name, image_path, token, dry_run)
    return resp["images"][image_path.name]["hash"]


def create_creative(version: str, ad_account: str, token: str, spec: dict, image_hash: str, dry_run: bool) -> str:
    url = graph_url(version, f"act_{ad_account}/adcreatives")
    object_story_spec = {
        "page_id": PAGE_ID,
        "instagram_user_id": INSTAGRAM_USER_ID,
        "link_data": {
            "image_hash": image_hash,
            "link": spec["link"],
            "message": spec["primary_text"],
            "name": spec["headline"],
            "description": spec["description"],
            "call_to_action": {
                "type": "LEARN_MORE",
                "value": {"link": spec["link"]},
            },
        },
    }
    payload = {
        "name": f"{spec['ad_name']} · creative",
        "object_story_spec": json.dumps(object_story_spec, ensure_ascii=False),
    }
    resp = api_post(url, payload, token, dry_run)
    return resp["id"]


def create_ad(version: str, ad_account: str, token: str, name: str, adset_id: str, creative_id: str, dry_run: bool) -> str:
    url = graph_url(version, f"act_{ad_account}/ads")
    payload = {
        "name": name,
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
    }
    resp = api_post(url, payload, token, dry_run)
    return resp["id"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="Print payloads without POSTing")
    args = parser.parse_args()

    env = load_env()
    token = env.get("META_ACCESS_TOKEN")
    ad_account_raw = env.get("META_AD_ACCOUNT_ID", "")
    ad_account = ad_account_raw[4:] if ad_account_raw.startswith("act_") else ad_account_raw
    version = env.get("META_API_VERSION", "v25.0")
    if not token or not ad_account:
        sys.stderr.write("Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID in .env\n")
        return 1

    existing = load_campaign_ids()
    if "KIDS_CAMPAIGN_ID" in existing and not args.dry_run:
        sys.stderr.write(
            f"Refusing to rebuild: KIDS_CAMPAIGN_ID={existing['KIDS_CAMPAIGN_ID']} already in .campaign-ids.\n"
            "Pause the existing campaign and remove the line if you really want to recreate.\n"
        )
        return 2

    for spec in AD_SETS.values():
        if not spec["image_path"].exists():
            sys.stderr.write(f"Missing image: {spec['image_path']}\n")
            return 3

    print(f"=== Launching kids campaign {'(DRY RUN)' if args.dry_run else ''} ===")
    print(f"Ad account: act_{ad_account}  · API: {version}")
    print(f"Start: {START_TIME}  · End: {END_TIME}")
    print()

    campaign_id = create_campaign(version, ad_account, token, args.dry_run)
    print(f"campaign: {campaign_id}  ({CAMPAIGN_NAME})")

    new_ids = {"KIDS_CAMPAIGN_ID": campaign_id}

    for lang, spec in AD_SETS.items():
        L = lang.upper()
        adset_id = create_ad_set(version, ad_account, token, campaign_id, spec, args.dry_run)
        print(f"adset {L}: {adset_id}  ({spec['name']}, €{spec['daily_budget_cents']/100:.2f}/day)")
        new_ids[f"KIDS_{L}_ADSET_ID"] = adset_id

        image_hash = upload_image(version, ad_account, token, spec["image_path"], args.dry_run)
        print(f"image  {L}: {image_hash}  ({spec['image_path'].name})")

        creative_id = create_creative(version, ad_account, token, spec, image_hash, args.dry_run)
        print(f"creat  {L}: {creative_id}")
        new_ids[f"KIDS_{L}_CREATIVE_ID"] = creative_id

        ad_id = create_ad(version, ad_account, token, spec["ad_name"], adset_id, creative_id, args.dry_run)
        print(f"ad     {L}: {ad_id}  ({spec['ad_name']})")
        new_ids[f"KIDS_{L}_AD_ID"] = ad_id

    if not args.dry_run:
        append_campaign_ids(new_ids)
        print(f"\nIDs appended to {IDS_PATH.relative_to(ROOT)}")
    else:
        print("\n[DRY] not writing .campaign-ids")

    print("\nAll PAUSED. Diana flips to ACTIVE in Ads Manager after review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
