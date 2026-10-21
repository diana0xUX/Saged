/**
 * Cal.com → NocoDB webhook handler
 * Receives a Cal.com booking event and creates a row in "Booking Handpan School"
 *
 * Deploy options (all free):
 *   A) Cloudflare Worker — paste into workers.cloudflare.com → Create Worker
 *   B) Val.town          — paste into val.town → New Val → HTTP handler
 *   C) Vercel Function   — save as /api/calcom-webhook.js in a Vercel project
 *
 * Then set the deployed URL as a Cal.com webhook:
 *   Cal.com → Settings → Webhooks → New webhook → paste URL → trigger: BOOKING_CREATED
 */

const NOCODB_URL    = "https://admin.saged.club";
const NOCODB_TOKEN  = "niIrlNav-3NkyiB82YDtPznbKLfhs0pptRIg4HKb";
const NOCODB_BASE   = "p2txdvaha72xsn4";
const NOCODB_TABLE  = "mzerh9imrwgjmuf"; // Booking Handpan School

export default async function handler(request) {
  // Cal.com sends a GET ping to verify the endpoint — reply OK
  if (request.method !== "POST") {
    return new Response("OK", { status: 200 });
  }

  let payload;
  try {
    payload = await request.json();
  } catch {
    return new Response("Bad JSON", { status: 400 });
  }

  // Cal.com wraps booking data inside payload.payload
  const booking  = payload.payload ?? payload;
  const attendee = booking.attendees?.[0] ?? {};
  const responses = booking.responses ?? {};

  // Extract promo code if present (Cal.com passes it in booking metadata or notes)
  const promoCode = booking.metadata?.promo ?? responses.notes?.value?.match(/promo[:\s]+(\S+)/i)?.[1] ?? "";
  const amount    = promoCode ? 25 : 30; // €25 first class with promo, €30 regular

  const row = {
    "Name":           responses.name?.value  ?? attendee.name  ?? "",
    "Email":          responses.email?.value ?? attendee.email ?? "",
    "Phone":          responses.attendeePhoneNumber?.value ?? attendee.phoneNumber ?? "",
    "Date":           booking.startTime ? booking.startTime.split("T")[0] : "",
    "Amount":         amount,
    "Final Amount":   amount,
    "Promo Code":     promoCode,
    "Payment":        "Stripe",
    "Booking Status": "Confirmed",
    "Notes":          responses.notes?.value ?? "",
  };

  const res = await fetch(
    `${NOCODB_URL}/api/v1/db/data/noco/${NOCODB_BASE}/${NOCODB_TABLE}`,
    {
      method:  "POST",
      headers: {
        "xc-token":     NOCODB_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(row),
    }
  );

  const body = await res.json().catch(() => ({}));
  return new Response(JSON.stringify({ ok: res.ok, nocodb: body }), {
    status: res.ok ? 200 : 500,
    headers: { "Content-Type": "application/json" },
  });
}
