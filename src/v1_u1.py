"""1-1 바이브코딩이란 — 실습 없음.

비유 한 줄로 끝까지 잇는다.
  코딩 = 사과를 처음 보는 원시인(컴퓨터)에게 원시인 말로 하나하나 가르치기 · 빠뜨리면 그대로 실수(버그)
  바이브코딩 = 우리말로 말하면 통역사(AI)가 원시인 말(코드)로 풀어 쓰고 · 나는 결과를 보고 판단
→ 말의 유래 · 흐름 · 내 일과 AI 일 · 만든 것 · 한계(통역사도 빠뜨린다) · 1부 순서 · 완성 화면.
사실 출처: scratchpad/v1_facts.md (Karpathy · Collins · levels.io · MenuGen · Veracode · Wiz · Replit)
"""
import viz2
from anim import BG, G, N, O, OK, R, W, _D, _t
from deck import flow, light
from hx import code, esc, note
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


def anim_teach():
    """가르치는 말 네 줄을 한 줄씩 실행 → 원시인이 그대로 해서 잘 먹는다. 12초 · 한 번."""
    return _scene("ap")


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


def slides():
    return [
        # ── 코딩 = 원시인에게 사과 가르치기
        light("사과를 처음 보는 원시인", '<div class="v1shot v1vid"><figure>'
              '<video src="img/v1_caveman.mp4" poster="img/v1_caveman.webp" autoplay muted loop playsinline></video>'
              '<figcaption>AI 생성 영상 · Z-Image Turbo · Wan 2.2 (Apache 2.0)</figcaption></figure><div class="v1side">'
              + "".join(f'<div class="v1sd"><b>{h}</b><span>{x}</span></div>' for h, x in [
                  ("처음 보는 물건", "사과가 무엇인지 모른다"), ("먹는 법도 모른다", "돌려 보고 · 냄새만 맡는다"),
                  ("알려 준 것만 한다", "빠뜨리면 그대로 실수"), ("컴퓨터도 같다", "알려 주는 글 = 코드")])
              + "</div></div>", T),
        light("코딩 = 하나하나 가르치기", anim_teach()
              + src(APPLE) + note("코딩", "컴퓨터가 알아듣는 말로 · 할 일을 하나하나 빠짐없이 적는 일"), T),
        light("하나라도 빠뜨리면", anim_bug()
              + src(APPLE) + note("버그", "컴퓨터는 적힌 그대로만 한다 · 빠뜨린 한 줄이 그대로 실수가 된다"), T),
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


CSS = """
  /* 1-1 · 비유 영상 */
  .v1vid video{width:100%; max-height:440px; border:1.5px solid #D9DDE3; border-radius:12px; box-shadow:0 8px 22px rgba(15,27,45,.10); background:#F7EEDB; display:block;}
"""
