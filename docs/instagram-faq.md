# Instagram FAQ menu — @saged.club

Auto-reply chips that appear in the IG DM thread before the person types anything. They tap a question → IG sends the pre-written answer.

**Limits:** 4 FAQs max · question chip ~30 chars · answer ~500 chars · one language per FAQ entry.

**Strategy:** primary language is Russian (main audience). UA fallback is handled manually via the lead-handling playbook — don't try to dual-language inside the auto-reply, it gets noisy.

Tone matches `docs/lead-handling.md`: warm, plain, ends with a specific next-step question.

---

## The 4 FAQs (in this order)

### 1. Question chip: `Сколько стоит?`

Answer (RU):
```
Курс — 60 €. Это две встречи по 2 часа:
🪷 первая — лепим руками
🪷 вторая, через неделю — глазурь и обжиг

В цену входит вся глина, инструменты, все обжиги, чай. Группа до 6 человек.

Ближайший четверг — какое время удобнее: 12:00, 15:00 или 19:00?
```

### 2. Question chip: `Где студия?`

Answer (RU):
```
C/ de les Cuines, 8 — старый город Валенсии, в двух шагах от Mercat Central.

Метро Xàtiva — 5 минут пешком, Àngel Guimerà — 7 минут. Парковка в центре сложная, лучше метро или велосипед.

Подсказать ближайший четверг?
```

### 3. Question chip: `Нужен ли опыт?`

Answer (RU):
```
Совсем нет. Большинство впервые трогают глину 🪷

Корица ведёт каждого с нуля, в вашем темпе. Не нужно "получаться" — нужно прийти и провести 2 часа руками в глине.

Хотите забронировать четверг?
```

### 4. Question chip: `Как записаться?`

Answer (RU):
```
Просто выберите четверг и время: 12:00, 15:00 или 19:00 — напишите сюда или в WhatsApp +34 605 54 33 00.

Мы подтвердим место и пришлём ссылку на оплату. Бронь — минимум за день до встречи.

Какой четверг подходит?
```

---

## UA versions (for manual reply if someone writes in Ukrainian)

### 1. Скільки коштує?
```
Курс — 60 €. Це дві зустрічі по 2 години:
🪷 перша — ліпите руками
🪷 друга, за тиждень — глазур і випал

У ціну входить уся глина, інструменти, усі випали, чай. Група до 6 осіб.

Найближчий четвер — який час зручніше: 12:00, 15:00 чи 19:00?
```

### 2. Де студія?
```
C/ de les Cuines, 8 — старе місто Валенсії, поруч із Mercat Central.

Метро Xàtiva — 5 хвилин пішки, Àngel Guimerà — 7 хвилин. У центрі паркуватися складно, краще метро чи велосипед.

Підказати найближчий четвер?
```

### 3. Чи потрібен досвід?
```
Зовсім ні. Більшість уперше торкаються глини 🪷

Кориця веде кожного з нуля, у вашому темпі. Не треба, щоб "вийшло" — треба прийти і провести 2 години руками в глині.

Хочете забронювати четвер?
```

### 4. Як записатися?
```
Просто оберіть четвер і час: 12:00, 15:00 чи 19:00 — напишіть сюди або у WhatsApp +34 605 54 33 00.

Ми підтвердимо місце і надішлемо посилання на оплату. Бронь — мінімум за день до зустрічі.

Який четвер підходить?
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

- "Можно ли с детьми / подарочный сертификат / пропущу вторую" — already answered on the site FAQ, lower DM volume. Keep them on the page, not in the IG menu.
- A "цены и пакеты" carousel — premature. One offer, one price right now.
- Bot escalation rules — high-touch audience, conversion lives in human reply. Auto-reply is the opener, not the closer.
