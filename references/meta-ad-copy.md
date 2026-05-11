# Meta ad copy — RU + UA, character-counted

For Meta Sales-objective campaigns once the FB Page + Pixel + Stripe are all green. Designed for **Reels / Stories / Feed video placements** using the `hero-ru.mp4` (id `959536350220678`) and `hero-ua.mp4` (id `1542298757583243`).

Character limits Meta enforces:
- **Primary text**: 125 chars before "see more" truncation (max 2,200)
- **Headline**: 27 chars before truncation (max 40)
- **Description**: 27 chars before truncation (max 30)
- **CTA**: Pre-defined list (BOOK_NOW, LEARN_MORE, SIGN_UP, GET_OFFER, etc.)

---

# 🇷🇺 Russian — Ad Set A

## Ad 1A — Process hook (slow, tactile, brand-led)

**Primary text** (122 chars — fits before truncation):
```
Два часа за столом с глиной. Курс из двух занятий, каждый четверг в старой Валенсии. €60 за обе встречи. Saged.club 🪷
```

**Headline** (24 chars):
```
Керамика с Корицей
```

**Description** (29 chars):
```
Каждый четверг · Валенсия
```

**CTA**: `BOOK_NOW` · destination: `https://saged.club/`

---

## Ad 2A — Outcome hook (what you take home)

**Primary text** (120 chars):
```
Лепим, обжигаем, глазуруем — забираешь домой свою керамику через две недели. €60 · до 6 человек · четверги в Валенсии.
```

**Headline** (24 chars):
```
Своё, сделано руками
```

**Description** (28 chars):
```
Saged.club · Старая Валенсия
```

**CTA**: `BOOK_NOW` · destination: `https://saged.club/`

---

# 🇺🇦 Ukrainian — Ad Set B

## Ad 1B — Process hook

**Primary text** (123 chars):
```
Дві години за столом з глиною. Курс із двох занять, щочетверга у старій Валенсії. €60 за обидві зустрічі. Saged.club 🪷
```

**Headline** (24 chars):
```
Кераміка з Корицею
```

**Description** (29 chars):
```
Щочетверга · Валенсія
```

**CTA**: `BOOK_NOW` · destination: `https://saged.club/uk/`

---

## Ad 2B — Outcome hook

**Primary text** (118 chars):
```
Ліпимо, випалюємо, глазуруємо — забираєш свою кераміку додому за два тижні. €60 · до 6 осіб · четверги у Валенсії.
```

**Headline** (24 chars):
```
Своє, зроблено руками
```

**Description** (28 chars):
```
Saged.club · Стара Валенсія
```

**CTA**: `BOOK_NOW` · destination: `https://saged.club/uk/`

---

# Campaign structure summary

When all the API blockers are resolved (Page access for System User), I'll build via Marketing API:

```
Campaign: Saged · Керамика с Корицей · Sales
├── Objective: OUTCOME_SALES
├── Optimization: PURCHASE (Pixel event from Cal.com confirmation)
├── Budget: €70 / 14-day run (auto-allocated across ad sets)
│
├── Ad Set A — Russian speakers · Valencia
│   ├── Location: Valencia + 25km radius
│   ├── Language: ru
│   ├── Age: 25-55
│   ├── Detailed targeting: Advantage+ Audience expansion enabled
│   ├── Daily budget: €5
│   └── Ads:
│       ├── Ad 1A — Process hook (video 959536350220678)
│       └── Ad 2A — Outcome hook (same video, different copy)
│
└── Ad Set B — Ukrainian speakers · Valencia
    ├── Location: Valencia + 25km radius
    ├── Language: uk
    ├── Age: 25-55
    ├── Detailed targeting: Advantage+ Audience expansion enabled
    ├── Daily budget: €5
    └── Ads:
        ├── Ad 1B — Process hook (video 1542298757583243)
        └── Ad 2B — Outcome hook (same video, different copy)
```

# Pre-launch verification checklist

Before flipping the campaign ACTIVE:

- [ ] Page assigned to System User claude (issue #40)
- [ ] Pixel firing PageView on saged.club (verified after consent — done)
- [ ] Pixel firing Purchase on Cal.com booking confirmation (need to verify after first real booking)
- [ ] Conversions API endpoint receiving events (System User token works — verified)
- [ ] Domain saged.club verified in Meta BM (done)
- [ ] AEM event priority: Purchase = #1
- [ ] Stripe activated for live charges
- [ ] Test booking with real card or test-mode passes

# Backup plan if API still blocks

Diana builds the campaign manually in Ads Manager using:
1. Videos already in library (`959536350220678` + `1542298757583243`)
2. This file's primary text / headline / description copy
3. The campaign structure tree above
4. Daily budget €5 per ad set
5. Geographic + language targeting per spec

Time: ~15 min in Ads Manager UI.
