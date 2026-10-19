#!/usr/bin/env python3
"""Render learn/source.md (USMS 核对汇总版) to learn/index.html.

Keeps teaching text. Does not summarize or drop sections.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARN = ROOT / "learn"
SOURCE = LEARN / "source.md"

ALIAS = {
    "0": "map",
    "1": "alts",
    "2": "s101",
    "3": "guides",
    "4": "layers",
    "5": "terms",
    "6": "gear-usms",
    "7": "drills",
    "7.1": "free",
    "7.2": "back",
    "7.3": "breast",
    "7.4": "fly",
    "7.5": "starts",
    "7.6": "turns",
    "7.7": "underwater",
    "8": "stroke-principles",
    "8.1": "free-path",
    "8.2": "back-path",
    "8.3": "breast-path",
    "8.4": "fly-path",
    "9": "wall",
    "10": "transfer",
    "11": "intensity",
    "12": "workout",
    "13": "plans",
    "14": "assess",
    "15": "ow",
    "16": "special",
    "17": "dryland",
    "18": "train-safety",
    "19": "video",
    "20": "coach",
    "21": "path",
    "22": "diag",
    "23": "fields",
    "24": "sources",
}

H3_ALIAS = {
    "1.2": "water",
}

NAV = [
    (
        "入口",
        [
            ("map", "总图"),
            ("meta", "体例"),
            ("alts", "入水 / ALTS"),
            ("s101", "Swimming 101"),
        ],
    ),
    (
        "四式",
        [
            ("guides", "Guide 怎么用"),
            ("drills", "220 条索引"),
            ("free", "自由泳"),
            ("back", "仰泳"),
            ("breast", "蛙泳"),
            ("fly", "蝶泳"),
        ],
    ),
    (
        "池壁",
        [
            ("starts", "出发"),
            ("turns", "转身"),
            ("underwater", "水下海豚腿"),
            ("wall", "Transition"),
        ],
    ),
    (
        "训练",
        [
            ("layers", "Drill / Set / Workout"),
            ("terms", "训练语言"),
            ("gear-usms", "器材约束"),
            ("stroke-principles", "四式原则与路径"),
            ("transfer", "Drill 迁移"),
            ("intensity", "强度方法"),
            ("workout", "写一堂课"),
            ("plans", "计划 / 六周"),
            ("assess", "测试与追踪"),
        ],
    ),
    (
        "目标",
        [
            ("ow", "开放水域"),
            ("special", "铁三 / 回归 / 低容量"),
            ("dryland", "陆上"),
        ],
    ),
    (
        "安全与诊断",
        [
            ("train-safety", "训练安全"),
            ("video", "录像分析"),
            ("path", "按目标选路径"),
            ("diag", "诊断模板"),
            ("fields", "处方字段"),
        ],
    ),
    ("附录", [("sources", "官方来源"), ("close", "结论")]),
]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def heading_id(title: str) -> str:
    if title.startswith("结论"):
        return "close"
    m = re.match(r"^(\d+\.\d+)\s+", title)
    if m:
        return ALIAS.get(m.group(1), "s-" + m.group(1).replace(".", "-"))
    m = re.match(r"^(\d+)\.\s+", title)
    if m:
        return ALIAS.get(m.group(1), "s-" + m.group(1))
    slug = re.sub(r"[^\w]+", "-", title, flags=re.U).strip("-")
    return slug[:48] or "sec"


def h3_id(title: str, parent: str, n: int) -> str:
    m = re.match(r"^(\d+\.\d+)\s+", title)
    if m and m.group(1) in H3_ALIAS:
        return H3_ALIAS[m.group(1)]
    if m:
        return "s-" + m.group(1).replace(".", "-")
    return f"{parent}-h{n}"


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"(?<!href=\")(?<!>)(https://[^\s)<]+)", r'<a href="\1">\1</a>', s)
    return s


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def is_table_sep(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def render_table(rows: list[str]) -> str:
    parsed: list[list[str]] = []
    for row in rows:
        if is_table_sep(row):
            continue
        parsed.append([c.strip() for c in row.strip().strip("|").split("|")])
    if not parsed:
        return ""
    width = max(len(r) for r in parsed)
    for r in parsed:
        while len(r) < width:
            r.append("")
    head, body = parsed[0], parsed[1:]
    parts = [
        '<div class="table-wrap">',
        "<table>",
        "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>",
        "<tbody>",
    ]
    for r in body:
        parts.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    parts.extend(["</tbody>", "</table>", "</div>"])
    return "\n".join(parts)


def render_blocks(text: str, parent_id: str = "sec") -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    h3_n = 0
    while i < n:
        line = lines[i]
        raw = line.rstrip()
        if not raw.strip():
            i += 1
            continue
        if raw.strip() == "---":
            i += 1
            continue
        if raw.startswith("```"):
            fence = [raw]
            i += 1
            while i < n and not lines[i].startswith("```"):
                fence.append(lines[i].rstrip("\n"))
                i += 1
            if i < n:
                i += 1
            code = "\n".join(fence[1:])
            out.append(f"<pre><code>{esc(code)}</code></pre>")
            continue
        if is_table_row(raw):
            rows = [raw]
            i += 1
            while i < n and (is_table_row(lines[i]) or not lines[i].strip()):
                if is_table_row(lines[i]):
                    rows.append(lines[i].rstrip())
                i += 1
            out.append(render_table(rows))
            continue
        if raw.startswith("> "):
            quote = [raw[2:]]
            i += 1
            while i < n and lines[i].startswith("> "):
                quote.append(lines[i][2:].rstrip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue
        if raw.startswith("### "):
            h3_n += 1
            title = raw[4:].strip()
            hid = h3_id(title, parent_id, h3_n)
            out.append(f'<h3 id="{esc(hid)}">{inline(title)}</h3>')
            i += 1
            continue
        if re.match(r"^[-*] ", raw):
            items: list[str] = []
            while i < n and re.match(r"^[-*] ", lines[i]):
                items.append(lines[i][2:].rstrip())
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", raw) and not raw.strip().endswith("。"):
            items = []
            start = i
            while i < n and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].rstrip()))
                i += 1
            if len(items) >= 2:
                out.append("<ol>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ol>")
                continue
            i = start
        out.append("<p>" + inline(raw) + "</p>")
        i += 1
    return "\n".join(out)


def is_sub_h2(title: str) -> bool:
    return bool(re.match(r"^\d+\.\d+\s+", title))


def split_preamble(preamble: str) -> tuple[str, str]:
    lede: list[str] = []
    rest: list[str] = []
    in_rest = False
    for line in preamble.split("\n"):
        if line.startswith("### "):
            in_rest = True
        if in_rest:
            rest.append(line)
        else:
            lede.append(line)
    return "\n".join(lede).strip(), "\n".join(rest).strip()


def parse_source(md: str) -> tuple[str, str, list[tuple[str, str, str]]]:
    lines = md.split("\n")
    title = "USMS 成人游泳训练体系"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    preamble: list[str] = []
    sections: list[tuple[str, str, str]] = []
    cur_id = ""
    cur_title = ""
    cur_body: list[str] = []

    def flush() -> None:
        nonlocal cur_id, cur_title, cur_body
        if cur_id:
            sections.append((cur_id, cur_title, "\n".join(cur_body).rstrip()))
        cur_id, cur_title, cur_body = "", "", []

    for line in lines:
        if line.startswith("## "):
            flush()
            cur_title = line[3:].strip()
            cur_id = heading_id(cur_title)
            cur_body = []
            continue
        if not cur_id:
            preamble.append(line)
        else:
            cur_body.append(line)
    flush()
    return title, "\n".join(preamble).strip("\n"), sections


def nav_html() -> str:
    parts = []
    for group, items in NAV:
        parts.append(f'<div class="g">{esc(group)}</div>')
        for href, label in items:
            parts.append(f'<a href="#{href}">{esc(label)}</a>')
    return "\n      ".join(parts)


def page_html(title: str, preamble: str, sections: list[tuple[str, str, str]]) -> str:
    lede, meta = split_preamble(preamble)
    body: list[str] = []
    body.append(
        '<header class="page-head">\n'
        f"      <h1>{inline(title)}</h1>\n"
        "      <p class=\"sub\">核对汇总版原文。下面按逐字稿展开，不按摘要压缩。</p>\n"
        "      <p class=\"site-cross\">上课口诀见 <a href=\"../strokes/\">四泳姿教学</a>。"
        "个人自救见 <a href=\"../safety/\">水中自救</a>。"
        "自由泳阶段诊断另见 <a href=\"freestyle/\">完整学习体系 3.0</a>。"
        "器材见 <a href=\"../gear/snorkels/\">呼吸管</a>、"
        "<a href=\"../gear/fins/\">脚蹼</a>、"
        "<a href=\"../gear/paddles/\">划手掌</a>。</p>\n"
        f"      {render_blocks(lede, 'lede')}\n"
        "    </header>"
    )
    if meta:
        body.append(
            f'<section id="meta" class="meta">\n'
            f"      {render_blocks(meta, 'meta')}\n"
            "    </section>"
        )
    for sid, heading, text in sections:
        blocks = render_blocks(text, sid)
        hclass = ' class="h2-sub"' if is_sub_h2(heading) else ""
        body.append(
            f'<section id="{esc(sid)}">\n'
            f"      <h2{hclass}>{inline(heading)}</h2>\n"
            f"      {blocks}\n"
            "    </section>"
        )
    inner = "\n\n    ".join(body)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>USMS 成人游泳训练体系</title>
  <meta name="description" content="USMS 成人游泳训练体系核对汇总版：入水、四式、出发转身、训练方法与安全边界。">
  <link rel="stylesheet" href="css/app.css">
  <link rel="stylesheet" href="../css/site.css">
</head>
<body class="page-learn">
<header class="site-bar">
  <a class="site-brand" href="../">成人游泳训练</a>
  <nav aria-label="站点">
    <a href="./" aria-current="page">学习</a>
    <a href="../safety/">自救</a>
    <a href="../gear/snorkels/">呼吸管</a>
    <a href="../gear/paddles/">划手掌</a>
    <a href="../gear/fins/">脚蹼</a>
  </nav>
</header>
<div class="app">
  <aside class="side">
    <p class="brand">USMS 成人游泳训练体系</p>
    <div class="ver">核对汇总版 · 2026-08-21</div>
    <nav>
      {nav_html()}
    </nav>
  </aside>

  <main class="main">
    {inner}
  </main>
</div>
<script src="js/nav.js?4"></script>
</body>
</html>
"""


def main() -> None:
    md = SOURCE.read_text(encoding="utf-8")
    title, preamble, sections = parse_source(md)
    html_out = page_html(title, preamble, sections)
    (LEARN / "index.html").write_text(html_out, encoding="utf-8")
    visible = re.sub(r"<script[\s\S]*?</script>", "", html_out)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible)
    src_h2 = len(re.findall(r"^## ", md, re.M))
    html_h2 = len(sections)
    print(
        f"source_chars={len(md)} sections={len(sections)} "
        f"md_h2={src_h2} html_h2={html_h2} "
        f"html_bytes={len(html_out.encode())} visible_chars={len(visible.strip())}"
    )
    if html_h2 != src_h2:
        raise SystemExit(f"h2 mismatch: md={src_h2} html={html_h2}")


if __name__ == "__main__":
    main()
