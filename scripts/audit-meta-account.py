#!/usr/bin/env python3
"""Audit Meta campaign structure and targeting against Saged.club safeguards.

Read-only. Writes a dated Markdown report and a gitignored JSON snapshot.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _meta import ROOT, fb_get, load_env

EXPECTED_CITY_NAME = "Valencia"
EXPECTED_COUNTRY = "ES"
EXPECTED_RADIUS_KM = 17
EXPECTED_MAX_AGE = 54
EXPECTED_LOCATION_TYPES = {"home"}
ALLOWED_OBJECTIVES = {"OUTCOME_TRAFFIC"}
HISTORICAL_SPEND_CAMPAIGNS = {
    "120244368076410513",
    "120245456772570513",
    "120248011726860513",
    "120248011753470513",
}


def get_all(env: dict[str, str], path: str, fields: str, limit: int = 200) -> list[dict]:
    payload = fb_get(
        env["META_API_VERSION"], path, env["META_ACCESS_TOKEN"],
        fields=fields, limit=limit,
    )
    return payload.get("data") or []


def verify_city(env: dict[str, str]) -> dict:
    payload = fb_get(
        env["META_API_VERSION"], "search", env["META_ACCESS_TOKEN"],
        type="adgeolocation", q=EXPECTED_CITY_NAME,
        location_types=json.dumps(["city"]), country_code=EXPECTED_COUNTRY,
        limit=50,
    )
    matches = [x for x in payload.get("data", [])
               if x.get("name") == EXPECTED_CITY_NAME and x.get("country_code") == EXPECTED_COUNTRY]
    if not matches:
        raise RuntimeError("Could not verify Valencia, Spain through Meta geo search")
    exact = sorted(matches, key=lambda x: 0 if x.get("region") == "Valencia" else 1)[0]
    return exact


def verify_locale(env: dict[str, str], name: str) -> dict:
    payload = fb_get(
        env["META_API_VERSION"], "search", env["META_ACCESS_TOKEN"],
        type="adlocale", q=name, limit=50,
    )
    matches = [x for x in payload.get("data", []) if x.get("name", "").lower() == name.lower()]
    if not matches:
        raise RuntimeError(f"Could not verify locale {name!r} through Meta locale search")
    return matches[0]


def inspect_adset(adset: dict, city_key: str, locale_ids: dict[str, int]) -> list[str]:
    issues: list[str] = []
    targeting = adset.get("targeting") or {}
    geo = targeting.get("geo_locations") or {}
    cities = geo.get("cities") or []
    city_keys = {str(c.get("key")) for c in cities}
    radii = {int(c.get("radius", 0)) for c in cities if c.get("radius") is not None}
    location_types = set(geo.get("location_types") or [])
    countries = set(geo.get("countries") or [])
    locales = {int(x) for x in targeting.get("locales") or []}

    if city_keys != {str(city_key)}:
        issues.append(f"wrong city keys {sorted(city_keys) or 'none'}")
    if countries:
        issues.append(f"country-wide targeting {sorted(countries)}")
    if radii != {EXPECTED_RADIUS_KM}:
        issues.append(f"radius {sorted(radii) or 'missing'}km")
    if location_types != EXPECTED_LOCATION_TYPES:
        issues.append(f"location types {sorted(location_types) or 'missing'}")
    if int(targeting.get("age_max") or 65) > EXPECTED_MAX_AGE:
        issues.append(f"age max {targeting.get('age_max', 65)}")
    if (targeting.get("targeting_automation") or {}).get("advantage_audience") != 0:
        issues.append("Advantage+ audience not explicitly off")
    allowed_locale_ids = set(locale_ids.values())
    unknown_locales = locales - allowed_locale_ids
    if unknown_locales:
        issues.append(f"unexpected locale IDs {sorted(unknown_locales)}")
    if len(locales & {locale_ids["Russian"], locale_ids["Ukrainian"]}) > 1:
        issues.append("Russian and Ukrainian combined")
    if adset.get("optimization_goal") not in {"LINK_CLICKS", "LANDING_PAGE_VIEWS"}:
        issues.append(f"optimization {adset.get('optimization_goal')}")
    if adset.get("bid_strategy") not in {None, "LOWEST_COST_WITHOUT_CAP"}:
        issues.append(f"bid strategy {adset.get('bid_strategy')}")
    return issues


def main() -> int:
    env = load_env()
    verified_city = verify_city(env)
    verified_locales = {name: verify_locale(env, name) for name in ("Russian", "Ukrainian", "English (UK)", "English (US)", "Spanish")}
    locale_ids = {name: int(item["key"]) for name, item in verified_locales.items()}

    campaigns = get_all(
        env, f"{env['META_AD_ACCOUNT_ID']}/campaigns",
        "id,name,objective,status,effective_status,created_time,start_time,stop_time,daily_budget,lifetime_budget,bid_strategy",
    )
    adsets = get_all(
        env, f"{env['META_AD_ACCOUNT_ID']}/adsets",
        "id,name,campaign_id,status,effective_status,created_time,start_time,end_time,daily_budget,lifetime_budget,optimization_goal,billing_event,bid_strategy,destination_type,targeting,promoted_object",
    )
    ads = get_all(
        env, f"{env['META_AD_ACCOUNT_ID']}/ads",
        "id,name,campaign_id,adset_id,status,effective_status,created_time,issues_info,creative{id,name,object_story_spec,asset_feed_spec}",
    )

    campaign_by_id = {c["id"]: c for c in campaigns}
    ads_by_adset: dict[str, list[dict]] = {}
    for ad in ads:
        ads_by_adset.setdefault(ad.get("adset_id", ""), []).append(ad)

    now = datetime.now(timezone.utc)
    active_campaigns = [c for c in campaigns if c.get("effective_status") in {"ACTIVE", "PAUSED", "IN_PROCESS", "WITH_ISSUES"}]
    live_adsets = [a for a in adsets if a.get("effective_status") in {"ACTIVE", "PAUSED", "CAMPAIGN_PAUSED", "WITH_ISSUES", "IN_PROCESS"}]

    report = [
        f"# Meta account safety audit — {now.date().isoformat()}", "",
        f"Generated {now.strftime('%Y-%m-%d %H:%M UTC')}. This audit is read-only.", "",
        "## Live-verified targeting IDs", "",
        f"- Valencia, Spain: `{verified_city['key']}` ({verified_city.get('region', 'region unavailable')})",
    ]
    for name, item in verified_locales.items():
        report.append(f"- {name}: `{item['key']}`")

    report += ["", "## Campaigns", "", "| Campaign | ID | Objective | Status | Stop date |", "|---|---|---|---|---|"]
    for c in sorted(active_campaigns, key=lambda x: x.get("created_time", ""), reverse=True):
        report.append(f"| {c.get('name','?')} | `{c['id']}` | {c.get('objective','?')} | {c.get('status')} / {c.get('effective_status')} | {c.get('stop_time','—')} |")

    report += ["", "## Ad-set safeguards", "", "| Campaign | Ad set | Status | Budget/day | Result |", "|---|---|---|---:|---|"]
    failing = 0
    for adset in sorted(live_adsets, key=lambda x: x.get("created_time", ""), reverse=True):
        campaign = campaign_by_id.get(adset.get("campaign_id"), {})
        issues = inspect_adset(adset, str(verified_city["key"]), locale_ids)
        if campaign.get("objective") not in ALLOWED_OBJECTIVES:
            issues.insert(0, f"campaign objective {campaign.get('objective')}")
        ad_issues = []
        for ad in ads_by_adset.get(adset["id"], []):
            if ad.get("effective_status") == "WITH_ISSUES":
                ad_issues.append(f"ad `{ad.get('name','?')}` has delivery issues")
        issues.extend(ad_issues)
        if issues:
            failing += 1
        budget = float(adset.get("daily_budget") or 0) / 100
        result = "Safe" if not issues else "; ".join(issues)
        report.append(f"| {campaign.get('name','?')} | {adset.get('name','?')} (`{adset['id']}`) | {adset.get('status')} / {adset.get('effective_status')} | €{budget:.2f} | {result} |")

    report += ["", "## Safe-action policy", "",
               "- Campaigns or ad sets with historical spend are preserved and paused rather than deleted.",
               "- New or replacement entities must be created paused.",
               "- Russian and Ukrainian remain separate ad sets.",
               "- Geo and locale IDs above were resolved live, not copied from old documentation.", "",
               f"**Summary:** {len(active_campaigns)} current campaign records, {len(live_adsets)} current ad sets, {failing} ad sets needing attention.", ""]

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    report_path = reports_dir / f"meta-account-audit-{now.date().isoformat()}.md"
    report_path.write_text("\n".join(report))
    raw_dir = ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"meta-account-audit-{now.date().isoformat()}.json"
    raw_path.write_text(json.dumps({"verified_city": verified_city, "verified_locales": verified_locales, "campaigns": campaigns, "adsets": adsets, "ads": ads}, indent=2))
    print(report_path)
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
