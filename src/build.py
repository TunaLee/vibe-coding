#!/usr/bin/env python3
"""바이브코딩 온라인 강의 덱을 만든다 → docs/

사용: python3 src/build.py  →  부마다 한 파일 (단원별로 나누지 않는다)
  docs/part1.html  1부 [부 표지 → 단원마다 단원 표지 · 1부 지도 · 본문 · 산출물]
  docs/part2.html  2부 [같은 틀]
  docs/part3.html  3부 [표지 · 목차 · 차시 간지 · 본문]
  docs/index.html  부 · 단원 목록 (part1.html#u-1-3 처럼 단원 표지로 바로 열림)
"""
import importlib
import os
import sys
from pathlib import Path

import art
import deck
import deck_gas
import explain
import hx
import intro
import stats_hx

ROOT = Path(__file__).resolve().parent.parent
BASE_CSS = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS



def _tpl(css):
    return (ROOT / "src" / "template.html").read_text().replace("</style>", css + "</style>", 1)


def _write(name, tpl, title, parts):
    out = ROOT / "docs" / name
    out.write_text(tpl.replace("{{DECK_TITLE}}", title).replace("{{SLIDES}}", "\n\n".join(parts)))
    print(name, len(parts) - 1, "장")


def make_lab_zips():
    """실습 뼈대 → docs/dl/<이름>.zip (덱에서 바로 내려받기)."""
    import zipfile
    dl = ROOT / "docs" / "dl"
    dl.mkdir(exist_ok=True)
    for name in ("delegate_todo",):
        src = ROOT / "labs" / name
        with zipfile.ZipFile(dl / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(src.rglob("*")):
                if f.is_file() and f.name != ".DS_Store":
                    z.write(f, Path(name) / f.relative_to(src))


def _part_cover(n, title):
    return f'''<section id="p{n}" class="slide dk cover-dk" data-title="{n}부 {title}">
  <div class="glow"></div>
  <div class="kick">바이브코딩 · {n}부</div>
  <h1>{title}</h1>
</section>'''




PARTS = [(1, "바이브코딩 입문"), (2, "바이브코딩 심화"), (3, "하네스 엔지니어링")]


def _landing(course):
    """docs/index.html — 부 · 단원 목록 (단원을 누르면 그 부 파일의 단원 표지로)."""
    cols = "".join(
        f'<section><h2><a href="part{n}.html">{n}부 · {t}</a></h2><ol>'
        + "".join(f'<li><a href="part{n}.html#u-{c}">{c} {ut}</a></li>' for c, ut in units) + "</ol></section>"
        for n, t, units in course)
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>바이브코딩 강의</title><style>body{font-family:-apple-system,"Pretendard",sans-serif;max-width:760px;margin:48px auto;'
            'padding:0 16px;color:#16233A;background:#fff}h1{font-size:28px}h2{font-size:20px;margin-top:32px}h2 a{color:#F28C28}'
            'li{margin:8px 0;font-size:17px}a{color:#16233A}</style></head><body><h1>바이브코딩 강의</h1>' + cols + "</body></html>")


def build():
    import v1kit
    import v2kit
    import v3kit
    import vibe3
    make_lab_zips()
    course = [(1, PARTS[0][1], [(u, t) for u, t, _, _ in v1kit.UNITS]),
              (2, PARTS[1][1], [(u, t) for u, t, _, _ in v2kit.UNITS]),
              (3, PARTS[2][1], [(c, t) for c, t, _ in v3kit.AGENDA])]
    (ROOT / "docs" / "index.html").write_text(_landing(course))
    for n, kit, pre in ((1, v1kit, "v1_u"), (2, v2kit, "v2_u")):
        css = BASE_CSS + v3kit.CSS + v1kit.CSS + (v2kit.CSS if n == 2 else "")
        parts = [art.DEFS, _part_cover(n, PARTS[n - 1][1]).replace('cover-dk"', 'cover-dk active"', 1)]
        for i, (u, _, _, _) in enumerate(kit.UNITS, 1):
            mod = importlib.import_module(f"{pre}{i}")
            css += getattr(mod, "CSS", "")
            parts += [kit.cover(u), kit.roadmap(u)] + mod.slides() + [kit.nextup(u)]
        _write(f"part{n}.html", _tpl(css), f"{n}부 {PARTS[n - 1][1]}", parts)
    p3 = vibe3.slides()
    p3[0] = p3[0].replace('data-title="표지"', 'id="p3" data-title="3부 하네스 엔지니어링"', 1)
    k = 0
    for j, s in enumerate(p3):
        if 'class="slide dk divider"' in s and k < len(v3kit.AGENDA):
            p3[j] = s.replace("<section ", f'<section id="u-{v3kit.AGENDA[k][0]}" ', 1)
            k += 1
    _write("part3.html", _tpl(BASE_CSS + vibe3.CSS), "3부 하네스 엔지니어링", [art.DEFS] + p3)


if __name__ == "__main__":
    build()
