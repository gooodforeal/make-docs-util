#!/usr/bin/env python3
"""Статическое оглавление для DOCX: поле TOC в Word иначе пустое до обновления."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    "docs/01-introduction.md",
    "docs/02-requirements.md",
    "docs/03-architecture.md",
    "docs/04-protocol.md",
    "docs/05-algorithms.md",
    "docs/06-evaluation.md",
    "docs/07-conclusion.md",
]


def slug(title: str) -> str:
    text = title.strip().lower()
    text = re.sub(r"[«»\"“”]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-]+", "", text, flags=re.UNICODE)
    return text


def main() -> None:
    lines = ["# Оглавление {-}", ""]
    for rel in CHAPTERS:
        for raw in (ROOT / rel).read_text(encoding="utf-8").splitlines():
            if raw.startswith("# "):
                title = raw[2:].strip()
                lines.append(f"- [{title}](#{slug(title)})")
            elif raw.startswith("## "):
                title = raw[3:].strip()
                lines.append(f"    - [{title}](#{slug(title)})")
    out = ROOT / "build" / "toc.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"TOC written to {out}")


if __name__ == "__main__":
    main()
