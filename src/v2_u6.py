"""2-6 외부 서비스 연결 (API · MCP).

API 키(무엇 · 비유 출입증 · 보관 위치 · .env · .gitignore) → 공공데이터포털 특일 정보 발급 → 요청 · 응답
→ 서버 함수(키 숨기기) → 요청 예 → MCP(Claude Code가 Supabase 직접 다루기 · 연결 · 안전 설정 · 대화 예 · 캘린더 일정 → 할 일) → 실습.
API · MCP 개념은 2-3 에서 설명 — 여기서는 「발급 · 보관 · 붙이기」만.
사실 출처: data.go.kr/data/15012690/openapi.do · vercel.com/docs/functions · supabase.com/docs/guides/getting-started/mcp
· code.claude.com/docs/en/mcp
"""
import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
import v2anim
from v2anim import lane
from v2kit import brief, chat, codemap, shot

T = "2-6"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
HOLI = ("공공데이터포털 · 한국천문연구원 특일 정보", "https://www.data.go.kr/data/15012690/openapi.do")
FUNC = ("Vercel · Functions", "https://vercel.com/docs/functions")
CSS = v2anim.CSS + """
  /* 2-6 · 캘린더 일정 → 할 일 (v2c) */
  .v2c{display:grid; grid-template-columns:310px 52px 1fr 52px 330px; align-items:stretch; margin:0 0 12px;}
  .v2cW{border:1.5px solid #D0D7DE; border-radius:12px; background:#fff; overflow:hidden; display:flex; flex-direction:column;}
  .v2cH{display:flex; align-items:center; gap:8px; padding:10px 12px; background:#F6F8FA; border-bottom:1px solid #D0D7DE; font-size:16.5px; font-weight:800; color:#16233A;}
  .v2cH i{width:12px; height:12px; border-radius:3px;} .v2cH i.g{background:#1A73E8;} .v2cH i.o{background:#D97757;} .v2cH i.b{background:#3ECF8E;}
  .v2cWk{display:grid; grid-template-columns:repeat(5,1fr); flex:1;}
  .v2cD{border-right:1px solid #E3E7EC; padding:8px 4px; display:flex; flex-direction:column; align-items:center; gap:2px; min-height:270px;}
  .v2cD:last-child{border-right:0;} .v2cD span{font-size:13px; color:#6B7785;} .v2cD b{font-size:15.5px; color:#16233A; margin-bottom:10px;}
  .v2cD .ev{width:100%; box-sizing:border-box; font-size:13.5px; font-weight:700; color:#fff; background:#1A73E8; border-radius:6px; padding:10px 3px; text-align:center; word-break:keep-all; line-height:1.3;
    outline:3px solid transparent; outline-offset:2px; animation:v2cRead .4s var(--d) forwards;}
  .v2cD .ev.c1{--c:#F28C28;} .v2cD .ev.c2{--c:#8E44AD;} .v2cD .ev.c3{--c:#2E8B57;}
  .v2cChat{padding:10px 12px; display:flex; flex-direction:column; gap:8px;}
  .v2cChat .m{font-size:15.5px; border-radius:10px; padding:7px 11px; opacity:0; animation:v2cIn .35s var(--d) forwards;}
  .v2cChat .me{align-self:flex-end; background:#FFF1E0; color:#16233A; font-weight:600;}
  .v2cChat .ai{background:#EEF3FA; border:1px solid #C9D6E6; color:#16233A;}
  .v2cChat .tool{font-family:var(--mono); font-size:13.5px; color:#3A4657; background:#F4F6F9; border:1px dashed #9AA5B1;}
  .v2cChat .tool em{font-style:normal; font-weight:800; margin-right:6px;} .v2cChat .tool.l em{color:#1A73E8;} .v2cChat .tool.r em{color:#1F9D63;}
  .v2cP{align-self:center; justify-self:center; display:flex; flex-direction:column; align-items:center; gap:2px; border:2px solid #C9CFD8; border-radius:10px;
    padding:6px 4px; width:46px; background:#fff; color:#9AA5B1; animation:v2cPlug .5s var(--d) forwards;}
  .v2cP b{font-size:12px;} .v2cP span{font-size:11.5px;}
  .v2cP.l{--pc:#1A73E8;} .v2cP.r{--pc:#1F9D63;}
  .v2cT{width:100%; border-collapse:collapse; font-size:15.5px;}
  .v2cT th{text-align:left; font-size:12.5px; color:#6B7785; font-weight:700; padding:7px 10px; border-bottom:1px solid #E3E7EC;}
  .v2cT td{padding:9px 10px; border-bottom:1px solid #EEF1F4; color:#16233A;}
  .v2cT td small{margin-left:6px; font-size:11px; font-weight:800; color:#1A73E8; background:#E8F0FE; border-radius:8px; padding:1px 6px;}
  .v2cT tr.nw{opacity:0; animation:v2cRow .5s var(--d) forwards;}
  .v2cT tr.c1{--c:#F28C28;} .v2cT tr.c2{--c:#8E44AD;} .v2cT tr.c3{--c:#2E8B57;}
  @keyframes v2cIn{from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none}}
  @keyframes v2cRead{to{outline-color:var(--c)}}
  @keyframes v2cPlug{to{border-color:var(--pc); color:var(--pc); background:#fff; box-shadow:0 0 0 4px rgba(0,0,0,.04)}}
  @keyframes v2cRow{0%{opacity:0; background:transparent} 30%{opacity:1; background:#FFF8E6} 100%{opacity:1; background:transparent; box-shadow:inset 4px 0 0 var(--c)}}
  @media print{.v2cChat .m,.v2cT tr.nw{opacity:1; animation:none}}
"""
SMCP = ("Supabase · MCP", "https://supabase.com/docs/guides/getting-started/mcp")


def cal_to_tasks():
    """Google 캘린더 일정 → Claude Code(MCP 두 개) → 팀 할 일 보드. 칸은 제자리 · 읽힌 일정과 추가된 행이 같은 색으로 켜짐."""
    days = [("월", "11/30"), ("화", "12/1"), ("수", "12/2"), ("목", "12/3"), ("금", "12/4")]
    ev = {0: ("주간 회의", "c1", 1.7), 2: ("고객사 미팅", "c2", 1.9), 4: ("보고서 마감", "c3", 2.1)}
    cols = ""
    for i, (w, dt) in enumerate(days):
        e = ev.get(i)
        blk = f'<div class="ev {e[1]}" style="--d:{e[2]}s">{e[0]}</div>' if e else ""
        cols += f'<div class="v2cD"><span>{w}</span><b>{dt}</b>{blk}</div>'
    cal = ('<div class="v2cW"><div class="v2cH"><i class="g"></i>Google 캘린더 · 이번 주</div>'
           f'<div class="v2cWk">{cols}</div></div>')
    def msg(cls, html_, d):
        return f'<div class="m {cls}" style="--d:{d}s">{html_}</div>'
    cc = ('<div class="v2cW"><div class="v2cH"><i class="o"></i>Claude Code</div><div class="v2cChat">'
          + msg("me", "이번 주 캘린더 일정을 우리 할 일에 넣어 줘", .6)
          + msg("tool l", "<em>Google Calendar MCP</em> 이번 주 일정 조회", 1.3)
          + msg("ai", "일정 3건 · 날짜를 기한으로 할 일 3건 추가할까요?", 2.6)
          + msg("me", "응", 3.3)
          + msg("tool r", "<em>Supabase MCP</em> tasks 에 3행 추가", 3.8)
          + msg("ai", "완료 · 할 일 3건 추가", 5.2) + '</div></div>')
    rows = [("주간 보고서 작성", "11/27", "진행 중", "", 0), ("교육 자료 준비", "11/25", "할 일", "", 0),
            ("주간 회의", "11/30", "할 일", "c1", 4.2), ("고객사 미팅", "12/2", "할 일", "c2", 4.5), ("보고서 마감", "12/4", "할 일", "c3", 4.8)]
    tr = "".join(f'<tr class="{"nw " + c if c else ""}" style="--d:{d}s"><td>{t}{"<small>캘린더</small>" if c else ""}</td><td>{du}</td><td>{st}</td></tr>'
                 for t, du, st, c, d in rows)
    board = ('<div class="v2cW"><div class="v2cH"><i class="b"></i>팀 할 일 보드 · tasks</div>'
             f'<table class="v2cT"><thead><tr><th>할 일</th><th>기한</th><th>상태</th></tr></thead><tbody>{tr}</tbody></table></div>')
    plug = lambda side, name, d: f'<div class="v2cP {side}" style="--d:{d}s"><b>MCP</b><span>{name}</span></div>'
    return ('<div class="v2c">' + cal + plug("l", "읽기", 1.3) + cc + plug("r", "쓰기", 3.8) + board + '</div>')


def slides():
    return [
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
        light("push 와 .env", lane([("프로젝트 폴더", "app.js · .env"), ("git commit · push", ".gitignore 확인"), ("GitHub", "공개 저장소")],
                                     [(0, 1, "app.js", .4, False), (1, 2, "app.js", 1.6, True), (0, 1, ".env", 3.0, False)],
                                     [(1, ".env · 제외", "no", 4.2), (2, "키 없음", "ok", 5.0)], h=200)
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
        light("서버 함수의 키 보호", lane([("브라우저", "추가 창"), ("서버 함수", "api/holidays · Vercel"), ("공공데이터포털", "특일 정보")],
                                      [(0, 1, "12월 공휴일?", .4, False), (1, 2, "연 · 월 + 인증키", 1.8, False),
                                       (2, 1, "20261225 · 기독탄신일", 3.2, False), (1, 0, "12-25 · 기독탄신일", 4.6, True)],
                                      [(1, "인증키는 여기서만", "ok", 2.2), (0, "키 없음 · 결과만", "ok", 5.9)], h=190)
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
        # ── MCP
        light("MCP 연결 전후", viz2.pair(
            "MCP 없이", [("표 만들기", "Claude Code가 SQL 작성 → 사람이 SQL Editor 에 붙여 넣기"),
                        ("데이터 확인", "사람이 Table Editor 열어 보고 전달"), ("오류", "빨간 문구 복사 · 붙여넣기")],
            "Supabase MCP 연결", [("표 만들기", "Claude Code가 직접 실행"), ("데이터 확인", "「기한 지난 할 일 몇 건?」 질문"),
                                ("오류", "Claude Code가 직접 읽기")])
              + note("MCP", "Claude Code가 외부 서비스를 도구로 쓰는 연결 · 개념은 2-3"), T),
        light("Supabase MCP 추가", code("터미널 · 프로젝트 폴더에서", esc(
            'claude mcp add --scope project --transport http supabase \\\n  "https://mcp.supabase.com/mcp?project_ref=<프로젝트 ID>&read_only=true"'))
              + flow([("claude mcp add", "연결 추가"), ("claude /mcp", "목록에서 supabase"), ("Authenticate", "브라우저 로그인 · 조직 선택"),
                      ("연결 완료", "Claude Code 도구에 supabase")], hl=2)
              + note("직접 할 것", "브라우저 로그인은 사람이 · 비밀번호 · 토큰을 대화창에 붙여 넣지 않음")
              + src(SMCP, ("Claude Code · MCP", "https://code.claude.com/docs/en/mcp")), T),
        light("MCP 안전 설정", viz2.tiles([
            ("project_ref", "프로젝트 하나에만 연결"), ("read_only=true", "읽기만 · 표 · 행 변경 불가"),
            ("개발용 프로젝트", "실제 서비스 DB 에 연결하지 않기"), ("실행 승인", "도구 실행마다 내용 보고 허용")], 4)
              + note("표를 만들 때만", "read_only 를 잠시 빼고 연결 · 끝나면 다시 읽기 전용")
              + src(SMCP), T),
        light("MCP 동작", lane([("나", "질문"), ("Claude Code", "도구 선택"), ("Supabase MCP", "execute_sql"), ("DB", "tasks")],
                              [(0, 1, "기한 지난 할 일 몇 건?", .4, False), (1, 2, "조회 실행", 2.4, False), (2, 3, "SQL", 3.6, False),
                               (3, 2, "2", 4.8, False), (2, 1, "2", 6.0, False), (1, 0, "2건 · 박서연 1 · 최민재 1", 7.2, True)],
                              [(1, "실행 승인 · 사람", "ok", 1.8)], h=200)
              + note("화면 확인 없이", "표 구조 · 행 수 · RLS 정책을 대화로 확인"), T),
        light("캘린더 일정 → 할 일", cal_to_tasks()
              + note("준비", "Claude Code 에 Google Calendar MCP 연결 · Supabase MCP 는 쓰기 허용 · 개발용 DB")
              + src(("Claude Code · MCP", "https://code.claude.com/docs/en/mcp"), SMCP), T),
        # ── 실습
        lab("2-6", "공휴일 API · Supabase MCP", T, "내 앱 → 공휴일 차단 · 키는 서버에만 · Claude Code에 Supabase MCP",
            ["공공데이터포털 인증키 발급", ".env · .gitignore 요청", "서버 함수 · 공휴일 차단 요청", "Supabase MCP 연결", "MCP 로 할 일 수 조회"],
            ["기한 12월 25일 저장 막힘", "git status · GitHub 에 키 없음", "MCP 질문에 할 일 수 답변"],
            files="예시/개발계획.md 6 칸 (비교용)"),
        brief("2-6", T, ["인증키 발급", ".env · .gitignore", "서버 함수 · 공휴일 차단", "Supabase MCP 연결", "MCP 로 조회"],
              [("목표", "기한 공휴일 차단 · Supabase MCP"), ("입력", "개발 계획 v2 · 6 칸 · 인증키"),
               ("진행 방식", "키는 서버 함수에서만 · 태스크 하나씩"), ("하지 말 것", "키를 대화창 · 코드 · 커밋에 넣기")],
              ["환경변수", ".gitignore", "서버 함수", "MCP"],
              ["기한이 공휴일이면 경고 · 저장 막힘", ".env 가 git status 에 없음"],
              "공휴일 응답이 비면 인증키 반영 대기 · 하루 뒤 다시"),
        light("실습 2-6 확인", checks([
            (".env 가 .gitignore 에 있나", "git status 에 안 보임"), ("브라우저 개발자 도구에 키가 안 보이나", "서버 함수 경유"),
            ("기한이 공휴일이면 저장이 막히나", "12월 25일 · 1월 1일"), ("MCP 가 read_only 로 연결됐나", "변경 불가 확인")],
            "넷 다 「예」 → 커밋 · 2-7 품질 관리"), T),
    ]
