"""1-4 개발 계획.

기획서만 넘긴 결과(애니메이션) → 비유(조감도 · 설계 도면) → 기획서.md → 개발계획.md 다섯 칸(애니메이션) → 기능 하나 따라가기 → 완료 기준 · 태스크
→ 개발자 페르소나 · plan 모드로 세우기 → 실습.
입력 = 1-3 산출물 기획서.md · 예시 문장은 labs/mini_notion/예시/개발계획.md 에서 그대로 읽는다. 산출물 개발계획.md 는 1-6 개발의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import brief, chat, labcard, tstep
from v3kit import phmap

GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")

T = "1-4"
EX = Path(__file__).resolve().parent.parent / "labs" / "mini_notion" / "예시"
PERSONA = Path(__file__).resolve().parent.parent / "labs" / "persona"


def _persona(who):
    """페르소나 파일 전체 — 수강생이 그대로 따라 쓸 다섯 줄."""
    return (PERSONA / f"{who}.md").read_text(encoding="utf-8").strip()


def _prd():
    return (EX / "개발계획.md").read_text(encoding="utf-8").strip()


def _sec(no):
    """개발계획.md 의 「## no.」 칸을 제목 줄과 함께 그대로."""
    t = _prd()
    i = t.index(f"## {no}.")
    j = t.find("\n## ", i + 1)
    return t[i: j if j > 0 else None].strip()


def _line(no, key):
    """개발계획.md 의 「## no.」 칸에서 key 가 든 줄 하나."""
    import re
    x = next(x for x in _sec(no).split("\n") if key in x).strip()
    x = re.sub(r"^- (\[ \] )?", "", x)                       # 목록 · 체크 상자 기호
    return " · ".join(c.strip() for c in x.strip("|").split("|")) if x.startswith("|") else x


def _gaps():
    """기획서만 넘긴 결과 — 기획서 기능 칸의 한 단어(블록 · 저장)가 켜지고, 빈 칸 질문 → AI 추측이 차례로. 한 번 재생."""
    rows = [("블록", "블록 종류는?", "표 · 이미지 · 코드까지 열 가지"),
            ("저장", "어디에 저장?", "서버를 새로 만듦"),
            ("", "무엇부터 만들지?", "AI 가 정한 순서"),
            ("", "어디까지면 끝?", "기준 없음 · 대화마다 다름")]
    line = '페이지 · <u style="--d:1.0s">블록</u> · 「/」 메뉴 · 끌어 옮기기 · <u style="--d:2.6s">저장</u>'
    r = "".join(f'<div class="v14gR"><div class="v14gQ" style="--d:{1.2 + i * 1.6:.1f}s">{q}</div><i style="--d:{1.8 + i * 1.6:.1f}s">→</i>'
                f'<div class="v14gA" style="--d:{1.8 + i * 1.6:.1f}s">{g}</div></div>' for i, (_, q, g) in enumerate(rows))
    return (f'<div class="v14g"><div class="v14gL"><div class="v14gH">기획서.md · 기능 칸</div><div class="v14gT">{line}</div>'
            '<div class="v14gC">Claude Code 가 읽음</div></div>'
            f'<div class="v14gW"><div class="v14gHd"><span>빈 칸</span><span></span><span>AI 추측 · 예</span></div>{r}</div></div>'
            '<div class="v14gN" style="--d:8.2s"><b>빈 칸</b>묻지 않고 추측으로 채움 · 대화마다 다른 결과</div>')


# 기획서 칸 → 개발계획 칸 — (기획서에서 온 것, 새로 정하나, 개발계획 칸, 한 줄)
MAP = [("기능", False, "1. 기능", "F1~F5 · 기능 하나에 한 줄"),
       ("화면", False, "2. 화면", "화면마다 보이는 요소"),
       ("개발자 질문", True, "3. 데이터", "저장할 값 · 저장 위치"),
       ("문제점 · 이용자", False, "4. 완료 기준", "눌러서 확인할 문장"),
       ("개발자 질문", True, "5. 태스크", "만들 순서 · T1~T6")]


def _map():
    """기획서.md → 개발계획.md — 다섯 칸이 한 줄씩: 기획서 칸 → 화살표 → 개발계획 칸이 채워짐. 새로 정하는 칸은 주황(질문)."""
    r = ""
    for i, (frm, new, to, sub) in enumerate(MAP):
        d = .6 + i * 1.3
        r += (f'<div class="v14mR"><div class="v14mF{" q" if new else ""}" style="--d:{d:.1f}s">{"? " if new else ""}{frm}</div>'
              f'<i style="--d:{d + .4:.1f}s">→</i>'
              f'<div class="v14mT{" q" if new else ""}" style="--d:{d + .6:.1f}s"><b>{to}</b><span>{sub}</span></div></div>')
    return (f'<div class="v14m"><div class="v14mHd"><span>기획서.md</span><span></span><span>개발계획.md</span></div>{r}</div>'
            '<div class="v14mK" style="--d:7.4s"><span class="a">기획서에 있던 것 → 자세히 옮김</span><span class="b">없던 것 → 개발자가 묻고 내가 답함</span></div>')


def _thread():
    """기능 하나 따라가기 — F3 「/」 메뉴가 개발계획.md 다섯 칸에 어떻게 이어지는지 한 줄씩. 왼쪽 세로선을 점이 내려감."""
    rows = [("1. 기능", _line("1", "F3")), ("2. 화면", _line("2", "편집 화면")), ("3. 데이터", _line("3", "블록 종류")),
            ("4. 완료 기준", _line("4", "「/」")), ("5. 태스크", _line("5", "T3"))]
    r = "".join(f'<div class="v14tR" style="--d:{.4 + i * 1.2:.1f}s"><b>{h}</b><span>{esc(x)}</span></div>' for i, (h, x) in enumerate(rows))
    return f'<div class="v14t"><div class="v14tTag">F3 「/」 메뉴</div><div class="v14tL"><i class="v14tDot"></i>{r}</div></div>'


CSS = """
  /* 1-4 · 기획서만 넘긴 결과 (v14g) */
  .v14g{display:grid; grid-template-columns:330px 1fr; gap:28px; margin-top:20px; align-items:start;}
  .v14gL{background:#F4F6F9; border:2px solid #C9D6E6; border-radius:14px; padding:18px; opacity:0; animation:v14In .5s .2s forwards;}
  .v14gH{font-size:15px; font-weight:800; color:#6B7785; margin-bottom:10px;}
  .v14gT{font-size:21px; font-weight:700; color:#16233A; line-height:1.6; word-break:keep-all;}
  .v14gT u{text-decoration:none; border-radius:6px; padding:0 3px; animation:v14Hi .4s var(--d) forwards;}
  .v14gC{margin-top:16px; font-size:15px; color:#6B7785;}
  .v14gHd,.v14gR{display:grid; grid-template-columns:220px 36px 1fr; gap:10px; align-items:center;}
  .v14gHd span{font-size:15px; font-weight:800; color:#6B7785; padding-bottom:6px; border-bottom:2px solid #D9DDE3;}
  .v14gR{margin-top:12px;}
  .v14gQ{background:#fff; border:2px dashed #9AA6B4; border-radius:12px; padding:12px 14px; font-size:19px; font-weight:700; color:#16233A; opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14gR i{font-style:normal; font-weight:800; font-size:20px; color:#C0392B; opacity:0; animation:v14In .3s var(--d) forwards;}
  .v14gA{background:#FDECEA; border:2px solid #E6B0AA; border-radius:12px; padding:12px 14px; font-size:19px; font-weight:700; color:#C0392B; opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14gN{margin-top:22px; display:flex; gap:12px; align-items:center; font-size:19px; font-weight:700; color:#16233A; opacity:0; animation:v14In .5s var(--d) forwards;}
  .v14gN b{background:#C0392B; color:#fff; border-radius:8px; padding:4px 10px; font-size:15px;}
  /* 1-4 · 기획서.md → 개발계획.md (v14m) */
  .v14m{margin-top:16px;}
  .v14mHd,.v14mR{display:grid; grid-template-columns:260px 50px 1fr; gap:12px; align-items:center;}
  .v14mHd span{font-size:16px; font-weight:800; color:#16233A; padding-bottom:6px; border-bottom:3px solid #16233A;}
  .v14mHd span:last-child{color:#C76A12; border-color:#F28C28;}
  .v14mR{margin-top:11px;}
  .v14mF{background:#F4F6F9; border:2px solid #C9D6E6; border-radius:12px; padding:13px 16px; font-size:20px; font-weight:800; color:#16233A; opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14mF.q{background:#FFF1E2; border:2px dashed #F28C28; color:#C76A12;}
  .v14mR i{font-style:normal; font-weight:800; font-size:22px; color:#F28C28; text-align:center; opacity:0; animation:v14In .3s var(--d) forwards;}
  .v14mT{display:flex; gap:16px; align-items:baseline; background:#fff; border:2px solid #C9D6E6; border-radius:12px; padding:13px 16px; opacity:0; transform:translateX(-12px); animation:v14In .5s var(--d) forwards;}
  .v14mT.q{border-color:#F28C28;}
  .v14mT b{font-size:20px; color:#16233A; min-width:120px;} .v14mT span{font-size:17px; color:#3A4657;}
  .v14mK{margin-top:20px; display:flex; gap:14px; opacity:0; animation:v14In .5s var(--d) forwards;}
  .v14mK span{flex:1; border-radius:12px; padding:11px 14px; font-size:17px; font-weight:700;}
  .v14mK .a{background:#F4F6F9; color:#16233A;} .v14mK .b{background:#FFF1E2; color:#C76A12;}
  /* 1-4 · 기능 하나 따라가기 (v14t) */
  .v14t{margin-top:14px;}
  .v14tTag{display:inline-block; background:#16233A; color:#fff; font-size:19px; font-weight:800; border-radius:10px; padding:8px 16px; opacity:0; animation:v14In .4s .1s forwards;}
  .v14tL{position:relative; margin:14px 0 0 18px; padding-left:30px; border-left:3px solid #C9D6E6;}
  .v14tDot{position:absolute; left:-10px; top:0; width:17px; height:17px; border-radius:50%; background:#F28C28; animation:v14Dn 6s .4s forwards;}
  .v14tR{display:grid; grid-template-columns:150px 1fr; gap:16px; align-items:center; background:#fff; border:2px solid #C9D6E6; border-radius:12px;
    padding:12px 16px; margin-bottom:11px; opacity:0; transform:translateX(-12px); animation:v14In .5s var(--d) forwards;}
  .v14tR b{font-size:19px; color:#C76A12;} .v14tR span{font-size:17.5px; color:#16233A; font-weight:600;}
  @keyframes v14In{to{opacity:1; transform:none;}}
  @keyframes v14Hi{to{background:#FDECEA; color:#C0392B; box-shadow:0 0 0 2px #E6B0AA;}}
  @keyframes v14Dn{to{top:calc(100% - 20px);}}
  @media print{.v14gL,.v14gQ,.v14gR i,.v14gA,.v14gN,.v14mF,.v14mR i,.v14mT,.v14mK,.v14tTag,.v14tR{opacity:1; animation:none; transform:none}}
"""


def slides():
    return [
        # ── 배경 → 비유 → 애니메이션
        light("기획서만 넘긴 결과", _gaps(), T),
        light("조감도와 설계 도면", phmap("v1_u4_blueprint.webp", "조감도와 설계 도면", *GEN, viz2.maprows([
                  ("조감도", "기획서", "어떤 집인지 · 왜"), ("설계 도면", "개발 계획", "기능 · 화면 · 데이터"),
                  ("공정표", "태스크", "무엇부터 짓나"), ("준공 검사", "완료 기준", "도면대로 지었나")], "집 짓기", "앱 만들기")), T),
        # ── 개발 계획
        light("기획서.md → 개발계획.md", _map(), T),
        light("기능 하나 따라가기", _thread() + note("파일", "labs/mini_notion/예시/개발계획.md"), T),
        ba("확인 가능한 완료 기준", T, "「메모가 잘 저장된다」\n「블록을 쉽게 바꾼다」",
           "「주간 회의록에 체크 상자 「보고서 초안」 추가 후 새로고침해도 남아 있다」\n「빈 블록에 「/」 → 「체크 상자」 고르면 체크 상자로 바뀐다」",
           "값 · 동작 · 결과가 다 들어간 문장"),
        # ── 태스크
        light("태스크", viz2.maprows([
            ("T1 화면 뼈대 · 페이지 목록", "F1", "왼쪽 목록 · 새 페이지 · 삭제"), ("T2 블록 편집", "F2", "엔터로 새 블록 · 체크 상자 체크"),
            ("T3 「/」 메뉴", "F3", "「/」 → 메뉴 → 블록 종류 바뀜"), ("T4 블록 끌어 옮기기", "F4", "손잡이로 순서 바뀜"),
            ("T5 저장", "F5", "새로고침 뒤 그대로"), ("T6 완료 기준 점검", "완료 기준", "모바일 폭 · 다섯 줄 모두 ✓")], "태스크", "기능 하나 = 태스크 하나"), T),
        # ── 개발자 페르소나 · plan 모드
        light("개발자 페르소나", '<div class="twocol"><div>' + code("개발자.md", esc(_persona("개발자")))
              + '</div><div>' + viz2.tiles([("만들기", "기획자.md 옆에 새 파일 · 네 줄"), ("기획자.md 와 차이", "역할 · 마지막 줄 칸"),
                                          ("첫 줄", "기획서에 없는 것은 먼저 질문")], 1) + "</div></div>", T),
        light("개발 계획 대화 예시", chat([
            ("me", "개발자.md 대로 기획서.md 를 읽고 개발 계획을 세워 줘"),
            ("ai", "블록 종류는 몇 가지로 할까요? 페이지는 어디에 저장할까요?\n저장 위치 · 서버 또는 내 브라우저 (서버는 로그인 필요)"),
            ("me", "제목 · 글 · 체크 상자 · 구분선 네 가지 · 내 브라우저에 저장"),
            ("ai", "계획: 기능 F1~F5 · 태스크 T1~T6 · 완료 기준 5개\n승인하면 개발계획.md 로 저장한다.")], "Plan Mode 대화 예"), T),
        # ── 실습
        labcard("1-4", "기획서로 개발 계획 세우기", T, "기획서.md", "개발계획.md", ["개발자 페르소나", "Plan Mode"]),
        brief("1-4", T, ["개발자.md 만들기", "모드 표시 → Plan · 「개발자.md 대로 기획서.md 를 읽고 개발 계획을 세워 줘」 · 질문에 답하기",
                         "계획에 피드백", "승인 → 개발계획.md"],
              [],
              ["개발자 페르소나", "완료 기준", "태스크"],
              ["개발계획.md 다섯 칸이 생김", "태스크마다 끝나면 보이는 화면이 적힘"],
              "계획이 너무 길면 「태스크를 여섯 개 안으로 줄여 줘」"),
        tstep("1-4", 1, "개발자.md 만들기", T, term=("mini_notion/개발자.md", _persona("개발자")),
              rows=[("만들기", "VS Code 탐색기 → 새 파일 → 개발자.md"), ("쓰기", "네 줄 · 말투는 바꿔도 됨"), ("저장", "macOS ⌘S · Windows Ctrl+S")]),
        tstep("1-4", 2, "Plan Mode 요청 · 질문", T, "lab14_q1.webp", "개발자 페르소나의 선택 질문",
              rows=[("Plan Mode", "모드 표시 → Plan · 1-3 과 같음"), ("질문", "저장 방식 · 기술 · 기획서에 없던 것"), ("1부 선택", "순수 HTML/JS · localStorage")]),
        tstep("1-4", 3, "계획에 피드백", T, "lab14_feedback.webp", "3번 고칠 점 적기",
              rows=[("3번", "Tell Claude what to change"), ("피드백", "정렬 순서 · 파일 이름"), ("다시", "고친 계획 → 승인")]),
        tstep("1-4", 4, "개발계획.md 저장", T, "lab14_saved.webp", "개발계획.md 저장 결과",
              rows=[("결과", "개발계획.md · F 번호 · T 번호"), ("반영", "피드백 두 가지"), ("코드", "아직 없음")]),
        light("실습 1-4 확인", checks([
            ("기획서 기능이 다 들어 있나", "빠졌으면 추가 요청"), ("태스크마다 F 번호가 있나", "기능 하나 = 태스크 하나"),
            ("저장 위치가 적혀 있나", "예 · 내 브라우저 localStorage"), ("완료 기준을 눌러서 확인할 수 있나", "값 · 동작 · 결과")],
            "「아니요」 → 그 칸만 다시 요청 · 넷 다 「예」 → 1-5"), T),
    ]
