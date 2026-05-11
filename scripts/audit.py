#!/usr/bin/env python3
"""
audit.py — pulls last-7-day Meta Ads performance for saged.club.

Run weekly (cron / GitHub Action / by hand). Reads .env for credentials.
Writes a Markdown report to reports/YYYY-MM-DD.md.

No external dependencies. Uses only stdlib (urllib + json).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path


# ---------- config + helpers ----------

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
REPORTS = ROOT / "reports"


def load_env(path: Path) -> dict:
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k] = v
    return env


def fb_get(version: str, path: str, token: str, **params) -> dict:
    params["access_token"] = token
    url = f"https://graph.facebook.com/{version}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def fmt_eur(s: str | float) -> str:
    try:
        return f"€{float(s):.2f}"
    except (ValueError, TypeError):
        return "—"


def action_value(actions: list[dict], type_: str) -> int:
    for a in actions or []:
        if a.get("action_type") == type_:
            return int(float(a.get("value", 0)))
    return 0


# ---------- main ----------

def main() -> int:
    if not ENV.exists():
        print(f"missing {ENV}", file=sys.stderr)
        return 1

    env = load_env(ENV)
    V = env.get("META_API_VERSION", "v25.0")
    AC = env.get("META_AD_ACCOUNT_ID")
    T = env.get("META_ACCESS_TOKEN")
    if not (AC and T):
        print("missing META_AD_ACCOUNT_ID or META_ACCESS_TOKEN in .env", file=sys.stderr)
        return 1

    today = datetime.utcnow().date()
    since = today - timedelta(days=7)
    until = today

    # 1. account-level insights
    acc = fb_get(V, f"{AC}/insights", T,
                 time_range=json.dumps({"since": since.isoformat(), "until": until.isoformat()}),
                 fields="spend,impressions,reach,frequency,clicks,ctr,cpc,cpm,actions,cost_per_action_type")
    acc_data = (acc.get("data") or [{}])[0]

    # 2. campaign-level insights
    camps = fb_get(V, f"{AC}/insights", T,
                   time_range=json.dumps({"since": since.isoformat(), "until": until.isoformat()}),
                   level="campaign",
                   fields="campaign_id,campaign_name,objective,spend,reach,clicks,ctr,cpc,actions",
                   limit=50)

    # 3. ad-level (top + bottom)
    ads = fb_get(V, f"{AC}/insights", T,
                 time_range=json.dumps({"since": since.isoformat(), "until": until.isoformat()}),
                 level="ad",
                 fields="ad_name,campaign_name,spend,impressions,clicks,ctr,frequency,actions",
                 limit=50)

    # 4. account status
    acct = fb_get(V, AC, T, fields="name,account_status,amount_spent,balance,currency,timezone_name")

    # ---------- render Markdown ----------

    lines = []
    lines.append(f"# Weekly Meta Ads Report — {until.isoformat()}\n")
    lines.append(f"_Period: {since.isoformat()} → {until.isoformat()}_\n")
    lines.append(f"Account: `{AC}` · status code: **{acct.get('account_status','?')}** · lifetime: {fmt_eur(int(acct.get('amount_spent',0))/100 if acct.get('amount_spent') else 0)}\n")

    # account summary
    lines.append("## This week, at a glance\n")
    lines.append(f"- **Spend**: {fmt_eur(acc_data.get('spend',0))}")
    lines.append(f"- **Reach**: {acc_data.get('reach','—')} people")
    lines.append(f"- **Impressions**: {acc_data.get('impressions','—')}")
    lines.append(f"- **Clicks**: {acc_data.get('clicks','—')} (CTR {acc_data.get('ctr','—')[:5] if acc_data.get('ctr') else '—'}%)")
    lines.append(f"- **CPC**: {fmt_eur(acc_data.get('cpc',0))}")
    lines.append(f"- **CPM**: {fmt_eur(acc_data.get('cpm',0))}")

    purchases = action_value(acc_data.get("actions", []), "purchase")
    leads = action_value(acc_data.get("actions", []), "lead")
    msg_blocks = action_value(acc_data.get("actions", []), "onsite_conversion.messaging_block")

    lines.append(f"- **Workshop bookings (Purchase events)**: {purchases}")
    lines.append(f"- **Leads (form starts)**: {leads}")
    if msg_blocks:
        lines.append(f"- ⚠️  **Messaging blocks**: {msg_blocks} (negative quality signal)")
    if purchases > 0:
        cpa = float(acc_data.get("spend", 0)) / purchases
        lines.append(f"- **Cost per booking**: {fmt_eur(cpa)}")
    lines.append("")

    # campaigns
    lines.append("## Campaigns\n")
    lines.append("| Name | Objective | Spend | Reach | CTR | CPC | Results |")
    lines.append("|---|---|---:|---:|---:|---:|---|")
    for c in camps.get("data", []):
        actions = c.get("actions", []) or []
        top_actions = ", ".join(f"{a['action_type']}:{a['value']}" for a in actions[:3])
        lines.append(
            f"| {c.get('campaign_name','?')[:48]} | "
            f"{c.get('objective','?')} | "
            f"{fmt_eur(c.get('spend',0))} | "
            f"{c.get('reach','—')} | "
            f"{(c.get('ctr','—') or '—')[:5]} | "
            f"{fmt_eur(c.get('cpc',0))} | "
            f"{top_actions[:50]} |"
        )
    lines.append("")

    # top / bottom ads by CTR
    ad_rows = sorted(ads.get("data", []), key=lambda a: float(a.get("ctr") or 0), reverse=True)
    if ad_rows:
        lines.append("## Top 3 ads by CTR\n")
        for a in ad_rows[:3]:
            lines.append(f"- **{a.get('ad_name','?')[:60]}** — CTR {a.get('ctr','—')[:5]}%, spend {fmt_eur(a.get('spend',0))}, freq {(a.get('frequency','—') or '—')[:4]}")
        lines.append("")

        lines.append("## Bottom 3 ads by CTR\n")
        for a in ad_rows[-3:]:
            lines.append(f"- **{a.get('ad_name','?')[:60]}** — CTR {a.get('ctr','—')[:5]}%, spend {fmt_eur(a.get('spend',0))}, freq {(a.get('frequency','—') or '—')[:4]}")
        lines.append("")

    # anomalies
    lines.append("## Watch list\n")
    fatigued = [a for a in ad_rows if float(a.get("frequency") or 0) > 3]
    if fatigued:
        lines.append(f"- 🚩 **Audience fatigue** ({len(fatigued)} ad{'s' if len(fatigued)!=1 else ''}, frequency > 3): " + ", ".join(a.get("ad_name","?")[:40] for a in fatigued[:5]))
    if msg_blocks > 5:
        lines.append(f"- 🚩 **{msg_blocks} message-blocks** — audience is responding negatively to messaging follow-up")
    if purchases == 0 and float(acc_data.get("spend", 0)) > 20:
        lines.append(f"- 🚩 **No bookings tracked** despite {fmt_eur(acc_data.get('spend',0))} spent — check Pixel + landing page conversion event")
    if acct.get("account_status") == 3:
        lines.append(f"- 🚩 **Account UNSETTLED** — pay outstanding invoice or Meta may throttle delivery")
    if not lines[-1].startswith("- 🚩"):
        lines.append("- ✅ Nothing concerning this week.")
    lines.append("")

    lines.append("---")
    lines.append(f"_Generated by `scripts/audit.py` at {datetime.utcnow().isoformat(timespec='seconds')}Z_")

    # write report
    REPORTS.mkdir(exist_ok=True)
    out = REPORTS / f"{until.isoformat()}.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}")

    # print to stdout too
    print()
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
