"""1-1 바이브코딩이란 — 실습 없음.

비유 한 줄로 끝까지 잇는다.
  코딩 = 사과를 처음 보는 원시인(컴퓨터)에게 원시인 말로 하나하나 가르치기 · 빠뜨리면 그대로 실수(버그)
  바이브코딩 = 우리말로 말하면 통역사(AI)가 원시인 말로 풀어 가르치고 · 나는 먹는 모습을 보고 판단
→ 말의 유래 · 흐름 · 내 일과 AI 일 · 만든 것 · 한계(통역사도 빠뜨린다) · 1부 순서 · 완성 화면.
사실 출처: scratchpad/v1_facts.md (Karpathy · Collins · levels.io · MenuGen · Veracode · Wiz · Replit)
"""
import viz2
from anim import BG, K, N, O, OK, R, S, W, _D, _t
from deck import flow, light
from hx import code, esc, note
from stats_hx import big, quote, src
from v1kit import shot

T = "1-1"
BROWN = "#8D5A2B"
STEPS = ["① 이건 「사과」 · 먹는 것", "② 손으로 집는다", "③ 입에 넣고 깨문다", "④ 씨는 뱉는다"]


# ── 그림 조각 ─────────────────────────────────────────
def _person(x, y, color=K, cave=False):
    """서 있는 사람 · cave=True 면 원시인(헝클어진 머리 · 가죽옷)."""
    hair = ""
    if cave:
        spikes = " ".join(f"L{x - 26 + i * 8:g} {y - 70 - (8 if i % 2 else 0):g}" for i in range(8))
        hair = f'<path d="M{x - 28:g} {y - 52:g} {spikes} L{x + 28:g} {y - 52:g} Z" fill="{BROWN}"/>'
    body = (f'<line x1="{x:g}" y1="{y - 30:g}" x2="{x:g}" y2="{y + 40:g}" stroke="{color}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{x:g}" y1="{y - 10:g}" x2="{x - 32:g}" y2="{y + 18:g}" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
            f'<line x1="{x:g}" y1="{y - 10:g}" x2="{x + 32:g}" y2="{y + 18:g}" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
            f'<line x1="{x:g}" y1="{y + 40:g}" x2="{x - 22:g}" y2="{y + 92:g}" stroke="{color}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{x:g}" y1="{y + 40:g}" x2="{x + 22:g}" y2="{y + 92:g}" stroke="{color}" stroke-width="7" stroke-linecap="round"/>')
    tunic = (f'<path d="M{x - 24:g} {y - 18:g} L{x + 24:g} {y - 18:g} L{x + 30:g} {y + 46:g} L{x + 14:g} {y + 38:g} '
             f'L{x:g} {y + 48:g} L{x - 14:g} {y + 38:g} L{x - 30:g} {y + 46:g} Z" fill="{BROWN}"/>') if cave else ""
    head = f'<circle cx="{x:g}" cy="{y - 52:g}" r="24" fill="#F6D7B0" stroke="{color}" stroke-width="3"/>'
    return body + tunic + hair + head


def _apple(x, y, r=20):
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{R}"/>'
            f'<line x1="{x:g}" y1="{y - r:g}" x2="{x + 3:g}" y2="{y - r - 10:g}" stroke="{BROWN}" stroke-width="3"/>'
            f'<ellipse cx="{x + 10:g}" cy="{y - r - 6:g}" rx="8" ry="4" fill="{OK}"/>')


def _card(x, y, w, s, fill=W, stroke=K, cls="tn", dash=False):
    d = ' stroke-dasharray="7 6"' if dash else ""
    return (f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="48" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2.2"{d}/>'
            + _t(x + 18, y + 25, s, cls, "start"))


def _scene(p, steps, missing=None):
    """나 → 원시인 말로 한 줄씩 → 원시인이 그대로 해 본다. missing: 빠뜨린 줄 번호."""
    d = _D(p, 11)
    b = [f'<rect x="0" y="0" width="1160" height="420" rx="18" fill="{BG}"/>',
         _person(110, 210), _t(110, 340, "나", "tt"),
         _t(560, 34, "원시인이 아는 말로 · 하나씩 · 빠짐없이", "to")]
    for i, s in enumerate(steps):
        y = 62 + i * 66
        if i == missing:
            b.append(f'<g {d.show(10 + i * 11)}>{_card(330, y, 460, "④ (빠뜨림)", "#FFF", R, "ts", True)}</g>')
        else:
            b.append(f'<g {d.show(10 + i * 11)}>{_card(330, y, 460, s)}</g>')
        b.append(f'<line x1="790" y1="{y + 24}" x2="900" y2="{y + 24}" stroke="{S}" stroke-width="1.5" stroke-dasharray="4 5" {d.show(10 + i * 11)}/>')
    b += [_person(990, 210, K, cave=True), _t(990, 340, "원시인 = 컴퓨터", "tt"), _t(990, 368, "사과를 처음 본다", "ts")]
    # 사과 — 처음엔 원시인 앞 → 적힌 대로 손 → 입
    stops = [(0, "transform:translate(0px,0px)"), (60, "transform:translate(0px,0px)"),
             (70, "transform:translate(32px,-20px)"), (80, "transform:translate(10px,-70px)"), (100, "transform:translate(10px,-70px)")]
    b.append(f'<g {d.a(stops)}>{_apple(1050, 250)}</g>')
    if missing is None:
        b.append(f'<g {d.show(84)}><rect x="880" y="20" width="220" height="44" rx="22" fill="{OK}"/>'
                 + _t(990, 43, "✓ 먹었다", "tw") + "</g>")
    else:
        b.append(f'<g {d.show(84)}><rect x="860" y="20" width="260" height="44" rx="22" fill="{R}"/>'
                 + _t(990, 43, "✕ 씨까지 삼켰다", "tw") + "</g>")
    return d.svg(1160, 420, "".join(b))


def anim_teach():
    """원시인에게 사과 먹는 법을 네 줄로 가르친다 → 그대로 먹는다. 11초 · 한 번."""
    return _scene("ap", STEPS)


def anim_bug():
    """④ 를 빠뜨림 → 원시인은 적힌 그대로 · 씨까지 삼킨다. 11초 · 한 번."""
    return _scene("aq", STEPS, missing=3)


def anim_vibe():
    """나는 우리말 한 줄 → 통역사(AI)가 원시인 말 네 줄로 → 원시인이 먹고 → 나는 결과만 본다. 12초 · 한 번."""
    d = _D("vb", 12)
    b = [f'<rect x="0" y="0" width="1160" height="420" rx="18" fill="{BG}"/>',
         _person(90, 230), _t(90, 360, "나", "tt"), _t(90, 388, "우리말로 한 줄", "ts")]
    # 우리말 요청 말풍선
    b.append(f'<g {d.show(4)}><rect x="20" y="40" width="300" height="52" rx="26" fill="{W}" stroke="{O}" stroke-width="2.5"/>'
             + _t(170, 67, "「사과 먹는 법 알려 줘」", "tn") + "</g>")
    b.append(f'<line x1="320" y1="66" x2="372" y2="180" stroke="{O}" stroke-width="3" marker-end="url(#{d.id("o")})" {d.show(12)}/>')
    # 통역사 = AI
    b.append(f'<g {d.show(14)}><rect x="300" y="182" width="200" height="96" rx="16" fill="{N}"/>'
             + _t(400, 216, "통역사", "tw") + _t(400, 246, "AI · Claude Code", "tw") + "</g>")
    for i, s in enumerate(STEPS):
        y = 62 + i * 66
        b.append(f'<g {d.show(24 + i * 7)}>{_card(560, y, 330, s)}</g>')
        b.append(f'<line x1="500" y1="230" x2="556" y2="{y + 24}" stroke="{S}" stroke-width="1.5" {d.show(24 + i * 7)}/>')
    b += [_person(1030, 230, K, cave=True), _t(1030, 360, "원시인 = 컴퓨터", "tt")]
    stops = [(0, "transform:translate(0px,0px)"), (62, "transform:translate(0px,0px)"),
             (72, "transform:translate(30px,-20px)"), (80, "transform:translate(10px,-70px)"), (100, "transform:translate(10px,-70px)")]
    b.append(f'<g {d.a(stops)}>{_apple(1088, 270)}</g>')
    # 나는 결과만 본다
    b.append(f'<g {d.show(86)}><rect x="20" y="110" width="300" height="48" rx="24" fill="{OK}"/>'
             + _t(170, 135, "잘 먹나? ✓ 확인", "tw") + "</g>")
    return d.svg(1160, 420, "".join(b))


def slides():
    return [
        # ── 코딩 = 원시인에게 사과 가르치기
        light("컴퓨터 = 사과를 처음 보는 원시인", anim_teach()
              + note("코딩", "컴퓨터가 알아듣는 말로 · 할 일을 하나하나 빠짐없이 적는 일"), T),
        light("하나라도 빠뜨리면", anim_bug()
              + note("버그", "컴퓨터는 적힌 그대로만 한다 · 빠뜨린 한 줄이 그대로 실수가 된다"), T),
        light("회의실 예약도 마찬가지", '<div class="twocol"><div>'
              + viz2.tiles([("사람 말", "「겹치는 예약은 막아 줘」 한 문장"),
                            ("컴퓨터에게는", "같은 회의실? · 같은 날? · 시간이 겹치나?"),
                            ("겹치면", "「이미 예약된 시간」 표시 · 저장 안 함")], 1)
              + "</div><div>"
              + code("app.js · 원시인 말로 적은 것 (1부 예제)", esc(
                  "const clash = load().some((x) =>\n"
                  "  x.room === b.room &&\n"
                  "  x.date === b.date &&\n"
                  "  x.start < b.end && b.start < x.end);\n"
                  "if (clash) {\n"
                  "  $(\"err\").textContent = \"이미 예약된 시간\";\n"
                  "  return;\n"
                  "}"))
              + "</div></div>", T),
        light("기존 코딩의 어려움", flow([("원시인 말 배우기", "문법 · 개발 도구"), ("하나하나 적기", "기능마다 직접"),
                                       ("시켜 보기", "실행"), ("빠뜨린 곳 찾기", "오류 문장 해석")], hl=0)
              + viz2.tiles([("배우는 데", "원시인 말(프로그래밍 언어)부터"), ("만드는 데", "한 줄씩 직접 타이핑"),
                            ("고치는 데", "어디서 빠뜨렸는지 직접 찾기")], 3), T),
        # ── 바이브코딩 = 통역사에게 맡기기
        light("바이브코딩 = 통역사에게 맡기기", anim_vibe()
              + note("바이브코딩", "나는 우리말로 원하는 것을 말하고 · 원시인 말은 AI가 쓴다 · 나는 결과를 본다"), T),
        light("비유와 실제", viz2.maprows([
            ("나", "나", "원하는 것을 우리말로"),
            ("통역사", "AI (Claude Code)", "코드를 대신 쓴다"),
            ("원시인", "컴퓨터", "적힌 코드를 그대로 실행"),
            ("먹는 모습 보기", "화면을 눌러 확인", "코드 대신 결과를 본다"),
            ("「씨는 뱉게 해 줘」", "말로 고치기", "빠진 것을 다시 요청")], "원시인과 사과", "바이브코딩"), T),
        light("바이브코딩이라는 말", quote(
            "코드가 있다는 것조차 잊고 · 느낌(vibe)에 맡기는 새로운 코딩",
            "Andrej Karpathy · 2025-02-02 · 처음 쓴 말 (번역)")
              + big([("2025", "", "Collins 사전 올해의 단어", True), ("자연어", "", "사람 말로 AI에게 코드를 쓰게 하는 것 (사전 뜻)")], 2)
              + src(("Karpathy · X", "https://x.com/karpathy/status/1886192184808149383"),
                    ("Collins · 2025-11-06", "https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/")), T),
        light("바이브코딩의 흐름", flow([("말로 요청", "「겹치는 예약은 막아 줘」"), ("AI가 코드 작성", "app.js 에 규칙 추가"),
                                       ("실행해 보기", "겹치게 예약 → 막힘?"), ("말로 고치기", "「오류 문구를 빨간색으로」")], hl=2)
              + viz2.tiles([("한 바퀴", "요청 → 작성 → 확인"), ("여러 바퀴", "작게 나눠 여러 번 돌린다 (1-6)"),
                            ("사람의 일", "원하는 것을 말하고 결과를 판단")], 3), T),
        light("내 일과 AI의 일", viz2.pair(
            "내 일", [("무엇을 만들지", "기획서 · PRD"), ("되는지 판단", "화면을 눌러 확인"), ("공개 여부 결정", "배포 · 공유")],
            "AI의 일", [("코드 작성", "화면 · 규칙 · 저장"), ("오류 수정", "오류 문장 읽고 고침"), ("반복 작업", "파일 만들기 · 명령 실행")], hl="l")
              + note("판단은 사람", "AI는 시킨 것을 만들고 · 맞는지는 사람이 본다"), T),
        # ── 할 수 있는 것 · 조심할 것
        light("바이브코딩으로 만든 것", viz2.tiles([
            ("브라우저 3D 비행 게임", "fly.pieter.com · 혼자 AI와 만든 게임"),
            ("메뉴판 사진 → 음식 그림", "MenuGen · Karpathy 가 만든 서비스"),
            ("내 업무 도구", "예약 · 체크리스트 · 계산기 (1부에서 만들 것)")], 3)
              + note("배울 점", "만들기는 빨라졌다 · 남에게 공개하는 일은 따로 배워야 한다 (1-7)")
              + src(("levelsio · X", "https://x.com/levelsio/status/1899596115210891751"),
                    ("Karpathy · MenuGen", "https://karpathy.bearblog.dev/vibe-coding-menugen/")), T),
        light("가능성과 한계", viz2.fit(
            [("화면 1~3개 웹 페이지", "예약 · 투표 · 체크리스트"), ("내 업무 도우미", "계산기 · 정리 도구"), ("시제품", "아이디어를 화면으로")],
            [("돈 · 개인정보를 다루는 서비스", "보안 점검이 따로 필요"), ("많은 사람이 동시에 쓰는 서비스", "서버 · DB 설계"),
             ("코드를 안 보고 운영", "고장 원인을 못 찾음")],
            gt="지금 만들기 좋은 앱", bt="아직 어려운 앱"), T),
        light("통역사의 빈틈", big([("약 38%", "", "AI가 쓴 코드 중 보안 구멍이 생긴 작업", True)], 1)
              + viz2.tiles([("열쇠를 문 앞에", "화면 코드에 DB 키 · 이메일 3만 5천 개 노출 (Moltbook)"),
                            ("창고를 비움", "에이전트가 운영 데이터를 삭제 (Replit)")], 2)
              + src(("Veracode · 2026-10-29", "https://www.veracode.com/blog/fall-2026-genai-code-security"),
                    ("Wiz · 2026-02-02", "https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys"),
                    ("Replit CEO · 2025-07-20", "https://x.com/amasad/status/1946986468586721478")), T),
        light("문제와 1부의 순서", viz2.maprows([
            ("원하는 것을 AI가 추측으로 채움", "기획서 · PRD 를 먼저", "1-3 · 1-4"),
            ("고친 뒤 망가지면 되돌릴 수 없음", "Git 으로 저장 시점 남기기", "1-5"),
            ("한 번에 다 만들면 어디가 틀렸는지 모름", "작게 나눠 확인하며", "1-6"),
            ("키 · 개인정보가 그대로 공개", "공개 전 확인", "1-7")], "바이브코딩의 문제", "1부에서 하는 일"), T),
        light("1부 완성 화면", shot("room_main.webp", "회의실 예약 · 1부 공통 예제 완성본", [
            ("날짜 하나 · 회의실 3곳", "하루 시간표 · 30분 칸"), ("빈 칸 클릭", "예약 · 겹치면 막힘"),
            ("인터넷 주소로 공유", "1-7 배포까지"), ("내 아이디어", "같은 순서로 하나 더")]), T),
    ]
