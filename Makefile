njt/cif.csv: njt/scrape_cif.py
	uv run njt/scrape_cif.py

index.html print.html: build.py figures.yaml templates/index.html.j2 templates/print.html.j2
	uv run --with PyYAML --with Jinja2 build.py

.PHONY: clean
clean:
	rm -f index.html print.html
