# Intake templates — "where did you find us?"

**Epic:** [#111 Social media mediaplan](https://github.com/diana0xUX/Saged/issues/111)
**Related:** [#113 Lena trial · Reel concept research + shoot brief](https://github.com/diana0xUX/Saged/issues/113), [`social-measurement-sheet.md`](social-measurement-sheet.md)
**Purpose:** copy-paste templates for the intake question that closes the attribution loop for the Lena 4-week trial.

---

## WhatsApp first-reply templates

Drop the "where did you find us" line **after Diana's greeting**, **before logistics**. Phrasing chosen to feel like genuine curiosity, not a survey. One soft emoji (🌿) to match Saged's voice; cut it if it feels too much for Diana's natural tone.

### Russian (primary audience)

> Здравствуйте! Спасибо, что написали. Я Диана, основательница Saged.
>
> Маленький вопрос для начала — как вы нас нашли? (Reels, сторис, кто-то порекомендовал, Гугл — что-то ещё?) Помогает понимать, что работает 🌿
>
> *[затем логистика про конкретный класс / коворкинг / детский урок]*

### Ukrainian

> Доброго дня! Дякую, що написали. Я Діана, засновниця Saged.
>
> Маленьке питання спочатку — як ви нас знайшли? (Reels, сторіс, хтось порадив, Google — щось інше?) Допомагає розуміти, що працює 🌿
>
> *[потім логістика про конкретний клас / коворкінг / дитячий урок]*

### English

> Hi! Thanks for reaching out. I'm Diana, founder of Saged.
>
> Quick one before we dive in — where did you hear about us? (Reels, Stories, friend, Google — somewhere else?) Helps me see what's working 🌿
>
> *[then logistics about the specific class / coworking / kids class]*

### Voice notes for adapting

- Drop the emoji if it feels off — the line works without it
- "Маленький вопрос для начала" / "Quick one before we dive in" cushions the ask. Don't lead with the question naked — it reads as a form.
- Reasoning "Помогает понимать, что работает" / "Helps me see what's working" makes it feel like genuine sharing, not market research
- If lead has already mentioned in their first message where they came from (e.g. "Saw your Reel about..."), **skip the question** and log it directly. Don't ask redundantly.

---

## Cal.com — custom question on adult workshop event

Cal.com supports custom booking-form questions per event type. We're adding ONE dropdown to the recurring adult Thursday workshop event.

### What to add

| Field | Value |
|---|---|
| Question type | Dropdown / Single-select |
| Identifier | `where-found` |
| Label (EN) | Where did you hear about us? |
| Label (RU) | Как вы нас нашли? |
| Label (UA) | Як ви нас знайшли? |
| Options | Instagram — Reel · Instagram — Story · Instagram — post · TikTok · Friend / referral · Google · Other |
| Required | **No** (less friction at checkout — better to lose attribution than lose the booking) |
| Show on | Booking form |

### Path A — Cal.com UI (~2 minutes, no setup)

If Diana wants to ship it right now:

1. Go to **cal.com** → Event Types
2. Open the **adult Thursday workshop** event ("Керамика с Корицей" or whatever it's called)
3. Tab: **Advanced** → scroll to **Booking questions** (or **Questions** depending on UI version)
4. Click **Add a question** (or **+** button)
5. Type: **Dropdown** / **Multiple choice** (single-select)
6. Fill in the fields per the table above
7. **Save**

That's the whole thing. Done.

### Path B — Cal.com API (~10 min setup, then automated)

If we want to script this (and any future Cal.com changes), Diana adds her Cal.com API key to `.env`:

```
CAL_COM_API_KEY=cal_live_...
```

Path to get it: cal.com → Settings → Developer → API keys → Create. Scope: read + write on event types.

Then I run a one-time script that PATCHes the event type with the custom booking field via Cal.com API v2.

**Recommendation:** Path A. Cal.com UI is fast for a one-off; setting up API access is overkill for one field. Switch to API only if we end up wanting to script multiple events later.

---

## In-class casual ask

When a new student starts their first session, Korytsia / Vita / Diana drop one casual line in passing:

> "Слушай, а как ты вообще про нас узнала?"
> *(plain conversational, not a script)*

→ Log answer in the tracking sheet within 24h of the class.

Don't make it a formal survey. People remember "Instagram" generally; probe gently for "which post specifically" if they're chatty.

---

## What this unlocks

Once the WhatsApp template + Cal.com question are live:

- Every new lead has a high-probability attribution to a channel (or `IG-untagged` if they're vague)
- The measurement sheet's "Bookings ascribed" column can be filled honestly
- Lena's 4-week pilot has a comparable baseline
- The 1.5× decision rule becomes computable, not vibes-based

Without this, the Lena trial measurement is theatre.

---

## Implementation status

- [ ] WhatsApp templates: pasted into Diana's WhatsApp chat shortcuts / saved replies (or printed near her desk if she replies manually)
- [ ] Cal.com question added (Path A or Path B)
- [ ] Korytsia + Vita briefed on the in-class ask (one sentence in passing)
- [ ] First booking with `where-found = Reel` logged → confirms the pipeline works end-to-end
