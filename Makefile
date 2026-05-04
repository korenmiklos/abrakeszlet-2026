.PHONY: all
all: index.html print.html

njt/cif.csv: njt/scrape_cif.py
	uv run njt/scrape_cif.py

njt/expired.csv: njt/scrape_expired.py
	uv run njt/scrape_expired.py

njt/monthly.csv: njt/cumulate.py njt/cif.csv njt/expired.csv
	uv run njt/cumulate.py

index.html print.html: build.py figures.yaml templates/index.html.j2 templates/print.html.j2
	uv run --with PyYAML --with Jinja2 build.py

.PHONY: clean
clean:
	rm -f index.html print.html
