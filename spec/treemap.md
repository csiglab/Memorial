# Spec — Treemap del arreglo

> `organigrama.html` — explorador jerárquico **progresivo** del corpus. Sin dependencias: HTML+CSS+JS propios, un solo archivo, que hace `fetch('notas.json')`. Mismos tokens que `notas.html` (`spec/design.md`).

## Principio

Una vista = **un solo nivel**. `#map` dibuja únicamente los hijos de `current`; el click en una rama **desciende** al siguiente nivel (`Consejos → nivel 2 → nivel 3 → … → nota`). Nada se anida en pantalla.

## Datos

- Fuente: `notas.json` (manifest de `bin/manifest.py`). Campos: `p`, `t`, `tags`, `b` (bytes), `x`.
- Árbol: `docs` → carpetas → notas. La raíz no se dibuja.

## Métrica

- `Notas` (por defecto): área ∝ nº de notas. `Bytes`: área ∝ `b`. Botón `Métrica` alterna.
- El valor de una rama es la suma de sus hojas; se muestra como `N notas` / `N KB`.

## Layout

- **Squarified treemap** de un nivel (Bruls et al.).
- Color: heredado de la **línea raíz** (13, paleta curada); ramas = mezcla con blanco con **tono alternado por hermano** (par/impar); hojas = tono casi pleno. Texto según luminancia.

## Interacciones

| Acción | Resultado |
| --- | --- |
| Click en rama | **Desciende** un nivel (anima desde el rectángulo clicado) |
| Click en nota | Abre `notas.html#/<ruta>` (misma pestaña) |
| Migas de pan | Sube a cualquier ancestro |
| `↑ Subir` / `Backspace` | Sube un nivel |
| `Restablecer` / `Esc` | Vuelve a la raíz y limpia la búsqueda |
| Buscar | Resalta coincidencias (título/ruta/tags, sin acentos); `Enter` desciende al ancestro común |
| Leyenda | Click en una línea raíz → desciende a ella |
| Hover | Tooltip: nombre, ruta, conteo/bytes, tags |
| Resize | Recomputa |

## Animación (FLIP)

- Al descender: los hijos crecen desde el rectángulo de la rama clicada.
- Al subir/restablecer/cambiar métrica: la nueva vista se expande desde el área completa.
- Reuso de elementos por `path`; transición CSS en `left/top/width/height`.

## Estado en la URL

- `#/<ruta-relativa-a-docs>` fija el nivel actual (enlace compartible y pruebas). Se mantiene con `history.replaceState`.

## Estados

- Sin `notas.json` (p. ej. `file://`): estado de error con la instrucción de servir por HTTP.
- Rama sin hijos con valor (p. ej. todas vacías en modo bytes): vista vacía.

## Verificación

- Node: recorrer todas las ramas hasta el nivel de notas, cobertura de área = área, migas, búsqueda, métrica y subida de nivel.
- Headless Chromium: capturas en la raíz y en un nivel profundo vía hash.

## Estilo

Página de app: enlaza `src/css/tipografia.css` (ET Book + escala de títulos; `spec/design.md`). Conserva su paleta propia (color por línea raíz) y su layout; solo cambia la tipografía.
