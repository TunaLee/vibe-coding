#!/usr/bin/env python3
"""바이브코딩 온라인 강의 덱을 만든다 → docs/

사용: python3 src/build.py  →  docs/index.html 한 파일 (1부 · 2부 · 3부 전체, 단원별 파일로 나누지 않는다)
  표지 → 과정 지도 → 1부 [단원 표지 · 1부 지도 · 본문 · 산출물] → 2부 [같은 틀] → 3부 [표지 · 목차 · 차시 간지 · 본문]
  단원 사이 링크는 덱 안 이동 (#u-1-1 …)
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


def _course_map(parts):
    cols = "".join(
        f'<div class="vamc"><a class="vamh" href="#p{n}">{n}부 · {t}</a>'
        + "".join(f'<a class="vamu" href="#u-{c}"><span>{c}</span>{ut}</a>' for c, ut in units) + "</div>"
        for n, t, units in parts)
    return f'''<section class="slide" data-title="과정 지도">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <h2>과정 지도</h2>
  <div class="vam">{cols}</div>
</section>'''


MAP_CSS = """
  .vam{display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:6px;}
  .vamc{display:flex; flex-direction:column; gap:7px;}
  .vamh{font-size:20px; font-weight:800; color:#fff; background:#16233A; border-radius:12px; padding:10px 14px; text-decoration:none; margin-bottom:4px;}
  .vamu{display:flex; gap:10px; align-items:baseline; font-size:17px; font-weight:600; color:#16233A; text-decoration:none;
    background:#F4F6F9; border-radius:10px; padding:8px 12px;}
  .vamu span{font-family:var(--mono); font-size:14px; font-weight:800; color:#E07A12; flex:none;}
  .vamu:hover,.vamh:hover{outline:2px solid #F28C28;}
"""


def build():
    import v1kit
    import v2kit
    import v3kit
    import vibe3
    make_lab_zips()
    css, parts = BASE_CSS + v3kit.CSS + v1kit.CSS + v2kit.CSS + MAP_CSS, []
    seen = set()

    def add_css(c):
        nonlocal css
        if c and c not in seen:
            seen.add(c)
            css += c

    course = [(1, "바이브코딩 입문", [(u, t) for u, t, _, _ in v1kit.UNITS]),
              (2, "바이브코딩 심화", [(u, t) for u, t, _, _ in v2kit.UNITS]),
              (3, "하네스 엔지니어링", [(c, t) for c, t, _ in v3kit.AGENDA])]
    parts += [art.DEFS, '''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">1부 입문 · 2부 심화 · 3부 하네스 엔지니어링</div>
  <h1>바이브코딩</h1>
</section>''', _course_map(course)]
    for n, kit, pre in ((1, v1kit, "v1_u"), (2, v2kit, "v2_u")):
        parts.append(_part_cover(n, course[n - 1][1]))
        for i, (u, _, _, _) in enumerate(kit.UNITS, 1):
            mod = importlib.import_module(f"{pre}{i}")
            add_css(getattr(mod, "CSS", ""))
            parts += [kit.cover(u), kit.roadmap(u)] + mod.slides() + [kit.nextup(u)]
    add_css(vibe3.CSS)
    p3 = vibe3.slides()
    p3[0] = p3[0].replace('<section class="slide dk cover-dk active" data-title="표지">', '<section id="p3" class="slide dk cover-dk" data-title="3부 하네스 엔지니어링">')
    k = 0
    for j, s in enumerate(p3):
        if 'class="slide dk divider"' in s and k < len(v3kit.AGENDA):
            p3[j] = s.replace("<section ", f'<section id="u-{v3kit.AGENDA[k][0]}" ', 1)
            k += 1
    parts += p3
    _write("index.html", _tpl(css), "바이브코딩 강의", parts)


if __name__ == "__main__":
    build()
