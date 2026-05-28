# Instagram FAQ menu — @saged.club

Auto-reply chips that appear in the IG DM thread before the person types anything. They tap a question → IG sends the pre-written answer.

**Limits:** 4 FAQs max · question chip ~30 chars · answer ~500 chars · one language per FAQ entry.

**Strategy:** primary language is Russian (main audience). UA fallback is handled manually via the lead-handling playbook — don't try to dual-language inside the auto-reply, it gets noisy.

Each chip covers all three products briefly with emoji prefixes — 🪻 adult course / 🌻 kids class / 🌾 coworking — so a parent or potential coworker recognises their option without tapping the wrong chip first. Every answer ends with a routing question that asks them to pick a format.

Tone matches `docs/lead-handling.md`: warm, plain, ends with a specific next-step question.

---

## The 4 FAQs (in display order)

Live on `@saged.club` as of 2026-05-28.

### 1. Question chip: `Сколько стоит? Что входит в цену?`

Combines the price + value question into one chip — both came in DMs frequently enough that one chip serves both.

Answer (RU):
```
🪻 Взрослый курс — 60 € за 2 встречи по 2 часа
🌻 Детский класс (6–10 лет) — 25 € за 1,5 часа
🌾 Коворкинг — 200 €/мес

В цену входит всё: глина, инструменты, оба обжига, глазурь, чай. Группа до 6 человек.

Что вас интересует?
```

### 2. Question chip: `Где студия?`

Answer (RU):
```
C/ de les Cuines, 8 — старый город Валенсии, в двух шагах от Mercat Central.

Метро Xàtiva — 5 минут пешком, Àngel Guimerà — 7 минут. Парковка в центре сложная — лучше метро или велосипед.

Какой формат интересует — взрослый курс, детский класс или коворкинг?
```

### 3. Question chip: `Как записаться?`

Answer (RU):
```
Зависит от формата:

🪻 Взрослый курс (60 €): выберите четверг и время на saged.club → "Записаться"
🌻 Детский класс (25 €): добавим в список ожидания → позовём, когда соберётся 4–6 детей
🌾 Коворкинг (200 €/мес): напишите сюда, расскажем условия

Что выбираете?
```

### 4. Question chip: `На каком языке?`

Answer (RU):
```
Кориця говорит на украинском и русском — выбираете комфортный.

Английский — базовые инструкции переводим легко, и для детей, и для взрослых.

Si hablas español — escríbenos, разберёмся вместе.

Какой формат вам интересен?
```

---

## UA versions (for manual reply if someone writes in Ukrainian)

### 1. Скільки коштує? Що входить у ціну?
```
🪻 Курс для дорослих — 60 € за 2 зустрічі по 2 години
🌻 Дитячий клас (6–10 років) — 25 € за 1,5 години
🌾 Коворкінг — 200 €/міс

У ціну входить усе: глина, інструменти, обидва випали, глазур, чай. Група до 6 осіб.

Що вас цікавить?
```

### 2. Де студія?
```
C/ de les Cuines, 8 — старе місто Валенсії, поруч із Mercat Central.

Метро Xàtiva — 5 хвилин пішки, Àngel Guimerà — 7 хвилин. У центрі паркуватися складно, краще метро чи велосипед.

Який формат вас цікавить — дорослий курс, дитячий клас чи коворкінг?
```

### 3. Як записатися?
```
Залежить від формату:

🪻 Дорослий курс (60 €): оберіть четвер і час на saged.club → "Записатися"
🌻 Дитячий клас (25 €): додамо у список очікування → покличемо, коли збереться 4–6 дітей
🌾 Коворкінг (200 €/міс): напишіть сюди, розкажемо умови

Що обираєте?
```

### 4. Якою мовою?
```
Кориця розмовляє українською та російською — оберіть зручнішу.

Англійською — базові інструкції перекладаємо легко, і для дітей, і для дорослих.

Si hablas español — escríbenos, розберемося разом.

Який формат вас цікавить?
```

---

## Where to set it up

**Instagram mobile app (Creator account required).** The feature was removed from Meta Business Suite Automations sometime before 2026-05-28 — Diana confirmed Business Suite no longer shows an FAQ template; the IG mobile app is the only surface.

Steps in the IG app:
1. Profile → ☰ menu (top-right) → look for "Frequently asked questions" (or scroll the long list)
2. Tap to open the FAQ settings — shows up to 4 question slots
3. Add each question + answer pair from above
4. Toggle **Show Questions** ON at the top
5. Test: DM @saged.club from a personal IG account — the 4 chips should appear at the top of the new thread

**Account type prerequisite:** the IG account must be set to **Creator** (not Personal). Business accounts may or may not see this feature depending on app version — Creator is the reliable path. Switching account type doesn't affect the connected FB Page or ad account.

**API automation (future):** see #103. Blocked on `pages_messaging` + `instagram_manage_messages` scopes + Meta App Review.

---

## When to update this doc

Add new questions to this doc (not to IG directly) whenever:
- The same question shows up in 3+ DMs in a week
- A campaign creative raises a new concern (e.g., "is it just for women?")
- An answer above gets a follow-up "but what about…?" — that's the real question

Bump the IG menu only when one of the current 4 stops earning taps. Don't expand past 4 — the chip stack gets ignored.

After any chip edit in this doc, mirror the change in the IG mobile app (no API path yet — see #103).

---

## What's NOT here (and why)

- **"Нужен ли опыт?"** — strong question but lower priority than price / location / booking / language. Covered by the greeting auto-reply and `docs/lead-handling.md`. If a chip's tap volume drops to near zero, swap it back in.
- **"Когда ближайшее занятие?"** — would be a strong 5th chip (schedule is the most actionable question), but Meta caps the menu at 4. The booking chip routes this for adult Thursdays; kids waitlist is handled in live reply.
- **"Подарочный сертификат / пропущу вторую встречу"** — niche follow-ups, low DM volume. Answered live or via `docs/lead-handling.md`.
- **Coworking-specific deep questions** (схема студии, hours, intro course details) — chip 3 routes them to write back. Coworking is the slowest seller; high-touch DM works fine without auto-chips.
- **Bot escalation rules** — high-touch audience, conversion lives in human reply. The auto-reply is the opener, not the closer.
