#!/usr/bin/env python3
"""
launch-schedule-traffic-test.py

Hypothesis: paying €2/day per audience to send RU + UA speakers in Valencia
directly to saged.club/#schedule will produce WhatsApp booking messages.

Creates (ALL PAUSED — Diana activates):
  - 1 campaign: OUTCOME_TRAFFIC
  - 2 ad sets: RU and UA, Valencia 17km, age 25–54
  - 2 ads: simple link to saged.club/#schedule with Russian/Ukrainian copy

Budget: €2/day per ad set → €4/day total → ~€28/week test.
Stop / evaluate after 7 days or €28 spent.
"""
from __future__ import annotations
import json, sys, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _meta import load_env, fb_get

# ── Load credentials ──────────────────────────────────────────────────────────
env = load_env()
TOKEN   = env["META_ACCESS_TOKEN"]
VERSION = env["META_API_VERSION"]
ACCOUNT = env["META_AD_ACCOUNT_ID"]
PAGE_ID = "373458682506494"

# ── Runtime-verified constants (never trust from memory) ──────────────────────
VALENCIA_KEY_EXPECTED = "699854"   # Valencia, Spain — verified below
RU_LOCALE_EXPECTED    = 17         # Russian — verified below
UA_LOCALE_EXPECTED    = 52         # Ukrainian — verified below

DEST_URL = "https://saged.club/#schedule"
DAILY_BUDGET_CENTS = 200  # €2.00 per ad set per day


# ── Verification helpers ──────────────────────────────────────────────────────

def verify_locale(lang_name: str, expected_id: int) -> int:
    data = fb_get(VERSION, "search", TOKEN, type="adlocale", q=lang_name)
    matches = [d["key"] for d in data.get("data", []) if d["name"].lower() == lang_name.lower()]
    if not matches:
        sys.exit(f"FATAL: locale '{lang_name}' not found in Meta API")
    actual = int(matches[0])
    if actual != expected_id:
        sys.exit(
            f"FATAL: locale mismatch for '{lang_name}'\n"
            f"  script has: {expected_id}\n"
            f"  API says:   {actual}\n"
            "Update the expected constant before re-running."
        )
    print(f"  ✓ locale {lang_name} = {actual}")
    return actual


def verify_city_key(city_name: str, country_code: str, expected_key: str) -> str:
    data = fb_get(VERSION, "search", TOKEN, type="adgeolocation",
                  q=city_name, location_types='["city"]')
    matches = [
        (d["key"], d.get("country_code", ""))
        for d in data.get("data", [])
        if d["name"].lower() == city_name.lower()
    ]
    if not matches:
        sys.exit(f"FATAL: city '{city_name}' not found in Meta API")
    actual_key, actual_cc = matches[0]
    if actual_key != expected_key or actual_cc != country_code:
        sys.exit(
            f"FATAL: city key mismatch for '{city_name}, {country_code}'\n"
            f"  script has: {expected_key}\n"
            f"  API says:   key={actual_key}, country={actual_cc}\n"
            "Past incident 2026-07-20: wrong key sent ads to Egypt. Fix constant first."
        )
    print(f"  ✓ city {city_name}, {country_code} = {actual_key}")
    return actual_key


# ── API post helper ───────────────────────────────────────────────────────────

def fb_post(path: str, **fields) -> dict:
    url = f"https://graph.facebook.com/{VERSION}/{path}"
    data = urllib.parse.urlencode({**fields, "access_token": TOKEN}).encode()
    try:
        with urllib.request.urlopen(url, data=data, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"API error {e.code} on {path}: {body[:600]}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("0/5  Verifying locale IDs and city key against Meta API...")
    ru_locale = verify_locale("Russian", RU_LOCALE_EXPECTED)
    ua_locale = verify_locale("Ukrainian", UA_LOCALE_EXPECTED)
    valencia_key = verify_city_key("Valencia", "ES", VALENCIA_KEY_EXPECTED)

    # ── 1. Campaign ───────────────────────────────────────────────────────────
    print("\n1/5  Creating campaign...")
    camp = fb_post(
        f"{ACCOUNT}/campaigns",
        name="Saged · Schedule Traffic Test · Oct 2026",
        objective="OUTCOME_TRAFFIC",
        status="PAUSED",
        special_ad_categories="[]",
        is_adset_budget_sharing_enabled="false",
    )
    camp_id = camp["id"]
    print(f"     → campaign {camp_id}")

    # ── 2 & 3. Ad sets ────────────────────────────────────────────────────────
    ad_sets = [
        ("RU", ru_locale, "Saged · Traffic · RU · Valencia 17km"),
        ("UA", ua_locale, "Saged · Traffic · UA · Valencia 17km"),
    ]
    adset_ids = {}
    for lang, locale_id, name in ad_sets:
        print(f"\n{2 if lang == 'RU' else 3}/5  Creating {lang} ad set...")
        targeting = json.dumps({
            "geo_locations": {
                "cities": [{"key": valencia_key, "radius": 17, "distance_unit": "kilometer"}],
                "location_types": ["home"],
            },
            "age_min": 25,
            "age_max": 54,
            "locales": [locale_id],
            "targeting_automation": {"advantage_audience": 0},
        })
        adset = fb_post(
            f"{ACCOUNT}/adsets",
            name=name,
            campaign_id=camp_id,
            daily_budget=DAILY_BUDGET_CENTS,
            billing_event="IMPRESSIONS",
            optimization_goal="LINK_CLICKS",
            bid_strategy="LOWEST_COST_WITHOUT_CAP",
            targeting=targeting,
            destination_type="WEBSITE",
            status="PAUSED",
        )
        adset_ids[lang] = adset["id"]
        print(f"     → ad set {adset['id']}")

    # ── 4 & 5. Ads ────────────────────────────────────────────────────────────
    ads_copy = {
        "RU": {
            "message": "Занятия по керамике в Валенсии — для взрослых и детей. Расписание на неделю. Запись через WhatsApp.",
            "headline": "Расписание занятий — Saged.club",
            "description": "Выберите день и время — напишите нам, подберём место.",
        },
        "UA": {
            "message": "Заняття з кераміки у Валенсії — для дорослих і дітей. Розклад на тиждень. Запис через WhatsApp.",
            "headline": "Розклад занять — Saged.club",
            "description": "Оберіть день і час — напишіть нам, підберемо місце.",
        },
    }

    for i, (lang, adset_id) in enumerate(adset_ids.items(), start=4):
        print(f"\n{i}/5  Creating {lang} ad...")
        copy = ads_copy[lang]
        creative_spec = json.dumps({
            "page_id": PAGE_ID,
            "link_data": {
                "link": DEST_URL,
                "message": copy["message"],
                "name": copy["headline"],
                "description": copy["description"],
                "call_to_action": {"type": "LEARN_MORE"},
            },
        })
        creative = fb_post(
            f"{ACCOUNT}/adcreatives",
            name=f"Saged · Schedule · {lang} · Oct 2026",
            object_story_spec=creative_spec,
        )
        creative_id = creative["id"]

        ad = fb_post(
            f"{ACCOUNT}/ads",
            name=f"Saged · Schedule · {lang} · Oct 2026",
            adset_id=adset_id,
            creative=json.dumps({"creative_id": creative_id}),
            status="PAUSED",
        )
        print(f"     → ad {ad['id']}")

    print("\n✓ Done — all entities PAUSED.")
    print(f"\n  Campaign:  {camp_id}")
    for lang, sid in adset_ids.items():
        print(f"  {lang} ad set: {sid}")
    print(f"\n  Budget:    €{DAILY_BUDGET_CENTS/100:.2f}/day × 2 ad sets = €{DAILY_BUDGET_CENTS/100*2:.2f}/day")
    print("  Target:    RU + UA speakers · Valencia 17km · home · age 25–54")
    print(f"  URL:       {DEST_URL}")
    print("\n  Activate in Meta Ads Manager when ready.")
    print("  Evaluate after 7 days or €28 spent:")
    print("    Signal → WhatsApp messages received from schedule link")
    print("    Null   → 0 messages + CTR < 1% → kill the test")


if __name__ == "__main__":
    main()
