#!/usr/bin/env python3
"""Pause unsafe Instagram-created campaigns and prepare safe paused replacements.

Every geo/locale ID is resolved live before any write. New entities are always
created PAUSED. Existing campaigns are preserved; nothing is deleted.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _meta import ROOT, fb_get, load_env

UNSAFE_CAMPAIGN_IDS = ["120249745435670513", "120249679890510513"]
CAMPAIGN_SPECS = [
    ("Saged · Adult Ceramics · Oct 2026 · Safe Draft", "adult"),
    ("Saged · Kids Ceramics · Oct 2026 · Safe Draft", "kids"),
]
LOCALE_NAMES = {"RU": "Russian", "UA": "Ukrainian"}
DAILY_BUDGET_CENTS = 125


def fb_post(env: dict[str, str], path: str, **params) -> dict:
    params["access_token"] = env["META_ACCESS_TOKEN"]
    url = f"https://graph.facebook.com/{env['META_API_VERSION']}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Meta API error {exc.code} on {path}: {body[:1000]}") from exc


def verify_city(env: dict[str, str]) -> dict:
    payload = fb_get(
        env["META_API_VERSION"], "search", env["META_ACCESS_TOKEN"],
        type="adgeolocation", q="Valencia",
        location_types=json.dumps(["city"]), country_code="ES", limit=50,
    )
    matches = [x for x in payload.get("data", [])
               if x.get("name") == "Valencia" and x.get("country_code") == "ES"]
    if not matches:
        raise RuntimeError("Valencia, Spain could not be verified; refusing all writes")
    result = sorted(matches, key=lambda x: 0 if x.get("region") == "Valencia" else 1)[0]
    if str(result.get("key")) != "699854":
        raise RuntimeError(f"Valencia key changed to {result.get('key')}; refusing all writes")
    return result


def verify_locale(env: dict[str, str], name: str, expected_key: str) -> dict:
    payload = fb_get(
        env["META_API_VERSION"], "search", env["META_ACCESS_TOKEN"],
        type="adlocale", q=name, limit=50,
    )
    matches = [x for x in payload.get("data", []) if x.get("name", "").lower() == name.lower()]
    if not matches:
        raise RuntimeError(f"Locale {name} could not be verified; refusing all writes")
    result = matches[0]
    if str(result.get("key")) != expected_key:
        raise RuntimeError(f"{name} key changed to {result.get('key')}; refusing all writes")
    return result


def existing_campaigns(env: dict[str, str]) -> dict[str, dict]:
    payload = fb_get(
        env["META_API_VERSION"], f"{env['META_AD_ACCOUNT_ID']}/campaigns", env["META_ACCESS_TOKEN"],
        fields="id,name,status,effective_status", limit=200,
    )
    return {c["name"]: c for c in payload.get("data", [])}


def main() -> int:
    if "--apply" not in sys.argv:
        print("Dry run only. Re-run with --apply to pause unsafe campaigns and create paused drafts.")
        return 0

    env = load_env()
    city = verify_city(env)
    locale_items = {
        "RU": verify_locale(env, "Russian", "17"),
        "UA": verify_locale(env, "Ukrainian", "52"),
    }
    changes: list[str] = []

    # Stop spend risk first. Preserve the entities and their history.
    for campaign_id in UNSAFE_CAMPAIGN_IDS:
        result = fb_post(env, campaign_id, status="PAUSED")
        if not result.get("success"):
            raise RuntimeError(f"Meta did not confirm pause for campaign {campaign_id}: {result}")
        changes.append(f"Paused unsafe campaign `{campaign_id}`")

    existing = existing_campaigns(env)
    created: dict[str, dict] = {}
    for campaign_name, product in CAMPAIGN_SPECS:
        if campaign_name in existing:
            campaign_id = existing[campaign_name]["id"]
            fb_post(env, campaign_id, status="PAUSED")
            changes.append(f"Reused and paused existing draft campaign `{campaign_id}` ({campaign_name})")
        else:
            campaign = fb_post(
                env, f"{env['META_AD_ACCOUNT_ID']}/campaigns",
                name=campaign_name,
                objective="OUTCOME_TRAFFIC",
                buying_type="AUCTION",
                special_ad_categories=json.dumps([]),
                is_adset_budget_sharing_enabled="false",
                status="PAUSED",
            )
            campaign_id = campaign["id"]
            changes.append(f"Created paused campaign `{campaign_id}` ({campaign_name})")
        created[campaign_name] = {"id": campaign_id, "adsets": {}}

        for code in ("RU", "UA"):
            adset_name = f"{product.title()} · {code} · Valencia 17km · Oct 2026"
            targeting = {
                "age_min": 25,
                "age_max": 54,
                "geo_locations": {
                    "cities": [{
                        "key": str(city["key"]),
                        "radius": 17,
                        "distance_unit": "kilometer",
                    }],
                    "location_types": ["home"],
                },
                "locales": [int(locale_items[code]["key"])],
                "targeting_automation": {"advantage_audience": 0},
            }
            adset = fb_post(
                env, f"{env['META_AD_ACCOUNT_ID']}/adsets",
                name=adset_name,
                campaign_id=campaign_id,
                daily_budget=str(DAILY_BUDGET_CENTS),
                billing_event="IMPRESSIONS",
                optimization_goal="LANDING_PAGE_VIEWS",
                bid_strategy="LOWEST_COST_WITHOUT_CAP",
                destination_type="WEBSITE",
                targeting=json.dumps(targeting),
                status="PAUSED",
            )
            created[campaign_name]["adsets"][code] = adset["id"]
            changes.append(f"Created paused ad set `{adset['id']}` ({adset_name}) at €1.25/day")

    now = datetime.now(timezone.utc)
    report_path = ROOT / "reports" / f"meta-safe-campaign-prep-{now.date().isoformat()}.md"
    lines = [
        f"# Safe Meta campaign preparation — {now.date().isoformat()}", "",
        f"Generated {now.strftime('%Y-%m-%d %H:%M UTC')}.", "",
        "## Changes applied", "",
        *[f"- {change}" for change in changes], "",
        "## Verified safeguards", "",
        f"- Valencia, Spain was resolved live as `{city['key']}`.",
        f"- Russian was resolved live as `{locale_items['RU']['key']}`; Ukrainian as `{locale_items['UA']['key']}`.",
        "- Russian and Ukrainian are separate ad sets.",
        "- Requested location is Valencia 17km, residents (`home`) only. Re-run the account audit to verify what Meta saved.",
        "- Age range is 25–54.",
        "- Advantage+ audience is off.",
        "- Objective is traffic, optimized for landing-page views.",
        "- All new campaigns and ad sets are paused.",
        "- Combined prepared budget is €5/day if every ad set is later activated.", "",
        "## Remaining before launch", "",
        "- Add approved RU and UA ads to the matching product and language ad sets.",
        "- Confirm each ad destination and UTM parameters.",
        "- Keep everything paused until Diana reviews the copy, image and schedule.",
        "- Do not activate if the account audit shows Meta broadened `home` to include `frequently_in`.", "",
        "## IDs", "", "```json", json.dumps(created, ensure_ascii=False, indent=2), "```", "",
    ]
    report_path.write_text("\n".join(lines))
    print(report_path)
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
