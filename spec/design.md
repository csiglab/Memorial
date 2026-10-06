# Design Spec — Memorial Dominicanensis

> Sistema del proyecto: **tipografía ET Book con la escala de Tufte** (tomada de `projects/dominibilis`). Solo cambia la **tipografía**: **no** se alteran colores, layout ni composición.

## Tipografía

- **Familia de texto**: **ET Book** (serif), servida localmente desde `css/et-book/**` (roman, italic, bold, old-style) mediante `@font-face` con rutas relativas `et-book/…`. Declarada en `src/css/tipografia.css`.
- **Monoespaciada**: `Consolas, "Liberation Mono", Menlo, Courier, monospace` (etiquetas y código).
- **Sans de apoyo** (`.sans`): `"Gill Sans", "Gill Sans MT", Calibri, sans-serif`.
- **Escala (Tufte)**: `h1` 400; `h2`/`h3` en **cursiva** y peso 400; párrafos con interlineado amplio. Los tamaños concretos se ajustan por componente, conservando la composición.

## Assets

Vendorizados en `src/`:
- `src/css/tipografia.css` — `@font-face` de ET Book + tokens `--sans`/`--mono` + escala de títulos. **Sin color ni layout.**
- `src/css/et-book/**` — las fuentes.
- `src/img/logo.webp` — logotipo del proyecto (se usa en las cabeceras).
- `src/favicon.ico`.

Rutas relativas: páginas en `src/` → `css/…`, `img/logo.webp`, `favicon.ico`; páginas en `src/projects/<x>/` → `../../css/…`, `../../img/logo.webp`, `../../favicon.ico`. El subproyecto `projects/dominibilis/` conserva sus propios `css/` e `img/`.

**No** se usa `tufte.min.css`: su hoja arrastra colores y layout, fuera del alcance de este cambio.

## Colores y layout

- **Sin cambios**: cada página conserva su paleta (Memorial: `--canvas`, `--navy`, `--lime`, `--steel`; treemap y visor: sus paletas propias) y su composición.
- Las páginas de app (`notas.html`, `organigrama.html`) mantienen su UI funcional; solo cambia la familia/tipografía.

## Páginas

- `src/index.html` — portada del memorial (cabecera con logo).
- `src/about.html` — Acerca del proyecto (contenido del index de dominibilis, con la paleta y el chrome del proyecto).
- `src/projects/arreglo-institucional/{index,notas,organigrama}.html` — con ET Book y la escala de títulos; colores y layout intactos.

## Reglas de uso

- Texto en ET Book; etiquetas/valores en la monoespaciada.
- `h2`/`h3` en cursiva y peso 400 (estilo Tufte).
- El logo `img/logo.webp` encabeza las páginas.
- No introducir colores ni rejillas nuevas: la tipografía se aplica sobre el diseño existente.
