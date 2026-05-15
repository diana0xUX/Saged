#!/usr/bin/env python3
"""
audit-weekly.py — pulls last-7-day Meta Ads performance + diff vs prior week.

Replaces the old audit.py. Run via GitHub Action every Monday at 07:00 UTC, or by hand:
  python3 scripts/audit-weekly.py [YYYY-MM-DD]

Writes Markdown to reports/weekly/YYYY-Www.md (ISO week number).
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _meta import (
    REPORTS, load_env, insights, fmt_eur, fmt_int, fmt_pct,
    delta, conversions_from, load_template, safe_format,
)


def render_campaign_table(env: dict, *, since: date, until: date) -> str:
    rows = insights(
        env, since=since, until=until, level="campaign",
        fields=["campaign_name", "objective", "spend", "reach", "clicks", "ctr", "cpc", "actions"],
    )
    if not rows:
        return "_No campaign spend in this period._"
    out = ["| Campaign | Objective | Spend | Reach | CTR | CPC | Conversions |", "|---|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        conv = conversions_from(r)
        out.append(
            f"| {(r.get('campaign_name', '?'))[:40]} | "
            f"{(r.get('objective', '?'))[:18]} | "
            f"{fmt_eur(r.get('spend', 0))} | "
            f"{fmt_int(r.get('reach', 0))} | "
            f"{fmt_pct(r.get('ctr', 0))}% | "
            f"{fmt_eur(r.get('cpc', 0))} | "
            f"{conv} |"
        )
    return "\n".join(out)


def render_adset_table(env: dict, *, since: date, until: date) -> str:
    rows = insights(
        env, since=since, until=until, level="adset",
        fields=["adset_name", "spend", "impressions", "clicks", "ctr", "cpc", "frequency", "actions"],
    )
    if not rows:
        return "_No ad-set spend in this period._"
    out = ["| Ad set | Spend | Impressions | CTR | CPC | Freq | Conversions |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in rows:
        conv = conversions_from(r)
        out.append(
            f"| {(r.get('adset_name', '?'))[:40]} | "
            f"{fmt_eur(r.get('spend', 0))} | "
            f"{fmt_int(r.get('impressions', 0))} | "
            f"{fmt_pct(r.get('ctr', 0))}% | "
            f"{fmt_eur(r.get('cpc', 0))} | "
            f"{fmt_pct(r.get('frequency', 0))} | "
            f"{conv} |"
        )
    return "\n".join(out)


def render_ad_list(env: dict, *, since: date, until: date, top: bool) -> str:
    rows = insights(
        env, since=since, until=until, level="ad",
        fields=["ad_name", "spend", "impressions", "clicks", "ctr", "frequency"],
    )
    if not rows:
        return "_No ad data._"
    sorted_rows = sorted(rows, key=lambda r: float(r.get("ctr") or 0), reverse=top)
    selected = sorted_rows[:3]
    lines = []
    for r in selected:
        lines.append(
            f"- **{(r.get('ad_name', '?'))[:60]}** — CTR {fmt_pct(r.get('ctr', 0))}%, "
            f"spend {fmt_eur(r.get('spend', 0))}, freq {fmt_pct(r.get('frequency', 0))}"
        )
    return "\n".join(lines) if lines else "_No data._"


def build_tldr(curr: dict, prev: dict) -> str:
    spend = float(curr.get("spend") or 0)
    conv = conversions_from(curr)
    prev_conv = conversions_from(prev)
    if spend == 0:
        return "_No spend this week._"
    cpa = (spend / conv) if conv > 0 else None
    pieces = [f"**{fmt_eur(spend)}** spent · **{conv}** campaign-attributed conversions"]
    if cpa is not None:
        pieces.append(f"· CPA **{fmt_eur(cpa)}**")
    if prev_conv == 0 and conv > 0:
        pieces.append("· _First conversions this week._")
    elif conv > prev_conv:
        pieces.append(f"· _Up from {prev_conv} last week._")
    elif conv < prev_conv:
        pieces.append(f"· _Down from {prev_conv} last week._")
    return " ".join(pieces)


def build_watchlist(curr: dict, prev: dict, env: dict, since: date, until: date) -> str:
    flags = []
    spend = float(curr.get("spend") or 0)
    conv = conversions_from(curr)
    freq = float(curr.get("frequency") or 0)
    ctr = float(curr.get("ctr") or 0)

    # Per-adset for fatigue/imbalance
    adsets = insights(env, since=since, until=until, level="adset",
                     fields=["adset_name", "spend", "ctr", "cpc", "frequency"])
    fatigued = [a for a in adsets if float(a.get("frequency") or 0) > 3]

    if spend > 20 and conv == 0:
        flags.append(f"🚩 **{fmt_eur(spend)} spent, 0 conversions** — review landing-page conversion or audience match")
    if freq > 3:
        flags.append(f"🚩 **Frequency {freq:.1f}** account-wide — audience saturating, refresh creative or expand")
    if fatigued:
        names = ", ".join(a.get("adset_name", "?")[:30] for a in fatigued[:3])
        flags.append(f"🟡 **{len(fatigued)} ad set(s) with freq > 3**: {names}")
    if ctr > 0 and ctr < 1.0:
        flags.append(f"🟡 **CTR {ctr:.2f}%** below 1% — creative may need refresh")

    # CTR imbalance between ad sets
    if len(adsets) >= 2:
        ctrs = sorted([float(a.get("ctr") or 0) for a in adsets])
        if ctrs[0] > 0 and (ctrs[-1] / ctrs[0]) > 2.5:
            flags.append(f"🟡 **Ad set CTR imbalance**: top ({ctrs[-1]:.2f}%) is {ctrs[-1]/ctrs[0]:.1f}× the bottom ({ctrs[0]:.2f}%) — consider shifting budget")

    if not flags:
        return "- ✅ Nothing concerning this week."
    return "\n".join(f"- {f}" for f in flags)


def build_recommendations(curr: dict, prev: dict, env: dict, since: date, until: date) -> str:
    """Hand-tuned heuristics → concrete suggestions."""
    recs = []
    spend = float(curr.get("spend") or 0)
    conv = conversions_from(curr)
    prev_conv = conversions_from(prev)

    adsets = insights(env, since=since, until=until, level="adset",
                     fields=["adset_name", "spend", "ctr", "cpc"])

    # Recommendation 1: ad set budget rebalance if CTR is very imbalanced
    if len(adsets) >= 2:
        sorted_adsets = sorted(adsets, key=lambda a: float(a.get("ctr") or 0), reverse=True)
        top = sorted_adsets[0]
        bot = sorted_adsets[-1]
        top_ctr = float(top.get("ctr") or 0)
        bot_ctr = float(bot.get("ctr") or 0)
        if top_ctr > 0 and bot_ctr > 0 and (top_ctr / bot_ctr) > 2.0:
            recs.append(
                f"**Consider rebalancing budget**: `{top.get('adset_name', '?')[:40]}` "
                f"(CTR {top_ctr:.2f}%) is significantly outperforming "
                f"`{bot.get('adset_name', '?')[:40]}` (CTR {bot_ctr:.2f}%). "
                "If pattern holds another week, shift €1–2/day from lower to higher."
            )

    # Recommendation 2: no conversions warning
    if spend > 30 and conv == 0:
        recs.append(
            "**Funnel check**: " + fmt_eur(spend) + " spent, 0 attributed conversions. "
            "Verify Custom Conversion is still active in Events Manager. Click-through to Cal.com booking "
            "page from one of the ads and confirm the page loads fine."
        )

    # Recommendation 3: conversion trend
    if conv > prev_conv and prev_conv > 0:
        recs.append(f"**Conversions trending up** ({prev_conv} → {conv} week-over-week). Don't change anything that's working.")
    elif conv > 0 and prev_conv > conv:
        recs.append(f"**Conversions trending down** ({prev_conv} → {conv}). Check if anything changed: pixel, creative, landing page, Cal.com event-type config.")

    # Recommendation 4: scale signal
    if conv >= 5 and spend / conv < 30:
        recs.append(f"**Scale signal**: CPA below €30 with {conv} conversions/week. Consider raising daily budget by 20% (one-step increment to avoid resetting Meta's learning).")

    if not recs:
        return "_No specific recommendations this week. Continue current setup._"
    return "\n".join(f"- {r}" for r in recs)


def main() -> int:
    env = load_env()

    # The end-of-week to report on.
    if len(sys.argv) > 1:
        end = date.fromisoformat(sys.argv[1])
    else:
        end = datetime.utcnow().date() - timedelta(days=1)

    start = end - timedelta(days=6)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=6)

    iso_year, iso_week, _ = end.isocalendar()

    # Account-level totals
    curr_rows = insights(env, since=start, until=end)
    prev_rows = insights(env, since=prev_start, until=prev_end)
    curr = curr_rows[0] if curr_rows else {}
    prev = prev_rows[0] if prev_rows else {}

    # Link clicks extraction
    def link_clicks(d):
        for a in (d.get("actions") or []):
            if a.get("action_type") == "link_click":
                return int(float(a.get("value", 0)))
        return 0

    conv_curr = conversions_from(curr)
    conv_prev = conversions_from(prev)
    cpa_curr = (float(curr.get("spend") or 0) / conv_curr) if conv_curr > 0 else None
    cpa_prev = (float(prev.get("spend") or 0) / conv_prev) if conv_prev > 0 else None

    vars = {
        "iso_week": f"{iso_year}-W{iso_week:02d}",
        "since": start.isoformat(),
        "until": end.isoformat(),
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "tldr": build_tldr(curr, prev),
        "spend": fmt_eur(curr.get("spend", 0)),
        "prev_spend": fmt_eur(prev.get("spend", 0)),
        "spend_delta": delta(curr.get("spend", 0), prev.get("spend", 0)),
        "reach": fmt_int(curr.get("reach", 0)),
        "prev_reach": fmt_int(prev.get("reach", 0)),
        "reach_delta": delta(curr.get("reach", 0), prev.get("reach", 0)),
        "impressions": fmt_int(curr.get("impressions", 0)),
        "prev_impressions": fmt_int(prev.get("impressions", 0)),
        "impressions_delta": delta(curr.get("impressions", 0), prev.get("impressions", 0)),
        "link_clicks": link_clicks(curr),
        "prev_link_clicks": link_clicks(prev),
        "link_clicks_delta": delta(link_clicks(curr), link_clicks(prev)),
        "ctr": fmt_pct(curr.get("ctr", 0)),
        "prev_ctr": fmt_pct(prev.get("ctr", 0)),
        "ctr_delta": delta(curr.get("ctr", 0), prev.get("ctr", 0)),
        "cpc": fmt_eur(curr.get("cpc", 0)),
        "prev_cpc": fmt_eur(prev.get("cpc", 0)),
        "cpc_delta": delta(curr.get("cpc", 0), prev.get("cpc", 0)),
        "conversions": conv_curr,
        "prev_conversions": conv_prev,
        "conversions_delta": delta(conv_curr, conv_prev),
        "cpa": fmt_eur(cpa_curr) if cpa_curr else "—",
        "prev_cpa": fmt_eur(cpa_prev) if cpa_prev else "—",
        "cpa_delta": delta(cpa_curr, cpa_prev) if cpa_curr and cpa_prev else "—",
        "campaign_table": render_campaign_table(env, since=start, until=end),
        "adset_table": render_adset_table(env, since=start, until=end),
        "top_ads": render_ad_list(env, since=start, until=end, top=True),
        "bottom_ads": render_ad_list(env, since=start, until=end, top=False),
        "watchlist": build_watchlist(curr, prev, env, start, end),
        "recommendations": build_recommendations(curr, prev, env, start, end),
    }

    template = load_template("report-weekly.md")
    body = safe_format(template, **vars)

    out_dir = REPORTS / "weekly"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{iso_year}-W{iso_week:02d}.md"
    out_file.write_text(body)
    print(f"wrote {out_file}")
    print()
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
