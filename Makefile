CHAPTERS = \
	docs/01-introduction.md \
	docs/02-requirements.md \
	docs/03-architecture.md \
	docs/04-protocol.md \
	docs/05-algorithms.md \
	docs/06-evaluation.md \
	docs/07-conclusion.md

SVGS := $(wildcard images/*.svg)
PNGS := $(SVGS:.svg=.png)

PANDOC ?= pandoc
PDF_ENGINE ?= tectonic

COMMON = \
	--metadata-file=metadata.yaml \
	--citeproc \
	--bibliography=refs.bib \
	--csl=styles/ieee.csl \
	--resource-path=. \
	--from=markdown+tex_math_dollars \
	--metadata=link-citations=true

.PHONY: all pdf docx html figures clean

all: pdf docx html

figures: $(PNGS)

images/%.png: images/%.svg
	rsvg-convert -f png -w 1600 "$<" -o "$@"

pdf: figures
	mkdir -p build
	$(PANDOC) $(COMMON) $(CHAPTERS) \
		--toc \
		--number-sections \
		--pdf-engine=$(PDF_ENGINE) \
		-o build/lumen.pdf

docx: figures
	mkdir -p build
	python3 scripts/build_toc.py
	$(PANDOC) $(COMMON) build/toc.md $(CHAPTERS) \
		--number-sections \
		-o build/lumen.docx
	rm -f build/toc.md

html: figures
	python3 scripts/build_html.py

clean:
	rm -rf build
	rm -f images/*.png
