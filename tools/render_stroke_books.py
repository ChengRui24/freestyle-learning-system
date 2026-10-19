#!/usr/bin/env python3
"""Render the four-stroke diagnosis booklets from learn/{back,breast,fly}/source.md."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from render_learn import heading_id, inline, render_blocks  # noqa: E402
from seo import head_for  # noqa: E402

LEARN = ROOT / "learn"

BOOKS = {
    "back": {
        "brand": "仰泳学习体系",
        "ver": "阶段 / 诊断 / 专项 · 对齐四泳姿",
        "sub": "用来定阶段、看现象、选一个专项，再按课堂教学的口令上课。",
        "stroke": "back",
        "stroke_label": "仰泳",
    },
    "breast": {
        "brand": "蛙泳学习体系",
        "ver": "阶段 / 诊断 / 专项 · 对齐四泳姿",
        "sub": "用来定阶段、看现象、选一个专项，再按课堂教学的口令上课。",
        "stroke": "breast",
        "stroke_label": "蛙泳",
    },
    "fly": {
        "brand": "蝶泳学习体系",
        "ver": "阶段 / 诊断 / 专项 · 对齐四泳姿",
        "sub": "用来定阶段、看现象、选一个专项，再按课堂教学的口令上课。",
        "stroke": "fly",
        "stroke_label": "蝶泳",
    },
    "course": {
        "brand": "课程安排",
        "ver": "四式通用",
        "sub": "学习流程、通过条件，以及一节课的热身、专项、主项和放松。",
    },
}

TEACH = {"back": "back", "breast": "breast", "fly": "fly"}

SIBLINGS = [
    ("freestyle/", "自由泳"),
    ("back/", "仰泳"),
    ("fly/", "蝶泳"),
    ("breast/", "蛙泳"),
]


def parse_book(md: str) -> tuple[str, str, list[tuple[str, str, str]]]:
    lines = md.split("\n")
    title = "学习体系"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    preamble: list[str] = []
    sections: list[tuple[str, str, str]] = []
    cur_id = ""
    cur_title = ""
    cur_body: list[str] = []
    seen: dict[str, int] = {}

    def flush() -> None:
        nonlocal cur_id, cur_title, cur_body
        if cur_id:
            sections.append((cur_id, cur_title, "\n".join(cur_body).rstrip()))
        cur_id, cur_title, cur_body = "", "", []

    for line in lines:
        if line.startswith("## "):
            flush()
            cur_title = line[3:].strip()
            base = heading_id(cur_title)
            n = seen.get(base, 0) + 1
            seen[base] = n
            cur_id = base if n == 1 else f"{base}-{n}"
            cur_body = []
            continue
        if not cur_id:
            preamble.append(line)
        else:
            cur_body.append(line)
    flush()
    return title, "\n".join(preamble).strip("\n"), sections


def page(key: str, title: str, preamble: str, sections: list[tuple[str, str, str]]) -> str:
    meta = BOOKS[key]

    def cur(name: str) -> str:
        return ' aria-current="page"' if name == key else ""
    nav = []
    if key in TEACH:
        nav.append('<a href="#teach">课堂教学</a>')
    for sid, stitle, _ in sections:
        nav.append(f'<a href="#{html.escape(sid)}">{html.escape(stitle)}</a>')
    siblings = []
    for href, label in SIBLINGS:
        if href.startswith(key):
            siblings.append(label)
        else:
            siblings.append(f'<a href="../{href}">{label}</a>')
    sib = " · ".join(siblings)
    if key == "course":
        cross = (
            '<p class="site-cross">各式的阶段和专项见 '
            '<a href="../freestyle/">自由泳</a>、'
            '<a href="../back/">仰泳</a>、'
            '<a href="../fly/">蝶泳</a>、'
            '<a href="../breast/">蛙泳</a>。'
            '上课口令在各册的课堂教学里。四泳姿页只留通用路径和连贯口令。'
            '入水共同课见 <a href="../#alts">USMS 汇总</a>。</p>'
        )
    else:
        cross = (
            '<p class="site-cross">四式阶段诊断：'
            f"{sib}。"
            '课堂教学（口令、纠错、要点）在本册下文。'
            '入水共同课见 <a href="../#alts">USMS 汇总</a>。'
            '一节课怎么排见 <a href="../course/">课程安排</a>。'
            '个人自救见 <a href="../../safety/">水中自救</a>。</p>'
        )
    body = []
    body.append(
        '<header class="page-head">\n'
        f"      <h1>{inline(title)}</h1>\n"
        f'      <p class="sub">{html.escape(meta["sub"])}</p>\n'
        f"      {cross}\n"
        f"      {render_blocks(preamble, 'lede')}\n"
        "    </header>"
    )
    if key in TEACH:
        frag = (LEARN / "teach" / f"{TEACH[key]}.html").read_text(encoding="utf-8")
        body.append(
            '<section id="teach">\n'
            "      <h2>课堂教学：口令、纠错与要点</h2>\n"
            "      <p>从陆上到水中按口诀与练习走；看见的现象到分类纠错里核对；"
            "动作原理看技术要点。一节课只取其中一个模块。</p>\n"
            f"      {frag}\n"
            "    </section>"
        )
    as_list = key in {"back", "breast", "fly"}
    for sid, stitle, text in sections:
        body.append(
            f'<section id="{html.escape(sid)}">\n'
            f"      <h2>{inline(stitle)}</h2>\n"
            f"      {render_blocks(text, sid, drill_lists=as_list)}\n"
            "    </section>"
        )
    main = "\n\n    ".join(body)
    nav_html = "\n      ".join(nav)
    seo = head_for(key)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{seo}
  <link rel="stylesheet" href="../css/app.css">
  <link rel="stylesheet" href="../css/teach.css">
  <link rel="stylesheet" href="../../css/site.css">
</head>
<body class="page-learn">
<header class="site-bar">
  <a class="site-brand" href="../../">成人游泳训练</a>
  <nav aria-label="站点">
    <a href="../" aria-current="page">学习</a>
    <a href="../../safety/">自救</a>
    <a href="../../gear/">器材</a>
  </nav>
</header>
<nav class="section-nav" aria-label="学习">
  <a href="../course/"{cur("course")}>课程安排</a>
  <a href="../../strokes/">四泳姿</a>
  <a href="../">汇总</a>
  <a href="../freestyle/"{cur("freestyle")}>自由泳</a>
  <a href="../back/"{cur("back")}>仰泳</a>
  <a href="../fly/"{cur("fly")}>蝶泳</a>
  <a href="../breast/"{cur("breast")}>蛙泳</a>
</nav>
<div class="app">
  <aside class="side">
    <p class="brand">{html.escape(meta["brand"])}</p>
    <div class="ver">{html.escape(meta["ver"])}</div>
    <nav>
      {nav_html}
    </nav>
  </aside>
  <main class="main">
    {main}
  </main>
</div>
<script src="../js/nav.js?4"></script>
</body>
</html>
"""


def main() -> None:
    for key in BOOKS:
        src = LEARN / key / "source.md"
        md = src.read_text(encoding="utf-8")
        title, preamble, sections = parse_book(md)
        if not sections:
            raise SystemExit(f"{src} has no sections")
        out = LEARN / key / "index.html"
        out.write_text(page(key, title, preamble, sections), encoding="utf-8")
        print(f"{key}: {len(sections)} sections -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
