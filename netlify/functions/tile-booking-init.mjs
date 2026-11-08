const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = process.env.NOCODB_TOKEN;
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = process.env.NOCODB_TILE_TABLE;

export default async (request) => {
  if (request.method !== "POST") return new Response("OK", { status: 200 });

  let body;
  try { body = await request.json(); } catch { return new Response("Bad JSON", { status: 400 }); }

  const { date, time, people, amount } = body;
  if (!date || !time || !people || !amount) {
    return new Response("Missing fields", { status: 400 });
  }

  const row = {
    "Date":   date,
    "Time":   time,
    "People": parseInt(people),
    "Amount": parseFloat(amount),
    "Status": "pending",
  };

  const res = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}`,
    {
      method: "POST",
      headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
      body: JSON.stringify(row),
    }
  );

  const data = await res.json();
  return new Response(JSON.stringify({ ok: res.ok, id: data.Id }), {
    status: res.ok ? 200 : 500,
    headers: { "Content-Type": "application/json" },
  });
};

export const config = { path: "/api/tile-booking-init" };
