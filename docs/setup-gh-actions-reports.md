# GitHub Actions setup — Meta Ads reports

One-time setup so daily + weekly reports run automatically in the cloud, with secrets stored privately in GitHub.

**Time required**: ~3 minutes.

## Step 1 — Open the secrets page

Go to: <https://github.com/diana0xUX/Saged/settings/secrets/actions>

(Or manually: GitHub → diana0xUX/Saged → **Settings** → **Secrets and variables** → **Actions**)

You should see an empty "Repository secrets" section with a green **"New repository secret"** button.

## Step 2 — Add four secrets

Click **New repository secret** four times, once for each row below. Copy the value from your local `.env` file (in the repo root). Names must match exactly.

| Secret name | Value from your `.env` |
|---|---|
| `META_API_VERSION` | `v25.0` |
| `META_AD_ACCOUNT_ID` | (the long ID starting with `act_...` — copy the full line value) |
| `META_ACCESS_TOKEN` | (the long token starting with `EAAS...`) |
| `META_PIXEL_ID` | `1533639615120579` |

After adding each, you'll see the name in the list but **never the value** — that's correct. Secrets are encrypted at rest; even you can only update or delete, not read.

## Step 3 — Trigger the first manual run to confirm

Go to: <https://github.com/diana0xUX/Saged/actions>

You should see two workflows: **"Daily Meta Ads report"** and **"Weekly Meta Ads report"**.

- Click **Daily Meta Ads report**
- Click the **"Run workflow"** dropdown (top right of the page)
- Leave the date blank → click the green **Run workflow** button
- Wait ~30 seconds, refresh, you should see a green ✅
- Check the repo: a new file should appear in `reports/daily/YYYY-MM-DD.md` (auto-committed by the bot)

Repeat for **Weekly Meta Ads report** to confirm.

## Step 4 — Done

The workflows will now auto-run:
- **Daily** at 07:00 UTC (09:00 Madrid time in summer; 08:00 in winter)
- **Weekly** every Monday at 07:00 UTC

Reports show up in `reports/daily/` and `reports/weekly/` automatically.

## How to read the reports

Open the latest file in `reports/daily/` or `reports/weekly/`. Each report has:
- **TL;DR** — one-line summary
- **Numbers** with Δ (delta) vs the prior period — quick "is it getting better or worse"
- **Per ad set** — RU vs UA performance side-by-side
- **Watch list** — automatic flags for things that need attention
- **Recommendations** (weekly only) — suggestions like "rebalance budget toward UA"

## Troubleshooting

**Workflow run is red ❌ with "missing required env"**
You missed a secret in Step 2, or a name doesn't match. Re-check spelling.

**Workflow run is red ❌ with API errors**
The Meta access token expired. Generate a new one and update the `META_ACCESS_TOKEN` secret. Long-lived system-user tokens shouldn't expire under normal use, but if Meta auto-rotates them the workflow will start failing.

**No commit happened after a run**
That's normal if the data hasn't changed (e.g., re-running for the same day). Check the workflow log; you'll see "No changes to commit (report unchanged)."

**Want to back-fill old dates**
Use `workflow_dispatch` (the manual "Run workflow" button) and pass a date — generates a report for that day/week. Example: pass `2026-05-12` to generate `reports/daily/2026-05-12.md`.

## Rotate token later

If you ever need to rotate the Meta access token:
1. Generate new token in Meta Business → System Users
2. Update `META_ACCESS_TOKEN` at the secrets URL above (edit, paste, save)
3. Update your local `.env` file too so manual runs still work
4. No code changes needed
