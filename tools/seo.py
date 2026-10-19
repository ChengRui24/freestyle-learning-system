#!/usr/bin/env python3
"""Shared search metadata for the GitHub Pages site.

Change ORIGIN here if the site moves to a custom domain, then re-run this
file and the page renderers. `python3 tools/seo.py` refreshes the sitemap
and the <head> of every public HTML page.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://chengrui24.github.io/freestyle-learning-system"
SITE_NAME = "成人游泳训练"
OG_IMAGE = f"{ORIGIN}/og.png"
FAVICON = f"{ORIGIN}/favicon.svg"
LASTMOD = "2026-10-19"

PAGES: dict[str, dict] = {
    "home": {
        "file": "index.html",
        "title": "成人游泳训练",
        "description": "成人游泳训练入口：USMS 学习体系、水中自救，以及 FINIS 呼吸管、划手掌、脚蹼选型。",
        "path": "/",
        "crumbs": [],
    },
    "learn": {
        "file": "learn/index.html",
        "title": "USMS 成人游泳训练体系",
        "description": "USMS 成人游泳训练体系核对汇总版：入水、四式、出发转身、训练方法与安全边界。",
        "path": "/learn/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习")],
    },
    "course": {
        "file": "learn/course/index.html",
        "title": "成人游泳课程安排",
        "description": "四式共用的上课安排：定阶段、看一个现象、做一个专项，再回到完整泳姿复测。包含通过条件，以及热身、专项、主项和放松。",
        "path": "/learn/course/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习"), ("/learn/course/", "课程安排")],
    },
    "freestyle": {
        "file": "learn/freestyle/index.html",
        "title": "自由泳完整学习体系 3.0",
        "description": "爬泳／自由泳学习阶段、里程碑、问题诊断与专项练习库。专项练习不是终点，回到完整自由泳后仍然改善，才算真正学会。",
        "path": "/learn/freestyle/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习"), ("/learn/freestyle/", "自由泳")],
    },
    "back": {
        "file": "learn/back/index.html",
        "title": "仰泳学习体系",
        "description": "仰泳学习阶段、现象诊断和专项练习。用来判断卡在哪一环，再按课堂教学口令从陆上练到水中，回到完整仰泳复测。",
        "path": "/learn/back/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习"), ("/learn/back/", "仰泳")],
    },
    "fly": {
        "file": "learn/fly/index.html",
        "title": "蝶泳学习体系",
        "description": "蝶泳学习阶段、现象诊断和专项练习。先定最弱的一环，做一个专项，再回到完整蝶泳复测。蝶泳不作为第一种入水泳姿。",
        "path": "/learn/fly/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习"), ("/learn/fly/", "蝶泳")],
    },
    "breast": {
        "file": "learn/breast/index.html",
        "title": "蛙泳学习体系",
        "description": "蛙泳学习阶段、现象诊断和专项练习。入水、漂浮和回站是共用前提。选一个专项后，回到完整蛙泳确认改进还在。",
        "path": "/learn/breast/",
        "crumbs": [("/", "成人游泳训练"), ("/learn/", "学习"), ("/learn/breast/", "蛙泳")],
    },
    "strokes": {
        "file": "strokes/index.html",
        "title": "四泳姿教学 · 通用路径与连贯口令",
        "description": "自由泳、仰泳、蝶泳、蛙泳共用的学习路径和连贯口令。各式的阶段诊断和课堂教学在对应泳姿册里。",
        "path": "/strokes/",
        "crumbs": [("/", "成人游泳训练"), ("/strokes/", "四泳姿")],
    },
    "safety": {
        "file": "safety/index.html",
        "title": "成人水中自救与个人生存",
        "description": "成人水中自救与个人生存：稳、浮、看、喊、抓、移、出。含泳池回墙、沿壁逃生，以及湖海河流等事故路线。",
        "path": "/safety/",
        "crumbs": [("/", "成人游泳训练"), ("/safety/", "水中自救")],
    },
    "gear": {
        "file": "gear/index.html",
        "title": "成人游泳训练器材",
        "description": "成人游泳训练器材选型，目前以 FINIS 为样本：呼吸管、划手掌、脚蹼。先用器材放大一个问题，再脱掉复测。",
        "path": "/gear/",
        "crumbs": [("/", "成人游泳训练"), ("/gear/", "器材")],
    },
    "snorkels": {
        "file": "gear/snorkels/index.html",
        "title": "FINIS 游泳呼吸管产品线与配件完整对比",
        "description": "四款 FINIS 成人中置呼吸管、功能配件和维修件对比。用来暂时拿掉换气，专心看划水和身体线。",
        "path": "/gear/snorkels/",
        "crumbs": [("/", "成人游泳训练"), ("/gear/", "器材"), ("/gear/snorkels/", "呼吸管")],
    },
    "paddles": {
        "file": "gear/paddles/index.html",
        "title": "FINIS 划手掌（手蹼）介绍与对比",
        "description": "六款 FINIS 划手掌的结构、反馈和训练边界：加阻力、技术反馈、路线和高肘约束。按要放大的问题来选。",
        "path": "/gear/paddles/",
        "crumbs": [("/", "成人游泳训练"), ("/gear/", "器材"), ("/gear/paddles/", "划手掌")],
    },
    "fins": {
        "file": "gear/fins/index.html",
        "title": "FINIS 成人训练脚蹼选择指南",
        "description": "六款 FINIS 成人训练脚蹼，按 Tech Sheet 比较叶片受力、推进、浮力和踢腿节奏后再选型。",
        "path": "/gear/fins/",
        "crumbs": [("/", "成人游泳训练"), ("/gear/", "器材"), ("/gear/fins/", "脚蹼")],
    },
}

SITEMAP_ORDER = [
    "home",
    "learn",
    "course",
    "strokes",
    "freestyle",
    "back",
    "fly",
    "breast",
    "safety",
    "gear",
    "snorkels",
    "paddles",
    "fins",
]


def abs_url(path: str) -> str:
    if path == "/":
        return ORIGIN + "/"
    return ORIGIN + path


def head_for(key: str) -> str:
    page = PAGES[key]
    url = abs_url(page["path"])
    title = page["title"]
    description = page["description"]
    title_html = html.escape(title, quote=True)
    description_html = html.escape(description, quote=True)
    site_description = PAGES["home"]["description"]
    graph: list[dict] = [
        {
            "@type": "WebSite",
            "@id": abs_url("/") + "#website",
            "name": SITE_NAME,
            "url": abs_url("/"),
            "description": site_description,
            "inLanguage": "zh-CN",
        }
    ]
    webpage: dict = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": abs_url("/") + "#website"},
        "inLanguage": "zh-CN",
        "primaryImageOfPage": {"@type": "ImageObject", "url": OG_IMAGE},
    }
    crumbs = page["crumbs"]
    if len(crumbs) > 1:
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index + 1,
                        "name": name,
                        "item": abs_url(path),
                    }
                    for index, (path, name) in enumerate(crumbs)
                ],
            }
        )
    graph.append(webpage)
    payload = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("<", "\\u003c")
    return "\n".join(
        [
            f"  <title>{title_html}</title>",
            f'  <meta name="description" content="{description_html}">',
            '  <meta name="robots" content="index, follow">',
            f'  <link rel="canonical" href="{url}">',
            f'  <link rel="icon" href="{FAVICON}" type="image/svg+xml">',
            '  <meta property="og:type" content="website">',
            '  <meta property="og:locale" content="zh_CN">',
            f'  <meta property="og:site_name" content="{SITE_NAME}">',
            f'  <meta property="og:title" content="{title_html}">',
            f'  <meta property="og:description" content="{description_html}">',
            f'  <meta property="og:url" content="{url}">',
            f'  <meta property="og:image" content="{OG_IMAGE}">',
            '  <meta property="og:image:type" content="image/png">',
            '  <meta property="og:image:width" content="1200">',
            '  <meta property="og:image:height" content="630">',
            f'  <meta property="og:image:alt" content="{SITE_NAME}">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{title_html}">',
            f'  <meta name="twitter:description" content="{description_html}">',
            f'  <meta name="twitter:image" content="{OG_IMAGE}">',
            f'  <script type="application/ld+json">{payload}</script>',
        ]
    )


def sitemap_xml() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for key in SITEMAP_ORDER:
        loc = abs_url(PAGES[key]["path"])
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{LASTMOD}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


_FRESH = re.compile(
    r"[ \t]*<title>.*?</title>(?:[ \t]*\n[ \t]*<meta name=\"description\" content=\"[^\"]*\">)?[ \t]*\n?"
)
_EXISTING = re.compile(
    r"[ \t]*<title>.*?</title>.*?<script type=\"application/ld\+json\">.*?</script>[ \t]*\n?",
    re.DOTALL,
)


def apply_head(text: str, key: str) -> str:
    block = head_for(key) + "\n"
    existing = _EXISTING.search(text)
    if existing and 'rel="canonical"' in existing.group(0):
        return text[: existing.start()] + block + text[existing.end() :]
    fresh = _FRESH.search(text)
    if not fresh:
        raise SystemExit(f"{key}: no <title> to replace")
    return text[: fresh.start()] + block + text[fresh.end() :]


def main() -> None:
    for key, page in PAGES.items():
        path = ROOT / page["file"]
        original = path.read_text(encoding="utf-8")
        updated = apply_head(original, key)
        if updated == original:
            print(f"unchanged {page['file']}")
            continue
        path.write_text(updated, encoding="utf-8")
        print(f"updated {page['file']}")
    sitemap = ROOT / "sitemap.xml"
    sitemap.write_text(sitemap_xml(), encoding="utf-8")
    print(f"wrote {sitemap.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
