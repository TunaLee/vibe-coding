"""2-10 품질 · 운영 (구 2-7 품질 관리 + 2-8 배포 · 모니터링).

SDLC 청사진(1부 · 2부 단원 위치) → 배경(직접 클릭 확인의 한계) → 비유(출고 전 검수 · 생성 그림) → 테스트 · 실행 결과(node --test 실측)
→ AI 에게 테스트 맡기기 · 브라우저 MCP → 에러 메시지 읽기(node 실측) · 자주 보는 에러 · 디버깅 흐름 → AI 코드 리뷰 · 보안 점검 → 실습.
공통 예제: 팀 할 일 보드 v2 (기한 지남 판정 · 공휴일 차단 · 남의 할 일 삭제 불가).
사실 출처: code.claude.com/docs/en/commands (/code-review · /review · /security-review · /diff) · github.com/microsoft/playwright-mcp
· nodejs.org test runner · developer.mozilla.org HTTP 상태 코드 · supabase.com RLS
실측: 겹침 함수 테스트(node --test · 실패 1 → 「<=」를 「<」로 고친 뒤 3개 통과) · TypeError 메시지(node app.js).
"""
import viz2
from deck import ba, flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v2kit import brief, chat, codemap
from v3kit import phmap

T = "2-10"
ENV_DOC = ("Vercel · Environment variables", "https://vercel.com/docs/environment-variables")
ZIMG = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def sdlc():
    """SDLC 여섯 단계 + 단계마다 1부 · 2부 단원 · 테스트 칸 강조."""
    steps = [("기획", "1-3 · 2-4"), ("설계", "1-4 개발 계획 · 2-4"), ("구현", "1-6 · 2-5 ~ 2-8"),
             ("테스트", "2-10"), ("배포", "1-7 · 2-8"), ("운영", "2-10 · 2-11")]
    cells = "".join(f'<div class="v2u7s{" on" if i == 3 else ""}" style="--d:{i * .15:.2f}s"><b>{h}</b><span>{u}</span></div>'
                    for i, (h, u) in enumerate(steps))
    return (f'<div class="v2u7sd">{cells}<div class="v2u7back">운영 중 버그 → 다시 구현 · 테스트</div></div>')


def testrun():
    """테스트 실행 애니메이션 — 1차 실행(ok · ok · not ok) → 수정 → 2차 실행(모두 ok). node --test TAP 실측 출력."""
    t1 = [("ok", "ok 1 - 기한 11-19 · 할 일 → 기한 지남"), ("ok", "ok 2 - 기한 11-19 · 완료 → 기한 지남 아님"),
          ("ng", "not ok 3 - 기한이 오늘 → 기한 지남 아님"), ("ng", "  error: 'true == false'"), ("", "# pass 2 · # fail 1")]
    t2 = [("ok", "ok 1 - 기한 11-19 · 할 일 → 기한 지남"), ("ok", "ok 2 - 기한 11-19 · 완료 → 기한 지남 아님"),
          ("ok", "ok 3 - 기한이 오늘 → 기한 지남 아님"), ("", "# pass 3 · # fail 0")]
    def term(head, lines, d0):
        r = "".join(f'<div class="l {c}" style="--d:{d0 + i * .45:.2f}s">{esc(x)}</div>' for i, (c, x) in enumerate(lines))
        return f'<div class="v2u7term"><div class="h">{head}</div>{r}</div>'
    return ('<div class="v2u7run">' + term("1차 실행 · node --test", t1, .3)
            + '<div class="v2u7fix" style="--d:2.9s"><b>수정</b><span>날짜 비교 「&lt;=」 → 「&lt;」</span></div>'
            + term("2차 실행", t2, 3.6) + '</div>')


def stepflow(steps, cls="v2u7sf"):
    """단계가 차례로 켜지는 흐름 — 한 번 재생 후 마지막 단계까지 켜진 채 멈춤."""
    c = "".join(f'<div class="st" style="--d:{.4 + i * .8:.2f}s"><b>{h}</b><span>{x}</span></div>' for i, (h, x) in enumerate(steps))
    return f'<div class="{cls}">{c}</div>'


def logstream():
    """로그가 한 줄씩 쌓이는 화면 — 500 줄은 빨강 · 4xx 는 노랑. 값은 예."""
    rows = [("", "", "GET", "/", "200", ""), ("", "", "POST", "/api/mcp", "200", "tools/call add_task"),
            ("err", "", "GET", "/api/holidays", "500", "Error: HOLIDAY_API_KEY is not set"),
            ("warn", "", "POST", "/api/mcp", "401", "토큰 없음"), ("", "", "GET", "/api/holidays", "200", "")]
    r = "".join(f'<div class="ln {c}" style="--d:{.4 + i * .6:.2f}s"><span>{t}</span><span>{m}</span><span>{u}</span><b>{st}</b><em>{x}</em></div>'
                for i, (c, t, m, u, st, x) in enumerate(rows))
    return f'<div class="v2u8log"><div class="hd"><span></span><span>방식</span><span>주소</span><b>상태</b><em>메시지</em></div>{r}</div>'


def stepflow8(steps):
    c = "".join(f'<div class="st" style="--d:{.4 + i * .7:.2f}s"><b>{h}</b><span>{x}</span></div>' for i, (h, x) in enumerate(steps))
    return f'<div class="v2u8sf">{c}</div>'


def slides():
    return [
        # ── 청사진
        light("소프트웨어 개발 생명주기 (SDLC)", sdlc()
              + viz2.tiles([("품질 관리", "단계마다 기준을 정하고 확인"), ("테스트", "기능이 기준대로 동작하는지 검사"),
                            ("디버깅", "버그의 원인을 찾아 고치기")], 3)
              + src(("AWS · What is SDLC", "https://aws.amazon.com/what-is/sdlc/")), T),
        # ── 배경 · 비유
        light("직접 클릭 확인의 한계", viz2.pair(
            "1부 앱", [("확인할 기능", "완료 기준 5개"), ("사용자", "나 혼자 · 브라우저 하나"), ("확인 방법", "직접 클릭 · 몇 분")],
            "2부 앱", [("확인할 기능", "기한 지남 · 로그인 · 공휴일 · 권한 · 입력값"), ("사용자", "로그인한 팀원 여럿"),
                     ("확인 방법", "고칠 때마다 전부 다시 · 빠뜨리기 쉬움")])
              + note("테스트", "확인 순서를 파일로 남겨 매번 같은 검사를 자동으로"), T),
        light("출고 전 검수 비유", phmap(
            "v2_u7_check.webp", "출고 전 검수", *ZIMG,
            viz2.maprows([
                ("검수 항목표", "테스트 목록", "개발 계획 완료 기준"), ("매번 같은 검사", "자동 실행", "명령 한 줄 · 몇 초"),
                ("불량 표시", "실패한 테스트", "어느 기능 · 어떤 입력"), ("검수 통과 → 출고", "테스트 통과 → 배포", "push 전 확인")],
                "검수", "테스트")), T),
        # ── 테스트
        light("예제 앱 기준 테스트", viz2.maprows([
            ("기한이 어제인 할 일 · 할 일 칸", "빨간 표시", "「기한 지남」 · 칸 맨 위"),
            ("기한 2026-12-25 로 추가", "저장 막힘", "「공휴일 · 기독탄신일」"),
            ("다른 사람이 담당인 할 일 삭제", "거부", "내가 담당인 할 일만 삭제"),
            ("로그인 없이 추가", "로그인 화면", "「+ 할 일」 안 보임")], "입력 · 행동", "기대 결과")
              + note("테스트 한 개", "정해 둔 입력 → 기대 결과와 비교 → 통과 · 실패"), T),
        light("테스트 종류", viz2.pair(
            "단위 테스트", [("검사 대상", "함수 하나 · 예: 시간 겹침 판단"), ("속도", "수백 개도 몇 초"), ("못 잡는 것", "화면 · 로그인 · DB 연결")],
            "화면 테스트 (E2E)", [("검사 대상", "브라우저에서 클릭 · 입력 전체 흐름"), ("속도", "한 개에 수 초 ~ 수십 초"),
                              ("잡는 것", "버튼 · 화면 문구 · 로그인 흐름")], hl="r")
              + note("E2E", "End to End · 사용자의 처음부터 끝까지"), T),
        light("테스트 실행 결과 예", testrun()
              + note("읽는 법", "ok = 통과 · not ok = 실패 · 「true == false」 = 실제 true · 기대 false"), T),
        light("AI 에게 테스트 맡기기", chat([
            ("me", "개발 계획 완료 기준으로 테스트를 만들고 실행해 줘. 실패하면 고치기 전에 원인부터 알려 줘"),
            ("ai", "테스트 6개 작성 · 5개 통과 · 1개 실패.\n기한이 오늘인 할 일이 「기한 지남」으로 표시됨 — 날짜 비교에 「<=」 사용. 고칠까요?"),
            ("me", "응. 고친 뒤 테스트 전체 다시 실행해 줘"),
            ("ai", "수정 · 테스트 6개 모두 통과")], "Claude Code 대화 예")
              + viz2.tiles([("기대 결과", "사람 · 개발 계획 완료 기준"), ("테스트 코드 · 실행", "Claude Code"),
                            ("금지", "통과시키려고 기대 결과 바꾸기")], 3), T),
        light("화면 테스트 요청 예", chat([
            ("me", "브라우저를 열어서 개발 계획 완료 기준을 하나씩 눌러 확인해 줘"),
            ("ai", "localhost:3000 열기 → 로그인\n주간 보고서 작성 추가 ○\n기한 어제인 할 일 → 「기한 지남」 ○\n기한 12-25 → 「공휴일」 · 저장 막힘 ○\n다른 사람 할 일 → 삭제 버튼 없음 ○\n콘솔 에러 0건")], "Claude Code · 브라우저 MCP 대화 예")
              + note("Playwright MCP (2-7)", "브라우저를 Claude Code 가 직접 열고 눌러 봄 · 완료 기준마다 통과 · 실패"), T),
        # ── 디버깅
        light("에러 메시지 읽는 법", codemap([
            ("TypeError", "종류 · 값의 종류가 맞지 않음"),
            ("Cannot read properties of undefined", "내용 · 비어 있는 값(undefined)을 읽으려 함"),
            ("(reading 'filter')", "읽으려던 것 · filter"),
            ("at render (app.js 3번째 줄)", "위치 · app.js 3번째 줄 · render 함수"),
        ], title="에러 메시지 · node app.js 실행 결과")
              + note("읽는 순서", "종류 → 내용 → 위치 · 첫 줄과 첫 「at」 줄이 핵심"), T),
        light("디버깅 흐름", stepflow([
            ("재현", "같은 순서로 다시 · 언제 나는지"), ("에러 · 로그 전달", "원문 그대로 · 캡처"),
            ("수정", "원인 설명 → Claude Code 수정"), ("재테스트", "같은 순서 + 테스트 전체")])
              + viz2.tiles([("브라우저 콘솔", "F12 → Console · 화면 쪽 에러"), ("터미널", "서버 실행 창 · 테스트 결과"),
                            ("Vercel 로그", "배포 뒤 서버 함수 · MCP 서버 에러")], 3)
              + note("고친 뒤", "재현 순서를 테스트로 남기기 · 같은 버그 재발 방지"), T),
        ba("버그 전달 방법", T, "「할 일 추가가 안 돼」",
           "「주간 보고서 작성 · 김하늘 · 11-27 저장 → 반응 없음.\n콘솔: new row violates row-level security policy」",
           "재현 순서 · 기대 결과 · 실제 결과 · 에러 원문"),
        # ── 품질 관리
        light("AI 코드 리뷰", viz2.maprows([
            ("/diff", "바뀐 곳 보기", "Claude 가 고친 파일 · 줄"),
            ("/code-review (별칭 /review)", "바뀐 코드의 버그 찾기", "--fix 로 찾은 문제 바로 고치기"),
            ("/security-review", "브랜치 변경의 보안 취약점", "GitHub 저장소(origin) 필요 · 1-7 에서 연결")], "명령", "하는 일")
              + note("시점", "push 전 · 큰 기능 하나 끝날 때마다")
              + src(("Claude Code · Commands", "https://code.claude.com/docs/en/commands")), T),
        light("보안 기본 점검", viz2.tiles([
            ("키 노출", "API 키 · secret 키가 코드 · GitHub 에 없음 · .env 는 .gitignore (2-6)"),
            ("권한", "RLS 켜짐 · 다른 사람 할 일 수정 · 삭제 불가 (2-5)"),
            ("입력값 검증", "빈 칸 · 잘못된 날짜 · 너무 긴 글 · 스크립트 차단")], 3)
              + note("점검 요청", "/security-review + 「키 노출 · 권한 · 입력값 세 가지 확인해 줘」"), T),
        light("배포 뒤 오류 원인", viz2.pair(
            "내 컴퓨터", [(".env", "키 · Supabase 주소 · 인증 설정"), ("결과", "공휴일 · MCP 서버 정상")],
            "Vercel 배포", [(".env", "없음 · GitHub 에 안 올라감 (2-6)"), ("결과", "/api/holidays · /api/mcp 500")], hl="r")
              + note("환경변수 등록", "키를 Vercel 프로젝트 설정에 따로 입력 · 등록 뒤 Redeploy"), T),
        light("Vercel 환경변수 등록", flow([
            ("Vercel 프로젝트", "1-7 에서 만든 것"), ("Settings", "Environment Variables"), ("Key · Value", ".env 한 줄씩 · Import .env 가능"),
            ("환경 선택", "Production · Preview"), ("Redeploy", "새 배포부터 적용")], hl=4)
              + viz2.tiles([("Config", "저장 뒤 값 확인 가능 · Supabase 주소 · 공개 키"),
                            ("Secret", "쓰기 전용 · 공휴일 API 키 · Supabase secret 키"),
                            ("적용 시점", "새 배포부터 · 등록 · 수정 뒤 Redeploy")], 3)
              + src(ENV_DOC), T),
        light("모니터링", viz2.pair(
            "1부 방식", [("에러를 아는 때", "사용자가 단톡방에 제보"), ("방문 수", "모름"), ("원인 찾기", "제보 내용 추측")],
            "모니터링", [("에러를 아는 때", "로그에 빨간 줄 · 바로"), ("방문 수", "날짜별 그래프"), ("원인 찾기", "요청 · 상태 코드 · 에러 원문")])
              + note("모니터링", "배포한 뒤에도 서비스가 잘 돌아가는지 지켜보는 일"), T),
        light("가게 운영 비유", phmap(
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
                            ("팀 할 일 보드 규모", "팀원 8명 · 무료 범위 안")], 3)
              + src(("Vercel · Web Analytics quickstart", "https://vercel.com/docs/analytics/quickstart"),
                    ("Vercel · Web Analytics pricing", "https://vercel.com/docs/analytics/limits-and-pricing")), T),
        # ── 대응
        light("문제 대응 흐름", stepflow8([
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
        lab("2-10", "테스트 · 운영", T, "완료 기준을 테스트로 만들고, 배포 주소의 로그로 MCP 호출까지 확인",
            ["완료 기준으로 테스트 요청 · 실행", "실패 원인 확인 → 수정", "/code-review · /security-review",
             "Vercel 환경변수 · Redeploy", "Logs 에서 /api/mcp 호출 확인"],
            ["테스트 전부 통과", "배포 주소에서 2부 기능 동작", "Logs 에 MCP 호출 줄"], files="2-9 까지의 앱"),
        brief("2-10", T,
              ["테스트 요청 · 실행", "수정 승인", "리뷰 · 보안 점검", "환경변수 · Redeploy", "로그 확인"],
              [("목표", "완료 기준 자동 테스트 · 배포 뒤 확인"), ("범위", "공휴일 · 권한 · MCP 도구"),
               ("실패 시", "원인 설명 먼저 · 수정은 승인 뒤"), ("하지 말 것", "통과시키려고 기대 결과 바꾸기 · 키를 로그에")],
              ["테스트", "/security-review", "Environment Variables", "Logs"],
              ["not ok 0개", "Logs 에 5xx 없음", "POST /api/mcp 200"],
              "배포 주소만 안 되면 「Vercel 로그를 붙일 테니 원인 찾아 줘」"),
    ]


CSS = """
  /* 2-7 · SDLC 청사진 */
  .v2u7sd{position:relative; display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin:4px 0 46px;}
  .v2u7s{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:16px 10px; text-align:center;
         opacity:0; animation:v2u7in .45s ease-out var(--d) forwards;}
  .v2u7s b{display:block; font-size:24px; color:#16233A;} .v2u7s span{display:block; margin-top:6px; font-size:14px; color:#6B7785; font-family:var(--mono);}
  .v2u7s:not(:last-of-type)::after{content:"→"; position:absolute; right:-12px; top:50%; transform:translateY(-50%); color:#F28C28; font-weight:900; font-size:16px;}
  .v2u7s.on{border-color:#F28C28; background:#FFF3E6; box-shadow:0 6px 18px rgba(242,140,40,.18);} .v2u7s.on span{color:#E07A12; font-weight:800;}
  .v2u7back{position:absolute; left:50%; right:0; bottom:-36px; border:2px dashed #F7C99A; border-top:none; border-radius:0 0 14px 14px;
            height:24px; font-size:13px; color:#E07A12; font-weight:700; text-align:center; padding-top:6px;}
  /* 2-7 · 테스트 실행 애니메이션 */
  .v2u7run{display:grid; grid-template-columns:1fr 150px 1fr; gap:16px; align-items:stretch;}
  .v2u7term{background:#16233A; border-radius:14px; padding:14px 16px; min-height:250px; font-family:var(--mono); font-variant-ligatures:none; font-feature-settings:'liga' 0, 'calt' 0;}
  .v2u7term .h{font-size:12px; color:#9AA6B5; font-weight:700; margin-bottom:10px;}
  .v2u7term .l{font-size:13.5px; line-height:1.55; color:#C9D2DE; white-space:pre-wrap; opacity:0; animation:v2u7in .35s ease-out var(--d) forwards;}
  .v2u7term .l.ok{color:#7FD38C;} .v2u7term .l.ng{color:#FF8A80; font-weight:700;}
  .v2u7fix{align-self:center; text-align:center; border:2px solid #F28C28; border-radius:14px; background:#FFF3E6; padding:14px 10px;
           opacity:0; animation:v2u7pop .5s ease-out var(--d) forwards;}
  .v2u7fix b{display:block; font-size:20px; color:#E07A12;} .v2u7fix span{display:block; margin-top:6px; font-size:14px; color:#16233A; font-family:var(--mono); font-variant-ligatures:none; font-feature-settings:'liga' 0, 'calt' 0;}
  /* 2-7 · 차례로 켜지는 흐름 */
  .v2u7sf{display:grid; grid-template-columns:repeat(4,1fr); gap:28px; margin-bottom:22px;}
  .v2u7sf .st{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:18px 14px; text-align:center;
              animation:v2u7lit .5s ease-out var(--d) forwards;}
  .v2u7sf .st:not(:last-child)::after{content:"→"; position:absolute; right:-22px; top:50%; transform:translateY(-50%); color:#F28C28; font-weight:900;}
  .v2u7sf b{display:block; font-size:22px; color:#16233A;} .v2u7sf span{display:block; margin-top:6px; font-size:14px; color:#6B7785;}
  @keyframes v2u7lit{to{border-color:#F28C28; background:#FFF3E6; box-shadow:0 6px 18px rgba(242,140,40,.18);}}
  @keyframes v2u7pop{from{opacity:0; transform:scale(.8)} to{opacity:1; transform:none}}
  @media print{.v2u7term .l,.v2u7fix{opacity:1; animation:none}}
  @keyframes v2u7in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u7s{opacity:1; animation:none}}

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
