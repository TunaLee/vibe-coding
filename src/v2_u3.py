"""2-3 API · MCP.

API: 배경(앱이 모르는 공휴일) → 비유(메뉴판 · 주문서 · 1-6 식당 주방과 이어짐 · 생성 그림) → 요청 · 응답 애니메이션 → 요청 · 응답 한 줄씩 뜻.
MCP: 배경(사람 손 복사 · 붙여넣기 vs MCP 애니메이션) → 비유(USB-C · 공식 문서) → API 와 MCP 차이 → 앱 만들 때 쓰는 MCP(허브 애니메이션) → 대화 예.
연결 명령 · 권한 · 키 보관은 2-6. 3부 3-3 의 구조 · 호출 순서 설명은 반복하지 않는다.
사실 출처
- 공휴일 API: data.go.kr/data/15012690 (한국천문연구원_특일 정보 · getRestDeInfo · locdate · dateName · isHoliday · 서비스 키 필수 · 무료)
- MCP 비유 · 예: modelcontextprotocol.io/docs/getting-started/intro (「Think of MCP like a USB-C port for AI applications」 · Figma 디자인으로 웹 앱)
- Supabase MCP 도구: supabase.com/docs/guides/getting-started/mcp (list_tables · execute_sql · apply_migration · query_logs)
- Playwright MCP: github.com/microsoft/playwright-mcp (브라우저 자동화)
"""
import viz2
from deck import light
from hx import esc, note
from stats_hx import src
from v2kit import chat, codemap
from v3kit import phmap

T = "2-3"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
API_DOC = ("공공데이터포털 · 한국천문연구원_특일 정보", "https://www.data.go.kr/data/15012690/openapi.do")
MCP_DOC = ("modelcontextprotocol.io · What is MCP", "https://modelcontextprotocol.io/docs/getting-started/intro")


def exchange():
    """요청이 오른쪽으로, 응답이 왼쪽으로 — 한 번 재생 후 멈춤."""
    req = esc("getRestDeInfo\nsolYear=2026 · solMonth=12\nServiceKey=내 서비스 키")
    res = esc('locdate: 20261225\ndateName: "기독탄신일"\nisHoliday: "Y"')
    return ('<div class="v2u3ex">'
            '<div class="v2u3end"><b>내 앱</b><span>팀 할 일 보드</span></div>'
            '<div class="v2u3mid">'
            f'<div class="v2u3msg rq"><em>요청 · 주문서</em><pre>{req}</pre></div>'
            f'<div class="v2u3msg rs"><em>응답 · 받은 음식</em><pre>{res}</pre></div>'
            '</div>'
            '<div class="v2u3end srv"><b>한국천문연구원 서버</b><span>특일 정보 · 공휴일 목록</span></div>'
            '</div>')


def lanes():
    """API 줄과 MCP 줄 — 차례로 나타남."""
    def lane(head, boxes, d0):
        out = []
        for i, (b, s, *hl) in enumerate(boxes):
            d = d0 + i * .4
            if i:
                out.append(f'<i class="v2u3la" style="--d:{d - .15:.2f}s">→</i>')
            out.append(f'<div class="v2u3lb{" hl" if hl else ""}" style="--d:{d:.2f}s"><b>{b}</b><span>{s}</span></div>')
        return f'<div class="v2u3ln"><div class="v2u3lh">{head}</div>{"".join(out)}</div>'
    return ('<div class="v2u3lanes">'
            + lane("API", [("내 앱 코드", "이용자가 기한을 고를 때"), ("API 형식", "서비스마다 다른 주소 · 칸", True), ("공휴일 서버", "한국천문연구원")], .3)
            + lane("MCP", [("나", "「표 만들어 줘」"), ("Claude Code", "도구 고르기"), ("MCP", "모든 서비스에 같은 규격", True),
                           ("Supabase MCP 서버", "안에서 Supabase API 호출")], 1.6)
            + "</div>")


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
            + row("MCP 연결", [("나", "「tasks 표 만들어 줘」", False), ("Claude Code", "SQL 작성", False),
                              ("Supabase", "직접 실행 · 결과", False), ("Claude Code", "오류면 다시 고침", False)], 2.3, True)
            + '<div class="v2u3cnt"><span class="c1">사람 손 3번 · 오류마다 반복</span><span class="c2">사람 손 0번 · 요청 한 줄</span></div>'
            + "</div>")


def hub():
    """Claude Code 에서 MCP 서버 네 개로 선이 차례로 이어짐."""
    srv = [("Supabase", "표 만들기 · SQL 실행 · 로그 보기 (2-5 · 2-6)"), ("Playwright", "브라우저 열기 · 클릭 · 화면 확인 (2-7)"),
           ("Notion", "기획서 · 개발 계획 페이지 읽기"), ("Figma", "디자인 파일 → 화면 코드")]
    rows = "".join(f'<div class="v2u3hr" style="--d:{.5 + i * .5:.2f}s"><i class="v2u3wire"></i><div class="v2u3hs"><b>{n}</b><span>{x}</span></div></div>'
                   for i, (n, x) in enumerate(srv))
    return (f'<div class="v2u3hub"><div class="v2u3core"><b>Claude Code</b><span>MCP 클라이언트</span></div>'
            f'<div class="v2u3hrs">{rows}</div></div>')


def slides():
    return [
        # ── API
        light("앱이 모르는 정보", viz2.pair(
            "공휴일을 직접 입력", [("목록", "해마다 사람이 입력"), ("대체공휴일 · 임시공휴일", "발표 뒤 다시 수정"), ("틀리면", "공휴일이 기한으로 들어감")],
            "가진 곳에 묻기 · API", [("목록", "한국천문연구원 특일 정보"), ("갱신", "제공하는 쪽이 관리"), ("앱이 할 일", "연도 · 월을 보내고 답 받기")])
              + note("API", "다른 프로그램의 기능 · 데이터를 정해진 형식으로 요청하는 창구"), T),
        light("메뉴판과 주문서", phmap("v2_u3_menu.webp", "메뉴판을 보고 주문하는 손님", *GEN, viz2.maprows([
            ("다른 가게 주방", "공휴일 서버", "한국천문연구원 · 1-6 의 주방 = 서버"), ("메뉴판", "API 목록", "공휴일 · 국경일 · 24절기"),
            ("주문서 양식", "요청 형식", "연도 · 월 · 서비스 키"), ("회원 카드", "서비스 키", "이용자 확인 (2-6)"),
            ("받은 음식", "응답", "날짜 · 이름 · 휴일 여부")], "식당", "API")), T),
        light("API 요청과 응답", exchange()
              + note("형식", "메뉴판에 없는 주문 · 양식이 틀린 주문은 오류 응답")
              + src(API_DOC), T),
        light("요청과 응답 읽기", codemap([
            ("getRestDeInfo", "공휴일 정보 조회 · 메뉴 이름"),
            ("solYear=2026  solMonth=12", "2026년 12월"),
            ("ServiceKey=내 서비스 키", "공공데이터포털에서 받은 키"),
            ("locdate: 20261225", "날짜 · 2026-12-25"),
            ('dateName: "기독탄신일"', "공휴일 이름"),
            ('isHoliday: "Y"', "쉬는 날 · 기한으로 받지 않음")], ask="「2026년 12월 공휴일 알려 줘」", title="요청 · 응답")
              + src(API_DOC), T),
        # ── MCP
        light("Claude Code와 Supabase 연결", relay()
              + note("MCP 연결 뒤", "Claude Code 가 Supabase 에 직접 실행 · 결과까지 확인"), T),
        light("USB-C 포트", phmap("usbc_port.webp", "노트북의 USB-C 포트", "사진 · Logant547 · CC BY 4.0",
                                    "https://commons.wikimedia.org/wiki/File:USB-C_connector_on_a_laptop.jpg", viz2.maprows([
            ("노트북", "Claude Code", "도구를 쓰는 쪽"), ("USB-C 규격", "MCP", "연결 · 주고받는 형식"),
            ("모니터 · 외장 디스크", "MCP 서버", "Supabase · 브라우저 · 노션"),
            ("꽂으면 기능을 알림", "도구 목록", "list_tables · execute_sql …")], "USB-C", "MCP"))
              + note("공식 소개", "「MCP 는 AI 앱을 위한 USB-C 포트」 — modelcontextprotocol.io · 원문 Think of MCP like a USB-C port"), T),
        light("API와 MCP", lanes()
              + viz2.pair(
                  "API", [("부르는 쪽", "내 앱 코드"), ("형식", "서비스마다 다름"), ("쓰는 때", "이용자가 앱을 쓸 때")],
                  "MCP", [("부르는 쪽", "Claude Code · AI"), ("형식", "하나의 규격 · 말로 요청"), ("쓰는 때", "내가 앱을 만들 때")]), T),
        light("앱 개발용 MCP", hub()
              + src(("Supabase MCP", "https://supabase.com/docs/guides/getting-started/mcp"),
                    ("Playwright MCP", "https://github.com/microsoft/playwright-mcp"), MCP_DOC), T),
        light("Supabase MCP 대화 예", chat([
            ("me", "Supabase 에 팀 할 일 표 만들어 줘. members 와 tasks 두 개, owner_id 로 연결"),
            ("ai", "apply_migration 으로 표 2개를 만들까요?\nmembers(id · name · email) · tasks(… owner_id → members.id)"),
            ("me", "응"),
            ("ai", "완료 · list_tables 결과 members · tasks")], "Claude Code 대화 예")
              + note("연결 · 권한", "등록 명령 · 로그인 · 읽기 전용 설정은 2-6"), T),
    ]


CSS = """
  /* 2-3 · 요청과 응답 */
  .v2u3ex{display:grid; grid-template-columns:200px 1fr 220px; gap:16px; align-items:center; margin:6px 0 16px;}
  .v2u3end{border:2px solid #1F3A5F; border-radius:16px; padding:22px 16px; text-align:center; background:#fff; min-height:160px; display:flex; flex-direction:column; justify-content:center;}
  .v2u3end b{font-size:21px; color:#16233A;} .v2u3end span{font-size:15px; color:#6B7785; margin-top:6px;}
  .v2u3end.srv{border-color:#F28C28; background:#FFF3E6;} .v2u3end.srv b{color:#E07A12;}
  .v2u3mid{display:flex; flex-direction:column; gap:16px;}
  .v2u3msg{border-radius:14px; padding:10px 16px; border:1.5px solid #D9DDE3; background:#fff; opacity:0;}
  .v2u3msg em{display:block; font-style:normal; font-size:13px; font-weight:800; margin-bottom:4px;}
  .v2u3msg pre{margin:0; font-family:var(--mono); font-size:15px; line-height:1.5; color:#1F3A5F; white-space:pre; font-variant-ligatures:none;}
  .v2u3msg.rq{border-color:#9DB7DA; background:#F2F7FF; animation:v2u3right 1.2s ease-out .4s forwards;} .v2u3msg.rq em{color:#1F4E8C;}
  .v2u3msg.rs{border-color:#F7C99A; background:#FFF8F0; animation:v2u3left 1.2s ease-out 2.0s forwards;} .v2u3msg.rs em{color:#E07A12;}
  @keyframes v2u3right{0%{opacity:0; transform:translateX(-90px)} 30%{opacity:1} 100%{opacity:1; transform:none}}
  @keyframes v2u3left{0%{opacity:0; transform:translateX(90px)} 30%{opacity:1} 100%{opacity:1; transform:none}}
  /* 2-3 · API 줄 · MCP 줄 */
  .v2u3lanes{display:flex; flex-direction:column; gap:12px; margin:0 0 14px;}
  .v2u3ln{display:flex; align-items:center; gap:10px;}
  .v2u3lh{width:70px; font-size:20px; font-weight:800; color:#16233A;}
  .v2u3lb{flex:1; border:1.5px solid #D9DDE3; border-radius:12px; padding:9px 12px; background:#fff; opacity:0; animation:v2u3in .45s ease-out var(--d) forwards;}
  .v2u3lb b{display:block; font-size:17px; color:#16233A;} .v2u3lb span{font-size:13.5px; color:#3A4657;}
  .v2u3lb.hl{border-color:#F28C28; background:#FFF3E6;} .v2u3lb.hl b{color:#E07A12;}
  .v2u3la{font-style:normal; font-size:20px; font-weight:800; color:#F28C28; opacity:0; animation:v2u3in .3s ease-out var(--d) forwards;}
  /* 2-3 · 사람 손 vs MCP */
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
  /* 2-3 · MCP 허브 */
  .v2u3hub{display:grid; grid-template-columns:220px 1fr; gap:28px; align-items:center; margin:4px 0 14px;}
  .v2u3core{border:2.5px solid #F28C28; background:#FFF3E6; border-radius:18px; padding:30px 16px; text-align:center;}
  .v2u3core b{display:block; font-size:24px; color:#E07A12;} .v2u3core span{font-size:15px; color:#3A4657;}
  .v2u3hrs{display:flex; flex-direction:column; gap:12px; border-left:4px solid #F28C28; padding:4px 0;} .v2u3core{position:relative;} .v2u3core::after{content:""; position:absolute; right:-28px; top:50%; width:28px; height:4px; background:#F28C28;}
  .v2u3hr{display:grid; grid-template-columns:110px 1fr; align-items:center;}
  .v2u3wire{display:block; height:4px; background:#F28C28; border-radius:2px; transform-origin:left; transform:scaleX(0); animation:v2u3wire .45s ease-out var(--d) forwards;}
  .v2u3hs{border:1.5px solid #D9DDE3; border-left:5px solid #1F3A5F; border-radius:12px; padding:10px 16px; background:#fff; opacity:0; animation:v2u3in .4s ease-out calc(var(--d) + .4s) forwards;}
  .v2u3hs b{display:block; font-size:19px; color:#16233A;} .v2u3hs span{font-size:15px; color:#3A4657;}
  @keyframes v2u3wire{to{transform:scaleX(1)}}
  @keyframes v2u3in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u3wire{transform:none; animation:none} .v2u3rs,.v2u3ra,.v2u3cnt span,.v2u3hs,.v2u3msg,.v2u3lb,.v2u3la{opacity:1; animation:none}}
"""
