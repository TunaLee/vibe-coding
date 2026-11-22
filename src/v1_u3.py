"""1-3 기획서 작성.

왜 기획하나(모호 vs 구체 · 개발 흐름) → 만들 것(미니 노션) → 기획서 다섯 칸 → Plan Mode → 페르소나(직접 쓰는 다섯 줄) → 대화 · 피드백 → 실습.
예시 문장은 labs/mini_notion/예시/기획서.md 에서 그대로 읽는다. 산출물 기획서.md 는 1-4 개발 계획의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import brief, chat, shot, labcard, tstep

T = "1-3"
EX = Path(__file__).resolve().parent.parent / "labs" / "mini_notion" / "예시"
PERSONA = Path(__file__).resolve().parent.parent / "labs" / "persona"


def _persona(who):
    """페르소나 파일 전체 — 수강생이 그대로 따라 쓸 다섯 줄."""
    return (PERSONA / f"{who}.md").read_text(encoding="utf-8").strip()


def _plan():
    return (EX / "기획서.md").read_text(encoding="utf-8").strip()


def _heads():
    return "\n".join(x for x in _plan().split("\n") if x.startswith("#"))


# IT 기업 개발 흐름 — (단계, 담당, 산출물, 1부 단원, 1부에서 하는 일)
DEVFLOW = [
    ("기획", "기획자 · PM", "기획서", "1-3", "기획자 페르소나 · 기획서.md"),
    ("요구사항 정의", "PM · 개발 리드", "PRD", "1-4", "개발계획.md · 기능 · 완료 기준"),
    ("설계", "디자이너 · 개발자", "화면 · 구조 설계", "1-4", "개발계획.md · 화면 · 데이터"),
    ("개발 계획", "개발 리드", "태스크 · 일정", "1-4", "개발자 페르소나 · 태스크 T1~T6"),
    ("개발", "개발자", "코드 · 커밋", "1-5 · 1-6", "Claude Code · Git"),
    ("테스트", "QA", "버그 목록", "1-6", "완료 기준 확인"),
    ("배포 · 회고", "개발 · 운영", "서비스 주소", "1-7 · 1-8", "배포 주소 · 회고"),
]


def _devflow():
    c = "".join(f'<div class="v1dfc" style="--d:{.3 + i * .6:.1f}s"><i>{i + 1}</i><b>{st}</b>'
                f'<span>{who}</span><em>{out}</em></div>' for i, (st, who, out, _, _) in enumerate(DEVFLOW))
    return f'<div class="v1df">{c}</div>'


def _devmap():
    head = "".join(f'<div class="v1dmh">{st}</div>' for st, *_ in DEVFLOW)
    co = "".join(f'<div class="v1dmc">{who}</div>' for _, who, *_ in DEVFLOW)
    me = "".join(f'<div class="v1dmm" style="--d:{.4 + i * .45:.2f}s"><b>{w}</b></div>'
                 for i, (_, _, _, u, w) in enumerate(DEVFLOW))
    return (f'<div class="v1dm"><div class="v1dml"></div>{head}'
            f'<div class="v1dml">회사<small>역할별 담당자</small></div>{co}'
            f'<div class="v1dml on">1부<small>나 · Claude · Claude Code</small></div>{me}</div>')


CSS = """
  /* 1-3 · 기획서 구성 애니메이션 (v1pl) */
  .v1plW{display:grid; grid-template-columns:360px 44px 1fr; gap:14px; align-items:center; margin-top:4px;}
  .v1plL{display:flex; flex-direction:column; gap:10px;}
  .v1plH{font-size:18px; font-weight:800; color:#3A4657;}
  .v1plS{font-size:21px; font-weight:800; color:#16233A; background:#fff; border:2px solid #D9DDE3; border-radius:12px; padding:9px 14px;
    opacity:0; animation:v1plIn .5s var(--d) forwards, v1plHi .6s var(--h) forwards;}
  .v1plS.msg{background:#FFFBEA; border-color:#F2DE9B;} .v1plS em{display:block; font-style:normal; font-size:13px; font-weight:800; color:#8A94A3;}
  .v1plA{font-size:40px; font-weight:900; color:#F28C28; text-align:center; opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1plD{background:#fff; border:3px solid #16233A; border-radius:16px; padding:12px 16px; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  .v1plF{font-family:var(--mono); font-size:15px; font-weight:700; color:#fff; background:#16233A; border-radius:8px; padding:4px 10px; display:inline-block; margin-bottom:6px;}
  .v1plR{display:grid; grid-template-columns:140px 1fr auto; gap:14px; align-items:center; padding:11px 10px; border-top:1.5px solid #E3E6EA; border-radius:10px;
    animation:v1plRow 1.6s var(--h) both;}
  .v1plR b{font-size:20px; color:#E07A12;}
  .v1plT{font-size:21px; font-weight:800; color:#16233A; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  .v1plR.no .v1plT{text-decoration:line-through; text-decoration-color:#C0392B; text-decoration-thickness:3px; color:#6B7785;}
  .v1plR i{font-style:normal; font-size:14px; font-weight:800; color:#fff; background:#16233A; border-radius:8px; padding:3px 10px; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  @keyframes v1plIn{from{opacity:0} to{opacity:1}}
  @keyframes v1plHi{to{border-color:#F28C28; box-shadow:0 0 0 3px #FCD9B3; opacity:.5}}
  @keyframes v1plRow{0%{background:transparent} 25%{background:#FFE7CC} 100%{background:transparent}}
  @media print{.v1plS,.v1plA,.v1plD,.v1plT,.v1plR i{opacity:1; animation:none} .v1plR{animation:none}}
  /* 1-3 · 피드백 반영 애니메이션 (v1rw) */
  .v1rwW{display:flex; flex-direction:column; gap:26px; margin-top:40px;}
  .v1rwR{display:grid; grid-template-columns:150px 1fr 40px 1fr 40px 1.15fr; gap:12px; align-items:center;}
  .v1rwTop span{font-size:16px; font-weight:800; color:#6B7785;}
  .v1rwH{font-size:23px; font-weight:800; color:#16233A; opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1rwV{font-size:24px; font-weight:800; color:#16233A; background:#F4F6F9; border-radius:14px; padding:22px 18px;
    opacity:0; animation:v1plIn .5s var(--d) forwards, v1rwX .6s var(--x) forwards;}
  .v1rwV u{text-decoration:none; border-radius:4px; padding:0 2px; animation:v1rwU .6s var(--u) forwards;}
  .v1rwA{font-style:normal; font-size:30px; font-weight:900; color:#F28C28; text-align:center; opacity:0; animation:v1plIn .4s var(--d) forwards;}
  .v1rwQ{font-size:21px; font-weight:800; color:#16233A; background:#FFF8F0; border:2.5px solid #F28C28; border-radius:16px; padding:20px 16px;
    opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1rwN{font-size:24px; font-weight:800; color:#1E7B45; background:#F1FAF4; border:2.5px solid #6FB585; border-radius:14px; padding:22px 18px;
    opacity:0; animation:v1plIn .6s var(--d) forwards;}
  @keyframes v1rwU{to{background:#FDECEA; color:#C0392B; box-shadow:0 0 0 2px #E6B0AA;}}
  @keyframes v1rwX{to{opacity:.4; text-decoration:line-through;}}
  @media print{.v1rwH,.v1rwV,.v1rwQ,.v1rwN,.v1rwA{opacity:1; animation:none}}
  /* 1-3 · IT 기업 개발 흐름 (v1df · v1dm) */
  .v1df{display:grid; grid-template-columns:repeat(7,1fr); gap:10px; margin-top:26px;}
  .v1dfc{position:relative; background:#fff; border:2px solid #C9D6E6; border-radius:14px; padding:16px 10px 18px; text-align:center;
    opacity:0; animation:v1dfIn .5s var(--d) forwards;}
  .v1dfc:not(:last-child)::after{content:"→"; position:absolute; right:-14px; top:44%; font-size:20px; font-weight:800; color:#F28C28;}
  .v1dfc i{display:inline-flex; width:30px; height:30px; border-radius:50%; background:#16233A; color:#fff; font-style:normal;
    font-weight:800; align-items:center; justify-content:center; font-size:15px; margin-bottom:10px;}
  .v1dfc b{display:block; font-size:21px; color:#16233A; margin-bottom:12px; letter-spacing:-.02em;}
  .v1dfc span{display:block; font-size:15px; color:#6B7785; margin-bottom:12px; min-height:38px;}
  .v1dfc em{display:inline-block; font-style:normal; font-size:15px; font-weight:700; color:#C76A12; background:#FFF1E2;
    border-radius:10px; padding:5px 9px;}
  .v1dm{display:grid; grid-template-columns:150px repeat(7,1fr); gap:8px; margin-top:22px; align-items:stretch;}
  .v1dmh{font-size:18px; font-weight:800; color:#16233A; text-align:center; padding-bottom:6px; border-bottom:3px solid #16233A;}
  .v1dml{font-size:20px; font-weight:800; color:#16233A; display:flex; flex-direction:column; justify-content:center;}
  .v1dml small{font-size:13px; font-weight:600; color:#6B7785; margin-top:4px;} .v1dml.on{color:#C76A12;}
  .v1dmc{background:#EAF0F7; border-radius:12px; padding:16px 8px; font-size:15.5px; font-weight:600; color:#16233A; text-align:center;
    display:flex; align-items:center; justify-content:center; min-height:84px;}
  .v1dmm{background:#FFF1E2; border:2px solid #F28C28; border-radius:12px; padding:12px 8px; text-align:center; min-height:84px;
    display:flex; flex-direction:column; justify-content:center; opacity:0; animation:v1dfIn .45s var(--d) forwards;}
  .v1dmm small{font-size:14px; font-weight:800; color:#C76A12; margin-bottom:5px;} .v1dmm b{font-size:16px; color:#16233A;}
  @keyframes v1dfIn{from{opacity:0; transform:translateY(10px)} to{opacity:1; transform:none}}
  @media print{.v1dfc,.v1dmm{opacity:1; animation:none}}
  .v1big{font-size:34px; font-weight:800; color:#16233A; line-height:1.35; text-align:center; margin:18px 0 22px; letter-spacing:-.02em;}
  .v1big em{font-style:normal; color:#F28C28;}
  .v1u3im{width:100%; border-radius:14px; border:1.5px solid #D9DDE3; background:#F7EEDB; display:block;}
"""


def plan_build():
    """기획서 구성 — 단톡방 · 메모에 흩어진 재료가 하나씩 켜지며 기획서.md 의 칸을 차례로 채움. 칸 간격 2.2초 · 한 번 재생."""
    rows = [("배경", "현재 방식", "회의록 · 메모가 메모장 · 단톡방 · 워드 파일에 흩어짐", "msg", "「나와의 채팅」에 남긴 회의 메모"),
            ("문제점", "실제 장면", "지난 회의록 위치를 몰라 다시 물어봄", "msg", "「지난주 회의록 어디 있어요?」"),
            ("목표 이용자", "사람 · 기기", "회의가 잦은 직장인 나 · PC 브라우저", "memo", "나 혼자 · 회사 PC"),
            ("서비스 컨셉", "한 문장 + 규칙", "페이지마다 블록으로 쓰는 메모장 · 할 일은 체크 상자", "memo", "노션 같은 블록 메모"),
            ("화면 구성", "3개 이내", "페이지 목록 · 편집 화면 · 「/」 메뉴", "memo", "목록 · 편집 · 「/」"),
            ("하지 않을 것", "이번에 안 만들 것", "공유 · 로그인 · 이미지 · 데이터베이스 표", "memo", "팀 공유도?")]
    left, right = "", ""
    for i, (h, tag, body, kind, raw) in enumerate(rows):
        d = 3.6 + i * 2.2
        left += (f'<div class="v1plS {kind}" style="--d:{.3 + i * .25:.2f}s;--h:{d:.1f}s">'
                 f'<em>{"단톡방" if kind == "msg" else "메모"}</em>{raw}</div>')
        right += (f'<div class="v1plR{" no" if i == 5 else ""}" style="--h:{d + .3:.1f}s"><b>{h}</b><span class="v1plT" style="--d:{d + .5:.1f}s">{body}</span>'
                  f'<i style="--d:{d + .5:.1f}s">{tag}</i></div>')
    return (f'<div class="v1plW"><div class="v1plL"><div class="v1plH">흩어진 재료</div>{left}</div>'
            f'<div class="v1plA" style="--d:2.2s">→</div>'
            f'<div class="v1plD" style="--d:2.2s"><div class="v1plF">기획서.md</div>{right}</div></div>')


def fb_rewrite():
    """피드백 반영 — 흐린 문장 → 흐린 말 강조 → Claude 질문 → 구체 문장으로 바뀜. 두 줄 · 장면 간격 2초."""
    rows = [("문제점", "메모 관리가 <u>불편하다</u>", "실제로 어떤 일이 있었나요?", "지난주 회의록이 어느 파일에 있는지 몰라 다시 물어봤다"),
            ("목표 이용자", "<u>메모하는 모든 사람</u>", "누가 · 어떤 기기로 쓰나요?", "회의가 잦은 직장인 나 · PC 브라우저")]
    out = ('<div class="v1rwR v1rwTop"><span></span><span>흐린 문장</span><span></span><span>Claude 질문</span><span></span><span>고친 문장</span></div>')
    for i, (h, vague, q, done) in enumerate(rows):
        t = .3 + i * 6.4
        out += (f'<div class="v1rwR"><div class="v1rwH" style="--d:{t:.1f}s">{h}</div>'
                f'<div class="v1rwV" style="--d:{t:.1f}s;--u:{t + 1.2:.1f}s;--x:{t + 4.2:.1f}s">「{vague}」</div>'
                f'<i class="v1rwA" style="--d:{t + 2.2:.1f}s">→</i>'
                f'<div class="v1rwQ" style="--d:{t + 2.2:.1f}s">{q}</div>'
                f'<i class="v1rwA" style="--d:{t + 4.2:.1f}s">→</i>'
                f'<div class="v1rwN" style="--d:{t + 4.2:.1f}s">「{done}」</div></div>')
    return f'<div class="v1rwW">{out}</div>'


def slides():
    return [
        # ── 왜 기획하나
        light("모호한 요청과 구체적 요청", shot("v1_u3_salt.webp", "모호한 요청 · 「소금 적당히」", [
            ("모호 · 「소금 적당히」", "사람마다 다른 양"), ("구체 · 「소금 1g」", "누가 해도 같은 맛"),
            ("모호 · 「미니 노션 만들어 줘」", "AI 가 기능 · 화면을 정함"), ("구체 · 기획서", "내가 정한 대로")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("IT 기업의 개발 흐름", _devflow(), T),
        # ── 만들 것
        light("미니 노션 완성 화면", shot("notion_main.webp", "미니 노션 · 완성 화면", [
            ("화면", "왼쪽 페이지 목록 · 오른쪽 편집"), ("블록", "제목 · 글 · 체크 상자 · 구분선"),
            ("「/」 메뉴", "블록 종류 고르기"), ("저장", "새로고침 뒤에도 그대로")]), T),
        light("미니 노션 기능", viz2.tiles([
            ("페이지 목록", "왼쪽 목록 · 새 페이지 · 삭제"), ("블록 편집", "제목 · 글 · 체크 상자 · 구분선"),
            ("「/」 메뉴", "「/」 입력 → 블록 종류 고르기"), ("블록 끌어 옮기기", "손잡이로 순서 바꾸기"),
            ("저장", "새로고침 뒤에도 그대로"), ("더 넣고 싶은 것", "기획서에 적으면 같이 개발")], 3), T),
        # ── 기획서
        light("기획서", shot("v1_u3_plan.webp", "기획서 · 한 장의 문서", [
            ("머릿속 아이디어", "설명할 때마다 내용이 바뀜"), ("기획서", "왜 · 누가 · 무엇을 · 어떤 화면"),
            ("기획서.md", "Claude Code 가 읽는 파일")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("기획서 구성", viz2.maprows([
            ("배경", "왜 만드나", "회의록이 메모장 · 단톡방 · 워드에 흩어짐"),
            ("문제점", "실제로 겪은 불편", "지난주 회의록을 못 찾아 다시 물어봄"),
            ("이용자", "누가 · 어디서", "회의가 잦은 직장인 · PC 브라우저"),
            ("기능", "무엇을 하나", "페이지 · 블록 · 「/」 메뉴 · 끌어 옮기기 · 저장"),
            ("화면", "어떻게 보이나", "왼쪽 페이지 목록 · 오른쪽 블록 편집")], "칸", "묻는 것"), T),
        # ── Claude Code 와 기획하기
        light("Plan Mode", viz2.pair(
            "바로 작성", [("요청", "「기획서 써 줘」"), ("결과", "기획서.md 가 바로 생김"), ("빈 칸", "Claude Code 추측으로 채움")],
            "Plan Mode", [("요청", "Shift+Tab → 요청"), ("결과", "파일은 그대로 · 질문과 초안만"), ("저장", "승인한 뒤에 기획서.md")])
              + src(("Claude Code · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        light("페르소나", viz2.pair(
            "페르소나 없이", [("요청", "「기획서 써 줘」"), ("Claude Code", "그럴듯한 기획서를 한 번에 씀"), ("빈 곳", "배경 · 문제점을 지어냄")],
            "기획자 페르소나", [("요청", "「기획자.md 대로 같이 쓰자」"), ("Claude Code", "기획자처럼 질문을 하나씩"), ("빈 곳", "내 답으로 채움")]), T),
        light("기획자 페르소나", '<div class="twocol"><div>' + code("기획자.md", esc(_persona("기획자")))
              + '</div><div>' + viz2.tiles([("만들기", "mini_notion 폴더에 새 파일 · 다섯 줄"), ("바꿔도 됨", "경력 · 말투"),
                                          ("마지막 줄", "기획서 칸 = 질문 순서")], 1) + "</div></div>", T),
        light("기획자 페르소나 대화 예시", '<div class="twocol"><div>' + chat([
            ("me", "기획자.md 대로 미니 노션 기획서를 같이 쓰자"),
            ("ai", "배경부터 묻는다. 회의록 · 메모는 현재 어디에 쓰나요?"),
            ("me", "메모장 · 단톡방 「나와의 채팅」 · 워드 파일에 흩어져 있어"),
            ("ai", "그 방식에서 실제로 문제가 된 일이 있었나요?"),
            ("me", "지난주 회의록이 어느 파일에 있는지 몰라 다시 물어봤어")], "Plan Mode 대화 예")
              + '</div><div><img class="v1u3im" src="img/v1_u3_ask.webp" alt="질문하는 AI · 답하는 사람"/></div></div>'
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("피드백 반영 전후", fb_rewrite(), T),
        # ── 실습
        labcard("1-3", "기획서 작성", T, "기획자.md", "기획서.md", ["Plan Mode", "질문에 답하기", "피드백"]),
        brief("1-3", T, ["기획자.md 만들기", "Shift+Tab → Plan Mode", "「기획자.md 대로 미니 노션 기획서를 같이 쓰자」", "질문에 답하기 · 초안에 피드백", "승인 → 기획서.md"],
              [("목표", "미니 노션 기획서 · 다섯 칸"), ("입력", "기획자.md · 내 경험"), ("진행 방식", "Plan Mode · 질문에 답하기")],
              ["기획자.md", "Plan Mode", "문제점", "기능"],
              ["다섯 칸이 모두 내 답으로 채워짐", "원하는 기능이 빠짐없이 적힘"],
              "모르는 질문엔 「아직 안 정함」으로 답하기", folder="mini_notion/기획서.md"),
        tstep("1-3", 1, "기획자.md 만들기", T, term=("mini_notion/기획자.md", _persona("기획자")),
              rows=[("만들기", "VS Code 탐색기 → 새 파일 → 기획자.md"), ("쓰기", "다섯 줄 · 경력 · 말투는 바꿔도 됨"), ("저장", "macOS ⌘S · Windows Ctrl+S")]),
        tstep("1-3", 2, "Plan Mode 요청", T, "lab13_plan.webp", "Plan Mode 에서 요청을 쓴 화면",
              rows=[("Plan Mode", "Shift+Tab → plan mode on"), ("요청", "기획자.md 대로 같이 쓰기"), ("파일", "아직 안 씀")]),
        tstep("1-3", 3, "질문에 답하기", T, "lab13_q1.webp", "기획자 페르소나의 첫 질문",
              rows=[("질문", "한 번에 하나"), ("답", "실제 겪은 장면"), ("모를 때", "「아직 안 정함」")]),
        tstep("1-3", 4, "초안에 피드백", T, "lab13_draft.webp", "초안 요약과 흐린 부분 질문",
              rows=[("초안", "칸별 요약"), ("흐린 부분", "다시 묻기 → 내 답으로"), ("피드백", "빠진 기능 · 고칠 문장")]),
        tstep("1-3", 5, "승인 · 저장", T, "lab13_saved.webp", "기획서.md 저장 결과",
              rows=[("승인", "2번 · 수정마다 직접 승인"), ("저장", "Do you want to create → 1. Yes"), ("결과", "mini_notion/기획서.md")]),
        light("실습 1-3 확인", checks([
            ("문제점이 실제 장면인가", "「불편하다」만 있으면 다시"), ("이용자가 실제 사람인가", "「모두」면 다시"),
            ("원하는 기능이 다 있나", "「/」 메뉴 · 끌어 옮기기 등"), ("내가 말하지 않은 내용이 없나", "있으면 지우기")],
            "넷 다 「예」 → 기획서.md 저장"), T),
    ]
