"""1-3 기획서 작성.

만들 수 있는 것 → 아이디어 고르기(세 갈래 · 난이도 · 한 줄) → 기획서(모호 vs 구체 · 다섯 칸 · 칸별 기준) → Claude와 다듬기 → 실습.
예시 문장은 labs/team_board/예시/기획서.md 에서 그대로 읽는다. 산출물 기획서.md 는 1-4 PRD 의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import brief, chat, shot

T = "1-3"
EX = Path(__file__).resolve().parent.parent / "labs" / "team_board" / "예시"


def _plan():
    return (EX / "기획서.md").read_text(encoding="utf-8").strip()


def _heads():
    return "\n".join(x for x in _plan().split("\n") if x.startswith("#"))


# IT 기업 개발 흐름 — (단계, 담당, 산출물, 1부 단원, 1부에서 하는 일)
DEVFLOW = [
    ("기획", "기획자 · PM", "기획서", "1-3", "기획서.md"),
    ("요구사항 정의", "PM · 개발 리드", "PRD", "1-4", "PRD.md"),
    ("설계", "디자이너 · 개발자", "화면 · 구조 설계", "1-6", "Plan Mode 계획"),
    ("개발 계획", "개발 리드", "태스크 · 일정", "1-6", "태스크 T1~T6"),
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
    me = "".join(f'<div class="v1dmm" style="--d:{.4 + i * .45:.2f}s"><small>{u}</small><b>{w}</b></div>'
                 for i, (_, _, _, u, w) in enumerate(DEVFLOW))
    return (f'<div class="v1dm"><div class="v1dml"></div>{head}'
            f'<div class="v1dml">회사<small>역할별 담당자</small></div>{co}'
            f'<div class="v1dml on">1부<small>나 · Claude · Claude Code</small></div>{me}</div>')


CSS = """
  /* 1-3 · 기획서 구성 애니메이션 (v1pl) */
  .v1plW{display:grid; grid-template-columns:330px 40px 1fr; gap:14px; align-items:center;}
  .v1plL{display:flex; flex-direction:column; gap:9px;}
  .v1plH{font-size:15px; font-weight:800; color:#6B7785;}
  .v1plS{font-size:17px; font-weight:700; color:#16233A; background:#fff; border:2px solid #D9DDE3; border-radius:12px; padding:8px 12px;
    opacity:0; animation:v1plIn .5s var(--d) forwards, v1plHi .6s var(--h) forwards;}
  .v1plS.msg{background:#FFFBEA; border-color:#F2DE9B;} .v1plS em{display:block; font-style:normal; font-size:12px; font-weight:800; color:#8A94A3;}
  .v1plA{font-size:34px; font-weight:900; color:#F28C28; text-align:center; opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1plD{background:#16233A; border-radius:16px; padding:14px 18px; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  .v1plF{font-family:var(--mono); font-size:13px; color:#8FA3BC; margin-bottom:6px;}
  .v1plR{display:grid; grid-template-columns:150px 1fr auto; gap:12px; align-items:center; padding:9px 0; border-top:1px solid #2C4466;}
  .v1plR b{font-family:var(--mono); font-size:16px; color:#F6B26B;}
  .v1plT{font-size:17px; font-weight:700; color:#fff; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  .v1plR.no .v1plT{text-decoration:line-through; text-decoration-color:#F28C28; color:#C9D3E0;}
  .v1plR i{font-style:normal; font-size:12px; font-weight:800; color:#16233A; background:#F28C28; border-radius:8px; padding:2px 8px; opacity:0; animation:v1plIn .6s var(--d) forwards;}
  @keyframes v1plIn{from{opacity:0} to{opacity:1}}
  @keyframes v1plHi{to{border-color:#F28C28; box-shadow:0 0 0 3px #FCD9B3; opacity:.55}}
  @media print{.v1plS,.v1plA,.v1plD,.v1plT,.v1plR i{opacity:1; animation:none}}
  /* 1-3 · 피드백 반영 애니메이션 (v1rw) */
  .v1rwW{display:flex; flex-direction:column; gap:22px; margin-top:8px;}
  .v1rwR{display:grid; grid-template-columns:130px 1fr 300px 1fr; gap:14px; align-items:center;}
  .v1rwH{font-size:19px; font-weight:800; color:#16233A; opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1rwV{font-size:20px; font-weight:700; color:#16233A; background:#F4F6F9; border-radius:12px; padding:14px 16px;
    opacity:0; animation:v1plIn .5s var(--d) forwards, v1rwX .6s var(--x) forwards;}
  .v1rwV u{text-decoration:none; border-radius:4px; animation:v1rwU .6s var(--u) forwards;}
  .v1rwQ{font-size:17px; font-weight:700; color:#16233A; background:#FFF8F0; border:2px solid #F28C28; border-radius:14px; padding:10px 14px;
    opacity:0; animation:v1plIn .5s var(--d) forwards;}
  .v1rwQ em{display:block; font-style:normal; font-size:12px; font-weight:800; color:#E07A12;}
  .v1rwN{font-size:20px; font-weight:800; color:#1E7B45; background:#F1FAF4; border:2px solid #9FC5A8; border-radius:12px; padding:14px 16px;
    opacity:0; animation:v1plIn .6s var(--d) forwards;}
  @keyframes v1rwU{to{background:#FDECEA; color:#C0392B; box-shadow:0 0 0 2px #E6B0AA;}}
  @keyframes v1rwX{to{opacity:.45; text-decoration:line-through;}}
  @media print{.v1rwH,.v1rwV,.v1rwQ,.v1rwN{opacity:1; animation:none}}
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
    rows = [("배경", "현재 방식", "주간 회의 할 일이 회의록 · 단톡방에 흩어짐", "msg", "「보고서는 하늘 님이 금요일까지」"),
            ("문제점", "실제 장면", "기한 지난 일을 늦게 앎", "msg", "「설문 정리 기한 지났는데 몰랐어요」"),
            ("목표 이용자", "사람 · 기기", "팀원 8명 · PC 브라우저", "memo", "팀 8명 · 회사 PC"),
            ("서비스 컨셉", "한 문장 + 규칙", "할 일 · 진행 중 · 완료 세 칸 보드 · 기한 지나면 빨간 표시", "memo", "할 일을 칸별로 한눈에"),
            ("화면 구성", "3개 이내", "보드 · 추가 창 · 할 일 상세", "memo", "보드 · 추가 창 · 상세"),
            ("하지 않을 것", "1부 범위 밖", "로그인 · 알림 · 첨부 · 댓글", "memo", "로그인 · 알림도?")]
    left, right = "", ""
    for i, (h, tag, body, kind, raw) in enumerate(rows):
        d = 3.6 + i * 2.2
        left += (f'<div class="v1plS {kind}" style="--d:{.3 + i * .25:.2f}s;--h:{d:.1f}s">'
                 f'<em>{"단톡방" if kind == "msg" else "메모"}</em>{raw}</div>')
        right += (f'<div class="v1plR{" no" if i == 5 else ""}"><b>## {h}</b><span class="v1plT" style="--d:{d + .5:.1f}s">{body}</span>'
                  f'<i style="--d:{d + .5:.1f}s">{tag}</i></div>')
    return (f'<div class="v1plW"><div class="v1plL"><div class="v1plH">흩어진 재료</div>{left}</div>'
            f'<div class="v1plA" style="--d:2.2s">→</div>'
            f'<div class="v1plD" style="--d:2.2s"><div class="v1plF">기획서.md</div>{right}</div></div>')


def fb_rewrite():
    """피드백 반영 — 흐린 문장 → 흐린 말 강조 → Claude 질문 → 구체 문장으로 바뀜. 두 줄 · 장면 간격 2초."""
    rows = [("문제점", "할 일 관리가 <u>불편하다</u>", "실제로 어떤 일이 있었나요?", "기한 지난 일을 그다음 회의에서야 안다"),
            ("목표 이용자", "<u>일하는 모든 사람</u>", "누가 · 어떤 기기로 쓰나요?", "팀원 8명 · PC 브라우저")]
    out = ""
    for i, (h, vague, q, done) in enumerate(rows):
        t = .3 + i * 6.4
        out += (f'<div class="v1rwR"><div class="v1rwH" style="--d:{t:.1f}s">{h}</div>'
                f'<div class="v1rwV" style="--d:{t:.1f}s;--u:{t + 1.2:.1f}s;--x:{t + 4.2:.1f}s">「{vague}」</div>'
                f'<div class="v1rwQ" style="--d:{t + 2.2:.1f}s"><em>Claude</em>{q}</div>'
                f'<div class="v1rwN" style="--d:{t + 4.2:.1f}s">「{done}」</div></div>')
    return f'<div class="v1rwW">{out}</div>'


def slides():
    return [
        # ── IT 기업의 개발 흐름
        light("IT 기업의 개발 흐름", _devflow(), T),
        light("개발 흐름과 1부 단원", _devmap(), T),
        # ── 무엇을 만들까
        light("앱 아이디어 예시", viz2.tiles([
            ("팀 할 일 보드", "할 일 · 담당자 · 기한 · 기한 지남 표시"), ("점심 메뉴 투표", "후보 올리기 · 한 표씩"),
            ("업무 체크리스트", "매주 반복 항목 · 완료 표시"), ("경비 정산 계산기", "금액 입력 · 1인당 금액"),
            ("사내 FAQ 페이지", "질문 검색 · 답 펼치기"), ("행사 D-day 안내", "남은 날 · 준비물 목록")], 3)
              + note("공통점", "화면 1~3개 · 입력 몇 칸 · 결과 즉시 표시"), T),
        light("공통 예제 · 팀 할 일 보드", shot("board_main.webp", "팀 할 일 보드 · 1-6 완성 화면", [
            ("화면", "1개 · 할 일 · 진행 중 · 완료 세 칸"), ("입력", "3칸 · 할 일 · 담당자 · 기한"),
            ("규칙", "기한이 지난 미완료 할 일은 빨간 표시"), ("저장", "내 브라우저")]), T),
        # ── 아이디어 고르기
        light("아이디어 유형", viz2.maprows([
            ("① 클론 · 기능 하나", "협업 툴의 칸반 보드 → 팀 할 일 보드", "이름 · 로고는 따라 하지 않음"),
            ("② 반복하는 일", "회의 뒤 단톡방 할 일 공지 → 할 일 보드", "「이번 주에 같은 일을 두 번 했나」"),
            ("③ 만들고 싶던 것", "흩어진 가족 일정 → 가족 일정 보드", "가장 자주 쓸 화면 하나만")], "유형", "예")
              + note("고르는 기준", "내가 직접 쓸 것 · 결과를 내가 판단 가능"), T),
        light("난이도 기준", viz2.fit(
            [("화면 1~3개", "보드 · 추가 창"), ("내 브라우저에 저장", "서버 · DB 없음"), ("입력 → 결과 즉시", "버튼 클릭 → 화면 변화")],
            [("로그인 · 회원가입", "계정 · 비밀번호 관리"), ("결제", "돈 · 보안"), ("여러 사람 실시간 공유", "서버 저장 · 2부 DB"),
             ("외부 서비스 연동", "슬랙 · 메일 · 2부 API")],
            gt="1부 범위", bt="1부 제외")
              + note("제외 항목", "기획서 「하지 않을 것」 칸"), T),
        ba("범위 줄이기", T, "「팀 업무 관리 시스템」\n일정 · 할 일 · 휴가 · 결재 · 알림",
           "「팀 할 일 보드」\n세 칸 보드 · 담당자 · 기한 · 기한 지남 표시", "한 화면 · 핵심 규칙 하나"),
        light("한 줄 아이디어", '<div class="v1big"><em>누가</em> · <em>언제</em> · <em>무엇을</em> · <em>한 화면에서</em></div>'
              + viz2.tiles([("누가", "팀원 8명"), ("언제", "주간 회의가 끝난 뒤"), ("무엇을", "할 일 · 담당자 · 기한을 보고 챙김"),
                            ("한 화면에서", "세 칸 보드")], 4)
              + note("예", "「팀원 8명이 주간 회의가 끝난 뒤, 할 일 · 담당자 · 기한을 세 칸 보드 한 화면에서 보고 챙김」"), T),
        # ── 기획서
        light("모호한 요청과 구체적 요청", shot("v1_u3_salt.webp", "모호한 요청 · 「소금 적당히」", [
            ("모호 · 「소금 적당히」", "사람마다 다른 양"), ("구체 · 「소금 1g」", "누가 해도 같은 맛"),
            ("모호 · 「좋은 데로 데려다줘」", "목적지 불명 · 안내 불가"), ("구체 · 「서울역 → 강남역 · 최단 경로」", "경로 안내")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo"),
                    ("참고 · 알파AI스쿨 「바이브 코딩이란?」", "https://www.youtube.com/watch?v=cFdyp_pPgPQ"),
                    ("참고 · 한빛미디어 「바이브 코딩 입문 1강」", "https://www.youtube.com/watch?v=n6xAUiTTrZU")), T),
        light("기획서", shot("v1_u3_plan.webp", "기획서 · 한 장의 문서", [
            ("머릿속 아이디어", "설명할 때마다 내용이 바뀜"), ("기획서", "왜 · 누구에게 · 무엇을 · 어떤 화면"),
            ("기획서.md 파일", "1-4 PRD 의 입력 · Claude Code 가 읽음")])
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("기획서 구성", plan_build()
              + note("파일", "기획서.md · 칸마다 「## 제목」 · 「하지 않을 것」은 1-4 PRD 의 「제외」 칸"), T),
        light("기획서 예시", '<div class="twocol"><div>' + code("기획서.md · 칸 제목", esc(_heads()))
              + '</div><div>' + viz2.tiles([("한 파일", "칸마다 「## 제목」 · 3~5줄"), ("분량", "한 화면 분량"),
                                          ("다음 단원", "1-4 · Claude Code 가 이 파일을 읽음")], 1) + "</div></div>"
              + note("파일", "labs/team_board/예시/기획서.md"), T),
        # ── Claude와 만들기
        light("Claude로 기획서 쓰기", flow([("한 줄 아이디어", "누가 · 언제 · 무엇을"), ("Claude 질문", "소크라테스식 · 하나씩"), ("내 답", "실제 장면 · 숫자"),
                                            ("초안", "다섯 칸 + 하지 않을 것"), ("피드백 · 수정", "빠진 칸 · 큰 기능")])
              + note("순서", "질문 먼저 · 초안은 그다음 · 답은 사실만"), T),
        light("Claude의 역질문 예시", '<div class="twocol"><div>' + chat([
            ("me", "팀 할 일 보드 기획서를 쓰려고 해. 소크라테스식 대화로 진행해 줘"),
            ("ai", "팀은 몇 명이고, 지금은 할 일을 어떻게 나누나요?"),
            ("me", "8명이고 회의 끝나면 단톡방에 「보고서는 하늘 님이 금요일까지」처럼 남겨"),
            ("ai", "그 방식에서 실제로 문제가 된 일이 있었나요?"),
            ("me", "기한 지난 일을 그다음 회의에서야 알았어")], "Claude · 대화 예")
              + '</div><div><img class="v1u3im" src="img/v1_u3_ask.webp" alt="질문하는 AI · 답하는 사람"/></div></div>'
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("피드백 반영 전후", fb_rewrite()
              + note("피드백 요청 예", "「흐린 문장을 찾아서 물어봐 줘」"), T),
        light("피드백 요청 방법", viz2.tiles([
            ("빠진 칸", "비었거나 짧은 칸 찾기"), ("큰 기능", "1부 범위 밖 기능 골라내기"),
            ("이용자 관점", "처음 쓰는 팀원이 헷갈릴 곳")], 3)
              + note("결정", "제안은 Claude · 반영 여부는 사람"), T),
        light("기획서에서 흔한 실수", viz2.tiles([
            ("기능 나열만", "배경 · 문제점 없이 기능 목록"), ("화면 10개", "한 번에 전부 만들려 함"),
            ("이용자 「모두」", "누구 기준인지 불명"), ("해결책만", "문제점 칸에 「앱이 없다」")], 2), T),
        # ── 실습
        lab("1-3", "기획서 작성", T, "내 아이디어 → Claude와 다섯 칸 기획서 → 기획서.md",
            ["아이디어 고르기 · 한 줄로", "Claude에게 질문받으며 초안", "피드백 요청 → 다듬기", "기획서.md 로 저장"],
            ["다섯 칸 + 하지 않을 것 · 화면 3개 이내", "로그인 · 결제 · 외부 연동은 「하지 않을 것」에"],
            files="예시/기획서.md (비교용)"),
        brief("1-3", T, ["claude.ai 새 대화", "한 줄 아이디어 보내기", "질문에 답하기", "초안 → 피드백 요청", "기획서.md 로 저장"],
              [("목표", "기획서 초안 · 다섯 칸"), ("입력", "내 한 줄 아이디어"), ("진행 방식", "소크라테스식 대화 · 질문 하나씩"), ("하지 말 것", "로그인 · 결제 · 외부 연동 넣기")],
              ["배경", "문제점", "목표 이용자", "하지 않을 것"],
              ["다섯 칸이 모두 내 사실로 채워짐", "「하지 않을 것」 칸이 있음"],
              "아이디어가 없으면 ② 반복하는 일 · 「이번 주에 같은 일을 두 번 했나」", folder="claude.ai → 내 프로젝트 폴더/기획서.md"),
        light("실습 1-3 확인", checks([
            ("문제점이 실제 장면인가", "「불편하다」만 있으면 다시"), ("목표 이용자가 실제 사람인가", "「모두」면 다시"),
            ("화면이 3개 이내인가", "넘는 화면은 「하지 않을 것」 칸에"), ("하지 않을 것이 있는가", "로그인 · 결제 · 외부 연동")],
            "넷 다 「예」 → 기획서.md 저장 · 1-4 PRD 의 입력"), T),
    ]
