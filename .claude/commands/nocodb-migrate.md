# NocoDB Migration from Notion

Migrates all Notion databases to NocoDB on the Hetzner server, then verifies every row count matches.

## What this does

1. Stops NocoDB container
2. Wipes the SQLite database (start fresh)
3. Restarts NocoDB and waits for it to be ready
4. Runs `/opt/setup_nocodb.py` — signs in, creates all 14 tables from Notion schema, inserts all records
5. Reports total rows inserted

## Server details

- Host: `2.28.140.155`
- SSH key: `~/.ssh/saged_hetzner`
- NocoDB container name: `nocodb` (ID: `bee2c18a9f07`)
- NocoDB version: `0.301.5` (fully free, no license required)
- SQLite data file: `/opt/nocodb/noco.db`
- NocoDB base ID: `p2txdvaha72xsn4` (base title: "Saged")
- NocoDB URL: `http://localhost:8080` (also at `admin.saged.club`)
- Admin login: `admin@saged.club` / `Saged2026admin!`
- API token: `niIrlNav-3NkyiB82YDtPznbKLfhs0pptRIg4HKb`

## Run the full migration (wipe + rebuild)

```bash
ssh -i ~/.ssh/saged_hetzner -o StrictHostKeyChecking=no root@2.28.140.155 '
docker stop nocodb && \
rm /opt/nocodb/noco.db && \
docker start nocodb && \
until curl -sf http://localhost:8080/api/v1/health 2>/dev/null | grep -q OK; do sleep 2; done && \
python3 /opt/setup_nocodb.py && \
python3 /opt/fix_select_columns.py
'
```

`setup_nocodb.py` creates tables + inserts data (all columns as SingleLineText).
`fix_select_columns.py` then converts 37 columns to proper SingleSelect/MultiSelect using Notion's schema.
Both scripts must run — skip fix_select_columns and dropdown fields show as plain text inputs.

## Run migration only (keep existing tables, re-insert data)

If the NocoDB structure is intact and you only want to refresh the data:

```bash
ssh -i ~/.ssh/saged_hetzner -o StrictHostKeyChecking=no root@2.28.140.155 'python3 /opt/migrate_only.py'
```

## Expected result

```
✅ Done: 265 inserted, 0 skipped
```

## Key facts

- **Never delete Notion data** — one-way read from Notion, write to NocoDB
- NocoDB 0.301.5 is the correct version — fully free with forms, no license needed
- Do NOT upgrade to 2026.x — those versions have a commercial license that breaks form views
- The old 2026.09.1 database is backed up at `/opt/nocodb/noco.db.2026-backup`
- Setup script: `/opt/setup_nocodb.py` — creates base, tables, migrates data in one run
- Old scripts (`migrate_v2.py`, `verify_migration.py`) reference old base ID — use setup_nocodb.py instead
- setup_nocodb.py inserts all columns as SingleLineText first; fix_select_columns.py converts 37 to proper Select types
- Grid view renders blank in headless/test browsers (ResizeObserver missing) — works fine in real Chrome/Firefox
- Scripts on server: `/opt/setup_nocodb.py`, `/opt/fix_select_columns.py`, `/opt/verify_all.py`
