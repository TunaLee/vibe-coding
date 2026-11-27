"""1-6 바이브코딩 실습 (40분).

웹의 3요소 → 브라우저로 열기 → 권한 모드 → 개발계획.md(1-4)의 태스크 단위 진행 → 수정 · 되돌리기 → 실습.
공통 예제: labs/mini_notion/예시 (완성본 app/). 태스크 번호 · 이름은 사람마다 달라 장에 박지 않는다. Git 개념은 1-5 에서 · 여기서는 「커밋해 줘 · 되돌려 줘」로만.
사실 출처: code.claude.com/docs/en/permission-modes · code.claude.com/docs/en/checkpointing
"""
import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note, table
from stats_hx import src
from v1kit import brief, chat, shot, labcard, tstep
from v3kit import phmap

T = "1-6"



FILES = [("index.html", "34줄", "뼈대", "화면에 어떤 칸이 있나", "집 · 골조",
          [("aside", "왼쪽 · 페이지 목록"), ("main", "오른쪽 · 편집 화면"), ("#slash", "「/」 메뉴")]),
         ("style.css", "45줄", "모양", "칸이 어떻게 보이나", "집 · 인테리어",
          [("aside", "폭 240px · 연회색 바탕"), ("h1", "제목 글씨 34px"), (".handle", "손잡이 · 마우스 올릴 때만")]),
         ("app.js", "150줄", "동작 · 저장", "누르면 무슨 일이 생기나", "집 · 전기 · 배관",
          [("renderPages", "F1 · 목록 그리기"), ("slashCheck", "F3 · 「/」 보이면 메뉴"),
           ("dragSetup", "F4 · 끌어 옮기기"), ("save", "F5 · 브라우저에 저장")])]


def _web3():
    """웹의 3요소 — 같은 미니 노션 화면이 HTML만 → + CSS → + JS 로 바뀜. JS 칸에서 「+ 새 페이지」를 누르면 목록에 「제목 없음」이 생김.
    코드 조각은 예시 앱(labs/mini_notion/예시/app) 의 실제 줄을 줄여 옮김. 평택대 덱 p3._web3 구조."""
    raw = ('<div class="v16wR"><p>미니 노션</p><ul><li>시작하기</li><li>주간 회의록</li></ul><button>+ 새 페이지</button>'
           '<h1>시작하기</h1><p>「/」 를 입력하면 블록 종류를 고를 수 있다</p></div>')

    def page(js):
        new = '<li class="nw">제목 없음</li>' if js else ""
        on0 = ' class="on0"' if js else ' class="on"'
        btn = '<b class="bt">+ 새 페이지</b>'
        g = " g" if js else ""
        return (f'<div class="v16wS"><div class="sd"><i>미니 노션</i><ul><li{on0}>시작하기</li><li>주간 회의록</li>{new}</ul>{btn}</div>'
                f'<div class="mn"><h1>{"<span class=t0>시작하기</span><span class=t1>제목 없음</span>" if js else "시작하기"}</h1>'
                f'<div class="bk{g}"><u></u>보고서 초안</div><div class="bk{g}">회의 메모</div></div></div>')
    code_h = """<aside>
  <ul id="pages"></ul>
  <button id="newPage">
    + 새 페이지</button>
</aside>
<main><h1 id="title"></h1></main>"""
    code_c = """body { display: grid;
  grid-template-columns: 240px 1fr; }
aside { background: #f7f7f5; }
h1 { font-size: 34px; }"""
    code_j = """newPage.onclick = () => {
  state.pages.push(새 페이지);
  save();     // 브라우저에 저장
  render();   // 목록 다시 그리기
};"""
    cols = [("HTML만", "뼈대 · 내용", "index.html", raw, code_h), ("+ CSS", "모양 · 배치 · 색", "style.css", page(False), code_c),
            ("+ JS", "누르면 동작 · 저장", "app.js", page(True), code_j)]
    return '<div class="v16w">' + "".join(
        f'<div class="v16wc{" on" if i == 2 else ""}" style="--d:{.3 + i * 2:.1f}s"><div class="v16wh"><b>{h}</b><span>{sub}</span></div>'
        f'<div class="v16wb"><div class="br"><i></i><i></i><i></i><span>미니 노션</span></div>{pg}</div>'
        f'<pre class="v16wk"><em>{f}</em>\n{esc(code)}</pre></div>'
        for i, (h, sub, f, pg, code) in enumerate(cols)) + "</div>"


def _page():
    """미니 노션 첫 화면 (웹의 3요소 + CSS 칸과 같은 모양)."""
    return ('<div class="v16wS"><div class="sd"><i>미니 노션</i><ul><li class="on">시작하기</li><li>주간 회의록</li></ul>'
            '<b class="bt">+ 새 페이지</b></div><div class="mn"><h1>시작하기</h1>'
            '<div class="bk"><u></u>보고서 초안</div><div class="bk">회의 메모</div></div></div>')


def _bw(addr):
    return (f'<div class="v16wb"><div class="br"><i></i><i></i><i></i><span class="ad">{addr}</span></div>'
            f'<div class="pg">{_page()}</div><div class="emp">여는 중…</div></div>')


def _open():
    """브라우저로 열기 — 서버 없이 index.html 을 더블클릭 → 브라우저가 폴더의 파일 세 개를 직접 읽어 화면을 그림. 한 번 재생 후 정지."""
    return ('<div class="v16s"><div class="pc"><span class="pcl">내 컴퓨터</span>'
            '<div class="fd"><b>미니 노션 폴더</b><i class="f1">index.html</i><i class="f2">style.css</i><i class="f3">app.js</i></div>'
            '<div class="ln"><span class="lb">① index.html 더블클릭</span><div class="ar rt"></div><em class="tk"><u>html</u><u>css</u><u>js</u></em>'
            '<span class="lb">② 브라우저가 파일 세 개를 읽음</span></div>'
            f'<div class="bwW"><span class="bwl">브라우저</span>{_bw("file:///…/mini-notion/index.html")}<span class="lb4">③ 화면을 그림</span></div>'
            '</div>'
            '<div class="lg"><p><b>열기</b>index.html 더블클릭</p><p><b>고친 뒤</b>새로고침 · macOS ⌘R · Windows F5</p>'
            '<p><b>주소</b>file:// 로 시작 · 내 컴퓨터에서만 열림</p></div></div>')

def _node():
    """Node.js — 크롬 안의 V8 엔진(JS 실행기)이 브라우저 밖 「내 컴퓨터」로 옮겨 감 → 파일 · 서버 · 로그인 처리가 열림. 한 번 재생 후 정지."""
    return ('<div class="v16n"><div class="row">'
            '<div class="bx br"><span class="cap">브라우저 · Chrome</span><div class="pg">웹 화면</div>'
            '<div class="en"><b>V8 엔진</b><span>JS 실행기</span></div><small>JS 는 원래 여기서만 실행</small></div>'
            '<div class="mid"><span>2009 · Node.js</span><i></i><span>브라우저 밖 실행</span></div>'
            '<div class="bx pc"><span class="cap">내 컴퓨터 · 서버</span>'
            '<div class="en mv"><b>Node.js</b><span>V8 + 컴퓨터 기능</span></div>'
            '<ul><li style="--d:3.0s">파일 읽기 · 쓰기</li><li style="--d:3.4s">서버 열기 · localhost:3000</li>'
            '<li style="--d:3.8s">로그인 · 비밀번호 확인</li></ul></div></div>'
            '<div class="lg"><p><b>V8</b>크롬의 JS 엔진</p><p><b>Node.js</b>V8 을 브라우저 밖에서 실행</p>'
            '<p><b>열린 일</b>JS 로 서버까지 작성</p></div></div>')


def _bug():
    """버그 알리기 예 — 왼쪽: 「/」 를 쳐도 메뉴가 안 뜨는 화면 + 브라우저 콘솔의 빨간 오류 줄.
    오른쪽: Claude Code 입력창에 실제로 적는 버그 보고(① 순서 ② 기대 ③ 실제 ④ 오류 원문 + 캡처)가 한 줄씩 채워짐."""
    rows = [("① 순서", "새 페이지 → 빈 블록 클릭 → 「/」 입력"),
            ("② 기대", "블록 종류 메뉴가 열림"),
            ("③ 실제", "아무 반응 없음 · 새로고침해도 같음"),
            ("④ 오류 원문", "Uncaught TypeError: Cannot read properties of null (reading 'classList') at app.js:87"),
            ("⑤ 캡처", "[화면 캡처 붙임]")]
    r = "".join(f'<li class="k{i}" style="--d:{1.6 + i * .6:.1f}s"><b>{h}</b><span>{esc(t)}</span></li>' for i, (h, t) in enumerate(rows))
    return ('<div class="v16b"><div class="bad"><s>「「/」 메뉴가 안 돼요」</s><span>어디서 · 무엇을 했는지 없음 → AI 가 짐작으로 고침</span></div>'
            '<div class="row"><div class="lt">'
            '<div class="bw"><div class="bar"><i></i><i></i><i></i><span>미니 노션</span></div>'
            '<div class="pg"><h4>주간 회의</h4><p>보고서 초안</p><p class="cur">/<u></u></p><div class="no">메뉴가 안 열림</div></div>'
            '<div class="con"><em>Console</em><p>Uncaught TypeError: Cannot read properties of null (reading \'classList\')<small>app.js:87</small></p></div></div>'
            '<div class="tip"><b>오류 원문 찾기</b>Chrome F12 · macOS ⌥⌘J → Console 의 빨간 줄 복사</div></div>'
            '<div class="in"><div class="ih">Claude Code 입력창 · 예</div><p class="h">빈 블록에 「/」 를 입력해도 메뉴가 안 떠.</p>'
            f'<ul>{r}</ul></div></div></div>')


def _next():
    """웹 구조 — 클라이언트(브라우저) ↔ 웹 서버(Next.js · Node.js) ↔ DB. 미니 노션 로그인 한 번을 7단계로 따라감.
    ① 화면 요청 ② HTML · CSS · JS ③ 이메일 · 비밀번호 ④ 서버 → DB 사용자 찾기 ⑤ DB → 서버 ⑥ 비밀번호 비교 ⑦ 통과 · 페이지 목록.
    Next.js 괄호는 화면 코드 + 서버 코드(클라이언트 · 서버 칸)만 묶고, DB 는 밖(2부 Supabase). 한 번 재생 후 정지."""
    D = [.6 + 1.3 * k for k in range(7)]
    tok = [("a r", "① 화면 요청"), ("a l", "② HTML · CSS · JS"), ("a r", "③ 이메일 · 비밀번호"),
           ("b r", "④ kim@… 찾기"), ("b l", "⑤ 사용자 · 페이지 목록"), None, ("a l", "⑦ 통과 · 페이지 목록")]
    lane = {"a": "", "b": ""}
    for k, t in enumerate(tok):
        if t:
            ln, d = t[0].split()
            lane[ln] += f'<span class="xk {d}" style="--d:{D[k]:.1f}s">{t[1]}</span>'
    steps = ["화면 요청", "화면 받음", "로그인 정보 보냄", "DB 에 사용자 찾기", "DB 가 돌려줌", "비밀번호 비교", "통과 · 내 페이지"]
    log = "".join(f'<li style="--d:{D[k]:.1f}s"><em>{"①②③④⑤⑥⑦"[k]}</em>{x}</li>' for k, x in enumerate(steps))

    def lanes(k):
        return (f'<div class="ln"><div class="tr"><i class="r"></i><small>요청</small></div>'
                f'<div class="tr"><i class="l"></i><small>응답</small></div>{lane[k]}</div>')
    return ('<div class="v16x"><div class="nx"><span>Next.js 프로젝트 하나 · 화면 코드 + 서버 코드</span></div>'
            '<div class="row">'
            '<div class="bx cl"><span class="cap">클라이언트 · 브라우저</span>'
            '<div class="bar"><i></i><i></i><i></i><span>localhost:3000/login</span></div>'
            '<div class="scr"><div class="ly l0">여는 중…</div>'
            '<div class="ly l1" style="--d:3.0s"><p>이메일 <u>kim@posco.com</u></p><p>비밀번호 <u>••••••</u></p><em>로그인</em></div>'
            '<div class="ly l2" style="--d:9.0s"><b>내 페이지</b><p>주간 회의</p><p>보고서 초안</p></div></div>'
            '<small class="ft">app/login/page.tsx 가 그린 화면</small></div>'
            + lanes("a") +
            '<div class="bx sv"><span class="cap">웹 서버 · Next.js</span><small class="on">Node.js 위에서 실행</small>'
            '<div class="f f1" style="--d:1.9s"><b>app/login/page.tsx</b><span>화면 · 브라우저로 보냄</span></div>'
            '<div class="f f2" style="--d:4.2s"><b>app/api/login/route.ts</b><span>로그인 처리 · 서버에만 있음</span></div>'
            '<div class="ok" style="--d:7.1s">⑥ 비밀번호 비교 → 통과</div></div>'
            + lanes("b") +
            '<div class="bx db"><span class="cap">DB</span><div class="cy"><i></i>'
            '<p class="t" style="--d:5.4s"><b>users</b>kim@posco.com · 비밀번호</p>'
            '<p class="t" style="--d:5.4s"><b>pages</b>주간 회의 · 보고서 초안</p></div><small class="ft">2부 · Supabase</small></div>'
            f'</div><ol class="lg2">{log}</ol>'
            '<div class="lg"><p><b>클라이언트</b>화면 · 요청 보냄</p><p><b>웹 서버</b>요청 처리 · 응답</p><p><b>DB</b>데이터 저장 · 찾기</p></div></div>')

def _code():
    """화면 뒤의 코드 — 개발계획.md → 파일 세 개(뼈대 · 모양 · 동작)가 차례로 · 마지막에 데이터 모양. 예시 앱 실제 이름 · 줄 수."""
    cols = ""
    for i, (f, n, role, q, house, rows) in enumerate(FILES):
        d = .8 + i * 1.6
        r = "".join(f'<li style="--d:{d + .4 + j * .25:.2f}s"><code>{esc(c)}</code><span>{x}</span></li>' for j, (c, x) in enumerate(rows))
        cols += (f'<div class="v16c c{i}" style="--d:{d:.1f}s"><div class="hd"><b>{f}</b><small>{n}</small></div>'
                 f'<div class="rl"><strong>{role}</strong><span>{q}</span></div><ul>{r}</ul><div class="hs">{house}</div></div>')
    data = ('<div class="v16d" style="--d:6.0s"><div class="lb">데이터<small>개발계획 3칸 → app.js 가 기억</small></div>'
            '<div class="pg"><b>페이지</b><span class="k">제목 · 주간 회의</span><span class="k">블록들</span>'
            '<span class="bk"><i>종류 · 제목</i>주간 회의</span><span class="bk"><i>종류 · 체크 상자</i>보고서 초안 · 체크 안 함</span>'
            '<span class="bk"><i>종류 · 구분선</i></span></div><div class="ls">→ localStorage</div></div>')
    return ('<div class="v16top" style="--d:.2s"><span>개발계획.md</span><i>→</i><span class="cc">Claude Code</span><i>→</i>'
            '<span>파일 세 개 · labs/mini_notion/예시/app</span></div>'
            f'<div class="v16cs">{cols}</div>{data}')


CSS = """
  /* 1-6 · Node.js (v16n) */
  .v16n .row{display:grid; grid-template-columns:400px 1fr 400px; align-items:center; gap:0;}
  .v16n .bx{position:relative; border:2px solid #D9DDE3; border-radius:16px; padding:40px 22px 20px; min-height:310px; background:#fff; display:flex; flex-direction:column; gap:12px;}
  .v16n .pc{border:2px dashed #F28C28; background:rgba(242,140,40,.05);}
  .v16n .cap{position:absolute; top:-14px; left:18px; background:#16233A; color:#fff; font-size:15px; font-weight:800; padding:4px 12px; border-radius:8px;}
  .v16n .pc .cap{background:#F28C28;}
  .v16n .pg{height:80px; border-radius:10px; background:#F4F6F8; display:flex; align-items:center; justify-content:center; color:#6B7785; font-size:17px;}
  .v16n .en{border-radius:12px; background:#16233A; color:#fff; padding:14px 18px; display:flex; align-items:baseline; gap:12px;}
  .v16n .en b{font-size:23px;} .v16n .en span{font-size:15px; color:#C9D2DE;}
  .v16n .br small{font-size:15px; color:#6B7785;}
  .v16n .mv{background:#F28C28; opacity:0; transform:translateX(-560px); animation:v16nMv 1.4s 1.2s cubic-bezier(.5,0,.3,1) forwards;}
  .v16n .mv span{color:#fff;}
  @keyframes v16nMv{0%{opacity:.6; transform:translateX(-560px)} 100%{opacity:1; transform:none}}
  .v16n ul{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .v16n li{font-size:18px; color:#16233A; padding:9px 14px; border-radius:9px; background:#fff; border:1px solid #F3C99B; opacity:0; animation:v16wIn .4s var(--d) forwards;}
  .v16n .mid{display:flex; flex-direction:column; align-items:center; gap:8px; font-size:15px; color:#6B7785; opacity:0; animation:v16wIn .4s .6s forwards;}
  .v16n .mid span:first-child{font-weight:800; color:#F28C28; font-size:17px;}
  .v16n .mid i{display:block; width:120px; height:3px; background:#F28C28; position:relative;}
  .v16n .mid i:after{content:""; position:absolute; right:-2px; top:-6px; border:7.5px solid transparent; border-left:11px solid #F28C28;}
  .v16n .lg,.v16x .lg{display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:24px; opacity:0; animation:v16wIn .5s 4.4s forwards;}
  .v16n .lg p,.v16x .lg p{margin:0; font-size:18px; color:#37414F; padding:13px 18px; border-radius:10px; background:#F4F6F8;}
  .v16n .lg b,.v16x .lg b{color:#16233A; margin-right:10px; font-size:19px;}
  /* 1-6 · 버그 알리기 (v16b) */
  .v16b .bad{display:flex; align-items:center; gap:16px; margin-bottom:16px; font-size:17px; color:#6B7785;}
  .v16b .bad s{font-size:19px; color:#B4232A; background:#FDECEC; padding:5px 12px; border-radius:8px;}
  .v16b .row{display:grid; grid-template-columns:470px 1fr; gap:24px; align-items:start;}
  .v16b .bw{border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#fff;}
  .v16b .bar{display:flex; align-items:center; gap:5px; padding:6px 10px; background:#E9ECF0;}
  .v16b .bar i{width:9px; height:9px; border-radius:50%; background:#C3C9D1;} .v16b .bar span{margin-left:8px; font-size:13px; color:#37414F;}
  .v16b .pg{position:relative; padding:14px 22px 16px; min-height:150px;}
  .v16b .pg h4{margin:0 0 8px; font-size:22px; color:#16233A;} .v16b .pg p{margin:4px 0; font-size:16px; color:#37414F;}
  .v16b .cur{display:flex; align-items:center;} .v16b .cur u{display:inline-block; width:2px; height:18px; background:#16233A; margin-left:2px; animation:v16bBl 1s steps(1) infinite;}
  @keyframes v16bBl{50%{opacity:0}}
  .v16b .no{position:absolute; left:60px; top:96px; border:2px dashed #B4232A; color:#B4232A; font-size:14px; font-weight:800; padding:6px 12px; border-radius:8px; opacity:0; animation:v16wIn .4s .6s forwards;}
  .v16b .con{background:#1E1E1E; padding:8px 14px 10px; opacity:0; animation:v16wIn .4s 1s forwards;}
  .v16b .con em{font-style:normal; font-size:12px; color:#9AA6B5;}
  .v16b .con p{margin:4px 0 0; font-family:ui-monospace,Menlo,monospace; font-size:12.5px; line-height:1.45; color:#FF8A80; background:rgba(255,80,80,.12); padding:6px 8px; border-radius:4px;}
  .v16b .con small{display:block; text-align:right; color:#9AA6B5;}
  .v16b .tip{margin-top:12px; font-size:15px; color:#37414F; background:#F4F6F8; border-radius:10px; padding:10px 14px;}
  .v16b .tip b{color:#16233A; margin-right:10px;}
  .v16b .in{border:2px solid #16233A; border-radius:14px; background:#fff; padding:14px 18px;}
  .v16b .ih{font-size:13px; font-weight:800; color:#6B7785;}
  .v16b .h{margin:6px 0 10px; font-size:20px; font-weight:800; color:#16233A;}
  .v16b ul{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:8px;}
  .v16b li{display:grid; grid-template-columns:108px 1fr; gap:10px; align-items:baseline; opacity:0; animation:v16wIn .4s var(--d) forwards;}
  .v16b li b{font-size:15px; color:#fff; background:#F28C28; border-radius:6px; padding:2px 8px; text-align:center;}
  .v16b li span{font-size:17px; color:#16233A; line-height:1.45;}
  .v16b li.k3 span{font-family:ui-monospace,Menlo,monospace; font-size:13.5px; color:#B4232A;}
  .v16b li.k4 b{background:#16233A;}
  /* 1-6 · 웹 구조 · Next.js (v16x) */
  .v16x .nx{width:calc(320px + 170px + 300px); margin-bottom:22px; border:2px solid #16233A; border-bottom:0; height:16px; border-radius:10px 10px 0 0; position:relative; opacity:0; animation:v16wIn .4s .2s forwards;}
  .v16x .nx span{position:absolute; left:50%; top:-14px; transform:translateX(-50%); background:#16233A; color:#fff; font-size:15px; font-weight:800; padding:3px 14px; border-radius:8px; white-space:nowrap;}
  .v16x .row{display:grid; grid-template-columns:320px 170px 300px 150px 1fr; align-items:stretch;}
  .v16x .bx{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:26px 14px 12px; display:flex; flex-direction:column; gap:10px; min-height:300px;}
  .v16x .cap{position:absolute; top:-13px; left:12px; background:#5B6B80; color:#fff; font-size:14px; font-weight:800; padding:3px 10px; border-radius:7px; white-space:nowrap;}
  .v16x .cl .cap{background:#3C6FD1;} .v16x .sv{border-color:#F28C28;} .v16x .sv .cap{background:#F28C28;} .v16x .db .cap{background:#1E8E5A;}
  .v16x .bar{display:flex; align-items:center; gap:4px; padding:5px 8px; background:#E9ECF0; border-radius:8px 8px 0 0;}
  .v16x .bar i{width:8px; height:8px; border-radius:50%; background:#C3C9D1;}
  .v16x .bar span{flex:1; margin-left:6px; padding:1px 8px; border-radius:5px; background:#fff; font-family:ui-monospace,Menlo,monospace; font-size:12px; color:#16233A;}
  .v16x .scr{position:relative; height:180px; border:1px solid #E3E7EC; border-top:0; border-radius:0 0 8px 8px; margin-top:-8px;}
  .v16x .ly{position:absolute; inset:0; padding:12px 16px; display:flex; flex-direction:column; gap:7px; background:#fff; border-radius:0 0 8px 8px;}
  .v16x .l0{align-items:center; justify-content:center; color:#9AA6B5; font-size:15px;}
  .v16x .l1,.v16x .l2{opacity:0; animation:v16wIn .4s var(--d) forwards;}
  .v16x .ly p{margin:0; font-size:14px; color:#37414F; display:flex; justify-content:space-between; align-items:center;}
  .v16x .ly u{text-decoration:none; width:150px; padding:3px 8px; border:1.5px solid #D9DDE3; border-radius:6px; font-size:13px; color:#16233A;}
  .v16x .ly em{font-style:normal; align-self:flex-end; background:#16233A; color:#fff; font-size:13px; padding:4px 12px; border-radius:7px;}
  .v16x .l2 b{font-size:17px; color:#16233A;} .v16x .l2 p{padding:5px 10px; background:#F4F6F8; border-radius:6px;}
  .v16x .ft{font-size:13px; color:#6B7785; margin-top:auto;} .v16x .on{font-size:13px; color:#6B7785;}
  .v16x .f{border-radius:9px; padding:8px 12px; border:1.5px solid #E3E7EC; transition:none; animation:v16xHi .5s var(--d) forwards;}
  .v16x .f b{display:block; font-family:ui-monospace,Menlo,monospace; font-size:14px; color:#16233A;} .v16x .f span{font-size:13px; color:#6B7785;}
  @keyframes v16xHi{to{border-color:#F28C28; background:rgba(242,140,40,.08);}}
  .v16x .ok{margin-top:auto; text-align:center; font-size:15px; font-weight:800; color:#fff; background:#1E8E5A; border-radius:9px; padding:8px; opacity:0; animation:v16wIn .4s var(--d) forwards;}
  .v16x .ln{position:relative; display:flex; flex-direction:column; justify-content:center; gap:46px; padding:0 8px;}
  .v16x .tr{position:relative; height:20px;} .v16x .tr small{position:absolute; left:0; right:0; top:8px; text-align:center; font-size:12px; color:#9AA6B5;}
  .v16x .tr i{position:absolute; left:0; right:0; top:0; height:2px; background:#C3C9D1;}
  .v16x .tr i.r:after{content:""; position:absolute; right:-2px; top:-5px; border:6px solid transparent; border-left:9px solid #C3C9D1;}
  .v16x .tr i.l:after{content:""; position:absolute; left:-2px; top:-5px; border:6px solid transparent; border-right:9px solid #C3C9D1;}
  .v16x .xk{position:absolute; left:4px; right:4px; text-align:center; font-size:14px; font-weight:800; color:#fff; padding:5px 4px; border-radius:8px; opacity:0; line-height:1.3;}
  .v16x .xk.r{top:calc(50% - 50px); background:#3C6FD1; animation:v16xR 1.1s var(--d) forwards;}
  .v16x .xk.l{top:calc(50% + 14px); background:#F28C28; animation:v16xL 1.1s var(--d) forwards;}
  .v16x .row > .ln:nth-of-type(4) .xk.r{background:#F28C28;} .v16x .row > .ln:nth-of-type(4) .xk.l{background:#1E8E5A;}
  @keyframes v16xR{0%{opacity:0; transform:translateX(-80px)} 20%{opacity:1} 75%{opacity:1} 100%{opacity:0; transform:translateX(80px)}}
  @keyframes v16xL{0%{opacity:0; transform:translateX(80px)} 20%{opacity:1} 75%{opacity:1} 100%{opacity:0; transform:translateX(-80px)}}
  .v16x .cy{position:relative; flex:1; display:flex; flex-direction:column; gap:8px; padding:20px 10px 10px; background:#EEF7F2; border-radius:50% 50% 12px 12px / 22px 22px 12px 12px;}
  .v16x .cy i{position:absolute; left:0; right:0; top:0; height:22px; border-radius:50%; background:#D3EDDF;}
  .v16x .t{position:relative; margin:0; font-size:12.5px; color:#37414F; background:#fff; border-radius:6px; padding:5px 8px; animation:v16xDb .5s var(--d) forwards;}
  .v16x .t b{display:block; font-family:ui-monospace,Menlo,monospace; color:#1E8E5A; font-size:13px;}
  @keyframes v16xDb{to{box-shadow:0 0 0 3px #1E8E5A;}}
  .v16x .lg2{list-style:none; margin:22px 0 0; padding:0; display:grid; grid-template-columns:repeat(7,1fr); gap:6px;}
  .v16x .lg2 li{font-size:13.5px; color:#37414F; background:#F4F6F8; border-radius:8px; padding:6px 8px; opacity:.25; animation:v16xOn .3s var(--d) forwards;}
  .v16x .lg2 em{font-style:normal; color:#F28C28; font-weight:800; margin-right:4px;}
  @keyframes v16xOn{to{opacity:1;}}
  .v16x .lg{margin-top:12px; animation-delay:9.6s;}
  /* 1-6 · 웹의 3요소 (v16w) — 평택대 p3w 구조 */
  .v16w{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:20px; align-items:start;}
  .v16wc{display:flex; flex-direction:column; gap:10px; opacity:0; animation:v16wIn .5s var(--d) forwards;}
  @keyframes v16wIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  .v16wh{display:flex; align-items:baseline; gap:10px;} .v16wh b{font-size:21px; color:#16233A;} .v16wh span{font-size:14px; color:#6B7785;}
  .v16wc.on .v16wh b{color:#E07A12;}
  .v16wb{border:1.5px solid #C9CFD8; border-radius:10px; overflow:hidden; background:#fff; height:250px; box-shadow:0 2px 8px rgba(0,0,0,.06);}
  .v16wb .br{display:flex; align-items:center; gap:5px; height:26px; padding:0 10px; background:#EEF1F4; border-bottom:1px solid #D9DDE3;}
  .v16wb .br i{width:9px; height:9px; border-radius:50%; background:#C9CFD8;}
  .v16wb .br span{margin-left:8px; font-size:11.5px; color:#6B7785;}
  .v16wR{font-family:"Times New Roman",Times,serif; color:#000; padding:8px 12px; font-size:14px; line-height:1.35;}
  .v16wR p{margin:0 0 4px;} .v16wR ul{margin:0 0 4px; padding-left:20px;} .v16wR button{font:inherit; font-size:13px; margin:2px 0 6px;}
  .v16wR h1{font-size:24px; margin:4px 0 6px; font-family:inherit;}
  .v16wS{display:grid; grid-template-columns:42% 1fr; height:224px; font-size:12.5px; color:#37352F;}
  .v16wS .sd{background:#F7F7F5; border-right:1px solid #EBEBEA; padding:10px 8px;}
  .v16wS .sd > i{display:block; font-style:normal; font-weight:700; font-size:12.5px; padding:0 6px 8px;}
  .v16wS ul{list-style:none; margin:0; padding:0;}
  .v16wS li{padding:4px 6px; border-radius:5px; white-space:nowrap;}
  .v16wS li.on, .v16wS li.on0{background:#E3E2DF; font-weight:600;}
  .v16wS li.on0{animation:v16wOff .3s calc(var(--d) + 1.4s) forwards;}
  .v16wS li.nw{opacity:0; background:#E3E2DF; font-weight:600; animation:v16wNew .4s calc(var(--d) + 1.4s) forwards;}
  .v16wS .bt{display:block; font-weight:400; color:#6B6B6B; padding:4px 6px; margin-top:4px; border-radius:5px;}
  .v16wc.on .v16wS .bt{animation:v16wClk .5s calc(var(--d) + .8s) 2 alternate;}
  .v16wS .mn{padding:12px 12px;} .v16wS h1{font-size:20px; margin:0 0 10px; position:relative; height:26px;}
  .v16wS h1 span{position:absolute; left:0; top:0; white-space:nowrap;} .v16wS h1 .t1{opacity:0; color:#C4C4C2; animation:v16wNew .3s calc(var(--d) + 1.4s) forwards;}
  .v16wS h1 .t0{animation:v16wGone .3s calc(var(--d) + 1.4s) forwards;}
  .v16wS .bk{padding:3px 0; font-size:12px;} .v16wS .bk.g{animation:v16wGone .3s calc(var(--d) + 1.4s) forwards;}
  .v16wS .bk u{display:inline-block; width:10px; height:10px; border:1.5px solid #9B9A97; border-radius:2px; margin-right:6px; vertical-align:-1px;}
  @keyframes v16wClk{to{background:#F6C99A; color:#16233A}}
  @keyframes v16wNew{to{opacity:1}} @keyframes v16wGone{to{opacity:0}} @keyframes v16wOff{to{background:transparent; font-weight:400}}
  .v16wk{margin:0; background:#1E1E2E; color:#E6E6E6; border-radius:10px; padding:10px 14px; font-family:var(--mono); font-size:12.5px; line-height:1.55; white-space:pre; overflow:hidden;}
  .v16wk em{font-style:normal; color:#F2B880; font-weight:700;}
  @media print{.v16wc{animation:none; opacity:1} .v16wS li.nw, .v16wS h1 .t1{animation:none; opacity:1} .v16wS h1 .t0, .v16wS .bk.g{animation:none; opacity:0}
    .v16wS li.on0{animation:none; background:transparent; font-weight:400}}
  /* 1-6 · 화면 뒤의 코드 (v16c) */
  .v16top{display:flex; gap:12px; align-items:center; font-size:16px; font-weight:800; color:#16233A; opacity:0; animation:v16In .4s var(--d) forwards;}
  .v16top span{background:#F4F6F9; border:1.5px solid #C9D6E6; border-radius:8px; padding:5px 12px;} .v16top span.cc{background:#16233A; color:#fff; border-color:#16233A;}
  .v16top i{font-style:normal; color:#F28C28;}
  .v16cs{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:14px;}
  .v16c{border:2px solid #C9D6E6; border-radius:14px; background:#fff; padding:12px 14px; opacity:0; transform:translateY(10px); animation:v16In .5s var(--d) forwards;}
  .v16c .hd{display:flex; justify-content:space-between; align-items:baseline; border-bottom:2px solid #E3E6EA; padding-bottom:6px;}
  .v16c .hd b{font-family:var(--mono); font-size:18px; color:#16233A;} .v16c .hd small{font-size:13px; color:#6B7785;}
  .v16c .rl{margin:8px 0 6px;} .v16c .rl strong{font-size:20px; color:#C76A12; margin-right:8px;} .v16c .rl span{font-size:14px; color:#3A4657;}
  .v16c ul{list-style:none; margin:0; padding:0;}
  .v16c li{display:flex; flex-direction:column; padding:5px 0; border-top:1px dashed #E3E6EA; opacity:0; animation:v16In .3s var(--d) forwards;}
  .v16c li code{font-size:13px; color:#6B7785;} .v16c li span{font-size:15.5px; font-weight:700; color:#16233A;}
  .v16c .hs{margin-top:8px; display:inline-block; font-size:13px; font-weight:700; color:#6B7785; background:#F4F6F9; border-radius:6px; padding:2px 8px;}
  .v16c.c0{border-top:5px solid #16233A;} .v16c.c1{border-top:5px solid #2383E2;} .v16c.c2{border-top:5px solid #F28C28;}
  .v16d{display:grid; grid-template-columns:170px 1fr auto; gap:14px; align-items:center; margin-top:14px; background:#FFF8F0; border:2px dashed #F2B880; border-radius:14px; padding:10px 14px;
    opacity:0; animation:v16In .5s var(--d) forwards;}
  .v16d .lb{font-size:19px; font-weight:800; color:#C76A12;} .v16d .lb small{display:block; font-size:12.5px; color:#6B7785;}
  .v16d .pg{display:flex; flex-wrap:wrap; gap:6px; align-items:center;} .v16d .pg b{font-size:16px; color:#16233A; margin-right:4px;}
  .v16d .k{font-size:13.5px; background:#fff; border:1.5px solid #E3E6EA; border-radius:6px; padding:2px 8px; color:#3A4657;}
  .v16d .bk{font-size:13.5px; background:#fff; border:1.5px solid #F2B880; border-radius:6px; padding:2px 8px; color:#16233A;} .v16d .bk i{font-style:normal; color:#C76A12; font-weight:700; margin-right:6px;}
  .v16d .ls{font-family:var(--mono); font-size:14px; font-weight:700; color:#16233A;}
  @keyframes v16In{to{opacity:1; transform:none;}}
  @media print{.v16top,.v16c,.v16c li,.v16d{opacity:1; animation:none; transform:none}}
  /* 1-6 · 브라우저로 열기 (v16s) */
  .v16s .pc{position:relative; display:grid; grid-template-columns:230px 1fr 440px; align-items:center;
    border:2px dashed #9AA6B5; border-radius:18px; padding:42px 26px 26px; margin-top:6px;}
  .v16s .pcl{position:absolute; top:-15px; left:22px; background:#fff; padding:0 10px; font-size:17px; font-weight:800; color:#16233A;}
  .v16s .fd{display:flex; flex-direction:column; gap:10px; padding:18px; border:1.5px solid #C9CFD8; border-radius:12px; background:#F7F8FA;}
  .v16s .fd b{font-size:19px; color:#16233A; margin-bottom:2px;}
  .v16s .fd i{font-style:normal; font-family:ui-monospace,Menlo,monospace; font-size:17px; padding:8px 12px; border-radius:7px; background:#fff; border:1.5px solid #D9DDE3;}
  .v16s .fd .f1{animation:v16sHi .4s 1.0s forwards;} .v16s .fd .f2{animation:v16sHi .4s 2.0s forwards;} .v16s .fd .f3{animation:v16sHi .4s 2.2s forwards;}
  @keyframes v16sHi{to{background:#FFF1E2; border-color:#E07A12; color:#B65A00;}}
  .v16s .ln{position:relative; padding:0 26px;}
  .v16s .lb{display:block; font-size:18px; font-weight:800; color:#9AA6B5; text-align:center; margin:8px 0;}
  .v16s .ln .lb:first-child{animation:v16sLb .3s 1.0s forwards;} .v16s .ln .lb:last-child{animation:v16sLb .3s 2.0s forwards;}
  @keyframes v16sLb{to{color:#E07A12;}}
  .v16s .ar{height:3px; background:#9AA6B5; position:relative; margin:14px 0;}
  .v16s .ar.rt::after{content:""; position:absolute; right:-8px; top:-7px; border:8px solid transparent; border-left-color:#9AA6B5;}
  .v16s .tk{position:absolute; top:50%; margin-top:-12px; display:flex; gap:4px; opacity:0; animation:v16sR 1.2s 2.2s forwards;}
  .v16s .tk u{text-decoration:none; font-size:13px; font-weight:800; color:#fff; background:#E07A12; border-radius:5px; padding:3px 7px;}
  @keyframes v16sR{0%{opacity:1; left:26px} 90%{opacity:1; left:calc(100% - 110px)} 100%{opacity:0; left:calc(100% - 110px)}}
  .v16s .bwW{position:relative; display:flex; flex-direction:column; gap:6px;}
  .v16s .bwl{font-size:16px; font-weight:700; color:#6B7785;}
  .v16s .lb4{font-size:18px; font-weight:800; color:#9AA6B5; text-align:center; animation:v16sLb .3s 3.5s forwards;}
  .v16s .v16wb{position:relative; height:250px;}
  .v16s .v16wb .ad{flex:1; margin-left:10px; padding:2px 10px; border-radius:6px; background:#fff; font-family:ui-monospace,Menlo,monospace; font-size:12.5px; color:#16233A;}
  .v16s .pg{opacity:0; animation:v16wIn .5s 3.5s forwards;}
  .v16s .emp{position:absolute; inset:26px 0 0; display:flex; align-items:center; justify-content:center; font-size:15px; color:#9AA6B5; animation:v16sOut .2s 3.5s forwards;}
  @keyframes v16sOut{to{opacity:0;}}
  .v16s .lg{display:grid; grid-template-columns:1fr 1.3fr 1.3fr; gap:14px; margin-top:22px; opacity:0; animation:v16wIn .5s 4.2s forwards;}
  .v16s .lg p{margin:0; font-size:18px; color:#37414F; padding:14px 18px; border-radius:10px; background:#F4F6F8;}
  .v16s .lg b{color:#16233A; margin-right:10px; font-size:19px;}
"""


def slides():
    return [
        # ── 웹의 3요소
        light("HTML과 프로그래밍 언어", shot("v1_u6_html_meme.webp", "개발자 유머 짤", [
            ("HTML", "HyperText Markup Language · 화면 구조를 표시하는 언어"),
            ("프로그래밍 언어", "조건 · 반복 · 계산으로 동작을 정함"),
            ("웹에서 동작 담당", "JS(JavaScript)")]), T),
        light("웹의 3요소", _web3(), T),
        light("브라우저로 열기", _open(), T),
        light("Node.js", _node(), T),
        light("웹 구조 · Next.js", _next(), T),
        # ── 서버
        light("권한 모드", viz2.maprows([
            ("Manual (default)", "읽기만 자동", "파일 수정 · 명령마다 물어봄"),
            ("acceptEdits", "파일 수정까지 자동", "흔한 파일 명령도 자동"),
            ("plan", "읽고 계획만", "소스 파일은 고치지 않음"),
            ("auto", "백그라운드 안전 검사 후 진행", "쓸 수 있는 환경에서만")], "모드", "Claude Code가 묻지 않고 하는 일")
              + note("이 강의에서 쓰지 않음", "dontAsk · bypassPermissions (격리된 컨테이너 · VM 전용)")
              + src(("Claude Code · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        light("모드 전환", viz2.tiles([
                  ("모드 표시", "입력창 아래 · 눌러서 고르기"), ("/plan", "요청 앞에 붙이면 plan"),
                  ("다음 대화", "고른 모드가 이어짐")], 3)
              + viz2.maprows([
            ("기획서 · 개발 계획", "plan", "파일 변경 없이 계획만"),
            ("첫 태스크 몇 개", "Manual", "수정마다 확인 · 승인"),
            ("흐름에 익숙해진 뒤", "acceptEdits", "수정은 자동 · 결과는 브라우저 확인")], "단계", "모드")
              + note("auto", "계정 · 환경에 따라 목록에 없을 수 있음"), T),
        # ── 한 번에 하나씩
        light("한 번에 구현할 때의 문제", viz2.tiles([
            ("오류 위치 파악 어려움", "여러 파일이 동시에 바뀜"), ("연쇄 오류", "「/」 메뉴 수정 → 엔터 동작 고장"),
            ("복구 지점 없음", "중간 커밋 없음")], 3)
              + viz2.pair(
                  "한 번에", [("요청 1번", "태스크 전부"), ("확인", "끝나고 한꺼번에")],
                  "하나씩", [("요청 = 태스크 수", "하나 끝나면 다음 하나"), ("확인", "태스크마다 · 문제 범위가 태스크 하나")]), T),
        # ── 테스트 케이스 · 디버깅
        light("순서도와 테스트 케이스", viz2.maprows([
            ("회사 이메일 · 비밀번호 일치", "로그인 완료", "kim@company.com · 맞는 비밀번호"),
            ("회사 이메일 아님", "거절", "kim@gmail.com"),
            ("비밀번호 틀림", "다시 입력", "회사 이메일 · 틀린 비밀번호 1번"),
            ("5번째 틀림", "10분 잠금", "틀린 비밀번호 5번")], "순서도 갈래", "기대 결과 · 입력")
              + note("테스트 케이스", "로그인 순서도의 갈래 하나 = 확인 하나 · 만들기 전에 AI에게 먼저 줌"), T),
        light("태스크 진행 순서", flow([
            ("테스트 케이스", "입력 → 기대 결과"), ("태스크 요청", "「이 태스크만 · 이 케이스로 확인」"), ("브라우저 확인", "케이스대로 직접 눌러 보기"),
            ("수정 요청", "기대 · 실제 · 오류 원문"), ("커밋", "케이스 모두 통과 뒤")], hl=0)
              + note("반복", "테스트 케이스 통과까지 확인 · 수정 반복 · 문제는 그 태스크 안에서 해결")
              + src(("참고 · 비디오머그 「나만 안 해 바이브 코딩」", "https://www.youtube.com/watch?v=C9aQKsL2NVM"),
                    ("참고 · 코딩애플 「AI 에이전트 만드는 기초 기술」", "https://www.youtube.com/watch?v=eu5H0iRJsJ4")), T),
        ba("태스크 요청 예시", T, "「나머지 다 만들어 줘」",
           "「개발 계획에서 「/」 메뉴 태스크만 진행해 줘.\n빈 블록에 「/」 → 「체크 상자」 고르면 그 블록이 체크 상자로 · 이 케이스로 확인해 줘」",
           "태스크 이름 + 테스트 케이스 (입력 → 기대 결과)"),
        # ── 마음에 안 들 때
        light("오류 해결 과정 비교", viz2.pair(
            "검색으로 해결", [("① 오류 메시지 복사", "빨간 글씨 그대로"), ("② 검색", "구글 · Stack Overflow"), ("③ 비슷한 질문 찾기", "영어 답변 해석"),
                         ("④ 내 코드에 맞게 고치기", "직접 수정"), ("⑤ 실행 → 다른 오류면 ①부터", "반복")],
            "바이브코딩", [("① 증상 · 오류 화면 전달", "「버튼을 눌러도 반응 없음」 + 화면 캡처"), ("② AI가 원인 파악 · 수정", "파일 읽기 · 고치기"),
                       ("③ 실행해 확인", "브라우저에서 다시 눌러 보기"), ("④ 안 되면 증상 다시 전달", "달라진 점 그대로")], hl="r")
              + src(("참고 · 이동훈의 루트AI 「바이브코딩 15분」", "https://www.youtube.com/watch?v=TImjZnT87ys")), T),
        light("버그 알리는 방법", _bug(), T),
        ba("구체적 수정 요청", T, "「더 예쁘게 해 줘」",
           "「왼쪽 목록에서 긴 페이지 제목이 잘려.\n목록 폭은 그대로, 제목은 두 줄까지 보이게」",
           "세 칸 · 어디 · 지금 상태 · 원하는 결과 · 한 번에 하나"),
        light("화면 캡처 첨부", viz2.tiles([
            ("화면 캡처 붙이기", "입력창에 붙여 넣기 · 끌어다 놓기"), ("가리키기", "「캡처에서 오른쪽 위 버튼」"),
            ("오류 문구", "브라우저 오류는 그대로 복사해 붙이기")], 3)
              + chat([("me", "[화면 캡처 붙임]\n「/」 메뉴가 화면 아래로 잘려서 「구분선」이 안 보여. 메뉴가 화면 안에 다 보이게 해 줘."),
                      ("ai", "메뉴 아래 공간이 모자라면 블록 위쪽에 열리게 바꿨다. 새로고침해서 확인해 줘.")], "캡처와 함께 요청 · 예")
              , T),
        light("Git으로 되돌리기", flow([
            ("수정 요청", "디자인 변경"), ("확인", "전보다 나빠짐"), ("「마지막 커밋 상태로 되돌려 줘」", ""), ("다시 요청", "수정 요청 세 칸 형식")], hl=2)
              + chat([("me", "방금 바꾼 디자인이 전보다 별로야. 마지막 커밋 상태로 되돌려 줘."),
                      ("ai", "마지막 커밋 뒤에 고친 style.css 를 되돌렸다.")], "되돌리기 대화 예")
              + note("커밋", "태스크마다 남긴 커밋이 돌아갈 세이브 포인트"), T),
        light("체크포인트와 Git", viz2.pair(
            "체크포인트 (/rewind · Esc 두 번)", [("남는 때", "요청마다 자동"), ("되감기", "코드 · 대화 · 둘 다"),
                                              ("못 잡는 것", "Bash 명령으로 바뀐 파일 · Claude Code 밖에서 고친 파일")],
            "Git 커밋", [("남는 때", "내가 「커밋해 줘」 한 시점"), ("보관", "지우기 전까지 · GitHub 에도"), ("배포", "커밋을 가져가 공개")], hl="r")
              + note("공식 문서", "체크포인트는 버전 관리를 대신하지 않음")
              + src(("Claude Code · Checkpointing", "https://code.claude.com/docs/en/checkpointing")), T),
        light("바이브 디버깅 순서", flow([
            ("증상 전달", "재현 · 기대 · 실제 · 오류 원문"),
            ("원인 먼저", "「고치기 전에 원인부터」"), ("통과 · 저장", "테스트 통과 → 커밋"), ("두 번 실패", "되돌리고 새 대화")], hl=0)
              + src(("Claude Code 문서 · Best practices", "https://code.claude.com/docs/en/best-practices")), T),
        # ── 실습
        labcard(T, "개발 계획으로 앱 만들기", T, "개발계획.md", "동작하는 앱", ["태스크 하나씩", "브라우저 확인", "커밋"]),
        brief("1-6", T,
              ["태스크 하나 요청 · 「첫 태스크만」", "브라우저로 눌러 보기", "완료 기준 대조", "「커밋해 줘」 → 다음 태스크",
               "다 만든 뒤 순서도 → 빠진 조건 피드백"],
              [],
              ["태스크 하나", "커밋해 줘", "순서도로 그려 줘", "되돌려 줘"],
              ["태스크마다 브라우저로 직접 눌러 봄", "순서도에 빠진 조건을 넣고 앱도 고침"],
              "엉뚱하게 만들기 시작하면 Esc 로 멈추고 다시 요청 · 망가지면 「마지막 커밋으로 되돌려 줘」"),
        tstep(T, 1, "태스크 하나 요청", T, ask=("Claude Code 입력창", "개발계획.md 의 첫 태스크만 만들어 줘"),
              rows=[("한 번에", "태스크 하나만"), ("승인", "파일마다 패널에서 승인"), ("자동 승인", "이 대화 동안 · 익숙해진 뒤")]),
        light("실습 1-6 · 2단계 브라우저 확인", viz2.tiles([("열기", "index.html 더블클릭"), ("눌러 보기", "방금 만든 기능 · 테스트 케이스대로"),
                                              ("새로고침", "macOS ⌘R · Windows F5"), ("다르면", "기대 · 실제 · 오류 원문으로 수정 요청")], 2), T),
        light("실습 1-6 · 3단계 완료 기준 대조", viz2.tiles([("보고", "Claude Code 작업 보고 · 만든 것 · 아직 없는 것"), ("대조", "개발계획.md 의 그 태스크 완료 기준"),
                                                ("아직 없는 것", "다음 태스크에서 만들 것인지 확인"), ("빠진 것", "그 태스크 안에서 다시 요청")], 2), T),
        tstep(T, 4, "커밋해 줘", T, ask=("Claude Code 입력창", "커밋해 줘"),
              rows=[("메시지", "Claude Code 가 작성"), ("커밋", "태스크마다 하나"), ("다음", "다음 태스크 → 같은 순서")]),
        tstep(T, 5, "순서도 그리기", T, ask=("Claude Code 입력창", "지금까지 만든 앱이 동작하는 순서를 순서도로 그려 줘"),
              rows=[("때", "태스크를 다 만든 뒤"), ("볼 것", "처리 · 조건 · 반복 · 끝 (1-1)"), ("찾을 것", "「이럴 땐?」 갈래가 없는 곳")]),
        tstep(T, 5, "빠진 조건 피드백", T, ask=("Claude Code 입력창 · 예", "「/」 메뉴에서 찾는 항목이 없으면\n「결과 없음」을 보여 주는 조건을 순서도에 넣고 앱도 고쳐 줘"),
              rows=[("피드백", "조건 하나씩 · 1-1 로그인 순서도처럼"), ("확인", "고친 순서도 · 브라우저로 그 갈래 눌러 보기"), ("끝", "「커밋해 줘」")]),
        light("실습 1-6 확인", checks([
            ("태스크마다 브라우저로 눌러 봤나", "테스트 케이스대로"), ("개발 계획 완료 기준을 다 확인했나", "빠진 것은 다시 요청"),
            ("커밋 기록이 태스크 수만큼 쌓였나", "「커밋 기록 보여 줘」"),
            ("순서도에 빠진 조건을 하나 이상 넣었나", "앱에도 반영됐는지 눌러 보기")],
            "막히면 labs/mini_notion/예시/app 과 비교"), T),
    ]
