"""1-1 바이브코딩이란 — 실습 없음.

비유 한 줄로 끝까지 잇는다.
  코딩 = 사과를 처음 보는 원시인(컴퓨터)에게 원시인 말로 하나하나 가르치기 · 빠뜨리면 그대로 실수(버그)
  바이브코딩 = 우리말로 말하면 통역사(AI)가 원시인 말(코드)로 풀어 쓰고 · 나는 결과를 보고 판단
→ 말의 유래 · 흐름 · 내 일과 AI 일 · 만든 것 · 한계(통역사도 빠뜨린다) · 1부 순서 · 완성 화면.
사실 출처: scratchpad/v1_facts.md (Karpathy · Collins · levels.io · MenuGen · Veracode · Wiz · Replit)
"""
import viz2
from anim import BG, G, N, O, OK, R, S, W, _D, _t
from deck import flow, light
from hx import METR_TH, code, esc, metr_chart, note
from stats_hx import big, quote, src
from v1kit import chat, codemap, shot

T = "1-1"
ERAS = [  # (해, 이름, 도구, 사람 몫 %, AI 몫, 사람 몫, AI가 파악하는 것) — 막대는 모양만 · 측정값 아님
    ("2021", "자동완성", "GitHub Copilot", 85, "다음 줄 · 함수 제안", "위치 · 구조 결정 · 작성 · 실행", "앞뒤 코드"),
    ("2022", "대화형", "ChatGPT", 55, "요청한 코드 작성", "붙일 위치 찾기 · 붙여넣기 · 실행", "요청 문장"),
    ("2025", "위임형", "Claude Code", 15, "파일 찾기 · 수정 · 실행 · 확인", "목표 · 결과 판단", "목표"),
]


def eras():
    """AI 코딩 도구 3단 계단 — 칸이 차례로 나타나고 사람 몫 막대가 줄어든다."""
    c = ""
    for i, (y, name, tool, h, ai, me, grasp) in enumerate(ERAS):
        c += (f'<div class="v1era v1cut" style="--d:{i * .8:.1f}s; margin-top:{(2 - i) * 34}px">'
              f'<div class="yr">{y}</div><b>{name}</b><span class="tl">{tool}</span>'
              f'<div class="bar"><i class="me" style="width:{h}%"></i><i class="ai" style="width:{100 - h}%"></i></div>'
              f'<div class="row"><em class="me">사람</em><small>{me}</small></div>'
              f'<div class="row"><em class="ai">AI</em><small>{ai}</small></div>'
              f'<div class="grasp">AI가 파악 · <b>{grasp}</b></div></div>')
    return f'<div class="v1eras">{c}</div>'


def autocomplete_anim():
    """편집기 · 로그인 함수 첫 줄 입력 → AI가 회색으로 검사 줄 제안 → Tab 수락 · 두 번 반복 후 정지 (약 9초).
    참고: GitHub Copilot 「inline suggestion」 화면 (회색 제안 → Tab 수락)."""
    from hx import esc
    def typed(txt, t0, dur):
        n = len(txt)
        return (f'<span class="ty" style="--n:{n}ch; animation:v1type {dur}s steps({n}) {t0}s forwards, '
                f'v1caret .5s step-end {t0}s {int(dur / .5) + 2}">{esc(txt)}</span>')
    def ghost(txt, t_show, t_ok):
        return (f'<span class="gh" style="animation:v1ghIn .4s ease-out {t_show}s forwards, v1ghOk .35s ease-out {t_ok}s forwards">{esc(txt)}</span>')
    L = [
        ("me", "function login(email, password) {", .3, 2.2),
        ("ai", '  if (!email.includes("@"))', 2.8, 4.3),
        ("ai", '    return "이메일 형식 오류";', 2.8, 4.3),
        ("ai", "  if (password.length < 8)", 2.8, 4.3),
        ("ai", '    return "비밀번호 8자 이상";', 2.8, 4.3),
        ("ai", '  return "로그인 성공";', 2.8, 4.3),
        ("ai", "}", 2.8, 4.3),
        ("me", "loginBtn.onclick = () =>", 4.9, 1.6),
        ("ai", "  alert(login(email.value, pw.value));", 7.0, 8.2),
    ]
    rows = ""
    for i, (who, txt, a, b) in enumerate(L, 1):
        body = typed(txt, a, b) if who == "me" else ghost(txt, a, b)
        rows += f'<div class="ln"><i>{i}</i>{body}</div>'
    keys = "".join(f'<div class="v1tab" style="animation:v1tabIn 1s ease-out {t}s forwards"><kbd>Tab</kbd><span>수락</span></div>' for t in (3.5, 7.6))
    tags = "".join(f'<div class="v1sug" style="top:{y}px; animation:v1ghIn .4s ease-out {t}s forwards, v1out .3s ease-in {t + 1.6}s forwards">AI 제안 · 회색</div>'
                   for y, t in ((52, 2.8), (282, 7.0)))
    return f'<div class="v1ed"><div class="bar"><b></b><b></b><b></b><span>app.js · 편집기 화면 예</span></div><div class="code">{rows}{tags}{keys}</div></div>'


def _typed_ko(txt, t0, step=.07):
    """한 글자씩 나타나는 입력 — 글자마다 시작 시각을 따로 준다(한글 폭과 무관)."""
    from hx import esc
    return "".join(f'<span class="v1k" style="animation-delay:{t0 + i * step:.2f}s">{esc(ch)}</span>' for i, ch in enumerate(txt))


def _todo(items, t0, gap=.6, cls=""):
    return "".join(f'<div class="v1td {cls}" style="animation-delay:{t0 + i * gap:.2f}s"><i>{i + 1}</i><span>{x}</span></div>'
                   for i, x in enumerate(items))


def chat_anim(mode):
    """대화형 · 위임형 화면 애니메이션 — 한 번 재생 후 정지.
    대화형: 요청 입력 → AI 코드 조각 답 → 사람이 이어서 할 일 다섯 개.
    위임형: 목표 한 줄 → AI 도구 단계(● 진행 → ✓ 완료) 셋 → 사람 할 일 두 개.
    참고: Claude Code 문서 「How Claude Code works」 · 코딩애플 「AI 에이전트 만드는 기초 기술」 단계 표시."""
    from hx import esc
    if mode == "chat":
        ask = "로그인 화면 HTML 코드 써 줘"
        t_send = .3 + len(ask) * .07
        reply = ['<p class="v1ln" style="animation-delay:{:.1f}s">아래 코드를 login.html 로 저장하면 된다.</p>'.format(t_send + 1.0),
                 '<pre class="v1ln" style="animation-delay:{:.1f}s">{}</pre>'.format(t_send + 1.5, esc('<form>\n  <input type="email">\n  <input type="password">\n  <button>로그인</button>\n</form>'))]
        left = (f'<div class="v1cw"><div class="v1hd">채팅 화면 예</div>'
                f'<div class="v1me"><p>{_typed_ko(ask, .3)}</p></div>'
                f'<div class="v1dots" style="animation-delay:{t_send + .2:.1f}s, {t_send + .95:.1f}s"><b></b><b></b><b></b></div>'
                f'<div class="v1ai">{"".join(reply)}</div></div>')
        right = ('<div class="v1side2"><div class="v1hh">사람이 이어서 할 일</div>'
                 + _todo(["새 파일 만들기 · 이름 정하기", "코드 붙여넣기 · 저장", "브라우저로 열기", "동작 안 하면 다시 질문", "받은 코드 다시 붙여넣기"], t_send + 2.4)
                 + f'<div class="v1gr" style="animation-delay:{t_send + 5.6:.1f}s">AI가 파악 · <b>요청 문장</b></div></div>')
    else:
        ask = "로그인 화면 만들어 줘"
        t_send = .3 + len(ask) * .07
        steps = [("폴더 확인", "기존 파일 · 스타일 파악"), ("파일 작성", "login.html · login.js"), ("실행해 확인", "잘못된 이메일 → 「이메일 형식 오류」")]
        rows = ""
        for i, (h, sub) in enumerate(steps):
            t = t_send + .9 + i * 1.4
            rows += (f'<div class="v1ust" style="animation-delay:{t:.1f}s"><span class="v1ic"><span class="v1run" style="animation-delay:{t:.1f}s, {t + 1.0:.1f}s">●</span>'
                     f'<span class="v1ok" style="animation-delay:{t + 1.0:.1f}s">✓</span></span><b>{h}</b><small>{sub}</small></div>')
        t_end = t_send + .9 + 3 * 1.4
        left = (f'<div class="v1cw cc"><div class="v1hd">Claude Code 화면 예</div>'
                f'<div class="v1me"><p>{_typed_ko(ask, .3)}</p></div>{rows}'
                f'<div class="v1ai"><p class="v1ln" style="animation-delay:{t_end:.1f}s">완료 · login.html 을 열면 된다.</p></div></div>')
        right = ('<div class="v1side2"><div class="v1hh">사람이 할 일</div>'
                 + _todo(["목표 한 줄 요청", "화면에서 결과 확인"], t_end + .6, cls="me2")
                 + f'<div class="v1gr" style="animation-delay:{t_end + 1.8:.1f}s">AI가 파악 · <b>목표</b></div></div>')
    return f'<div class="v1mode">{left}{right}</div>'


LANGS = [  # (시기, 이름, 예 코드, 특징, 요리 비유)
    ("1940년대 말 ~", "어셈블리", "mov eax, 3\nadd eax, 4", "CPU 명령 하나씩", "재료 손질부터 직접"),
    ("1957 FORTRAN · 1991 Python", "고급 언어", "print(3 + 4)", "영어 단어 · 수식", "밀키트"),
    ("2025 ~", "자연어", "「3 더하기 4를\n화면에 보여 줘」", "우리말 요청 → AI가 코드 작성", "식당에서 주문"),
]


def langs():
    """어셈블리 → 고급 언어 → 자연어 — 같은 계산(3 + 4)을 세 방식으로 · 칸이 차례로 나타남."""
    from hx import esc
    c = ""
    for i, (when, name, ex, feat, cook) in enumerate(LANGS):
        c += (f'<div class="v1lang v1cut" style="--d:{i * .8:.1f}s"><div class="v1ly">{when}</div><b>{name}</b>'
              f'<pre class="{"nl" if i == 2 else ""}">{esc(ex)}</pre><div class="v1lf">{feat}</div>'
              f'<div class="v1lk">{cook}</div></div>')
        if i < 2:
            c += '<i class="v1lar">→</i>'
    return (f'<div class="v1langs">{c}</div>'
            '<div class="v1lline"><span>기계에 가까운 말</span><b></b><span>사람에 가까운 말</span></div>')


def _fbox(x, y, w, t, d, cls="", r=None, h=50):
    """순서도 칸 — r 이 있으면 처음엔 「?」, r 초에 글자가 드러남."""
    txt = (f'<text class="qm" x="{x}" y="{y + 6}" style="--r:{r}s">?</text><text class="rv" x="{x}" y="{y + 6}" style="--r:{r}s">{t}</text>'
           if r else f'<text x="{x}" y="{y + 6}">{t}</text>')
    return (f'<g class="v1fw {cls}" style="--d:{d}s"><rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="{h / 2 if "ov" in cls else 10}"/>'
            f'{txt}</g>')


def _fdm(x, y, w, h, t, d, r=None):
    pts = f"M{x - w / 2} {y}L{x} {y - h / 2}L{x + w / 2} {y}L{x} {y + h / 2}z"
    txt = (f'<text class="qm" x="{x}" y="{y + 6}" style="--r:{r}s">?</text><text class="rv" x="{x}" y="{y + 6}" style="--r:{r}s">{t}</text>'
           if r else f'<text x="{x}" y="{y + 6}">{t}</text>')
    return f'<g class="v1fw dm" style="--d:{d}s"><path d="{pts}"/>{txt}</g>'


def _farr(mk, path, d, lab="", lx=0, ly=0, cls="", r=None):
    st = f' style="--r:{r}s"' if r else ""
    t = f'<text class="lb{" rv" if r else ""}" x="{lx}" y="{ly}"{st}>{lab}</text>' if lab else ""
    return f'<g class="v1fw ar {cls}" style="--d:{d}s"><path d="{path}" marker-end="url(#{mk})"/>{t}</g>'


def _fmarker(mk):
    return (f'<defs><marker id="{mk}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            '<path d="M0 0L10 5L0 10z" fill="#3A4657"/></marker></defs>')


def milk_flow():
    """알고리즘 · 우유와 아보카도 — 「우유 하나 사 와. 아보카도 있으면 6개 사 와」.
    위: 부탁한 뜻(우유 1개 → ◇ 아보카도 → 아보카도 6개) · 아래: 남편이 한 일(◇ 아보카도 → 우유 6개). 오른쪽은 알고리즘 뜻."""
    A = lambda *x, **k: _farr("v1mkA", *x, **k)
    top = ('<svg class="v1fwS" viewBox="0 0 860 160">' + _fmarker("v1mkA")
           + _fbox(45, 60, 80, "시작", 1.2, "ov") + A("M85 60H118", 1.5)
           + _fbox(200, 60, 160, "우유 1개 사기", 1.8) + A("M280 60H318", 2.1)
           + _fdm(420, 60, 200, 90, "아보카도 있나?", 2.4) + A("M520 60H573", 2.8, "예", 546, 48)
           + _fbox(670, 60, 190, "아보카도 6개 사기", 3.1) + A("M765 60H797", 3.4)
           + _fbox(828, 60, 60, "끝", 3.6, "ov")
           + A("M420 105V140H828V87", 3.9, "아니오", 470, 132) + "</svg>")
    bot = ('<svg class="v1fwS" viewBox="0 0 860 160">'
           + _fbox(45, 60, 80, "시작", 5.4, "ov") + A("M85 60H118", 5.7)
           + _fdm(220, 60, 200, 90, "아보카도 있나?", 6.0) + A("M320 60H373", 6.4, "예", 346, 48)
           + _fbox(460, 60, 170, "우유 6개 사기", 6.8, "bad") + A("M545 60H797", 7.4)
           + _fbox(828, 60, 60, "끝", 7.6, "ov")
           + A("M220 105V135H373", 8.0, "아니오", 270, 128) + _fbox(460, 135, 170, "우유 1개 사기", 8.2, h=40)
           + A("M545 135H828V87", 8.4) + "</svg>")
    left = (f'<div class="v1mkQ" style="--d:.3s"><span>부탁</span>「우유 하나 사 와. 아보카도 있으면 6개 사 와」</div>'
            f'<div class="v1mkR" style="--d:1.2s"><em>부탁한 뜻</em>{top}</div>'
            f'<div class="v1mkR x" style="--d:5.4s"><em>남편이 한 일</em>{bot}</div>')
    side = "".join(f'<div class="v1fwk" style="--d:{d}s"><i class="{c}"></i><b>{h}</b><span>{x}</span></div>' for c, h, x, d in [
        ("bx", "순서", "무엇을 먼저 하나", 9.4), ("dm", "조건", "「있으면」이 어디에 걸리나", 10.0), ("ov", "끝", "언제 멈추나", 10.6)])
    return (f'<div class="v1fwW"><div class="v1mkL">{left}</div><div class="v1fwR"><div class="v1fwD" style="--d:9s"><b>알고리즘</b>'
            f'<span>문제를 푸는 순서 있는 절차 · 그림으로 그리면 순서도</span></div>{side}</div></div>')


def ramen_flow():
    """생각해 보기 · 라면 끓이기 — 빈 순서도(칸마다 「?」)가 먼저 나오고, 6초부터 칸 글자가 하나씩 드러남.
    처리(순서) → ◇ 조건 → 아니오면 기다렸다 되돌아감(반복) → 예면 다음 → 끝."""
    A = lambda *x, **k: _farr("v1fwA", *x, **k)
    svg = ('<svg class="v1fwS" viewBox="0 0 900 360">' + _fmarker("v1fwA")
           + _fbox(65, 90, 100, "시작", .3, "ov") + A("M115 90H158", .5)
           + _fbox(240, 90, 160, "물 550ml 붓기", .7, r=6) + A("M320 90H363", .9)
           + _fbox(435, 90, 140, "불 켜기", 1.1, r=7.2) + A("M505 90H533", 1.3)
           + _fdm(620, 90, 170, 100, "물이 끓었나?", 1.5, r=8.4)
           + A("M705 90H738", 1.7, "아니오", 722, 58, r=8.4) + _fbox(810, 90, 140, "1분 기다리기", 1.9, r=9.6)
           + A("M810 65V18H620V38", 2.1, "반복", 715, 12, "lp", r=10.8)
           + A("M620 140V253", 2.3, "예", 636, 200, r=8.4)
           + _fbox(620, 280, 160, "면 · 스프 넣기", 2.5, r=12) + A("M540 280H492", 2.7)
           + _fbox(405, 280, 170, "4분 30초 끓이기", 2.9, r=13.2) + A("M320 280H272", 3.1)
           + _fbox(205, 280, 130, "불 끄기", 3.3, r=14.4) + A("M140 280H112", 3.5)
           + _fbox(65, 280, 90, "끝", 3.7, "ov") + "</svg>")
    side = "".join(f'<div class="v1fwk" style="--d:{d}s"><i class="{c}"></i><b>{h}</b><span>{x}</span></div>' for c, h, x, d in [
        ("bx", "처리", "무엇부터 하나", 4.2), ("dm", "조건", "어디서 갈라지나", 4.6),
        ("lp", "반복", "어디로 되돌아가나", 5.0), ("ov", "끝", "언제 멈추나", 5.4)])
    return (f'<div class="v1fwW"><div>{svg}</div><div class="v1fwR"><div class="v1fwD" style="--d:3.9s"><b>생각해 보기</b>'
            f'<span>라면 끓이기 · 빈칸 「?」 채우기</span></div>{side}</div></div>')


def flowchart():
    """순서도 · 사과 먹기 — 시작 → 과일 받기 → ◇ 사과인가 → 예: 집기 · 깨물기 · 씨 뱉기 → 끝 / 아니오: 모름 · 멈춤. 칸이 차례로 나타남."""
    def n(cls, t, d, sub=""):
        return f'<div class="v1fn {cls}" style="--d:{d:.1f}s"><b>{t}</b>{f"<small>{sub}</small>" if sub else ""}</div>'
    def a(d, lab=""):
        return f'<div class="v1fa" style="--d:{d:.1f}s">{f"<em>{lab}</em>" if lab else ""}→</div>'
    top = (n("ov", "시작", .2) + a(.5) + n("", "과일 받기", .7) + a(1.0) + n("dm", "사과인가?", 1.2)
           + a(1.6, "예") + n("", "① 집기", 1.8) + a(2.1) + n("", "② 깨물기", 2.3) + a(2.6) + n("", "③ 씨 뱉기", 2.8)
           + a(3.1) + n("ov", "끝", 3.3))
    no = (f'<div class="v1fno" style="--d:3.8s"><span>아니오 ↓</span>'
          + n("er", "모름 · 멈춤", 4.0, "eat(pear) → ReferenceError") + '</div>')
    legend = ('<div class="v1flg"><span><i class="ov"></i>시작 · 끝</span><span><i></i>처리</span>'
              '<span><i class="dm"></i>조건 · 갈림길</span></div>')
    return f'<div class="v1flow"><div class="v1frow">{top}</div>{no}</div>{legend}'


def fb_steps():
    """알고리즘 피드백 · 예 — AI가 만든 로그인 순서 3단계 → 내 피드백 두 개 → 단계 두 개가 끼어듦."""
    rows = [("", "① 이메일 · 비밀번호 입력", .3, ""), ("add", "회사 이메일(@company.com)만 허용", 2.6, "a"),
            ("", "② 비밀번호 일치 확인", .7, ""), ("add", "5번 틀리면 10분 잠금", 4.4, "b"),
            ("", "③ 로그인 완료 · 첫 화면", 1.1, "")]
    st = "".join(f'<div class="v1fs {c}" style="--d:{d:.1f}s">{f"<i>{k}</i>" if k else ""}<b>{t}</b></div>' for c, t, d, k in rows)
    fb = ('<div class="v1fbq" style="--d:1.8s"><span>나 · 피드백 a</span><p>사내 시스템이라 회사 이메일만 받아 줘</p></div>'
          '<div class="v1fbq" style="--d:3.6s"><span>나 · 피드백 b</span><p>비밀번호를 계속 틀리면 잠깐 잠가 줘</p></div>')
    return (f'<div class="v1fb"><div class="v1fbl"><div class="v1fbh">AI가 만든 로그인 순서</div>{st}</div>'
            f'<div class="v1fbr">{fb}</div></div>')


def algo_list(rows):
    """알고리즘 단계 — (번호, 내용, 꼬리표). 꼬리표 「조건」 「반복」은 주황. 0.5초 간격으로 한 줄씩."""
    r = "".join(f'<div class="v1al{" k" if tag in ("조건", "반복") else ""}" style="--d:{.3 + i * .5:.1f}s"><i>{n}</i><b>{t}</b>'
                f'{f"<em>{tag}</em>" if tag else ""}</div>' for i, (n, t, tag) in enumerate(rows))
    return f'<div class="v1alist">{r}</div>'


def comic(cuts):
    """3 · 4컷 — (그림, 말풍선, 장면, 코딩에서는). 0.8초 간격으로 한 컷씩 나타나고 멈춘다."""
    c = "".join(
        f'<div class="v1cut" style="--d:{i * .8:.1f}s"><div class="pic"><img src="img/{img}" alt="{scene}"/>'
        f'<span class="bub">{bub}</span><i>{i + 1}</i></div><b>{scene}</b><small>{code}</small></div>'
        for i, (img, bub, scene, code) in enumerate(cuts))
    return f'<div class="v1comic" style="grid-template-columns:repeat({len(cuts)},1fr)">{c}</div>'


def slides():
    return [
        # ── 코딩 = 원시인에게 사과 가르치기
        light("원시인과 사과", '<div class="v1shot v1vid"><figure>'
              '<video src="img/v1_caveman.mp4" poster="img/v1_caveman.webp" autoplay muted loop playsinline></video>'
              '</figure><div class="v1side">'
              + "".join(f'<div class="v1sd"><b>{h}</b><span>{x}</span></div>' for h, x in [
                  ("원시인", "컴퓨터 · 사전 지식 없음"), ("사과 먹는 법", "코드 · 할 일의 순서"),
                  ("알려 준 순서", "그대로 실행 · 빠진 단계는 못 함"), ("코드", "컴퓨터가 실행하는 명령의 목록")])
              + "</div></div>", T),
        light("코드의 저장과 실행", comic([
            ("v1_cut1.webp", "?", "처음 본 사과", "명령 없음 → 실행 불가"),
            ("v1_cut2.webp", "이건 사과 · 먹는 것", "이름 · 먹는 법 알려 줌", "코드 작성 · 저장"),
            ("v1_cut3.webp", "사과다!", "다음 사과 · 바로 먹음", "저장된 코드 · 매번 같은 실행"),
            ("v1_cut4.webp", "?", "처음 본 배", "코드에 없는 경우 · 처리 불가")])
              + note("코딩", "컴퓨터가 실행할 명령을 프로그래밍 언어로 작성하는 일")
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("기존 코딩과 바이브코딩", viz2.pair(
            "기존 코딩", [("① 언어 학습", "문법 · 개발 도구 사용법"), ("② 직접 작성", "모든 기능을 사람이 입력"), ("③ 오류 수정", "오류 메시지로 원인 추적")],
            "바이브코딩", [("① 말로 요청", "「로그인 화면 만들어 줘」"), ("② AI가 코드 작성", "파일 생성 · 실행"), ("③ 수정 사항만 요청", "「버튼을 크게」 「비밀번호는 8자 이상」")], hl="r")
              + note("바이브코딩", "AI와 대화를 주고받으며 프로그램을 만드는 개발 방식"), T),
        light("프로그래밍 언어의 발전", langs()
              + src(("IBM · FORTRAN", "https://www.ibm.com/history/fortran"), ("Python · History", "https://docs.python.org/3/license.html"),
                    ("참고 · 알파AI스쿨 「바이브 코딩이란?」 요리 비유", "https://www.youtube.com/watch?v=cFdyp_pPgPQ")), T),
        # ── 배경 · AI 코딩 도구의 변화
        light("AI 코딩 도구의 변화", eras()
              + note("막대", "사람 몫 · AI 몫의 상대 크기 (측정값 아님)")
              + src(("GitHub · 2021-06-29", "https://github.blog/2021-06-29-introducing-github-copilot-ai-pair-programmer/"),
                    ("OpenAI · 2022-11-30", "https://openai.com/index/chatgpt/"),
                    ("Anthropic · 2025-05-22", "https://www.anthropic.com/news/claude-4")), T),
        light("자동완성 방식 예", '<div class="v1mode"><div>' + autocomplete_anim()
              + '</div><div>' + viz2.tiles([("사람", "파일 · 위치 · 첫 줄 직접 입력"), ("AI", "회색 글자로 다음 줄 제안 · Tab 으로 수락"),
                                            ("AI가 파악", "앞뒤 코드")], 1) + '</div></div>'
              + src(("GitHub Copilot 문서 · inline suggestions", "https://docs.github.com/en/copilot/using-github-copilot/getting-code-suggestions-in-your-ide-with-github-copilot")), T),
        light("대화형 방식 예", chat_anim("chat"), T),
        light("위임형 방식 예", chat_anim("agent")
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("위임의 한계", '<div class="v1shot"><figure><img src="img/v1_algo_context.webp" alt="회사 안을 들여다보는 AI"/>'
              '<figcaption>AI · 회사 밖에서 보이는 정보만</figcaption></figure><div class="v1side">'
              + "".join(f'<div class="v1sd"><b>{h}</b><span>{x}</span></div>' for h, x in [
                  ("AI에게 맡길 수 있는 것", "흔한 로그인 · 예약 화면 · 코드 작성 · 반복 수정"),
                  ("AI에게 맡길 수 없는 것", "회사 규칙 · 업무 예외 · 사용자 습관 = 비즈니스 로직"),
                  ("사람이 할 일", "규칙 정하기 · AI가 만든 순서 읽기 · 빠진 곳 피드백"),
                  ("알고리즘 이해", "피드백의 기준 · 순서 · 조건 · 예외 읽기")])
              + "</div></div>"
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("우유와 아보카도", '<div class="v1mm"><img src="img/v1_algo_milk.webp" alt="우유 사고 아보카도 있으면 6개 사 와 · 우유 6개를 들고 온 남편"/></div>', T),
        light("알고리즘", milk_flow(), T),
        light("라면 끓이기 알고리즘", ramen_flow(), T),
        light("사과 먹기 알고리즘", '<div class="v1shot"><figure><img src="img/v1_algo_steps.webp" alt="세 개의 디딤돌 · 집기 · 깨물기 · 씨 뱉기"/>'
              '<figcaption>사과 먹기 · 디딤돌 세 개</figcaption></figure>'
              + algo_list([("①", "과일이 사과인가? 아니면 멈춤", "조건"), ("②", "손으로 집기", "순서"), ("③", "한 입 깨물기", "순서"),
                           ("④", "씨 뱉기", "끝")])
              + "</div>"
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("사과 먹기 순서도", flowchart()
              + note("순서도", "알고리즘을 도형과 화살표로 그린 그림 · 처리 · 조건 · 순서가 한눈에"), T),
        light("알고리즘 피드백 예", fb_steps()
              + note("요청 팁", "「순서를 단계로 보여 줘」 → 단계를 읽고 빠진 규칙 · 예외를 지적"), T),
        light("AI 코딩 도구의 실제 속도", big([("19%", "", "AI를 쓴 숙련 개발자 · 실제로 더 걸린 시간", True),
                                             ("20%", "", "같은 개발자들이 「빨라졌다」고 느낀 정도")], 2)
              + viz2.tiles([("대상", "숙련 개발자 16명 · 실제 작업 246건"),
                            ("도구", "Cursor + Claude 3.5 · 3.7 Sonnet (2025년 초)"),
                            ("2026 후속", "AI 없이 일하려는 개발자 감소 · 측정 방식 변경")], 3)
              + src(("METR · 2025-07-10", "https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/"),
                    ("METR · 2026-02-24", "https://metr.org/blog/2026-02-24-uplift-update/")), T),
        light("LLM과 코딩 에이전트", comic([
            ("v1_brain1.webp", "생각만", "LLM", "글 읽기 · 글 쓰기 · 판단"),
            ("v1_brain2.webp", "+ 도구", "LLM + 도구", "파일 읽기 · 검색 · 명령 실행"),
            ("v1_brain3.webp", "작업 · 확인", "코딩 에이전트", "도구로 작업 · 결과 확인 반복")])
              + note("에이전트", "판단하는 모델 + 행동하는 도구")
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works"),
                    ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("용어의 유래", quote(
            "내가 <mark>「바이브코딩」</mark>이라고 부르는 새로운 코딩 방식이 있다. 느낌(vibe)에 완전히 몸을 맡기고, "
            "AI의 빠른 발전을 받아들이고, 코드가 있다는 사실조차 잊는 방식이다.",
            "Andrej Karpathy · X · 2025-02-02 · 원문 「There's a new kind of coding I call “vibe coding”…」")
              + viz2.tiles([("2023-01 · Karpathy", "「가장 인기 있는 새 프로그래밍 언어는 영어」"),
                            ("2025-02 · Karpathy", "「바이브코딩」 처음 사용"),
                            ("2025-11 · Collins 사전", "올해의 단어 선정")], 3)
              + src(("Karpathy · 2023-01-24", "https://x.com/karpathy/status/1617979122625712128"),
                    ("Karpathy · 2025-02-02", "https://x.com/karpathy/status/1886192184808149383"),
                    ("Collins · 2025-11-06", "https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/")), T),
        light("AI가 혼자 끝내는 작업 길이", '<div class="mwrap">' + metr_chart() + '<div class="mcards">'
              + '<div class="bn hl"><div class="bv">105<small>일</small></div><div class="bl">작업 길이 2배 주기 (2024년 이후)</div></div>'
              + '<div class="bn"><div class="bv">작업 길이</div><div class="bl">사람이 하면 걸리는 시간 기준</div></div>'
              + '</div></div>' + src(METR_TH), T),
        # ── 할 수 있는 것 · 조심할 것
        light("바이브코딩 사례", viz2.tiles([
            ("브라우저 3D 비행 게임", "fly.pieter.com · 개발자 1명 + AI"),
            ("메뉴판 사진 → 음식 그림", "MenuGen · Karpathy"),
            ("업무 도구", "예약표 · 체크리스트 (1부 실습)")], 3)
              + note("배포", "공개 · 운영은 만들기와 별도 과정 (1-7)")
              + src(("levelsio · X", "https://x.com/levelsio/status/1899596115210891751"),
                    ("Karpathy · MenuGen", "https://karpathy.bearblog.dev/vibe-coding-menugen/")), T),
        light("가능성과 한계", viz2.fit(
            [("화면 1~3개 웹 페이지", "예약 · 투표 · 체크리스트"), ("업무 보조 도구", "계산기 · 자료 정리"), ("시제품", "아이디어 시연용 화면")],
            [("돈 · 개인정보 처리 서비스", "전문 보안 점검 필요"), ("동시 사용자가 많은 서비스", "서버 · DB 설계 필요"),
             ("코드 확인 없는 운영", "장애 원인 추적 어려움")],
            gt="지금 만들기 좋은 앱", bt="아직 어려운 앱"), T),
        light("요청과 결과", '<div class="v1core">'
              '<div class="bx me"><span>내 요청</span><b>「로그인 화면 만들어 줘」</b></div><i>→</i>'
              '<div class="bx ai"><span>AI 작업</span><b>읽기 · 작성 · 실행 · 확인</b></div><i>→</i>'
              '<div class="bx out"><span>결과</span><b>로그인 화면</b></div>'
              '<div class="q">요청 = 결과 ?</div></div>'
              + flow([("기획서", "무엇을 · 누구를 (1-3)"), ("PRD", "기능 · 완료 기준 (1-4)"), ("Git", "되돌릴 저장 시점 (1-5)"),
                      ("작게 요청 · 확인", "기능 하나씩 (1-6)"), ("공개 전 점검", "키 · 개인정보 (1-7)")], hl=-1)
              + note("1부", "요청에 맞는 결과를 얻는 과정 · 기획서 → PRD → Git → 요청 · 확인 → 배포"), T),
        light("1부 완성 화면", shot("room_main.webp", "회의실 예약 · 1부 공통 예제 완성본", [
            ("하루 시간표", "회의실 3곳 · 30분 단위"), ("예약", "빈 칸 클릭 · 이미 찬 시간은 예약 불가"),
            ("공유", "배포 주소 (1-7)"), ("내 앱", "같은 순서로 하나 더")]), T),
    ]


CSS = """
  /* 1-1 · 알고리즘 단계 */
  .v1alist{display:flex; flex-direction:column; gap:10px;}
  .v1al{display:grid; grid-template-columns:34px 1fr auto; gap:10px; align-items:center; padding:11px 16px; border:1.5px solid #E3E6EA; border-left:5px solid #1F3A5F; border-radius:10px; background:#fff; opacity:0; animation:v1cutIn .4s ease-out var(--d) forwards;}
  .v1al i{font-style:normal; font-weight:800; color:#1F3A5F; font-size:18px;} .v1al b{font-size:18px; color:#16233A;}
  .v1al em{font-style:normal; font-size:12px; font-weight:800; padding:3px 9px; border-radius:10px; background:#EEF1F5; color:#3A4657;}
  .v1al.k{border-left-color:#F28C28; background:#FFF8F0;} .v1al.k em{background:#F28C28; color:#fff;}
  @media print{.v1al{opacity:1; animation:none}}

  /* 1-1 · 순서도 */
  .v1flow{margin:56px 0 10px;}
  .v1frow{display:flex; align-items:center; gap:6px;}
  .v1fn{flex:0 0 auto; padding:18px 16px; border:2px solid #1F3A5F; border-radius:8px; background:#fff; text-align:center; opacity:0; animation:v1cutIn .4s ease-out var(--d) forwards;}
  .v1fn b{font-size:21px; color:#16233A; white-space:nowrap;} .v1fn small{display:block; font-family:var(--mono); font-size:15px; color:#C0392B; margin-top:4px;}
  .v1fn.ov{border-radius:30px; background:#F4F6F9;}
  .v1fn.dm{width:150px; height:150px; padding:0; display:grid; place-items:center; border:0; background:none; position:relative;}
  .v1fn.dm::before{content:""; position:absolute; inset:22px; border:2px solid #F28C28; background:#FFF3E6; transform:rotate(45deg); border-radius:6px;}
  .v1fn.dm b{position:relative; font-size:19px;}
  .v1fn.er{border-color:#C0392B; background:#FDECEA;}
  .v1fa{flex:0 0 auto; position:relative; color:#F28C28; font-weight:800; font-size:24px; opacity:0; animation:v1cutIn .3s ease-out var(--d) forwards;}
  .v1fa em{position:absolute; top:-20px; left:-2px; font-style:normal; font-size:13px; color:#E07A12;}
  .v1fno{display:flex; flex-direction:column; align-items:flex-start; gap:6px; margin:4px 0 0 330px; opacity:0; animation:v1cutIn .3s ease-out var(--d) forwards;}
  .v1fno > span{font-size:14px; font-weight:800; color:#C0392B;}
  .v1flg{display:flex; gap:22px; margin-top:40px; font-size:15px; color:#6B7785;}
  .v1flg span{display:flex; align-items:center; gap:7px;} .v1flg i{display:inline-block; width:22px; height:14px; border:2px solid #1F3A5F; border-radius:3px;}
  .v1flg i.ov{border-radius:10px;} .v1flg i.dm{width:12px; height:12px; border-color:#F28C28; transform:rotate(45deg);}
  @media print{.v1fn,.v1fa,.v1fno{opacity:1; animation:none}}
  /* 1-1 · 알고리즘 피드백 */
  .v1fb{display:grid; grid-template-columns:1.1fr 1fr; gap:28px; align-items:start; margin-top:6px;}
  .v1fbh{font-size:13px; font-weight:800; color:#6B7785; margin-bottom:10px;}
  .v1fs{display:flex; align-items:center; gap:10px; padding:13px 18px; margin-bottom:10px; border:1.5px solid #D9DDE3; border-left:5px solid #1F3A5F; border-radius:10px; background:#fff; opacity:0; animation:v1cutIn .4s ease-out var(--d) forwards;}
  .v1fs b{font-size:19px; color:#16233A;}
  .v1fs.add{border-color:#F7C99A; border-left-color:#F28C28; background:#FFF3E6; margin-left:26px; max-height:0; padding-top:0; padding-bottom:0; margin-bottom:0; overflow:hidden; animation:v1fsIn .6s ease-out var(--d) forwards;}
  .v1fs i, .v1fbq span{font-style:normal; font-size:12px; font-weight:800; color:#fff; background:#F28C28; border-radius:10px; padding:2px 8px;}
  @keyframes v1fsIn{to{opacity:1; max-height:70px; padding-top:13px; padding-bottom:13px; margin-bottom:10px}}
  .v1fbr{display:flex; flex-direction:column; gap:16px; padding-top:28px;}
  .v1fbq{opacity:0; animation:v1cutIn .4s ease-out var(--d) forwards;}
  .v1fbq p{margin:6px 0 0; padding:12px 16px; border-radius:14px; background:#FFF3E6; border:1px solid #F7C99A; font-size:18px; color:#16233A;}
  @media print{.v1fs,.v1fbq{opacity:1; animation:none} .v1fs.add{max-height:none; padding:13px 18px; margin-bottom:10px}}

  /* 1-1 · 비유 영상 */
  .v1comic{display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:6px;}
  .v1cut{opacity:0; animation:v1cutIn .6s ease-out var(--d) forwards;}
  @keyframes v1cutIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  @media print{.v1cut{opacity:1; animation:none}}
  .v1cut .pic{position:relative; border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#F7EEDB;}
  .v1cut img{display:block; width:100%; aspect-ratio:16/9; object-fit:cover;}
  .v1cut .bub{position:absolute; right:10px; bottom:10px; background:#fff; border:2px solid #16233A; border-radius:16px; padding:5px 12px; font-size:17px; font-weight:800; color:#16233A;}
  .v1cut .pic i{position:absolute; left:10px; top:10px; width:28px; height:28px; border-radius:50%; background:#F28C28; color:#fff; font-style:normal; font-weight:800; font-size:15px; display:grid; place-items:center;}
  .v1cut b{display:block; font-size:19px; color:#16233A; margin-top:12px; line-height:1.3;}
  .v1cut small{display:block; font-size:15px; color:#E07A12; font-weight:700; margin-top:4px;}
  .v1eras{display:grid; grid-template-columns:repeat(3,1fr); gap:20px; align-items:start; margin-top:4px;}
  .v1era{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:18px 20px;}
  .v1era:last-child{border-color:#F28C28; background:#FFF8F0;}
  .v1era .yr{font-family:var(--mono); font-size:15px; font-weight:800; color:#F28C28;}
  .v1era b{display:block; font-size:24px; color:#16233A; margin-top:2px;} .v1era .tl{font-size:15px; color:#6B7785;}
  .v1era .bar{display:flex; height:14px; border-radius:7px; overflow:hidden; margin:14px 0 10px;}
  .v1era .bar .me{background:#1F3A5F;} .v1era .bar .ai{background:#F28C28;}
  .v1era .row{display:flex; gap:10px; align-items:baseline; margin-top:6px;}
  .v1era em{font-style:normal; font-size:13px; font-weight:800; min-width:30px;} .v1era em.me{color:#1F3A5F;} .v1era em.ai{color:#E07A12;}
  .v1era small{font-size:15px; color:#3A4657; line-height:1.4;}
  .qt mark{background:#FFE08A; padding:0 3px; border-radius:3px;}
  .v1era .grasp{margin-top:12px; padding-top:10px; border-top:1px dashed #D9DDE3; font-size:15px; color:#6B7785;} .v1era .grasp b{display:inline; font-size:17px; color:#E07A12;}
  .v1ghost{color:#8A94A3; font-style:italic;}
  .v1mode{display:grid; grid-template-columns:1.35fr 1fr; gap:24px; align-items:start;}
  /* 자동완성 편집기 */
  .v1ed{background:#1E2433; border-radius:14px; overflow:hidden; box-shadow:0 10px 26px rgba(15,27,45,.18);}
  .v1ed .bar{display:flex; gap:7px; align-items:center; padding:10px 14px; background:#161B27;}
  .v1ed .bar b{width:11px; height:11px; border-radius:50%; background:#3A4252;} .v1ed .bar b:nth-child(1){background:#FF5F57;} .v1ed .bar b:nth-child(2){background:#FEBC2E;} .v1ed .bar b:nth-child(3){background:#28C840;}
  .v1ed .bar span{margin-left:8px; font-size:13px; color:#8A94A3; font-family:var(--mono);}
  .v1ed .code{position:relative; padding:14px 0 18px; font-family:var(--mono); font-size:16px; line-height:2.05; font-variant-ligatures:none; font-feature-settings:'liga' 0, 'calt' 0;}
  .v1ed .ln{display:flex; white-space:pre; height:32.8px;}
  .v1ed .ln i{width:44px; text-align:right; padding-right:16px; color:#4B5568; font-style:normal;}
  .v1ed .ty{display:inline-block; overflow:hidden; width:0; color:#E6EDF7; border-right:2px solid transparent; vertical-align:top;}
  .v1ed .gh{opacity:0; color:#98A3B6; font-style:italic;}
  @keyframes v1type{to{width:var(--n)}}
  @keyframes v1caret{0%{border-right-color:#F28C28} 50%{border-right-color:transparent}}
  @keyframes v1ghIn{to{opacity:1}}
  @keyframes v1ghOk{from{color:#98A3B6; font-style:italic} to{color:#E6EDF7; font-style:normal; opacity:1}}
  @keyframes v1out{to{opacity:0}}
  @keyframes v1tabIn{0%{opacity:0; transform:scale(.8)} 25%{opacity:1; transform:scale(1)} 45%{transform:scale(.92)} 60%{transform:scale(1)} 80%{opacity:1} 100%{opacity:0}}
  .v1sug{position:absolute; right:16px; opacity:0; padding:4px 10px; border-radius:8px; background:#2A3142; color:#C9D2E0; font-size:13px; font-family:var(--sans,inherit);}
  .v1tab{position:absolute; right:16px; bottom:16px; opacity:0; display:flex; gap:8px; align-items:center;}
  .v1tab kbd{padding:6px 14px; border-radius:8px; background:#F28C28; color:#fff; font-weight:800; font-size:15px; box-shadow:0 3px 0 #B8641A;}
  .v1tab span{color:#F7C99A; font-size:14px; font-weight:700;}
  @media print{.v1ed .ty{width:auto} .v1ed .gh{opacity:1; color:#E6EDF7; font-style:normal}}
  /* 대화형 · 위임형 화면 */
  .v1cw{border:1.5px solid #D9DDE3; border-radius:16px; background:#F7F8FA; padding:16px 20px; min-height:330px; display:flex; flex-direction:column; gap:10px;}
  .v1cw.cc{background:#1E2433; border-color:#1E2433;} .v1cw .v1hd{font-size:13px; font-weight:800; color:#6B7785;} .v1cw.cc .v1hd{color:#8A94A3;}
  .v1cw .v1me{align-self:flex-end; max-width:88%;} .v1cw .v1me p{margin:0; padding:10px 15px; border-radius:14px; background:#FFF3E6; border:1px solid #F7C99A; font-size:17px; color:#16233A; white-space:normal;}
  .v1cw .v1k{display:inline; opacity:0; animation:v1ghIn .01s linear forwards;}
  .v1cw .v1dots{display:flex; gap:5px; padding:6px 2px; opacity:0; animation:v1ghIn .2s forwards, v1out .2s forwards;}
  .v1cw .v1dots b{width:8px; height:8px; border-radius:50%; background:#9AA6B5;}
  .v1cw .v1ai .v1ln{margin:0 0 8px; opacity:0; animation:v1cutIn .4s ease-out forwards; font-size:17px; color:#16233A;}
  .v1cw.cc .v1ai .v1ln, .v1cw .v1ai pre.v1ln{color:#E6EDF7;}
  .v1cw .v1ai pre{background:#1E2433; color:#E6EDF7; padding:10px 14px; border-radius:10px; font-family:var(--mono); font-size:15px; white-space:pre; font-variant-ligatures:none;}
  .v1ust{display:grid; grid-template-columns:26px 130px 1fr; gap:8px; align-items:baseline; opacity:0; animation:v1cutIn .35s ease-out forwards; color:#E6EDF7; font-size:16px;}
  .v1ust small{color:#98A3B6; font-size:14.5px;} .v1ust .v1ic{position:relative; display:inline-block; width:18px; height:18px;}
  .v1ust .v1run, .v1ust .v1ok{position:absolute; left:0; top:0; font-weight:800; line-height:18px; background:none; border:0; padding:0;}
  .v1ust .v1run{color:#F28C28; opacity:0; animation:v1ghIn .2s forwards, v1out .2s forwards;} .v1ust .v1ok{color:#3FB950; opacity:0; animation:v1ghIn .2s forwards;}
  .v1side2 .v1hh{font-size:15px; font-weight:800; color:#6B7785; margin:4px 0 10px;}
  .v1td{display:flex; gap:12px; align-items:center; padding:12px 14px; margin-bottom:8px; border-radius:12px; background:#fff; border:1.5px solid #D9DDE3; opacity:0; animation:v1cutIn .4s ease-out forwards;}
  .v1td i{width:26px; height:26px; border-radius:50%; background:#1F3A5F; color:#fff; font-style:normal; font-weight:800; font-size:14px; display:grid; place-items:center; flex:none;}
  .v1td span{font-size:18px; color:#16233A; font-weight:600;} .v1td.me2{border-color:#F28C28; background:#FFF8F0;} .v1td.me2 i{background:#F28C28;}
  .v1side2 .v1gr{margin-top:12px; font-size:15px; color:#6B7785; opacity:0; animation:v1ghIn .4s forwards;} .v1side2 .v1gr b{color:#E07A12; font-size:17px;}
  @media print{.v1cw .v1k,.v1cw .v1ai .v1ln,.v1ust,.v1ust .v1ok,.v1td,.v1side2 .v1gr{opacity:1; animation:none} .v1cw .v1dots,.v1ust .v1run{display:none}}
  /* 1부의 핵심 */
  .v1core{position:relative; display:grid; grid-template-columns:1fr 44px 1fr 44px 1fr; align-items:center; margin:6px 0 34px; padding:26px 24px 46px; border-radius:18px; background:#FFF8F0; border:2px solid #F28C28;}
  .v1core .bx{background:#fff; border:2px solid #D9DDE3; border-radius:14px; padding:16px 18px; text-align:center;}
  .v1core .bx span{display:block; font-size:14px; font-weight:800; color:#6B7785;} .v1core .bx b{display:block; font-size:20px; color:#16233A; margin-top:4px;}
  .v1core .bx.me{border-color:#F28C28;} .v1core .bx.ai{background:#1F3A5F; border-color:#1F3A5F;} .v1core .bx.ai span{color:#C9D2E0;} .v1core .bx.ai b{color:#fff;}
  .v1core i{font-style:normal; font-size:26px; color:#F28C28; font-weight:800; text-align:center;}
  .v1core .q{position:absolute; left:50%; bottom:-20px; transform:translateX(-50%); background:#F28C28; color:#fff; font-weight:900; font-size:22px; padding:8px 26px; border-radius:999px; box-shadow:0 6px 16px rgba(242,140,40,.3);}
  /* 언어의 발전 */
  .v1langs{display:grid; grid-template-columns:minmax(0,1fr) 36px minmax(0,1fr) 36px minmax(0,1fr); align-items:stretch; margin-top:4px;}
  .v1lang{border:2px solid #D9DDE3; border-radius:16px; background:#fff; padding:16px 18px; display:flex; flex-direction:column;}
  .v1lang:last-of-type{border-color:#F28C28; background:#FFF8F0;}
  .v1lang .v1ly{font-family:var(--mono); font-size:13.5px; font-weight:800; color:#F28C28;} .v1lang b{font-size:23px; color:#16233A; margin:2px 0 10px;}
  .v1lang pre{margin:0; overflow:hidden; background:#1E2433; color:#E6EDF7; border-radius:10px; padding:12px 14px; font-family:var(--mono); font-size:16px; white-space:pre; min-height:62px; font-variant-ligatures:none;}
  .v1lang pre.nl{background:#fff; color:#16233A; border:1.5px solid #F7C99A; font-family:inherit; font-weight:700; white-space:pre-wrap;}
  .v1lang .v1lf{font-size:15.5px; color:#3A4657; margin:10px 0 8px;}
  .v1lang .v1lk{display:block; margin-top:auto; padding:8px 12px; border-radius:10px; background:#F4F6F9; writing-mode:horizontal-tb; font-size:15.5px; color:#16233A; font-weight:700;} .v1lang .v1lk span{font-size:12.5px; font-weight:800; color:#E07A12; margin-right:8px;}
  .v1lar{font-style:normal; align-self:center; text-align:center; font-size:26px; font-weight:800; color:#F28C28;}
  .v1lline{display:flex; align-items:center; gap:12px; margin-top:16px; font-size:14px; font-weight:800; color:#6B7785;}
  .v1lline b{flex:1; height:4px; border-radius:2px; background:linear-gradient(90deg,#1F3A5F,#F28C28);}
  /* 1-1 · 알고리즘 · 라면 순서도 (v1fw) */
  .v1fwW{display:grid; grid-template-columns:1fr 300px; gap:22px; align-items:center;}
  .v1fwS{width:100%; display:block; overflow:visible;}
  .v1fwS text{font-size:19px; font-weight:700; fill:#16233A; text-anchor:middle;}
  .v1fw{opacity:0; animation:v1fwIn .6s var(--d) forwards;}
  .v1fw rect{fill:#fff; stroke:#1F3A5F; stroke-width:2.5;}
  .v1fw.ov rect{fill:#16233A;} .v1fw.ov text{fill:#fff;}
  .v1fw.dm path{fill:#FFF1E2; stroke:#F28C28; stroke-width:2.5;}
  .v1fw.ar path{fill:none; stroke:#3A4657; stroke-width:2.5;}
  .v1fw.ar .lb{font-size:16px; font-weight:800; fill:#E07A12;}
  .v1fw.lp path{stroke:#F28C28; stroke-width:3.5; stroke-dasharray:8 6;}
  .v1fw.lp{animation:v1fwIn .6s var(--d) forwards, v1fwP 1s calc(var(--d) + .8s) 2;}
  .v1fwR{display:flex; flex-direction:column; gap:12px;}
  .v1fwD{background:#16233A; color:#fff; border-radius:14px; padding:14px 18px;}
  .v1fwD b{display:block; font-size:22px; margin-bottom:4px;} .v1fwD span{font-size:16px; color:#D6DEEA;}
  .v1fw .qm{fill:#E07A12; font-size:26px; animation:v1fwOut .4s var(--r) forwards;}
  .v1fw .rv{opacity:0; animation:v1fwIn .5s var(--r) forwards;}
  .v1fw.bad rect{fill:#FDECEA; stroke:#C0392B; stroke-width:3;} .v1fw.bad text{fill:#A93226;}
  .v1fw.bad{animation:v1fwIn .6s var(--d) forwards, v1fwP 1s calc(var(--d) + .8s) 2;}
  .v1fwD{opacity:0; animation:v1fwIn .6s var(--d) forwards;}
  .v1mm{display:flex; justify-content:center;} .v1mm img{height:450px; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.12);}
  .v1mkL{display:flex; flex-direction:column; gap:10px;}
  .v1mkQ{font-size:21px; font-weight:800; color:#16233A; background:#FFF8F0; border:2px solid #F28C28; border-radius:14px; padding:10px 16px;
    opacity:0; animation:v1fwIn .6s var(--d) forwards;}
  .v1mkQ span{font-size:14px; color:#fff; background:#F28C28; border-radius:8px; padding:3px 9px; margin-right:10px; vertical-align:middle;}
  .v1mkR{border:1.5px solid #D9DDE3; border-radius:14px; padding:8px 12px 2px; opacity:0; animation:v1fwIn .6s var(--d) forwards;}
  .v1mkR.x{border-color:#E6B0AA; background:#FFFAFA;}
  .v1mkR em{font-style:normal; font-size:15px; font-weight:800; color:#6B7785;} .v1mkR.x em{color:#A93226;}
  .v1fwk{display:grid; grid-template-columns:34px 1fr; gap:2px 12px; align-items:center; background:#F4F6F9; border-radius:12px; padding:10px 14px;
    opacity:0; animation:v1fwIn .6s var(--d) forwards;}
  .v1fwk i{grid-row:1/span 2; width:30px; height:22px; border:2.5px solid #1F3A5F; border-radius:5px; background:#fff;}
  .v1fwk i.dm{width:20px; height:20px; transform:rotate(45deg); border-color:#F28C28; background:#FFF1E2; border-radius:2px; margin-left:5px;}
  .v1fwk i.lp{border:none; border-top:3.5px dashed #F28C28; border-radius:0; height:0; background:none;}
  .v1fwk i.ov{border-radius:11px; background:#16233A; border-color:#16233A;}
  .v1fwk b{font-size:18px; color:#16233A;} .v1fwk span{font-size:15px; color:#3A4657;}
  @keyframes v1fwIn{from{opacity:0} to{opacity:1}}
  @keyframes v1fwP{50%{opacity:.25}}
  @keyframes v1fwOut{to{opacity:0}}
  @media print{.v1fw,.v1fwk,.v1fwD,.v1mkQ,.v1mkR,.v1fw .rv{opacity:1; animation:none} .v1fw .qm{display:none}}
  .v1vid video{width:100%; max-height:440px; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#F7EEDB; display:block;}
"""
