#!/usr/bin/env python3
"""Extract the V8 teaching panels from strokes/index.html into per-stroke fragments.

Run this BEFORE slimming strokes/index.html. It writes:
  learn/teach/<stroke>.html   (课堂教学 fragment for that stroke's book)
  learn/teach/cues.json       (module titles + 连贯口令 for the slim 四泳姿 page)

The fragments keep the original record ids and wording. Review-only markup
(揭晓/标记 buttons) is dropped. Source refs are rewritten to the slim
/strokes/ page, which keeps 原文与来源.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "strokes" / "index.html"
OUT = ROOT / "learn" / "teach"

STROKES = {
    "crawl": "爬泳",
    "back": "仰泳",
    "fly": "蝶泳",
    "breast": "蛙泳",
}
VIEWS = [
    ("courseView", "口诀与练习"),
    ("errorView", "分类纠错"),
    ("techView", "技术要点"),
]


def demote_headings(node) -> None:
    for tag, new in (("h4", "h5"), ("h3", "h4"), ("h2", "h3")):
        for el in node.find_all(tag):
            el.name = new


def clean(panel, stroke: str) -> str:
    for sel in (".recall-actions", ".module-toc", ".back-toc", ".next-module"):
        for el in panel.select(sel):
            el.decompose()
    for el in panel.find_all(attrs={"hidden": True}):
        del el.attrs["hidden"]
    for a in panel.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#S"):
            a["href"] = f"../../strokes/{href}"
        elif href.startswith("#stroke-"):
            a["href"] = "../../strokes/"
    demote_headings(panel)
    return str(panel)


def main() -> None:
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    if soup.find(id="courseView") is None:
        raise SystemExit("strokes/index.html no longer has the teaching panels; "
                         "fragments in learn/teach/ are the source now.")
    OUT.mkdir(parents=True, exist_ok=True)
    cues: dict[str, list[dict[str, str]]] = {}
    for stroke, label in STROKES.items():
        parts = [f'<div class="v8-teach" data-stroke="{stroke}">']
        for view_id, view_label in VIEWS:
            view = soup.find(id=view_id)
            panel = view.find("section", attrs={"data-stroke": stroke})
            if panel is None:
                raise SystemExit(f"missing {view_id} panel for {stroke}")
            parts.append(f'<section class="teach-view" id="teach-{view_id[:-4].lower()}-{stroke}">')
            parts.append(f"<h3>{view_label}</h3>")
            parts.append(clean(panel, stroke))
            parts.append("</section>")
        parts.append("</div>")
        out = OUT / f"{stroke}.html"
        out.write_text("\n".join(parts) + "\n", encoding="utf-8")
        print(f"{stroke}: {out.stat().st_size} bytes -> {out.relative_to(ROOT)}")

        modules = []
        course = soup.find(id="courseView").find("section", attrs={"data-stroke": stroke})
        for unit in course.find_all("section", class_="unit"):
            title_el = unit.find(["h2", "h3"])
            title = title_el.get_text(" ", strip=True) if title_el else unit.get("id", "")
            cue = ""
            for rec in unit.find_all("article", class_="record"):
                text = rec.get_text(" ", strip=True)
                if "连贯口令" in text:
                    dl = rec.find("dl")
                    if dl:
                        cue = " ".join(dl.get_text(" ", strip=True).replace("连贯口令", "", 1).split())
                    break
            if not cue:
                last = unit.find("article", id=re.compile(r"-L$"))
                if last and last.find("dl"):
                    cue = "；".join(
                        " ".join(dd.get_text(" ", strip=True).split())
                        for dd in last.find("dl").find_all("dd")
                    )
            modules.append({"id": unit.get("id", ""), "title": title, "cue": cue})
        cues[stroke] = modules
    (OUT / "cues.json").write_text(
        json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")
    print("cues:", {k: len(v) for k, v in cues.items()})


if __name__ == "__main__":
    main()
