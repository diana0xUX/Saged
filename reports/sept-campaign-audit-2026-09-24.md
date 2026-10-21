# Campaign Audit — "Sept" · September 24, 2026

## What this is

A campaign called **"Sept"** was created on **September 23, 2026** through the Instagram "Promote" button — not through the API workflow. It is currently ACTIVE but not spending any money because both ads inside it are PAUSED with issues.

It will auto-expire on **October 1** if left alone. Max possible spend before then: **~€40** (€5/day × 8 days) — only if the ads somehow un-pause themselves.

---

## Campaign summary

| Field | Value |
|---|---|
| **Name** | Sept |
| **ID** | `120249679890510513` |
| **Status** | ACTIVE |
| **Created** | Sep 23, 2026 |
| **End date** | Oct 1, 2026 |
| **Daily budget** | €5/day |
| **Spend to date** | €0 |
| **Objective** | OUTCOME_TRAFFIC |
| **How it was created** | Instagram "Promote" button |

---

## The two ads inside

Both are **PAUSED — WITH ISSUES** (Meta flagged them, not us). That's why €0 has been spent.

### Ad 1 — "kids"
English copy for kids ceramics, ages 7–14, Wed + Fri 16:30. CTA sends people to the @saged.club Instagram profile.

> *"Looking for a creative activity for your child in Valencia? 🏺 Our ceramics classes are designed for kids aged 7–14 — a chance to work with clay, experiment and create something with their own hands. 🧒 Ages 7–14 · 🗓 Wed + Fri · 16:30 · 📍 Valencia · Message us on WhatsApp for details and availability."*

### Ad 2 — "All"
English copy for adult ceramics, general audience. CTA sends people to the @saged.club Instagram profile.

> *"Looking for something creative to do in Valencia? 🏺 Come work with clay, make something with your own hands and enjoy a slow creative afternoon at Saged Club. No previous experience needed ✨ 📍 Valencia · 🗓 Different sessions available · Message us on WhatsApp to find a time that works for you."*

---

## What's wrong with the targeting

This campaign was auto-built by Instagram and violates every targeting rule the studio has learned the hard way.

| Problem | What the campaign has | What it should be |
|---|---|---|
| **Cities** | Castellón, Gandía, Paterna, Sagunto | Valencia city only (key `699854`) |
| **Radius** | 40km around each wrong city | 17km (Metro minimum) |
| **Location type** | `home` + `recent` (includes tourists) | `home` only |
| **Optimization** | `PROFILE_VISIT` (IG profile clicks) | `LINK_CLICKS` or `MESSAGES` |
| **CTA destination** | @saged.club Instagram profile | WhatsApp or landing page |
| **Advantage+ audience** | ON | OFF (it overrides age/language) |
| **Age range** | 20–65 | 20–54 |
| **Extra languages** | Polish + Belarusian added automatically | Russian, Ukrainian, English, Spanish only |

**The geo alone makes this unfixable** — the campaign is targeting people in Castellón (90km north), Gandía (60km south) and Paterna (suburb) instead of Valencia city. There is no Valencia in the geo at all.

---

## Why the copy is actually fine

The ad text itself is decent — clear, friendly, mentions WhatsApp, no fake urgency. The kids ad correctly states age and schedule. If this targeting were rebuilt properly, the copy could be reused.

The images appear to be real studio photos (confirmed from Meta CDN).

---

## What to do

**Immediate:** Pause the campaign now. The ads have issues and aren't spending, but ACTIVE status means Meta could un-pause them if it resolves the issue internally.

**For October:** If you want to run ads in October — which makes sense (October bookings come from September-visible schedule) — rebuild one clean campaign through the API:
- **Objective**: `OUTCOME_TRAFFIC` → `LINK_CLICKS`, or better `OUTCOME_ENGAGEMENT` → `MESSAGES` (WhatsApp CTA)
- **Geo**: Valencia city, key `699854`, 17km, `home` only
- **Languages**: Russian (17) + Ukrainian (52) separate ad sets; English (6+24) third ad set
- **Age**: 25–54
- **Advantage+**: OFF
- **Budget**: €3–5/day per ad set
- **Copy**: reuse the "All" ad body above, translated to RU/UA, with a WhatsApp CTA instead of the Instagram profile link

---

## What this is not

This is not a geo bug like July 2026 (€95.46 lost to Egypt). It's not spending anything. The "WITH ISSUES" flag on both ads is actually protecting the budget here.

**Total risk if left alone until Oct 1: ≤€40. Current damage: €0.**

---

*Generated Sep 24, 2026 · Data from Meta Marketing API v25.0 · Campaign ID `120249679890510513`*
