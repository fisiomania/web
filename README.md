# Fisio Manía · web

Sitio de [Fisio Manía](https://fisiomania.com.ar): fisiología humana explicada fácil, con clases en YouTube y simulaciones interactivas. Sitio estático publicado con GitHub Pages (dominio en `CNAME`).

## Estructura

- `index.html`: home.
- `renal.html`, `medio-interno.html`, `regulacion-ph.html`, `sangre.html`, `respiratorio.html`: una página por tema. Cargan sus videos desde el `.json` del mismo nombre.
- `simulaciones.html` y `simulaciones/`: catálogo y simulaciones interactivas.
- `sobre-fisiomania.html`: presentación del proyecto.
- `sitemap.xml` y `robots.txt`: SEO. Al agregar una página nueva, sumarla al sitemap.

## Videos de YouTube

`actualizar_videos.py` descarga las listas de reproducción y guarda los `.json`. El workflow `.github/workflows/actualizar.yml` lo corre todos los días y sube los cambios. Necesita el secreto `YOUTUBE_API_KEY` en Settings → Secrets and variables → Actions.

## Al crear una página nueva

Incluir título, `description`, `canonical`, Open Graph, el código de Google Analytics (`G-X6X1NQJZHP`) y agregarla al `sitemap.xml`.
