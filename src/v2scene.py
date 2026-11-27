"""2부 장면 애니메이션 — 칸은 제자리, 칸 안의 내용만 바뀐다(로딩 → 요청 줄 → 처리 → 응답 → 화면).
카드 · 칩이 칸 사이를 옮겨 다니는 방식은 쓰지 않는다. 칸 사이 선은 그 순간 그어지고 남는다.
CSS 접두어 v2s. 단원 모듈은 CSS 에 v2scene.CSS 를 더한다.
"""
from hx import esc

TASKS = [("주간 회의록", "2026-11-27", "작성 중"), ("교육 자료 정리", "2026-11-25", "초안"), ("예산안 메모", "2026-11-18", "작성 중")]
NEW = ("고객사 미팅 회의록", "2026-12-02", "초안")


def _at(d):
    return f'style="--d:{d:.1f}s"'


def wire(top, bottom, d_top, d_bot):
    """칸 사이 선 두 줄 — 위: 요청(→) · 아래: 응답(←). 정해진 때에 그어지고 글자가 켜짐."""
    return (f'<div class="v2sWr"><div class="ln rq" {_at(d_top)}><span>{top}</span><i></i></div>'
            f'<div class="ln rs" {_at(d_bot)}><i></i><span>{bottom}</span></div></div>')


def reqres(write=False):
    """요청과 응답 — 브라우저(화면 + Network) · 서버 · DB.
    읽기: 로딩 줄 → GET 요청 → 서버가 SQL → DB 행 3개 → JSON 응답 200 → 화면에 페이지 3개.
    쓰기: 「추가」 클릭 → POST 요청 → insert → DB 새 행 → 201 → 목록에 1건 추가."""
    T = [.3, 1.0, 1.8, 2.6, 3.3, 3.9, 4.5, 5.1, 5.8]
    # ── 브라우저 화면
    rows = "".join(f'<div class="rw" {_at(T[8] + i * .12)}><b>{t}</b><span>{d[5:].replace("-", "/")}</span><em>{s}</em></div>'
                   for i, (t, d, s) in enumerate(TASKS))
    if write:
        rows = "".join(f'<div class="rw on"><b>{t}</b><span>{d[5:].replace("-", "/")}</span><em>{s}</em></div>' for t, d, s in TASKS)
        rows += f'<div class="rw nw" {_at(T[8])}><b>{NEW[0]}</b><span>{NEW[1][5:].replace("-", "/")}</span><em>{NEW[2]}</em></div>'
        top = (f'<div class="add"><span class="in">{NEW[0]}</span><span class="bt" {_at(T[1] - .3)}>+ 새 페이지</span></div>')
        skel = ""
    else:
        top = ""
        skel = f'<div class="sk" {_at(T[8])}><i></i><i></i><i></i></div>'
    meth, path, code_, codet = ("POST", "/api/pages", "201", "Created") if write else ("GET", "/api/pages", "200", "OK")
    if write:
        js = '[{ "id": 44, "title": "고객사 미팅 회의록", … }]'
    else:
        js = ('[{ "id": 41, "title": "주간 회의록", … },\n'
              ' { "id": 42, "title": "교육 자료 정리", … },\n'
              ' { "id": 43, "title": "예산안 메모", … }]')
    net = (f'<div class="net"><div class="nh"><b>Network</b><span>Name</span><span>Method</span><span>Status</span></div>'
           f'<div class="nr" {_at(T[1])}><span class="fn">pages</span><span>{meth}</span>'
           f'<span class="st"><i class="pd" {_at(T[7])}>(pending)</i><b class="ok" {_at(T[7])}>{code_} {codet}</b></span></div>'
           f'<pre class="pv" {_at(T[7])}><em>Response</em>{esc(js)}</pre></div>')
    browser = (f'<div class="v2sBr"><div class="bar"><i></i><i></i><i></i><span>mini-notion.vercel.app</span></div>'
               f'<div class="app"><div class="ah">미니 노션 · 페이지 목록</div>{top}<div class="ls">{skel}{rows}</div></div>{net}</div>')
    # ── 서버
    if write:
        sl = [(f"POST {path}", T[2]), ("로그인 확인 → insert", T[2] + .3), ("새 행 → JSON", T[6])]
    else:
        sl = [(f"GET {path}", T[2]), ("pages 표 조회", T[2] + .3), ("행 3개 → JSON", T[6])]
    server = ('<div class="v2sBx srv"><div class="bh"><b>서버</b><small>Next.js · Vercel</small></div>'
              + "".join(f'<div class="cl" {_at(d)}>{esc(x)}</div>' for x, d in sl) + '</div>')
    # ── DB
    dr = "".join(f'<tr class="{"hl" if not write else ""}" {_at(T[3] + i * .15)}><td>{41 + i}</td><td>{t}</td></tr>' for i, (t, _, _) in enumerate(TASKS))
    if write:
        dr += f'<tr class="nw" {_at(T[3])}><td>44</td><td>{NEW[0]}</td></tr>'
    db = (f'<div class="v2sBx db"><div class="bh"><b>DB</b><small>Supabase · pages</small></div>'
          f'<table><tr><th>id</th><th>title</th></tr>{dr}</table></div>')
    req = "① 요청 · " + meth
    return ('<div class="v2s">' + browser
            + wire(req, f"⑤ 응답 · {code_} · JSON", T[1], T[6])
            + server
            + wire("② 조회 · SQL", "④ 행 · 결과", T[2] + .3, T[4])
            + db + '</div>')


def steps(items, d0=1.0, gap=None):
    """장면 아래 단계 줄 — 장면의 시점에 맞춰 한 칸씩 켜짐. items: [(번호 글자, 설명, 초)]."""
    c = "".join(f'<div class="s" {_at(d)}><b>{n}</b><span>{x}</span></div>' for n, x, d in items)
    return f'<div class="v2sSt">{c}</div>'


CSS = """
  /* 2부 · 장면 애니메이션 (v2s) — 칸은 제자리 · 내용만 바뀜 */
  .v2s{display:grid; grid-template-columns:470px 1fr 200px 1fr 210px; align-items:stretch; margin:0 0 12px;}
  .v2sBr{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 6px 18px rgba(22,35,58,.10);}
  .v2sBr .bar{display:flex; align-items:center; gap:6px; padding:7px 10px; background:#EEF1F5; border-bottom:1px solid #D9DDE3;}
  .v2sBr .bar i{width:9px; height:9px; border-radius:50%; background:#C9CFD8;}
  .v2sBr .bar span{margin-left:8px; flex:1; background:#fff; border-radius:12px; padding:3px 12px; font-family:var(--mono); font-size:13px; color:#3A4657;}
  .v2sBr .app{padding:8px 14px; min-height:120px;}
  .v2sBr .ah{font-size:17px; font-weight:800; color:#16233A; margin-bottom:6px;}
  .v2sBr .add{display:flex; gap:8px; margin-bottom:6px;}
  .v2sBr .add .in{flex:1; border:1.5px solid #C9CFD8; border-radius:8px; padding:4px 10px; font-size:14px; color:#16233A;}
  .v2sBr .add .bt{background:#1F3A5F; color:#fff; font-size:14px; font-weight:700; border-radius:8px; padding:4px 14px; animation:v2sPress .35s var(--d) both;}
  .v2sBr .ls{position:relative; display:flex; flex-direction:column; gap:5px;}
  .v2sBr .sk{position:absolute; inset:0; display:flex; flex-direction:column; gap:5px; animation:v2sOut .3s var(--d) forwards;}
  .v2sBr .sk i{display:block; height:25px; border-radius:6px; background:linear-gradient(90deg,#EEF1F5 0%,#F7F8FA 50%,#EEF1F5 100%); background-size:200% 100%;
    animation:v2sShim 1.1s linear infinite;}
  .v2sBr .rw{display:grid; grid-template-columns:1fr 60px 64px; align-items:center; height:25px; padding:0 10px; border-radius:6px; background:#F1F4F8;
    font-size:14px; opacity:0; animation:v2sIn .35s var(--d) forwards;}
  .v2sBr .rw.on{opacity:1; animation:none;}
  .v2sBr .rw.nw{animation:v2sNew 1.4s var(--d) forwards;}
  .v2sBr .rw b{font-weight:600; color:#16233A;} .v2sBr .rw span{font-family:var(--mono); font-size:13px; color:#3A4657;} .v2sBr .rw em{font-style:normal; font-size:12.5px; color:#6B7785;}
  .v2sBr .net{margin-top:auto; border-top:1.5px solid #D9DDE3; background:#FAFBFC; padding:6px 10px 8px; font-size:12.5px;}
  .v2sBr .nh,.v2sBr .nr{display:grid; grid-template-columns:70px 1fr 60px 110px; gap:6px; align-items:center;}
  .v2sBr .nh b{font-size:12.5px; color:#16233A;} .v2sBr .nh span{color:#6B7785;}
  .v2sBr .nr{margin-top:4px; padding:3px 0; border-top:1px solid #E3E7EC; opacity:0; animation:v2sIn .3s var(--d) forwards; font-family:var(--mono);}
  .v2sBr .nr .fn{grid-column:2; color:#1F3A5F;}
  .v2sBr .nr .st{position:relative; height:16px;}
  .v2sBr .nr .pd{position:absolute; left:0; font-style:normal; color:#9AA5B1; animation:v2sOut .2s var(--d) forwards;}
  .v2sBr .nr .ok{position:absolute; left:0; color:#1E7B45; opacity:0; animation:v2sIn .25s var(--d) forwards;}
  .v2sBr .pv{margin:5px 0 0; background:#fff; border:1px solid #E3E7EC; border-radius:6px; padding:5px 8px; font-family:var(--mono); font-size:11.5px; line-height:1.45;
    color:#1F3A5F; white-space:pre; opacity:0; animation:v2sIn .35s var(--d) forwards;}
  .v2sBr .pv em{display:block; font-style:normal; font-weight:800; color:#6B7785;}
  .v2sBx{border:2px solid #D9DDE3; border-radius:12px; background:#fff; padding:10px 12px; display:flex; flex-direction:column; gap:7px; align-self:center;}
  .v2sBx .bh b{font-size:19px; color:#16233A; margin-right:6px;} .v2sBx .bh small{display:block; font-size:12.5px; color:#6B7785;}
  .v2sBx .cl{font-family:var(--mono); font-size:12.5px; color:#1F3A5F; background:#F4F6F9; border-radius:6px; padding:5px 8px; opacity:.25;
    animation:v2sLit .35s var(--d) forwards;}
  .v2sBx.db table{border-collapse:collapse; width:100%; font-size:13px;}
  .v2sBx.db th{text-align:left; font-family:var(--mono); font-size:12px; color:#fff; background:#1F3A5F; padding:3px 6px;}
  .v2sBx.db td{border-bottom:1px solid #E3E7EC; padding:4px 6px; color:#16233A;}
  .v2sBx.db td:first-child{font-family:var(--mono); color:#6B7785;}
  .v2sBx.db tr.hl td{animation:v2sRow 1.6s var(--d) forwards;}
  .v2sBx.db tr.nw{opacity:0; animation:v2sIn .3s var(--d) forwards;} .v2sBx.db tr.nw td{background:#FFF3E0; font-weight:700;}
  .v2sWr{display:flex; flex-direction:column; justify-content:center; gap:44px; padding:0 4px;}
  .v2sWr .ln{position:relative; height:30px;}
  .v2sWr .ln i{position:absolute; left:0; right:0; bottom:0; height:3px; background:#F28C28; transform:scaleX(0); animation:v2sDraw .45s var(--d) forwards;}
  .v2sWr .ln.rq i{transform-origin:left;} .v2sWr .ln.rs i{transform-origin:right; background:#1F3A5F;}
  .v2sWr .ln.rq i::after{content:""; position:absolute; right:-2px; top:-5px; border:6px solid transparent; border-left:9px solid #F28C28;}
  .v2sWr .ln.rs i::after{content:""; position:absolute; left:-2px; top:-5px; border:6px solid transparent; border-right:9px solid #1F3A5F;}
  .v2sWr .ln span{position:absolute; left:0; right:0; top:0; text-align:center; font-size:13px; font-weight:800; white-space:nowrap; opacity:0;
    animation:v2sIn .3s var(--d) forwards;}
  .v2sWr .ln.rq span{color:#E07A12;} .v2sWr .ln.rs span{color:#1F3A5F;}
  .v2sSt{display:grid; grid-template-columns:repeat(5,1fr); gap:8px; margin:0 0 10px;}
  .v2sSt .s{border-top:3px solid #D9DDE3; padding:6px 4px 0; opacity:.3; animation:v2sStep .4s var(--d) forwards;}
  .v2sSt .s b{font-size:15px; color:#16233A; margin-right:6px;} .v2sSt .s span{font-size:14px; color:#3A4657;}
  @keyframes v2sIn{from{opacity:0} to{opacity:1}}
  @keyframes v2sOut{to{opacity:0; visibility:hidden}}
  @keyframes v2sLit{to{opacity:1; background:#FFF3E0; color:#16233A}}
  @keyframes v2sStep{to{opacity:1; border-top-color:#F28C28}}
  @keyframes v2sDraw{to{transform:scaleX(1)}}
  @keyframes v2sShim{from{background-position:200% 0} to{background-position:-200% 0}}
  @keyframes v2sRow{0%{background:transparent} 25%{background:#FFE3C4} 100%{background:#FFF3E0}}
  @keyframes v2sNew{0%{opacity:0; background:#FFE3C4} 30%{opacity:1; background:#FFE3C4} 100%{opacity:1; background:#FFF3E0; box-shadow:inset 4px 0 0 #F28C28}}
  @keyframes v2sPress{0%,60%{transform:none} 80%{transform:scale(.92); background:#F28C28} 100%{transform:none}}
  @media print{.v2sBr .rw,.v2sBr .nr,.v2sBr .pv,.v2sBr .nr .ok,.v2sWr .ln span,.v2sBx.db tr.nw{opacity:1; animation:none}
    .v2sBr .sk,.v2sBr .nr .pd{display:none} .v2sWr .ln i{transform:none; animation:none} .v2sBx .cl,.v2sSt .s{opacity:1; animation:none}}
"""


# ── AI 대화 장면 — 대화창(호스트) · 가운데 칸(MCP 서버) · 오른쪽 칸(DB · 페이지 목록). 칸은 제자리 · 줄이 차례로 켜짐 ──
def agent(host, msgs, mid, right, wires, host_cls="o"):
    """host: 대화창 이름 · msgs: [(cls me|ai|tool|ok, html, 초)] · mid: (제목, 작은 글, [(줄, 초)]) · right: html
    wires: ((위 글자, 초), (아래 글자, 초), (위2, 초), (아래2, 초))."""
    m = "".join(f'<div class="m {c}" {_at(d)}>{h}</div>' for c, h, d in msgs)
    chat = f'<div class="v2sAg"><div class="hd"><i class="{host_cls}"></i>{host}</div><div class="ms">{m}</div></div>'
    mt, ms, ml = mid
    midb = (f'<div class="v2sBx srv"><div class="bh"><b>{mt}</b><small>{ms}</small></div>'
            + (ml if isinstance(ml, str) else "".join(f'<div class="cl" {_at(d)}>{esc(x)}</div>' for x, d in ml)) + '</div>')
    (a, da), (b, db_), (c, dc), (e, de) = wires
    return ('<div class="v2s v2sA">' + chat + wire(a, b, da, db_) + midb + wire(c, e, dc, de) + right + '</div>')


def board(rows, title="미니 노션 · pages"):
    """rows: [(제목, 날짜, 상태, 새 행이면 초 · 아니면 None)]."""
    tr = "".join(f'<tr class="{"nw" if d is not None else ""}" {_at(d or 0)}><td>{t}</td><td>{du}</td><td>{st}</td></tr>' for t, du, st, d in rows)
    return (f'<div class="v2sBx db bd"><div class="bh"><b>{title.split(" · ")[0]}</b><small>{" · ".join(title.split(" · ")[1:])}</small></div>'
            f'<table><tr><th>페이지</th><th>날짜</th><th>상태</th></tr>{tr}</table></div>')


def tools(names, pick, d_list, d_pick):
    """MCP 서버의 도구 목록 — d_list 에 전부 켜지고(목록 읽기), d_pick 에 하나만 주황(고른 도구)."""
    r = "".join(f'<div class="tl{" pk" if n == pick else ""}" style="--d:{d_list:.1f}s; --p:{d_pick:.1f}s"><b>{n}</b><span>{x}</span></div>' for n, x in names)
    return r


CSS += """
  /* 2부 · AI 대화 장면 (v2sA) */
  .v2sA{grid-template-columns:400px 1fr 250px 1fr 290px;}
  .v2sAg{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 6px 18px rgba(22,35,58,.10);}
  .v2sAg .hd{display:flex; align-items:center; gap:8px; padding:9px 12px; background:#F6F8FA; border-bottom:1px solid #D9DDE3; font-size:16px; font-weight:800; color:#16233A;}
  .v2sAg .hd i{width:12px; height:12px; border-radius:3px; background:#D97757;} .v2sAg .hd i.g{background:#10A37F;} .v2sAg .hd i.b{background:#1A73E8;}
  .v2sAg .ms{padding:10px 12px; display:flex; flex-direction:column; gap:7px;}
  .v2sAg .m{font-size:14.5px; border-radius:10px; padding:6px 10px; opacity:0; animation:v2sIn .3s var(--d) forwards; line-height:1.4;}
  .v2sAg .m.me{align-self:flex-end; background:#FFF1E0; color:#16233A; font-weight:600; max-width:90%;}
  .v2sAg .m.ai{background:#EEF3FA; border:1px solid #C9D6E6; color:#16233A;}
  .v2sAg .m.tool{font-family:var(--mono); font-size:12.5px; color:#3A4657; background:#F4F6F9; border:1px dashed #9AA5B1;}
  .v2sAg .m.tool em{font-style:normal; font-weight:800; color:#E07A12; margin-right:6px;}
  .v2sAg .m.ok{align-self:flex-start; font-size:13px; font-weight:700; color:#1E7B45; background:#E6F4EC;}
  .v2sBx.srv .tl{border:1.5px solid #E3E7EC; border-radius:8px; padding:4px 8px; opacity:.3; animation:v2sIn2 .3s var(--d) forwards;}
  .v2sBx.srv .tl b{display:block; font-family:var(--mono); font-size:12.5px; color:#1F3A5F;} .v2sBx.srv .tl span{font-size:12px; color:#3A4657;}
  .v2sBx.srv .tl.pk{animation:v2sIn2 .3s var(--d) forwards, v2sPick .4s var(--p) forwards;}
  .v2sBx.bd td{font-size:13px;} .v2sBx.bd td:first-child{font-family:inherit; color:#16233A;}
  @keyframes v2sIn2{to{opacity:1}}
  @keyframes v2sPick{to{border-color:#F28C28; background:#FFF3E0}}
  @media print{.v2sAg .m{opacity:1; animation:none} .v2sBx.srv .tl{opacity:1; animation:none}}
"""
