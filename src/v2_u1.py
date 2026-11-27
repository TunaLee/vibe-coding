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
from hx import note
from stats_hx import src
from v2kit import codemap
import v2scene
from v2scene import reqres, steps

T = "2-1"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
SB_API = ("Supabase · REST API", "https://supabase.com/docs/guides/api")
MDN_M = ("MDN · HTTP 요청 메서드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods")
MDN_S = ("MDN · HTTP 상태 코드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status")
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


def slides():
    return [
        light("클라이언트 · 서버 · DB", viz2.maprows([
            ("클라이언트", "브라우저 · 화면", "요청을 보내고 받은 데이터로 화면을 그림"),
            ("서버", "요청을 받는 프로그램", "누가 무엇을 원하는지 확인 · DB 에 묻기"),
            ("DB", "데이터 저장소", "표에 행으로 보관 · 서버만 직접 접근")], "칸", "하는 일")
              + note("1-6 웹 구조", "같은 세 칸 · 2부는 서버 · DB 를 Supabase 가 맡음"), T),
        light("API", counter()
              + note("API", "서버가 정해 둔 요청 창구 · 형식대로 요청하면 응답 · 외부 API 도 같은 구조 (2-5)"), T),
        light("요청과 응답", reqres()
              + steps([("①", "화면이 데이터 요청", 1.0), ("②", "서버가 SQL 로 DB 조회", 2.1), ("③", "DB 가 행 3개 돌려줌", 2.6),
                       ("④", "서버가 JSON 으로 응답", 4.5), ("⑤", "받은 데이터로 화면 그림", 5.8)])
              + src(SB_API, NETP), T),
        light("요청과 응답 읽기", codemap([
            ("GET", "방식 · 가져오기"),
            ("/rest/v1/tasks?select=*", "주소 · tasks 표의 모든 열"),
            ("200 OK", "상태 · 성공"),
            ('[{ "id": 41, "title": "주간 보고서 작성", … }]', "내용 · JSON · 할 일 한 건이 { } 하나"),
        ], title="Network 탭의 요청 한 줄")
              + note("직접 보기", "F12 → Network → 새로고침 · 요청 줄을 눌러 Response")
              + src(MDN_M, NETP), T),
        light("쓰기 요청", reqres(write=True)
              + steps([("①", "「추가」 클릭 · POST", 1.0), ("②", "서버가 insert", 2.1), ("③", "DB 에 새 행", 2.6),
                       ("④", "201 · 만든 행 응답", 4.5), ("⑤", "목록에 한 줄 추가", 5.8)])
              + src(SB_API, MDN_M), T),
        light("요청 방식과 상태 코드", viz2.pair(
            "방식", [("GET", "가져오기 · 보드 보기"), ("POST", "새로 만들기 · 할 일 추가"),
                    ("PATCH", "고치기 · 상태 변경"), ("DELETE", "지우기 · 할 일 삭제")],
            "상태 코드", [("200 · 201", "성공 · 만듦"), ("401 · 403", "로그인 필요 · 권한 없음"),
                       ("404", "주소 · 행 없음"), ("500", "서버 안의 오류")], hl="")
              + note("에러를 전할 때", "방식 · 주소 · 상태 코드 세 가지를 같이")
              + src(MDN_M, MDN_S), T),
    ]
