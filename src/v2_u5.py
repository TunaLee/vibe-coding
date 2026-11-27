"""2-5 외부 API · 키.

API 키(무엇 · 비유 출입증 · 보관 위치 · .env · .gitignore) → 공공데이터포털 특일 정보 발급 → 요청 · 응답
→ 서버 함수(키 숨기기 · 장면) → 요청 예 → 실습.
요청 · 응답 · API 개념은 2-1 · MCP 는 2-6.
사실 출처: data.go.kr/data/15012690/openapi.do · vercel.com/docs/functions · supabase.com/docs/guides/getting-started/mcp
· code.claude.com/docs/en/mcp
"""
import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
import v2scene
from v2kit import brief, chat, codemap, shot

T = "2-5"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
HOLI = ("공공데이터포털 · 한국천문연구원 특일 정보", "https://www.data.go.kr/data/15012690/openapi.do")
FUNC = ("Vercel · Functions", "https://vercel.com/docs/functions")
CSS = """
  /* 2-5 · push 와 .env (v26p) */
  .v26p{display:grid; grid-template-columns:1fr 220px 1fr; gap:22px; align-items:center; margin:6px 0 14px;}
  .v26p .pn{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; padding:10px 14px; display:flex; flex-direction:column; gap:7px; min-height:230px;}
  .v26p .pn .h{font-size:17px; font-weight:800; color:#16233A; margin-bottom:4px;}
  .v26p .f{display:flex; align-items:center; gap:10px; border:1px solid #E3E7EC; border-radius:8px; padding:7px 12px; background:#F6F8FA;}
  .v26p .f b{font-family:var(--mono); font-size:15px; color:#1F3A5F;} .v26p .f em{margin-left:auto; font-style:normal; font-size:12.5px; font-weight:800; border-radius:8px; padding:2px 8px;}
  .v26p .f.key em{color:#B85A00; background:#FFE3C4;}
  .v26p .f.nw{opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .f.no{opacity:0; border-style:dashed; background:#FDECEA; animation:v26in .35s var(--d) forwards;} .v26p .f.no b{text-decoration:line-through; color:#C0392B;} .v26p .f.no em{color:#C0392B;}
  .v26p .mid{display:flex; flex-direction:column; gap:16px; align-items:stretch;}
  .v26p .gi{border:2px solid #F28C28; background:#FFF8F0; border-radius:10px; padding:8px 12px; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .gi span{display:block; font-size:13px; font-weight:800; color:#E07A12;} .v26p .gi code{font-size:17px; font-weight:700;}
  .v26p .cmd{text-align:center; font-family:var(--mono); font-size:16px; font-weight:700; color:#fff; background:#1F3A5F; border-radius:10px; padding:8px; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .gh{border-color:#1F3A5F;}
  /* 2-5 · 서버 함수의 키 보호 (v26k) */
  .v26k{grid-template-columns:400px 1fr 260px 1fr 220px;}
  .v26k .warn{margin-top:8px; font-size:14px; font-weight:800; color:#C0392B; background:#FDECEA; border-radius:8px; padding:6px 10px; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26k .nk{margin-top:6px; font-size:12.5px; font-weight:800; color:#1E7B45; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26k .cl.ky{font-size:11.5px;}
  .v26k .v2sBx.db .cl{opacity:.25; animation:v2sLit .35s var(--d) forwards;}
  @keyframes v26in{from{opacity:0} to{opacity:1}}
  @media print{.v26p .f.nw,.v26p .f.no,.v26p .gi,.v26p .cmd,.v26k .warn,.v26k .nk{opacity:1; animation:none}}
"""
SMCP = ("Supabase · MCP", "https://supabase.com/docs/guides/getting-started/mcp")


def push_scene():
    """push 와 .env — 내 폴더 파일 4개 · .gitignore · GitHub 저장소. 저장소에 파일이 하나씩 생기고 .env 자리는 「없음」."""
    loc = [("app.js", ""), ("api/holidays.js", ""), (".gitignore", ""), (".env", "key")]
    lf = "".join(f'<div class="f {k}"><b>{n}</b>{"<em>키</em>" if k else ""}</div>' for n, k in loc)
    gh = [("app.js", 1.6), ("api/holidays.js", 1.9), (".gitignore", 2.2)]
    rf = "".join(f'<div class="f nw" style="--d:{d}s"><b>{n}</b></div>' for n, d in gh)
    rf += '<div class="f no" style="--d:2.8s"><b>.env</b><em>없음 · 제외됨</em></div>'
    return ('<div class="v26p"><div class="pn"><div class="h">내 컴퓨터 · 프로젝트 폴더</div>' + lf + '</div>'
            '<div class="mid"><div class="gi" style="--d:.6s"><span>.gitignore</span><code>.env</code></div>'
            '<div class="cmd" style="--d:1.2s">git push</div></div>'
            '<div class="pn gh"><div class="h">GitHub 저장소</div>' + rf + '</div></div>')


def key_scene():
    """서버 함수의 키 보호 — 브라우저(키 없는 요청) · 서버 함수(키를 붙여 요청) · 공공데이터포털. 칸은 제자리."""
    br = ('<div class="v2sBr"><div class="bar"><i></i><i></i><i></i><span>team-board.vercel.app</span></div>'
          '<div class="app"><div class="ah">할 일 추가</div><div class="add"><span class="in">기한 · 2026-12-25</span><span class="bt" style="--d:.5s">저장</span></div>'
          '<div class="warn" style="--d:5.0s">공휴일 · 기독탄신일 · 저장 안 됨</div></div>'
          '<div class="net"><div class="nh"><b>Network</b><span>Name</span><span>Method</span><span>Status</span></div>'
          '<div class="nr" style="--d:.9s"><span class="fn">holidays?year=2026&amp;month=12</span><span>GET</span>'
          '<span class="st"><i class="pd" style="--d:4.3s">(pending)</i><b class="ok" style="--d:4.3s">200 OK</b></span></div>'
          '<div class="nk" style="--d:4.6s">요청 · 응답 어디에도 키 없음</div></div></div>')
    fn = ('<div class="v2sBx srv"><div class="bh"><b>서버 함수</b><small>api/holidays.js · Vercel</small></div>'
          '<div class="cl" style="--d:1.6s">GET /api/holidays</div>'
          '<div class="cl ky" style="--d:2.1s">ServiceKey = process.env.HOLIDAY_API_KEY</div>'
          '<div class="cl" style="--d:3.8s">공휴일만 골라 전달</div></div>')
    gov = ('<div class="v2sBx db"><div class="bh"><b>공공데이터포털</b><small>특일 정보</small></div>'
           '<div class="cl" style="--d:2.6s">getRestDeInfo · 2026 · 12</div>'
           '<div class="cl" style="--d:3.1s">20261225 · 기독탄신일 · Y</div></div>')
    return ('<div class="v2s v26k">' + br + v2scene.wire("① 연 · 월만", "④ 공휴일 목록", .9, 3.8) + fn
            + v2scene.wire("② 연 · 월 + 키", "③ 응답", 2.1, 3.1) + gov + '</div>')


def slides():
    return [
        light("앱이 모르는 정보", viz2.pair(
            "공휴일을 직접 입력", [("목록", "해마다 사람이 입력"), ("대체공휴일 · 임시공휴일", "발표 뒤 다시 수정"), ("틀리면", "공휴일이 기한으로 들어감")],
            "가진 곳에 묻기 · 외부 API", [("목록", "한국천문연구원 특일 정보"), ("갱신", "제공하는 쪽이 관리"), ("앱이 할 일", "연도 · 월을 보내고 답 받기")])
              + note("외부 API", "다른 회사 · 기관 서버가 열어 둔 창구 · 요청 · 응답은 2-1 과 같음"), T),
        # ── API 키
        light("API 키", viz2.tiles([
            ("API 키", "서비스가 호출한 사람을 알아보는 비밀 문자열"), ("노출되면", "남이 내 이름으로 호출 · 한도 소진 · 요금"),
            ("보관", ".env 파일 · 서버에서만 읽기")], 3)
              + code("모양 · 예 (가짜 값)", esc("HOLIDAY_API_KEY=a1b2c3d4e5f6...")), T),
        light("출입증 비유", shot("v2_u6_key.webp", "출입증 · 잠긴 서랍에 보관", [
            ("출입증", "API 키"), ("출입문", "외부 서비스"), ("잠긴 서랍", ".env · 서버"), ("게시판에 붙인 출입증", "코드 · GitHub 에 적은 키")])
              + src(GEN), T),
        light("키를 두는 곳", viz2.pair(
            "코드에 직접", [("위치", "app.js 안 문자열"), ("GitHub 에 올리면", "누구나 검색 · 복사"), ("키 교체", "코드 수정 · 다시 커밋")],
            ".env 파일", [("위치", "프로젝트 폴더의 .env"), ("GitHub 에 올리면", ".gitignore 로 제외 · 안 올라감"), ("키 교체", ".env 한 줄")])
              + note("환경변수", "코드 밖에 둔 설정 값 · 코드는 이름으로만 읽음"), T),
        light(".env · .gitignore", codemap([
            (".env", "비밀 값을 적는 파일"),
            ("HOLIDAY_API_KEY=발급받은_키", "이름 = 값 · 한 줄에 하나"),
            (".gitignore", "Git 이 무시할 파일 목록"),
            (".env", "이 줄 하나 · .env 는 커밋 · push 제외"),
            ("process.env.HOLIDAY_API_KEY", "코드에서 이름으로 값 읽기")],
            ask="공휴일 API 키를 .env 에 두고 .gitignore 에 추가해 줘", title="파일 · 코드 · 예")
              + note("확인", "git status 에 .env 가 안 보이면 정상"), T),
        light("push 와 .env", push_scene()
              + note(".gitignore", "목록에 있는 파일은 커밋 · push 에서 빠짐 · 키는 내 컴퓨터에만"), T),
        # ── 공휴일 API
        light("공휴일 API 발급", flow([("공공데이터포털", "data.go.kr · 회원가입"), ("검색", "「한국천문연구원 특일 정보」"),
                                     ("활용신청", "목적 한 줄 · 개발계정"), ("인증키 확인", "마이페이지 · 인증키"), (".env", "HOLIDAY_API_KEY")], hl=3)
              + note("비용", "무료 · 인증키 반영까지 시간이 걸릴 수 있음")
              + src(HOLI), T),
        light("공휴일 API 요청 · 응답", codemap([
            ("SpcdeInfoService · 공휴일 정보 조회", "한국천문연구원 특일 정보 · 공휴일"),
            ("solYear=2026 · solMonth=12", "보낼 값 · 연 · 월"),
            ("ServiceKey=…", "인증키 · .env 의 값"),
            ("locdate 20261225", "받는 값 · 날짜"),
            ("dateName 기독탄신일", "공휴일 이름"),
            ("isHoliday Y", "공공기관 휴일 여부")],
            title="요청 · 응답 · 예")
              + note("쓰는 곳", "기한으로 고른 날이 공휴일이면 「공휴일 · 이름」 경고 · 저장 막기")
              + src(HOLI), T),
        # ── 서버 함수
        light("키 노출 경로", viz2.pair(
            "브라우저 → 공공데이터포털", [("키 위치", "앱 코드 · 브라우저에 내려감"), ("보이는 곳", "개발자 도구 · 네트워크 탭"),
                                      ("결과", "누구나 키 복사")],
            "브라우저 → 서버 함수 → 공공데이터포털", [("키 위치", "Vercel 서버 · 환경변수"), ("보이는 곳", "없음 · 결과만 내려감"),
                                              ("결과", "키 노출 없음")]), T),
        light("서버 함수의 키 보호", key_scene()
              + codemap([("api/holidays.js", "Vercel 이 서버에서 실행하는 파일"),
                         ("export function GET(request)", "주소로 요청이 오면 실행"),
                         ("process.env.HOLIDAY_API_KEY", "키는 서버 안에서만 읽기")])
              + src(FUNC), T),
        light("공휴일 차단 대화 예시", chat([
            ("me", "기한이 공휴일이면 저장을 막아 줘. 공휴일은 공공데이터포털 특일 정보 API 에서 받고, 키는 서버 함수에서만 읽게 해 줘"),
            ("ai", "계획 · api/holidays.js 생성 → 추가 창에서 호출. 경고 문구는 「공휴일 · 기독탄신일」 형식으로 할까요?"),
            ("me", "응"),
            ("ai", "완료 · 기한 2026-12-25 선택 → 공휴일 경고 · 저장 막힘")], "Claude Code 대화 예")
              + note("확인", "기한에 12월 25일 · 1월 1일 넣고 저장"), T),
        ba("공휴일 반영 전후", T, "기한 12월 25일 → 그대로 저장\n연휴가 끝난 뒤에야 알아챔",
           "기한 12월 25일 → 「공휴일 · 기독탄신일」\n저장 막힘 · 다른 날 고르기",
           "기획서 v2 문제점 「공휴일이 기한으로 들어감」 해결"),
        # ── 실습
        lab("2-5", "공휴일 API · 키 보관", T, "내 앱 → 공휴일 차단 · 키는 서버에만",
            ["공공데이터포털 인증키 발급", ".env · .gitignore 요청", "서버 함수 · 공휴일 차단 요청", "Network 탭에서 키 확인"],
            ["기한 12월 25일 저장 막힘", "git status · GitHub 에 키 없음"],
            files="예시/개발계획.md 6 칸 (비교용)"),
        brief("2-5", T, ["인증키 발급", ".env · .gitignore", "서버 함수 · 공휴일 차단", "Network 탭 확인"],
              [("목표", "기한 공휴일 차단"), ("입력", "개발 계획 v2 · 6 칸 · 인증키"),
               ("진행 방식", "키는 서버 함수에서만 · 태스크 하나씩"), ("하지 말 것", "키를 대화창 · 코드 · 커밋에 넣기")],
              ["환경변수", ".gitignore", "서버 함수", "Network"],
              ["기한이 공휴일이면 경고 · 저장 막힘", ".env 가 git status 에 없음"],
              "공휴일 응답이 비면 인증키 반영 대기 · 하루 뒤 다시"),
        light("실습 2-5 확인", checks([
            (".env 가 .gitignore 에 있나", "git status 에 안 보임"), ("브라우저 개발자 도구에 키가 안 보이나", "서버 함수 경유"),
            ("기한이 공휴일이면 저장이 막히나", "12월 25일 · 1월 1일"), ("Network 탭 요청에 키가 없나", "holidays 요청 · 응답")],
            "넷 다 「예」 → 커밋 · 2-6 MCP"), T),
    ]
