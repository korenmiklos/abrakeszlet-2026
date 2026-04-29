# abrakeszlet-2026

Ábrakészlet (chart book) magas szintű döntéshozóknak. Két nézet, egy forrás:

- **`index.html`** — reveal.js diabemutató (lapozható prezentációs mód).
- **`print.html`** — folyamatos, görgethető oldal nyomtatáshoz / PDF / DOCX exporthoz.

Mindkettőt a `figures.yaml` vezérli; a GitHub Action minden `main`-re push után újrarenderel
és kitelepít a GitHub Pages-re.

## Szerkesztés

Csak a [`figures.yaml`](figures.yaml)-t kell szerkeszteni. Példa:

```yaml
title: "Ábrakészlet 2026"
subtitle: "Magas szintű döntéshozóknak"

figures:
  - type: section
    title: "Makrogazdaság"

  - type: datawrapper
    id: "AbCdE"           # a Datawrapper chart ID (Embed panel)
    height: 500           # opcionális; a JS úgyis átméretezi

  - type: image
    src: "figures/gdp.png"
    alt: "GDP-növekedés 2010–2025"
```

A számozás (`1. ábra`, `2. ábra`, …) automatikusan generálódik a sorrend alapján.
A `section` típus fejezetcímet ad, számot nem kap. A Datawrapper ábrákban a chartba beleszerkesztett cím marad meg — a YAML-ben ne adj nekik címet.

## Datawrapper

A Datawrapper "Publish & Embed" panelén az **Embed code (responsive iframe)** alatt
találod a chart ID-t (pl. `AbCdE` a `https://datawrapper.dwcdn.net/AbCdE/1/` URL-ben).
Elég csak az `id`-t megadni, a build összerakja az iframe-et és beilleszti a hivatalos
auto-resize scriptet ([dokumentáció](https://www.datawrapper.de/_/docs/embedding/responsive)).

Teljes URL is megadható `src`-ként, ha pl. egy konkrét verziót akarsz fixálni:

```yaml
- type: datawrapper
  src: "https://datawrapper.dwcdn.net/AbCdE/3/"
```

## PNG ábrák

Tedd a fájlokat a [`figures/`](figures/) mappába és hivatkozz rájuk relatívan
(`figures/foo.png`). A GitHub Action ezeket átmásolja a kitelepített site-ba.

## Helyi build

```bash
pip install -r requirements.txt
python build.py
open index.html  # vagy: open print.html
```

## Export PDF-be

A `print.html` jobb felső sarkában a **Nyomtatás / PDF** gombbal a böngésző
"Save as PDF" funkciójával készül a PDF (Chrome/Safari/Edge mind támogatja).
A CSS A4 oldalméretre és oldaltörésekre van hangolva.

## Export DOCX-be

[Pandoc](https://pandoc.org/) segítségével:

```bash
python build.py
pandoc print.html -o abrakeszlet.docx --extract-media=.
```

A Datawrapper iframe-ek nem konvertálódnak DOCX-be — ehhez a charteket előbb
PNG-ként kell exportálni a Datawrapper-ből (Publish → Export → PNG), és a YAML-ben
`type: image`-ként hivatkozni rájuk.

## Telepítés (GitHub Pages)

A repó beállításai között: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Ezután minden `main`-re push automatikusan újrarendeli és kitelepíti a két oldalt.
