"""2-8 배포 · 모니터링 (20분).

배경(배포 뒤 키 없음 → 동작 안 함) → 환경변수 등록 · Config/Secret → 모니터링 배경 → 비유(가게 운영 · 생성 그림 · 1-7 「가게 문 열기」의 다음)
→ Vercel 로그 · 로그 남기기 → Web Analytics · Hobby 범위 → 문제 대응 흐름(2-7 디버깅 + push 재배포) · 되돌리기 → 실습.
GitHub–Vercel 연결은 1-7 그대로. .env · .gitignore 개념은 2-6 에서 설명 — 여기서는 다시 설명하지 않는다.
사실 출처: vercel.com/docs/environment-variables (새 배포부터 적용 · Config/Secret · Import .env) · vercel.com/docs/logs/runtime (Hobby 1시간 보관 · 4xx 경고 · 5xx 에러)
· vercel.com/docs/analytics/quickstart · vercel.com/docs/analytics/limits-and-pricing (Hobby 월 5만 이벤트 · 보고 기간 1개월 · 초과 시 수집 중지)
· vercel.com/docs/instant-rollback (Hobby 는 바로 이전 배포로만)
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v2kit import brief, chat
from v3kit import phmap

T = "2-8"
ZIMG = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
ENV_DOC = ("Vercel · Environment variables", "https://vercel.com/docs/environment-variables")


def envmove():
    """키 이동 애니메이션 — ① .env 키가 GitHub 에서 막힘(.gitignore) → Vercel 키 없음 · 500
    ② 같은 키를 Vercel 환경변수에 등록 → Redeploy → 200 · 공휴일 표시. 한 번 재생 후 멈춤."""
    def row(cls, label, mid, end_bad, end_ok):
        return (f'<div class="v2u8row {cls}"><span class="lb">{label}</span>'
                '<div class="bx a"><b>내 컴퓨터</b><small>.env · 키 3개</small></div>'
                f'<div class="bx m"><b>{mid[0]}</b><small>{mid[1]}</small></div>'
                f'<div class="bx z"><b>Vercel 배포</b><small class="bad">{end_bad}</small><small class="okk">{end_ok}</small></div>'
                '<i class="key">키</i><i class="x">✕</i></div>')
    return ('<div class="v2u8mv">'
            + row("r1", "등록 전", ("GitHub", ".gitignore → .env 제외"), "키 없음 · 500", "")
            + row("r2", "등록 후", ("Environment Variables", "Vercel 설정에 직접 입력"), "", "Redeploy · 200 · 공휴일 표시")
            + '</div>')


def logstream():
    """로그가 한 줄씩 쌓이는 화면 — 500 줄은 빨강 · 4xx 는 노랑. 값은 예."""
    rows = [("", "11:41:52", "GET", "/", "200", ""), ("", "11:41:53", "GET", "/api/bookings", "200", ""),
            ("err", "11:42:10", "GET", "/api/holidays", "500", "Error: HOLIDAY_API_KEY is not set"),
            ("warn", "11:42:18", "POST", "/api/bookings", "401", "로그인 없음"), ("", "11:42:31", "GET", "/", "200", "")]
    r = "".join(f'<div class="ln {c}" style="--d:{.4 + i * .6:.2f}s"><span>{t}</span><span>{m}</span><span>{u}</span><b>{st}</b><em>{x}</em></div>'
                for i, (c, t, m, u, st, x) in enumerate(rows))
    return f'<div class="v2u8log"><div class="hd"><span>시간 (UTC)</span><span>방식</span><span>주소</span><b>상태</b><em>메시지</em></div>{r}</div>'


def stepflow(steps):
    c = "".join(f'<div class="st" style="--d:{.4 + i * .7:.2f}s"><b>{h}</b><span>{x}</span></div>' for i, (h, x) in enumerate(steps))
    return f'<div class="v2u8sf">{c}</div>'


def slides():
    return [
        # ── 환경변수
        light("배포 뒤 오류 원인", envmove()
              + note("환경변수 등록", "키를 Vercel 프로젝트 설정에 따로 입력 · .env 는 GitHub 에 올리지 않음 (2-6)"), T),
        light("Vercel 환경변수 등록", flow([
            ("Vercel 프로젝트", "1-7 에서 만든 것"), ("Settings", "Environment Variables"), ("Key · Value", ".env 한 줄씩 · Import .env 가능"),
            ("환경 선택", "Production · Preview"), ("Redeploy", "새 배포부터 적용")], hl=4)
              + viz2.tiles([("Config", "저장 뒤 값 확인 가능 · Supabase 주소 · 공개 키"),
                            ("Secret", "쓰기 전용 · 공휴일 API 키 · Supabase secret 키"),
                            ("적용 시점", "새 배포부터 · 등록 · 수정 뒤 Redeploy")], 3)
              + src(ENV_DOC), T),
        # ── 모니터링
        light("모니터링", viz2.pair(
            "1부 방식", [("에러를 아는 때", "사용자가 단톡방에 제보"), ("방문 수", "모름"), ("원인 찾기", "제보 내용 추측")],
            "모니터링", [("에러를 아는 때", "로그에 빨간 줄 · 바로"), ("방문 수", "날짜별 그래프"), ("원인 찾기", "요청 · 상태 코드 · 에러 원문")])
              + note("모니터링", "배포한 뒤에도 서비스가 잘 돌아가는지 지켜보는 일"), T),
        light("가게 운영", phmap(
            "v2_u8_shop.webp", "가게 운영 · 손님 수 · 고장 신고", *ZIMG,
            viz2.maprows([
                ("가게 문 열기 (1-7)", "배포", "주소로 누구나"), ("손님 수 세기", "Web Analytics", "방문자 · 페이지 뷰"),
                ("영업 일지", "로그", "요청마다 시간 · 주소 · 결과"), ("고장 신고벨", "5xx 에러 표시", "빨간 줄")], "가게", "서비스")), T),
        light("Vercel 로그", viz2.tiles([
            ("위치", "프로젝트 → Logs"), ("한 줄", "시간 · 주소 · 상태 코드 · console 출력"),
            ("색", "4xx 경고 (노랑) · 5xx 에러 (빨강)"), ("보관", "Hobby 1시간 · Pro 1일")], 4)
              + logstream()
              + note("Live", "실시간 보기 · 배포 직후 직접 눌러 보며 확인 · 로그 화면은 예")
              + src(("Vercel · Runtime Logs", "https://vercel.com/docs/logs/runtime")), T),
        light("로그 남기기", chat([
            ("me", "공휴일 API 호출이 실패하면 원인을 Vercel 로그에 남겨 줘. 키 값은 로그에 쓰지 마"),
            ("ai", "api/holidays.js 실패 지점에 console.error 추가\n· 상태 코드 · 실패한 날짜만 기록 · 키는 기록 안 함")], "Claude Code 대화 예")
              + viz2.tiles([("console.log", "로그의 일반 줄"), ("console.error", "로그의 에러 줄 · 빨강 필터에 잡힘"),
                            ("기록 금지", "키 · 비밀번호 · 개인정보")], 3), T),
        light("Web Analytics", flow([
            ("프로젝트 → Analytics", "Enable"), ("스크립트 추가", "「Vercel Web Analytics 붙여 줘」"),
            ("push", "자동 재배포"), ("방문 기록", "며칠 뒤 그래프")], hl=1)
              + viz2.tiles([("보이는 것", "방문자 · 페이지 뷰 · 유입 경로 · 국가 · 기기"),
                            ("Hobby 한도", "월 50,000 이벤트 · 보고 기간 1개월 · 초과 시 수집 중지"),
                            ("팀 예약 앱 규모", "팀원 20명 · 무료 범위 안")], 3)
              + src(("Vercel · Web Analytics quickstart", "https://vercel.com/docs/analytics/quickstart"),
                    ("Vercel · Web Analytics pricing", "https://vercel.com/docs/analytics/limits-and-pricing")), T),
        # ── 대응
        light("문제 대응 흐름", stepflow([
            ("알아차림", "로그 빨간 줄 · 제보"), ("재현", "배포 주소에서 같은 순서"), ("에러 · 로그 전달", "원문 그대로"),
            ("수정 · 테스트", "2-7 흐름"), ("push", "자동 재배포 (1-7)"), ("로그 재확인", "빨간 줄 사라짐")])
              + note("급할 때", "Instant Rollback · 바로 이전 배포로 되돌린 뒤 천천히 수정 (Hobby 는 직전 배포만)")
              + src(("Vercel · Instant Rollback", "https://vercel.com/docs/instant-rollback")), T),
        light("공휴일 표시 실패 대응", chat([
            ("me", "배포 주소에서 공휴일이 안 보여. Vercel 로그:\nGET /api/holidays 500 · Error: HOLIDAY_API_KEY is not set"),
            ("ai", "코드 문제 아님 · Vercel 환경변수에 HOLIDAY_API_KEY 없음.\nSettings → Environment Variables 에 Secret 으로 등록 → Redeploy"),
            ("me", "등록하고 Redeploy 했어"),
            ("ai", "로그 확인 · GET /api/holidays 200 · 12-25 「공휴일」 표시")], "Claude Code 대화 예")
              + note("원인 갈래", "코드 수정 → push · 설정 누락 → 환경변수 등록 · Redeploy"), T),
        # ── 실습
        lab("2-8", "환경변수 · 모니터링", T, "배포 주소에서 DB · 공휴일 API 가 동작하고, 로그 · 방문 기록이 보이게",
            ["Vercel 환경변수 등록", "Redeploy · 배포 주소 확인", "Logs 에서 요청 확인", "Web Analytics 켜기 · push",
             "일부러 낸 에러를 로그에서 찾기"],
            ["배포 주소에서 예약 · 공휴일 정상", "Logs 에 200 줄", "Analytics 방문 1건 이상"], files="2-7 까지의 앱 · .env"),
        brief("2-8", T,
              ["환경변수 등록 (Config · Secret)", "Redeploy", "Logs · Live 로 요청 확인", "Analytics 스크립트 요청 · push", "로그 남기기 요청"],
              [("목표", "배포 주소에서 2부 기능 전부 동작"), ("환경변수", ".env 의 키 전부 · 종류 구분"),
               ("로그", "실패 원인 기록 · 키는 기록 안 함"), ("하지 말 것", "키를 코드 · 채팅 · 로그에 쓰기")],
              ["Environment Variables", "Redeploy", "Logs", "Web Analytics"],
              ["배포 주소에서 로그인 · 예약 · 공휴일 정상", "Logs 에 5xx 없음", "Analytics 그래프에 방문 기록"],
              "배포 주소만 안 되면 「Vercel 로그를 붙일 테니 원인 찾아 줘」 · 환경변수 이름 오타 확인"),
    ]


CSS = """
  /* 2-8 · 키 이동 애니메이션 */
  .v2u8mv{display:flex; flex-direction:column; gap:22px; margin-bottom:18px;}
  .v2u8row{position:relative; display:grid; grid-template-columns:90px 1fr 1fr 1fr; gap:60px; align-items:center;}
  .v2u8row .lb{font-size:15px; font-weight:800; color:#6B7785;}
  .v2u8row .bx{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:14px 16px; min-height:78px;}
  .v2u8row .bx:not(.z)::after{content:"→"; position:absolute; right:-40px; top:50%; transform:translateY(-50%); color:#9AA6B5; font-weight:900;}
  .v2u8row .bx b{display:block; font-size:19px; color:#16233A;} .v2u8row .bx small{display:block; margin-top:4px; font-size:14px; color:#6B7785;}
  .v2u8row .bx small:empty{display:none;}
  .v2u8row .bad{color:#D93025!important; font-weight:800; opacity:0; animation:v2u8in .4s ease-out 1.9s forwards;}
  .v2u8row .okk{color:#1E8E3E!important; font-weight:800; opacity:0; animation:v2u8in .4s ease-out 4.6s forwards;}
  .v2u8row.r1 .z{animation:v2u8bad .4s ease-out 1.9s forwards;} .v2u8row.r2 .z{animation:v2u8good .4s ease-out 4.6s forwards;}
  .v2u8row .key{position:absolute; top:50%; left:calc(150px + (100% - 270px) / 3 - 56px); transform:translateY(-50%); font-style:normal; font-size:13px; font-weight:800; color:#fff;
                background:#F28C28; border-radius:999px; padding:5px 12px; opacity:0;}
  .v2u8row.r1 .key{animation:v2u8k1 1.6s ease-in-out .3s forwards;}
  .v2u8row.r2 .key{animation:v2u8k2 1.8s ease-in-out 2.8s forwards;}
  .v2u8row .x{position:absolute; top:50%; left:calc(150px + (100% - 270px) / 3 + 18px); transform:translateY(-50%); font-style:normal; font-size:26px; color:#D93025; font-weight:900; opacity:0;}
  .v2u8row.r1 .x{animation:v2u8in .3s ease-out 1.6s forwards; background:#fff; padding:0 4px; z-index:2;}
  @keyframes v2u8k1{0%{opacity:0} 20%{opacity:1} 75%{left:calc(150px + (100% - 270px) / 3 + 8px); opacity:1} 100%{left:calc(150px + (100% - 270px) / 3 + 8px); opacity:0}}
  @keyframes v2u8k2{0%{opacity:0} 15%{opacity:1} 100%{left:calc(100% - 64px); opacity:1}}
  @keyframes v2u8bad{to{border-color:#D93025; background:#FDECEA;}}
  @keyframes v2u8good{to{border-color:#1E8E3E; background:#E6F4EA;}}
  @keyframes v2u8in{from{opacity:0} to{opacity:1}}
  /* 2-8 · 로그가 쌓이는 화면 */
  .v2u8log{margin-top:18px; border-radius:14px; overflow:hidden; background:#16233A; font-family:var(--mono); font-variant-ligatures:none;}
  .v2u8log .hd, .v2u8log .ln{display:grid; grid-template-columns:110px 70px 170px 70px 1fr; gap:10px; padding:8px 18px; font-size:14px;}
  .v2u8log .hd{color:#9AA6B5; font-size:12px; font-weight:700; border-bottom:1px solid #2A3A55;}
  .v2u8log .hd em, .v2u8log .ln em{font-style:normal;}
  .v2u8log .ln{color:#C9D2DE; opacity:0; animation:v2u8in .35s ease-out var(--d) forwards; border-left:4px solid transparent;}
  .v2u8log .ln b{color:#7FD38C;}
  .v2u8log .ln.err{background:rgba(217,48,37,.22); border-left-color:#FF6B5E;} .v2u8log .ln.err b, .v2u8log .ln.err em{color:#FF8A80; font-weight:800;}
  .v2u8log .ln.warn{background:rgba(242,180,40,.16); border-left-color:#F2B428;} .v2u8log .ln.warn b, .v2u8log .ln.warn em{color:#F7D27A;}
  /* 2-8 · 차례로 켜지는 흐름 */
  .v2u8sf{display:grid; grid-template-columns:repeat(6,1fr); gap:22px; margin-bottom:22px;}
  .v2u8sf .st{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:16px 10px; text-align:center;
              animation:v2u8lit .5s ease-out var(--d) forwards;}
  .v2u8sf .st:not(:last-child)::after{content:"→"; position:absolute; right:-18px; top:50%; transform:translateY(-50%); color:#F28C28; font-weight:900;}
  .v2u8sf b{display:block; font-size:19px; color:#16233A;} .v2u8sf span{display:block; margin-top:6px; font-size:13px; color:#6B7785;}
  @keyframes v2u8lit{to{border-color:#F28C28; background:#FFF3E6; box-shadow:0 6px 18px rgba(242,140,40,.18);}}
  @media print{.v2u8row .key,.v2u8row .x{display:none} .v2u8row .bad,.v2u8row .okk,.v2u8log .ln{opacity:1; animation:none}}
"""
