#!/usr/bin/env python3
"""
audit-daily.py — pulls yesterday's Meta Ads performance + diff vs day-before.

Run via GitHub Action daily at 07:00 UTC, or by hand:
  python3 scripts/audit-daily.py [YYYY-MM-DD]

Writes Markdown to reports/daily/YYYY-MM-DD.md.
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _meta import (
    REPORTS, load_env, insights, pixel_events, fmt_eur, fmt_int, fmt_pct,
    delta, conversions_from, load_template, safe_format,
)


def render_adset_table(env: dict, *, since: date, until: date) -> str:
    """Pull adset-level insights and render as Markdown table."""
    rows = insights(
        env, since=since, until=until, level="adset",
        fields=["adset_name", "campaign_name", "spend", "impressions", "clicks", "ctr", "cpc", "frequency", "actions"],
    )
    if not rows:
        return "_No ad-set spend yesterday._"

    out = ["| Ad set | Spend | Impressions | CTR | CPC | Conversions |", "|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        name = (r.get("adset_name", "?"))[:40]
        conv = conversions_from(r)
        out.append(
            f"| {name} | {fmt_eur(r.get('spend', 0))} | "
            f"{fmt_int(r.get('impressions', 0))} | "
            f"{fmt_pct(r.get('ctr', 0))}% | "
            f"{fmt_eur(r.get('cpc', 0))} | "
            f"{conv} |"
        )
    return "\n".join(out)


def render_pixel_table(env: dict) -> str:
    events = pixel_events(env, hours_back=24)
    if not events:
        return "_No Pixel events fired in the last 24h._"
    out = ["| Event | Count |", "|---|---:|"]
    for name, count in sorted(events.items(), key=lambda x: -x[1]):
        out.append(f"| `{name}` | {count} |")
    return "\n".join(out)


def build_watchlist(today_data: dict, prev_data: dict) -> str:
    flags = []
    spend_today = float(today_data.get("spend") or 0)
    spend_prev = float(prev_data.get("spend") or 0)
    ctr_today = float(today_data.get("ctr") or 0)
    freq = float(today_data.get("frequency") or 0)
    conv_today = conversions_from(today_data)

    if spend_today == 0 and spend_prev > 0:
        flags.append("🚩 **No spend yesterday** despite spend the day before — check delivery status in Ads Manager")
    if spend_today > 0 and conv_today == 0 and spend_today > 5:
        flags.append(f"🟡 **{fmt_eur(spend_today)} spent, 0 conversions** — normal in first days, watch trend")
    if freq > 3:
        flags.append(f"🚩 **Frequency {freq:.1f}** — audience seeing the ad too often; refresh creative or expand targeting")
    if ctr_today > 0 and ctr_today < 1.0:
        flags.append(f"🟡 **CTR {ctr_today:.2f}%** is below 1% — creative may not be landing")

    if not flags:
        return "- ✅ Nothing concerning yesterday."
    return "\n".join(f"- {f}" for f in flags)


def build_tldr(today_data: dict, prev_data: dict, pixel: dict) -> str:
    spend = float(today_data.get("spend") or 0)
    clicks = int(float(today_data.get("clicks") or 0))
    conv = conversions_from(today_data)
    schedule_pixel = pixel.get("Schedule", 0)
    if spend == 0:
        return "_No spend yesterday._"
    pieces = [f"**{fmt_eur(spend)}** spent · **{clicks}** clicks · **{conv}** campaign-attributed conversions"]
    if schedule_pixel > conv:
        organic = schedule_pixel - conv
        pieces.append(f"_(Pixel saw {schedule_pixel} Schedule events total → ~{organic} from non-campaign sources like Telegram/direct)_")
    return " ".join(pieces)


def main() -> int:
    env = load_env()

    # Default: yesterday. Override with argv[1]: YYYY-MM-DD = the "since" date (i.e. the day being reported on).
    if len(sys.argv) > 1:
        target = date.fromisoformat(sys.argv[1])
    else:
        target = datetime.utcnow().date() - timedelta(days=1)

    prev = target - timedelta(days=1)

    # Account-level for yesterday + day-before
    today_rows = insights(env, since=target, until=target)
    prev_rows = insights(env, since=prev, until=prev)
    today_data = today_rows[0] if today_rows else {}
    prev_data = prev_rows[0] if prev_rows else {}

    # Per-adset (yesterday only)
    adset_table = render_adset_table(env, since=target, until=target)

    # Pixel events (24h)
    pixel = pixel_events(env, hours_back=24)
    pixel_table = render_pixel_table(env)

    # Render values
    conv_today = conversions_from(today_data)
    conv_prev = conversions_from(prev_data)
    link_clicks_today = 0
    for a in (today_data.get("actions") or []):
        if a.get("action_type") == "link_click":
            link_clicks_today = int(float(a.get("value", 0)))
            break
    link_clicks_prev = 0
    for a in (prev_data.get("actions") or []):
        if a.get("action_type") == "link_click":
            link_clicks_prev = int(float(a.get("value", 0)))
            break

    vars = {
        "report_date": target.isoformat(),
        "since": target.isoformat(),
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "tldr": build_tldr(today_data, prev_data, pixel),
        "spend": fmt_eur(today_data.get("spend", 0)),
        "prev_spend": fmt_eur(prev_data.get("spend", 0)),
        "spend_delta": delta(today_data.get("spend", 0), prev_data.get("spend", 0)),
        "impressions": fmt_int(today_data.get("impressions", 0)),
        "prev_impressions": fmt_int(prev_data.get("impressions", 0)),
        "impressions_delta": delta(today_data.get("impressions", 0), prev_data.get("impressions", 0)),
        "reach": fmt_int(today_data.get("reach", 0)),
        "prev_reach": fmt_int(prev_data.get("reach", 0)),
        "reach_delta": delta(today_data.get("reach", 0), prev_data.get("reach", 0)),
        "link_clicks": link_clicks_today,
        "prev_link_clicks": link_clicks_prev,
        "link_clicks_delta": delta(link_clicks_today, link_clicks_prev),
        "ctr": fmt_pct(today_data.get("ctr", 0)),
        "prev_ctr": fmt_pct(prev_data.get("ctr", 0)),
        "ctr_delta": delta(today_data.get("ctr", 0), prev_data.get("ctr", 0)),
        "cpc": fmt_eur(today_data.get("cpc", 0)),
        "prev_cpc": fmt_eur(prev_data.get("cpc", 0)),
        "cpc_delta": delta(today_data.get("cpc", 0), prev_data.get("cpc", 0)),
        "conversions": conv_today,
        "prev_conversions": conv_prev,
        "conversions_delta": delta(conv_today, conv_prev),
        "adset_table": adset_table,
        "pixel_events_table": pixel_table,
        "watchlist": build_watchlist(today_data, prev_data),
    }

    template = load_template("report-daily.md")
    body = safe_format(template, **vars)

    out_dir = REPORTS / "daily"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{target.isoformat()}.md"
    out_file.write_text(body)
    print(f"wrote {out_file}")
    print()
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
