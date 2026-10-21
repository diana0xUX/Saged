const NOCODB_URL   = "https://admin.saged.club";
const NOCODB_TOKEN = "niIrlNav-3NkyiB82YDtPznbKLfhs0pptRIg4HKb";
const NOCODB_BASE  = "p2txdvaha72xsn4";
const NOCODB_TABLE = "mzerh9imrwgjmuf"; // Booking Handpan School

export default async (request) => {
  if (request.method !== "POST") return new Response("OK", { status: 200 });

  let payload;
  try { payload = await request.json(); } catch { return new Response("Bad JSON", { status: 400 }); }

  const booking   = payload.payload ?? payload;
  const attendee  = booking.attendees?.[0] ?? {};
  const responses = booking.responses ?? {};
  const promoCode = booking.metadata?.promo ?? "";
  const amount    = promoCode ? 25 : 30;

  const row = {
    "Name":           responses.name?.value  ?? attendee.name  ?? "",
    "Email":          responses.email?.value ?? attendee.email ?? "",
    "Phone":          responses.attendeePhoneNumber?.value ?? "",
    "Date":           booking.startTime?.split("T")[0] ?? "",
    "Amount":         amount,
    "Final Amount":   amount,
    "Promo Code":     promoCode,
    "Payment":        "Stripe",
    "Booking Status": "Confirmed",
    "Notes":          responses.notes?.value ?? "",
  };

  const res = await fetch(`${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}`, {
    method: "POST",
    headers: { "xc-token": NOCODB_TOKEN, "Content-Type": "application/json" },
    body: JSON.stringify(row),
  });

  return new Response(JSON.stringify({ ok: res.ok }), { status: res.ok ? 200 : 500 });
};

export const config = { path: "/api/calcom-webhook" };
