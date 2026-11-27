"""1-4 개발 계획.

기획서만 넘긴 결과 → 비유(조감도 · 설계 도면) → 개발 리더 페르소나 → 대화 예시 → 화면 나누기 → 쉬운 말 요약 → 검토 질문 셋 → 실습.
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
    """기획서만 넘긴 결과 — 기획서는 내 말(장면 · 확인 문장) · 개발자가 정할 것(저장 위치 · 순서 · 기술)이 빈칸 → AI 추측. 한 번 재생."""
    rows = [("어디에 저장?", "서버를 새로 만듦"), ("무엇부터 만들지?", "AI 가 정한 순서"),
            ("어떤 기술 · 파일로?", "대화마다 다름"), ("한 번에 다?", "전부 한꺼번에 · 오류 위치 모름")]
    line = ('기능 · 페이지 목록 · 블록 · 「/」 메뉴 · <u style="--d:1.0s">저장</u><br/>'
            '확인 문장 · 새로고침해도 <u style="--d:1.6s">그대로 있다</u>')
    r = "".join(f'<div class="v14gR"><div class="v14gQ" style="--d:{1.2 + i * 1.6:.1f}s">{q}</div><i style="--d:{1.8 + i * 1.6:.1f}s">→</i>'
                f'<div class="v14gA" style="--d:{1.8 + i * 1.6:.1f}s">{g}</div></div>' for i, (q, g) in enumerate(rows))
    return (f'<div class="v14g"><div class="v14gL"><div class="v14gH">기획서.md · 내 말로 쓴 것</div><div class="v14gT">{line}</div>'
            '<div class="v14gC">있음 · 무엇을 · 왜 · 어떻게 확인<br/><b style="color:#C0392B">없음 · 어떻게 만들지</b></div></div>'
            f'<div class="v14gW"><div class="v14gHd"><span>개발자가 정할 것</span><span></span><span>AI 추측 · 예</span></div>{r}</div></div>'
            '<div class="v14gN" style="--d:8.2s"><b>개발 계획</b>이 빈칸을 채우는 문서 · 쓰는 건 AI 개발자 · 나는 읽고 확인</div>')


def _easy():
    """쉬운 말 요약 — 개발계획.md 원문(어려운 말)이 흐려지고 → 요청 한 줄 → 요약 여섯 줄이 차례로. 요약은 예시 파일에서 읽음."""
    raw = [_line("1", "F3"), "저장: 브라우저 localStorage", _line("5", "T4")]
    t = _prd()
    summ = [x.strip() for x in t[t.index("## 쉬운 말 요약"):].split("\n") if x.strip()[:2] in {f"{n}." for n in range(1, 10)}]
    left = "".join(f'<div class="v14eR">{esc(x)}</div>' for x in raw)
    right = "".join(f'<div class="v14eS" style="--d:{3.0 + i * .6:.1f}s">{esc(x)}</div>' for i, x in enumerate(summ))
    return ('<div class="v14e"><div class="v14eL" style="--d:.2s"><div class="v14eH">개발계획.md · 원문 일부</div>' + left + '</div>'
            '<div class="v14eM" style="--d:1.6s">개발 리더가<br/>계획 끝에 붙임<i>→</i></div>'
            f'<div class="v14eRt"><div class="v14eH">쉬운 말 요약 · 화면이 바뀌는 순서</div>{right}</div></div>')


def _review():
    """개발 계획 검토 — 질문 세 개가 차례로 · 질문마다 예시 확인 결과."""
    qs = [("내가 고른 기능이 다 들어 있나", "「끌어 옮기기」 → 4번 단계에 있음"),
          ("모르는 단어가 있나", "「localStorage 가 뭐야?」 → 이 브라우저 안의 저장 공간"),
          ("단계마다 화면에서 무엇을 보면 되나", "3번 끝 → 빈 줄에 / → 메뉴가 뜸")]
    r = "".join(f'<div class="v14vQ" style="--d:{.4 + i * 1.6:.1f}s"><i>{i + 1}</i><b>{q}</b><span style="--d:{1.1 + i * 1.6:.1f}s">예 · {a}</span></div>'
                for i, (q, a) in enumerate(qs))
    return (f'<div class="v14v">{r}</div><div class="v14gN" style="--d:5.4s"><b>하나라도 「아니요」</b>그 부분만 다시 요청 · 「요약 3번을 더 쉽게」</div>')


def _tone():
    """개발자 말투 → 개발 리더 말투 — 같은 질문 · 보고가 쉬운 말로 바뀜. 줄마다 왼쪽(전문 용어) 흐려지고 오른쪽 등장."""
    rows = [("질문", "상태는 localStorage 로 persist 할까요, 백엔드 DB 로 할까요?",
             "쓴 내용을 어디에 보관할까요? A 이 브라우저 안 · 추천 · 로그인 없음 · 다른 기기에선 안 보임 / B 인터넷 서버 · 어디서나 보임 · 로그인 필요"),
            ("보고", "T3 구현 중 contenteditable 의 input 이벤트와 충돌 발생",
             "「/」 메뉴를 만들다가 글자 입력과 부딪히는 곳을 찾았어요 · 메뉴가 떠 있는 동안 글자 입력을 잠깐 멈추게 할게요"),
            ("피드백", "DnD 핸들의 hit area 가 작음",
             "손잡이가 작아서 잡기 어려워요 · 마우스가 줄에 올라가면 손잡이가 보이게 하고 잡는 범위를 넓힐게요")]
    r = ""
    for i, (k, dev, lead) in enumerate(rows):
        d = .4 + i * 2.2
        r += (f'<div class="v14oR"><b style="--d:{d:.1f}s">{k}</b><div class="v14oD" style="--d:{d:.1f}s;--x:{d + 1.0:.1f}s">{esc(dev)}</div>'
              f'<i style="--d:{d + 1.0:.1f}s">→</i><div class="v14oL" style="--d:{d + 1.2:.1f}s">{esc(lead)}</div></div>')
    return (f'<div class="v14o"><div class="v14oH"><span></span><span>개발자 말투</span><span></span><span>개발 리더 말투 · 개발리더.md</span></div>{r}</div>'
            '<div class="v14gN" style="--d:7.2s"><b>같은 내용</b>「기획자도 알아듣게」 한 줄이면 처음부터 쉬운 말로</div>')


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
            '<div class="v14scQ"><small>기획서 · 화면</small>왼쪽 페이지 목록 · 오른쪽 큰 제목 → 블록 · 빈 줄에 / → 메뉴</div><div class="v14scA">↓</div>'
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
  .v14gT{font-size:18px; font-weight:700; color:#16233A; line-height:1.6; word-break:keep-all;}
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
  /* 1-4 · 개발자 말투 → 개발 리더 말투 (v14o) */
  .v14oH,.v14oR{display:grid; grid-template-columns:70px 1fr 30px 1.35fr; gap:12px; align-items:center;}
  .v14oH{margin-top:14px;} .v14oH span{font-size:14px; font-weight:800; color:#6B7785; padding-bottom:6px; border-bottom:2px solid #E3E6EA;}
  .v14oH span:last-child{color:#C76A12; border-color:#F28C28;}
  .v14oR{margin-top:14px;}
  .v14oR b{font-size:17px; color:#16233A; opacity:0; animation:v14In .3s var(--d) forwards;}
  .v14oD{font-family:var(--mono); font-size:14px; color:#E3E6EA; background:#1E2433; border-radius:10px; padding:12px 14px; line-height:1.5; opacity:0;
    animation:v14In .3s var(--d) forwards, v14Fade .6s var(--x) forwards;}
  .v14oR i{font-style:normal; font-weight:800; color:#F28C28; font-size:20px; text-align:center; opacity:0; animation:v14In .3s var(--d) forwards;}
  .v14oL{background:#FFF8F0; border:2px solid #F2B880; border-radius:10px; padding:12px 14px; font-size:16.5px; font-weight:700; color:#16233A; line-height:1.5;
    opacity:0; transform:translateX(-10px); animation:v14In .45s var(--d) forwards;}
  @keyframes v14Fade{to{opacity:.45}}
  /* 1-4 · 쉬운 말 요약 · 검토 (v14e · v14v) */
  .v14e{display:grid; grid-template-columns:330px 170px 1fr; gap:16px; margin-top:16px; align-items:center;}
  .v14eH{font-size:14px; font-weight:800; color:#6B7785; margin-bottom:8px;}
  .v14eL{background:#1E2433; border-radius:12px; padding:14px; opacity:0; animation:v14Blur 2.4s var(--d) forwards;}
  .v14eL .v14eH{color:#9AA6B4;}
  .v14eR{font-family:var(--mono); font-size:13px; color:#E3E6EA; line-height:1.55; padding:6px 0; border-top:1px solid #333B4D;}
  .v14eM{background:#16233A; color:#fff; border-radius:14px 14px 4px 14px; padding:14px; font-size:16px; font-weight:800; line-height:1.5; text-align:center; position:relative;
    opacity:0; animation:v14In .4s var(--d) forwards;}
  .v14eM i{position:absolute; right:-18px; top:50%; transform:translateY(-50%); font-style:normal; color:#F28C28; font-size:22px;}
  .v14eS{background:#FFF8F0; border:2px solid #F2B880; border-radius:10px; padding:9px 12px; margin-bottom:7px; font-size:16.5px; font-weight:700; color:#16233A;
    opacity:0; transform:translateX(-10px); animation:v14In .45s var(--d) forwards;}
  .v14v{margin-top:18px;}
  .v14vQ{display:grid; grid-template-columns:40px 360px 1fr; gap:14px; align-items:center; background:#fff; border:2px solid #C9D6E6; border-radius:12px; padding:14px 16px; margin-bottom:12px;
    opacity:0; transform:translateX(-10px); animation:v14In .45s var(--d) forwards;}
  .v14vQ i{font-style:normal; width:32px; height:32px; border-radius:50%; background:#16233A; color:#fff; display:inline-flex; align-items:center; justify-content:center; font-weight:800;}
  .v14vQ b{font-size:20px; color:#16233A;}
  .v14vQ span{font-size:17px; font-weight:700; color:#9A4F0C; background:#FFF1E2; border-radius:8px; padding:8px 12px; opacity:0; animation:v14In .4s var(--d) forwards;}
  @keyframes v14Blur{0%{opacity:0} 20%{opacity:1; filter:none} 100%{opacity:.55; filter:blur(.6px)}}
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
  @media print{.v14oR b,.v14oD,.v14oR i,.v14oL,.v14eL,.v14eM,.v14eS,.v14vQ,.v14vQ span,.v14gL,.v14gQ,.v14gR i,.v14gA,.v14gN,.v14tTag,.v14tR{opacity:1; animation:none; transform:none}}
"""


def slides():
    return [
        # ── 배경 → 비유 → 애니메이션
        light("기획서만 넘긴 결과", _gaps(), T),
        light("조감도와 설계 도면", '<div class="v14b"><img src="img/v1_u4_blueprint.webp" alt="조감도와 설계 도면"/>' + viz2.maprows([
                  ("조감도", "기획서", "내가 씀 · 어떤 집 · 왜"), ("설계 도면", "개발 계획", "AI 개발자가 씀"),
                  ("도면 설명", "쉬운 말 요약", "내가 읽고 확인"), ("준공 검사", "완료 기준", "기획서 확인 문장 그대로")], "집 짓기", "앱 만들기") + "</div>"
              + src(GEN), T),
        # ── 개발 계획
        # ── 개발 리더 페르소나
        light("개발 리더 페르소나", '<div class="twocol"><div>' + code("개발리더.md", esc(_persona("개발리더")))
              + '</div><div>' + viz2.tiles([("첫 줄", "개발을 몰라도 알아듣는 질문 · 계획"), ("둘째 줄", "전문 용어는 바로 뜻 풀이"),
                                          ("셋째 줄", "선택지 · 추천 · 이유로 질문"), ("마지막 줄", "칸 끝에 쉬운 말 요약")], 1) + "</div></div>", T),
        light("개발 계획 대화 예시", chat([
            ("me", "개발리더.md 대로 기획서.md 를 읽고 개발 계획을 세워 줘"),
            ("ai", "기획서에 없는 것 하나를 먼저 묻는다. 쓴 내용을 어디에 보관할까요?\nA 이 브라우저 안 · 추천 · 로그인 없음 · 다른 기기에서는 안 보임\nB 인터넷 서버 · 어디서나 보임 · 로그인 필요"),
            ("me", "A"),
            ("ai", "A 로 정했다. 계획은 여섯 단계 · 단계마다 끝나면 화면에서 볼 것을 적었다.\n맨 끝 「쉬운 말 요약」부터 읽어 보면 된다.")], "Plan Mode 대화 예"), T),
        light("화면 나누기", _screen(), T),
        light("쉬운 말 요약", _easy(), T),
        light("개발 계획 검토", _review(), T),
        # ── 실습
        labcard("1-4", "기획서로 개발 계획 세우기", T, "기획서.md", "개발계획.md", ["개발 리더 페르소나", "선택지 고르기", "검토 질문 셋"]),
        brief("1-4", T, ["개발리더.md 만들기", "Plan · 「개발리더.md 대로 기획서.md 를 읽고 개발 계획 세워 줘」",
                         "선택지 고르기 · 모르면 「쉽게 다시 설명해 줘」", "쉬운 말 요약 → 검토 질문 셋 → 피드백 · 승인"],
              [],
              ["개발 리더 페르소나", "선택지", "검토"],
              ["질문 · 설명이 다 알아들을 수 있는 말", "개발계획.md 끝에 쉬운 말 요약"],
              "어려운 말이 나오면 바로 「○○ 가 뭐야?」 · 길면 「태스크를 여섯 개 안으로 줄여 줘」"),
        tstep("1-4", 1, "개발리더.md 만들기", T, term=("mini_notion_v2/개발리더.md", _persona("개발리더")),
              rows=[("만들기", "VS Code 탐색기 → 새 파일 → 개발리더.md"), ("쓰기", "여섯 줄 · 첫 두 줄은 꼭"), ("저장", "macOS ⌘S · Windows Ctrl+S")]),
        tstep("1-4", 2, "Plan Mode 요청 · 선택지", T, ask=("Claude Code 입력창 · Plan 모드", "개발리더.md 대로 기획서.md 를 읽고 개발 계획 세워 줘"),
              rows=[("질문", "저장 방식 · 기술 · 기획서에 없던 것"), ("고르기", "추천 · 이유 읽고 고르기"), ("모를 때", "「A 와 B 차이를 쉽게 설명해 줘」")]),
        tstep("1-4", 3, "쉬운 말 요약 검토", T, term=("쉬운 말 요약 · 예", _prd()[_prd().index("## 쉬운 말 요약"):]),
              rows=[("요약", "계획 끝에 자동 첨부"), ("볼 것", "고른 기능이 다 있나"), ("단어", "모르면 바로 질문")]),
        tstep("1-4", 4, "계획에 피드백", T, ask=("승인 대신 고칠 점 입력 · 예", "기획서의 끌어 옮기기가 빠졌어 · 넣어 줘\n태스크 이름을 더 쉬운 말로 바꿔 줘"),
              rows=[("고칠 때", "승인 대신 고칠 점 입력"), ("피드백", "빠진 기능 · 순서 · 이름"), ("다시", "고친 계획 → 승인")]),
        light("실습 1-4 확인", checks([
            ("내가 고른 기능이 다 들어 있나", "기획서 기능 칸 다섯 가지"), ("질문 · 설명을 다 알아들었나", "모르면 물어보고 이해함"),
            ("단계마다 볼 화면이 적혀 있나", "쉬운 말 요약 1~6"), ("저장 위치를 내가 골랐나", "예 · 이 브라우저")],
            "「아니요」 → 그 부분만 다시 요청 · 넷 다 「예」 → 1-5"), T),
    ]
