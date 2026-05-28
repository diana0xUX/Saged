# Skills

Reusable recipes extracted from retros. Each file = one technique, one problem, one recipe.

Open the index, find the situation you're in, follow the recipe. Don't try to read these end-to-end — they're reference, not narrative.

When a retro produces a new lesson that you'd reach for again next time, write it here. One-time fixes belong in commit messages; durable patterns belong here.

## Index

| When you need to… | Open |
|---|---|
| Write a new Meta campaign / ad set / ad via API | [`meta-api-write-preflight.md`](meta-api-write-preflight.md) |
| Build a multi-step API resource (campaign → ad sets → ads) with safe re-runs | [`idempotent-build-script.md`](idempotent-build-script.md) |

## Format

Follows the basecamp-skills schema from `~/fieldcraft/protocols/retro-after-merge.md` § Skills Extraction:

- ≤80 body lines
- One technique per file
- Header sections: `## Problem`, `## Recipe`, optional `## Anti-patterns`
- First line: `_Last used: YYYY-MM-DD (one-line context)._`

## Maintenance

- New skill? Add a row to the index above when you write it.
- Skill no longer applies (API deprecated, replaced)? Mark with `> **Superseded** — see [other-skill](other-skill.md)` at the top; don't delete the file (future-me may need to know why the old approach was wrong).
- Patterns appearing in 3+ retros without being skilled out? That's a backlog — extract.
