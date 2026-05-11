# Audit prompt for Claude browser extension

Paste the prompt below into **Claude for Chrome** (or any Claude browser extension that can read the active tab) while you have Meta Ads Manager open. Navigate to each screen as Claude asks, and it will collect everything for the Phase 0 audit.

When Claude is done, copy the final Markdown report it produces and paste it back into the main chat with me.

---

## The prompt — copy everything below this line

```
You are helping run a Phase 0 audit of a Meta Ads Manager account for a small ceramic studio in Valencia, Spain. The studio runs Russian-language and Ukrainian-language ads for pottery workshops. Previous spend of €150 produced zero bookings; we need to diagnose why.

# Strict rules
- READ ONLY. Do not click any button that changes settings, pauses campaigns, edits copy, sends messages, or otherwise mutates the account.
- I (the user) will navigate to each screen. Tell me exactly where to click next.
- If data is missing or unclear, say "Not visible" or "Not set". Never invent numbers.
- If you see multiple ad accounts, ask me which one to audit before proceeding.
- Output the final report in the exact Markdown structure at the bottom of this prompt.

# Screens to collect from

## Screen 1 — Ad Account overview
URL: https://adsmanager.facebook.com/
Make sure the correct ad account is selected (top-left dropdown).
Collect:
- Ad account name
- Ad account ID (format: act_##########)
- Currency
- Timezone
- Total spend, last 90 days (set date range top-right to "Last 90 days")
- Count of active vs paused campaigns

## Screen 2 — Campaigns list, last 90 days
Stay on the "Campaigns" tab. Date range = Last 90 days.
For each campaign that spent money, collect:
- Campaign name
- Objective (Sales, Leads, Engagement, Traffic, Awareness, App Promotion, Messages)
- Status (Active, Paused, Completed)
- Start and end date
- Total spend (€)
- "Results" column value (e.g., "12 link clicks", "0 leads")
- Cost per result
- Reach
- Impressions
- Frequency

## Screen 3 — Drill into the highest-spend campaign
Click the campaign name, then the "Ad Sets" tab inside it.
For each ad set, collect:
- Ad set name
- Daily or lifetime budget
- Optimization goal (Conversions, Link clicks, Landing page views, Reach, Impressions, etc.)
- Billing event (Impressions or Link clicks)
- Status
- Spend, impressions, link clicks, CTR, CPC, CPM, results, cost per result

## Screen 4 — Ad set targeting
Click an ad set name, then "Edit" or look at the targeting summary panel.
For each ad set, collect:
- Location (countries, cities, radius in km/mi)
- Age range
- Gender
- Languages (this is critical — note whether Russian, Ukrainian, both, or none are set)
- Detailed targeting: interests, behaviors, demographics (list them; note if "Advantage+ Audience" is enabled)
- Custom audiences (included or excluded)
- Placements (Automatic, or list manual placements: Facebook Feed, IG Feed, Reels, Stories, etc.)

## Screen 5 — Ads in the campaign
Click the "Ads" tab inside the campaign.
For each ad, collect:
- Ad name
- Format (single image, carousel, video, Reel, collection, instant experience)
- Primary text (body copy)
- Headline
- Description (if present)
- Call-to-action button text (e.g., "Learn More", "Book Now", "Send Message", "Sign Up")
- Destination URL — full link. CRITICAL: is it an Instagram profile, a Facebook page, a WhatsApp link, a Messenger link, or a real website URL?
- Language of the copy (Russian / Ukrainian / Spanish / English / mixed)
- Status

## Screen 6 — Events Manager (Pixel + CAPI status)
URL: https://business.facebook.com/events_manager2
Collect:
- Is there a Meta Pixel linked to this business / ad account? Pixel name and ID.
- Date of last event fired
- Events firing in the last 7 days, with counts (PageView, ViewContent, AddToCart, InitiateCheckout, Lead, Purchase, CompleteRegistration, custom events)
- Conversions API status (Connected / Not connected)
- Event Match Quality score (per event, if shown — 0–10 scale)
- Any setup warnings or red banners

## Screen 7 — Audiences
URL: https://adsmanager.facebook.com/audiences
Collect:
- List of Custom Audiences: name, source type (Customer List, Website, Engagement, App, Offline), size, age (date created), availability status
- List of Lookalike Audiences: name, seed audience, percentage (1%, 3%, 5%, etc.), country, size

# Output format — produce this exact structure at the end

```markdown
# Audit results — [date]

## 1. Ad Account
- Name:
- ID:
- Currency:
- Timezone:
- 90-day spend:
- Active / paused campaigns:

## 2. Campaigns (last 90 days)
| Campaign | Objective | Status | Dates | Spend | Results | Cost/result | Reach | Impressions | Frequency |
|---|---|---|---|---|---|---|---|---|---|
| ... | | | | | | | | | |

## 3. Ad Sets (in highest-spend campaign)
| Ad set | Budget | Optimization goal | Billing event | Spend | Impressions | Link clicks | CTR | CPC | CPM | Results | Cost/result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ... | | | | | | | | | | | |

## 4. Targeting per ad set
For each ad set, list location, age, gender, languages, detailed targeting, custom audiences, placements.

## 5. Ads
For each ad, give: name, format, primary text, headline, CTA button, destination URL, language, status.

## 6. Events Manager
- Pixel: [name + ID, or "Not installed"]
- Last event: [date]
- Events in last 7 days: [list with counts]
- Conversions API: [Connected / Not connected]
- EMQ scores: [list]
- Warnings: [list]

## 7. Audiences
- Custom Audiences: [list with size + source + date]
- Lookalikes: [list with seed + %]

## 🚩 Red flags
- [List anything concerning, e.g., objective is "Engagement" not "Sales", destination URL is an IG profile, no Pixel installed, language not set, only static images, frequency >3, etc.]

## Notes / anomalies
- [Anything else worth surfacing]
```

# What to flag automatically as red flags
- Campaign objective is anything other than Sales or Leads (when bookings are the goal).
- Optimization goal is "Link clicks", "Landing page views", "Reach", or "Impressions" — should be a conversion event.
- Destination URL is Instagram profile, Facebook page, WhatsApp link, or Messenger link — not a real landing page.
- No Meta Pixel installed, or last event > 30 days ago.
- Conversions API not connected.
- Event Match Quality score < 6.
- Language targeting is empty or doesn't include Russian or Ukrainian (since these are the target audiences).
- Only static images — no video or Reel format.
- Frequency > 3 (audience fatigue).
- Ad copy is in Spanish or English instead of Russian/Ukrainian.

# If you can't access something
- If a screen requires permissions you don't have, tell the user which permission is missing.
- If a campaign has been deleted, note "No campaigns found in date range" — that itself is a finding.
- If the user has no ad account, note it and stop.

# Start
Begin by asking the user to confirm:
1. They are logged into the right Meta Business Manager.
2. They have the correct ad account selected.

Then walk through Screens 1 through 7 in order, telling the user exactly where to click before each section.
```

---

## How to use it

1. Open **Meta Ads Manager** in Chrome: https://adsmanager.facebook.com/
2. Make sure you're logged into the studio's account (not your personal one).
3. Open the Claude browser extension.
4. Paste the entire prompt (everything inside the code block above) into Claude.
5. Follow Claude's instructions, screen by screen.
6. When it produces the final Markdown report, copy it.
7. Paste the report back into our main conversation — I'll diagnose root causes and decide on Phase 1 priorities.

## If you don't have Claude for Chrome

The same prompt works if you screenshot each Ads Manager screen and feed them to Claude (in the desktop app or web), one at a time. Slower but functional.
