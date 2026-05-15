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

---

## Sprint — Campaign launch + first revenue + coworking pages (2026-05-12 → 2026-05-14)

Three-day arc: Stripe approval landed silently → end-to-end smoke test caught two infra gaps →
campaign went live 2026-05-12 at €10/day → first real paid booking came in via Telegram (not the
ad) → first workshop ran 2026-05-14 → coworking offering shipped as RU/UA/EN landing pages.
First real revenue through the funnel: €60 from one Telegram-direct booking. Campaign at €15
spend, 0 ad-attributed conversions yet (normal at 48h).

### Process wins

- **[process] Smoke test caught two blocking infra gaps before €€ moved.**
  Bug 1: Stripe was connected to the Cal.com account but not enabled on the specific event
  type — first test booking went through for free. Bug 2: Cal.com's Meta Pixel app only fires
  `Schedule`, never `Purchase` — campaign was built for Purchase optimization, would have run
  blind. Both fixed before any real spend. Validates the "smoke-test before launch ads"
  protocol from #61's pass condition.

- **[process] ScheduleWakeup pattern for async verification.**
  Meta Pixel stats endpoint has ~30 min aggregation lag. Instead of polling or asking Diana to
  refresh Events Manager repeatedly, set a 30-min ScheduleWakeup and returned to verify
  autonomously. Diana could close the tab. When the wakeup fired at 11:29 UTC, Schedule events
  had landed and verification proceeded. Better than retry-loops; better than user-facing waits.

- **[process] Took maximum autonomous action when explicitly authorized.**
  Diana said "do what you can" mid-session when overwhelmed by cross-app debugging. While she
  stepped away: created Custom Conversion via API (mapping Schedule→Purchase €60), discovered
  Meta locks ad-set optimization after publish, created v2 ad sets, updated `.campaign-ids`,
  closed issues, updated halt.md. Came back to a single one-command flip-to-active. The trust
  signal from "do what you can" maps to a real authorization expansion.

- **[process] Detected overwhelm signal mid-session and adjusted.**
  After ~10 rounds of cross-app navigation, Diana asked "what do I need to do?" — short, low-
  energy. Recognized as overwhelm. Dropped the AskUserQuestion picker that was queued in my
  head; gave one plain-language action ("cancel the test booking, I'll handle the rest"). Saved
  the pattern to cross-session memory (`feedback_diana_overwhelm_signal.md`) so this doesn't
  have to be re-learned.

- **[process] Local smoke-test of three-language site before deploy.**
  Spun up python http.server on 127.0.0.1, scripted HTTP checks across all three coworking
  pages, asset references, cross-link resolution. Caught nothing (everything passed) but the
  test design caught a false-positive (HTML entities vs literal strings) which surfaced a real
  bug in the test, not the site. Cheap, fast, repeatable.

- **[process] Cross-session memory captured 5 reusable learnings.**
  Wrote: `cal-com-meta-pixel-events`, `meta-api-edit-locks`, `pixel-vs-campaign-attribution`,
  `diana-overwhelm-signal`, `saged-club-campaign-live-2026-05-12`. These are non-obvious facts
  that would have cost real time to re-discover. Already validated in this session by re-
  reading the API edit-lock memory while planning the v2 ad-set rebuild.

### Process fails

- **[process] Almost missed the campaign-objective mismatch.**
  Smoke test confirmed `Schedule` events firing on Meta. I was about to mark task #5 complete
  and recommend campaign flip — *before* checking that the existing ad sets were configured for
  `Schedule` as the optimization event. They weren't; they were built for `Purchase`. Caught it
  while pulling campaign config "just to confirm before flipping" — but should have been
  Step 1 of smoke-test scoring, not a defensive check.
  Mitigation: smoke-test checklist should include "does the entity that consumes this event
  *actually consume this event name*?" — not just "does the event fire?"

- **[process] Sent Diana to Events Manager UI when API was already available.**
  Spent two rounds asking Diana to navigate business.facebook.com/events_manager → Test Events
  before realizing `.env` had `META_ACCESS_TOKEN` and I could just query the stats endpoint
  myself. Should have read `.env` and KNOWLEDGE.md at the start of the smoke-test, not after
  Diana got confused.
  Mitigation: when the user has tokens/credentials in the project's `.env`, default to API
  verification before UI navigation. Save the user's clicks.

- **[process] Language switcher shipped with absolute paths, broke in `file://` preview.**
  Built cross-links as `/coworking/`, `/uk/coworking/` etc. Worked perfectly under the python
  http.server tests; broke instantly when Diana opened the page via `file://`. Took two fix
  rounds (relative paths, then explicit `index.html`) before she could click between languages.
  Mitigation: hand-edited static sites with no build step almost always get previewed via
  `file://` at some point. Use relative paths *and* explicit filenames (`index.html`) by
  default, not just on prompt.

- **[process] Smoke-test false positives wasted a debugging round.**
  Python test compared expected strings literal-for-literal against HTML body. The HTML had
  `&nbsp;` non-breaking-space entities where expected strings had ASCII spaces — caused
  "missing content" alerts that triggered me to re-check page correctness when the issue was
  the test. Lost 30 seconds of doubt.
  Mitigation: any HTML content assertion must `html.unescape()` and normalize `\xa0` → ` `
  before substring match.

### Project lessons

- **[project] Cal.com config is per-event-type, not account-level.**
  Stripe connection at account level does not enable payment on a specific event type — each
  event type's "Apps" tab must explicitly turn on Stripe with a price. Same for Meta Pixel app.
  This bit us once with Stripe, again with the Pixel. Memorize: every Cal.com integration is
  scoped to the event type, not the account.

- **[project] Meta API rules force "create new entity, leave old paused" pattern.**
  Campaign objective is locked once any ad set exists (error 1885073). Ad set optimization is
  locked after publish (error 3260011). When optimization needs to change, the recovery is
  always: create a new ad set in the same campaign, leave old one paused, repoint scripts.
  Don't try to delete; pause is safer.

- **[project] Cal.com Meta Pixel app vocabulary: Lead/CompleteRegistration/Schedule/PageView.**
  No Purchase event option. No value/currency parameter. For Sales-objective campaigns needing
  Purchase optimization, the workaround is a Meta Custom Conversion mapping
  `event_name = Schedule` → `category PURCHASE` with `default_conversion_value`. Working
  Custom Conversion ID for Saged: `980444324695740` (Schedule → Purchase €60).

- **[project] Meta API Custom Conversion endpoint uses `event_source_id`, not `pixel_id`.**
  Every other Meta API endpoint takes `pixel_id`. This one is different. Error message is
  helpful (`"The parameter event_source_id is required"`) but costs a round-trip if you
  assume the common name.

- **[project] Meta Pixel `/stats?aggregation=event` endpoint has ~30 min aggregation lag.**
  Don't trust real-time absence of events. Test Events UI requires `test_event_code` parameter
  in the event payload — Cal.com doesn't send it, so production Cal.com Schedule events don't
  appear in Test Events at all even when firing correctly.

- **[project] Pixel-total events ≠ campaign-attributed conversions.**
  `/{pixel-id}/stats` shows ALL events fired on the Pixel (ad-driven + organic + direct).
  `/{campaign-id}/insights` `actions` field shows only events Meta attributes to the campaign.
  When reporting "is the campaign working?", always pull campaign insights. When reporting "is
  the Pixel working?", pull stats. Diana's first booking via Telegram showed in Pixel-total
  but contributed 0 to campaign attribution.

- **[project] Stripe approval is silent now.**
  No celebratory "you're approved" email. Confirmation = `pk_live_*` keys appearing in the
  dashboard + bank account confirmation email. Future "did Stripe approve us?" questions are
  answered by the dashboard, not the inbox.

- **[project] Three-language static-site pattern works without complications.**
  `/coworking/` (RU) + `/uk/coworking/` (UA) + `/en/coworking/` (EN). hreflang alternates for
  SEO; language switcher with relative `index.html`-explicit hrefs for file:// + http://
  parity. Logo on EN page goes to `/` since no `/en/` main exists yet — acceptable orphan.

- **[project] First-revenue channel ≠ predicted-primary channel.**
  Campaign launched with Telegram as a low-priority channel in the social strategy. First real
  customer came via Telegram, not Meta. Worth weighting this in the Day 8 review: if Telegram
  keeps converting and Meta doesn't, that's a meaningful redirect of investment toward
  building the @sagedclub public channel (#39).

### Feedback for Alisher

- **`ScheduleWakeup` is underused.** This was the right pattern for the Pixel-aggregation-lag
  case (wait 30 min, come back, verify). Probably belongs in a "patterns for async
  verification" doc — anywhere we have an external system with eventual consistency, the choice
  is "poll" vs "schedule a check vs "ask the user to wait." Wakeup wins on every dimension
  (no polling cost, no user wait).

- **The `feature_diana_overwhelm_signal` memory entry is the kind of context that doesn't
  belong in code or commits.** Auto-memory is doing real work for cross-session continuity of
  *how I work with this person*, not just *what's in the repo*. Five memory entries this
  session and all of them earned their slot.

- **Builder-auditor protocol didn't get invoked.** Most decisions in this session were live-
  tactical (flip optimization event from Purchase to Schedule? Yes, go). The async Senty cycle
  fits long-running implementations; it doesn't fit "Diana is here, decision is reversible,
  campaign is paused, ship it." Maybe a "tactical live mode" protocol would name this
  explicitly so I'm not pattern-matching against a workflow that doesn't apply.

- **The "do what you can" authorization expansion is powerful.** When Diana said it, I went
  from advisor to operator and did substantial Meta API config work autonomously. Worth
  noting as a project-level pattern: certain phrases ("just do it," "handle it," "do what you
  can") expand the autonomy envelope past the default-conservative position. Recording these
  in feedback memory so future sessions catch the signal faster.

---

## Sprint — Post-launch polish (2026-05-14 evening → 2026-05-15)

Three small content commits after the main coworking-page retro:
- "Два занятия по 2 часа" added to €60 inclusions (RU + UA mirror)
- "Забронировать слот" → "Забронировать место" wording change (RU + UA)
- Footer cross-promo line linking main pages to /coworking/ + /coworking/#intro

Not a sprint in the protocol sense — closer to "afternoon polish."
Worth a short retro anyway to keep the discipline and capture two real tactical lessons.

### Process wins

- **[process] Bilingual mirror discipline held across three content changes.**
  Each content edit was mirrored in RU + UA in the same commit (matching CLAUDE.md's
  non-negotiable rule). Section-count parity grep ran clean (11 = 11) without intervention.
  The rule continues to pay rent without requiring extra ceremony.

- **[process] AskUserQuestion was the right tool for the "cross-promo placement" choice.**
  Three real placement options (footer line / dedicated section / topbar nav) with genuine
  tradeoffs. Diana picked footer, ship. Compare to overwhelm-signal cases where pickers
  hurt — here, picker helped because the question had real forks, not unclear scope.

- **[process] One-commit-per-content-change kept history clean.**
  Three small commits with focused messages rather than one "misc edits" mega-commit. Each
  shows up in git log as a discoverable change.

### Process fails

- **[process] Language switcher shipped twice-broken before reaching working state.**
  Round 1: absolute paths (`/coworking/`) — broke when Diana previewed via file://.
  Round 2: relative paths (`../coworking/`) — still broke because Chrome shows directory
  listings for `file://.../coworking/` URLs in dark mode (the "black screen with white text"
  screenshot).
  Round 3: explicit `index.html` in the hrefs — finally worked in both http:// and file://.
  Wrong action: shipped Round 1 without considering Diana would preview locally.
  Root cause: defaulted to "production-style" absolute paths because the test server made
  them work in my smoke-test, even though I knew Diana was editing locally.
  Mitigation: hand-edited static sites with no build step → relative paths + explicit
  `index.html` in every cross-page link. Saved as project lesson below.

- **[process] Left the python http.server running.**
  Started it for the smoke test; offered to stop it; never actually killed it. Still running
  on port 8765 at the time of this retro. Not destructive, but stale background processes
  accumulate.
  Mitigation: when offering a cleanup ("say 'stop server' to kill"), set a follow-up to
  kill it after some idle window, or just kill it when the next unrelated commit happens.

### Project lessons

- **[project] Static-site `file://` preview is a first-class deployment context, not an
  afterthought.** Diana works in a vanilla HTML/CSS/JS repo with no build step. The natural
  preview workflow is `open file://...` from Finder. This means:
  - All cross-page links must be **relative** (absolute paths starting with `/` resolve to
    the filesystem root in file:// mode → 404)
  - Directory URLs (ending in `/`) get the browser's directory-listing page in file:// mode
    → use explicit `index.html` in every link
  - These are not "nice to have" — they are required for the local preview flow to work
  Both rules combined: language switchers and any cross-page link should look like
  `href="../uk/coworking/index.html"`, never `href="/uk/coworking/"` and never
  `href="../uk/coworking/"` (without `index.html`).

- **[project] Cross-promo via footer is the right surface for "by the way" offerings.**
  Adding coworking + intro-course links to the main page's footer (vs new section / new nav
  link) preserves the Thursday-workshop landing flow while still making the orphan
  /coworking/ page discoverable. Pattern: when a secondary offering shouldn't compete with
  the primary CTA on a landing page, footer cross-promo is unobtrusive.

### Feedback for Alisher

- **Retro cadence is uneven.** The protocol seems tuned for sprint-length work (the previous
  retro covered 3 days of major launches). Today's polish work was 30 min of edits. A
  one-page "daily summary" or "shift retro" could fit between full sprint retros — captures
  small tactical lessons without inflating into a full retro template. Worth thinking about.

- **The "let me re-test it locally" → diana's screenshot → "ah, file://" loop today was a
  useful reminder that my mental model of the deployment context can drift from the user's
  actual workflow.** I assumed http-served preview because that's what my smoke test used;
  Diana was on file://. Worth adding a habit: when first showing the user a result, ask
  "are you opening this via the local server or via Finder?" before assuming.

- **`docs/retro-log.md` is now 3 retro entries deep.** Worth a meta-pass at some point to
  extract recurring patterns across retros (e.g., bilingual-mirror parity check appears in
  every entry). That'd compress 3 entries' worth of lessons into a smaller standing-rules
  doc, leaving retros for new lessons rather than re-asserting old ones.

