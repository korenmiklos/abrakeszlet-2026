import csv
import sys
import time
import urllib.request
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path


OUTPUT = Path(__file__).parent / "cif.csv"
START_DATE = date(2010, 6, 1)


class LinkTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_a = False
        self.entries: list[str] = []
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_a = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == "a" and self.in_a:
            self.in_a = False
            text = self.current_text.strip()
            if text:
                self.entries.append(text)

    def handle_data(self, data):
        if self.in_a:
            self.current_text += data


def fetch_counts(d: date) -> tuple[int, int]:
    url = f"https://njt.hu/p/search_cif/{d:%Y%m%d}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    parser = LinkTextParser()
    parser.feed(html)

    torveny = sum(1 for e in parser.entries if "törvény" in e.lower())
    rendelet = sum(1 for e in parser.entries if "rendelet" in e.lower())
    return torveny, rendelet


def load_existing() -> set[str]:
    if not OUTPUT.exists():
        return set()
    with open(OUTPUT, newline="") as f:
        reader = csv.DictReader(f)
        return {row["date"] for row in reader}


def main():
    end_date = date.today()
    done = load_existing()

    # If resuming, append; otherwise write fresh
    write_header = not OUTPUT.exists() or len(done) == 0
    mode = "w" if write_header else "a"

    with open(OUTPUT, mode, newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["date", "torveny", "rendelet"])
            # Rewrite existing rows if starting fresh
            done = set()

        d = START_DATE
        total = (end_date - START_DATE).days + 1
        i = 0
        while d <= end_date:
            i += 1
            ds = d.isoformat()
            if ds in done:
                d += timedelta(days=1)
                continue

            try:
                torveny, rendelet = fetch_counts(d)
                writer.writerow([ds, torveny, rendelet])
                f.flush()
                print(f"[{i}/{total}] {ds}: törvény={torveny}, rendelet={rendelet}")
            except Exception as e:
                print(f"[{i}/{total}] {ds}: ERROR {e}", file=sys.stderr)

            d += timedelta(days=1)
            time.sleep(0.2)

    print(f"Done. Output: {OUTPUT}")


if __name__ == "__main__":
    main()
