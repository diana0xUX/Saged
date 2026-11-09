import crypto from "crypto";

const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = process.env.NOCODB_TOKEN;
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = "mpxruyx8yk6w0ak";
const STRIPE_WHSEC = process.env.STRIPE_RAZOM_WEBHOOK_SECRET;
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

async function sendManyChat(email, name, dateLabel) {
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
            text: `✅ Оплата отримана, ${name || "дякуємо"}!\n\nВаше місце на «Батьки і діти»${dateLabel ? ` (${dateLabel})` : ""} заброньовано. Ми напишемо вам за день до заняття з нагадуванням та адресою.\n\nSaged Club · saged.club/razom/`
          }]
        }
      },
      message_tag: "CONFIRMED_EVENT_UPDATE"
    })
  });
}

// client_reference_id format: YYYYMMDD_sub (субота) or YYYYMMDD_ned (неділя)
function parseDateRef(ref) {
  if (!ref) return { date: "", label: "" };
  const [raw, day] = ref.split("_");
  if (!raw || raw.length !== 8) return { date: "", label: "" };
  const y = raw.slice(0,4), m = raw.slice(4,6), d = raw.slice(6,8);
  const UA_MONTHS = ["січня","лютого","березня","квітня","травня","червня","липня","серпня","вересня","жовтня","листопада","грудня"];
  const mo = parseInt(m,10) - 1;
  const dayName = day === "sub" ? "субота" : "неділя";
  const lang = day === "sub" ? "укр" : "рус";
  return {
    date: `${y}-${m}-${d}`,
    label: `${dayName}, ${parseInt(d,10)} ${UA_MONTHS[mo]} · 12:00 · ${lang}`,
  };
}

export default async (request) => {
  const rawBody   = await request.text();
  const sigHeader = request.headers.get("stripe-signature") ?? "";

  if (STRIPE_WHSEC) {
    try { verifyStripe(rawBody, sigHeader, STRIPE_WHSEC); }
    catch { return new Response("Signature invalid", { status: 400 }); }
  }

  const event = JSON.parse(rawBody);
  if (event.type !== "checkout.session.completed") return new Response("OK", { status: 200 });

  const session = event.data.object;
  if (session.payment_status !== "paid") return new Response("OK", { status: 200 });

  const name  = session.customer_details?.name  ?? "";
  const email = session.customer_details?.email ?? "";
  const { date, label } = parseDateRef(session.client_reference_id ?? "");

  // Find oldest open slot
  const q = encodeURIComponent("(Status,eq,open)");
  const listRes = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}?where=${q}&sort=CreatedAt&limit=1`,
    { headers: { "xc-token": NOCODB_TOKEN } }
  );
  const listData = await listRes.json();
  const row = listData.list?.[0];

  if (!row) {
    console.error("[razom-stripe-webhook] no open slots");
    await sendTelegram(`⚠️ <b>Батьки і діти</b>\nОплата отримана, але вільних місць немає!\nІм'я: ${name}\nEmail: ${email}${label ? `\nДата: ${label}` : ""}`);
    return new Response(JSON.stringify({ ok: false, reason: "sold out" }), { status: 200 });
  }

  await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}/${row.Id}`,
    {
      method: "PATCH",
      headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify({ Status: "paid", Name: name, Email: email, Date: date }),
    }
  );

  await sendTelegram(`💳 <b>Нове бронювання — Батьки і діти</b>\nІм'я: ${name}\nEmail: ${email}${label ? `\nДата: ${label}` : ""}\nСума: €50`);
  await sendManyChat(email, name, label);

  return new Response(JSON.stringify({ ok: true }), { status: 200 });
};

export const config = { path: "/api/razom-stripe-webhook" };
