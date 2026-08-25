#!/usr/bin/env python3
"""Extract structured data from source.md for the static site."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARN = ROOT / "learn"
MD = (LEARN / "source.md").read_text(encoding="utf-8")


def split_table(block: str) -> list[list[str]]:
    rows = []
    for line in block.strip().splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    return rows


def extract_stages() -> list[dict]:
    m = re.search(r"# 2\. 自由泳完整学习主线\n\n(\|.+?)\n\n# 3\.", MD, re.S)
    if not m:
        raise SystemExit("stages table not found")
    rows = split_table(m.group(1))[1:]
    out = []
    for stage, task, milestone, stuck in rows:
        code = stage.split()[0]
        name = stage[len(code) :].strip()
        out.append(
            {
                "id": code,
                "name": name,
                "task": task,
                "milestone": milestone,
                "stuck": stuck,
            }
        )
    return out


def extract_c_tables() -> dict[str, list[dict]]:
    sections = {
        "C1": ("C1 呼吸与换气", "C2 身体线型和平衡"),
        "C2": ("C2 身体线型和平衡", "C3 打腿"),
        "C3": ("C3 打腿", "C4 身体转动、移臂和入水"),
        "C4": ("C4 身体转动、移臂和入水", "C5 抱水、划水和推水"),
        "C5": ("C5 抱水、划水和推水", "C6 完整配合、节奏和技术耐力"),
        "C6": ("C6 完整配合、节奏和技术耐力", "# 15."),
    }
    titles = {
        "C1": "呼吸与换气",
        "C2": "身体线型和平衡",
        "C3": "打腿",
        "C4": "身体转动、移臂和入水",
        "C5": "抱水、划水和推水",
        "C6": "完整配合、节奏和技术耐力",
    }
    result: dict[str, list[dict]] = {}
    for key, (start, end) in sections.items():
        m = re.search(re.escape(start) + r"(.+?)" + re.escape(end), MD, re.S)
        if not m:
            raise SystemExit(f"C table {key} not found")
        table = split_table(m.group(1))[1:]
        items = []
        for code_name, locate, impact, drills in table:
            parts = code_name.split(" ", 1)
            items.append(
                {
                    "id": parts[0],
                    "name": parts[1] if len(parts) > 1 else "",
                    "locate": locate,
                    "impact": impact,
                    "drills": drills,
                    "group": key,
                    "groupTitle": titles[key],
                }
            )
        result[key] = items
    return result


def extract_quick_tests() -> list[dict]:
    m = re.search(r"# 13\. 快速诊断测试\n\n(\|.+?)\n\n# 14\.", MD, re.S)
    if not m:
        raise SystemExit("quick tests not found")
    rows = split_table(m.group(1))[1:]
    return [{"result": a, "suspect": b} for a, b in rows]


def extract_drills() -> list[dict]:
    start = MD.find("# D-BP 身体位置、浮力与转动")
    end = MD.find("# 16. 常用专项练习链")
    body = MD[start:end]
    chunks = re.split(r"\n## (D-[A-Z]+(?:\d+[A-Z]?)[^\n]*)\n", body)
    cats = {
        "D-BP": "身体位置、浮力与转动",
        "D-K": "打腿",
        "D-P": "水感、抱水、划水和推水",
        "D-R": "移臂、入水和前方衔接",
        "D-BR": "呼吸与换气",
        "D-I": "单臂、左右协调与完整动作迁移",
        "D-E": "效率、节奏和技术耐力",
        "D-OW": "开放水域",
    }
    drills = []
    # chunks[0] is preamble; then title, body, title, body...
    for i in range(1, len(chunks), 2):
        title = chunks[i].strip()
        text = chunks[i + 1].strip()
        text = re.sub(r"\n---\s*\n# .+\s*$", "", text)
        text = re.sub(r"\n---\s*$", "", text)
        text = re.sub(r"\n# D-[A-Z].+\s*$", "", text)
        text = text.strip()
        m = re.match(r"(D-[A-Z]+)(\d+[A-Z]?)\s+(.+)", title)
        if not m:
            raise SystemExit(f"bad drill title: {title}")
        prefix, num, name = m.group(1), m.group(2), m.group(3)
        en = ""
        if "｜" in name:
            name, en = [x.strip() for x in name.split("｜", 1)]
        elif " / " in name:
            # keep full Chinese-facing name
            pass
        drills.append(
            {
                "id": f"{prefix}{num}",
                "prefix": prefix,
                "category": cats[prefix],
                "name": name,
                "en": en,
                "body": text,
            }
        )
    return drills


def extract_chains() -> list[dict]:
    start = MD.find("# 16. 常用专项练习链")
    end = MD.find("# 17. 单次训练闭环")
    body = MD[start:end]
    parts = re.split(r"\n## (16\.\d+ [^\n]+)\n", body)
    chains = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        text = parts[i + 1].strip()
        steps = [ln.strip() for ln in text.splitlines() if ln.strip() and ln.strip() != "---"]
        chains.append({"id": title.split()[0], "title": title, "steps": steps})
    return chains


def main() -> None:
    data = {
        "stages": extract_stages(),
        "quickTests": extract_quick_tests(),
        "symptoms": extract_c_tables(),
        "drills": extract_drills(),
        "chains": extract_chains(),
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    (LEARN / "data.json").write_text(payload, encoding="utf-8")
    (LEARN / "data.js").write_text(
        "window.FS_DATA = " + payload + ";\n", encoding="utf-8"
    )
    print(
        f"stages={len(data['stages'])} "
        f"symptoms={sum(len(v) for v in data['symptoms'].values())} "
        f"drills={len(data['drills'])} "
        f"chains={len(data['chains'])}"
    )


if __name__ == "__main__":
    main()
