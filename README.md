# Mi Retratito — clon estático

Clon fiel del sitio original (Google Sites, `miretratito.art`), rehecho como
HTML estático para servir **rápido** desde **Cloudflare Pages**, con SEO completo.

<!-- progreso:inicio (generado por _source/build.py, no editar a mano) -->
## 🌱 Evolución del sitio

Hola 👋 Esta sección se actualiza sola cada vez que se reconstruye el sitio.
Vas a ver cómo tu web se va llenando poco a poco.

**Avance general** `███░░░░░░░` 33%  (26/78 piezas)

| Sección | Avance | | Notas |
|---|---|---|---|
| Inicio (retrato) | `░░░░░░░░░░` | 0/1 |  |
| Photography | `░░░░░░░░░░` | 0/12 | imágenes |
| Digital Art | `░░░░░░░░░░` | 0/15 | imágenes |
| Generative Art | `██████████` | 5/5 | embebidas en vivo: Spotlights, Entropy, Aquarius, Lucinda, Urbano 2.0 |
| Poetry | `░░░░░░░░░░` | 0/21 | imágenes |
| Music | `██████████` | 12/12 | audio embebido ✓ |
| Collabs | `████████░░` | 9/12 | audio embebido |

**Listo ya:** textos y pies de foto de todas las páginas · música y collabs sonando · SEO completo (sin `noindex`) · diseño fiel al original · responsive.

**Falta:** soltar las imágenes limpias en `img/` (ver `IMAGES_NEEDED.md`). Las obras generativas se van embebiendo en vivo a medida que llegan sus enlaces de objkt/transient.
<!-- progreso:fin -->

Respeta la estructura visual de la autora: fondo blanco, tipografía **Lato**,
acento **teal `#7DB6B1`**, encabezados tipo banner con el título encima.

## Estructura

```
index.html  photography.html  digital-art.html  generative-art.html
music.html  poetry.html  collabs.html  contact.html
styles.css  app.js  favicon.svg
robots.txt  sitemap.xml  humans.txt  llms.txt
_redirects  _headers        (configuración de Cloudflare Pages)
img/                         (imágenes — ver IMAGES_NEEDED.md)
_source/build.py  _source/content.json   (generador, para regenerar)
```

## Qué ya funciona

- Las **8 páginas** con todos los textos, títulos y pies de foto del original.
- **Música y Collabs**: los reproductores siguen embebidos desde el Google Drive
  de la autora, así que suenan sin descargar nada.
- **SEO**: `<title>`, meta description, canonical, Open Graph, Twitter Card,
  JSON-LD (Person), `sitemap.xml`, `robots.txt`, `humans.txt`, `llms.txt`.
  Sin `noindex` (el problema del sitio original).
- Responsive, menú móvil, lightbox en las galerías, `prefers-reduced-motion`.

## Qué falta (imágenes)

El scrape del Google Sites no permite copiar las imágenes (URLs con token que
devuelven 403, y en baja resolución). Hay que soltar los **masters limpios**
(desde los NFTs en objkt y los archivos propios de la autora).

Mira **`IMAGES_NEEDED.md`**: lista cada archivo con su nombre exacto.
Suéltalos en `img/` con ese nombre y la página los toma sola. Mientras tanto,
cada hueco muestra un marco con el título, así el sitio luce intencional.

El **arte generativo** usaba un widget interno de Google Sites que no se puede
clonar. Hay que pegar los embeds limpios de objkt en `generative-art.html`.

## Regenerar

Si editas textos en `_source/content.json`:

```
cd _source && python3 build.py   # reescribe el sitio en la raíz
```

## Desplegar en Cloudflare Pages

1. Cloudflare → Workers & Pages → Create → Pages → conectar este repo.
2. Framework preset: **None**. Build command: *(vacío)*. Output dir: `/` (raíz).
3. Custom domain: `miretratito.art` (y `www` → redirige a la raíz vía `_redirects`).

Así el dominio raíz (sin www) y el SSL quedan limpios de una vez.
