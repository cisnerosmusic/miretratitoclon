#!/usr/bin/env python3
# Static site generator for the Mi Retratito clone.
# Mirrors the original Google Sites visual structure (white, Lato, teal #7DB6B1,
# banner headers with overlaid title) but as fast, clean, SEO-ready static HTML.
#
# Run it from the _source/ folder:  python3 build.py
# It writes the site to the repo root and refreshes the "Evolución" section of
# the README, so progress fills in by itself as images are added to img/.
import json, html, re
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
# In the repo, build.py lives in _source/ and outputs to the repo root.
OUT = ROOT.parent if ROOT.name == "_source" else (ROOT / "site")
IMG = OUT / "img"
OUT.mkdir(exist_ok=True); IMG.mkdir(exist_ok=True)
C = json.load(open(ROOT / "content.json", encoding="utf-8"))
S = C["site"]
NAV = C["nav"]
DOMAIN = "https://" + S["domain"]

manifest = []  # (filename, description)

def esc(t): return html.escape(t or "", quote=True)

def nav_html(active):
    links = []
    for n in NAV:
        href = "/" if n["slug"] == "index" else "/" + n["slug"]
        act = ' class="active" aria-current="page"' if n["slug"] == active else ""
        links.append(f'<a href="{href}"{act}>{esc(n["label"])}</a>')
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
        rows.append(f'<article class="track"><h2>{esc(it["title"])}</h2>{meta}{player}</article>')
    return f'<div class="tracks">{"".join(rows)}</div>'

def doc(slug, title, desc, body, active=None):
    active = active or slug
    canonical = DOMAIN + ("/" if slug == "index" else "/" + slug)
    og_img = DOMAIN + "/img/og.jpg"
    manifest.append(("img/og.jpg", "Social share image (1200x630). Optional but recommended."))
    jsonld = ""
    if slug == "index":
        jsonld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Person",
            "name": "Mi Retratito", "alternateName": S["handle"],
            "description": S["bio"], "url": DOMAIN, "email": "mailto:" + S["email"],
            "jobTitle": "Digital Artist, Poet, Musician, Photographer"
        }, ensure_ascii=False) + '</script>'
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
<p class="foot-mail"><a href="mailto:{esc(S["email"])}">{esc(S["email"])}</a>{' · <a href="'+esc(S["linktree"])+'" target="_blank" rel="noopener">Links</a>' if S.get("linktree") else ''}</p>
<p class="foot-copy">&copy; Mi Retratito</p>
</div></footer>
<script src="/app.js" defer></script>
</body>
</html>
"""

# ---------- build pages ----------
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
(OUT/"index.html").write_text(doc("index", "Mi Retratito", S["bio"][:155], home_body), encoding="utf-8")

for slug in ["photography", "digital-art", "poetry"]:
    d = C[slug]
    body = banner(slug, d["heading"], d.get("intro","")) + f'<section class="wrap section">{gallery(slug, d["items"])}</section>'
    (OUT/f"{slug}.html").write_text(doc(slug, f'{d["heading"]} — Mi Retratito', d.get("intro", d["heading"]), body), encoding="utf-8")

def gen_embeds(items):
    cards = []
    for it in items:
        desc = f'<p class="gen-desc">{esc(it["desc"])}</p>' if it.get("desc") else ""
        link = f'<a class="gen-link" href="{esc(it["link"])}" target="_blank" rel="noopener">View the NFT ↗</a>' if it.get("link") else ""
        ratio = esc(it.get("ratio", "16 / 9"))
        if it.get("media"):
            # Click-to-play facade: poster first, iframe loads only on demand (lighter + cleaner).
            poster = (f'<img class="gen-poster" src="{esc(it["poster"])}" alt="{esc(it["title"])}" loading="lazy">'
                      if it.get("poster") else "")
            frame = (f'<div class="gen-stage" style="aspect-ratio:{ratio}" '
                     f'data-src="{esc(it["media"])}" data-title="{esc(it["title"])}">'
                     f'{poster}<button class="gen-play" type="button" aria-label="Play {esc(it["title"])}">'
                     f'<span>▶</span> Play</button></div>')
        else:
            frame = (f'<div class="gen-stage pending" style="aspect-ratio:{ratio}"><span>{esc(it["title"])}</span></div>')
        cards.append(f'<article class="gen">{frame}<div class="gen-meta"><h2>{esc(it["title"])}</h2>{desc}{link}</div></article>')
    return f'<div class="gens">{"".join(cards)}</div>'

ga = C["generative-art"]
has_live = any(it.get("media") for it in ga["items"])
note = ("" if has_live else
    '<div class="notice"><p>Generative pieces are minted as NFTs on '
    '<a href="https://objkt.com" target="_blank" rel="noopener">objkt</a> / '
    '<a href="https://www.transient.xyz" target="_blank" rel="noopener">transient</a>. '
    'Live embeds will be added here.</p></div>')
ga_inner = gen_embeds(ga["items"]) if ga["items"] else gallery("generative-art", [{"title": f"Piece {i:02d}"} for i in range(1,5)])
ga_body = banner("generative-art", ga["heading"], ga.get("intro","")) + f'<section class="wrap section">{note}{ga_inner}</section>'
(OUT/"generative-art.html").write_text(doc("generative-art", f'{ga["heading"]} — Mi Retratito', ga.get("intro",""), ga_body), encoding="utf-8")

m = C["music"]
m_body = banner("music", m["heading"], m.get("intro","")) + f'<section class="wrap section">{drive_players(m["items"])}</section>'
(OUT/"music.html").write_text(doc("music", f'{m["heading"]} — Mi Retratito', m.get("intro",""), m_body), encoding="utf-8")

cb = C["collabs"]
cb_body = banner("collabs", cb["heading"], cb.get("intro","")) + f'<section class="wrap section">{drive_players(cb["items"])}</section>'
(OUT/"collabs.html").write_text(doc("collabs", f'{cb["heading"]} — Mi Retratito', cb.get("intro",""), cb_body), encoding="utf-8")

contact_body = (
    banner("contact", "Contact", "Let's talk.") +
    '<section class="wrap section contact">'
    '<p class="contact-lead">For prints, collaborations, commissions and bookings.</p>'
    f'<p class="contact-mail"><a href="mailto:{esc(S["email"])}">{esc(S["email"])}</a></p>'
    + (f'<p class="contact-links"><a href="{esc(S["linktree"])}" target="_blank" rel="noopener">All links ↗</a></p>' if S.get("linktree") else "")
    + f'<p class="contact-handle">{esc(S["handle"])}</p>'
    f'<p class="contact-tags">{esc(S["hashtags"])}</p></section>'
)
(OUT/"contact.html").write_text(doc("contact", "Contact — Mi Retratito", "Contact Mi Retratito for prints, collaborations and commissions.", contact_body), encoding="utf-8")

# ---------- meta files ----------
pages_for_map = [("/" if n["slug"]=="index" else "/"+n["slug"]) for n in NAV]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages_for_map:
    sm.append(f"  <url><loc>{DOMAIN}{p}</loc><changefreq>monthly</changefreq></url>")
sm.append("</urlset>")
(OUT/"sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
(OUT/"robots.txt").write_text("User-agent: *\nAllow: /\n\n" f"Sitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
(OUT/"humans.txt").write_text(
    "/* ARTIST */\nName: Mi Retratito\nRole: Digital artist, poet, musician, photographer\n"
    f"Contact: {S['email']}\nHandle: {S['handle']}\n\n/* SITE */\n"
    "Static HTML, no framework. Hosted on Cloudflare Pages.\nFonts: Lato.\n", encoding="utf-8")
(OUT/"llms.txt").write_text(
    "# Mi Retratito\n\n" f"> {S['bio']}\n\n"
    "Mi Retratito is the portfolio of a multidisciplinary digital artist working across "
    "photography, digital and generative art, music, and poetry.\n\n## Pages\n"
    f"- [Home]({DOMAIN}/): overview and biography\n"
    f"- [Photography]({DOMAIN}/photography): analog and digital photography\n"
    f"- [Digital Art]({DOMAIN}/digital-art): composed digital images\n"
    f"- [Generative Art]({DOMAIN}/generative-art): code-based works, minted as NFTs on objkt\n"
    f"- [Music]({DOMAIN}/music): original tracks\n"
    f"- [Poetry]({DOMAIN}/poetry): poems\n"
    f"- [Collabs]({DOMAIN}/collabs): collaborative works\n"
    f"- [Contact]({DOMAIN}/contact): {S['email']}\n\n## Notes\n"
    "- The artist welcomes use of her published music and art for reference and study.\n", encoding="utf-8")
(OUT/"_redirects").write_text("https://www.miretratito.art/* https://miretratito.art/:splat 301\n", encoding="utf-8")
(OUT/"_headers").write_text(
    "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n"
    "/img/*\n  Cache-Control: public, max-age=31536000, immutable\n"
    "/styles.css\n  Cache-Control: public, max-age=86400\n"
    "/app.js\n  Cache-Control: public, max-age=86400\n", encoding="utf-8")
(OUT/"favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    '<rect width="64" height="64" rx="10" fill="#212121"/>'
    '<text x="32" y="44" font-family="Georgia,serif" font-size="38" fill="#7DB6B1" text-anchor="middle">M</text></svg>', encoding="utf-8")

# image manifest
seen=set(); lines=["# Imágenes que faltan","",
                   "Suelta cada archivo en la carpeta `img/` con el nombre EXACTO que ves aquí.",
                   "El sitio funciona sin ellas (muestra un marco con el título) y se va llenando a medida que las agregas.",""]
for fn, dsc in manifest:
    if fn in seen: continue
    seen.add(fn)
    lines.append(f"- `{fn}` — {dsc}")
(OUT/"IMAGES_NEEDED.md").write_text("\n".join(lines), encoding="utf-8")

# ---------- progress block for README ----------
def have(fn): return (OUT/fn).exists() and (OUT/fn).stat().st_size > 1000
def bar(done, total):
    if total == 0: return "──────────", "n/a"
    filled = round(done/total*10)
    return "█"*filled + "░"*(10-filled), f"{round(done/total*100)}%"

# count real images per gallery
def count_imgs(slug, n):
    return sum(1 for i in range(1, n+1) if have(f"img/{slug}-{i:02d}.jpg"))

rows = []
# (label, done, total, extra note)
ph = count_imgs("photography", len(C["photography"]["items"]))
da = count_imgs("digital-art", len(C["digital-art"]["items"]))
po = count_imgs("poetry", len(C["poetry"]["items"]))
gen_live = [it["title"] for it in C["generative-art"]["items"] if it.get("media")]
gen_total = max(len(C["generative-art"]["items"]), 1)
music_audio = sum(1 for it in C["music"]["items"] if it.get("drive"))
collab_audio = sum(1 for it in C["collabs"]["items"] if it.get("drive"))
portrait = 1 if have("img/portrait.jpg") else 0

sections = [
    ("Inicio (retrato)", portrait, 1, ""),
    ("Photography", ph, len(C["photography"]["items"]), "imágenes"),
    ("Digital Art", da, len(C["digital-art"]["items"]), "imágenes"),
    ("Generative Art", len(gen_live), gen_total, "embebidas en vivo: " + (", ".join(gen_live) if gen_live else "ninguna aún")),
    ("Poetry", po, len(C["poetry"]["items"]), "imágenes"),
    ("Music", music_audio, len(C["music"]["items"]), "audio embebido ✓"),
    ("Collabs", collab_audio, len(C["collabs"]["items"]), "audio embebido"),
]
total_done = sum(s[1] for s in sections)
total_all = sum(s[2] for s in sections)
overall_bar, overall_pct = bar(total_done, total_all)

prog = []
prog.append("<!-- progreso:inicio (generado por _source/build.py, no editar a mano) -->")
prog.append("## 🌱 Evolución del sitio")
prog.append("")
prog.append("Hola 👋 Esta sección se actualiza sola cada vez que se reconstruye el sitio.")
prog.append("Vas a ver cómo tu web se va llenando poco a poco.")
prog.append("")
prog.append(f"**Avance general** `{overall_bar}` {overall_pct}  ({total_done}/{total_all} piezas)")
prog.append("")
prog.append("| Sección | Avance | | Notas |")
prog.append("|---|---|---|---|")
for label, done, tot, note in sections:
    b, pct = bar(done, tot)
    prog.append(f"| {label} | `{b}` | {done}/{tot} | {note} |")
prog.append("")
prog.append("**Listo ya:** textos y pies de foto de todas las páginas · música y collabs sonando · "
            "SEO completo (sin `noindex`) · diseño fiel al original · responsive.")
prog.append("")
prog.append("**Falta:** soltar las imágenes limpias en `img/` (ver `IMAGES_NEEDED.md`). "
            "Las obras generativas se van embebiendo en vivo a medida que llegan sus enlaces de objkt/transient.")
prog.append("<!-- progreso:fin -->")
progress_block = "\n".join(prog)

readme_path = OUT/"README.md"
if readme_path.exists():
    txt = readme_path.read_text(encoding="utf-8")
    if "<!-- progreso:inicio" in txt and "<!-- progreso:fin -->" in txt:
        txt = re.sub(r"<!-- progreso:inicio.*?<!-- progreso:fin -->", progress_block, txt, flags=re.S)
    else:
        # insert after first heading block
        txt = txt.rstrip() + "\n\n" + progress_block + "\n"
    readme_path.write_text(txt, encoding="utf-8")

print("Built:", sorted(p.name for p in OUT.glob('*.html')))
print(f"Progress: {total_done}/{total_all} images ({overall_pct})")
print("Images needed:", len(seen))
