#!/usr/bin/env python3
"""바이브코딩 온라인 강의 덱을 만든다 → docs/

사용: python3 src/build.py [part1 | part3]
  1부 — 단원마다 한 파일  docs/1-1-vibe-coding.html …  (P1_ONLY=3,6 으로 일부만)
  3부 — 단원마다 한 파일  docs/3-1-harness.html …  + 합본 docs/3-all.html
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

P3_SLUG = ["harness", "agent-design", "mcp", "claude-md", "skill", "guardrails", "verify", "operate"]


def _tpl(css):
    return (ROOT / "src" / "template.html").read_text().replace("</style>", css + "</style>", 1)


def _write(name, tpl, title, parts):
    out = ROOT / "docs" / name
    out.write_text(tpl.replace("{{DECK_TITLE}}", title).replace("{{SLIDES}}", "\n\n".join(parts)))
    print(name, len(parts) - 1, "장")


def build_part1():
    import v1kit
    import v3kit
    only = [x for x in os.environ.get("P1_ONLY", "").split(",") if x]
    for i, (u, title, _, _) in enumerate(v1kit.UNITS, 1):
        if only and str(i) not in only:
            continue
        mod = importlib.import_module(f"v1_u{i}")
        tpl = _tpl(BASE_CSS + v3kit.CSS + v1kit.CSS + getattr(mod, "CSS", ""))
        parts = [art.DEFS, v1kit.cover(u), v1kit.roadmap(u)] + mod.slides() + [v1kit.nextup(u)]
        _write(v1kit.file_of(u), tpl, f"{u} {title}", parts)


def build_part3():
    import v3kit
    import vibe3
    tpl = _tpl(BASE_CSS + vibe3.CSS)
    _write("3-all.html", tpl, "3부 하네스 엔지니어링 · 내 업무 에이전트", [art.DEFS] + vibe3.slides())
    for i, (c, t, _) in enumerate(v3kit.AGENDA, 1):
        mod = importlib.import_module(f"v3_c{i}")
        cov = v3kit.cover().replace("바이브코딩 · 3", f"바이브코딩 · {c}").replace("하네스 엔지니어링<br/>· 내 업무 에이전트", t)
        _write(f"{c}-{P3_SLUG[i - 1]}.html", tpl, f"{c} {t}", [art.DEFS, cov] + mod.slides())


if __name__ == "__main__":
    arg = sys.argv[1:]
    if arg in ([], ["part1"]):
        build_part1()
    if arg in ([], ["part3"]):
        build_part3()
