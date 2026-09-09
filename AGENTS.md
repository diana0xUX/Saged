# Saged.club agent rules

Read `CLAUDE.md`, `KNOWLEDGE.md`, and `creative/DESIGNER.md` before project work.

## Mobile optimisation is mandatory

Every website or landing-page change must be designed and verified for mobile in the same turn.

- Treat 390 px width as the primary layout, then verify desktop.
- Keep tap targets at least 44×44 px; primary mobile actions should be at least 48 px tall.
- Check that no horizontal scrolling appears at 390 px.
- Keep important text and CTAs visible without collisions, clipping, or fixed-bar overlap.
- Use responsive images and readable body text (16 px minimum).
- Respect iPhone safe areas for fixed bottom controls with `env(safe-area-inset-bottom)`.
- Verify the real page or an isolated public-assets preview before publishing.
- Do not mark a page complete if only the desktop layout was checked.

## Privacy

The `finances/` directory is private and gitignored. Never serve or publish it.
