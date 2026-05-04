#!/usr/bin/env python3
"""Render index.html (reveal.js deck) and print.html (scrollable) from figures.yaml."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "figures.yaml"
TEMPLATES_DIR = ROOT / "templates"
OUTPUTS = ("index.html", "print.html")


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _dw_src_and_id(item: dict) -> tuple[str, str]:
    src = item.get("src")
    chart_id = item.get("id")
    if src:
        if not src.endswith("/"):
            src = src + "/"
        m = re.search(r"datawrapper\.dwcdn\.net/([^/]+)/", src)
        if m and not chart_id:
            chart_id = m.group(1)
    elif chart_id:
        src = f"https://datawrapper.dwcdn.net/{chart_id}/"
    else:
        raise ValueError(f"datawrapper figure needs `id` or `src`: {item!r}")
    return src, chart_id or "chart"


def normalize(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    counter = 0
    for raw in items or []:
        kind = raw.get("type")
        if kind == "section":
            out.append({"type": "section", "title": raw.get("title", "")})
            continue

        counter += 1
        entry: dict = {
            "type": kind,
            "number": counter,
            "label": f"{counter}. ábra",
            "anchor": f"abra-{counter}",
        }

        entry["caption"] = raw.get("caption", "")

        if kind == "datawrapper":
            src, chart_id = _dw_src_and_id(raw)
            entry["src"] = src
            entry["chart_id"] = chart_id
            entry["height"] = int(raw.get("height", 500))
        elif kind == "image":
            src = raw.get("src")
            if not src:
                raise ValueError(f"image figure needs `src`: {raw!r}")
            entry["src"] = src
            entry["alt"] = raw.get("alt", "")
        else:
            raise ValueError(f"unknown figure type: {kind!r} in {raw!r}")

        out.append(entry)
    return out


def render() -> None:
    cfg = load_config()
    figures = normalize(cfg.get("figures", []))
    has_datawrapper = any(f.get("type") == "datawrapper" for f in figures)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    ctx = {
        "title": cfg.get("title", ""),
        "subtitle": cfg.get("subtitle", ""),
        "author": cfg.get("author", ""),
        "date": cfg.get("date", ""),
        "figures": figures,
        "has_datawrapper": has_datawrapper,
    }
    for name in OUTPUTS:
        tpl = env.get_template(f"{name}.j2")
        (ROOT / name).write_text(tpl.render(**ctx), encoding="utf-8")
        print(f"wrote {name}")

    n_figs = sum(1 for f in figures if f["type"] != "section")
    print(f"{n_figs} ábra rendered.")


if __name__ == "__main__":
    try:
        render()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
