"""2-7 품질 관리 · 테스트 · 디버깅 (35분).

SDLC 청사진(1부 · 2부 단원 위치) → 배경(직접 클릭 확인의 한계) → 비유(출고 전 검수 · 생성 그림) → 테스트 · 실행 결과(node --test 실측)
→ AI 에게 테스트 맡기기 · 브라우저 MCP → 에러 메시지 읽기(node 실측) · 자주 보는 에러 · 디버깅 흐름 → AI 코드 리뷰 · 보안 점검 → 실습.
공통 예제: 팀 회의실 예약 v2 (예약 겹침 · 공휴일 차단 · 남의 예약 삭제 불가).
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

T = "2-7"
ZIMG = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def sdlc():
    """SDLC 여섯 단계 + 단계마다 1부 · 2부 단원 · 테스트 칸 강조."""
    steps = [("기획", "1-3 · 2-4"), ("설계", "1-4 PRD · 2-4"), ("구현", "1-6 · 2-5 · 2-6"),
             ("테스트", "2-7"), ("배포", "1-7 · 2-8"), ("운영", "2-8 · 2-9")]
    cells = "".join(f'<div class="v2u7s{" on" if i == 3 else ""}" style="--d:{i * .15:.2f}s"><b>{h}</b><span>{u}</span></div>'
                    for i, (h, u) in enumerate(steps))
    return (f'<div class="v2u7sd">{cells}<div class="v2u7back">운영 중 버그 → 다시 구현 · 테스트</div></div>')


def testrun():
    """테스트 실행 애니메이션 — 1차 실행(ok · ok · not ok) → 수정 → 2차 실행(모두 ok). node --test TAP 실측 출력."""
    t1 = [("ok", "ok 1 - 14:00~15:00 과 14:30~15:30 은 겹친다"), ("ok", "ok 2 - 14:00~15:00 과 16:00~17:00 은 겹치지 않는다"),
          ("ng", "not ok 3 - 15:00 에 끝난 뒤 15:00 시작은 겹치지 않는다"), ("ng", "  error: 'true == false'"), ("", "# pass 2 · # fail 1")]
    t2 = [("ok", "ok 1 - 14:00~15:00 과 14:30~15:30 은 겹친다"), ("ok", "ok 2 - 14:00~15:00 과 16:00~17:00 은 겹치지 않는다"),
          ("ok", "ok 3 - 15:00 에 끝난 뒤 15:00 시작은 겹치지 않는다"), ("", "# pass 3 · # fail 0")]
    def term(head, lines, d0):
        r = "".join(f'<div class="l {c}" style="--d:{d0 + i * .45:.2f}s">{esc(x)}</div>' for i, (c, x) in enumerate(lines))
        return f'<div class="v2u7term"><div class="h">{head}</div>{r}</div>'
    return ('<div class="v2u7run">' + term("1차 실행 · node --test", t1, .3)
            + '<div class="v2u7fix" style="--d:2.9s"><b>수정</b><span>시간 비교 「&lt;=」 → 「&lt;」</span></div>'
            + term("2차 실행", t2, 3.6) + '</div>')


def stepflow(steps, cls="v2u7sf"):
    """단계가 차례로 켜지는 흐름 — 한 번 재생 후 마지막 단계까지 켜진 채 멈춤."""
    c = "".join(f'<div class="st" style="--d:{.4 + i * .8:.2f}s"><b>{h}</b><span>{x}</span></div>' for i, (h, x) in enumerate(steps))
    return f'<div class="{cls}">{c}</div>'


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
            "2부 앱", [("확인할 기능", "예약 · 로그인 · 공휴일 · 권한 · 입력값"), ("사용자", "로그인한 팀원 여럿"),
                     ("확인 방법", "고칠 때마다 전부 다시 · 빠뜨리기 쉬움")])
              + note("테스트", "확인 순서를 파일로 남겨 매번 같은 검사를 자동으로"), T),
        light("출고 전 검수 비유", phmap(
            "v2_u7_check.webp", "출고 전 검수", *ZIMG,
            viz2.maprows([
                ("검수 항목표", "테스트 목록", "PRD 완료 기준"), ("매번 같은 검사", "자동 실행", "명령 한 줄 · 몇 초"),
                ("불량 표시", "실패한 테스트", "어느 기능 · 어떤 입력"), ("검수 통과 → 출고", "테스트 통과 → 배포", "push 전 확인")],
                "검수", "테스트")), T),
        # ── 테스트
        light("예제 앱 기준 테스트", viz2.maprows([
            ("대회의실 14:00~15:00 예약 뒤 14:30~15:30 예약", "저장 안 됨", "「이미 예약된 시간」"),
            ("2026-12-25 예약", "막힘", "「공휴일」 표시"),
            ("다른 사람의 예약 삭제", "거부", "내 예약만 삭제"),
            ("로그인 없이 예약", "로그인 화면", "예약 창 안 열림")], "입력 · 행동", "기대 결과")
              + note("테스트 한 개", "정해 둔 입력 → 기대 결과와 비교 → 통과 · 실패"), T),
        light("테스트 종류", viz2.pair(
            "단위 테스트", [("검사 대상", "함수 하나 · 예: 시간 겹침 판단"), ("속도", "수백 개도 몇 초"), ("못 잡는 것", "화면 · 로그인 · DB 연결")],
            "화면 테스트 (E2E)", [("검사 대상", "브라우저에서 클릭 · 입력 전체 흐름"), ("속도", "한 개에 수 초 ~ 수십 초"),
                              ("잡는 것", "버튼 · 화면 문구 · 로그인 흐름")], hl="r")
              + note("E2E", "End to End · 사용자의 처음부터 끝까지"), T),
        light("테스트 실행 결과 예", testrun()
              + note("읽는 법", "ok = 통과 · not ok = 실패 · 「true == false」 = 실제 true · 기대 false"), T),
        light("AI 에게 테스트 맡기기", chat([
            ("me", "PRD 완료 기준으로 테스트를 만들고 실행해 줘. 실패하면 고치기 전에 원인부터 알려 줘"),
            ("ai", "테스트 6개 작성 · 5개 통과 · 1개 실패.\n15:00 에 끝난 예약 뒤 15:00 시작 예약이 막힘 — 시간 비교에 「<=」 사용. 고칠까요?"),
            ("me", "응. 고친 뒤 테스트 전체 다시 실행해 줘"),
            ("ai", "수정 · 테스트 6개 모두 통과")], "Claude Code 대화 예")
              + viz2.tiles([("기대 결과", "사람 · PRD 완료 기준"), ("테스트 코드 · 실행", "Claude Code"),
                            ("금지", "통과시키려고 기대 결과 바꾸기")], 3), T),
        light("Playwright 브라우저 MCP", viz2.tiles([
            ("주소 열기", "localhost · 배포 주소"), ("클릭 · 입력", "예약 칸 · 로그인 칸"),
            ("화면 구조 읽기", "버튼 · 문구 확인"), ("콘솔 메시지 읽기", "브라우저 에러 확인")], 4)
              + code("연결 명령 · 한 번만", esc("claude mcp add playwright npx @playwright/mcp@latest"))
              + note("MCP", "Claude Code 에 브라우저 조작 도구를 붙이는 연결 (2-6)")
              + src(("Playwright MCP · Microsoft", "https://github.com/microsoft/playwright-mcp")), T),
        light("화면 테스트 요청 예", chat([
            ("me", "브라우저를 열어서 PRD 완료 기준을 하나씩 눌러 확인해 줘"),
            ("ai", "localhost:3000 열기 → 로그인\n대회의실 14:00 예약 ○\n같은 칸 14:30 예약 → 「이미 예약된 시간」 ○\n12-25 선택 → 「공휴일」 · 예약 막힘 ○\n다른 사람 예약 → 삭제 버튼 없음 ○\n콘솔 에러 0건")], "Claude Code · 브라우저 MCP 대화 예")
              + note("확인 결과", "완료 기준마다 통과 · 실패 · 콘솔 에러 수"), T),
        # ── 디버깅
        light("에러 메시지 읽는 법", codemap([
            ("TypeError", "종류 · 값의 종류가 맞지 않음"),
            ("Cannot read properties of undefined", "내용 · 비어 있는 값(undefined)을 읽으려 함"),
            ("(reading 'filter')", "읽으려던 것 · filter"),
            ("at render (app.js:3:19)", "위치 · app.js 3번째 줄 · render 함수"),
        ], title="에러 메시지 · node app.js 실행 결과")
              + note("읽는 순서", "종류 → 내용 → 위치 · 첫 줄과 첫 「at」 줄이 핵심"), T),
        light("자주 보는 에러", viz2.maprows([
            ("404 Not Found", "주소 · 파일 경로 틀림", "요청한 것이 없음"),
            ("401 Unauthorized", "로그인 · 키 없음", "누구인지 확인 실패"),
            ("500 Internal Server Error", "서버 함수 안의 오류", "Vercel 로그 확인 (2-8)"),
            ("new row violates row-level security policy", "Supabase 권한 규칙(RLS)에 막힘", "권한 설정 확인 (2-5)")], "에러 문구", "뜻")
              + src(("MDN · HTTP 상태 코드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status"),
                    ("Supabase · Row Level Security", "https://supabase.com/docs/guides/database/postgres/row-level-security")), T),
        light("디버깅 흐름", stepflow([
            ("재현", "같은 순서로 다시 · 언제 나는지"), ("에러 · 로그 전달", "원문 그대로 · 캡처"),
            ("수정", "원인 설명 → Claude Code 수정"), ("재테스트", "같은 순서 + 테스트 전체")])
              + viz2.tiles([("브라우저 콘솔", "F12 → Console · 화면 쪽 에러"), ("터미널", "서버 실행 창 · 테스트 결과"),
                            ("Vercel 로그", "배포 뒤 서버 함수 에러 (2-8)")], 3)
              + note("고친 뒤", "재현 순서를 테스트로 남기기 · 같은 버그 재발 방지"), T),
        ba("버그 전달 방법", T, "「예약이 안 돼」",
           "「소회의실 A · 11-20 · 14:00~15:00 저장 → 반응 없음.\n콘솔: new row violates row-level security policy」",
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
            ("권한", "RLS 켜짐 · 다른 사람 예약 수정 · 삭제 불가 (2-5)"),
            ("입력값 검증", "빈 칸 · 잘못된 시간 · 너무 긴 글 · 스크립트 차단")], 3)
              + note("점검 요청", "/security-review + 「키 노출 · 권한 · 입력값 세 가지 확인해 줘」"), T),
        light("입력값 검증 예", viz2.maprows([
            ("회의 이름 빈칸", "저장 안 됨", "「회의 이름 입력」"),
            ("시작 14:00 · 끝 13:00", "저장 안 됨", "「끝 시간이 시작보다 빠름」"),
            ("회의 이름에 &lt;script&gt; 태그", "글자 그대로 표시", "스크립트 실행 안 됨"),
            ("회의 이름 2,000자", "저장 안 됨", "100자 제한")], "입력", "기대 결과")
              + note("검증 위치", "화면 + DB 둘 다 · 화면 검사는 우회 가능"), T),
        # ── 실습
        lab("2-7", "테스트 · 디버깅 · 점검", T, "PRD 완료 기준을 테스트로 만들고, 실패를 고치고, 보안 세 가지를 점검",
            ["PRD 완료 기준으로 테스트 요청 · 실행", "실패 원인 확인 → 수정 → 다시 실행", "브라우저 MCP 로 화면 확인",
             "/code-review · /security-review", "통과 뒤 커밋 · push"],
            ["테스트 전부 통과", "키 노출 · 권한 · 입력값 확인", "고친 버그마다 커밋"], files="PRD.md v2 (2-4) · 2-6 까지의 앱"),
        brief("2-7", T,
              ["테스트 요청 · 실행", "실패 원인 듣고 수정 승인", "브라우저 MCP 연결 · 화면 확인", "리뷰 · 보안 점검", "커밋 · push"],
              [("목표", "PRD 완료 기준을 자동 테스트로"), ("범위", "예약 겹침 · 공휴일 · 권한 · 입력값"),
               ("실패 시", "원인 설명 먼저 · 수정은 승인 뒤"), ("하지 말 것", "통과시키려고 테스트 기대 결과 바꾸기")],
              ["테스트", "Playwright MCP", "/code-review", "/security-review"],
              ["테스트 결과에 not ok 0개", "브라우저 콘솔 에러 0건", "/security-review 지적 사항 처리"],
              "테스트가 계속 실패하면 「실패한 테스트 하나만 다시 실행하고 원인 설명해 줘」"),
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
"""
