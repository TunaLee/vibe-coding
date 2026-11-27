"""2-1 웹 앱의 데이터 흐름.

클라이언트 · 서버 · DB(1-6 웹 구조 복습 · 한 장)
→ 요청과 응답(장면: 로딩 → GET → SQL → 행 → JSON → 화면) → 요청 · 응답 읽기 → 쓰기 요청(POST → insert → 201 → 목록 추가)
→ 상태 코드.
외부 API(공휴일)는 2-5 · MCP 는 2-6.
사실 출처: supabase.com/docs/guides/api (REST · /rest/v1/표이름) · developer.mozilla.org HTTP 메서드 · 상태 코드
· developer.chrome.com/docs/devtools/network
"""
import viz2
from deck import light
from hx import esc, note
from stats_hx import src
from v2kit import codemap
import v2scene
from v2scene import reqres, steps

T = "2-1"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
SB_API = ("Supabase · REST API", "https://supabase.com/docs/guides/api")
MDN_M = ("MDN · HTTP 요청 메서드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods")
MDN_S = ("MDN · HTTP 상태 코드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status")
MDN_MSG = ("MDN · HTTP 메시지", "https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/Messages")
MDN_HTTP = ("MDN · HTTP 개요", "https://developer.mozilla.org/ko/docs/Web/HTTP/Guides/Overview")
NETP = ("Chrome DevTools · Network", "https://developer.chrome.com/docs/devtools/network")

CSS = """
  /* 2-1 · API = 은행 창구 (v21api) */
  .v21api{display:grid; grid-template-columns:230px 1fr 40px 260px; gap:14px; align-items:stretch; margin:10px 0 16px; min-height:300px;}
  .v21api .h{font-size:18px; font-weight:800; color:#16233A; margin-bottom:8px;} .v21api .h small{display:block; font-size:13px; font-weight:600; color:#6B7785;}
  .v21api .cu,.v21api .ct,.v21api .vault{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; padding:10px 12px; display:flex; flex-direction:column; gap:7px;}
  .v21api .slip{border:1.5px dashed #F28C28; background:#FFF8F0; border-radius:8px; padding:6px 10px; font-size:14px; color:#16233A; opacity:0; animation:v21in .35s var(--d) forwards;}
  .v21api .slip em{display:block; font-style:normal; font-size:12px; font-weight:800; color:#E07A12;}
  .v21api .slip.bad{border-color:#C0392B; background:#FDECEA;} .v21api .slip.bad em{color:#C0392B;}
  .v21api .w{display:grid; grid-template-columns:44px 64px 1fr; align-items:center; gap:8px; border:1.5px solid #E3E7EC; border-radius:8px; padding:6px 10px;
    opacity:0; animation:v21in .3s var(--d) forwards;}
  .v21api .w.on{animation:v21in .3s var(--d) forwards, v21pick .35s var(--p) forwards;}
  .v21api .w b{font-size:15px; color:#16233A;} .v21api .w code{font-size:13px; font-weight:700; color:#1F3A5F;} .v21api .w span{font-family:var(--mono); font-size:12.5px; color:#3A4657;}
  .v21api .rej{margin-top:auto; font-size:14px; font-weight:800; color:#C0392B; background:#FDECEA; border-radius:8px; padding:6px 10px; opacity:0; animation:v21in .35s var(--d) forwards;}
  .v21api .wall{background:repeating-linear-gradient(45deg,#D9DDE3 0 8px,#EEF1F5 8px 16px); border-radius:6px; position:relative;}
  .v21api .wall span{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%) rotate(-90deg); white-space:nowrap; font-size:12.5px; font-weight:800; color:#3A4657; background:#fff; padding:2px 8px; border-radius:6px;}
  .v21api .vault{border:2px solid #1F3A5F; background:#F4F6F9;}
  .v21api .sf{font-size:13px; color:#6B7785; margin:-6px 0 4px;}
  .v21api .r{font-size:14px; color:#16233A; background:#fff; border:1px solid #E3E7EC; border-radius:6px; padding:5px 9px; animation:v21row .4s var(--d) forwards;}
  @keyframes v21in{from{opacity:0} to{opacity:1}}
  @keyframes v21pick{to{border-color:#F28C28; background:#FFF3E0}}
  @keyframes v21row{to{background:#FFF3E0; border-color:#F7C99A}}
  @media print{.v21api .slip,.v21api .w,.v21api .rej{opacity:1; animation:none}}
  /* 2-1 · 웹 앱의 3요소 (v21three) */
  .v21three{display:grid; grid-template-columns:1fr 90px 1fr 90px 1fr; align-items:stretch; margin:0 0 12px;}
  .v21three .k{border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:12px 14px; display:flex; flex-direction:column; gap:10px; opacity:0; animation:v21in .45s var(--d) forwards;}
  .v21three .t b{font-size:22px; color:#16233A; margin-right:8px;} .v21three .t span{font-size:14px; color:#6B7785;}
  .v21three .mk{border-radius:10px; min-height:96px; padding:8px 10px; display:flex; flex-direction:column; gap:5px; justify-content:center;}
  .v21three .mk.br{border:1.5px solid #C9CFD8; background:#F6F8FA; position:relative; padding-top:16px;}
  .v21three .mk.br i{position:absolute; top:5px; left:8px; width:30px; height:5px; border-radius:3px; background:#C9CFD8;}
  .v21three .chips{display:flex; gap:6px;} .v21three .chips em{flex:1; text-align:center; font-style:normal; font-weight:800; font-size:14px; color:#fff; border-radius:6px; padding:6px 0;}
  .v21three .chips .h{background:#E44D26;} .v21three .chips .c{background:#264DE4;} .v21three .chips .j{background:#C9A400;}
  .v21three .mk.br small{font-size:12.5px; color:#6B7785; text-align:center;}
  .v21three .mk.sv{background:#16233A;} .v21three .mk.sv code{font-size:13px; color:#E8ECF1; background:none;}
  .v21three .mk.db{border:1.5px solid #C9CFD8; background:#fff;} .v21three .mk.db table{border-collapse:collapse; width:100%; font-size:13px;}
  .v21three .mk.db th{background:#1F3A5F; color:#fff; font-family:var(--mono); font-size:12px; padding:3px 6px; text-align:left;} .v21three .mk.db td{border-bottom:1px solid #E3E7EC; padding:3px 6px;}
  .v21three ul{margin:0; padding-left:18px; font-size:15px; color:#3A4657; line-height:1.55;}
  .v21three .ln{display:flex; flex-direction:column; justify-content:center; gap:22px; padding:0 6px; opacity:0; animation:v21in .4s var(--d) forwards;}
  .v21three .ln span{font-size:13.5px; font-weight:800; text-align:center; border-bottom:3px solid #F28C28; color:#E07A12; padding-bottom:2px;}
  .v21three .ln span + span{border-color:#1F3A5F; color:#1F3A5F;}
  .v21cmp{display:grid; grid-template-columns:1fr 1.3fr; gap:12px; margin:0 0 12px; opacity:0; animation:v21in .45s var(--d) forwards;}
  .v21cmp span,.v21cmp b{font-size:15.5px; border-radius:10px; padding:8px 12px; text-align:center;}
  .v21cmp span{background:#EEF1F5; color:#3A4657;} .v21cmp b{background:#FFE3C4; color:#B85A00;}
  /* 2-1 · HTTP 메시지 (v21msg) */
  .v21msg{display:grid; grid-template-columns:1fr 1fr; gap:18px; margin:0 0 12px;}
  .v21msg .msg{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; padding:10px 12px; display:flex; flex-direction:column; gap:6px;}
  .v21msg .h{font-size:17px; font-weight:800; color:#16233A; margin-bottom:2px;}
  .v21msg .pt{display:grid; grid-template-columns:1fr 180px; gap:10px; align-items:center; border-radius:8px; padding:6px 8px; background:#F6F8FA; opacity:.25;
    animation:v21lit .4s var(--d) forwards;}
  .v21msg .pt .tx{display:flex; flex-direction:column;} .v21msg .pt code{font-size:13.5px; color:#16233A; background:none; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  .v21msg .pt em{font-style:normal; font-size:13px; font-weight:800; border-left:3px solid currentColor; padding-left:8px;}
  .v21msg .pt.s em{color:#E07A12;} .v21msg .pt.h em{color:#1F4E8C;} .v21msg .pt.b em{color:#1E7B45;}
  @keyframes v21lit{to{opacity:1}}
  @media print{.v21three .k,.v21three .ln,.v21cmp{opacity:1; animation:none} .v21msg .pt{opacity:1; animation:none}}
"""


def counter():
    """은행 창구 = API — 손님(브라우저)은 금고(DB)에 직접 못 들어감 · 정해진 창구(요청 목록)로만 요청 · 직원(서버)이 금고에서 꺼내 줌.
    창구 4개가 차례로 켜짐 → 조회 창구에 신청서 → 금고 행이 켜짐 → 목록에 없는 요청은 거절. 칸은 제자리."""
    win = [("조회", "GET", "/rest/v1/tasks", .4), ("등록", "POST", "/rest/v1/tasks", .7),
           ("변경", "PATCH", "/rest/v1/tasks?id=…", 1.0), ("삭제", "DELETE", "/rest/v1/tasks?id=…", 1.3)]
    w = "".join(f'<div class="w{" on" if i == 0 else ""}" style="--d:{d}s; --p:2.4s"><b>{k}</b><code>{m}</code><span>{u}</span></div>'
                for i, (k, m, u, d) in enumerate(win))
    return ('<div class="v21api">'
            '<div class="cu"><div class="h">손님 · 브라우저</div><div class="slip" style="--d:2.0s"><em>신청서 = 요청</em>조회 · tasks 전체</div>'
            '<div class="slip bad" style="--d:4.0s"><em>신청서 = 요청</em>금고 직접 열기</div></div>'
            f'<div class="ct"><div class="h">창구 = API<small>정해진 요청만 받음</small></div>{w}'
            '<div class="rej" style="--d:4.4s">창구 목록에 없는 요청 → 거절</div></div>'
            '<div class="wall"><span>직원만 출입</span></div>'
            '<div class="vault"><div class="h">금고 · DB</div><div class="sf">직원 = 서버</div>'
            '<div class="r" style="--d:3.0s">41 · 주간 보고서 작성</div><div class="r" style="--d:3.15s">42 · 교육 자료 준비</div>'
            '<div class="r" style="--d:3.3s">43 · 예산안 검토</div></div></div>')


def three():
    """웹 앱의 3요소 — 클라이언트(1-6 웹의 3요소 HTML · CSS · JS 가 안에) · 서버 · DB. 칸이 차례로 나타나고 사이 선이 그어짐."""
    cl = ('<div class="k" style="--d:.3s"><div class="t"><b>클라이언트</b><span>화면 · 브라우저</span></div>'
          '<div class="mk br"><i></i><div class="chips"><em class="h">HTML</em><em class="c">CSS</em><em class="j">JS</em></div>'
          '<small>1-6 웹의 3요소</small></div>'
          '<ul><li>요청 보내기</li><li>받은 데이터로 화면 그리기</li></ul></div>')
    sv = ('<div class="k" style="--d:1.1s"><div class="t"><b>서버</b><span>처리 · 프로그램</span></div>'
          '<div class="mk sv"><code>요청 받기</code><code>누구인지 · 권한 확인</code><code>DB 에 묻기 → 답 만들기</code></div>'
          '<ul><li>요청마다 실행</li><li>키 · 규칙은 여기에만</li></ul></div>')
    db = ('<div class="k" style="--d:1.9s"><div class="t"><b>DB</b><span>저장 · 데이터베이스</span></div>'
          '<div class="mk db"><table><tr><th>id</th><th>title</th></tr><tr><td>41</td><td>주간 보고서 작성</td></tr>'
          '<tr><td>42</td><td>교육 자료 준비</td></tr></table></div>'
          '<ul><li>표에 행으로 보관</li><li>서버만 직접 접근</li></ul></div>')
    ln = lambda a, b, d: f'<div class="ln" style="--d:{d}s"><span>{a} →</span><span>← {b}</span></div>'
    return ('<div class="v21three">' + cl + ln("요청", "응답", 1.0) + sv + ln("질의", "결과", 1.8) + db + '</div>'
            '<div class="v21cmp" style="--d:2.6s"><span>웹 페이지 3요소 · HTML · CSS · JS = 화면 하나</span>'
            '<b>웹 앱 3요소 · 클라이언트 · 서버 · DB = 화면 + 처리 + 저장</b></div>')


def message():
    """HTTP 메시지 — 요청 · 응답 글자 그대로. 시작 줄 · 헤더 · 빈 줄 · 본문이 차례로 켜짐."""
    def blk(title, parts, d0):
        r = ""
        for i, (cls, lab, lines) in enumerate(parts):
            body = "".join(f"<code>{esc(x) if x else '&nbsp;'}</code>" for x in lines)
            r += f'<div class="pt {cls}" style="--d:{d0 + i * .5:.1f}s"><div class="tx">{body}</div><em>{lab}</em></div>'
        return f'<div class="msg"><div class="h">{title}</div>{r}</div>'
    rq = blk("요청 · 클라이언트 → 서버", [
        ("s", "시작 줄 · 방식 · 주소", ["GET /rest/v1/tasks?select=* HTTP/1.1"]),
        ("h", "헤더 · 받는 곳 · 키 · 형식", ["Host: 프로젝트ID.supabase.co", "apikey: sb_publishable_…", "Accept: application/json"]),
        ("b", "빈 줄 뒤 본문 · GET 은 없음", [""])], .3)
    rs = blk("응답 · 서버 → 클라이언트", [
        ("s", "시작 줄 · 상태 코드", ["HTTP/1.1 200 OK"]),
        ("h", "헤더 · 본문 형식", ["Content-Type: application/json"]),
        ("b", "본문 · JSON", ['[{ "id": 41, "title": "주간 보고서 작성", … }]'])], 2.0)
    return f'<div class="v21msg">{rq}{rs}</div>'


def slides():
    return [
        light("웹 앱의 3요소", three()
              + note("2부", "서버 · DB 는 Supabase · 클라이언트는 팀 보드 화면"), T),
        # ── HTTP
        light("HTTP 메시지", message()
              + note("직접 보기", "F12 → Network → 새로고침 · 요청 줄을 눌러 Headers · Response")
              + src(MDN_MSG, NETP), T),
        light("HTTP 특징", viz2.tiles([
            ("요청 → 응답", "클라이언트가 먼저 요청 · 서버는 답만"), ("한 번에 하나", "요청 하나에 응답 하나"),
            ("기억하지 않음", "요청마다 따로 · 로그인 정보를 매번 헤더에"), ("HTTPS", "내용 암호화 · 주소창 자물쇠")], 4)
              + note("HTTP", "클라이언트와 서버가 주고받는 글의 형식 · 웹의 기본 약속")
              + src(MDN_HTTP), T),
        light("요청 방식과 상태 코드", viz2.pair(
            "방식", [("GET", "가져오기 · 보드 보기"), ("POST", "새로 만들기 · 할 일 추가"),
                    ("PATCH", "고치기 · 상태 변경"), ("DELETE", "지우기 · 할 일 삭제")],
            "상태 코드", [("200 · 201", "성공 · 만듦"), ("401 · 403", "로그인 필요 · 권한 없음"),
                       ("404", "주소 · 행 없음"), ("500", "서버 안의 오류")], hl="")
              + note("에러를 전할 때", "방식 · 주소 · 상태 코드 세 가지를 같이")
              + src(MDN_M, MDN_S), T),
        # ── API
        light("API", counter()
              + note("API", "서버가 정해 둔 요청 창구 · HTTP 로 형식대로 요청하면 응답 · 외부 API 도 같은 구조 (2-5)"), T),
        # ── 장면
        light("요청과 응답", reqres()
              + steps([("①", "화면이 데이터 요청", 1.0), ("②", "서버가 SQL 로 DB 조회", 2.1), ("③", "DB 가 행 3개 돌려줌", 2.6),
                       ("④", "서버가 JSON 으로 응답", 4.5), ("⑤", "받은 데이터로 화면 그림", 5.8)])
              + src(SB_API, NETP), T),
        light("쓰기 요청", reqres(write=True)
              + steps([("①", "「추가」 클릭 · POST", 1.0), ("②", "서버가 insert", 2.1), ("③", "DB 에 새 행", 2.6),
                       ("④", "201 · 만든 행 응답", 4.5), ("⑤", "목록에 한 줄 추가", 5.8)])
              + src(SB_API, MDN_M), T),
    ]
