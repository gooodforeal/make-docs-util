# Люмен

Техническая документация учебного проекта **«Люмен»** — протокола адаптивного управления mesh-сетью уличного освещения.

Сам контроллер, прошивка и сервер **не реализуются**. В репозитории только исходники документации и сборка трёх артефактов.

## Что получается

| Команда | Результат |
| --- | --- |
| `make pdf` | `build/lumen.pdf` |
| `make docx` | `build/lumen.docx` |
| `make html` | статический сайт в `build/html/` (вход — `index.html`) |
| `make` | все три цели |
| `make clean` | удаляет `build/` и сгенерированные `images/*.png` |

Оглавление, формулы, рисунки, таблицы и список литературы попадают во все три формата.

## Зависимости

Нужны **Python 3.9+** (для `make html` и `make docx`) и утилиты сборки.

На macOS:

```bash
brew install python pandoc tectonic librsvg
python3 -m pip install -r requirements.txt
```

- **Python 3** — скрипты `scripts/build_html.py` и `scripts/build_toc.py`
- **pandoc** — Markdown → PDF / DOCX / HTML
- **tectonic** — TeX-движок для PDF (сам подтягивает пакеты при первой сборке)
- **librsvg** — SVG → PNG для вставки рисунков

`requirements.txt` фиксирует, что сторонние pip-пакеты не требуются: хватает стандартной библиотеки.

Для PDF нужны системные шрифты **Times New Roman**, **Arial** и **Menlo** (есть в macOS).

## Состав репозитория

```
docs/          главы в Markdown
images/        схемы в SVG (PNG собирается автоматически)
refs.bib       список литературы
metadata.yaml  титул, язык, шрифты
styles/        CSS сайта, CSL
scripts/       сборка HTML и оглавления DOCX
requirements.txt
Makefile
```

Откройте `docs/01-introduction.md`, чтобы начать читать исходник, либо соберите сайт и откройте `build/html/index.html`.
