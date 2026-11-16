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
from v1kit import shot

T = "1-1"
STEPS = ["① 이건 「사과」 · 먹는 것", "② 손으로 집는다", "③ 입에 넣고 깨문다", "④ 씨는 뱉는다"]
DONE = ["사과를 알아봄", "손으로 집음", "깨물어 먹음", "씨를 뱉음"]
APPLE = ("사과 사진 · Evan-Amos · CC0", "https://commons.wikimedia.org/wiki/File:Honeycrisp-Apple.jpg")


# ── 그림 조각 — 가르치는 말(코드)을 한 줄씩 실행하고 · 원시인이 한 일이 옆에 쌓인다 ──
def _panel(x, w, title, sub=""):
    return (f'<rect x="{x}" y="10" width="{w}" height="380" rx="16" fill="{W}" stroke="{G}" stroke-width="2"/>'
            + _t(x + 22, 40, title, "tt", "start") + (_t(x + w - 22, 40, sub, "ts", "end") if sub else ""))


def _row(x, y, w, s, kind="code"):
    if kind == "miss":
        return (f'<rect x="{x}" y="{y}" width="{w}" height="50" rx="10" fill="#FFF5F5" stroke="{R}" stroke-width="2" stroke-dasharray="7 6"/>'
                + _t(x + 18, y + 26, "④ (빠뜨림)", "ts", "start", f'style="fill:{R};font-weight:700"'))
    if kind in ("ok", "bad"):
        c = OK if kind == "ok" else R
        return (f'<rect x="{x}" y="{y}" width="{w}" height="50" rx="10" fill="{W}" stroke="{c}" stroke-width="2"/>'
                + _t(x + 18, y + 26, ("✓ " if kind == "ok" else "✕ ") + s, "tn", "start", f'style="fill:{c}"'))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="50" rx="10" fill="{BG}" stroke="{G}" stroke-width="1.5"/>'
            + _t(x + 18, y + 26, s, "tn", "start"))


def _run(d, cx, cw, rx, rw, t0, step, missing=None, typed=None):
    """코드 줄(cx) · 실행 표시 · 한 일(rx). t0 = 실행 시작 %, step = 줄 간격 %. typed = 줄이 나타나는 % 목록."""
    b = []
    for i, s in enumerate(STEPS):
        y = 62 + i * 66
        row = _row(cx, y, cw, s, "miss" if i == missing else "code")
        b.append(f'<g {d.show(typed[i])}>{row}</g>' if typed else row)
        res = _row(rx, y, rw, "씨까지 삼킴" if i == missing else DONE[i], "bad" if i == missing else "ok")
        b.append(f'<g {d.show(t0 + i * step + 4)}>{res}</g>')
    # 실행 중인 줄 — 주황 테두리가 한 줄씩 내려간다
    st = [(0, "opacity:0;transform:translateY(0px)"), (t0 - 2, "opacity:0;transform:translateY(0px)"), (t0, "opacity:1;transform:translateY(0px)")]
    for i in range(1, 4):
        st += [(t0 + i * step - 2, f"opacity:1;transform:translateY({(i - 1) * 66}px)"), (t0 + i * step, f"opacity:1;transform:translateY({i * 66}px)")]
    st += [(t0 + 4 * step, "opacity:1;transform:translateY(198px)"), (t0 + 4 * step + 3, "opacity:0;transform:translateY(198px)"), (100, "opacity:0;transform:translateY(198px)")]
    b.append(f'<rect x="{cx - 6}" y="56" width="{cw + 12}" height="62" rx="13" fill="none" stroke="{O}" stroke-width="3.5" {d.a(st)}/>')
    return b


def _badge(d, t, x, w, ok, s):
    c = OK if ok else R
    return f'<g {d.show(t)}><rect x="{x}" y="330" width="{w}" height="46" rx="23" fill="{c}"/>{_t(x + w / 2, 354, s, "tw")}</g>'


def _scene(p, missing=None):
    d = _D(p, 12)
    b = [_panel(20, 300, "원시인 = 컴퓨터"),
         f'<image href="img/v1_apple.webp" x="70" y="70" width="200" height="181"/>',
         _t(170, 290, "사과를 처음 본다", "tn"), _t(170, 320, "적힌 것만 그대로 한다", "ts"),
         _panel(350, 440, "가르치는 말", "= 코드"), _panel(820, 320, "원시인이 한 일", "= 실행 결과")]
    b += _run(d, 370, 400, 840, 280, 14, 16, missing)
    b.append(_badge(d, 84, 840, 280, missing is None, "잘 먹었다" if missing is None else "버그 · 씨까지 삼킴"))
    return d.svg(1160, 400, "".join(b))


def anim_bug():
    """④ 를 빠뜨림 → 실행은 그대로 → 씨까지 삼킨다. 12초 · 한 번."""
    return _scene("aq", missing=3)


def anim_vibe():
    """나는 우리말 한 줄 → AI(통역사)가 코드 네 줄을 쓴다 → 실행 → 나는 결과만 본다. 13초 · 한 번."""
    d = _D("vb", 13)
    b = [_panel(20, 280, "나"),
         f'<g {d.show(3)}><rect x="40" y="80" width="240" height="56" rx="28" fill="#FFF3E6" stroke="{O}" stroke-width="2.5"/>'
         + _t(160, 109, "「사과 먹는 법 알려 줘」", "tn") + "</g>",
         _t(160, 170, "우리말 한 줄", "ts"),
         f'<line x1="282" y1="108" x2="362" y2="108" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})" {d.show(8)}/>',
         _panel(350, 440, "AI가 쓰는 코드", "통역사"), _panel(820, 320, "컴퓨터가 한 일", "= 실행 결과")]
    b += _run(d, 370, 400, 840, 280, 44, 9, typed=[12, 19, 26, 33])
    b.append(_badge(d, 84, 840, 280, True, "잘 먹었다"))
    b.append(f'<g {d.show(90)}><rect x="40" y="330" width="240" height="46" rx="23" fill="{N}"/>{_t(160, 354, "결과만 보고 판단", "tw")}</g>')
    return d.svg(1160, 400, "".join(b))


ERAS = [  # (해, 이름, 도구, 사람 몫 %, AI 몫 설명, 사람 몫 설명) — 막대는 모양만 · 측정값 아님
    ("2021", "자동완성", "GitHub Copilot", 85, "다음 줄 · 함수 제안", "나머지 작성 · 실행 · 수정"),
    ("2022", "채팅", "ChatGPT", 55, "코드를 답으로 작성", "복사 · 붙여넣기 · 실행 · 오류 전달"),
    ("2025", "에이전트", "Claude Code", 15, "파일 읽기 · 작성 · 실행 · 확인", "요청 · 결과 판단"),
]


def eras():
    """AI 코딩 도구 3단 계단 — 칸이 차례로 나타나고 사람 몫 막대가 줄어든다."""
    c = ""
    for i, (y, name, tool, h, ai, me) in enumerate(ERAS):
        c += (f'<div class="v1era v1cut" style="--d:{i * .8:.1f}s; margin-top:{(2 - i) * 34}px">'
              f'<div class="yr">{y}</div><b>{name}</b><span class="tl">{tool}</span>'
              f'<div class="bar"><i class="me" style="width:{h}%"></i><i class="ai" style="width:{100 - h}%"></i></div>'
              f'<div class="row"><em class="me">사람</em><small>{me}</small></div>'
              f'<div class="row"><em class="ai">AI</em><small>{ai}</small></div></div>')
    return f'<div class="v1eras">{c}</div>'


def anim_loop():
    """공식 에이전트 루프 — 요청 → 맥락 파악 → 작업 → 결과 확인 → (반복) → 완료 · 사람은 언제든 끼어듦. 9초 · 한 번.
    참고: Claude Code 문서 「How Claude Code works」 agentic loop 도해 · IBM Technology 「What Is Vibe Coding?」 02:18~02:38."""
    d = _D("lp", 9)
    def node(cx, cy, t, sub, at):
        return (f'<g {d.show(at)}><rect x="{cx - 95}" y="{cy - 32}" width="190" height="64" rx="14" fill="{N}"/>'
                + _t(cx, cy - 9, t, "tw", extra='style="font-size:18px"') + _t(cx, cy + 15, sub, "tw", extra='style="font-size:13px;font-weight:600;opacity:.8"') + "</g>")
    b = [f'<rect x="0" y="0" width="1160" height="400" rx="18" fill="{BG}"/>',
         f'<g {d.show(2)}><rect x="30" y="52" width="230" height="68" rx="14" fill="#FFF3E6" stroke="{O}" stroke-width="2.5"/>'
         + _t(145, 76, "내 요청", "tt") + _t(145, 102, "「겹치는 예약 막아 줘」", "ts") + "</g>",
         f'<line x1="262" y1="86" x2="476" y2="86" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})" {d.show(10)}/>',
         node(580, 86, "① 맥락 파악", "파일 찾기 · 읽기", 16),
         f'<path d="M675 96 Q770 130 742 248" fill="none" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})" {d.show(26)}/>',
         node(720, 290, "② 작업", "코드 수정 · 명령 실행", 32),
         f'<path d="M622 300 Q580 330 538 300" fill="none" stroke="{N}" stroke-width="3" marker-end="url(#{d.id("k")})" {d.show(42)}/>',
         node(440, 290, "③ 결과 확인", "실행 · 오류 확인", 48)]
    close = [(0, "stroke-dashoffset:260;opacity:0"), (58, "stroke-dashoffset:260;opacity:0"), (59, "stroke-dashoffset:260;opacity:1"), (70, "stroke-dashoffset:0;opacity:1"), (100, "stroke-dashoffset:0;opacity:1")]
    b.append(f'<path d="M420 256 Q412 150 486 120" fill="none" stroke="{O}" stroke-width="4" stroke-dasharray="260" '
             f'marker-end="url(#{d.id("o")})" {d.a(close)}/>')
    b.append(f'<g {d.show(70)}>' + _t(580, 200, "반복", "to", extra='style="font-size:20px"') + _t(580, 224, "완료될 때까지", "ts") + "</g>")
    b.append(f'<line x1="816" y1="290" x2="926" y2="290" stroke="{OK}" stroke-width="3" marker-end="url(#{d.id("g")})" {d.show(78)}/>')
    b.append(f'<g {d.show(82)}><rect x="930" y="258" width="200" height="64" rx="14" fill="{W}" stroke="{OK}" stroke-width="2.5"/>'
             + _t(1030, 281, "완료 · 결과 보고", "tn") + _t(1030, 304, "확인 통과", "ts") + "</g>")
    b.append(f'<g {d.show(90)}><rect x="830" y="52" width="300" height="68" rx="14" fill="{W}" stroke="{S}" stroke-width="2" stroke-dasharray="6 5"/>'
             + _t(980, 76, "사람", "tt") + _t(980, 102, "결과 보고 수정 요청 · 언제든 끼어들기", "ts") + "</g>")
    b.append(f'<path d="M830 96 Q760 170 650 196" fill="none" stroke="{S}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#{d.id("k")})" {d.show(90)}/>')
    return d.svg(1160, 400, "".join(b))


def comic(cuts):
    """4컷 — (그림, 말풍선, 장면, 코딩에서는). 0.8초 간격으로 한 컷씩 나타나고 멈춘다."""
    c = "".join(
        f'<div class="v1cut" style="--d:{i * .8:.1f}s"><div class="pic"><img src="img/{img}" alt="{scene}"/>'
        f'<span class="bub">{bub}</span><i>{i + 1}</i></div><b>{scene}</b><small>{code}</small></div>'
        for i, (img, bub, scene, code) in enumerate(cuts))
    return f'<div class="v1comic">{c}</div>'


def slides():
    return [
        # ── 코딩 = 원시인에게 사과 가르치기
        light("사과를 처음 보는 원시인", '<div class="v1shot v1vid"><figure>'
              '<video src="img/v1_caveman.mp4" poster="img/v1_caveman.webp" autoplay muted loop playsinline></video>'
              '<figcaption>AI 생성 영상 · Z-Image Turbo · Wan 2.2 (Apache 2.0)</figcaption></figure><div class="v1side">'
              + "".join(f'<div class="v1sd"><b>{h}</b><span>{x}</span></div>' for h, x in [
                  ("원시인", "컴퓨터 · 사전 지식 없음"), ("사과 먹는 법", "코드 · 할 일의 순서"),
                  ("알려 준 순서", "그대로 실행 · 빠진 단계는 못 함"), ("코드", "컴퓨터가 실행하는 명령의 목록")])
              + "</div></div>", T),
        light("알려 준 것만 하는 컴퓨터", comic([
            ("v1_cut1.webp", "?", "처음 본 사과", "명령 없음 → 실행 불가"),
            ("v1_cut2.webp", "이건 사과 · 먹는 것", "이름 · 먹는 법 알려 줌", "코드 작성 · 저장"),
            ("v1_cut3.webp", "사과다!", "다음 사과 · 바로 먹음", "저장된 코드 · 매번 같은 실행"),
            ("v1_cut4.webp", "?", "처음 본 배", "코드에 없는 경우 · 처리 불가")])
              + note("코딩", "컴퓨터가 실행할 명령을 프로그래밍 언어로 작성하는 일")
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("하나라도 빠뜨리면", anim_bug()
              + src(APPLE) + note("버그", "빠지거나 잘못 적힌 명령 때문에 생기는 오동작"), T),
        light("회의실 예약도 마찬가지", '<div class="twocol"><div>'
              + viz2.tiles([("요청", "「겹치는 예약은 막아 줘」"),
                            ("코드에 필요한 조건", "같은 회의실 · 같은 날짜 · 시간 겹침"),
                            ("겹칠 때 처리", "「이미 예약된 시간」 표시 · 저장 취소")], 1)
              + "</div><div>"
              + code("app.js · 겹치는 예약 막기 (1부 예제)", esc(
                  "const clash = load().some((x) =>\n"
                  "  x.room === b.room &&\n"
                  "  x.date === b.date &&\n"
                  "  x.start < b.end && b.start < x.end);\n"
                  "if (clash) {\n"
                  "  $(\"err\").textContent = \"이미 예약된 시간\";\n"
                  "  return;\n"
                  "}"))
              + "</div></div>", T),
        light("기존 코딩의 어려움", flow([("언어 학습", "문법 · 개발 도구"), ("코드 작성", "기능마다 직접 입력"),
                                       ("실행", "결과 확인"), ("오류 수정", "오류 메시지 해석")], hl=0)
              + viz2.tiles([("학습", "프로그래밍 언어 · 개발 도구 사용법"), ("작성", "모든 기능을 사람이 직접 입력"),
                            ("수정", "오류 메시지로 원인 추적")], 3), T),
        # ── 배경 · AI 코딩 도구의 변화
        light("AI 코딩 도구의 변화", eras()
              + note("막대", "사람 몫 · AI 몫의 상대 크기 (측정값 아님)")
              + src(("GitHub · 2021-06-29", "https://github.blog/2021-06-29-introducing-github-copilot-ai-pair-programmer/"),
                    ("OpenAI · 2022-11-30", "https://openai.com/index/chatgpt/"),
                    ("Anthropic · 2025-05-22", "https://www.anthropic.com/news/claude-4")), T),
        light("바이브코딩이라는 말", viz2.maprows([
            ("2023-01 · Karpathy", "「가장 인기 있는 새 프로그래밍 언어는 영어」", "자연어로 지시하는 시대 예고"),
            ("2025-02 · Karpathy", "「바이브코딩」 처음 사용", "코드 대신 느낌(vibe)과 결과로 만들기"),
            ("2025-11 · Collins 사전", "올해의 단어 선정", "자연어 지시로 AI가 코드를 작성하는 방식")], "시점", "사건")
              + src(("Karpathy · 2023-01-24", "https://x.com/karpathy/status/1617979122625712128"),
                    ("Karpathy · 2025-02-02", "https://x.com/karpathy/status/1886192184808149383"),
                    ("Collins · 2025-11-06", "https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/")), T),
        light("AI가 혼자 끝내는 작업 길이", '<div class="mwrap">' + metr_chart() + '<div class="mcards">'
              + '<div class="bn hl"><div class="bv">105<small>일</small></div><div class="bl">작업 길이 2배 주기 (2024년 이후)</div></div>'
              + '<div class="bn"><div class="bv">작업 길이</div><div class="bl">사람이 하면 걸리는 시간 기준</div></div>'
              + '</div></div>' + src(METR_TH), T),
        # ── 바이브코딩 = 통역사에게 맡기기
        light("바이브코딩 = 통역사에게 맡기기", anim_vibe()
              + note("바이브코딩", "자연어 요청 → AI가 코드 작성 → 사람이 결과 확인"), T),
        light("비유와 실제", viz2.maprows([
            ("나", "나", "요구 사항 설명"),
            ("통역사", "AI (Claude Code)", "코드 작성"),
            ("원시인", "컴퓨터", "코드 실행"),
            ("먹는 모습 보기", "화면 확인", "코드 대신 결과로 판단"),
            ("「씨는 뱉게 해 줘」", "수정 요청", "자연어로 다시 요청")], "원시인과 사과", "바이브코딩"), T),
        # ── 동작 원리
        light("바이브코딩의 반복 고리", anim_loop()
              + src(("Claude Code 문서 · How Claude Code works", "https://code.claude.com/docs/en/how-claude-code-works")), T),
        light("고리 한 바퀴 · 회의실 예약 예", viz2.tiles([
            ("① app.js 찾기", "맥락 파악 · 파일 검색"), ("② 예약 저장 코드 읽기", "맥락 파악 · 파일 읽기"),
            ("③ 겹침 규칙 추가", "작업 · 파일 수정"), ("④ 겹치게 예약 실행", "결과 확인 · 실행"),
            ("⑤ 오류 발견 → 다시 수정", "반복 · ② 작업으로"), ("⑥ 완료 보고", "「app.js 에 겹침 막기 추가」")], 3)
              + note("사람", "④ 결과를 화면에서 다시 확인 · 다르면 수정 요청"), T),
        light("내 일과 AI의 일", viz2.pair(
            "내 일", [("만들 것 정의", "기획서 · PRD"), ("동작 확인", "화면 직접 조작"), ("공개 결정", "배포 · 공유")],
            "AI의 일", [("코드 작성", "화면 · 규칙 · 저장"), ("오류 수정", "오류 메시지 해석 · 수정"), ("반복 작업", "파일 생성 · 명령 실행")], hl="l")
              + note("판단", "결과 확인 · 공개 결정은 사람"), T),
        # ── 할 수 있는 것 · 조심할 것
        light("바이브코딩으로 만든 것", viz2.tiles([
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
        light("통역사의 빈틈", big([("약 38%", "", "AI 생성 코드 작업 중 보안 취약점 발생 비율", True)], 1)
              + viz2.tiles([("키 노출 · Moltbook", "화면 코드에 DB 키 포함 · 이메일 3만 5천 개 유출"),
                            ("데이터 삭제 · Replit", "AI 에이전트가 운영 DB 데이터 삭제")], 2)
              + src(("Veracode · 2026-10-29", "https://www.veracode.com/blog/fall-2026-genai-code-security"),
                    ("Wiz · 2026-02-02", "https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys"),
                    ("Replit CEO · 2025-07-20", "https://x.com/amasad/status/1946986468586721478")), T),
        light("문제와 1부의 순서", viz2.maprows([
            ("AI가 빈칸을 추측으로 채움", "기획서 · PRD 작성", "1-3 · 1-4"),
            ("수정 후 이전 상태 복구 불가", "Git 저장 시점", "1-5"),
            ("오류 위치 파악 어려움", "기능 단위 작업 · 확인", "1-6"),
            ("키 · 개인정보 노출", "공개 전 점검", "1-7")], "바이브코딩의 문제", "1부에서 하는 일"), T),
        light("1부 완성 화면", shot("room_main.webp", "회의실 예약 · 1부 공통 예제 완성본", [
            ("하루 시간표", "회의실 3곳 · 30분 단위"), ("예약", "빈 칸 클릭 · 겹치면 차단"),
            ("공유", "배포 주소 (1-7)"), ("내 앱", "같은 순서로 하나 더")]), T),
    ]


CSS = """
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
  .v1vid video{width:100%; max-height:440px; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#F7EEDB; display:block;}
"""
