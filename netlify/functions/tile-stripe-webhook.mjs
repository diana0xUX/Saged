import crypto from "crypto";

const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = process.env.NOCODB_TOKEN;
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = process.env.NOCODB_TILE_TABLE;
const STRIPE_WHSEC = process.env.STRIPE_WEBHOOK_SECRET;

function verifyStripe(rawBody, header, secret) {
  const parts = Object.fromEntries(header.split(",").map(p => p.split("=")));
  const payload = `${parts.t}.${rawBody}`;
  const expected = crypto.createHmac("sha256", secret).update(payload, "utf8").digest("hex");
  if (Math.abs(Date.now() / 1000 - parseInt(parts.t)) > 300) throw new Error("stale");
  if (!crypto.timingSafeEqual(Buffer.from(expected, "hex"), Buffer.from(parts.v1, "hex"))) throw new Error("sig");
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
    return new Response(JSON.stringify({ ok: false, reason: "no match" }), { status: 200 });
  }

  const patchRes = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}/${row.Id}`,
    {
      method: "PATCH",
      headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify({ "Status": "paid", "Name": name, "Email": email }),
    }
  );

  return new Response(JSON.stringify({ ok: patchRes.ok }), { status: 200 });
};

export const config = { path: "/api/tile-stripe-webhook" };
