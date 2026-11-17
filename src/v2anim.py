"""2부 애니메이션 도구 — 상자 줄 사이를 데이터 칩이 이동하는 장면 (한 번 재생 후 마지막 장면에 멈춤).
lane(nodes, hops, results) · CSS 접두어 v2mv. 단원 모듈은 CSS 에 v2anim.CSS 를 더한다.
"""


def lane(nodes, hops, results=(), h=210):
    """nodes: [(제목, 한 줄)] · hops: [(출발 칸, 도착 칸, 칩 글자, 시작 초, 남김?)] · results: [(칸, 글자, "ok"|"no", 초)].
    칩은 출발 → 도착 1.1초 이동 · 남김=True 면 도착 칸 아래에 남는다. 도착하면 그 칸 테두리가 주황."""
    n = len(nodes)
    c = [(i + .5) / n * 100 for i in range(n)]
    lit = {}
    for a, b, _, d, _ in hops:
        lit[b] = min(lit.get(b, 99), d + 1.1)
        lit.setdefault(a, d)
        lit[a] = min(lit[a], d)
    nd = "".join(
        f'<div class="v2mvn" style="left:{c[i]:.2f}%; width:{100 / n - 3:.1f}%; --l:{lit.get(i, 99):.1f}s"><b>{t}</b><span>{s}</span></div>'
        for i, (t, s) in enumerate(nodes))
    hp = "".join(
        f'<div class="v2mvt{" keep" if keep else ""}" style="--a:{c[a]:.2f}%; --b:{c[b]:.2f}%; --d:{d:.1f}s">{lab}</div>'
        for a, b, lab, d, keep in hops)
    rs = "".join(
        f'<div class="v2mvr {k}" style="left:{c[i]:.2f}%; --d:{d:.1f}s">{"✓" if k == "ok" else "✕"} {t}</div>'
        for i, t, k, d in results)
    ar = "".join(f'<i class="v2mva" style="left:{(c[i] + c[i + 1]) / 2:.2f}%">→</i>' for i in range(n - 1))
    return f'<div class="v2mv" style="height:{h}px">{nd}{ar}{hp}{rs}</div>'


CSS = """
  /* 2부 · 데이터 이동 애니메이션 */
  .v2mv{position:relative; margin:10px 0 6px;}
  .v2mvn{position:absolute; top:0; transform:translateX(-50%); border:2px solid #D9DDE3; border-radius:14px; background:#fff;
         padding:14px 12px; text-align:center; animation:v2mvlit .4s ease-out var(--l) forwards;}
  .v2mvn b{display:block; font-size:20px; color:#16233A;} .v2mvn span{font-size:14.5px; color:#6B7785;}
  .v2mva{position:absolute; top:28px; transform:translateX(-50%); font-style:normal; color:#B8C0CB; font-size:22px; font-weight:800;}
  .v2mvt{position:absolute; top:96px; left:var(--a); transform:translateX(-50%); white-space:nowrap; padding:7px 13px; border-radius:20px;
         background:#1F3A5F; color:#fff; font-size:14.5px; font-weight:700; opacity:0; animation:v2mvhop 1.25s ease-in-out var(--d) forwards;}
  .v2mvt.keep{animation-name:v2mvhopk; background:#F28C28;}
  .v2mvr{position:absolute; top:146px; transform:translateX(-50%); white-space:nowrap; font-size:16px; font-weight:800; padding:6px 12px; border-radius:10px;
         opacity:0; animation:v2mvin .4s ease-out var(--d) forwards;}
  .v2mvr.ok{color:#1E7B45; background:#E6F4EC;} .v2mvr.no{color:#C0392B; background:#FBE9E7;}
  @keyframes v2mvlit{to{border-color:#F28C28; box-shadow:0 6px 16px rgba(242,140,40,.18)}}
  @keyframes v2mvhop{0%{left:var(--a); opacity:1} 88%{left:var(--b); opacity:1} 100%{left:var(--b); opacity:0}}
  @keyframes v2mvhopk{0%{left:var(--a); opacity:1} 88%{left:var(--b); opacity:1} 100%{left:var(--b); opacity:1}}
  @keyframes v2mvin{from{opacity:0; transform:translate(-50%,8px)} to{opacity:1; transform:translate(-50%,0)}}
  @media print{.v2mvt.keep, .v2mvr{opacity:1; animation:none} .v2mvt.keep{left:var(--b)} .v2mvt{animation:none}}
"""
