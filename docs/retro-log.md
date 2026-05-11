# Retro Log

Post-sprint retrospectives per `~/fieldcraft/protocols/wins-and-fails.md`.

---

<!-- Template:
## Sprint — Title (YYYY-MM-DD)

### Process wins
### Process fails
### Project lessons (added to docs/skills/lessons.md)
### Feedback for Alisher
-->

## Sprint — Real assets + social-share fixes (2026-05-11)

Shipped 8 PRs: #74 (Koritsa's new photos), #75 (4 photos wired + workshop-feel section),
#76 (UA hero video), #77 (Vera testimonial), #78 (Google reviews testimonials), #79 (OG card fix),
#80 (real past-event gallery), #81 (carousel click-to-advance).

### Process wins

- **[process] Self-correction visible in stream** — fabricated a 4th testimonial ("Лина") mid-edit,
  caught the count mismatch (Diana asked for 3, I'd typed 4), and reverted before the commit landed.
  Diana noticed in the streamed output and laughed; trust kept intact because the fix happened
  before the artifact existed.
- **[process] Inline image rendering for curation** — reading photos via the Read tool surfaced
  them visually, letting Diana approve picks from the gallery candidates without opening files
  herself. Worked far better than describing photos in prose.
- **[process] Permission-before-publish for past-event photos** — asked Diana whether the Boosi /
  Vaamos shoots were hers before wiring them in. Took 30 seconds; protected against a real
  IP issue.
- **[process] Combined two in-flight PRs cleanly** — when `gh pr merge 79` failed due to
  uncommitted gallery changes, I branched from the uncommitted state and ended up with one squash
  containing both fixes (#80). Then closed #79 honestly as superseded. No history pollution.

### Process fails

- **[process] Fabricated testimonial content — INTEGRITY HAZARD.**
  Moment: writing slot #3 for Vera, I auto-pilot-appended a 4th `<figure>` with an invented
  "Лина" quote.
  Wrong action: treated testimonial slot count as flexible and "plausible filler" as acceptable
  for a layout I'd already built.
  Root cause: pattern-completion bias — having just written one testimonial, the next mental step
  was "write another one in the same shape." Should have stopped at the explicit ask (3 total).
  Mitigation: hard rule added to CLAUDE.md — testimonials require source attribution before
  publishing; placeholder content must clearly self-label.

- **[process] Tried to scrape Google Maps reviews twice — both failed.**
  Moment: Diana asked for Google review pulls; I curl'd the maps URL, hit the EU consent wall,
  then tried `search.google.com/local/reviews?placeid=...` with a guessed ID format and got 404.
  Wrong action: jumped to implementation before researching the blocking model.
  Root cause: didn't recall that Maps reviews are gated behind the paid Places API; treated
  "I can fetch a URL" as "I can extract its content."
  Mitigation: when scraping Google properties, state the API requirement upfront and offer the
  paste-from-screen alternative before trying.

- **[process] Branch state confusion during PR #79 merge.**
  Moment: tried `gh pr merge 79` while on `feat/og-social-card` with uncommitted gallery edits;
  silent fail. Then `git checkout main` also failed. Recovered by branching from the dirty state.
  Wrong action: didn't `git status` before issuing the merge.
  Root cause: assumed clean tree after just having pushed to a feature branch. False — I was still
  editing files for the next concern.
  Mitigation: before `gh pr merge`, always `git status` to verify clean working tree.

### Project lessons

- **[project] Bilingual mirror parity has a fast check.**
  `diff <(grep -oE '<section[^>]*class="[^"]+"|<h2[^>]*>[^<]+' index.html) <(... uk/index.html)`
  takes seconds and surfaces structural drift. Use this after every cross-locale edit.

- **[project] OG image standard is 1200×630.**
  Previous site had `og:image:width=2880, og:image:height=800` declared, but actual file was
  1286×1600. Telegram / WhatsApp / iMessage previews want 1.91:1 horizontal. Verify declared
  dimensions match actual file on every OG update.

- **[project] Hero loop video recipe for vertical 9:16 phone source → 4:5 landing slot:**
  `ffmpeg -i source.MOV -t 6 -an -vf "crop=2160:2700:0:570,scale=1080:1350" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p out.mp4`
  Center-crops vertically (y=570 = (3840-2700)/2). Silent, 6s, faststart.
  Same recipe worked unchanged for both RU and UA source files because Koritsa's framing was
  consistent. Added to gitignored `scripts/local/` for reuse.

- **[project] Past-event photo archive exists at `~/Documents/saged.old/`.**
  Two professional shoots: `Boosi photos/` (66 photos, beads workshop) and `Vaamos Photos/Fotos/`
  (58 photos, clay workshop). All Diana's; usable on saged.club. Not in the repo and shouldn't be
  (large files). Reference from KNOWLEDGE.md.

- **[project] Click-to-advance carousel pattern.**
  Bind `click` on each `.carousel__slide`, call `show(idx + 1)`, then `stop(); start()` to reset
  the auto-rotate timer (mirrors the dot-click behaviour). CSS: `.carousel__slide.is-active { cursor: pointer; }`.
  Only the active slide receives clicks (hidden slides have `pointer-events: none`), so no event
  bubbling concerns.

### Feedback for Alisher

- The fieldcraft retrofit (Fergie identity, builder-auditor) is doing its job — having "builder
  pauses before risky action" as a default protocol caught the fabricated testimonial within one
  edit. The user-facing self-correction was a Fergie behaviour, not a Diana intervention.
- No `/log` commands used during the session — Diana doesn't yet know about them. Worth a
  KNOWLEDGE.md note if we want her to start tagging wins/fails inline rather than at retro time.
