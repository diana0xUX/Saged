import crypto from "crypto";

const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = process.env.NOCODB_TOKEN;
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = "mpxruyx8yk6w0ak";
const STRIPE_WHSEC = process.env.STRIPE_RAZOM_WEBHOOK_SECRET;
const MC_TOKEN     = process.env.MANYCHAT_TOKEN;

function verifyStripe(rawBody, header, secret) {
  const parts = Object.fromEntries(header.split(",").map(p => p.split("=")));
  const payload = `${parts.t}.${rawBody}`;
  const expected = crypto.createHmac("sha256", secret).update(payload, "utf8").digest("hex");
  if (Math.abs(Date.now() / 1000 - parseInt(parts.t)) > 300) throw new Error("stale");
  if (!crypto.timingSafeEqual(Buffer.from(expected, "hex"), Buffer.from(parts.v1, "hex"))) throw new Error("sig");
}

async function sendManyChat(email, name) {
  if (!MC_TOKEN) return;
  // Find subscriber by email
  const findRes = await fetch(
    `https://api.manychat.com/fb/subscriber/findBySystemField?field=email&value=${encodeURIComponent(email)}`,
    { headers: { Authorization: `Bearer ${MC_TOKEN}` } }
  );
  const findData = await findRes.json();
  const sub = findData.data?.[0];
  if (!sub) return;

  // Send confirmation DM
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
            text: `✅ Оплата отримана, ${name || "дякуємо"}!\n\nВаше місце на «Батьки і діти» заброньовано. Ми напишемо вам за день до заняття з нагадуванням та адресою.\n\nSaged Club · saged.club/razom/`
          }]
        }
      },
      message_tag: "CONFIRMED_EVENT_UPDATE"
    })
  });
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
    return new Response(JSON.stringify({ ok: false, reason: "sold out" }), { status: 200 });
  }

  await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}/${row.Id}`,
    {
      method: "PATCH",
      headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify({ Status: "paid", Name: name, Email: email }),
    }
  );

  await sendManyChat(email, name);

  return new Response(JSON.stringify({ ok: true }), { status: 200 });
};

export const config = { path: "/api/razom-stripe-webhook" };
