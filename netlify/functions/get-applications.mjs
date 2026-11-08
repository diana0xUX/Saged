const NETLIFY_TOKEN   = process.env.NETLIFY_API_TOKEN;
const NETLIFY_SITE_ID = process.env.NETLIFY_SITE_ID;

export default async (request) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };

  if (request.method === "OPTIONS") return new Response("", { status: 200, headers });

  // 1. Find the event-application form
  const formsRes = await fetch(
    `https://api.netlify.com/api/v1/sites/${NETLIFY_SITE_ID}/forms`,
    { headers: { "Authorization": `Bearer ${NETLIFY_TOKEN}` } }
  );
  const forms = await formsRes.json();
  const form  = Array.isArray(forms) ? forms.find(f => f.name === "event-application") : null;

  if (!form) {
    return new Response(JSON.stringify({ submissions: [], total: 0 }), { status: 200, headers });
  }

  // 2. Fetch submissions
  const subRes = await fetch(
    `https://api.netlify.com/api/v1/forms/${form.id}/submissions?per_page=100`,
    { headers: { "Authorization": `Bearer ${NETLIFY_TOKEN}` } }
  );
  const raw = await subRes.json();
  const submissions = (Array.isArray(raw) ? raw : []).map(s => ({
    id:        s.id,
    created:   s.created_at,
    name:      s.data?.name     ?? "—",
    instagram: s.data?.instagram ?? "",
    whatsapp:  s.data?.whatsapp  ?? "",
    event:     s.data?.["event-name"] ?? "—",
    price:     s.data?.price    ?? "",
    duration:  s.data?.duration ?? "",
    languages: s.data?.languages ?? [],
    days:      s.data?.days      ?? [],
    times:     s.data?.times     ?? [],
    bio:       s.data?.bio       ?? "",
    description: s.data?.description ?? "",
    included:  s.data?.included  ?? "",
    maxPeople: s.data?.["max-people"] ?? "",
    minPeople: s.data?.["min-people"] ?? "",
    videoLink: s.data?.["video-link"] ?? "",
    experience: s.data?.experience ?? "",
    notes:     s.data?.notes     ?? "",
    howFound:  s.data?.["how-found"] ?? "",
  }));

  return new Response(JSON.stringify({ submissions, total: submissions.length }), { status: 200, headers });
};

export const config = { path: "/api/get-applications" };
