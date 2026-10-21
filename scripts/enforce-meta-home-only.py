#!/usr/bin/env python3
"""Re-apply and verify residents-only targeting on the October paused drafts."""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _meta import fb_get, load_env

ADSETS = {
    "120249772446660513": 17,
    "120249772446940513": 52,
    "120249772447400513": 17,
    "120249772447870513": 52,
}


def post(env: dict[str, str], object_id: str, **params) -> dict:
    params["access_token"] = env["META_ACCESS_TOKEN"]
    url = f"https://graph.facebook.com/{env['META_API_VERSION']}/{object_id}"
    request = urllib.request.Request(url, urllib.parse.urlencode(params).encode(), method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def main() -> int:
    env = load_env()
    failed = False
    for adset_id, locale_id in ADSETS.items():
        targeting = {
            "age_min": 25,
            "age_max": 54,
            "geo_locations": {
                "cities": [{"key": "699854", "radius": 17, "distance_unit": "kilometer"}],
                "location_types": ["home"],
            },
            "locales": [locale_id],
            "targeting_automation": {"advantage_audience": 0},
        }
        post(env, adset_id, targeting=json.dumps(targeting), status="PAUSED")
        saved = fb_get(
            env["META_API_VERSION"], adset_id, env["META_ACCESS_TOKEN"],
            fields="id,name,status,effective_status,targeting",
        )
        location_types = set((saved.get("targeting") or {}).get("geo_locations", {}).get("location_types") or [])
        print(f"{adset_id}: saved location_types={sorted(location_types)}")
        if location_types != {"home"}:
            failed = True
    if failed:
        print("Meta broadened at least one ad set after an explicit home-only update. Drafts remain paused.")
        return 2
    print("All four ad sets are verified as home-only and paused.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
