// Cloudflare Pages Function: inject per-post OG metadata for /review/<id>.
// This makes Telegram/WhatsApp/Facebook previews show the post's own photo
// without needing JavaScript — the crawler only has to read the HTML.
const SITE = "https://whisperofwords-review.pages.dev";

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function setMeta(html, prop, content) {
  const re = new RegExp(`<meta property="${prop}" content="[^"]*"`);
  const tag = `<meta property="${prop}" content="${esc(content)}"`;
  if (re.test(html)) return html.replace(re, tag);
  return html.replace("</head>", `${tag} />\n</head>`);
}

export async function onRequestGet({ params, request, env }) {
  const id = params.id;
  if (!/^\d+$/.test(id || "")) return new Response("Not Found", { status: 404 });

  const metaRes = await env.ASSETS.fetch(new URL("/data/meta.json", request.url));
  if (!metaRes.ok) return new Response("Not Found", { status: 404 });
  const posts = await metaRes.json();
  const post = posts.find((p) => String(p.id) === String(id));
  if (!post) return new Response("Not Found", { status: 404 });

  const htmlRes = await env.ASSETS.fetch(new URL("/index.html", request.url));
  if (!htmlRes.ok) return new Response("Not Found", { status: 404 });
  let html = await htmlRes.text();

  const image = post.image || `${SITE}/assets/og-cover.png`;
  const desc = (post.excerpt || post.title).replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim().slice(0, 200);

  html = html.replace(/<title>[^<]*<\/title>/, `<title>${esc(post.title)} — Whisper Of Words</title>`);
  html = setMeta(html, "og:title", post.title);
  html = setMeta(html, "og:description", desc);
  html = setMeta(html, "og:url", `${SITE}/review/${post.id}`);
  html = setMeta(html, "og:image", image);
  html = setMeta(html, "og:site_name", "Whisper Of Words");

  return new Response(html, { headers: { "content-type": "text/html; charset=utf-8" } });
}
