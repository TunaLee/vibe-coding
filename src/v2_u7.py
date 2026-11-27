"""2-7 MCP 서버 만들기.

배경(Supabase MCP 는 개발자용 · 표 전체 → 팀원이 쓰는 업무 도구만) → 도구 설계(이름 · 설명 · 입력 칸 = AI 가 읽는 메뉴판)
→ 코드 뜻(mcp-handler · registerTool · 2-4 의 insert) → 동작 장면 → 만드는 순서 → Inspector · 로컬 연결 → 인증 → 배포 → 실습.
사실 출처
- vercel.com/docs/mcp/deploy-mcp-servers-to-vercel (mcp-handler v2 · @modelcontextprotocol/server v2 · zod 4 · Node 22+ · app/api/mcp/route.ts
  · createMcpHandler · server.registerTool · Streamable HTTP · withMcpAuth · protectedResourceHandler · 토큰 발급은 별도 인증 서버 · Inspector 명령)
- github.com/modelcontextprotocol/typescript-sdk (v2 2026-07-27 · server / client 패키지 분리)
- code.claude.com/docs/en/mcp (claude mcp add --transport http)
"""
import viz2
from deck import flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v2kit import brief, codemap
from v2scene import agent, board, tools, steps

T = "2-7"
VMCP = ("Vercel · Deploy MCP servers", "https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel")
SDK = ("MCP TypeScript SDK", "https://github.com/modelcontextprotocol/typescript-sdk")
CC = ("Claude Code · MCP", "https://code.claude.com/docs/en/mcp")
AUTH = ("MCP · Authorization", "https://modelcontextprotocol.io/specification/latest/basic/authorization")

TOOLS = [("add_task", "할 일 추가"), ("list_tasks", "할 일 목록"), ("update_task", "상태 · 기한 바꾸기"), ("list_due", "기간 안 마감 보기")]
BOARD = [("주간 보고서 작성", "11/27", "진행 중", None), ("교육 자료 준비", "11/25", "할 일", None)]

CSS = ""


def slides():
    return [
        light("팀 보드 MCP 서버", viz2.pair(
            "Supabase MCP (2-6)", [("쓰는 사람", "개발자 · 나"), ("할 수 있는 일", "표 전체 · SQL 무엇이든"),
                                  ("쓰는 곳", "Claude Code")],
            "팀 보드 MCP 서버", [("쓰는 사람", "로그인한 팀원 모두"), ("할 수 있는 일", "업무 도구 4개만 · 권한 규칙 그대로"),
                               ("쓰는 곳", "Claude Code · Claude · ChatGPT")], hl="r")
              + note("MCP 서버", "내 서비스의 기능을 AI 가 쓸 수 있는 도구로 열어 두는 프로그램"), T),
        light("도구 설계", viz2.maprows([
            ("add_task", "할 일 · 기한 · 담당자", "할 일 추가 · 쓰기"),
            ("list_tasks", "상태 · 담당자", "할 일 목록 · 읽기"),
            ("update_task", "할 일 번호 · 상태 · 기한", "상태 · 기한 바꾸기 · 쓰기"),
            ("list_due", "시작일 · 종료일", "기간 안 마감 · 일정 보기 · 읽기")], "도구 이름", "받는 칸 → 하는 일")
              + note("메뉴판", "도구 이름 · 설명 · 받는 칸을 AI 가 읽고 고름 · 설명이 흐리면 엉뚱한 도구 선택"), T),
        light("MCP 서버 코드 뜻", codemap([
            ("createMcpHandler((server) => {", "MCP 서버 만들기 · mcp-handler"),
            ('  server.registerTool("add_task", {', "도구 하나 등록 · 이름"),
            ('    description: "팀 보드에 할 일 하나를 추가한다",', "AI 가 읽는 설명"),
            ("    inputSchema: { title: z.string(), due: z.string() },", "받는 칸 · 형식"),
            ("  }, async ({ title, due }) => insertTask(title, due))", "실행 · 2-4 의 insert"),
            ("})", "app/api/mcp/route.ts · 주소 /api/mcp")],
            ask="개발 계획의 도구 목록대로 팀 보드 MCP 서버를 만들어 줘", title="Claude Code가 쓴 코드 · 예")
              + src(VMCP, SDK), T),
        light("MCP 서버 동작", agent("Claude Code", [
            ("me", "내일까지 회의록 정리 할 일로 추가해 줘", .3), ("tool", "<em>team-board</em> 도구 목록 읽기", 1.2),
            ("tool", "<em>add_task</em> 회의록 정리 · 2026-11-29", 1.9), ("ai", "추가 완료 · 기한 11/29", 4.4)],
            ("내 MCP 서버", "/api/mcp · Vercel", tools(TOOLS, "add_task", 1.2, 1.9)),
            board(BOARD + [("회의록 정리", "11/29", "할 일", 3.2)]),
            (("add_task 호출", 1.9), ("결과 · 추가됨", 3.8), ("insert", 2.5), ("새 행", 3.2)))
              + steps([("①", "요청", .3), ("②", "도구 목록 읽기", 1.2), ("③", "add_task 호출", 1.9),
                       ("④", "DB 에 새 행", 3.2), ("⑤", "결과 보고", 4.4)])
              + src(VMCP), T),
        light("만드는 순서", flow([
            ("도구 목록", "개발 계획에 이름 · 칸"), ("서버 만들기 요청", "Claude Code · mcp-handler"), ("Inspector 확인", "도구 목록 · 직접 호출"),
            ("Claude Code 연결", "localhost 로 시험"), ("push · 배포", "Vercel · 공개 주소")], hl=2)
              + note("2-3 개발 계획", "연동 대상 칸에 「팀 보드 MCP 서버 · 도구 4개」 추가"), T),
        light("MCP Inspector", code("터미널 · 서버 실행 중에", esc(
            "npx @modelcontextprotocol/inspector@latest \\\n  --server-url http://localhost:3000/api/mcp --transport http"))
              + viz2.tiles([("도구 목록", "이름 · 설명 · 받는 칸 확인"), ("직접 호출", "값을 넣고 add_task 실행"),
                            ("결과", "응답 JSON · 보드에 새 행")], 3)
              + note("요청", "「MCP Inspector 로 내 서버 열어 줘」 · 화면 확인은 사람이")
              + src(VMCP), T),
        light("Claude Code에 연결", code("터미널 · 로컬 시험", esc("claude mcp add --transport http team-board http://localhost:3000/api/mcp"))
              + viz2.tiles([("/mcp", "team-board · 도구 4개"), ("시험 요청", "「이번 주 마감 할 일 보여 줘」 → list_due"),
                            ("배포 뒤", "주소만 배포 주소로 바꿔 다시 추가")], 3)
              + src(CC), T),
        light("인증", viz2.pair(
            "인증 없음", [("누가 부르나", "주소를 아는 누구나"), ("할 일 추가", "아무 이름 · 확인 없음"), ("쓸 때", "로컬 시험만")],
            "로그인 (OAuth)", [("누가 부르나", "로그인한 팀원"), ("할 일 추가", "내 계정 · RLS 규칙 그대로"),
                             ("등록할 때", "Claude · ChatGPT 가 로그인 창 표시")], hl="r")
              + note("구조", "MCP 서버는 토큰 확인만 · 로그인 · 토큰 발급은 인증 서버가 따로 · 설정은 Claude Code 와 함께")
              + src(VMCP, AUTH), T),
        light("배포", flow([("push", "1-7 과 같음"), ("Vercel 자동 배포", "/api/mcp 포함"),
                            ("공개 주소", "team-board.vercel.app/api/mcp"), ("Inspector 재확인", "배포 주소 확인")], hl=2)
              + viz2.tiles([("공개 HTTPS 주소", "Claude · ChatGPT 등록 조건 · localhost 는 안 됨"),
                            ("환경변수", "Supabase 키 · 인증 설정 · Vercel 에 등록 (2-9)")], 2)
              + src(VMCP), T),
        # ── 실습
        lab("2-7", "팀 보드 MCP 서버", T, "할 일 추가 · 조회 도구를 가진 MCP 서버를 만들어 배포한다",
            ["개발 계획에 도구 목록 추가", "MCP 서버 만들기 요청", "Inspector 로 도구 확인", "Claude Code 에 localhost 연결 · 시험",
             "push · 배포 주소 확인"],
            ["Inspector 에 도구 4개", "Claude Code 요청으로 보드에 할 일 추가", "배포 주소 /api/mcp 응답"], files="2-6 까지의 앱 · 개발계획.md v2"),
        brief("2-7", T, ["도구 목록", "서버 만들기", "Inspector", "Claude Code 연결", "배포"],
              [("목표", "팀 보드 MCP 서버 · 도구 4개"), ("도구", "add_task · list_tasks · update_task · list_due"),
               ("권한", "로그인 계정 · RLS 그대로"), ("하지 말 것", "secret 키 · 삭제 도구 · 인증 없이 배포")],
              ["MCP 서버", "도구 설명", "Inspector", "/api/mcp"],
              ["Inspector 에서 add_task 실행 → 보드에 새 행", "/mcp 에 team-board 연결"],
              "도구가 안 보이면 서버 실행 창의 에러 원문을 그대로 Claude Code 에"),
        light("실습 2-7 확인", checks([
            ("Inspector 에 도구 4개가 보이나", "이름 · 설명 · 받는 칸"), ("Claude Code 요청으로 할 일이 추가되나", "보드 새로고침"),
            ("배포 주소 /api/mcp 가 열리나", "Inspector 로 배포 주소"), ("삭제 도구 · secret 키가 없나", "코드 검색")],
            "넷 다 「예」 → 2-8 Claude · ChatGPT 에 등록"), T),
    ]
