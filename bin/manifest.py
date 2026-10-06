#!/usr/bin/env python3
"""Genera notas.json (manifest del visor) desde docs/.

Solo stdlib. Uso:
    python3 manifest.py
Se ejecuta desde src/projects/arreglo-institucional/.
"""
import json
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # raíz del repo
BASE = REPO / "src" / "projects" / "arreglo-institucional"
DOCS = BASE / "docs"
OUT = BASE / "notas.json"

META_KEYS = ("Tags", "ID", "Extra", "L", "Status")


def balanced_links(text):
    """Extrae (texto, destino) de links markdown, con paréntesis balanceados."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "[" and (i == 0 or text[i - 1] != "!"):
            j = text.find("]", i)
            if j < 0:
                break
            k = j + 1
            while k < n and text[k] in " \t":
                k += 1
            if k < n and text[k] == "(":
                depth = 1
                m = k + 1
                while m < n and depth:
                    if text[m] == "(":
                        depth += 1
                    elif text[m] == ")":
                        depth -= 1
                    m += 1
                if depth:
                    # sin cierre balanceado (nombres Notion truncados): último ')' de la línea
                    eol = text.find("\n", k)
                    if eol < 0:
                        eol = n
                    close = text.rfind(")", k, eol)
                    if close > k:
                        m = close + 1
                    else:
                        out.append((text[i + 1 : j], text[k + 1 :].strip()))
                        i = j + 1
                        continue
                out.append((text[i + 1 : j], text[k + 1 : m - 1].strip()))
                i = m
                continue
        i += 1
    return out


def clean_inline(s):
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace("**", "").replace("__", "")
    s = s.replace("`", "")
    return s.strip()


def parse_note(path):
    rel = path.relative_to(DOCS).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    title = None
    tags = []
    meta = {}
    body_start = 0
    for idx, line in enumerate(lines[:15]):
        s = line.strip()
        if s.startswith("# ") and title is None:
            title = s[2:].strip()
            body_start = idx + 1
        m = re.match(r"^([A-Za-z]+):\s*(.+)$", s)
        if m and m.group(1) in META_KEYS and not s.startswith("#"):
            if m.group(1) == "Tags":
                tags = [t.strip(" ,") for t in re.split(r"[,;]", m.group(2)) if t.strip(" ,")]
            else:
                meta[m.group(1)] = m.group(2).strip()
    if title is None:
        title = path.stem
    body = "\n".join(lines[body_start:])
    parts = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("```"):
            continue
        s = re.sub(r"^(#{1,6}\s+|>\s?|‣\s*|[-*+]\s+|\d+[.)]\s+|\|\s?)", "", s).strip()
        s = clean_inline(s.strip("| ").replace("|", " "))
        if s:
            parts.append(s)
        if sum(len(p) for p in parts) > 240:
            break
    excerpt = " ".join(parts)[:240]
    links = []
    for _label, url in balanced_links(text):
        if not url or url.startswith("#"):
            continue
        links.append(url)
    return {
        "p": rel,
        "t": title,
        "tags": tags,
        "meta": meta,
        "x": excerpt,
        "b": len(text.encode("utf-8")),
        "links": links,
    }


def main():
    mds = sorted(DOCS.rglob("*.md"))
    notes = [parse_note(p) for p in mds]
    by_path = {n["p"]: n for n in notes}
    missing = {}
    backlinks = {}
    resolved = {}
    for n in notes:
        src = Path(n["p"])
        res = []
        for url in n["links"]:
            if re.match(r"^https?://", url):
                res.append({"u": url, "ext": True})
                continue
            if re.search(r"\.(png|jpe?g|ico|svg|webp|gif|csv)(\?.*)?$", url, re.I):
                res.append({"u": url, "asset": True})
                continue
            dec = urllib.parse.unquote(url.split("#")[0])
            if not dec.lower().endswith(".md"):
                res.append({"u": url, "ext": True})
                continue
            # resolución contra DOCS (los links son relativos a la nota origen)
            cand = (DOCS / src.parent / dec)
            try:
                cand = cand.resolve().relative_to(DOCS.resolve()).as_posix()
            except Exception:
                cand = None
            if cand and cand in by_path:
                res.append({"u": url, "to": cand})
                backlinks.setdefault(cand, []).append(n["p"])
            else:
                res.append({"u": url, "to": None})
                missing.setdefault(n["p"], []).append(url)
        resolved[n["p"]] = res
    for n in notes:
        n["to"] = resolved[n["p"]]
        del n["links"]
    manifest = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": "docs",
        "count": len(notes),
        "notes": notes,
        "missing": missing,
        "backlinks": {k: sorted(set(v)) for k, v in backlinks.items()},
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    n_missing = sum(len(v) for v in missing.values())
    n_empty = sum(1 for n in notes if not n["x"])
    print(f"notas: {len(notes)} | vacías: {n_empty} | links a notas ausentes: {n_missing}")
    print(f"escrito: {OUT}")


if __name__ == "__main__":
    main()
