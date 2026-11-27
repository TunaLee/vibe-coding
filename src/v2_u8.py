"""2-8 MCP 서버 등록 · 활용.

등록할 곳(Claude Code · Claude 웹 · ChatGPT) → 원격 주소 조건 → Claude 에서 업무 등록(장면) → ChatGPT 에서 조회(장면)
→ 캘린더와 함께 일정 관리 → 쓰기 확인 · 점검 → 실습.
사실 출처
- support.claude.com/en/articles/11175166 (custom connector · Free 1개 · Customize → Connectors → Add custom connector · 공개 HTTPS 443 · localhost 불가)
- help.openai.com/en/articles/12584461 (Plugins → + → Add custom MCP server · Developer mode 불필요 · 전체 MCP 는 Business · Enterprise/Edu · Pro 는 읽기)
- developers.openai.com/api/docs/guides/developer-mode (쓰기 동작 기본 확인 · readOnlyHint 없으면 쓰기)
- code.claude.com/docs/en/mcp · claude.com/docs/connectors/google/calendar (읽기 전용)
"""
import viz2
from deck import lab, light
from hx import checks, note
from stats_hx import src
from v2kit import brief, chat
from v2scene import agent, board, tools, steps

T = "2-8"
CL = ("Claude · Custom connectors", "https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp")
OA = ("ChatGPT · Custom MCP servers", "https://help.openai.com/en/articles/12584461")
OAD = ("OpenAI · Developer mode", "https://developers.openai.com/api/docs/guides/developer-mode")
CC = ("Claude Code · MCP", "https://code.claude.com/docs/en/mcp")
GCAL = ("Claude · Google Calendar connector", "https://claude.com/docs/connectors/google/calendar")

TOOLS = [("add_task", "할 일 추가"), ("list_tasks", "할 일 목록"), ("update_task", "상태 · 기한 바꾸기"), ("list_due", "기간 안 마감 보기")]
BOARD = [("주간 보고서 작성", "11/27", "진행 중", None), ("회의록 정리", "11/29", "할 일", None)]

CSS = ""


def slides():
    return [
        light("MCP 서버 등록 위치", viz2.maprows([
            ("Claude Code", "claude mcp add --transport http …", "터미널 · 2-7 에서 연결"),
            ("Claude 웹 · 데스크톱", "Customize → Connectors → Add custom connector", "Free 는 1개"),
            ("ChatGPT", "Plugins → + → Add custom MCP server", "쓰기 도구는 Business · Enterprise · Edu")], "어디", "등록 경로")
              + note("같은 주소 하나", "team-board.vercel.app/api/mcp · 등록하는 곳만 다름")
              + src(CC, CL, OA), T),
        light("원격 MCP 주소 조건", viz2.tiles([
            ("공개 HTTPS", "인터넷에서 닿는 주소 · 443 포트"), ("localhost 안 됨", "Claude · ChatGPT 서버가 접속 · 내 컴퓨터는 못 찾음"),
            ("로그인", "OAuth · 등록할 때 로그인 창"), ("쓰기 확인", "쓰기 도구는 실행 전 사용자 확인")], 4)
              + note("등록 주소", "2-7 Vercel 배포 주소")
              + src(CL, OAD), T),
        light("Claude에서 업무 등록", agent("Claude", [
            ("me", "12월 4일 금요일까지 고객 제안서 작성, 담당 나로 할 일 등록해 줘", .3),
            ("tool", "<em>team-board</em> add_task · 고객 제안서 작성 · 2026-12-04", 1.4),
            ("ok", "허용", 2.0), ("ai", "등록 완료 · 기한 12/4 (금)", 4.4)],
            ("내 MCP 서버", "team-board.vercel.app", tools(TOOLS, "add_task", 1.0, 1.4)),
            board(BOARD + [("고객 제안서 작성", "12/04", "할 일", 3.2)]),
            (("add_task", 2.2), ("결과 · 추가됨", 3.8), ("insert", 2.6), ("새 행", 3.2)))
              + steps([("①", "말로 요청", .3), ("②", "도구 고르기", 1.4), ("③", "쓰기 확인 · 허용", 2.0),
                       ("④", "보드에 새 행", 3.2), ("⑤", "결과 보고", 4.4)])
              + src(CL), T),
        light("ChatGPT에서 조회", agent("ChatGPT", [
            ("me", "이번 주 마감인 팀 할 일 보여 줘", .3),
            ("tool", "<em>team-board</em> list_due · 11/30 ~ 12/04", 1.4),
            ("ai", "이번 주 마감 1건 · 고객 제안서 작성 12/4 (금)", 4.0)],
            ("내 MCP 서버", "team-board.vercel.app", tools(TOOLS, "list_due", 1.0, 1.4)),
            board(BOARD + [("고객 제안서 작성", "12/04", "할 일", None)]),
            (("list_due", 1.8), ("결과 · 1건", 3.4), ("select", 2.2), ("행 1개", 2.8)), host_cls="g")
              + note("같은 서버", "Claude 에서 넣은 할 일을 ChatGPT 에서 조회 · 데이터는 팀 보드 DB 한 곳")
              + src(OA), T),
        light("캘린더와 함께 일정 관리", chat([
            ("me", "이번 주 캘린더 일정이랑 내 할 일 마감이 겹치는 날 알려 주고, 겹치는 할 일은 다음 날로 미뤄 줘"),
            ("ai", "Google Calendar · 12/2 (수) 고객사 미팅\nteam-board · list_due → 12/2 마감 「교육 자료 준비」\n겹치는 날 1일 · 「교육 자료 준비」 기한을 12/3 으로 바꿀까요?"),
            ("me", "응"),
            ("ai", "team-board · update_task → 기한 12/3 · 완료")], "Claude 대화 예")
              + note("커넥터 둘", "Google Calendar 는 읽기 · 할 일 변경은 내 MCP 서버")
              + src(GCAL, CL), T),
        light("쓰기 확인 · 점검", viz2.tiles([
            ("쓰기 확인", "추가 · 변경 도구는 실행 전 허용 버튼"), ("읽기 표시", "조회 도구는 읽기 전용으로 표시 · 없으면 쓰기로 취급"),
            ("권한", "로그인 계정 기준 · 남의 할 일 변경 불가 (RLS)"), ("기록", "도구 호출마다 Vercel 로그 (2-9)")], 4)
              + note("삭제 도구", "만들지 않음 · 지우기는 보드 화면에서 사람이")
              + src(OAD, CL), T),
        # ── 실습
        lab("2-8", "Claude · ChatGPT 에서 업무 등록", T, "배포한 팀 보드 MCP 서버를 AI 앱에 등록해 대화로 할 일을 넣고 본다",
            ["Claude 웹에 custom connector 추가 · 로그인", "대화로 할 일 등록", "보드에서 확인",
             "ChatGPT 등록 (요금제가 되면)", "이번 주 마감 조회"],
            ["대화로 넣은 할 일이 보드에 보임", "다른 AI 앱에서 같은 할 일 조회"], files="2-7 배포 주소 · /api/mcp"),
        brief("2-8", T, ["커넥터 추가", "로그인", "할 일 등록", "보드 확인", "다른 앱에서 조회"],
              [("주소", "team-board.vercel.app/api/mcp"), ("등록 요청", "할 일 · 기한 · 담당자"),
               ("확인", "쓰기 전 허용 · 보드 새로고침"), ("하지 말 것", "인증 없는 주소 공유 · 개인 키 붙여 넣기")],
              ["custom connector", "원격 MCP", "OAuth", "쓰기 확인"],
              ["보드에 새 할 일", "다른 앱 조회 결과에 같은 할 일"],
              "커넥터 추가가 실패하면 배포 주소를 Inspector 로 먼저 확인"),
        light("실습 2-8 확인", checks([
            ("커넥터 추가 때 로그인 창이 떴나", "인증"), ("대화로 넣은 할 일이 보드에 보이나", "add_task"),
            ("추가 전에 허용을 물었나", "쓰기 확인"), ("다른 앱에서 같은 할 일이 조회되나", "같은 서버 · 같은 DB")],
            "넷 다 「예」 → 2-9 품질 · 운영"), T),
    ]
