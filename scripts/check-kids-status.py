#!/usr/bin/env python3
"""Watch the Saged kids campaign ads; macOS-notify on status transitions.

Runs from cron every 5 minutes. Reads `.env` for the Meta token, `.campaign-ids`
for the ad IDs, persists last-seen status in `.kids-monitor-state`, and writes
a transition log to `reports/kids-monitor.log`.

Stops being noisy once both ads reach a terminal state (ACTIVE or rejected) —
each transition only notifies once. Safe to leave the cron running.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
IDS_PATH = ROOT / ".campaign-ids"
STATE_PATH = ROOT / ".kids-monitor-state"
LOG_PATH = ROOT / "reports/kids-monitor.log"

TERMINAL_GOOD = {"ACTIVE"}
TERMINAL_BAD = {"DISAPPROVED", "WITH_ISSUES", "REJECTED", "PENDING_BILLING_INFO"}


def parse_kv(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def fetch_status(env: dict, ad_id: str) -> str:
    version = env.get("META_API_VERSION", "v25.0")
    token = env["META_ACCESS_TOKEN"]
    url = (
        f"https://graph.facebook.com/{version}/{ad_id}"
        f"?fields=effective_status&access_token={token}"
    )
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))["effective_status"]
    except urllib.error.HTTPError as e:
        log(f"HTTP {e.code} fetching {ad_id}: {e.read().decode('utf-8', 'replace')[:200]}")
        return "UNKNOWN"
    except Exception as e:
        log(f"error fetching {ad_id}: {e}")
        return "UNKNOWN"


def notify(message: str, sound: str = "Glass") -> None:
    title = "Saged · Kids Trial"
    safe_msg = message.replace('"', "'")
    safe_title = title.replace('"', "'")
    script = f'display notification "{safe_msg}" with title "{safe_title}" sound name "{sound}"'
    subprocess.run(["osascript", "-e", script], check=False)


def log(line: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a") as f:
        f.write(f"{ts} · {line}\n")


def transition(label, current, last):
    if current == last:
        return
    log(f"{label}: {last or '(initial)'} -> {current}")
    if current in TERMINAL_GOOD:
        notify(f"{label} ad APPROVED — delivery starting", "Glass")
    elif current in TERMINAL_BAD:
        notify(f"{label} ad needs attention: {current}", "Basso")
    # PENDING_REVIEW / IN_PROCESS / CAMPAIGN_PAUSED etc → log only, no banner


def main() -> int:
    env = parse_kv(ENV_PATH)
    ids = parse_kv(IDS_PATH)

    ru_ad = ids.get("KIDS_RU_AD_ID")
    ua_ad = ids.get("KIDS_UA_AD_ID")
    if not ru_ad or not ua_ad or not env.get("META_ACCESS_TOKEN"):
        log("missing IDs or token; not configured. Exiting.")
        return 1

    ru = fetch_status(env, ru_ad)
    ua = fetch_status(env, ua_ad)

    last = parse_kv(STATE_PATH)
    transition("RU", ru, last.get("LAST_RU"))
    transition("UA", ua, last.get("LAST_UA"))

    STATE_PATH.write_text(f"LAST_RU={ru}\nLAST_UA={ua}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
