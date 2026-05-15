"""
_meta.py — shared helpers for Meta Ads API access and Markdown report rendering.

Used by audit-daily.py and audit-weekly.py. Stdlib only.

Credentials loading:
- Local mode: reads from .env at repo root (gitignored)
- CI mode (GitHub Actions): reads from os.environ
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
REPORTS = ROOT / "reports"
TEMPLATES = ROOT / "docs" / "templates"


# ---------- env loading ----------

def load_env() -> dict[str, str]:
    """Load credentials from .env (local) or os.environ (CI)."""
    required = ("META_API_VERSION", "META_AD_ACCOUNT_ID", "META_ACCESS_TOKEN", "META_PIXEL_ID")
    env: dict[str, str] = {}

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()

    for k in required:
        if k not in env and k in os.environ:
            env[k] = os.environ[k]

    missing = [k for k in required if not env.get(k)]
    if missing:
        print(f"missing required env: {missing}", file=sys.stderr)
        sys.exit(1)

    return env


# ---------- API ----------

def fb_get(version: str, path: str, token: str, **params) -> dict:
    params["access_token"] = token
    url = f"https://graph.facebook.com/{version}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API error {e.code} on {path}: {body[:500]}", file=sys.stderr)
        return {"data": [], "error": body}


def insights(env: dict, *, since: date, until: date, level: str = "account", fields: list[str] | None = None, limit: int = 50) -> list[dict]:
    """Pull insights for a given level over a date range."""
    fields = fields or ["spend", "impressions", "reach", "frequency", "clicks", "ctr", "cpc", "cpm", "actions"]
    params = {
        "time_range": json.dumps({"since": since.isoformat(), "until": until.isoformat()}),
        "fields": ",".join(fields),
        "limit": limit,
    }
    if level != "account":
        params["level"] = level
    data = fb_get(env["META_API_VERSION"], f"{env['META_AD_ACCOUNT_ID']}/insights", env["META_ACCESS_TOKEN"], **params)
    return data.get("data") or []


def pixel_events(env: dict, *, hours_back: int = 24) -> dict[str, int]:
    """Return {event_name: count} totals for the Pixel over the past N hours."""
    now = int(datetime.utcnow().timestamp())
    start = now - (hours_back * 3600)
    data = fb_get(
        env["META_API_VERSION"],
        f"{env['META_PIXEL_ID']}/stats",
        env["META_ACCESS_TOKEN"],
        aggregation="event",
        start_time=start,
        end_time=now,
    )
    totals: dict[str, int] = {}
    for bucket in data.get("data", []):
        for e in bucket.get("data", []):
            totals[e["value"]] = totals.get(e["value"], 0) + int(e.get("count", 0))
    return totals


# ---------- formatters ----------

def fmt_eur(s) -> str:
    try:
        return f"€{float(s):.2f}"
    except (ValueError, TypeError):
        return "—"


def fmt_int(s) -> str:
    try:
        return f"{int(float(s)):,}".replace(",", " ")
    except (ValueError, TypeError):
        return "—"


def fmt_pct(s) -> str:
    try:
        return f"{float(s):.2f}"
    except (ValueError, TypeError):
        return "—"


def delta(now, prev, kind: str = "int") -> str:
    """Render a delta with arrow + percent. kind: 'int', 'eur', 'pct'."""
    try:
        n = float(now or 0)
        p = float(prev or 0)
    except (ValueError, TypeError):
        return "—"
    if p == 0:
        if n == 0:
            return "—"
        return "↑ new"
    diff_pct = (n - p) / p * 100
    arrow = "↑" if diff_pct > 0 else ("↓" if diff_pct < 0 else "→")
    return f"{arrow} {abs(diff_pct):.0f}%"


def action_value(actions: list[dict] | None, type_: str) -> int:
    for a in actions or []:
        if a.get("action_type") == type_:
            try:
                return int(float(a.get("value", 0)))
            except (ValueError, TypeError):
                pass
    return 0


def conversions_from(insight: dict, custom_conversion_ids: list[str] | None = None) -> int:
    """Sum custom conversion actions (offsite_conversion.custom.{id}) + standard purchase/schedule."""
    actions = insight.get("actions") or []
    total = 0
    for a in actions:
        atype = a.get("action_type", "")
        if atype in ("purchase", "schedule", "offsite_conversion.fb_pixel_purchase", "offsite_conversion.fb_pixel_schedule"):
            try:
                total += int(float(a.get("value", 0)))
            except (ValueError, TypeError):
                pass
        elif custom_conversion_ids and atype.startswith("offsite_conversion.custom."):
            cc_id = atype.split(".")[-1]
            if cc_id in custom_conversion_ids:
                try:
                    total += int(float(a.get("value", 0)))
                except (ValueError, TypeError):
                    pass
    return total


# ---------- template render ----------

def load_template(name: str) -> str:
    return (TEMPLATES / name).read_text()


def safe_format(template: str, **vars) -> str:
    """str.format() but unbalanced braces in dynamic content don't blow up.

    Pre-escapes inner content's curly braces; placeholders in the template
    are still real placeholders.
    """
    # First, find all valid placeholders to preserve them
    import re
    placeholders = set(re.findall(r"\{(\w+)\}", template))
    # Escape literal braces in dynamic content
    safe_vars = {}
    for k, v in vars.items():
        if isinstance(v, str):
            safe_vars[k] = v
        else:
            safe_vars[k] = str(v)
    # Use a manual substitution to avoid format() exploding on stray braces in content
    out = template
    for ph in placeholders:
        out = out.replace("{" + ph + "}", safe_vars.get(ph, f"{{MISSING:{ph}}}"))
    return out
