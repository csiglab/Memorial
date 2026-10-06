# Spec — Visor de notas del arreglo institucional

> Cómo se leen las notas de `src/projects/arreglo-institucional/docs/` sin mkdocs: un visor cliente (`notas.html`) sobre un manifest pregenerado (`notas.json`). El chrome visual lo fija `spec/design.md`; aquí solo el contrato funcional.

## Fuente y manifest

- Fuente: `docs/**/*.md` (≈617 notas). Se conserva tal cual; es la única verdad.
- `bin/manifest.py` (solo stdlib) recorre `docs/` y escribe `notas.json`:
  `{"generated", "root":"docs", "count", "notes":[{p, t, tags, meta, x, b, to}], "missing", "backlinks"}`.
  - `p`: ruta relativa a `docs/`, tal cual en disco (espacios, acentos, IDs).
  - `t`: primer `# `; si no hay, el nombre del archivo.
  - `tags`: línea `Tags:`; `meta`: `ID/Extra/L/Status` si existen.
  - `x`: extracto de ~240 caracteres para búsqueda y tarjetas.
  - `b`: tamaño del archivo en bytes (métrica del treemap, `spec/treemap.md`).
  - `to`: links resueltos `[{u, to|ext|asset}]`; `missing`: destinos `.md` ausentes; `backlinks`: quién cita a quién.
- Regenerar tras cada cambio en `docs/`: `python3 bin/manifest.py` desde la raíz del repo.

## Rutas

- Deep-link por hash: `notas.html#/<ruta-url-encoded-relativa-a-docs>`.
- El visor hace `fetch()` de `docs/<ruta>` relativo. Exige HTTP (localhost o Pages); por `file://` no funciona.

## Normalización de links

- Destino: `decodeURIComponent`, quitar `#fragmento`, resolver relativo a la nota origen, matchear contra el manifest.
- `.md` existente → ruta hash del visor. `.md` ausente → texto con estilo `.nota-ausente` (sin navegar).
- `http(s)`, imágenes y `.csv` → se dejan intactos (`target="_blank"` para externos).
- Los paréntesis dentro del destino (`(NWO)`) se parsean con balanceo, no con `[^)]`.

## Subset markdown del parser

Encabezados `#..######`, párrafos, `**bold**`, `*italic*`, `` `code` ``, bloques cercados, `> citas`, listas `-/*/1./‣` anidadas, `---`, tablas GFM, `[texto](url)`, `![alt](src)`. Sin math, sin admonitions (el corpus no los usa: verificado 0 casos).

## Presentación de nota

Banda meta superior (mono): `Tags`, `ID`, `Status` si existen. Título H1. Prosa con bloque `.prosa` (headings, tablas, citas, código). Al pie: *citado por* (backlinks del manifest). Nota vacía → estado explícito, no página en blanco.

## Navegación y búsqueda

Árbol lateral desde las rutas del manifest (líneas raíz → consejos → notas), breadcrumb por segmentos, buscador sobre título+ruta+extracto+tags en cliente.

## Estilo

El visor es una página de app: enlaza `src/css/tipografia.css` (ET Book + escala de títulos; `spec/design.md`) y conserva sus colores y layout. Solo cambia la tipografía.
