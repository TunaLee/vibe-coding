"""강사 대본 HTML — scripts/1-*.md 를 따로 보는 한 페이지(docs/part1-script.html)로 만든다.

대본 원본은 그대로 scripts/*.md 에서 고치고, build.py 가 덱과 함께 다시 만든다.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _inline(t):
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)


def _unit(path):
    lines = path.read_text().splitlines()
    title = lines[0].lstrip("# ").replace(" · 강사 대본", "") if lines else path.stem
    secs, cur = [], None
    for ln in lines[1:]:
        m = re.match(r"^## (\d+) · (.*)$", ln)
        if m:
            cur = {"no": m.group(1), "title": m.group(2), "body": []}
            secs.append(cur)
        elif cur is not None and ln.strip():
            cur["body"].append(ln)
    return path.stem, title, secs


def _body(lines):
    out = []
    for ln in lines:
        if ln.startswith(">"):
            t = ln.lstrip("> ").strip()
            k, _, rest = t.partition(" — ")
            if rest:
                out.append(f'<aside><span>{_inline(k)}</span>{_inline(rest)}</aside>')
            else:
                out.append(f"<aside>{_inline(t)}</aside>")
        else:
            out.append(f"<p>{_inline(ln)}</p>")
    return "".join(out)


CSS = """
:root{--ink:#16233A; --sub:#6B7785; --line:#E3E7EC; --bg:#F6F7F9; --card:#fff; --acc:#F28C28; --q:#FFF6EC;}
@media (prefers-color-scheme: dark){:root{--ink:#E8ECF1; --sub:#9AA6B5; --line:#2A3443; --bg:#0F1620; --card:#17202C; --q:#2A2116;}}
*{box-sizing:border-box;} html{scroll-behavior:smooth; scroll-padding-top:70px;}
body{margin:0; background:var(--bg); color:var(--ink); font-family:"Pretendard",-apple-system,"Apple SD Gothic Neo",sans-serif; line-height:1.8;}
header{position:sticky; top:0; z-index:5; display:flex; gap:14px; align-items:center; padding:12px 24px; background:var(--card); border-bottom:1px solid var(--line);}
header h1{margin:0; font-size:18px; white-space:nowrap;} header a{color:var(--sub); font-size:14px; text-decoration:none; white-space:nowrap;}
header input{flex:1; max-width:340px; margin-left:auto; padding:7px 12px; border:1px solid var(--line); border-radius:8px; background:var(--bg); color:var(--ink); font-size:15px;}
.wrap{display:grid; grid-template-columns:260px minmax(0,1fr); max-width:1200px; margin:0 auto;}
nav{position:sticky; top:58px; align-self:start; max-height:calc(100vh - 58px); overflow:auto; padding:20px 16px; font-size:14px;}
nav details{margin-bottom:6px;} nav summary{cursor:pointer; font-weight:800; padding:4px 0;}
nav a{display:block; color:var(--sub); text-decoration:none; padding:2px 0 2px 12px; line-height:1.5;} nav a:hover{color:var(--acc);}
main{padding:20px 28px 120px;}
h2{margin:40px 0 14px; font-size:26px; padding-bottom:8px; border-bottom:3px solid var(--acc);}
h2 a{font-size:14px; font-weight:400; color:var(--sub); margin-left:12px;}
section{background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px 22px; margin:12px 0;}
section h3{margin:0 0 6px; font-size:18px;} section h3 em{font-style:normal; color:var(--acc); margin-right:10px; font-variant-numeric:tabular-nums;}
section p{margin:6px 0; font-size:17px;}
aside{margin:10px 0 4px; padding:10px 14px; border-left:4px solid var(--acc); background:var(--q); border-radius:6px; font-size:15.5px;}
aside span{display:block; font-size:13px; font-weight:800; color:var(--acc);}
code{font-family:ui-monospace,Menlo,monospace; font-size:.9em; background:var(--bg); padding:1px 5px; border-radius:4px;}
mark{background:#FFE08A; color:#16233A;}
.hide{display:none;}
@media (max-width:820px){.wrap{grid-template-columns:1fr;} nav{display:none;} main{padding:12px 16px 80px;} header{padding:10px 16px;} header a{display:none;}}
@media print{header,nav{display:none;} .wrap{display:block;} section{break-inside:avoid; border:0; padding:6px 0;}}
"""

JS = """
const q=document.getElementById('q');
q.addEventListener('input',()=>{const v=q.value.trim();
  document.querySelectorAll('main section').forEach(s=>{s.classList.toggle('hide',!!v && !s.textContent.includes(v));});});
"""


def build(part=1):
    units = [_unit(p) for p in sorted((ROOT / "scripts").glob(f"{part}-*.md"))]
    nav, main = [], []
    for stem, title, secs in units:
        links = "".join(f'<a href="#s{s["no"]}">{s["no"]} · {html.escape(s["title"])}</a>' for s in secs)
        nav.append(f'<details><summary>{html.escape(title)}</summary>{links}</details>')
        main.append(f'<h2 id="u{stem}">{html.escape(title)}<a href="part{part}.html#u-{stem}">덱에서 보기</a></h2>')
        main += [f'<section id="s{s["no"]}"><h3><em>{s["no"]}</em>{html.escape(s["title"])}</h3>{_body(s["body"])}</section>'
                 for s in secs]
    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><title>{part}부 강사 대본</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css"/>
<style>{CSS}</style></head><body>
<header><h1>{part}부 강사 대본</h1><a href="part{part}.html">덱 열기</a><input id="q" placeholder="대본 검색"/></header>
<div class="wrap"><nav>{"".join(nav)}</nav><main>{"".join(main)}</main></div>
<script>{JS}</script></body></html>"""
    (ROOT / "docs" / f"part{part}-script.html").write_text(page)


if __name__ == "__main__":
    build()
