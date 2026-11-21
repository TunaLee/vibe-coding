"""vibe2 공통 도구 — 2부 표지 · 2부 지도 · 다음 단원. 화면 · 대화 · 실습 진행 · 코드 뜻은 v1kit 것을 그대로 쓴다.

바이브코딩 온라인 강의 2부 — 심화. 단원마다 HTML 한 파일(docs/2-N-이름.html).
공통 예제 = 팀 할 일 보드 시작 버전(labs/team_board · 1부 방식)에 DB · 로그인 · 외부 API · MCP 를 붙인 「팀 할 일 보드 v2」 (labs/team_board_v2).
이어지는 산출물: 2-4 기획서 · 개발 계획 v2 → 2-5 Supabase 저장 · 로그인 → 2-6 API 키 · MCP → 2-7 테스트 · 리뷰 → 2-8 배포 · 로그 → 2-9 운영 체크리스트
"""
from deck import light
from hx import note
from v1kit import brief as _brief, chat, codemap, shot  # noqa: F401  (단원 모듈이 v2kit 에서 가져다 쓴다)

FOLDER = "labs/team_board_v2"

# (단원, 제목, 분 — 화면에 쓰지 않음, 이 단원에서 남는 것)
UNITS = [
    ("2-1", "미리보기", 5, "2부 커리큘럼"),
    ("2-2", "데이터베이스", 15, "표 · 행 · 열 · Supabase"),
    ("2-3", "API · MCP", 20, "API 와 MCP 차이"),
    ("2-4", "기획 · 요구사항", 25, "기획서 · 개발 계획 v2"),
    ("2-5", "데이터 다루기", 35, "저장 · 조회 · 로그인"),
    ("2-6", "외부 서비스 연결", 35, "API 키 · MCP 연결"),
    ("2-7", "품질 관리 · 테스트 · 디버깅", 35, "테스트 · 수정 기록"),
    ("2-8", "배포 · 모니터링", 20, "환경변수 · 로그"),
    ("2-9", "마무리", 10, "운영 체크리스트"),
]
BY = {u[0]: u for u in UNITS}

SLUG = {"2-1": "preview", "2-2": "database", "2-3": "api-mcp", "2-4": "planning", "2-5": "data",
        "2-6": "integrations", "2-7": "quality", "2-8": "monitoring", "2-9": "wrap-up"}


def file_of(u):
    return f"#u-{u}"


def cover(u):
    _, title, _, _ = BY[u]
    return f'''<section id="u-{u}" class="slide dk cover-dk" data-title="{u} {title}">
  <div class="glow"></div>
  <div class="kick">바이브코딩 · {u}</div>
  <h1>{title}</h1>
</section>'''


def roadmap(u):
    """2부 지도 — 아홉 단원 · 현재 단원 강조 · 지난 단원은 흐리게."""
    cur = [x[0] for x in UNITS].index(u)
    cells = []
    for i, (c, t, _, out) in enumerate(UNITS):
        cls = "on" if i == cur else ("done" if i < cur else "")
        cells.append(f'<a class="v1u {cls}" href="{file_of(c)}"><span class="c">{c}</span><b>{t}</b><small>{out}</small></a>')
    return light("2부 커리큘럼", f'<div class="v1map v2map">{"".join(cells)}</div>'
                 + note("공통 예제", "팀 할 일 보드 + DB · 로그인 · 외부 API · MCP"), u)


def nextup(u):
    i = [x[0] for x in UNITS].index(u)
    out = UNITS[i][3]
    if i + 1 < len(UNITS):
        c, t, _, nout = UNITS[i + 1]
        nxt = f'<a class="v1next" href="{file_of(c)}"><span>{c}</span><b>{t}</b><small>→ {nout}</small></a>'
    else:
        nxt = '<a class="v1next" href="part3.html#u-3-1"><span>3부</span><b>하네스 엔지니어링</b><small>→ 내 업무 에이전트</small></a>'
    return f'''<section class="slide dk" data-title="다음 단원">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="v1end"><div class="v1got"><span>{u} 산출물</span><b>{out}</b></div>{nxt}</div>
</section>'''


def brief(no, u, steps, slots, keys, checks, stuck, folder="내 프로젝트 폴더", example=FOLDER):
    return _brief(no, u, steps, slots, keys, checks, stuck, folder, example)


CSS = """
  /* vibe2 · 지도 (아홉 칸 · 3열) */
  .v2map{grid-template-columns:repeat(3,1fr); gap:12px;} .v2map .v1u{min-height:96px; padding:14px 18px;}
  .v2map .v1u b{font-size:20px;} .v2map .v1u small{font-size:14px;}
"""
