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


def _screen():
    """화면 나누기 — 기획서 한 줄(「왼쪽 목록 · 오른쪽 편집」)이 실제 화면 칸으로 나뉨. 칸마다 점선 → 이름표(F 번호)가 차례로 붙음."""
    regs = [("aside", "페이지 목록", "F1", 1.2), ("bar", "안내 줄 · 페이지 삭제", "", 2.2), ("title", "큰 제목", "", 3.0),
            ("blocks", "블록 줄", "F2", 3.8), ("handle", "⋮⋮ 손잡이", "F4", 4.8), ("menu", "「/」 메뉴", "F3", 5.8)]
    inner = {"aside": '<span class="ln w7"></span><span class="ln on"></span><span class="ln"></span><span class="nw">+ 새 페이지</span>',
             "bar": '<span class="nw">「/」 를 입력하면 블록 종류를 고를 수 있다</span><span class="del">페이지 삭제</span>',
             "title": '<span class="big">주간 회의</span>',
             "blocks": '<span class="rw"><i></i><b class="ln w8"></b></span><span class="rw"><i></i><b class="cb"></b><b class="ln w6"></b></span>'
                       '<span class="rw"><i></i><b class="ln w7"></b></span><span class="rw"><i></i><b class="ln w4"></b></span>',
             "handle": "", "menu": '<span>제목</span><span>글</span><span class="on">체크 상자</span><span>구분선</span>'}
    r = "".join(f'<div class="v14w-{k}" style="--d:{d:.1f}s"><div class="in">{inner[k]}</div>'
                f'<em style="--d:{d + .3:.1f}s">{(f + " · ") if f else ""}{n}</em></div>' for k, n, f, d in regs)
    left = "".join(f'<li style="--d:{d + .3:.1f}s"><b>{f or "—"}</b>{n}</li>' for _, n, f, d in regs)
    return ('<div class="v14sc"><div class="v14scL">'
            '<div class="v14scQ"><small>기획서 · 화면 칸</small>왼쪽 페이지 목록 · 오른쪽 블록 편집</div><div class="v14scA">↓</div>'
            f'<div class="v14scP"><small>개발계획 · 2. 화면</small><ul>{left}'
            '<li style="--d:7.0s"><b>F5</b>저장 · 화면 밖 · 브라우저 안</li></ul></div></div>'
            f'<div class="v14w" style="--d:.3s"><div class="v14wTop"><i></i><i></i><i></i><span>미니 노션</span></div><div class="v14wB">{r}</div>'
            '<div class="v14wSave" style="--d:7.0s">F5 · 저장 → 브라우저 안 (화면에 안 보임)</div></div></div>')


def _thread():
    """기능 하나 따라가기 — 「/」 메뉴 하나가 개발계획.md 다섯 칸에 어떻게 적히는지 쉬운 말로 한 줄씩. 왼쪽 세로선을 점이 내려감."""
    rows = [("1. 기능", "무엇을 하나", "F3 · 빈 줄에 / 를 치면 블록 종류 메뉴가 뜸"),
            ("2. 화면", "어디에 보이나", "편집 화면 위 안내 「/ 를 입력하면 블록 종류를 고를 수 있다」"),
            ("3. 데이터", "무엇을 기억하나", "줄마다 블록 종류 · 제목 · 글 · 체크 상자 · 구분선 중 하나"),
            ("4. 완료 기준", "어떻게 확인하나", "빈 줄에 / → 「체크 상자」 선택 → 그 줄이 체크 상자로 바뀌면 통과"),
            ("5. 태스크", "언제 만드나", "세 번째 작업 T3 · 끝나면 / 메뉴가 뜨는 화면")]
    r = "".join(f'<div class="v14tR" style="--d:{.4 + i * 1.2:.1f}s"><b>{h}<small>{q}</small></b><span>{x}</span></div>' for i, (h, q, x) in enumerate(rows))
    return ('<div class="v14tW"><div class="v14t"><div class="v14tTag">「/」 메뉴 하나 따라가기</div><div class="v14tL"><i class="v14tDot"></i>' + r + '</div></div>'
            '<figure class="v14tF"><img src="img/notion_slash_menu.webp" alt="빈 줄에 / 를 친 화면"/><figcaption>빈 줄에 / → 블록 종류 메뉴</figcaption></figure></div>')


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
  /* 1-4 · 화면 나누기 (v14sc · v14w) */
  .v14sc{display:grid; grid-template-columns:300px 1fr; gap:24px; margin-top:10px; align-items:start;}
  .v14scQ,.v14scP{background:#F4F6F9; border:2px solid #C9D6E6; border-radius:12px; padding:12px 14px; font-size:17px; font-weight:700; color:#16233A;}
  .v14scQ small,.v14scP small{display:block; font-size:13px; color:#6B7785; margin-bottom:4px;}
  .v14scA{text-align:center; font-size:22px; font-weight:800; color:#F28C28; margin:4px 0;}
  .v14scP{background:#FFF8F0; border-color:#F2B880;}
  .v14scP ul{list-style:none; margin:4px 0 0; padding:0;}
  .v14scP li{display:flex; gap:10px; font-size:15.5px; padding:4px 0; opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14scP li b{min-width:28px; color:#C76A12;}
  .v14w{position:relative; border:2px solid #C9D6E6; border-radius:12px; background:#fff; overflow:visible; opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14wTop{display:flex; gap:6px; align-items:center; padding:8px 12px; border-bottom:1.5px solid #E3E6EA; font-size:13px; color:#6B7785;}
  .v14wTop i{width:9px; height:9px; border-radius:50%; background:#D9DDE3;} .v14wTop span{margin-left:8px;}
  .v14wB{position:relative; height:340px;}
  .v14wB > div{position:absolute; border-radius:8px; opacity:0; animation:v14Rg .5s var(--d) forwards;}
  .v14wB > div .in{position:absolute; inset:0; padding:10px 12px; display:flex; flex-direction:column; gap:9px;}
  .v14wB em{position:absolute; font-style:normal; white-space:nowrap; background:#F28C28; color:#fff; font-size:13.5px; font-weight:800; border-radius:6px; padding:2px 8px;
    opacity:0; animation:v14In .3s var(--d) forwards; z-index:3;}
  .v14w-aside{left:0; top:0; width:26%; height:100%; background:#F7F7F5; border-right:1.5px solid #EBEBEA;} .v14w-aside em{left:10px; bottom:10px;}
  .v14w-bar{left:30%; top:4%; width:66%; height:10%;} .v14wB .v14w-bar .in{flex-direction:row; justify-content:space-between; align-items:center; padding:0 10px;} .v14w-bar em{right:-6px; top:-12px;}
  .v14w-title{left:30%; top:17%; width:46%; height:13%;} .v14w-title em{right:-60px; top:10px;}
  .v14w-blocks{left:30%; top:34%; width:66%; height:58%;} .v14w-blocks em{right:-6px; bottom:-12px;}
  .v14w-handle{left:30%; top:34%; width:5%; height:58%;} .v14w-handle em{left:-46px; top:-14px;}
  .v14w-menu{left:44%; top:52%; width:24%; height:40%; background:#fff; box-shadow:0 6px 16px rgba(0,0,0,.14); z-index:2;}
  .v14w-menu .in{gap:2px; padding:6px;} .v14w-menu .in span{font-size:13px; padding:3px 6px; border-radius:4px; color:#37352F;} .v14w-menu .in span.on{background:#ECEBE8; font-weight:700;}
  .v14w-menu em{right:-40px; top:-12px;}
  .v14wB .ln{display:block; height:9px; width:90%; border-radius:4px; background:#E3E2DE;} .v14wB .ln.on{background:#D3D1CB;}
  .v14wB .w4{width:40%} .v14wB .w5{width:50%} .v14wB .w6{width:60%} .v14wB .w7{width:70%} .v14wB .w8{width:80%}
  .v14wB .nw{font-size:12px; color:#9B9A97;} .v14wB .del{font-size:12px; color:#C0392B;}
  .v14wB .big{font-size:24px; font-weight:800; color:#37352F;}
  .v14wB .rw{display:flex; align-items:center; gap:8px; height:24px;} .v14wB .rw i{width:8px; height:14px; border-left:3px dotted #C4C4C2; border-right:3px dotted #C4C4C2;}
  .v14wB .rw b{display:block;} .v14wB .cb{width:13px; height:13px; border:1.8px solid #37352F; border-radius:3px; flex:none;}
  .v14wSave{position:absolute; right:12px; bottom:-46px; background:#16233A; color:#fff; font-size:14px; font-weight:800; border-radius:8px; padding:6px 12px; opacity:0; animation:v14In .4s var(--d) forwards;}
  @keyframes v14Rg{0%{opacity:0; outline:2.5px dashed #F28C28; outline-offset:4px} 60%{opacity:1; outline:2.5px dashed #F28C28; outline-offset:0} 100%{opacity:1; outline:2px dashed #F2B880; outline-offset:0}}
  /* 1-4 · 기능 하나 따라가기 (v14t) */
  .v14t{margin-top:14px;}
  .v14tTag{display:inline-block; background:#16233A; color:#fff; font-size:19px; font-weight:800; border-radius:10px; padding:8px 16px; opacity:0; animation:v14In .4s .1s forwards;}
  .v14tL{position:relative; margin:14px 0 0 18px; padding-left:30px; border-left:3px solid #C9D6E6;}
  .v14tDot{position:absolute; left:-10px; top:0; width:17px; height:17px; border-radius:50%; background:#F28C28; animation:v14Dn 6s .4s forwards;}
  .v14tR{display:grid; grid-template-columns:140px 1fr; gap:16px; align-items:center; background:#fff; border:2px solid #C9D6E6; border-radius:12px;
    padding:12px 16px; margin-bottom:11px; opacity:0; transform:translateX(-12px); animation:v14In .5s var(--d) forwards;}
  .v14tR b{font-size:19px; color:#C76A12; display:flex; flex-direction:column;} .v14tR b small{font-size:13px; color:#6B7785; font-weight:700;}
  .v14tR span{font-size:16.5px; color:#16233A; font-weight:600;}
  .v14tW{display:grid; grid-template-columns:1fr 250px; gap:20px; align-items:start;}
  .v14tF{margin:50px 0 0; text-align:center;} .v14tF img{width:100%; border-radius:12px; border:1.5px solid #D9DDE3;}
  .v14tF figcaption{font-size:14px; color:#6B7785; margin-top:6px;}
  .v14b{display:grid; grid-template-columns:540px 1fr; gap:28px; align-items:center; margin-top:18px;}
  .v14b img{width:100%; height:auto; border-radius:14px; border:1.5px solid #D9DDE3;}
  @keyframes v14In{to{opacity:1; transform:none;}}
  @keyframes v14Hi{to{background:#FDECEA; color:#C0392B; box-shadow:0 0 0 2px #E6B0AA;}}
  @keyframes v14Dn{to{top:calc(100% - 20px);}}
  @media print{.v14gL,.v14gQ,.v14gR i,.v14gA,.v14gN,.v14tTag,.v14tR{opacity:1; animation:none; transform:none}}
"""


def slides():
    return [
        # ── 배경 → 비유 → 애니메이션
        light("기획서만 넘긴 결과", _gaps(), T),
        light("조감도와 설계 도면", '<div class="v14b"><img src="img/v1_u4_blueprint.webp" alt="조감도와 설계 도면"/>' + viz2.maprows([
                  ("조감도", "기획서", "어떤 집인지 · 왜"), ("설계 도면", "개발 계획", "기능 · 화면 · 데이터"),
                  ("공정표", "태스크", "무엇부터 짓나"), ("준공 검사", "완료 기준", "도면대로 지었나")], "집 짓기", "앱 만들기") + "</div>"
              + src(GEN), T),
        # ── 개발 계획
        light("화면 나누기", _screen(), T),
        light("기능 하나 따라가기", _thread(), T),
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
