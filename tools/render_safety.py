#!/usr/bin/env python3
"""Build safety/source.md from the ChatGPT transcripts and render safety/index.html.

Keeps teaching text. Only strips UI citation crumbs and obvious OCR glitches.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from seo import head_for  # noqa: E402
SAFETY = ROOT / "safety"
RAW_DIR = SAFETY / "raw"

CITE_LINES = {
    "美国大师游泳",
    "基督教青年会",
    "Red Cross",
    "Swim England",
    "游泳档案馆",
    "游泳协会",
    "健康政府",
    "PADI",
    "PADI 博客",
    "PADI Travel",
    "PADI Pros Blog",
    "Aeawave",
    "Halliwick",
    "lifesaving.org",
    "Royal Life Saving Society - Australia",
}
CITE_LINE_RE = re.compile(r"^(\+\d+|Red Cross|Swim England)$")

CN = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

HEADING_RE = re.compile(r"^([一二三四五六七八九十]+)、(.+)$")
NUM_TITLE_RE = re.compile(r"^(\d+)\.\s+(\S.*)$")
LETTER_TITLE_RE = re.compile(r"^([A-F])\.\s+(.+)$")

ALIAS = {
    1: "intro",
    2: "use",
    3: "bound",
    4: "core",
    10: "move",
    14: "exit",
    15: "pool",
    21: "still",
    26: "surf",
    31: "river",
    36: "boat",
    41: "cold",
    45: "other",
    52: "cross",
    55: "course",
    56: "lessons",
    58: "levels",
    60: "tests",
    61: "myths",
    62: "model",
}

NAV = [
    ("使用", [("intro", "体系定位"), ("use", "动作链"), ("bound", "自学边界")]),
    (
        "共用技术",
        [
            ("core", "核心技术库"),
            ("s-5", "仰漂"),
            ("s-7", "Log Roll"),
            ("s-8", "踩水"),
            ("move", "生存推进"),
            ("s-11", "Swim–Float–Swim"),
            ("exit", "离水"),
        ],
    ),
    (
        "情景",
        [
            ("pool", "泳池"),
            ("still", "湖库静水"),
            ("surf", "海岸"),
            ("river", "河流"),
            ("boat", "船艇"),
            ("cold", "冷水"),
            ("other", "洪水 / 车辆 / 冰面 / 码头"),
            ("cross", "抽筋 / 无镜 / 衣物"),
        ],
    ),
    (
        "训练",
        [
            ("course", "教学路线"),
            ("lessons", "12 课时"),
            ("levels", "能力等级"),
            ("tests", "综合测试"),
            ("myths", "常见误区"),
            ("model", "六层模型"),
        ],
    ),
    ("泳池细练", [("pool-extra", "对话第一段全文")]),
]


def cn_to_int(s: str) -> int:
    if s == "十":
        return 10
    if s.startswith("十"):
        return 10 + cn_to_int(s[1:]) if len(s) > 1 else 10
    if "十" in s:
        a, b = s.split("十", 1)
        tens = cn_to_int(a) if a else 1
        return tens * 10 + (cn_to_int(b) if b else 0)
    if len(s) == 1:
        return CN[s]
    raise ValueError(s)


def clean_transcript(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("编辑\n"):
        text = text[len("编辑\n") :]
    text = text.replace("-交替踏步", "交替踏步")
    text = text.replace("-冰面破裂", "冰面破裂")
    out: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped in CITE_LINES or CITE_LINE_RE.fullmatch(stripped):
            continue
        out.append(line.rstrip())
    cleaned = "\n".join(out)
    while "\n\n\n\n" in cleaned:
        cleaned = cleaned.replace("\n\n\n\n", "\n\n\n")
    return cleaned.strip() + "\n"


def build_source() -> str:
    full = clean_transcript((RAW_DIR / "complete.txt").read_text(encoding="utf-8"))
    pool = clean_transcript((RAW_DIR / "pool.txt").read_text(encoding="utf-8"))
    header = (
        "# 成人水中自救与个人生存：完整学习、教学与专项训练体系\n"
        "\n"
        "对话原文整理。第一部分是完整体系；第二部分是同一对话里更细的泳池专项，不删减并入。\n"
        "\n"
        "---\n\n"
    )
    extra = (
        "\n---\n\n"
        "# 泳池专项细练\n\n"
        "以下为同一对话中、在完整体系之前给出的泳池专项全文。"
        "与上文泳池情景互补：能踩到底 / 深水回墙拆法、Wall Crawl 细练、泳道线三项、"
        "Bobbing 深浅转换、360° 决策练习、无泳镜与浮具、以及 P0–P9 路线。\n\n"
    )
    return header + full + extra + pool


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def is_tsv_row(line: str) -> bool:
    return "\t" in line and len(line.split("\t")) >= 2


def render_table(rows: list[str]) -> str:
    parsed = [[c.strip() for c in row.split("\t")] for row in rows]
    width = max(len(r) for r in parsed)
    for r in parsed:
        while len(r) < width:
            r.append("")
    head, body = parsed[0], parsed[1:]
    html_rows = ["<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>"]
    html_rows.append("<tbody>")
    for r in body:
        html_rows.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    html_rows.append("</tbody>")
    return "<table>\n" + "\n".join(html_rows) + "\n</table>"


def render_order(parts: list[str]) -> str:
    bits: list[str] = []
    for i, p in enumerate(parts):
        if i:
            bits.append('<span class="arr" aria-hidden="true">→</span>')
        bits.append(f"<span>{inline(p)}</span>")
    return '<div class="order">' + "".join(bits) + "</div>"


def split_arrows(text: str) -> list[str] | None:
    if "→" not in text and "↓" not in text:
        return None
    # Keep long teaching sentences as paragraphs, even if they contain arrows.
    if "。" in text or (text.count("；") >= 1 and len(text) > 40):
        return None
    if len(text) > 80 and text.count("→") + text.count("↓") <= 3:
        return None
    parts = [p.strip(" 。；") for p in re.split(r"[→↓]", text) if p.strip(" 。；")]
    if len(parts) >= 3 and max(len(p) for p in parts) <= 24:
        return parts
    if len(parts) >= 3 and all(len(p) <= 40 for p in parts):
        return parts
    return None


def render_blocks(lines: list[str]) -> str:
    html_parts: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if is_tsv_row(line):
            rows = [line]
            i += 1
            while i < n and is_tsv_row(lines[i]):
                rows.append(lines[i])
                i += 1
            html_parts.append(render_table(rows))
            continue
        m_num = NUM_TITLE_RE.match(line)
        if m_num and len(line) < 80 and not line.endswith("。"):
            html_parts.append(f"<h3>{inline(m_num.group(1) + '. ' + m_num.group(2))}</h3>")
            i += 1
            continue
        m_let = LETTER_TITLE_RE.match(line)
        if m_let and len(line) < 80:
            html_parts.append(f"<h3>{inline(m_let.group(1) + '. ' + m_let.group(2))}</h3>")
            i += 1
            continue
        if line.strip() in ("↓", "→"):
            chain: list[str] = []
            while i < n:
                cur = lines[i].strip()
                if cur in ("↓", "→"):
                    i += 1
                    continue
                if not cur:
                    j = i + 1
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and lines[j].strip() in ("↓", "→"):
                        i = j
                        continue
                    if chain and j < n:
                        look = lines[j].strip()
                        if look and not HEADING_RE.match(look) and look not in ("↓", "→"):
                            if i < n and not lines[i].strip():
                                pass
                    break
                chain.append(cur.rstrip("。"))
                i += 1
                if i < n and lines[i].strip() == "":
                    j = i + 1
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and lines[j].strip() in ("↓", "→"):
                        i = j
                        continue
                    break
            if len(chain) >= 2:
                html_parts.append(render_order(chain))
            elif chain:
                html_parts.append("<p>" + inline(chain[0]) + "</p>")
            continue
        if line.startswith("→"):
            chain = [line.lstrip("→").strip()]
            i += 1
            while i < n and lines[i].startswith("→"):
                chain.append(lines[i].lstrip("→").strip())
                i += 1
            html_parts.append(render_order(chain))
            continue
        arrows = split_arrows(line)
        if arrows:
            html_parts.append(render_order(arrows))
            i += 1
            continue
        if line.endswith("；") or line.endswith(";"):
            items = []
            start = i
            while i < n and (lines[i].endswith("；") or lines[i].endswith(";")):
                items.append(lines[i].rstrip("；;"))
                i += 1
                while i < n and not lines[i].strip():
                    i += 1
            if len(items) >= 2:
                html_parts.append(
                    "<ul>" + "".join(f"<li>{inline(it)}</li>" for it in items) + "</ul>"
                )
                continue
            i = start
            html_parts.append("<p>" + inline(line) + "</p>")
            i += 1
            continue
        html_parts.append("<p>" + inline(line) + "</p>")
        i += 1
    return "\n".join(html_parts)


def parse_sections(md: str) -> tuple[str, list[tuple[str, str, str]]]:
    lines = md.split("\n")
    preamble: list[str] = []
    sections: list[tuple[str, str, str]] = []
    cur_id = ""
    cur_title = ""
    cur_body: list[str] = []
    extra_mode = False
    extra_n = 0

    def flush() -> None:
        nonlocal cur_id, cur_title, cur_body
        if cur_id:
            sections.append((cur_id, cur_title, "\n".join(cur_body).strip("\n")))
        cur_id, cur_title, cur_body = "", "", []

    for line in lines:
        if line.startswith("# 泳池专项细练"):
            flush()
            extra_mode = True
            cur_id, cur_title = "pool-extra", "泳池专项细练"
            continue
        m = HEADING_RE.match(line)
        if m:
            flush()
            title = m.group(1) + "、" + m.group(2)
            if extra_mode:
                extra_n += 1
                cur_id = f"p-{extra_n}"
            else:
                try:
                    num = cn_to_int(m.group(1))
                except (KeyError, ValueError):
                    num = 0
                cur_id = ALIAS.get(num, f"s-{num}" if num else re.sub(r"\W+", "-", m.group(1)))
            cur_title = title
            cur_body = []
            continue
        if not cur_id:
            preamble.append(line)
        else:
            cur_body.append(line)
    flush()
    return "\n".join(preamble).strip(), sections


def nav_html() -> str:
    parts = []
    for group, items in NAV:
        parts.append(f'<div class="g">{esc(group)}</div>')
        for href, label in items:
            parts.append(f'<a href="#{href}">{esc(label)}</a>')
    return "\n      ".join(parts)


def page_html(preamble: str, sections: list[tuple[str, str, str]]) -> str:
    body_sections = []
    pre_lines = [
        ln
        for ln in preamble.split("\n")
        if ln.strip() and not ln.startswith("#") and ln.strip() != "---"
    ]
    intro = render_blocks(pre_lines)
    body_sections.append(
        '<header class="page-head">\n'
        "      <h1>成人水中自救与个人生存</h1>\n"
        "      <p class=\"sub\">完整学习、教学与专项训练体系。下面按对话原文展开，不按摘要压缩。</p>\n"
        '      <p class="site-cross">泳姿学习见 <a href="../learn/">USMS 成人游泳训练体系</a>。'
        '阶段诊断见 <a href="../learn/freestyle/">自由泳</a>、'
        '<a href="../learn/back/">仰泳</a>、'
        '<a href="../learn/fly/">蝶泳</a>、'
        '<a href="../learn/breast/">蛙泳</a>。'
        "会自由泳不等于会自救。器材隔离变量见 "
        '<a href="../gear/snorkels/">呼吸管</a>、'
        '<a href="../gear/fins/">脚蹼</a>、'
        '<a href="../gear/paddles/">划手掌</a>。</p>\n'
        f"      {intro}\n"
        "    </header>"
    )
    for sid, title, body in sections:
        blocks = render_blocks(body.split("\n"))
        body_sections.append(
            f'<section id="{esc(sid)}">\n'
            f"      <h2>{inline(title)}</h2>\n"
            f"      {blocks}\n"
            "    </section>"
        )
    inner = "\n\n    ".join(body_sections)
    seo = head_for("safety")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
{seo}
  <link rel="stylesheet" href="../learn/css/app.css">
  <link rel="stylesheet" href="../css/site.css">
</head>
<body class="page-safety">
<header class="site-bar">
  <a class="site-brand" href="../">成人游泳训练</a>
  <nav aria-label="站点">
    <a href="../learn/">学习</a>
    <a href="./" aria-current="page">自救</a>
    <a href="../gear/">器材</a>
  </nav>
</header>
<div class="app">
  <aside class="side">
    <p class="brand">成人水中自救与个人生存</p>
    <div class="ver">对话原文 · 完整体系 / 泳池细练</div>
    <nav>
      {nav_html()}
    </nav>
  </aside>

  <main class="main">
    {inner}
  </main>
</div>
<script src="js/app.js?4"></script>
</body>
</html>
"""


def main() -> None:
    if not (RAW_DIR / "complete.txt").exists():
        raise SystemExit(f"missing transcripts in {RAW_DIR}")
    source = build_source()
    (SAFETY / "source.md").write_text(source, encoding="utf-8")
    preamble, sections = parse_sections(source)
    html_out = page_html(preamble, sections)
    (SAFETY / "index.html").write_text(html_out, encoding="utf-8")
    visible = re.sub(r"<script[\s\S]*?</script>", "", html_out)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible)
    print(
        f"source_chars={len(source)} sections={len(sections)} "
        f"html_bytes={len(html_out.encode())} visible_chars={len(visible.strip())}"
    )


if __name__ == "__main__":
    main()
