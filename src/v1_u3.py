"""1-3 기획서 작성.

왜 기획하나(모호 vs 구체 · 개발 흐름) → 만들 것(미니 노션) → 기획서 인터뷰(애니메이션) → 좋은 답 네 가지(애니메이션) → 먼저 묻기 모드 · 역할 메모 → 기획자.md · 말투 비교 → 대화 → 빈칸 찾기 → 실습.
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
    ("개발 계획", "개발 리드", "태스크 · 일정", "1-4", "개발 리더 페르소나 · 태스크 T1~T6"),
    ("개발", "개발자", "코드 · 커밋", "1-5 · 1-6", "Claude Code · Git"),
    ("테스트", "QA", "버그 목록", "1-6", "완료 기준 확인"),
    ("배포 · 회고", "개발 · 운영", "서비스 주소", "1-7 · 1-8", "배포 주소 · 회고"),
]


# IT 기업 조직 — (팀, 역할, 하는 일, 산출물)
ORG = [
    ("기획", "PM · 기획자", "무엇을 · 왜 만들지", "기획서 · PRD"),
    ("디자인", "UI · UX 디자이너", "화면 · 사용 흐름", "화면 설계"),
    ("개발", "개발 리드 · 프론트엔드 · 백엔드", "코드 작성", "코드 · 커밋"),
    ("QA", "테스터", "버그 찾기", "버그 목록"),
    ("운영", "DevOps · 인프라", "배포 · 서버 관리", "서비스 주소"),
]


def _org():
    top = '<div class="v1orgT"><b>서비스 팀</b><span>앱 하나를 만드는 사람들</span></div><div class="v1orgL"></div>'
    c = "".join(f'<div class="v1orgC" style="--d:{.5 + i * .35:.2f}s"><b>{t}</b><span>{r}</span><i>{w}</i><em>{o}</em></div>'
                for i, (t, r, w, o) in enumerate(ORG))
    me = ('<div class="v1orgM" style="--d:2.6s"><b>1부</b><span>다섯 팀의 일을 나 혼자 · Claude Code 와 함께</span></div>')
    return f'<div class="v1org">{top}<div class="v1orgR">{c}</div>{me}</div>'


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
  /* 1-3 · 기획서 인터뷰 (v13i) */
  .v13iH,.v13iR{display:grid; grid-template-columns:1.15fr 1fr 26px 150px; gap:10px; align-items:center;}
  .v13iH{margin-top:10px;} .v13iH span{font-size:14px; font-weight:800; color:#6B7785; padding-bottom:6px; border-bottom:2px solid #E3E6EA;}
  .v13iH span:last-child{color:#C76A12; border-color:#F28C28;}
  .v13iR{margin-top:9px;}
  .v13iR .q{background:#16233A; color:#fff; border-radius:12px 12px 12px 4px; padding:9px 12px; font-size:15.5px; font-weight:700; opacity:0; animation:v13On .35s var(--d) forwards;}
  .v13iR .a{background:#FFF8F0; border:2px solid #F2B880; border-radius:12px 12px 4px 12px; padding:8px 12px; font-size:15.5px; font-weight:700; color:#16233A; opacity:0; animation:v13On .35s var(--d) forwards;}
  .v13iR i{font-style:normal; font-weight:800; color:#F28C28; text-align:center; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13iR .k{background:#fff; border:2px solid #C9D6E6; border-left:6px solid #F28C28; border-radius:8px; padding:8px 12px; font-size:16px; font-weight:800; color:#16233A; opacity:0; animation:v13In .4s var(--d) forwards; transform:translateX(-8px);}
  @media print{.v13iR .q,.v13iR .a,.v13iR i,.v13iR .k{opacity:1; animation:none; transform:none}}
  /* 1-3 · 기획 구체화 방법 (v13m · v13k · v13g) */
  .v13m{display:grid; grid-template-columns:250px 1fr; gap:26px; margin-top:12px; align-items:start;}
  .v13mV{border:2px solid #E6B0AA; background:#FDECEA; border-radius:12px; padding:14px; opacity:0; animation:v13On .4s var(--d) forwards;}
  .v13mV small{display:block; font-size:13px; font-weight:800; color:#C0392B; margin-bottom:4px;}
  .v13mV b{font-size:21px; color:#16233A; background:linear-gradient(#C0392B,#C0392B) no-repeat 0 55%/0 2.5px; animation:v13Strike .5s var(--x) forwards;}
  .v13mA{margin-top:12px; font-size:16px; font-weight:800; color:#F28C28; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13mT{font-size:15px; font-weight:800; color:#6B7785; margin-bottom:8px;}
  .v13mS{display:grid; grid-template-columns:130px 1fr; gap:12px; align-items:center; background:#fff; border:2px solid #C9D6E6; border-radius:10px; padding:10px 14px; margin-bottom:8px;
    opacity:0; transform:translateX(-10px); animation:v13In .45s var(--d) forwards;}
  .v13mS i{font-style:normal; font-weight:800; color:#fff; background:#16233A; border-radius:6px; padding:3px 8px; text-align:center; font-size:15px;}
  .v13mS span{font-size:18px; font-weight:700; color:#16233A;}
  .v13mC{margin-top:12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13mC b{font-size:15px; color:#C76A12; margin-right:4px;} .v13mC.wide{margin-top:18px;}
  .v13mC span{font-size:15px; font-weight:700; color:#16233A; background:#FFF1E2; border:1.5px solid #F2B880; border-radius:8px; padding:4px 10px; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13mP{background:#FFFDF6; border:1.5px solid #E8E2CF; border-radius:10px; padding:10px 14px;}
  .v13mD{display:flex; justify-content:space-between; align-items:center; min-height:34px; border-bottom:1px dashed #E8E2CF; opacity:0; animation:v13On .35s var(--d) forwards;}
  .v13mD span{font-size:17px; color:#37352F; flex:1;} .v13mD.h span{font-size:20px; font-weight:800;} .v13mD.hr hr{border:none; border-top:2px solid #C9C7C1; margin:0; width:60%;}
  .v13mD em{font-style:normal; font-size:13px; font-weight:800; color:#C76A12; background:#FFF1E2; border-radius:6px; padding:2px 8px; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13mK{display:grid; grid-template-columns:330px 120px 1fr; gap:14px; align-items:center;}
  .v13k{position:relative; height:250px; background:#FFFDF6; border:1.5px solid #E8E2CF; border-radius:10px;}
  .v13k > div{position:absolute; border:2.5px solid #4A4A4A; border-radius:6px 10px 5px 9px; opacity:0; animation:v13Draw .6s var(--d) forwards;}
  .v13k span{position:absolute; left:8px; top:6px; font-size:15px; font-weight:700; color:#4A4A4A; font-style:italic;}
  .v13kA{left:12px; top:12px; width:88px; height:224px; transform:rotate(-.6deg);} .v13kA span{top:auto; bottom:44px;}
  .v13kT{left:112px; top:14px; width:150px; height:38px; transform:rotate(.5deg);}
  .v13kB{left:112px; top:62px; width:200px; height:174px; transform:rotate(-.4deg);}
  .v13kM{left:150px; top:130px; width:110px; height:80px; transform:rotate(1deg); background:#FFFDF6;}
  .v13kN{left:18px; top:204px; width:76px; height:24px; border-style:dashed !important;} .v13kN span{top:1px; left:4px; font-size:12px;}
  .v13kAr{font-size:17px; font-weight:800; color:#F28C28; text-align:center; opacity:0; animation:v13On .4s var(--d) forwards;}
  .v13kAr small{display:block; font-size:12.5px; color:#6B7785; font-weight:700; margin-top:4px;}
  .v13kF{margin:0; opacity:0; animation:v13On .5s var(--d) forwards;} .v13kF img{width:100%; border-radius:10px; border:1.5px solid #D9DDE3;}
  .v13kF figcaption{font-size:13px; color:#6B7785; text-align:center; margin-top:4px;}
  .v13mQs{margin-top:16px;}
  .v13mQh,.v13mQ{display:grid; grid-template-columns:230px 34px 1fr 1fr; gap:10px; align-items:center;}
  .v13mQh span{font-size:14px; font-weight:800; color:#6B7785; padding-bottom:6px; border-bottom:2px solid #E3E6EA;}
  .v13mQh span.if{color:#2383E2; border-color:#2383E2;} .v13mQh span.then{color:#C76A12; border-color:#F28C28;}
  .v13mQ{margin-top:12px;}
  .v13mQ s{text-decoration:none; font-size:18px; font-weight:700; color:#16233A; background:#FDECEA linear-gradient(#C0392B,#C0392B) no-repeat 8px 55%/0 2.5px; border:2px solid #E6B0AA;
    border-radius:10px; padding:10px 12px; opacity:0; animation:v13On .3s var(--d) forwards, v13Strike2 .5s var(--x) forwards;}
  .v13mQ i{font-style:normal; font-weight:800; color:#F28C28; font-size:20px; text-align:center; opacity:0; animation:v13On .3s var(--d) forwards;}
  .v13mQ b{font-size:17px; border-radius:10px; padding:10px 12px; opacity:0; animation:v13In .4s var(--d) forwards; transform:translateX(-8px);}
  .v13mQ b.if{background:#EAF3FD; border:2px solid #9CC3EE; color:#1B5FA8;} .v13mQ b.then{background:#FFF1E2; border:2px solid #F2B880; color:#9A4F0C;}
  .v13g{display:grid; grid-template-columns:300px 1fr; gap:26px; margin-top:16px; align-items:start;}
  .v13gMe{background:#16233A; color:#fff; border-radius:14px 14px 4px 14px; padding:16px 18px; font-size:19px; font-weight:700; line-height:1.5; opacity:0; animation:v13On .4s var(--d) forwards;}
  .v13gMe u{text-decoration:none; color:#F7B267;}
  .v13gN{margin-top:18px; background:#FFF1E2; border:2px dashed #F28C28; border-radius:12px; padding:12px 14px; font-size:16px; font-weight:800; color:#9A4F0C; line-height:1.5; opacity:0; animation:v13On .4s var(--d) forwards;}
  .v13gH,.v13gQ{display:grid; grid-template-columns:1fr 210px; gap:12px; align-items:center;}
  .v13gH span{font-size:14px; font-weight:800; color:#6B7785; padding-bottom:6px; border-bottom:2px solid #E3E6EA;}
  .v13gQ{margin-top:10px; opacity:0; animation:v13On .35s var(--d) forwards;}
  .v13gQ span{background:#fff; border:2px solid #C9D6E6; border-radius:10px; padding:10px 14px; font-size:17px; font-weight:700; color:#16233A;}
  .v13gQ b{background:#FFF1E2; border:2px solid #F2B880; border-radius:10px; padding:10px 14px; font-size:16px; color:#9A4F0C; opacity:0; animation:v13On .35s var(--d) forwards;}
  @keyframes v13In{to{opacity:1; transform:none}}
  @keyframes v13Strike{to{background-size:100% 2.5px; color:#9B9A97}}
  @keyframes v13Strike2{to{background-size:calc(100% - 16px) 2.5px; color:#9B9A97}}
  @keyframes v13Draw{0%{opacity:0; clip-path:inset(0 100% 0 0)} 100%{opacity:1; clip-path:inset(0 0 0 0)}}
  @media print{.v13mV,.v13mA,.v13mS,.v13mC,.v13mC span,.v13mD,.v13mD em,.v13k > div,.v13kAr,.v13kF,.v13mQ s,.v13mQ i,.v13mQ b,.v13gMe,.v13gN,.v13gQ,.v13gQ b{opacity:1; animation:none; transform:none}}
  /* 1-3 · 미니 노션 기능 (v13f) */
  .v13f{display:grid; grid-template-columns:1fr 1fr; gap:12px 20px; margin-top:0;}
  .v13fP{border:2px solid #C9D6E6; border-radius:14px; background:#F7F6F3; padding:12px 14px; opacity:.35; animation:v13On .4s var(--d) forwards;}
  .v13fH{display:flex; gap:10px; align-items:baseline; margin-bottom:8px;}
  .v13fH i{font-style:normal; background:#16233A; color:#fff; border-radius:50%; width:24px; height:24px; display:inline-flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex:none;}
  .v13fH b{font-size:21px; color:#16233A;} .v13fH span{font-size:15px; color:#C76A12; font-weight:700;}
  .v13fS{position:relative; height:186px; background:#fff; border-radius:10px; padding:10px 14px; overflow:hidden; font-family:inherit;}
  .v13fB{display:flex; justify-content:space-between; align-items:center; height:34px; padding:0 8px; margin-bottom:5px; border-radius:6px;
    opacity:0; animation:v13On .4s var(--d) forwards; color:#37352F;}
  .v13fB span{font-size:16px;} .v13fB.h span{font-size:19px; font-weight:800;}
  .v13fB em{font-style:normal; font-size:13px; font-weight:700; color:#C76A12; background:#FFF1E2; border-radius:6px; padding:2px 7px;}
  .v13f .v13fP:first-child .v13fB{outline:1.5px dashed #F2B880;}
  .v13fB.hr span{display:block; width:70%; height:2px; background:#C9C7C1;}
  .v13fSl{position:relative; height:34px; padding:0 8px; display:flex; align-items:center; font-size:18px;}
  .v13fCur{width:2px; height:20px; background:#37352F;}
  .v13fSl b{position:absolute; left:12px; font-weight:400; opacity:0; animation:v13On .1s var(--a) forwards, v13Off .2s var(--z) forwards;}
  .v13fNew{position:absolute; left:8px; font-size:16px; color:#37352F; opacity:0; background:#FFF1E2; border-radius:6px; padding:3px 8px; animation:v13On .4s var(--a) forwards;}
  .v13fM{position:absolute; left:22px; top:84px; width:180px; background:#fff; border:1.5px solid #E3E2DE; border-radius:8px; box-shadow:0 6px 16px rgba(0,0,0,.12);
    padding:4px; opacity:0; animation:v13On .2s var(--a) forwards, v13Off .2s var(--z) forwards;}
  .v13fM div{font-size:14px; line-height:20px; padding:1px 8px; border-radius:5px;}
  .v13fM div.on{animation:v13Sel .3s var(--d) forwards;}
  .v13fD{position:absolute; left:14px; right:14px; height:40px; display:flex; gap:10px; align-items:center; padding:0 8px; border-radius:6px; background:#fff; font-size:16px; color:#37352F;}
  .v13fD i{font-style:normal; color:#B0ADA6; font-weight:800; letter-spacing:-2px;}
  .v13fD.r0{top:14px; animation:v13Dn .8s calc(var(--b) + 1s) forwards;} .v13fD.r1{top:62px; animation:v13Dn .8s calc(var(--b) + 1s) forwards;}
  .v13fD.r2{top:110px; z-index:2; animation:v13Lift .3s calc(var(--b) + .4s) forwards, v13Up .8s calc(var(--b) + 1s) forwards;}
  .v13fD.r2 i{animation:v13Hd .3s calc(var(--b) + .4s) forwards;}
  .v13fBar{display:flex; gap:8px; align-items:center; font-size:14px; color:#6B7785; border-bottom:1.5px solid #E3E6EA; padding-bottom:6px; margin-bottom:10px;}
  .v13fBar i{font-style:normal; font-size:20px; color:#16233A; display:inline-block; animation:v13Spin .8s var(--b) forwards;}
  .v13fPg{animation:v13Fl 1s var(--b) forwards;}
  .v13fOk{position:absolute; right:14px; bottom:14px; background:#16233A; color:#fff; font-size:15px; font-weight:800; border-radius:8px; padding:6px 12px; opacity:0; animation:v13On .4s var(--d) forwards;}
  .v13cb{display:inline-block; width:14px; height:14px; border:1.8px solid #37352F; border-radius:3px; margin-right:8px; vertical-align:-2px; position:relative;}
  .v13cb.on{background:#2383E2; border-color:#2383E2;} .v13cb.on::after{content:""; position:absolute; left:3px; top:0; width:4px; height:8px; border:solid #fff; border-width:0 2px 2px 0; transform:rotate(45deg);}
  @keyframes v13On{to{opacity:1}} @keyframes v13Off{to{opacity:0}}
  @keyframes v13Sel{to{background:#ECEBE8; font-weight:800}}
  @keyframes v13Lift{to{box-shadow:0 8px 18px rgba(0,0,0,.18); background:#FFF8F0}}
  @keyframes v13Hd{to{color:#F28C28}}
  @keyframes v13Up{to{top:14px}} @keyframes v13Dn{to{transform:translateY(48px)}}
  @keyframes v13Spin{to{transform:rotate(360deg)}}
  @keyframes v13Fl{0%{opacity:1} 40%{opacity:.1} 100%{opacity:1}}
  @media print{.v13fP,.v13fB,.v13fNew,.v13fOk{opacity:1; animation:none}}
  /* 1-3 · IT 기업 조직 구성 (v1org) */
  .v1org{display:flex; flex-direction:column; align-items:center; margin-top:18px;}
  .v1orgT{background:#16233A; color:#fff; border-radius:14px; padding:14px 40px; text-align:center; opacity:0; animation:v1orgIn .5s .1s forwards;}
  .v1orgT b{display:block; font-size:24px;} .v1orgT span{font-size:15px; color:#C9D6E6;}
  .v1orgL{width:calc(100% - 220px); height:26px; border:3px solid #C9D6E6; border-bottom:0; border-radius:10px 10px 0 0; margin-top:16px;
    position:relative; opacity:0; animation:v1orgIn .4s .35s forwards;}
  .v1orgL::before{content:""; position:absolute; left:50%; top:-19px; width:3px; height:16px; background:#C9D6E6;}
  .v1orgR{display:grid; grid-template-columns:repeat(5,1fr); gap:14px; width:100%;}
  .v1orgC{background:#fff; border:2px solid #C9D6E6; border-radius:14px; padding:16px 10px; text-align:center; opacity:0;
    transform:translateY(10px); animation:v1orgIn .5s var(--d) forwards;}
  .v1orgC b{display:block; font-size:24px; color:#16233A; margin-bottom:8px;}
  .v1orgC span{display:block; font-size:15px; font-weight:700; color:#33465E; min-height:40px;}
  .v1orgC i{display:block; font-style:normal; font-size:15px; color:#6B7785; margin:8px 0 10px;}
  .v1orgC em{display:inline-block; font-style:normal; font-size:15px; font-weight:700; color:#C76A12; background:#FFF1E2; border-radius:10px; padding:5px 9px;}
  .v1orgM{margin-top:22px; width:100%; display:flex; gap:16px; align-items:center; justify-content:center; background:#FFF1E2;
    border:2px dashed #F28C28; border-radius:14px; padding:14px; opacity:0; animation:v1orgIn .5s var(--d) forwards;}
  .v1orgM b{font-size:20px; color:#C76A12;} .v1orgM span{font-size:19px; font-weight:700; color:#16233A;}
  @keyframes v1orgIn{to{opacity:1; transform:none;}}
  @media print{.v1orgT,.v1orgL,.v1orgC,.v1orgM{opacity:1; animation:none; transform:none}}
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
            ("이용자", "<u>메모하는 모든 사람</u>", "누가 · 어떤 기기로 쓰나요?", "회의가 잦은 직장인 나 · PC 브라우저")]
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


def _features():
    """미니 노션 기능 — 네 칸이 차례로 움직임: 블록 · 「/」 메뉴 · 끌어 옮기기 · 저장. 한 번 재생 후 마지막 장면."""
    b1, b2, b3, b4 = .3, 3.2, 7.6, 10.6
    blocks = [("h", "주간 회의", "제목"), ("p", "결정 사항 두 가지", "글"), ("c", '<i class="v13cb"></i>보고서 초안', "체크 상자"), ("hr", "", "구분선")]
    p1 = "".join(f'<div class="v13fB {k}" style="--d:{b1 + i * .5:.1f}s"><span>{t}</span><em>{tag}</em></div>' for i, (k, t, tag) in enumerate(blocks))
    menu = "".join(f'<div class="{"on" if n == "체크 상자" else ""}" style="--d:{b2 + 1.8:.1f}s">{n}</div>' for n in ("제목", "글", "체크 상자", "구분선"))
    p2 = (f'<div class="v13fB p" style="--d:{b2:.1f}s"><span>회의 내용 정리</span></div>'
          f'<div class="v13fSl"><span class="v13fCur"></span><b style="--a:{b2 + .6:.1f}s;--z:{b2 + 3:.1f}s">/</b>'
          f'<span class="v13fNew" style="--a:{b2 + 3:.1f}s"><i class="v13cb"></i>할 일</span></div>'
          f'<div class="v13fM" style="--a:{b2 + 1.1:.1f}s;--z:{b2 + 3:.1f}s">{menu}</div>')
    rows = [("참석자 4명", 0), ("회의 내용", 1), ('<i class="v13cb"></i>할 일 · 보고서 초안', 2)]
    p3 = "".join(f'<div class="v13fD r{i}" style="--b:{b3:.1f}s"><i>⋮⋮</i><span>{t}</span></div>' for t, i in rows)
    p4 = (f'<div class="v13fBar"><i style="--b:{b4 + .6:.1f}s">⟳</i><span>새로고침</span></div>'
          f'<div class="v13fPg" style="--b:{b4 + .6:.1f}s"><div class="v13fB h" style="--d:0s"><span>주간 회의</span></div>'
          f'<div class="v13fB c" style="--d:0s"><span><i class="v13cb on"></i>보고서 초안</span></div></div>'
          f'<div class="v13fOk" style="--d:{b4 + 2:.1f}s">그대로 남음</div>')
    def panel(n, title, cap, body, d):
        return (f'<div class="v13fP" style="--d:{d:.1f}s"><div class="v13fH"><i>{n}</i><b>{title}</b><span>{cap}</span></div>'
                f'<div class="v13fS">{body}</div></div>')
    return ('<div class="v13f">' + panel(1, "블록", "한 줄 = 블록 하나 · 종류 네 가지", p1, b1)
            + panel(2, "「/」 메뉴", "빈 줄에 / 입력 → 블록 종류 고르기", p2, b2)
            + panel(3, "끌어 옮기기", "⋮⋮ 손잡이를 잡고 끌면 순서가 바뀜", p3, b3)
            + panel(4, "저장", "새로고침해도 쓴 내용이 남음", p4, b4) + "</div>")


def _vague(text, d=.3, x=1.6):
    """흐린 말 카드 — 나타났다가 줄이 그어짐."""
    return (f'<div class="v13mV" style="--d:{d:.1f}s;--x:{x:.1f}s"><small>흐린 답</small><b>「{text}」</b></div>'
            f'<div class="v13mA" style="--d:{x + .2:.1f}s">좋은 답 ↓</div>')


def _scene():
    """방법 ① 사용 장면 — 하루 장면이 시간 순으로 한 줄씩 · 끝에 장면에서 나온 기능 칩."""
    rows = [("월 · 회의 직후", "회의 끝 → 새 페이지 「11/23 주간 회의」"), ("월 · 이어서", "참석자 · 결정 사항은 글 · 할 일은 체크 상자"),
            ("월 · 정리할 때", "급한 할 일 → 끌어서 맨 위로"), ("금 · 퇴근 전", "같은 페이지를 열어 끝낸 할 일 체크")]
    r = "".join(f'<div class="v13mS" style="--d:{2.2 + i * 1.0:.1f}s"><i>{t}</i><span>{x}</span></div>' for i, (t, x) in enumerate(rows))
    chips = "".join(f'<span style="--d:{6.4 + i * .25:.2f}s">{c}</span>' for i, c in enumerate(["새 페이지", "글", "체크 상자", "끌어 옮기기", "금요일까지 저장"]))
    return (f'<div class="v13m"><div class="v13mL">{_vague("회의록을 관리한다")}</div><div class="v13mR">'
            f'<div class="v13mT">내 하루 · 사용 장면</div>{r}<div class="v13mC" style="--d:6.2s"><b>장면에서 나온 기능</b>{chips}</div></div></div>')


def _sample():
    """방법 ② 예시 데이터 — 실제 회의록 한 장이 한 줄씩 · 줄마다 블록 종류 이름표."""
    rows = [("11/23 주간 회의", "제목", "h"), ("참석 · 김하늘 · 이준호 · 박서연 · 최민재", "글", ""), ("결정 사항 · 설문 결과는 다음 회의에서 공유", "글", ""),
            ('<i class="v13cb"></i>보고서 초안 · 하늘', "체크 상자", ""), ('<i class="v13cb"></i>설문 정리 · 준호', "체크 상자", ""), ('<hr/>', "구분선", "hr")]
    r = "".join(f'<div class="v13mD {k}" style="--d:{2.2 + i * .6:.1f}s"><span>{t}</span><em style="--d:{5.8 + i * .2:.1f}s">{tag}</em></div>'
                for i, (t, tag, k) in enumerate(rows))
    return (f'<div class="v13m"><div class="v13mL">{_vague("메모를 쓴다")}</div><div class="v13mR">'
            f'<div class="v13mT">내가 실제로 쓴 회의록 · 그대로 붙여 넣기</div><div class="v13mP">{r}</div>'
            '<div class="v13mC" style="--d:7.2s"><b>여기서 정해진 것</b><span style="--d:7.3s">블록 종류 네 가지</span>'
            '<span style="--d:7.5s">할 일 = 체크 상자</span></div></div></div>')


def _sketch():
    """방법 ③ 손그림 화면 — 연필 선 네모가 하나씩 그려지고 → 실제 화면."""
    parts = [("v13kA", "페이지 목록", 2.2), ("v13kT", "큰 제목", 3.0), ("v13kB", "줄마다 블록", 3.8), ("v13kM", "/ → 메뉴", 4.6), ("v13kN", "+ 새 페이지", 5.2)]
    k = "".join(f'<div class="{c}" style="--d:{d:.1f}s"><span>{t}</span></div>' for c, t, d in parts)
    return (f'<div class="v13m"><div class="v13mL">{_vague("깔끔한 화면")}</div><div class="v13mR v13mK">'
            f'<div><div class="v13mT">종이 · PPT 에 네모 몇 개</div><div class="v13k">{k}</div></div>'
            '<div class="v13kAr" style="--d:6.2s">사진 첨부 →<small>Claude Code 가 그림을 읽음</small></div>'
            '<figure class="v13kF" style="--d:6.6s"><img src="img/notion_main.webp" alt="미니 노션 실제 화면"/><figcaption>만든 화면</figcaption></figure></div></div>')


def _check():
    """방법 ④ 「~하면 ~된다」 — 흐린 문장이 지워지고 조건(파랑) + 결과(주황) 두 조각 문장으로."""
    rows = [("저장이 잘 된다", "새로고침하면", "쓴 내용이 그대로 있다"),
            ("메뉴가 편하다", "빈 줄에 / → 「체크 상자」를 고르면", "그 줄이 체크 상자가 된다"),
            ("순서를 쉽게 바꾼다", "할 일을 끌어 맨 위에 놓으면", "순서가 바뀐다")]
    r = "".join(f'<div class="v13mQ"><s style="--d:{.3 + i * 1.8:.1f}s;--x:{1.1 + i * 1.8:.1f}s">「{v}」</s><i style="--d:{1.1 + i * 1.8:.1f}s">→</i>'
                f'<b class="if" style="--d:{1.3 + i * 1.8:.1f}s">{a}</b><b class="then" style="--d:{1.8 + i * 1.8:.1f}s">{c}</b></div>'
                for i, (v, a, c) in enumerate(rows))
    return (f'<div class="v13mQs"><div class="v13mQh"><span>흐린 답</span><span></span><span class="if">하면</span><span class="then">된다</span></div>{r}</div>'
            '<div class="v13mC wide" style="--d:6.2s"><b>쓰는 곳</b><span style="--d:6.3s">기획서 확인 문장</span>'
            '<span style="--d:6.5s">1-6 에서 눌러 볼 목록</span><span style="--d:6.7s">누가 해도 같은 판단</span></div>')


def _gapask():
    """AI 에게 빈칸 찾게 하기 — 요청 한 줄 → AI 질문 다섯 개 → 내 짧은 답."""
    qs = [("페이지를 지우면 되살릴 수 있나요?", "아니, 확인 창만"), ("할 일을 다 하면 줄을 긋나요?", "응, 회색 줄"),
          ("휴대폰에서도 쓰나요?", "가끔 · 보이기만 하면 됨"), ("새 페이지는 목록 어디에?", "맨 아래"), ("글자 · 색은 어떤 느낌?", "노션처럼 흰 바탕")]
    r = "".join(f'<div class="v13gQ" style="--d:{1.6 + i * .9:.1f}s"><span>{q}</span><b style="--d:{2.0 + i * .9:.1f}s">{a}</b></div>' for i, (q, a) in enumerate(qs))
    return ('<div class="v13g"><div class="v13gL"><div class="v13gMe" style="--d:.3s">이 기획서로 만들면<br/>네가 <u>추측해야 하는 곳</u>을<br/>다섯 개 뽑아 줘</div>'
            '<div class="v13gN" style="--d:6.6s">내가 못 찾는 빈칸<br/>→ AI 가 질문으로 · 나는 답만</div></div>'
            f'<div class="v13gR"><div class="v13gH"><span>Claude Code 가 찾은 빈칸 · 예</span><span>내 답</span></div>{r}</div></div>')


def _interview():
    """기획서 인터뷰 — 기획자 질문(예시 답 포함) → 내 답 → 기획서.md 칸이 한 줄씩 채워짐. 한 번 재생."""
    rows = [("요즘 회의록 때문에 곤란했던 일 하나만?", "지난주 회의록을 못 찾아 다시 물어봤어", "문제점"),
            ("누가 · 어디서 쓰나요?", "나 혼자 · 회사 PC", "이용자"),
            ("회의 끝나고 어떤 순서로 쓰나요?", "새 페이지 → 할 일은 체크 상자 → 금요일에 체크", "사용 장면"),
            ("실제로 쓴 회의록 하나 붙여 줄래요?", "회의록 복사해서 붙여 넣음", "예시 데이터"),
            ("화면을 대충 그려서 찍어 줄래요?", "종이 그림 사진 첨부", "화면 스케치"),
            ("다 되면 뭘 눌러 보고 됐다고 할까요?", "새로고침해도 그대로면 됨", "확인 문장")]
    r = ""
    for i, (q, a, k) in enumerate(rows):
        d = .5 + i * 1.1
        r += (f'<div class="v13iR"><div class="q" style="--d:{d:.1f}s">{q}</div><div class="a" style="--d:{d + .4:.1f}s">{a}</div>'
              f'<i style="--d:{d + .7:.1f}s">→</i><div class="k" style="--d:{d + .8:.1f}s">{k}</div></div>')
    return ('<div class="v13iH"><span>기획자가 묻는 것</span><span>내 답</span><span></span><span>기획서.md 칸</span></div>'
            f'<div class="v13i">{r}</div>'
            '<div class="v14gN" style="--d:7.4s"><b>나는 답만</b>칸 이름은 몰라도 됨 · 정리는 기획자가</div>')


def _tone13():
    """보통 기획 용어 → 기획자.md 말투 — 같은 질문이 일상 말 + 예시 답으로. 1-4 말투 비교(v14o)와 같은 모양."""
    rows = [("문제", "배경과 문제점을 서술해 주세요",
             "요즘 회의록 때문에 곤란했던 일 하나만 들려주세요 · 예: 지난주 회의록을 못 찾았다"),
            ("장면", "주요 유저 플로우를 정의해 주세요",
             "회의 끝나고 이 앱을 어떤 순서로 쓸지 말해 주세요 · 예: 새 페이지 → 할 일 적기 → 금요일에 체크"),
            ("확인", "인수 조건을 작성해 주세요",
             "다 만들면 뭘 눌러 보고 됐다고 할까요? · 예: 새로고침해도 그대로 있으면 됨")]
    r = ""
    for i, (k, dev, lead) in enumerate(rows):
        d = .4 + i * 2.2
        r += (f'<div class="v14oR"><b style="--d:{d:.1f}s">{k}</b><div class="v14oD" style="--d:{d:.1f}s;--x:{d + 1.0:.1f}s">{esc(dev)}</div>'
              f'<i style="--d:{d + 1.0:.1f}s">→</i><div class="v14oL" style="--d:{d + 1.2:.1f}s">{esc(lead)}</div></div>')
    return (f'<div class="v14o"><div class="v14oH"><span></span><span>기획 용어로 묻기</span><span></span><span>기획자.md 말투 · 일상 말 + 예시 답</span></div>{r}</div>'
            '<div class="v14gN" style="--d:7.2s"><b>예시 답</b>무엇을 답할지 보이면 바로 답할 수 있음</div>')


def slides():
    return [
        # ── 왜 기획하나
        light("모호한 요청과 구체적 요청", shot("v1_u3_salt.webp", "모호한 요청 · 「소금 적당히」", [
            ("모호 · 「소금 적당히」", "사람마다 다른 양"), ("구체 · 「소금 1g」", "누가 해도 같은 맛"),
            ("모호 · 「미니 노션 만들어 줘」", "AI 가 기능 · 화면을 정함"), ("구체 · 기획서", "내가 정한 대로")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("IT 기업 조직 구성", _org(), T),
        light("IT 기업의 개발 흐름", _devflow(), T),
        # ── 만들 것
        light("미니 노션 완성 화면", shot("notion_main.webp", "미니 노션 · 완성 화면", [
            ("페이지 목록", "왼쪽 목록 · 새 페이지 · 삭제"), ("블록", "제목 · 글 · 체크 상자 · 구분선"),
            ("「/」 메뉴", "「/」 입력 → 블록 종류 고르기"), ("끌어 옮기기", "손잡이로 블록 순서 바꾸기"),
            ("저장", "새로고침 뒤에도 그대로"), ("더 넣고 싶은 것", "기획서에 적으면 같이 개발")]), T),
        light("미니 노션 기능", _features(), T),
        # ── 기획서
        light("기획서", shot("v1_u3_plan.webp", "기획서 · 한 장의 문서", [
            ("머릿속 아이디어", "설명할 때마다 내용이 바뀜"), ("기획서", "무엇이 불편 · 누가 · 어떤 장면 · 어떤 화면 · 어떻게 확인"),
            ("만드는 법", "기획자가 묻고 나는 답만 · 정리는 기획자")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("기획서 인터뷰", _interview(), T),
        # ── 좋은 답 네 가지
        light("좋은 답 ① 하루 시나리오", _scene(), T),
        light("좋은 답 ② 실제 메모", _sample(), T),
        light("좋은 답 ③ 손그림", _sketch(), T),
        light("좋은 답 ④ 「~하면 ~된다」 문장", _check(), T),
        # ── Claude Code 와 기획하기
        light("먼저 묻기 모드와 역할 메모", viz2.pair(
            "Plan Mode · 먼저 묻기 모드", [("켜는 법", "입력창 아래 모드 표시 → Plan"), ("하는 일", "바로 만들지 않고 먼저 질문 · 초안"),
                                       ("파일", "내가 승인한 뒤에 생김")],
            "페르소나 · 역할 메모", [("비유", "회의 때 받는 「오늘 당신은 사회자」 카드"), ("모양", "기획자.md 파일 하나 · 몇 줄"),
                                  ("쓰는 법", "「기획자.md 대로」 한마디")], hl="r")
              + note("둘을 같이", "먼저 묻기 모드 + 기획자.md → 기획자가 인터뷰하고 나는 답만")
              + src(("Claude Code · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        light("기획자 페르소나", '<div class="twocol"><div>' + code("기획자.md", esc(_persona("기획자")))
              + '</div><div>' + viz2.tiles([("듣는 사람", "IT 를 모르는 직장인 · 나"), ("질문", "하나씩 · 일상 말 · 예시 답"),
                                          ("흐린 답", "실제 있었던 일로 다시"), ("마지막 줄", "기획서 칸 = 기획자의 체크리스트")], 1) + "</div></div>", T),
        light("기획자 말투 비교", _tone13(), T),
        light("기획자 페르소나 대화 예시", '<div class="twocol"><div>' + chat([
            ("me", "기획자.md 대로 미니 노션 기획서를 같이 쓰자"),
            ("ai", "요즘 회의록 때문에 곤란했던 일 하나만 들려주세요.\n예: 지난주 회의록을 못 찾아 다시 물어봤다"),
            ("me", "메모가 여기저기 흩어져서 불편해"),
            ("ai", "조금만 더 구체적으로요. 최근에 실제로 있었던 일 하나만요.\n예: 언제 · 무엇을 찾다가 · 어떻게 됐는지"),
            ("me", "지난주 회의록이 어느 파일에 있는지 몰라 다시 물어봤어")], "Plan Mode 대화 예")
              + '</div><div><img class="v1u3im" src="img/v1_u3_ask.webp" alt="질문하는 AI · 답하는 사람"/></div></div>'
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("빈칸 찾기 요청", _gapask(), T),
        # ── 실습
        labcard("1-3", "기획서 작성", T, "기획자.md", "기획서.md", ["먼저 묻기 모드", "인터뷰에 답하기", "빈칸 찾기"]),
        brief("1-3", T, ["새 폴더 mini_notion_v2 만들어 열기 · 기획자.md 만들기", "모드 표시 → Plan · 「기획자.md 대로 미니 노션 기획서를 같이 쓰자」", "인터뷰에 답하기 · 메모 붙여 넣기 · 그림 사진 첨부", "「추측해야 하는 곳 뽑아 줘」 → 답하기", "승인 → 정리된 기획서.md 확인"],
              [],
              ["기획자.md", "먼저 묻기 모드", "인터뷰", "빈칸 찾기"],
              ["여섯 칸이 모두 내 답으로 채워짐", "확인 문장이 「~하면 ~된다」"],
              "모르는 질문엔 「아직 안 정함」으로 답하기", folder="workspace/mini_notion_v2/기획서.md"),
        tstep("1-3", 1, "새 폴더 · 기획자.md", T, term=("workspace/mini_notion_v2/기획자.md", _persona("기획자")),
              rows=[("새 폴더", "workspace 안에 mini_notion_v2 → VS Code 로 열기"), ("만들기", "탐색기 → 새 파일 → 기획자.md · 일곱 줄"), ("저장", "macOS ⌘S · Windows Ctrl+S")]),
        tstep("1-3", 2, "Plan Mode 요청", T, "lab13_plan.webp", "Plan Mode 에서 요청을 쓴 화면",
              rows=[("먼저 묻기 모드", "입력창 아래 모드 표시 → Plan"), ("요청", "「기획자.md 대로 같이 쓰자」"), ("파일", "아직 안 씀")]),
        tstep("1-3", 3, "인터뷰에 답하기", T, "lab13_q1.webp", "기획자 페르소나의 첫 질문",
              rows=[("답", "예시 답을 보고 내 경우로"), ("메모 · 그림", "복사해 붙여 넣기 · 사진 첨부"), ("모를 때", "「아직 안 정함」")]),
        tstep("1-3", 4, "빈칸 찾기", T, "lab13_draft.webp", "초안 요약과 흐린 부분 질문",
              rows=[("요청", "「추측해야 하는 곳 다섯 개 뽑아 줘」"), ("답", "짧게 · 하나씩"), ("피드백", "빠진 장면 · 고칠 문장")]),
        tstep("1-3", 5, "승인 · 저장", T, "lab13_saved.webp", "기획서.md 저장 결과",
              rows=[("승인", "2번 · 수정마다 직접 승인"), ("저장", "Do you want to create → 1. Yes"), ("결과", "mini_notion_v2/기획서.md")]),
        light("실습 1-3 확인", checks([
            ("사용 장면이 내 실제 하루인가", "「관리한다」만 있으면 다시"), ("예시 데이터가 들어 있나", "실제 회의록 · 메모 한 장"),
            ("화면 스케치가 있나", "사진이나 「왼쪽 · 오른쪽」 설명"), ("확인 문장이 「~하면 ~된다」인가", "「잘 된다」면 다시")],
            "「아니요」 → 그 칸만 다시 요청 · 넷 다 「예」 → 1-4"), T),
    ]
