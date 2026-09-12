#!/usr/bin/env python3
"""Сборка многостраничного статического сайта из глав документации."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "html"
ASSETS = OUT / "assets"
IMAGES_OUT = OUT / "images"

CHAPTERS = [
    ("01-introduction.html", "docs/01-introduction.md", "Введение"),
    ("02-requirements.html", "docs/02-requirements.md", "Постановка задачи и требования"),
    ("03-architecture.html", "docs/03-architecture.md", "Архитектура системы"),
    ("04-protocol.html", "docs/04-protocol.md", "Протокол LMP"),
    ("05-algorithms.html", "docs/05-algorithms.md", "Математическая модель и алгоритмы"),
    ("06-evaluation.html", "docs/06-evaluation.md", "Оценка характеристик"),
    ("07-conclusion.html", "docs/07-conclusion.md", "Заключение и литература"),
]


def nav_html(active: str | None) -> str:
    items = ['<a class="brand" href="index.html">Люмен</a>']
    items.append(
        '<div class="tag">Протокол адаптивного управления mesh-сетью уличного освещения</div>'
    )
    items.append("<ol>")
    for href, _, title in CHAPTERS:
        cls = ' class="active"' if href == active else ""
        items.append(f'<li{cls}><a href="{href}">{title}</a></li>')
    items.append("</ol>")
    return "\n".join(items)


def pager(index: int) -> str:
    prev_link = next_link = ""
    if index > 0:
        href, _, title = CHAPTERS[index - 1]
        prev_link = f'<a href="{href}">← {title}</a>'
    if index < len(CHAPTERS) - 1:
        href, _, title = CHAPTERS[index + 1]
        next_link = f'<a href="{href}">{title} →</a>'
    if index < 0:
        href, _, title = CHAPTERS[0]
        next_link = f'<a href="{href}">{title} →</a>'
        prev_link = ""
    return f'<div class="pager"><div>{prev_link}</div><div>{next_link}</div></div>'


def wrap(title: str, nav: str, body: str, extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} — Люмен</title>
  <link rel="stylesheet" href="assets/site.css"/>
  <script>
  window.MathJax = {{
    tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }}
  }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="layout">
    <nav class="side">{nav}</nav>
    <main><div class="paper">{body}{extra}</div></main>
  </div>
</body>
</html>
"""


def run_pandoc(sources: list[Path]) -> str:
    cmd = [
        "pandoc",
        *[str(src) for src in sources],
        "--from=markdown+tex_math_dollars",
        "--to=html5",
        "--math-method=mathjax",
        "--citeproc",
        f"--bibliography={ROOT / 'refs.bib'}",
        f"--csl={ROOT / 'styles' / 'ieee.csl'}",
        f"--resource-path={ROOT}",
        "--metadata",
        "link-citations=true",
    ]
    return subprocess.check_output(cmd, text=True)


def split_chapters(full_html: str) -> list[str]:
    chunks = [part for part in re.split(r"(?=<h1\b)", full_html) if part.strip()]
    if len(chunks) != 8:
        raise RuntimeError(f"expected 8 <h1> sections, got {len(chunks)}")
    bodies = chunks[:6]
    bodies.append(chunks[6] + chunks[7])
    return bodies


def retarget_citations(body: str, href: str) -> str:
    if href.startswith("07-"):
        return body
    return re.sub(r'href="#ref-', 'href="07-conclusion.html#ref-', body)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    ASSETS.mkdir(parents=True)
    IMAGES_OUT.mkdir(parents=True)
    shutil.copy2(ROOT / "styles" / "site.css", ASSETS / "site.css")
    for png in (ROOT / "images").glob("*.png"):
        shutil.copy2(png, IMAGES_OUT / png.name)
    for svg in (ROOT / "images").glob("*.svg"):
        shutil.copy2(svg, IMAGES_OUT / svg.name)

    all_sources = [ROOT / src for _, src, _ in CHAPTERS]
    bodies = split_chapters(run_pandoc(all_sources))

    for i, ((href, _, title), body) in enumerate(zip(CHAPTERS, bodies)):
        html = wrap(title, nav_html(href), retarget_citations(body, href), pager(i))
        (OUT / href).write_text(html, encoding="utf-8")

    index_body = """
    <div class="hero">
      <h1>Люмен</h1>
      <p class="lead">Протокол адаптивного управления mesh-сетью уличного освещения. Техническая документация учебного проекта.</p>
    </div>
    <p>Документ описывает требования, архитектуру узлов, протокол LMP, математическую модель согласования яркости и оценку энергосбережения. Исходники глав лежат в <code>docs/</code>; сайт, PDF и DOCX собираются командами <code>make html</code>, <code>make pdf</code> и <code>make docx</code>.</p>
    <h2>Оглавление</h2>
    <ol class="toc-home">
    """
    for href, _, title in CHAPTERS:
        index_body += f'<li><a href="{href}">{title}</a></li>\n'
    index_body += "</ol>"
    index_body += pager(-1)
    (OUT / "index.html").write_text(
        wrap("Оглавление", nav_html(None), index_body),
        encoding="utf-8",
    )
    print(f"HTML site written to {OUT}")


if __name__ == "__main__":
    main()
