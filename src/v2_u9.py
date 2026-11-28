"""2-9 웹 점검 · E2E 테스트.

배경(직접 클릭 확인의 한계) → Playwright MCP(브라우저를 Claude Code 가 직접 조작) → 실습 ① 웹 점검 요청
→ E2E 테스트(단위 테스트와 차이) → 실습 ② E2E 테스트 만들기 · 실행 요청 → 확인.
요청은 개념 수준으로 짧게 · 방법은 Claude Code 가 정한다.
사실 출처: github.com/microsoft/playwright-mcp (claude mcp add playwright npx @playwright/mcp@latest · 「보안 경계가 아님」)
· playwright.dev (Playwright Test · E2E)
"""
import viz2
from deck import lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import tstep

T = "2-9"
PWMCP = ("Playwright MCP · Microsoft", "https://github.com/microsoft/playwright-mcp")
PWT = ("Playwright · Writing tests", "https://playwright.dev/docs/writing-tests")

CSS = ""


def slides():
    return [
        light("직접 클릭 확인의 한계", viz2.pair(
            "1부 앱", [("확인할 기능", "완료 기준 몇 개"), ("사용자", "나 혼자 · 브라우저 하나"), ("확인 방법", "직접 클릭 · 몇 분")],
            "2부 앱", [("확인할 기능", "로그인 · 권한 · 페이지 CRUD · MCP"), ("사용자", "로그인한 팀원 여럿"),
                     ("확인 방법", "고칠 때마다 전부 다시 · 빠뜨리기 쉬움")], hl="r")
              + note("2-9", "브라우저 점검과 반복 검사를 Claude Code 에 맡기기"), T),
        light("Playwright MCP", viz2.tiles([
            ("주소 열기", "localhost · 배포 주소"), ("클릭 · 입력", "로그인 · 「+ 새 페이지」"),
            ("화면 읽기", "버튼 · 문구 · 깨진 곳"), ("콘솔 읽기", "브라우저 에러")], 4)
              + code("연결 · 한 번만 (Claude Code 가 실행)", esc("claude mcp add playwright npx @playwright/mcp@latest"))
              + note("주의", "믿을 수 있는 사이트만 · 공식 문서 「보안 경계가 아님」")
              + src(PWMCP), T),
        # ── 실습 ① 웹 점검
        tstep("2-9", 1, "Playwright 연결", T, ask=("Claude Code 입력창", "Playwright MCP 연결해 줘"),
              rows=[("확인", "/mcp 에 playwright"), ("승인", "패널에 뜬 명령 확인 → 허용"), ("다음", "웹 점검 요청")]),
        tstep("2-9", 2, "웹 점검", T, ask=("Claude Code 입력창", "Playwright 로 배포 주소를 열어\n완료 기준대로 눌러 보고 문제를 알려 줘"),
              rows=[("Claude Code 가 하는 일", "브라우저 열기 · 로그인 · 클릭"), ("받을 결과", "기준마다 통과 · 실패 · 콘솔 에러"),
                    ("고치기", "원인 듣고 승인 뒤")]),
        # ── E2E
        light("E2E 테스트", viz2.pair(
            "웹 점검 (Playwright MCP)", [("누가", "Claude Code 가 그때그때 눌러 봄"), ("남는 것", "대화 속 결과"), ("다시 하려면", "다시 요청")],
            "E2E 테스트", [("누가", "테스트 파일이 정해진 순서로 실행"), ("남는 것", "tests/ 파일 · Git 커밋"), ("다시 하려면", "명령 한 줄 · 몇 초 ~ 몇 분")], hl="r")
              + note("E2E", "End to End · 로그인부터 저장까지 사용자가 하는 흐름 전체를 브라우저로 검사")
              + src(PWT), T),
        tstep("2-9", 3, "E2E 테스트 만들기", T, ask=("Claude Code 입력창", "완료 기준을 E2E 테스트로 만들고 실행해 줘.\n실패하면 고치기 전에 원인부터 알려 줘"),
              rows=[("만들어지는 것", "tests/ 아래 테스트 파일"), ("받을 결과", "통과 · 실패 수 · 실패한 기준"), ("하지 말 것", "통과시키려고 기대 결과 바꾸기")]),
        tstep("2-9", 4, "고친 뒤 다시 실행", T, ask=("Claude Code 입력창", "E2E 테스트 전체 다시 실행해 줘"),
              rows=[("통과", "전부 통과 → 커밋 · push"), ("기능 수정 뒤", "같은 요청 한 줄"), ("남는 것", "테스트 파일 · 커밋 기록")]),
        light("실습 2-9 확인", checks([
            ("/mcp 에 playwright 가 연결됐나", "Playwright MCP"), ("웹 점검 결과에 콘솔 에러가 0건인가", "브라우저 에러"),
            ("tests/ 에 E2E 테스트 파일이 생겼나", "완료 기준마다 하나 이상"), ("E2E 테스트가 전부 통과하나", "실패 0")],
            "넷 다 「예」 → 커밋 · push · 2-10 마무리"), T),
    ]
