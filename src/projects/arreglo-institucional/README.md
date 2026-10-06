# Arreglo Institucional

> El arreglo institucional de la República Dominicana como promesa: consejos, agencias y observatorios. Parte de [Memorial Dominicanensis](../../../README.md).

Este proyecto nació como sitio **mkdocs**; hoy es **nativo**: HTML para el chrome y las páginas especiales, Markdown para el corpus, y un visor cliente que los une. Sin generador de sitio.

## Estructura

```
arreglo-institucional/
├── docs/            # el corpus: ≈620 notas en Markdown (fuente única)
├── index.html       # portada del proyecto (prosa Tufte)
├── notas.html       # visor de notas (JS cliente, sin dependencias)
├── organigrama.html # treemap del arreglo (vanilla, sin dependencias)
├── notas.json       # manifest del visor (generado, se commitea)
└── .gitignore
```

La tipografía del proyecto (ET Book + escala de títulos, ver [`spec/design.md`](../../../spec/design.md)) se sirve desde `src/css/tipografia.css` y `src/css/et-book/`; estas páginas la referencian con `../../css/tipografia.css`. El logo `src/img/logo.webp` encabeza todas las páginas. No se cambian colores ni layout.

## Servir

El visor usa `fetch()`, así que requiere HTTP (no `file://`):

```
python3 -m http.server 8000
# http://localhost:8000/
```

## Regenerar el manifest

Tras editar cualquier nota de `docs/`:

```
python3 bin/manifest.py
```

`bin/manifest.py` vive en la raíz del repo (solo stdlib) y escribe `notas.json`.

## Diseño

Tema, tipografía y componentes siguen [`spec/design.md`](../../../spec/design.md). El contrato del visor está en [`spec/notas.md`](../../../spec/notas.md).
