# Skill: Launching a New Paid Event

Reusable playbook for every new Saged workshop or event that needs a landing page, online payment, booking log, ManyChat confirmation message, and Meta ads.

**First used:** Spanish Tile Painting workshop, November 2026

---

## Quick checklist

- [ ] 1. Create the landing page
- [ ] 2. Create Stripe payment links (one per guest count)
- [ ] 3. Create NocoDB booking table
- [ ] 4. Deploy Netlify booking functions
- [ ] 5. Create Stripe webhook
- [ ] 6. Set up ManyChat flow
- [ ] 7. Create Meta ads
- [ ] 8. Final live check

---

## 1. Landing page

### File location
Create a new folder: `{event-slug}/index.html`
Example: `tile-painting/index.html`

Copy the tile-painting page as the starting template — it has all the right sections and CSS.

### Hero image
- Use `object-fit: cover` + `object-position: center top` so the subject's face appears below the text, not behind it.
- On mobile (`max-width: 600px`): hide `.hero-desc`, reduce `.hero h1` to `1.75rem`.

### Booking section structure (Airbnb-style)
```
Eyebrow (event name)
Large heading "Book your workshop"
Price per person
Materials/inclusions line
─── divider ───
Guests stepper (1–N)
─── divider ───
Date chips (grouped by month, horizontal scroll)
  Month nav ‹ November 2026 ›
  [Mon 10] [Tue 11] [Wed 12] ...
Time cards (side by side)
  [10:00–12:00 Morning ✓]  [14:00–16:00 Afternoon ✓]
─── sticky bottom bar ───
  Wed 11 Nov · 10:00–12:00     Total: €180
  [Continue to payment]
  🔒 Secure payment via Stripe
```

### Key JS constants to update per event
```javascript
const PRICE_PER_PERSON = 60;       // € price
const MAX_PEOPLE = 10;             // max group size
const VALID_DAYS = [1, 2, 3, 5];  // 0=Sun 1=Mon ... 6=Sat
const WEEKS_AHEAD = 4;             // how many weeks to show
```

### Book button click handler (always use this pattern)
The button first logs a pending booking to NocoDB, then opens Stripe:
```javascript
document.getElementById('book-btn').addEventListener('click', async function(e) {
  e.preventDefault();
  const href = this.href;
  if (!href || href === '#') return;

  const total   = people * PRICE_PER_PERSON;
  const dateISO = selectedDate ? selectedDate.toISOString().split('T')[0] : '';

  try {
    await fetch('/api/{event-slug}-booking-init', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: dateISO, time: selectedTime, people, amount: total }),
    });
  } catch (_) {}

  // Anchor-click pattern — preserves iOS deep-link / wa.me behaviour
  const a = document.createElement('a');
  a.href = href; a.target = '_blank'; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); a.remove();
});
```

---

## 2. Stripe payment links

### Why one link per guest count
Static payment links have a fixed price. The right total must be pre-baked into the link so the customer can't change it.

### Create prices and links via API (one-time script)

```python
import stripe, os

stripe.api_key = os.environ["STRIPE_SK"]   # never hardcode

PRICE_PER_PERSON = 60  # update per event
EVENT_NAME = "Spanish Tile Painting"
CURRENCY = "eur"

# Reuse existing product if one exists, or create:
# product = stripe.Product.create(name=EVENT_NAME)
product_id = "prod_XXXX"   # paste existing product id here

links = {}
for n in range(1, 11):
    total = PRICE_PER_PERSON * n
    price = stripe.Price.create(
        product=product_id,
        unit_amount=total * 100,
        currency=CURRENCY,
    )
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        # Lock quantity — customer cannot change it
    )
    links[n] = link.url
    print(f"{n}: '{link.url}',")
```

Run with: `STRIPE_SK=sk_live_... python3 stripe_create_links.py`
Paste the output into the page as `STRIPE_LINKS`.

### Finding an existing product
```bash
stripe products list --limit 20 --api-key sk_live_...
```

---

## 3. NocoDB booking table

### Create via API (do not create manually in the UI — API is faster and repeatable)

```bash
curl -X POST "https://admin.saged.club/api/v1/db/meta/projects/p2txdvaha72xsn4/tables" \
  -H "xc-token: $NOCODB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{Event Name} Bookings",
    "columns": [
      {"title": "Date",    "uidt": "Date"},
      {"title": "Time",    "uidt": "SingleLineText"},
      {"title": "People",  "uidt": "Number"},
      {"title": "Amount",  "uidt": "Currency"},
      {"title": "Status",  "uidt": "SingleLineText"},
      {"title": "Name",    "uidt": "SingleLineText"},
      {"title": "Email",   "uidt": "Email"},
      {"title": "Notes",   "uidt": "LongText"}
    ]
  }'
```

Save the returned `id` — you need it for the Netlify function.

### Add Netlify env vars
```bash
netlify env:set NOCODB_TOKEN "niIrlNav-3NkyiB82YDtPznbKLfhs0pptRIg4HKb"
netlify env:set NOCODB_{EVENT}_TABLE "{returned table id}"
```

---

## 4. Netlify booking functions

Create two files in `netlify/functions/`. Use `tile-booking-init.mjs` and `tile-stripe-webhook.mjs` as templates — just replace the env var name and path.

### `{event}-booking-init.mjs`
- Path: `/api/{event-slug}-booking-init`
- Receives: `{ date, time, people, amount }`
- Writes NocoDB row: Status=pending
- Returns: `{ ok, id }`

### `{event}-stripe-webhook.mjs`
- Path: `/api/{event-slug}-stripe-webhook`
- Receives: Stripe `checkout.session.completed` webhook
- Verifies `Stripe-Signature` header with `STRIPE_WEBHOOK_SECRET_{EVENT}` env var
- Finds most recent pending NocoDB row where Amount matches
- Updates: Status=paid, Name, Email from Stripe customer_details

The matching logic (time-window is optional since volume is low):
```javascript
const q = encodeURIComponent(`(Status,eq,pending)~and(Amount,eq,${amountEur})`);
// sort=-CreatedAt, limit=1 → always picks the most recent pending match
```

Deploy after writing: `netlify deploy --prod`

---

## 5. Stripe webhook

```bash
curl -X POST https://api.stripe.com/v1/webhook_endpoints \
  -u "sk_live_...:" \
  -d "url=https://saged.club/api/{event-slug}-stripe-webhook" \
  -d "enabled_events[]=checkout.session.completed" \
  -d "description={Event Name} booking confirmation"
```

The response includes `"secret": "whsec_..."` — add it to Netlify:
```bash
netlify env:set STRIPE_WEBHOOK_SECRET_{EVENT} "whsec_..."
netlify deploy --prod
```

---

## 6. ManyChat confirmation flow

**What this does:** when someone pays, they get a WhatsApp/Instagram DM confirming the date, time, and what to bring.

### Get a valid API token
ManyChat Settings → Integrations → API → Generate new token.
Save it: `netlify env:set MANYCHAT_TOKEN "..."`

The stored token for this account is in `.env` as `MANYCHAT_TOKEN`. **If it returns "Wrong token", regenerate it from ManyChat — tokens expire or get revoked.**

### Add ManyChat messaging to the stripe webhook function

After marking the NocoDB row as paid, look up the subscriber by email and send a flow:

```javascript
const MANYCHAT_TOKEN = process.env.MANYCHAT_TOKEN;

// 1. Find subscriber by email
const findRes = await fetch(
  `https://api.manychat.com/fb/subscriber/findBySystemField?field_name=email&field_value=${encodeURIComponent(email)}`,
  { headers: { "Authorization": `Bearer ${MANYCHAT_TOKEN}` } }
);
const findData = await findRes.json();
const subscriberId = findData.data?.id;

// 2. If found, send the booking confirmation flow
if (subscriberId) {
  await fetch("https://api.manychat.com/fb/sending/sendFlow", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${MANYCHAT_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      subscriber_id: subscriberId,
      flow_ns: "content20240101000000_XXXXXX",  // paste flow ID from ManyChat
    }),
  });
}
```

### Create the confirmation flow in ManyChat
1. ManyChat → Flows → New Flow → name it "{Event} Booking Confirmation"
2. Add a message block: "✅ Бронирование подтверждено! Вы записаны на {date} в {time}. Адрес: Carrer del Mossèn Femades 10, Валенсия. Возьмите с собой хорошее настроение — остальное мы обеспечим 🎨"
3. Copy the flow namespace (`content20240101...`) from the URL bar and paste it into the webhook function.
4. Set Custom Field values in the flow trigger to pass date/time — or hardcode into the message since each event has fixed sessions.

**Limitation:** ManyChat can only message people who have already interacted with the bot (opted in). New customers from Stripe who have never messaged won't receive it. For cold customers, the Stripe receipt email is the only confirmation.

---

## 7. Meta ads

Follow `CLAUDE.md` → "Meta Ads — always fix these" section. Mandatory every time:

| Setting | Value |
|---------|-------|
| Objective | `OUTCOME_TRAFFIC` |
| Geo | Valencia city key — verify via `/search?type=adgeolocation` at runtime |
| Location type | `home` only |
| Locale | Verify via `/search?type=adlocale` at runtime — never hardcode |
| Ad sets | Separate for RU and UA — never merge |
| Bid strategy | `LOWEST_COST_WITHOUT_CAP` |
| Targeting automation | `{"advantage_audience": 0}` |
| All entities | Created as PAUSED — Diana activates |
| Age | Never above 54 |

Script template: `scripts/local/build-meta-campaign.sh` (has `verify_locale()` and `verify_city_key()` guards).

**Events are organic-only. Never run paid ads for events.**

---

## 8. Final live check

Before telling Diana it's ready:

1. Open the page on mobile (phone or Chrome DevTools mobile view)
   - Hero: subject's face visible above text
   - Booking section scrolls correctly, chips are tappable
   - Sticky bar appears after selecting date + time

2. Click "Continue to payment" with a test selection
   - Check NocoDB table — a pending row should appear immediately
   - Confirm Stripe opens in new tab with the correct amount

3. Verify Stripe webhook is active:
   ```bash
   curl -s https://api.stripe.com/v1/webhook_endpoints \
     -u "sk_live_...:" | python3 -c "import sys,json; [print(w['url'], w['status']) for w in json.load(sys.stdin)['data']]"
   ```

4. Check Netlify functions are deployed:
   ```bash
   curl -X POST https://saged.club/api/{event-slug}-booking-init \
     -H "Content-Type: application/json" \
     -d '{"date":"2026-11-10","time":"10:00","people":2,"amount":120}'
   ```
   Should return `{"ok":true,"id":...}` and create a row in NocoDB.

---

## Known gotchas

- **A5 print flyers:** `overflow: hidden` clips content silently — always check footer is visible after any structural change. See `CLAUDE.md` § "A5 print HTML".
- **wa.me deep links from JS:** use the anchor-click pattern, not `window.open`. See `CLAUDE.md` § "wa.me deep-link from JavaScript".
- **Stripe payment link quantities:** creating a price with `unit_amount` and a payment link with `quantity: 1` locks the total. The customer sees the right price but cannot change the headcount — that's intentional.
- **ManyChat token format:** ManyChat API tokens are long strings from Settings → Integrations → API. The format `12345:hexstring` is not a valid ManyChat token format and will return "Wrong token" — regenerate from the dashboard.
- **NocoDB row matching:** if two people book the same guest count within seconds of each other, the webhook picks the most recent pending row. At current volume this is fine.
