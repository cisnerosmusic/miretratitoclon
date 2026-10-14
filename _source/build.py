#!/usr/bin/env python3
# Static site generator for the Mi Retratito clone.
# Mirrors the original Google Sites visual structure (white, Lato, teal #7DB6B1,
# banner headers with overlaid title) but as fast, clean, SEO-ready static HTML.
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
SITE = ROOT / "site"
IMG = SITE / "img"
SITE.mkdir(exist_ok=True); IMG.mkdir(exist_ok=True)
C = json.load(open(ROOT / "content.json", encoding="utf-8"))
S = C["site"]
NAV = C["nav"]
DOMAIN = "https://" + S["domain"]

manifest = []  # list of (filename, description) images the owner must drop in

def esc(t): return html.escape(t or "", quote=True)

def nav_html(active):
    links = []
    for n in NAV:
        href = "/" if n["slug"] == "index" else "/" + n["slug"]
        cls = " aria-current=\"page\"" if n["slug"] == active else ""
        act = " class=\"active\"" if n["slug"] == active else ""
        links.append(f'<a href="{href}"{act}{cls}>{esc(n["label"])}</a>')
    return (
        '<header class="site-head"><div class="wrap head-inner">'
        f'<a class="brand" href="/">Mi Retratito</a>'
        '<button class="nav-toggle" aria-label="Menu" aria-expanded="false">'
        '<span></span><span></span><span></span></button>'
        f'<nav class="site-nav" aria-label="Main">{"".join(links)}</nav>'
        '</div></header>'
    )

def banner(slug, title, subtitle="", home=False):
    fn = f"banner-{slug}.jpg"
    manifest.append((f"img/{fn}", f"Banner image for the {title} page (wide, ~2000px). Optional."))
    sub = f'<p class="banner-sub">{esc(subtitle)}</p>' if subtitle else ""
    cls = "banner home" if home else "banner"
    return (
        f'<section class="{cls}">'
        f'<img class="banner-bg" src="/img/{fn}" alt="" loading="eager" '
        f'onerror="this.style.display=\'none\';this.parentElement.classList.add(\'no-img\')">'
        f'<div class="banner-inner wrap"><h1>{esc(title)}</h1>{sub}</div>'
        f'<a class="scroll-down" href="#content" aria-label="Scroll down">↓</a>'
        f'</section>'
    )

def gallery(slug, items, start=1):
    cells = []
    for i, it in enumerate(items, start):
        fn = f"{slug}-{i:02d}.jpg"
        manifest.append((f"img/{fn}", f'{esc(it["title"])} — image for "{slug}".'))
        cap_parts = []
        if it.get("caption"): cap_parts.append(f'<span class="cap-line">{esc(it["caption"])}</span>')
        if it.get("place"): cap_parts.append(f'<span class="cap-place">{esc(it["place"])}</span>')
        cap = f'<figcaption><span class="cap-title">{esc(it["title"])}</span>{"".join(cap_parts)}</figcaption>'
        cells.append(
            f'<figure class="work pending">'
            f'<div class="frame">'
            f'<img src="/img/{fn}" alt="{esc(it["title"])}" loading="lazy" '
            f'onload="this.closest(\'figure\').classList.remove(\'pending\')" '
            f'onerror="this.remove()">'
            f'<span class="frame-title">{esc(it["title"])}</span>'
            f'</div>{cap}</figure>'
        )
    return f'<div class="gallery">{"".join(cells)}</div>'

def drive_players(items):
    rows = []
    for it in items:
        did = it.get("drive")
        meta = f'<p class="track-with">{esc(it["with"])}</p>' if it.get("with") else ""
        if did:
            player = (
                f'<div class="player"><iframe loading="lazy" '
                f'src="https://drive.google.com/file/d/{did}/preview" '
                f'allow="autoplay" title="{esc(it["title"])}"></iframe></div>'
            )
        else:
            player = '<p class="track-pending">Audio pending</p>'
        rows.append(
            f'<article class="track"><h2>{esc(it["title"])}</h2>{meta}{player}</article>'
        )
    return f'<div class="tracks">{"".join(rows)}</div>'

def page(slug, title, desc, body, active=None):
    active = active or slug
    canonical = DOMAIN + ("/" if slug == "index" else "/" + slug)
    og_img = DOMAIN + "/img/og.jpg"
    manifest.append(("img/og.jpg", "Social share image (1200x630). Optional but recommended."))
    jsonld = ""
    if slug == "index":
        jsonld = (
            '<script type="application/ld+json">' + json.dumps({
                "@context": "https://schema.org",
                "@type": "Person",
                "name": "Mi Retratito",
                "alternateName": S["handle"],
                "description": S["bio"],
                "url": DOMAIN,
                "email": "mailto:" + S["email"],
                "jobTitle": "Digital Artist, Poet, Musician, Photographer"
            }, ensure_ascii=False) + '</script>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mi Retratito">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#212121">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/styles.css">
{jsonld}
</head>
<body>
{nav_html(active)}
<main id="content">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<p class="foot-handle">{esc(S["handle"])}</p>
<p class="foot-tags">{esc(S["hashtags"])}</p>
<p class="foot-mail"><a href="mailto:{esc(S["email"])}">{esc(S["email"])}</a></p>
<p class="foot-copy">&copy; Mi Retratito</p>
</div></footer>
<script src="/app.js" defer></script>
</body>
</html>
"""

pages_meta = {}

# HOME
home_body = (
    banner("home", "Mi Retratito", S["tagline"], home=True) +
    '<section class="bio wrap"><div class="bio-portrait"><figure class="work pending">'
    '<div class="frame"><img src="/img/portrait.jpg" alt="Mi Retratito" loading="lazy" '
    'onload="this.closest(\'figure\').classList.remove(\'pending\')" onerror="this.remove()">'
    '<span class="frame-title">Portrait</span></div></figure></div>'
    f'<div class="bio-text"><p class="lead">{esc(S["bio"])}</p>'
    f'<p class="bio-handle">{esc(S["handle"])}</p></div></section>'
)
manifest.append(("img/portrait.jpg", "Artist portrait for the home page."))
Path(SITE/"index.html").write_text(page("index", "Mi Retratito", S["bio"][:155], home_body), encoding="utf-8")
pages_meta["index"] = "Mi Retratito"

# Gallery pages
for slug in ["photography", "digital-art", "poetry"]:
    d = C[slug]
    body = banner(slug, d["heading"], d.get("intro","")) + f'<section class="wrap section">{gallery(slug, d["items"])}</section>'
    title = f'{d["heading"]} — Mi Retratito'
    Path(SITE/f"{slug}.html").write_text(page(slug, title, d.get("intro", d["heading"]), body), encoding="utf-8")

# Digital art intro mentions NFTs on objkt? keep generic. Generative art page:
ga = C["generative-art"]
ga_body = (
    banner("generative-art", ga["heading"], ga.get("intro","")) +
    '<section class="wrap section"><div class="notice">'
    '<p>Generative pieces are minted as NFTs on <a href="https://objkt.com" target="_blank" rel="noopener">objkt</a>. '
    'Clean embeds will be added here.</p></div>'
    + gallery("generative-art", [{"title": f"Piece {i:02d}"} for i in range(1,5)]) +
    '</section>'
)
Path(SITE/"generative-art.html").write_text(
    page("generative-art", f'{ga["heading"]} — Mi Retratito', ga.get("intro",""), ga_body), encoding="utf-8")

# Music
m = C["music"]
m_body = banner("music", m["heading"], m.get("intro","")) + f'<section class="wrap section">{drive_players(m["items"])}</section>'
Path(SITE/"music.html").write_text(
    page("music", f'{m["heading"]} — Mi Retratito', m.get("intro",""), m_body), encoding="utf-8")

# Collabs
cb = C["collabs"]
cb_body = banner("collabs", cb["heading"], cb.get("intro","")) + f'<section class="wrap section">{drive_players(cb["items"])}</section>'
Path(SITE/"collabs.html").write_text(
    page("collabs", f'{cb["heading"]} — Mi Retratito', cb.get("intro",""), cb_body), encoding="utf-8")

# Contact
contact_body = (
    banner("contact", "Contact", "Let's talk.") +
    '<section class="wrap section contact">'
    f'<p class="contact-lead">For prints, collaborations, commissions and bookings.</p>'
    f'<p class="contact-mail"><a href="mailto:{esc(S["email"])}">{esc(S["email"])}</a></p>'
    f'<p class="contact-handle">{esc(S["handle"])}</p>'
    f'<p class="contact-tags">{esc(S["hashtags"])}</p>'
    '</section>'
)
Path(SITE/"contact.html").write_text(
    page("contact", "Contact — Mi Retratito", "Contact Mi Retratito for prints, collaborations and commissions.", contact_body), encoding="utf-8")

# ---------- meta files ----------
pages_for_map = [("/" if n["slug"]=="index" else "/"+n["slug"]) for n in NAV]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages_for_map:
    sm.append(f"  <url><loc>{DOMAIN}{p}</loc><changefreq>monthly</changefreq></url>")
sm.append("</urlset>")
Path(SITE/"sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

Path(SITE/"robots.txt").write_text(
    "User-agent: *\nAllow: /\n\n"
    f"Sitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")

Path(SITE/"humans.txt").write_text(
    "/* ARTIST */\n"
    "Name: Mi Retratito\n"
    "Role: Digital artist, poet, musician, photographer\n"
    f"Contact: {S['email']}\n"
    f"Handle: {S['handle']}\n\n"
    "/* SITE */\n"
    "Static HTML, no framework. Hosted on Cloudflare Pages.\n"
    "Fonts: Lato.\n", encoding="utf-8")

Path(SITE/"llms.txt").write_text(
    "# Mi Retratito\n\n"
    f"> {S['bio']}\n\n"
    "Mi Retratito is the portfolio of a multidisciplinary digital artist working across "
    "photography, digital and generative art, music, and poetry.\n\n"
    "## Pages\n"
    f"- [Home]({DOMAIN}/): overview and biography\n"
    f"- [Photography]({DOMAIN}/photography): analog and digital photography\n"
    f"- [Digital Art]({DOMAIN}/digital-art): composed digital images\n"
    f"- [Generative Art]({DOMAIN}/generative-art): code-based works, minted as NFTs on objkt\n"
    f"- [Music]({DOMAIN}/music): original tracks\n"
    f"- [Poetry]({DOMAIN}/poetry): poems\n"
    f"- [Collabs]({DOMAIN}/collabs): collaborative works\n"
    f"- [Contact]({DOMAIN}/contact): {S['email']}\n\n"
    "## Notes\n"
    "- The artist welcomes use of her published music and art for reference and study.\n", encoding="utf-8")

# Cloudflare Pages redirects: force apex (no-www) + clean URLs are automatic
Path(SITE/"_redirects").write_text(
    "https://www.miretratito.art/* https://miretratito.art/:splat 301\n", encoding="utf-8")

# Cloudflare headers: caching + basic security
Path(SITE/"_headers").write_text(
    "/*\n"
    "  X-Content-Type-Options: nosniff\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "  X-Frame-Options: SAMEORIGIN\n"
    "/img/*\n"
    "  Cache-Control: public, max-age=31536000, immutable\n"
    "/styles.css\n"
    "  Cache-Control: public, max-age=86400\n"
    "/app.js\n"
    "  Cache-Control: public, max-age=86400\n", encoding="utf-8")

# favicon (simple teal monogram)
Path(SITE/"favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect width="64" height="64" rx="10" fill="#212121"/>'
    '<text x="32" y="44" font-family="Georgia,serif" font-size="38" '
    'fill="#7DB6B1" text-anchor="middle">M</text></svg>', encoding="utf-8")

# write image manifest (dedup, keep order)
seen=set(); lines=["# Images needed for the site","",
                   "Drop each file into the site/img/ folder with the EXACT name shown.",
                   "The page works without them (shows a framed placeholder); it fills in as you add files.",""]
for fn, dsc in manifest:
    if fn in seen: continue
    seen.add(fn)
    lines.append(f"- `{fn}` — {dsc}")
Path(ROOT/"IMAGES_NEEDED.md").write_text("\n".join(lines), encoding="utf-8")

print("Built pages:", sorted(p.name for p in SITE.glob("*.html")))
print("Meta files:", [p.name for p in SITE.iterdir() if p.is_file() and p.suffix in ('.txt','.xml','.svg') or p.name in ('_redirects','_headers')])
print("Images needed:", len(seen))
