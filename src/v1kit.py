"""vibe1 공통 도구 — 단원 표지 · 1부 지도 · 다음 단원 · 화면 · 대화 · 실습 진행. 단원 모듈(v1_u1 … v1_u8)이 쓴다.

바이브코딩 온라인 강의 1부 — 입문. 단원마다 HTML 한 파일(docs/1-N-이름.html).
공통 예제 = 미니 노션 (labs/mini_notion). 수강생은 같은 순서로 자기 아이디어를 만든다.
이어지는 산출물: 1-3 기획서.md → 1-4 개발계획.md → 1-5 첫 커밋 → 1-6 앱 → 1-7 배포 주소 → 1-8 회고 → 2부
"""
from deck import light
from hx import note

FOLDER = "labs/mini_notion"

# (단원, 제목, 분 — 화면에 쓰지 않음, 이 단원에서 남는 것)
UNITS = [
    ("1-1", "바이브코딩이란", 20, "바이브코딩 개념"),
    ("1-2", "도구 · 실습 환경", 30, "계정 3개 · 설치"),
    ("1-3", "기획서 작성", 30, "기획서.md"),
    ("1-4", "개발 계획", 30, "개발계획.md"),
    ("1-5", "Git · GitHub 기초", 10, "첫 커밋"),
    ("1-6", "바이브코딩 실습", 40, "동작하는 앱"),
    ("1-7", "배포", 30, "공유 주소"),
    ("1-8", "마무리", 10, "회고 → 2부"),
]
BY = {u[0]: u for u in UNITS}


SLUG = {"1-1": "vibe-coding", "1-2": "setup", "1-3": "planning", "1-4": "dev-plan", "1-5": "git",
        "1-6": "build", "1-7": "deploy", "1-8": "wrap-up"}


def file_of(u):
    return f"#u-{u}"


def cover(u):
    _, title, mins, _ = BY[u]
    return f'''<section id="u-{u}" class="slide dk cover-dk" data-title="{u} {title}">
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
    return light("1부 커리큘럼", f'<div class="v1map">{"".join(cells)}</div>'
                 + note("공통 예제", "미니 노션 · 같은 순서로 내 아이디어를 만든다"), u)


def nextup(u):
    """마지막 장 — 이 단원에서 남은 것 + 다음 단원 링크."""
    i = [x[0] for x in UNITS].index(u)
    _, _, _, out = UNITS[i]
    if i + 1 < len(UNITS):
        c, t, m, nout = UNITS[i + 1]
        nxt = f'<a class="v1next" href="{file_of(c)}"><span>{c}</span><b>{t}</b><small>→ {nout}</small></a>'
    else:
        nxt = '<a class="v1next" href="part2.html#u-2-1"><span>2부</span><b>바이브 코딩 심화</b><small>→ DB · 외부 연동 · 품질 관리</small></a>'
    return f'''<section class="slide dk" data-title="다음 단원">
  <div class="coord"><b></b> / <span class="tot"></span></div>
  <div class="v1end"><div class="v1got"><span>{u} 산출물</span><b>{out}</b></div>{nxt}</div>
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


def brief(no, u, steps, slots, keys, checks, stuck, folder="내 프로젝트 폴더", example=FOLDER, slot_title="요청 항목"):
    """실습 진행 — 두 장으로 나눈다. ① 순서 + 확인 ② 요청에 들어갈 것.
    keys · stuck · folder · example 은 화면에 내지 않는다(호출부 호환용)."""
    st = "".join(f'<li style="--d:{i * .25:.2f}s"><em>{i + 1}</em><span>{x}</span></li>' for i, x in enumerate(steps))
    ck = "".join(f"<li>{x}</li>" for x in checks)
    a = light(f"실습 {no} 순서", f'<ol class="v1st">{st}</ol><div class="qk2"><b>확인</b><ul>{ck}</ul></div>', u)
    sl = "".join(f'<div class="v1sl" style="--d:{i * .2:.2f}s"><b>{k}</b><span>{v}</span></div>' for i, (k, v) in enumerate(slots))
    if not slots:
        return a
    b = light(f"실습 {no} {slot_title}", f'<div class="v1sls">{sl}</div>', u)
    return a + "\n" + b




def go(text, url):
    """수강생이 눌러서 들어갈 주소 — 새 탭으로 연다."""
    return f'<a class="go" href="{url}" target="_blank" rel="noopener">{text}</a>'


def labcard(no, title, u, inp, out, parts=(), files="", cards=()):
    """실습 소개 — 입력 → 산출물 한 줄 + 구성 칩. cards=(이름, 할 일, 결과) 를 주면 「할 일 → 결과」 카드로. 단계 · 확인은 다음 「순서」 장에."""
    from deck import coord
    if cards:
        cs = "".join(f'<div class="c" style="--d:{.3 + i * .4:.1f}s"><em>{i + 1}</em><b>{n}</b><p>{d}</p><i>↓</i><span>{r}</span></div>'
                     for i, (n, d, r) in enumerate(cards))
        return f'''<section class="slide lt labs" data-title="[실습 {no}] {title}">
  {coord()}
  <div class="eyebrow"><span class="tag">{u}</span><span class="labtag">실습 {no}</span></div>
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body"><div class="v1lk">{cs}</div></div>
</section>'''
    ch = "".join(f'<span style="--d:{.5 + i * .2:.1f}s">{p}</span>' for i, p in enumerate(parts))
    return f'''<section class="slide lt labs" data-title="[실습 {no}] {title}">
  {coord()}
  <div class="eyebrow"><span class="tag">{u}</span><span class="labtag">실습 {no}</span></div>
  <h2 class="s-title sm">{title}</h2>
  <div class="rule"></div>
  <div class="body"><div class="v1lc">
    <div class="io"><div class="b in"><small>입력</small><b>{inp}</b></div><i>→</i><div class="b out"><small>산출물</small><b>{out}</b></div></div>
    {f'<div class="pt">{ch}</div>' if parts else ''}
    {f'<div class="fl">실습 파일 · {files}</div>' if files else ''}
  </div></div>
</section>'''



def tstep(no, i, name, u, img=None, alt="", term=None, rows=(), need=None, srcs=(), ask=None):
    """실습 단계 화면(넓게) — 위에 실제 화면 · 아래에 할 일 칩."""
    import viz2
    from hx import code, esc
    from stats_hx import src
    if ask:
        lines = "".join(f"<p>{esc(x)}</p>" for x in ask[1].split("\n"))
        body = f'<div class="v1ask"><span>{ask[0]}</span>{lines}</div>'
    elif isinstance(img, (list, tuple)):
        ims = "".join(f'<img src="img/{x}" alt="{alt}"/>' for x in img)
        body = f'<div class="v1ts v1ts2"><span class="v1tsl">나오는 화면 · 예</span>{ims}</div>'
    elif img:
        body = f'<div class="v1ts"><img src="img/{img}" alt="{alt}"/></div>'
    elif term:
        body = '<div class="v1tt">' + code(term[0], esc(term[1])) + "</div>"
    else:
        body = (f'<div class="v1ts"><div class="need-img"><span class="nk">캡처 필요</span><span class="nd">{need}</span>'
                '<span class="nm2">강사 화면 캡처로 교체</span></div></div>')
    return light(f"실습 {no} · {i}단계 {name}", body + viz2.tiles(list(rows), len(rows)) + (src(*srcs) if srcs else ""), u)


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
  /* 눌러서 들어갈 주소 */
  a.go{color:#1F6FEB; font-weight:700; text-decoration:underline; text-underline-offset:3px;}
  a.go:hover{color:#F28C28;}
  /* 실습 단계 화면(넓게) */
  .v1ts{display:flex; justify-content:center; margin:0 0 18px;}
  .v1ts img{max-width:100%; max-height:310px; border-radius:10px; box-shadow:0 8px 24px rgba(22,35,58,.22);}
  .v1ts .need-img{width:760px; min-height:300px;}
  .v1tt{max-width:860px; margin:0 auto 18px;}
  .v1ts2{position:relative; gap:24px; padding-top:30px;}
  .v1ts2 img{max-height:300px;}
  .v1tsl{position:absolute; top:0; left:50%; transform:translateX(-50%); font-size:15px; font-weight:700; color:#6B7686;}
  /* 실습 요청 단계 — 입력창에 쓸 문장 */
  .v1ask{max-width:900px; margin:20px auto 40px; border:2px solid #16233A; border-radius:16px; padding:20px 30px 22px; background:#fff; box-shadow:0 8px 24px rgba(22,35,58,.12);}
  .v1ask span{display:block; font-size:16px; font-weight:700; color:#6B7686; margin-bottom:10px;}
  .v1ask p{margin:0; font-size:30px; font-weight:700; color:#16233A; line-height:1.5;}
  /* 실습 소개 — 할 일 → 결과 카드 */
  .v1lk{display:grid; grid-template-columns:repeat(3,1fr); gap:22px; margin-top:34px;}
  .v1lk .c{background:#F4F6F9; border-radius:18px; padding:24px 24px 22px; display:flex; flex-direction:column; align-items:flex-start; opacity:0; animation:v1stIn .45s var(--d) forwards;}
  .v1lk em{width:38px; height:38px; border-radius:50%; background:#16233A; color:#fff; font-style:normal; font-weight:800; font-size:19px; display:flex; align-items:center; justify-content:center; margin-bottom:14px;}
  .v1lk b{font-size:26px; color:#16233A; margin-bottom:10px;}
  .v1lk p{margin:0; font-size:18px; color:#4A5563; line-height:1.5; min-height:54px;}
  .v1lk i{font-style:normal; color:#F28C28; font-size:24px; font-weight:800; margin:10px 0 6px;}
  .v1lk span{font-size:19px; font-weight:700; color:#16233A; background:#FFF3E6; box-shadow:inset 0 0 0 2px #F28C28; border-radius:12px; padding:10px 14px; align-self:stretch;}
  /* 실습 소개 — 입력 → 산출물 */
  .v1lc{display:flex; flex-direction:column; align-items:center; gap:34px; margin-top:40px;}
  .v1lc .io{display:flex; align-items:center; gap:26px;}
  .v1lc .b{min-width:330px; border-radius:18px; padding:26px 34px; text-align:center; background:#F4F6F9;}
  .v1lc .b.out{background:#FFF3E6; box-shadow:inset 0 0 0 2px #F28C28;}
  .v1lc .b small{display:block; font-size:15px; font-weight:700; color:#6B7785; margin-bottom:8px;}
  .v1lc .b b{font-size:30px; color:#16233A;}
  .v1lc .io i{font-style:normal; font-size:40px; color:#F28C28; font-weight:800;}
  .v1lc .pt{display:flex; gap:14px;}
  .v1lc .pt span{background:#16233A; color:#fff; font-size:19px; font-weight:700; padding:11px 22px; border-radius:24px; opacity:0; animation:v1stIn .4s var(--d) forwards;}
  .v1lc .fl{font-size:16px; color:#6B7785;}
  /* 실습 순서 · 요청 칸 — 한 장에 한 가지 */
  .v1st{list-style:none; margin:4px 0 14px; padding:0; display:flex; flex-direction:column; gap:9px;}
  .v1st li{display:flex; align-items:center; gap:16px; background:#F4F6F9; border-radius:14px; padding:11px 20px;
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
