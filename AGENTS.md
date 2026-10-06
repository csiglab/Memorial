# AGENTS.md

## Purpose

Instructions for AI agents working in this repository. Follow the conventions below; when a project
directory carries its own `AGENTS.md` (e.g. `src/projects/relacion-analitica/`), it takes precedence
for work inside that project. The global git guideline (`~/configs/global/git/guideline.md`) is
binding for commits and naming.

## Project Context

### Description

Memoria Dominicanensis is the *memorial de los medios para el adelantamiento de Santo Domingo*: a
**native, static site** (no build step, no framework) that gathers the project's research and
instruments. It holds the **Memorial** landing (`src/index.html`), the **Arreglo Institucional**
project (a ~620-note corpus with a client-side note viewer and a progressive treemap), and the
**Relación Analítica de la República Dominicana** (indicators, in-browser "live" blocks and thematic
fichas). Content is in Spanish; agent instructions are in English.

### Objectives

- Keep one coherent visual system: **ET Book typography** with the **Memorial palette**, shared via
  `src/css/tipografia.css` and the page-level CSS tokens.
- Keep data single-sourced: the corpus lives in Markdown under `docs/`, and every generated artifact
  (`notas.json`) is produced from it.
- Keep the analytical relation and fichas current, honest and sourced (reference figures labelled
  with source and period; live blocks fetch public APIs and fall back gracefully).
- Stay **static and dependency-free**: vanilla HTML/CSS/JS, SVG charts authored in-house, no CDN,
  no site generator.

### Scope

- In: `src/` (site), `bin/` (tooling), `spec/` (specs), the projects under `src/projects/`, and
  `proto/` (reference). See the structure table below.
- Out: the upstream `csiglab/*` repositories and any backend or database; the import of external
  site generators (mkdocs and friends) that were intentionally removed.

## Repository Structure

| Path | Role |
|------|------|
| `bin/manifest.py` | Stdlib generator: walks `docs/` and writes the viewer manifest. |
| `spec/` | Specs: `design.md` (typography/palette), `notas.md` (viewer contract), `treemap.md`. |
| `src/` | **Site root** — serve this directory. |
| `src/index.html`, `src/about.html` | Memorial landing and About. |
| `src/css/tipografia.css`, `src/css/et-book/` | Shared typography (ET Book + scale). |
| `src/img/logo.webp`, `src/favicon.ico` | Project logo and icon. |
| `src/projects/arreglo-institucional/` | Corpus (`docs/`), `notas.json`, `notas.html` viewer, `organigrama.html` treemap. |
| `src/projects/relacion-analitica/` | Analytical relation (`index.html`, `about.html`) and `fichas-y-reportes/`. |
| `proto/` | Prototypes/reference material — not part of the served site. |
| `Makefile` | `build`, `manifest`, `serve`, `dev`, `clean`. |

## Agent Operating Principles

### Understand Before Changing

Read `spec/design.md` before touching styles, and the relevant spec (`spec/notas.md`,
`spec/treemap.md`) before touching the viewer or treemap. Data flow is
`docs/**/*.md → bin/manifest.py → src/projects/arreglo-institucional/notas.json → notas.html / organigrama.html`.
`notas.json` is **generated** — never edit it by hand; regenerate and commit the result.

### Prefer Existing Solutions

- Reuse `src/css/tipografia.css` and the page CSS tokens; never hardcode a new palette or font.
- Charts are **vanilla SVG** written inline; reuse the existing helpers (`sparkline`, `squarify`)
  instead of adding a charting library.
- Reuse the manifest shape (`{p, t, tags, meta, x, b, to}`) for anything that reads the corpus.
- Serve from `src/`; relative asset paths (`css/…`, `img/…`, `../../css/…`) already assume that root.

### Minimize Change

The pages are single-file apps with no build step. Make surgical edits. Preserve colors, layout and
component structure unless the task explicitly asks to change them (the move to ET Book typography
was a deliberate, typography-only change — do not re-introduce layout/colour shifts under that flag).

### Preserve Invariants

- **Generated files are generated.** `notas.json` comes from `bin/manifest.py`; regenerate, never
  hand-edit. Corpus markdown under `docs/` is the single source of truth.
- **The site must be served over HTTP.** Pages use `fetch()` for `notas.json` and public APIs;
  `file://` will fail. Use `make serve`.
- **Evidence over assertion.** Figures in `relacion-analitica` are *reference* values: label them
  with source and period, and keep the `[object Object]`-free, dependency-free rendering intact.
- **No dependencies, no generators.** Keep styles scoped (no new palette), and keep assets vendored
  under `src/`. Do not commit secrets.
- `.gitignore` covers editor/OS/env cruft; keep it.

### Keep Work Scoped

One concern per change set. Commit messages follow `tipo(scope): resumen` with the allowed types
(`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`) from the global guideline.

## Development Environment

### Requirements

- Python 3 (standard library only — the tooling has no third-party dependencies)
- A browser. Optional: Node for ad-hoc inline-script syntax checks.

### Setup

```sh
make serve            # serve src/ at http://localhost:8000/
# open http://localhost:8000/
```

### Common commands

```sh
make manifest         # regenerate notas.json (commit the result)
make serve            # PORT=8080 make serve overrides the port
make clean            # remove __pycache__ / .DS_Store
```

### Verification

There is no test suite. Smoke-test by serving the site and opening the touched pages over HTTP:
the Memorial (`/`), the About (`/about.html`), the arreglo viewer
(`/projects/arreglo-institucional/notas.html`) and treemap (`…/organigrama.html`), and the relation
(`/projects/relacion-analitica/index.html`). Confirm the viewer loads `notas.json`, the treemap
drills down, and the live block degrades to its fallback when the network is unavailable.

## Git Workflow

Global git configuration lives in `~/configs/global/git` (hooks via `core.hooksPath`) and
`~/configs/bin` (helpers). Four hooks are active.

### Check-in policy (`pre-commit.d/00-authorization-policy.sh`)

A staged file is only accepted if it carries the extended attribute `user.checkin=1`; otherwise the
commit is rejected with "Required check mark is missing".

```sh
mark-for-commit <file>…        # mark files (helpers live in ~/configs/bin)
mark-for-commit --list         # list marked files
git diff --cached --name-only -z --diff-filter=ACM | xargs -0 mark-for-commit   # bulk-mark staged
```

The mark is a filesystem xattr: it survives staging, is not versioned, and must be re-applied to
each new file.

### Annotation policy (`pre-commit.d/01-annotation-policy.sh`)

Staged source files (patterns in `annotations.conf`) must not contain BLOCK annotations —
`@WORKING`, `@FIXME`, `@QUESTION`, `@VERIFY` — or the commit is rejected. `@TODO`, `@HACK` and
`@WORKAROUND` only warn; `@TECH-DEBT`, `@NOTE`, etc. are informational.

### Encoding policy (`pre-commit.d/02-encoding-policy.sh`)

Staged text files must be UTF-8 without a BOM and use LF line endings only. Fix with
`dos2unix <file>`, `iconv`, or `sed -i '1s/^\xEF\xBB\xBF//' <file>`.

### Commit message hook (`prepare-commit-msg`)

Git only pre-fills the `type(<ref>): message` template when the editor opens with **no** message
source. Passing `-m "…"` preserves your message as-is; amending with `-m` behaves the same. The
`post-commit` hook clears the check-in marks from the committed files.

### Signing & branches

Commits may be signed and branches are environment-provided. Do **not** inspect git configuration
internals — never read, print, or search `.git/config` or any identity/signing values (`user.*`,
`commit.*`, `gpg.*`). Treat author identity, signing and hooks as opaque. Do not push unless
explicitly asked.

## When to Ask

- Moving or renaming the site structure (`src/`, project folders, asset paths).
- Changing the shared typography/palette tokens or the overall layout.
- Changing the data pipeline or the shape/output of generated files (`bin/manifest.py`, `notas.json`).
- Adding any dependency, CDN, or build/generator step.
- Any deployment action.
