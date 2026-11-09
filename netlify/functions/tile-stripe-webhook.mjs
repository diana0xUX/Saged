import crypto from "crypto";

const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = process.env.NOCODB_TOKEN;
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = process.env.NOCODB_TILE_TABLE;
const STRIPE_WHSEC = process.env.STRIPE_WEBHOOK_SECRET;
const MC_TOKEN     = process.env.MANYCHAT_TOKEN;
const TG_TOKEN     = process.env.TELEGRAM_BOT_TOKEN;
const TG_CHAT_ID   = process.env.TELEGRAM_CHAT_ID;

function verifyStripe(rawBody, header, secret) {
  const parts = Object.fromEntries(header.split(",").map(p => p.split("=")));
  const payload = `${parts.t}.${rawBody}`;
  const expected = crypto.createHmac("sha256", secret).update(payload, "utf8").digest("hex");
  if (Math.abs(Date.now() / 1000 - parseInt(parts.t)) > 300) throw new Error("stale");
  if (!crypto.timingSafeEqual(Buffer.from(expected, "hex"), Buffer.from(parts.v1, "hex"))) throw new Error("sig");
}

async function sendTelegram(text) {
  if (!TG_TOKEN || !TG_CHAT_ID) return;
  await fetch(`https://api.telegram.org/bot${TG_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: TG_CHAT_ID, text, parse_mode: "HTML" }),
  });
}

async function sendManyChat(email, name) {
  if (!MC_TOKEN) return;
  const findRes = await fetch(
    `https://api.manychat.com/fb/subscriber/findBySystemField?field=email&value=${encodeURIComponent(email)}`,
    { headers: { Authorization: `Bearer ${MC_TOKEN}` } }
  );
  const findData = await findRes.json();
  const sub = findData.data?.[0];
  if (!sub) return;
  await fetch("https://api.manychat.com/fb/sending/send_content", {
    method: "POST",
    headers: { Authorization: `Bearer ${MC_TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      subscriber_id: sub.id,
      data: {
        version: "v2",
        content: {
          messages: [{
            type: "text",
            text: `✅ Payment received, ${name || "thank you"}!\n\nYour spot at the Spanish Tile Painting workshop is booked. We'll message you the day before with a reminder and address.\n\nSaged Club · saged.club/tile-painting/`
          }]
        }
      },
      message_tag: "CONFIRMED_EVENT_UPDATE"
    })
  });
}

// client_reference_id format: YYYYMMDD_HHMM_N (e.g. 20261115_1000_3)
function parseTileRef(ref) {
  if (!ref) return { date: "", time: "", people: 1 };
  const parts = ref.split("_");
  const raw = parts[0];
  const timePart = parts[1] || "";
  const peoplePart = parts[2] || "1";
  if (!raw || raw.length !== 8) return { date: "", time: timePart ? timePart.slice(0,2)+':'+timePart.slice(2) : "", people: parseInt(peoplePart) || 1 };
  const y = raw.slice(0,4), m = raw.slice(4,6), d = raw.slice(6,8);
  const time = timePart.length >= 4 ? timePart.slice(0,2)+':'+timePart.slice(2) : timePart;
  return { date: `${y}-${m}-${d}`, time, people: parseInt(peoplePart) || 1 };
}

export default async (request) => {
  const rawBody  = await request.text();
  const sigHeader = request.headers.get("stripe-signature") ?? "";

  if (STRIPE_WHSEC) {
    try { verifyStripe(rawBody, sigHeader, STRIPE_WHSEC); }
    catch { return new Response("Signature invalid", { status: 400 }); }
  }

  const event = JSON.parse(rawBody);
  if (event.type !== "checkout.session.completed") return new Response("OK", { status: 200 });

  const session = event.data.object;
  if (session.payment_status !== "paid") return new Response("OK", { status: 200 });

  const amountEur = session.amount_total / 100;
  const name  = session.customer_details?.name  ?? "";
  const email = session.customer_details?.email ?? "";
  const phone = session.customer_details?.phone ?? "";
  const { date, time, people } = parseTileRef(session.client_reference_id ?? "");

  // Find the most recent pending row with this amount
  const q = encodeURIComponent(`(Status,eq,pending)~and(Amount,eq,${amountEur})`);
  const listRes = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}?where=${q}&sort=-CreatedAt&limit=1`,
    { headers: { "xc-token": NOCODB_TOKEN } }
  );
  const listData = await listRes.json();
  const row = listData.list?.[0];

  if (!row) {
    console.error("[tile-stripe-webhook] no pending row for amount", amountEur);
    await sendTelegram(`⚠️ <b>Tile Painting</b>\nОплата отримана, але pending row не знайдено!\nІм'я: ${name}\nEmail: ${email}${date ? `\nДата: ${date}` : ""}${time ? ` · ${time}` : ""}\nСума: €${amountEur}`);
    return new Response(JSON.stringify({ ok: false, reason: "no match" }), { status: 200 });
  }

  const patchRes = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}/${row.Id}`,
    {
      method: "PATCH",
      headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify({ Status: "paid", Name: name, Email: email, Phone: phone, Date: date, Time: time, People: people }),
    }
  );

  await sendTelegram(`💳 <b>Нове бронювання — Tile Painting</b>\nІм'я: ${name}\nEmail: ${email}${phone ? `\nТел: ${phone}` : ""}${date ? `\nДата: ${date}` : ""}${time ? ` · ${time}` : ""}\nГостей: ${people}\nСума: €${amountEur}`);
  await sendManyChat(email, name);

  return new Response(JSON.stringify({ ok: patchRes.ok }), { status: 200 });
};

export const config = { path: "/api/tile-stripe-webhook" };
