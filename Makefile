PYTHON ?= python3
PORT   ?= 8004
SITE   := src

.PHONY: help build manifest serve dev clean

help:
	@echo "build      regenerate generated data (alias of manifest)"
	@echo "manifest   regenerate src/projects/arreglo-institucional/notas.json from docs/"
	@echo "serve      serve the site (src/) at http://localhost:$(PORT)"
	@echo "dev        alias of serve"
	@echo "clean      remove __pycache__ and OS cruft"

build: manifest

manifest:
	$(PYTHON) bin/manifest.py

serve:
	$(PYTHON) -m http.server $(PORT) --directory $(SITE)

dev: serve

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true
