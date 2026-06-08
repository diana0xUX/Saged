# Kids-monitor runtime — why it lives outside ~/Documents/

Background: the kids-trial ad monitor (`scripts/check-kids-status.py`) runs every 5 minutes to watch RU/UA ad approval status and notify on transitions. The original cron schedule failed for **11 days** (2026-05-28 → 2026-06-08) without anyone noticing, because macOS TCC blocks the `cron` and `launchd`-spawned `python3` from reading files inside `~/Documents/`.

## Symptom

Every cron run wrote this to `reports/kids-monitor.cron.log`:

```
/Library/Developer/CommandLineTools/usr/bin/python3: can't open file
'/Users/diana/Documents/saged.club/scripts/check-kids-status.py':
[Errno 1] Operation not permitted
```

752 identical lines accumulated. Diana hadn't seen the kids-monitor `.log` (the transition log) update since the first day she set things up.

## Root cause

macOS TCC (Transparency, Consent, Control) protects `~/Documents/`, `~/Desktop/`, `~/Downloads/`, and removable volumes. Apps need Full Disk Access (or per-folder permission) to read or write these. `cron` and user `launchd` jobs get neither by default — even though they run as the user, they aren't in a session that has TCC inherited.

Granting Full Disk Access to `/usr/bin/python3` via System Settings would also work but requires GUI clicks every time the binary is reinstalled (e.g. Command Line Tools updates).

## Fix (2026-06-08)

Moved the kids-monitor's runtime to **`~/Library/Application Support/saged-kids-monitor/`** — `~/Library/` is **not** TCC-protected, so launchd-spawned `python3` can read and write there freely.

Runtime layout:

```
~/Library/Application Support/saged-kids-monitor/
    .env                       # copy of saged.club/.env (META_ACCESS_TOKEN, etc.)
    .campaign-ids              # copy of saged.club/.campaign-ids
    .kids-monitor-state        # last-seen RU/UA status (written by script)
    scripts/check-kids-status.py   # copy of saged.club/scripts/check-kids-status.py
    reports/
        kids-monitor.log       # transition log
        launchd.log            # stdout/stderr from launchd
```

The crontab entry was removed (`crontab -l > /tmp/crontab-backup-2026-06-08.txt` first), and the noisy log was archived to `reports/kids-monitor.cron.log.broken-cron-archive` so we have evidence of the failure window.

A user LaunchAgent at `~/Library/LaunchAgents/club.saged.kids-monitor.plist` runs the script every 300 seconds:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/club.saged.kids-monitor.plist
launchctl kickstart -k gui/$(id -u)/club.saged.kids-monitor   # force one immediate run
launchctl list club.saged.kids-monitor                         # show status; LastExitStatus = 0 means good
launchctl bootout gui/$(id -u)/club.saged.kids-monitor         # unload
```

## Maintenance — when you edit `.env`

The `.env` file (containing `META_ACCESS_TOKEN`) is duplicated:
- `~/Documents/saged.club/.env` — used by `audit-daily.py`, `audit-weekly.py`, etc. (run from Terminal which has Documents access)
- `~/Library/Application Support/saged-kids-monitor/.env` — used by the kids-monitor launchd job

If the token is rotated or any other variable changes, **update both**. One-liner:

```bash
cp ~/Documents/saged.club/.env "~/Library/Application Support/saged-kids-monitor/.env"
```

Same applies to `.campaign-ids` if ad IDs change.

## When the script itself changes

If `scripts/check-kids-status.py` in saged.club gets edited, the launchd copy needs to be refreshed too:

```bash
cp ~/Documents/saged.club/scripts/check-kids-status.py \
   "~/Library/Application Support/saged-kids-monitor/scripts/check-kids-status.py"
```

## How to know if it's healthy

```bash
launchctl list club.saged.kids-monitor                                  # LastExitStatus should be 0
ls -la "~/Library/Application Support/saged-kids-monitor/.kids-monitor-state"  # mtime should be < 5 min ago
tail -20 "~/Library/Application Support/saged-kids-monitor/reports/launchd.log"  # should be empty or recent
```

The `kids-monitor.log` (transition log) won't have new lines while both ads sit in the same status — that's normal. New entries appear only on state changes.

## Generalization to other periodic scripts

If `audit-daily.py` or any other script ever needs to be scheduled, the same TCC trap applies. Two options:

1. **Use this pattern** — copy script + config + state to `~/Library/Application Support/<name>/` and run via launchd.
2. **Grant `/usr/bin/python3` Full Disk Access** (System Settings → Privacy & Security → Full Disk Access → add the binary). One-time setup, breaks when Command Line Tools is updated.

This skill recommends option 1 for any new periodic job until/unless option 2 is chosen project-wide.
