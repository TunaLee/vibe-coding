"""vibe1 공통 도구 — 단원 표지 · 1부 지도 · 다음 단원 · 화면 · 대화 · 실습 진행. 단원 모듈(v1_u1 … v1_u8)이 쓴다.

바이브코딩 온라인 강의 1부 — 입문. 단원마다 HTML 한 파일(docs/1-N-이름.html).
공통 예제 = 회의실 예약 페이지 (labs/room_booking). 수강생은 같은 순서로 자기 아이디어를 만든다.
이어지는 산출물: 1-3 기획서.md → 1-4 PRD.md → 1-5 첫 커밋 → 1-6 앱 → 1-7 배포 주소 → 1-8 회고 → 2부
"""
from deck import light
from hx import note

FOLDER = "labs/room_booking"

# (단원, 제목, 분 — 화면에 쓰지 않음, 이 단원에서 남는 것)
UNITS = [
    ("1-1", "바이브코딩이란", 20, "바이브코딩 개념"),
    ("1-2", "도구 · 실습 환경", 30, "계정 3개 · 설치"),
    ("1-3", "기획서 작성", 30, "기획서.md"),
    ("1-4", "요구사항 정의 (PRD)", 30, "PRD.md"),
    ("1-5", "Git · GitHub 기초", 10, "첫 커밋"),
    ("1-6", "바이브코딩 실습", 40, "동작하는 앱"),
    ("1-7", "배포", 30, "공유 주소"),
    ("1-8", "마무리", 10, "회고 → 2부"),
]
BY = {u[0]: u for u in UNITS}


SLUG = {"1-1": "vibe-coding", "1-2": "setup", "1-3": "planning", "1-4": "prd", "1-5": "git",
        "1-6": "build", "1-7": "deploy", "1-8": "wrap-up"}


def file_of(u):
    return f"{u}-{SLUG[u]}.html"


def cover(u):
    _, title, mins, _ = BY[u]
    return f'''<section class="slide dk cover-dk active" data-title="표지">
  <div class="glow"></div>
  <div class="kick">바이브코딩 · {u}</div>
  <h1>{title}</h1>
</section>'''


def roadmap(u):
    """1부 지도 — 여덟 단원과 단원마다 남는 산출물 · 현재 단원 강조 · 지난 단원은 흐리게."""
    cur = [x[0] for x in UNITS].index(u)
    cells = []
    for i, (c, t, m, out) in enumerate(UNITS):
        cls = "on" if i == cur else ("done" if i < cur else "")
        cells.append(f'<a class="v1u {cls}" href="{file_of(c)}"><span class="c">{c}</span><b>{t}</b><small>{out}</small></a>')
    return light("1부 지도", f'<div class="v1map">{"".join(cells)}</div>'
                 + note("공통 예제", "회의실 예약 페이지 · 같은 순서로 내 아이디어를 만든다"), u)


def nextup(u):
    """마지막 장 — 이 단원에서 남은 것 + 다음 단원 링크."""
    i = [x[0] for x in UNITS].index(u)
    _, _, _, out = UNITS[i]
    if i + 1 < len(UNITS):
        c, t, m, nout = UNITS[i + 1]
        nxt = f'<a class="v1next" href="{file_of(c)}"><span>{c}</span><b>{t}</b><small>→ {nout}</small></a>'
    else:
        nxt = '<div class="v1next"><span>2부</span><b>바이브 코딩 심화</b><small>→ DB · 외부 연동 · 품질 관리</small></div>'
    return f'''<section class="slide dk" data-title="다음 단원">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="v1end"><div class="v1got"><span>{u}에서 남은 것</span><b>{out}</b></div>{nxt}</div>
</section>'''


def shot(img, cap, side=(), wide=False):
    """실제 화면 캡처 + 오른쪽 설명 줄. side: (머리, 한 줄)."""
    s = "".join(f'<div class="v1sd"><b>{h}</b><span>{x}</span></div>' for h, x in side)
    return (f'<div class="v1shot{" w" if wide else ""}"><figure><img src="img/{img}" alt="{cap}"/><figcaption>{cap}</figcaption></figure>'
            f'{f"<div class=v1side>{s}</div>" if s else ""}</div>')


def chat(turns, label="대화 예"):
    """대화 화면 예 — turns: ("me" | "ai", 문장). 줄바꿈은 \\n."""
    b = "".join(f'<div class="v1b {w}"><span>{"나" if w == "me" else "Claude"}</span><p>{t.replace(chr(10), "<br/>")}</p></div>' for w, t in turns)
    return f'<div class="v1chat"><div class="v1ch">{label}</div>{b}</div>'


def brief(no, u, steps, slots, keys, checks, stuck, folder="내 프로젝트 폴더", example=FOLDER, slot_title="요청에 들어갈 것"):
    """실습 진행 — 두 장으로 나눈다. ① 순서 + 확인 ② 요청에 들어갈 것.
    keys · stuck · folder · example 은 화면에 내지 않는다(호출부 호환용)."""
    st = "".join(f'<li style="--d:{i * .25:.2f}s"><em>{i + 1}</em><span>{x}</span></li>' for i, x in enumerate(steps))
    ck = "".join(f"<li>{x}</li>" for x in checks)
    a = light(f"실습 {no} 순서", f'<ol class="v1st">{st}</ol><div class="qk2"><b>확인</b><ul>{ck}</ul></div>', u)
    sl = "".join(f'<div class="v1sl" style="--d:{i * .2:.2f}s"><b>{k}</b><span>{v}</span></div>' for i, (k, v) in enumerate(slots))
    b = light(f"실습 {no} {slot_title}", f'<div class="v1sls">{sl}</div>', u)
    return a + "\n" + b


def codemap(rows, ask="", title=""):
    """코드 줄 → 우리말 뜻 — 입문자용. rows: (코드 한 줄, 뜻). ask = 사람의 요청 한 문장(위에 표시).
    줄이 0.35초 간격으로 차례로 나타나고 멈춘다."""
    from hx import esc
    head = (f'<div class="v1cmask"><span>요청</span><b>{ask}</b></div>' if ask else "")
    r = "".join(f'<div class="v1cmr" style="--d:{.3 + i * .35:.2f}s"><code>{esc(c)}</code><i>{"→" if m else ""}</i><span>{m}</span></div>'
                for i, (c, m) in enumerate(rows))
    t = f'<div class="v1cmt"><span>{title}</span><span>뜻</span></div>' if title else ""
    return f'{head}<div class="v1cmap">{t}{r}</div>'


CSS = """
  /* 실습 순서 · 요청 칸 — 한 장에 한 가지 */
  .v1st{list-style:none; margin:6px 0 18px; padding:0; display:flex; flex-direction:column; gap:12px;}
  .v1st li{display:flex; align-items:center; gap:16px; background:#F4F6F9; border-radius:14px; padding:14px 20px;
    opacity:0; animation:v1stIn .4s var(--d) forwards;}
  .v1st em{flex:none; width:36px; height:36px; border-radius:50%; background:#16233A; color:#fff; font-style:normal; font-weight:800;
    font-size:18px; display:flex; align-items:center; justify-content:center;}
  .v1st span{font-size:22px; font-weight:600; color:#16233A;}
  .v1sls{display:grid; grid-template-columns:1fr; gap:14px; margin-top:8px;}
  .v1sl{background:#FFF7EE; border:2px solid #F2C58F; border-radius:16px; padding:16px 24px; display:flex; align-items:baseline; gap:20px; opacity:0; animation:v1stIn .4s var(--d) forwards;}
  .v1sl b{flex:none; width:130px; font-size:18px; color:#C76A12;} .v1sl span{font-size:24px; font-weight:700; color:#16233A; line-height:1.4;}
  @keyframes v1stIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v1st li,.v1sl{opacity:1; animation:none}}
  /* vibe1 · 표지 · 지도 · 다음 단원 */
  .v1cmin{margin-top:26px; font-family:var(--mono); font-size:18px; color:#F28C28; font-weight:700; position:relative;}
  .v1map{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin:6px 0 18px;}
  .v1u{display:flex; flex-direction:column; gap:6px; padding:20px 20px; border:2px solid #D9DDE3; border-radius:16px; background:#fff; text-decoration:none; min-height:150px;}
  .v1u .c{font-family:var(--mono); font-size:15px; font-weight:800; color:#6B7785;}
  .v1u b{font-size:23px; color:#16233A; line-height:1.25;} .v1u small{font-size:16px; color:#3A4657; margin-top:auto;}
  .v1u.done{opacity:.5;} .v1u.on{border-color:#F28C28; background:#FFF3E6; box-shadow:0 6px 18px rgba(242,140,40,.18);}
  .v1u.on .c{color:#F28C28;}
  .v1end{position:absolute; inset:0; display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:center; padding:0 90px;}
  .v1got span, .v1next span{display:block; font-family:var(--mono); font-size:16px; color:#9AA6B5; font-weight:700; margin-bottom:12px;}
  .v1got b{font-size:46px; line-height:1.15; color:#fff;}
  .v1next{display:block; border:2px solid #F28C28; border-radius:22px; padding:34px 36px; text-decoration:none; background:rgba(242,140,40,.08);}
  .v1next b{display:block; font-size:40px; color:#fff; line-height:1.15;} .v1next small{display:block; margin-top:14px; font-size:20px; color:#F7C99A;}
  /* vibe1 · 화면 캡처 */
  .v1shot{display:grid; grid-template-columns:1.55fr 1fr; gap:26px; align-items:center;} .v1shot.w{grid-template-columns:1fr;}
  .v1shot figure{margin:0;} .v1shot img{width:100%; max-height:440px; object-fit:contain; object-position:top; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#fff;}
  .v1shot.w img{max-height:450px;}
  .v1shot figcaption{font-size:14px; color:#6B7785; margin-top:8px;}
  .v1side{display:flex; flex-direction:column; gap:12px;}
  .v1sd{border-left:5px solid #F28C28; background:#fff; border-radius:10px; padding:12px 16px; border-top:1px solid #EEF0F3; border-right:1px solid #EEF0F3; border-bottom:1px solid #EEF0F3;}
  .v1sd b{display:block; font-size:20px; color:#16233A;} .v1sd span{font-size:16px; color:#3A4657; line-height:1.45;}
  /* vibe1 · 대화 예 */
  .v1chat{border:1.5px solid #D9DDE3; border-radius:16px; background:#F7F8FA; padding:16px 20px; display:flex; flex-direction:column; gap:10px;}
  .v1ch{font-size:13px; font-weight:800; color:#6B7785; letter-spacing:.03em;}
  .v1b{display:flex; flex-direction:column; max-width:82%;} .v1b span{font-size:12px; font-weight:800; color:#6B7785; margin-bottom:3px;}
  .v1b p{margin:0; font-size:17px; line-height:1.5; padding:10px 15px; border-radius:14px; background:#fff; border:1px solid #E3E6EA; color:#16233A;}
  .v1b.me{align-self:flex-end; align-items:flex-end;} .v1b.me p{background:#FFF3E6; border-color:#F7C99A;}
  /* vibe1 · 코드 줄 → 뜻 */
  .v1cmask{display:flex; gap:14px; align-items:center; margin:0 0 14px; padding:12px 18px; border-radius:12px; background:#FFF3E6; border:1.5px solid #F7C99A;}
  .v1cmask span{font-size:13px; font-weight:800; color:#E07A12;} .v1cmask b{font-size:21px; color:#16233A;}
  .v1cmap{border:1.5px solid #D9DDE3; border-radius:14px; overflow:hidden; background:#fff;}
  .v1cmt{display:grid; grid-template-columns:1.25fr 40px 1fr; padding:9px 18px; background:#F4F6F9; font-size:13px; font-weight:800; color:#6B7785;}
  .v1cmt span:last-child{grid-column:3;}
  .v1cmr{display:grid; grid-template-columns:1.25fr 40px 1fr; align-items:center; padding:9px 18px; border-top:1px solid #EEF0F3; opacity:0; animation:v1cutIn .45s ease-out var(--d) forwards;}
  .v1cmr code{font-family:var(--mono); font-size:15.5px; color:#1F3A5F; white-space:pre; background:none; padding:0; font-variant-ligatures:none; font-feature-settings:'liga' 0, 'calt' 0;}
  .v1cmr i{font-style:normal; color:#F28C28; font-weight:800; text-align:center;}
  .v1cmr span{font-size:17px; color:#16233A; font-weight:600;}
  @keyframes v1cutIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  @media print{.v1cmr{opacity:1; animation:none}}
"""
