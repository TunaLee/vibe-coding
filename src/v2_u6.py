"""2-6 MCP.

배경(도구가 필요한 이유 · 평택대 교안 · 대화창 밖의 데이터 · 내장 도구와 외부 도구) → 등장 계기(회사마다 따로 만든 연결 · 연결 수가 곱으로 늘어남 → 2024-11 MCP 공개 → 확산)
→ 비유(USB-C · 공식 문서) → 구조(호스트 · 클라이언트 · 서버 · 도구 · 리소스 · 프롬프트) → 동작(도구 목록 읽기 → 고르기 → 실행)
→ API 와 MCP → 쓸 만한 MCP → 연결 방법 · 안전 설정 → 캘린더 일정 → 회의록 페이지 → 실습.
사실 출처
- anthropic.com/news/model-context-protocol (2024-11-25 · 「Every new data source requires its own custom implementation」)
- openai.com/index/chatgpt-plugins (2023-03-23) · openai.com/index/function-calling-and-other-api-updates (2023-06-13) · claude.com/blog/tool-use-ga (2024-05-30)
- openai.com/index/new-tools-and-features-in-the-responses-api (2025-05-21 원격 MCP) · blogs.microsoft.com 2025-05-19 (Steering Committee)
- modelcontextprotocol.io/registry/about (2025-09-08 preview) · anthropic.com/news/donating-the-model-context-protocol… (2025-12-09 AAIF)
- modelcontextprotocol.io/docs/getting-started/intro (USB-C) · /docs/learn/architecture (Host · Client · Server · Tools · Resources · Prompts)
- code.claude.com/docs/en/mcp (claude mcp add --transport http · scope · claude.ai 커넥터 자동 표시)
- claude.com/docs/connectors/google/calendar (읽기 전용) · supabase.com/docs/guides/getting-started/mcp · github.com/microsoft/playwright-mcp
- github.com/upstash/context7 · developers.figma.com/docs/figma-mcp-server · developers.notion.com/docs/mcp · github.com/github/github-mcp-server
"""
import viz2
from deck import flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
import v2scene
from v2scene import agent, tools
from v2kit import brief
from v3kit import phmap

T = "2-6"
ANN = ("Anthropic · Introducing the Model Context Protocol", "https://www.anthropic.com/news/model-context-protocol")
AAIF = ("Anthropic · Donating MCP · Agentic AI Foundation", "https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation")
INTRO = ("modelcontextprotocol.io · What is MCP", "https://modelcontextprotocol.io/docs/getting-started/intro")
ARCH = ("modelcontextprotocol.io · Architecture", "https://modelcontextprotocol.io/docs/learn/architecture")
CC = ("Claude Code · MCP", "https://code.claude.com/docs/en/mcp")
SMCP = ("Supabase · MCP", "https://supabase.com/docs/guides/getting-started/mcp")
GCAL = ("Claude · Google Calendar connector", "https://claude.com/docs/connectors/google/calendar")

def relay():
    """MCP 없이 — 사람이 복사 · 붙여 넣기를 오가는 줄 / MCP — 한 번 요청 · 직접 실행. 줄 안 칸이 차례로 나타남."""
    def row(head, steps, d0, hl):
        out = []
        for i, (who, x, hand) in enumerate(steps):
            d = d0 + i * .35
            if i:
                out.append(f'<i class="v2u3ra" style="--d:{d - .12:.2f}s">→</i>')
            out.append(f'<div class="v2u3rs{" hand" if hand else ""}" style="--d:{d:.2f}s"><b>{who}</b><span>{x}</span></div>')
        return f'<div class="v2u3rr{" on" if hl else ""}"><div class="v2u3rh">{head}</div><div class="v2u3rw">{"".join(out)}</div></div>'
    return ('<div class="v2u3relay">'
            + row("MCP 없이", [("Claude", "SQL 작성", False), ("나", "복사", True), ("Supabase 화면", "붙여 넣기 · 실행", True),
                              ("나", "오류 문구 복사", True), ("Claude", "수정 SQL", False)], .3, False)
            + row("MCP 연결", [("나", "「pages 표 만들어 줘」", False), ("Claude Code", "SQL 작성", False),
                              ("Supabase", "직접 실행 · 결과", False), ("Claude Code", "오류면 다시 고침", False)], 2.3, True)
            + '<div class="v2u3cnt"><span class="c1">사람 손 3번 · 오류마다 반복</span><span class="c2">사람 손 0번 · 요청 한 줄</span></div>'
            + "</div>")


def cal_to_tasks():
    """Google 캘린더 일정 → Claude Code(MCP 두 개) → 미니 노션. 칸은 제자리 · 읽힌 일정과 추가된 행이 같은 색으로 켜짐."""
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
          + msg("me", "이번 주 회의마다 회의록 페이지 만들어 줘", .6)
          + msg("tool l", "<em>Google Calendar MCP</em> 이번 주 일정 조회", 1.3)
          + msg("ai", "일정 3건 · 회의 날짜로 회의록 페이지 3개 만들까요?", 2.6)
          + msg("me", "응", 3.3)
          + msg("tool r", "<em>Supabase MCP</em> pages 에 3행 추가", 3.8)
          + msg("ai", "완료 · 회의록 페이지 3개", 5.2) + '</div></div>')
    rows = [("주간 회의록", "11/27", "작성 중", "", 0), ("교육 자료 정리", "11/25", "초안", "", 0),
            ("주간 회의 회의록", "11/30", "초안", "c1", 4.2), ("고객사 미팅 회의록", "12/2", "초안", "c2", 4.5), ("보고서 마감 회의록", "12/4", "초안", "c3", 4.8)]
    tr = "".join(f'<tr class="{"nw " + c if c else ""}" style="--d:{d}s"><td>{t}{"<small>캘린더</small>" if c else ""}</td><td>{du}</td><td>{st}</td></tr>'
                 for t, du, st, c, d in rows)
    board = ('<div class="v2cW"><div class="v2cH"><i class="b"></i>미니 노션 · pages</div>'
             f'<table class="v2cT"><thead><tr><th>페이지</th><th>날짜</th><th>상태</th></tr></thead><tbody>{tr}</tbody></table></div>')
    plug = lambda side, name, d: f'<div class="v2cP {side}" style="--d:{d}s"><b>MCP</b><span>{name}</span></div>'
    return ('<div class="v2c">' + cal + plug("l", "읽기", 1.3) + cc + plug("r", "쓰기", 3.8) + board + '</div>')


def timeline():
    """연결 방식의 변화 — 점이 왼쪽부터 차례로 켜짐 · 2024-11 MCP 공개가 주황."""
    ev = [("2023-03", "ChatGPT Plugins", "ChatGPT 전용 추가 기능", ""), ("2023-06", "Function calling", "OpenAI API 형식", ""),
          ("2024-05", "Claude tool use", "Anthropic API 형식", ""), ("2024-11", "MCP 공개", "Anthropic · 오픈 표준", "on"),
          ("2025-05", "OpenAI · Microsoft", "원격 MCP 지원 · 운영 위원회", ""), ("2025-12", "Linux Foundation", "Agentic AI Foundation 에 기증", "")]
    c = "".join(f'<div class="e {k}" style="--d:{.3 + i * .5:.1f}s"><i></i><span class="y">{y}</span><b>{n}</b><small>{x}</small></div>'
                for i, (y, n, x, k) in enumerate(ev))
    return (f'<div class="v27tl"><div class="ax"></div>{c}</div>'
            '<div class="v27grp"><span style="--d:.3s">회사마다 따로 만든 연결</span><span class="on" style="--d:1.8s">하나의 공개 규격</span></div>')


def wires():
    """AI 앱 3 × 서비스 4 — 따로 연결하면 선 12개(회색이 하나씩 그어짐) → MCP 를 사이에 두면 선 7개(주황)."""
    apps, svcs = ["Claude", "ChatGPT", "사내 챗봇"], ["Google 캘린더", "Supabase", "GitHub", "Notion"]
    W, H = 1120, 300
    ax, sx = 150, 970
    ay = [70 + i * 80 for i in range(3)]
    sy = [40 + i * 74 for i in range(4)]
    s = ""
    for side, xs, ys, names in (("l", ax, ay, apps), ("r", sx, sy, svcs)):
        for y, n in zip(ys, names):
            x0 = xs - 130 if side == "l" else xs
            s += (f'<rect x="{x0}" y="{y - 22}" width="130" height="44" rx="10" fill="#fff" stroke="#1F3A5F" stroke-width="2"/>'
                  f'<text x="{x0 + 65}" y="{y + 6}" text-anchor="middle" class="v27t">{n}</text>')
    k = 0
    for i, y1 in enumerate(ay):
        for j, y2 in enumerate(sy):
            s += (f'<line class="v27a" x1="{ax}" y1="{y1}" x2="{sx}" y2="{y2}" style="--d:{.3 + k * .12:.2f}s"/>')
            k += 1
    mx = (ax + sx) / 2
    s += (f'<g class="v27m" style="--d:3.4s"><rect x="{mx - 70}" y="20" width="140" height="260" rx="16" fill="#FFF3E0" stroke="#F28C28" stroke-width="3"/>'
          f'<text x="{mx}" y="150" text-anchor="middle" class="v27mt">MCP</text><text x="{mx}" y="176" text-anchor="middle" class="v27ms">하나의 규격</text></g>')
    for i, y in enumerate(ay):
        s += f'<line class="v27b" x1="{ax}" y1="{y}" x2="{mx - 70}" y2="{y + 0}" style="--d:{3.8 + i * .15:.2f}s"/>'
    for j, y in enumerate(sy):
        s += f'<line class="v27b" x1="{mx + 70}" y1="{y}" x2="{sx}" y2="{y}" style="--d:{4.3 + j * .15:.2f}s"/>'
    cnt = ('<div class="v27cnt"><span class="a" style="--d:2s">따로 연결 · 3 × 4 = <b>12개</b></span>'
           '<span class="b" style="--d:5s">MCP · 3 + 4 = <b>7개</b></span></div>')
    return f'<svg class="v27w" viewBox="0 0 {W} {H}">{s}</svg>{cnt}'


def arch():
    """구조 — 호스트(Claude Code) 안 클라이언트 3개 · 서버 3개 · 서버가 내놓는 것 세 가지."""
    rows = [("Supabase MCP 서버", "표 만들기 · SQL 실행"), ("Playwright MCP 서버", "브라우저 열기 · 클릭"), ("Google Calendar 서버", "일정 읽기")]
    cl = "".join(f'<div class="cli" style="--d:{.6 + i * .3:.1f}s">MCP 클라이언트</div>' for i in range(3))
    sv = "".join(f'<div class="srv" style="--d:{.8 + i * .3:.1f}s"><b>{n}</b><span>{x}</span></div>' for i, (n, x) in enumerate(rows))
    return (f'<div class="v27ar"><div class="host" style="--d:.3s"><div class="h">호스트 · Claude Code</div>{cl}</div>'
            f'<div class="lk">{"".join("<i></i>" for _ in range(3))}</div><div class="svs">{sv}</div></div>')


def tool_kinds():
    """Claude Code 내장 도구(내 컴퓨터 안) + 외부 도구(다른 회사 서비스) · 가운데 MCP 플러그. 평택대 교안 「내장 도구와 외부 도구」 구조."""
    inner = ["Read", "Write · Edit", "Bash", "Grep · Glob", "WebFetch"]
    outer = [("Google 캘린더", "회의 일정"), ("Supabase", "미니 노션 DB"), ("Notion · Slack", "회사 협업 도구"), ("미니 노션 MCP 서버", "2-7 에서 직접 만듦")]
    i = "".join(f'<span style="--d:{k * .08:.2f}s">{t}</span>' for k, t in enumerate(inner))
    o = "".join(f'<div class="tk-o" style="--d:{.8 + k * .12:.2f}s"><b>{h}</b><small>{d}</small></div>' for k, (h, d) in enumerate(outer))
    return ('<div class="tk">'
            f'<div class="tk-in"><div class="tk-h">Claude Code 내장 도구</div><div class="tk-chips">{i}</div>'
            '<div class="tk-f">설치하면 바로 · 내 컴퓨터의 파일 · 명령 · 웹</div></div>'
            '<div class="tk-plug"><b>MCP</b><i>⇄</i></div>'
            f'<div class="tk-out"><div class="tk-h">외부 도구</div>{o}</div></div>')


def slides():
    supa_tools = tools([("list_tables", "표 목록 보기"), ("execute_sql", "SQL 실행"), ("apply_migration", "표 만들기 · 바꾸기")],
                       "execute_sql", 1.3, 2.0)
    return [
        # ── 배경 · 도구가 필요한 이유 → 외부 도구 → MCP
        light("도구가 필요한 이유", viz2.calc_compare()
              + note("LLM 혼자 못 하는 것", "정확한 계산 · 오늘의 정보 · 사내 데이터 · 실제 행동 → 무엇을 부를지는 LLM, 실행은 도구"), T),
        light("대화창 밖의 데이터", relay()
              + note("AI 의 한계", "캘린더 · DB · 사내 문서는 대화창 밖 · 사람이 옮겨 주는 만큼만 앎"), T),
        light("내장 도구와 외부 도구", tool_kinds()
              + note("외부 도구", "다른 회사 서비스 · 회사마다 연결 방식이 달랐음 → 같은 규격이 필요해짐 = MCP"), T),
        light("회사마다 따로 만든 연결", timeline()
              + src(("OpenAI · ChatGPT plugins", "https://openai.com/index/chatgpt-plugins/"),
                    ("Claude · Tool use GA", "https://claude.com/blog/tool-use-ga"), ANN, AAIF), T),
        light("연결 수가 늘어나는 문제", wires()
              + note("발표문", "「새 데이터 소스마다 따로 구현이 필요하다」 · Anthropic 2024-11-25 · 앱 · 서비스 수는 예"), T),
        light("USB-C 포트", phmap("usbc_port.webp", "노트북의 USB-C 포트", "사진 · Logant547 · CC BY 4.0",
                                    "https://commons.wikimedia.org/wiki/File:USB-C_connector_on_a_laptop.jpg", viz2.maprows([
            ("노트북", "AI 앱 · 호스트", "Claude Code · Claude · ChatGPT"), ("USB-C 규격", "MCP", "연결 · 주고받는 형식"),
            ("모니터 · 외장 디스크", "MCP 서버", "Supabase · 캘린더 · 브라우저"),
            ("꽂으면 기능을 알림", "도구 목록", "list_tables · execute_sql …")], "USB-C", "MCP"))
              + note("공식 소개", "「MCP 는 AI 앱을 위한 USB-C 포트」 · Think of MCP like a USB-C port for AI applications")
              + src(INTRO), T),
        light("MCP 구조", arch()
              + viz2.tiles([("도구 (Tools)", "AI 가 실행하는 기능 · 새 페이지"), ("리소스 (Resources)", "AI 가 읽는 자료 · 파일 · 표"),
                            ("프롬프트 (Prompts)", "미리 만든 요청 틀")], 3), T),
        light("MCP 동작", agent("Claude Code", [
            ("me", "마감 지난 페이지 몇 개야?", .3), ("tool", "<em>supabase</em> 도구 목록 읽기", 1.3),
            ("tool", "<em>execute_sql</em> select count(*) from pages where date &lt; today …", 2.0),
            ("ai", "마감 지난 페이지 2개 · 박서연 1 · 최민재 1", 4.4)],
            ("Supabase MCP 서버", "도구 3개", supa_tools),
            '<div class="v2sBx db"><div class="bh"><b>DB</b><small>pages</small></div><table><tr><th>title</th><th>date</th></tr>'
            '<tr class="hl" style="--d:2.8s"><td>예산안 메모</td><td>11/18</td></tr><tr class="hl" style="--d:2.95s"><td>설문 결과</td><td>11/19</td></tr>'
            '<tr><td>보고서</td><td>12/04</td></tr></table></div>',
            (("도구 호출", 2.0), ("결과 · 2", 3.6), ("SQL", 2.4), ("행 2개", 3.2)))
              + v2scene.steps([("①", "질문", .3), ("②", "도구 목록 읽기", 1.3), ("③", "도구 고르기 · 실행", 2.0),
                               ("④", "결과 받기", 3.6), ("⑤", "답하기", 4.4)]), T),
        light("API와 MCP", viz2.pair(
            "API", [("부르는 쪽", "내 앱 코드"), ("형식", "서비스마다 다름"), ("쓰는 때", "이용자가 앱을 쓸 때 (2-1 · 2-5)")],
            "MCP", [("부르는 쪽", "AI · Claude Code · ChatGPT"), ("형식", "하나의 규격 · 도구 목록"), ("안에서", "MCP 서버가 각 서비스 API 호출")], hl="r"), T),
        light("쓸 만한 MCP", viz2.maprows([
            ("Playwright", "브라우저 열기 · 클릭 · 콘솔 확인", "화면 테스트 (2-9)"),
            ("Supabase", "표 만들기 · 조회 · 로그", "DB 작업을 말로"),
            ("Context7", "라이브러리 최신 문서", "버전 틀린 코드 줄이기"),
            ("Figma · Notion", "디자인 · 기획 문서 읽기", "화면 · 요구사항 입력"),
            ("GitHub", "이슈 · PR · Actions", "Claude Code 는 gh 로도 됨")], "MCP 서버", "하는 일")
              + src(("Playwright MCP", "https://github.com/microsoft/playwright-mcp"), SMCP,
                    ("Context7", "https://github.com/upstash/context7"), ("GitHub MCP", "https://github.com/github/github-mcp-server")), T),
        light("MCP 연결 방법", code("터미널 · 원격 MCP 서버 추가", esc(
            "claude mcp add --transport http supabase \\\n  \"https://mcp.supabase.com/mcp?project_ref=<프로젝트 ID>&read_only=true\""))
              + viz2.tiles([("범위 (scope)", "local 나만 · project 팀 공유 .mcp.json · user 내 모든 프로젝트"),
                            ("확인", "Claude Code 에서 /mcp · 목록 · 로그인"),
                            ("claude.ai 커넥터", "claude.ai 에서 켠 커넥터가 Claude Code 에도 표시 · 구독 로그인일 때")], 3)
              + note("요청", "「Supabase MCP 연결해 줘」 · 명령은 Claude Code 가 · 로그인은 사람이")
              + src(CC, SMCP), T),
        light("MCP 안전 설정", viz2.tiles([
            ("project_ref", "프로젝트 하나에만 연결"), ("read_only=true", "읽기만 · 쓸 때만 잠시 해제"),
            ("개발용 프로젝트", "실제 서비스 DB 에 연결하지 않기"), ("실행 승인", "도구 실행마다 내용 보고 허용")], 4)
              + note("Playwright MCP", "「보안 경계가 아님」 · 공식 문서 · 믿을 수 있는 사이트만")
              + src(SMCP, ("Playwright MCP", "https://github.com/microsoft/playwright-mcp")), T),
        light("캘린더 일정 → 회의록 페이지", cal_to_tasks()
              + note("준비", "claude.ai 에서 Google Calendar 커넥터 켜기 · 읽기 전용 · Supabase MCP 는 쓰기 허용 · 개발용 DB"), T),
        # ── 실습
        lab("2-6", "MCP 연결 · 캘린더 → 페이지", T, "Claude Code 에 MCP 를 붙여 캘린더 일정을 미니 노션 페이지로 옮긴다",
            ["claude.ai 에서 Google Calendar 커넥터 켜기", "Supabase MCP 연결 · 로그인", "/mcp 로 두 서버 확인",
             "이번 주 일정 → 페이지 요청", "미니 노션 화면에서 확인"],
            ["/mcp 에 두 서버 연결됨", "캘린더 일정 수만큼 새 페이지", "일정 날짜 = 페이지 날짜"], files="2-5 까지의 앱 · 개발용 Supabase 프로젝트"),
        brief("2-6", T, ["Google Calendar 커넥터", "Supabase MCP 연결", "/mcp 확인", "일정 → 페이지 요청", "페이지 목록 확인"],
              [("목표", "이번 주 캘린더 일정을 페이지로"), ("규칙", "일정 날짜 = 날짜 · 작성자는 나"),
               ("승인", "추가 전에 목록 먼저 보여 주기"), ("하지 말 것", "실제 서비스 DB · 일정 수정")],
              ["MCP", "커넥터", "/mcp", "read_only"],
              ["페이지 목록에 캘린더 일정 수만큼 새 페이지", "날짜가 일정 날짜와 같음"],
              "도구가 안 보이면 /mcp 에서 로그인 상태 확인 · 다시 연결"),
        light("실습 2-6 확인", checks([
            ("/mcp 에 두 서버가 연결됐나", "Google Calendar · Supabase"), ("추가 전에 목록을 먼저 보여 줬나", "승인 단계"),
            ("페이지 목록에 일정 수만큼 페이지가 생겼나", "날짜 = 일정 날짜"), ("끝난 뒤 read_only 로 되돌렸나", "쓰기 차단")],
            "넷 다 「예」 → 2-7 내 MCP 서버 만들기"), T),
    ]


CSS = """
  .v2u3msg.rq{border-color:#9DB7DA; background:#F2F7FF; animation:v2u3right 1.2s ease-out .4s forwards;} .v2u3msg.rq em{color:#1F4E8C;}
  @keyframes v2u3right{0%{opacity:0; transform:translateX(-90px)} 30%{opacity:1} 100%{opacity:1; transform:none}}
  /* 2-2 · 사람 손 vs MCP */
  .v2u3relay{display:flex; flex-direction:column; gap:14px; margin:4px 0 14px;}
  .v2u3rr{display:grid; grid-template-columns:96px 1fr; gap:12px; align-items:center; padding:12px 14px; border:1.5px solid #E1E5EB; border-radius:14px; background:#fff;}
  .v2u3rr.on{border-color:#F28C28; background:#FFF8F0;}
  .v2u3rh{font-size:18px; font-weight:800; color:#16233A;} .v2u3rr.on .v2u3rh{color:#E07A12;}
  .v2u3rw{display:flex; align-items:center; gap:8px;}
  .v2u3rs{flex:1; border:1.5px solid #D9DDE3; border-radius:10px; padding:8px 10px; background:#fff; opacity:0; animation:v2u3in .4s ease-out var(--d) forwards;}
  .v2u3rs b{display:block; font-size:16px; color:#16233A;} .v2u3rs span{font-size:13.5px; color:#3A4657;}
  .v2u3rs.hand{border-color:#E8A39B; background:#FDECEA;} .v2u3rs.hand b{color:#C0392B;}
  .v2u3ra{font-style:normal; font-size:18px; font-weight:800; color:#F28C28; opacity:0; animation:v2u3in .3s ease-out var(--d) forwards;}
  .v2u3cnt{display:grid; grid-template-columns:1fr 1fr; gap:14px;}
  .v2u3cnt span{text-align:center; font-size:17px; font-weight:800; padding:8px; border-radius:10px; opacity:0;}
  .v2u3cnt .c1{background:#FDECEA; color:#C0392B; animation:v2u3in .4s ease-out 2.0s forwards;}
  .v2u3cnt .c2{background:#FFE3C4; color:#B85A00; animation:v2u3in .4s ease-out 3.8s forwards;}
  @media print{.v2u3wire{transform:none; animation:none} .v2u3rs,.v2u3ra,.v2u3cnt span,.v2u3hs,.v2u3msg,.v2u3lb,.v2u3la{opacity:1; animation:none}}
  @keyframes v2u3in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u3rs,.v2u3ra,.v2u3cnt span{opacity:1; animation:none}}
  /* 2-5 · 캘린더 일정 → 페이지 (v2c) */
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
  /* 2-6 · 연결 방식의 변화 (v27tl) */
  .v27tl{position:relative; display:grid; grid-template-columns:repeat(6,1fr); gap:8px; margin:26px 0 10px; padding-top:22px;}
  .v27tl .ax{position:absolute; left:0; right:0; top:29px; height:3px; background:#D9DDE3;}
  .v27tl .e{position:relative; display:flex; flex-direction:column; gap:3px; opacity:0; animation:v27in .4s var(--d) forwards;}
  .v27tl .e i{position:absolute; top:-1px; left:4px; width:14px; height:14px; border-radius:50%; background:#1F3A5F; border:3px solid #fff;}
  .v27tl .e .y{margin-top:22px; font-family:var(--mono); font-size:14px; color:#6B7785;}
  .v27tl .e b{font-size:18px; color:#16233A;} .v27tl .e small{font-size:14px; color:#3A4657;}
  .v27tl .e.on i{background:#F28C28; width:18px; height:18px; top:-3px;} .v27tl .e.on b{color:#E07A12;}
  .v27grp{display:grid; grid-template-columns:3fr 3fr; gap:8px; margin:10px 0 14px;}
  .v27grp span{text-align:center; font-size:16px; font-weight:800; padding:8px; border-radius:10px; background:#EEF1F5; color:#3A4657; opacity:0; animation:v27in .4s var(--d) forwards;}
  .v27grp span.on{background:#FFE3C4; color:#B85A00;}
  /* 2-6 · 연결 수 (v27w) */
  .v27w{width:100%; height:300px; display:block;}
  .v27t{font-size:16px; font-weight:700; fill:#16233A;} .v27mt{font-size:26px; font-weight:800; fill:#E07A12;} .v27ms{font-size:14px; fill:#3A4657;}
  .v27a{stroke:#9AA5B1; stroke-width:2; stroke-dasharray:900; stroke-dashoffset:900; animation:v27draw .5s var(--d) forwards, v27fade .6s 3.2s forwards;}
  .v27b{stroke:#F28C28; stroke-width:3.5; stroke-dasharray:900; stroke-dashoffset:900; animation:v27draw .45s var(--d) forwards;}
  .v27m{opacity:0; animation:v27in .4s var(--d) forwards;}
  .v27cnt{display:grid; grid-template-columns:1fr 1fr; gap:14px; margin:4px 0 12px;}
  .v27cnt span{text-align:center; font-size:18px; padding:8px; border-radius:10px; opacity:0; animation:v27in .4s var(--d) forwards;}
  .v27cnt .a{background:#EEF1F5; color:#3A4657;} .v27cnt .b{background:#FFE3C4; color:#B85A00;}
  /* 2-6 · 구조 (v27ar) */
  .v27ar{display:grid; grid-template-columns:300px 80px 1fr; align-items:center; margin:0 0 14px;}
  .v27ar .host{border:2.5px solid #F28C28; background:#FFF8F0; border-radius:16px; padding:12px; display:flex; flex-direction:column; gap:10px; opacity:0; animation:v27in .4s var(--d) forwards;}
  .v27ar .host .h{font-size:19px; font-weight:800; color:#E07A12;}
  .v27ar .cli{border:1.5px solid #F7C99A; background:#fff; border-radius:10px; padding:9px 12px; font-size:15px; font-weight:700; color:#16233A; opacity:0; animation:v27in .3s var(--d) forwards;}
  .v27ar .lk{display:flex; flex-direction:column; gap:42px; padding-top:40px;} .v27ar .lk i{height:3px; background:#F28C28;}
  .v27ar .svs{display:flex; flex-direction:column; gap:10px; padding-top:40px;}
  .v27ar .srv{border:1.5px solid #D9DDE3; border-left:5px solid #1F3A5F; border-radius:10px; background:#fff; padding:7px 14px; opacity:0; animation:v27in .3s var(--d) forwards;}
  .v27ar .srv b{font-size:16px; color:#16233A; margin-right:10px;} .v27ar .srv span{font-size:14px; color:#3A4657;}
  @keyframes v27in{from{opacity:0} to{opacity:1}}
  @keyframes v27draw{to{stroke-dashoffset:0}}
  @keyframes v27fade{to{opacity:.15}}
  @media print{.v27tl .e,.v27grp span,.v27m,.v27cnt span,.v27ar .host,.v27ar .cli,.v27ar .srv{opacity:1; animation:none} .v27a,.v27b{stroke-dashoffset:0; animation:none}}
"""
