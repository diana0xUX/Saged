# Instagram FAQ menu — @saged.club

Auto-reply chips that appear in the IG DM thread before the person types anything. They tap a question → IG sends the pre-written answer.

**Limits:** 4 FAQs max · question chip ~30 chars · answer ~500 chars · one language per FAQ entry.

**Strategy:** primary language is Russian (main audience). UA fallback is handled manually via the lead-handling playbook — don't try to dual-language inside the auto-reply, it gets noisy.

Each chip covers all three products briefly with emoji prefixes — 🪻 adult course / 🌻 kids class / 🌾 coworking — so a parent or potential coworker recognises their option without tapping the wrong chip first. Every answer ends with a routing question that asks them to pick a format.

Tone matches `docs/lead-handling.md`: warm, plain, ends with a specific next-step question.

---

## The 4 FAQs (in this order)

### 1. Question chip: `Сколько стоит?`

Answer (RU):
```
🪻 Взрослый курс — 60 € · 2 встречи по 2 часа, каждый четверг
🌻 Детский класс (6–10 лет) — 25 € · 1,5 часа
🌾 Коворкинг для гончаров — 200 € в месяц

Всё включено: глина, инструменты, обжиг, глазурь, чай.

Что из этого вас интересует?
```

### 2. Question chip: `Где студия?`

Answer (RU):
```
C/ de les Cuines, 8 — старый город Валенсии, в двух шагах от Mercat Central.

Метро Xàtiva — 5 минут пешком, Àngel Guimerà — 7 минут. Парковка в центре сложная, лучше метро или велосипед.

Какой формат интересует — взрослый курс, детский класс или коворкинг?
```

### 3. Question chip: `Нужен ли опыт?`

Answer (RU):
```
Совсем нет 🪷

Большинство впервые трогают глину — и на взрослом курсе, и на детском классе. Кориця ведёт каждого с нуля, в вашем темпе.

Какой формат интересует?
```

### 4. Question chip: `Как записаться?`

Answer (RU):
```
Зависит от формата:

🪻 Взрослый курс (60 €): выберите четверг и время на saged.club → "Записаться"
🌻 Детский класс (25 €): добавим в список ожидания → позовём, когда соберётся 4–6 детей
🌾 Коворкинг (200 €/мес): напишите сюда, расскажем условия

Что выбираете?
```

---

## UA versions (for manual reply if someone writes in Ukrainian)

### 1. Скільки коштує?
```
🪻 Курс для дорослих — 60 € · 2 зустрічі по 2 години, щочетверга
🌻 Дитячий клас (6–10 років) — 25 € · 1,5 години
🌾 Коворкінг для гончарів — 200 € на місяць

Усе включено: глина, інструменти, випал, глазур, чай.

Що з цього вас цікавить?
```

### 2. Де студія?
```
C/ de les Cuines, 8 — старе місто Валенсії, поруч із Mercat Central.

Метро Xàtiva — 5 хвилин пішки, Àngel Guimerà — 7 хвилин. У центрі паркуватися складно, краще метро чи велосипед.

Який формат вас цікавить — дорослий курс, дитячий клас чи коворкінг?
```

### 3. Чи потрібен досвід?
```
Зовсім ні 🪷

Більшість уперше торкаються глини — і на дорослому курсі, і на дитячому класі. Кориця веде кожного з нуля, у вашому темпі.

Який формат цікавить?
```

### 4. Як записатися?
```
Залежить від формату:

🪻 Дорослий курс (60 €): оберіть четвер і час на saged.club → "Записатися"
🌻 Дитячий клас (25 €): додамо у список очікування → покличемо, коли збереться 4–6 дітей
🌾 Коворкінг (200 €/міс): напишіть сюди, розкажемо умови

Що обираєте?
```

---

## Where to set it up

Meta Business Suite (web — easiest):

1. Open `business.facebook.com` → log in with the @saged.club connected account
2. Left sidebar → **Inbox**
3. Top-right of inbox → gear icon ⚙️ → **Automated responses**
4. Scroll to **Frequently Asked Questions** (часто задаваемые вопросы) → toggle **On**
5. Channel: select **Instagram** (Facebook can be added later if needed)
6. Add the 4 question/answer pairs above, in order
7. Save

Mobile alt (IG app):
- Profile → ☰ menu → **Business tools** → **Saved replies / FAQs**
- Same 4 pairs

**Test it once:** message @saged.club from a personal IG account. The 4 chips should appear at the top of the new thread.

---

## When to update this doc

Add new questions to this doc (not to IG directly) whenever:
- The same question shows up in 3+ DMs in a week
- A campaign creative raises a new concern (e.g., "is it just for women?")
- An answer above gets a follow-up "but what about…?" — that's the real question

Bump the IG menu only when one of the current 4 stops earning taps. Don't expand past 4 — the chip stack gets ignored.

---

## What's NOT here (and why)

- "Подарочный сертификат / пропущу вторую встречу" — niche follow-ups, low DM volume. Answered live or via `docs/lead-handling.md`.
- Coworking-specific deep questions (схема студии, hours, intro course details) — chip 4 routes them to write back ("напишите сюда, расскажем"). Coworking is the slowest seller; high-touch DM works fine without auto-chips.
- Bot escalation rules — high-touch audience, conversion lives in human reply. The auto-reply is the opener, not the closer.
- Adult-course-specific timing nuance (Thursday slots 12/15/19) — fits chip 4 inline; full slot list goes into the live chat once the parent has picked "adult".
