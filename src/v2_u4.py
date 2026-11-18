"""2-4 기획 · 요구사항.

기본 흐름 복습(1부와 같음 · DB · MCP 는 양념) → DB · 외부 연동 주제 예 → 실습 주제(팀 회의실 예약)
→ 기획서 v2(소크라테스식 대화) → PRD v2 에 늘어나는 세 칸(데이터 구조 · 연동 대상 · 권한) → 완료 기준 → 실습.
예시 문장은 labs/room_booking_v2/예시/ 의 기획서.md · PRD.md 에서 그대로 읽는다. 산출물 PRD v2 는 2-5 · 2-6 구현의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v2kit import brief, chat, shot

T = "2-4"
EX = Path(__file__).resolve().parent.parent / "labs" / "room_booking_v2" / "예시"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def _prd():
    return (EX / "PRD.md").read_text(encoding="utf-8").strip()


def _sec(no):
    """PRD.md 의 「## no.」 칸을 제목 줄과 함께 그대로."""
    t = _prd()
    i = t.index(f"## {no}.")
    j = t.find("\n## ", i + 1)
    return t[i: j if j > 0 else None].strip()


CSS = """
  /* 2-4 · PRD 칸 지도 */
  .v2u4prd{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:8px 0 16px;}
  .v2u4prd div{border:1.5px solid #D9DDE3; border-radius:12px; background:#fff; padding:14px 16px; min-height:84px;}
  .v2u4prd div b{display:block; font-size:19px; color:#16233A;} .v2u4prd div span{font-size:14.5px; color:#6B7785;}
  .v2u4prd div.new{border-color:#F28C28; background:#FFF3E6; opacity:0; animation:v2u4pop .5s ease-out var(--d) forwards;}
  .v2u4prd div.new span{color:#E07A12; font-weight:700;}
  @keyframes v2u4pop{from{opacity:0; transform:translateY(14px) scale(.96)} to{opacity:1; transform:none}}
  /* 2-4 · 새 세 칸 예 */
  .v2u4three{display:grid; grid-template-columns:1.25fr 1.25fr 1fr; gap:14px; align-items:start;}
  .v2u4c{border:1.5px solid #F7C99A; border-radius:14px; background:#fff; overflow:hidden; opacity:0; animation:v2u4pop .55s ease-out var(--d) forwards;}
  .v2u4c .h{background:#FFF3E6; padding:10px 14px; display:flex; gap:8px; align-items:baseline; flex-wrap:wrap;}
  .v2u4c .h span{font-family:var(--mono); font-weight:800; color:#E07A12;} .v2u4c .h b{font-size:19px; color:#16233A;}
  .v2u4c .h small{font-size:13.5px; color:#6B7785;}
  .v2u4c table{border-collapse:collapse; width:100%;} .v2u4c th{background:#F4F6F9; font-size:13px; color:#3A4657; text-align:left; padding:6px 9px;}
  .v2u4c td{font-size:13.5px; color:#16233A; padding:6px 9px; border-top:1px solid #EEF0F3; line-height:1.4; vertical-align:top;}
  @media print{.v2u4prd div.new, .v2u4c{opacity:1; animation:none}}
"""


def _mdtable(sec):
    """PRD 칸의 마크다운 표 → 작은 HTML 표 (머리 줄 · 본문 줄)."""
    rows = [[c.strip() for c in x.strip().strip("|").split("|")] for x in sec.split("\n") if x.strip().startswith("|")]
    rows = [r for r in rows if not set("".join(r)) <= set("-: ")]
    th = "".join(f"<th>{esc(c)}</th>" for c in rows[0])
    tb = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f"<table><tr>{th}</tr>{tb}</table>"


def _three():
    cols = [("5", "데이터 구조", "표 · 열 · 예"), ("6", "연동 대상", "외부 서비스 · 키 보관"), ("7", "권한", "누가 · 무엇을")]
    c = "".join(f'<div class="v2u4c" style="--d:{.3 + i * .9:.1f}s"><div class="h"><span>{n}</span><b>{t}</b><small>{sub}</small></div>{_mdtable(_sec(n))}</div>'
                for i, (n, t, sub) in enumerate(cols))
    return f'<div class="v2u4three">{c}</div>'


def _prdmap():
    old = [("1. 목표", "1부와 같음"), ("2. MVP 범위", "1부와 같음"), ("3. 기능 명세", "F1 ~ F6"), ("4. 화면별 요소", "로그인 화면 추가")]
    new = [("5. 데이터 구조", "표 · 열 · 연결"), ("6. 연동 대상", "외부 서비스 · 키 보관"), ("7. 권한", "누가 무엇을"), ("8. 완료 기준", "공유 · 권한 · 공휴일")]
    cells = "".join(f'<div><b>{h}</b><span>{s}</span></div>' for h, s in old)
    cells += "".join(f'<div class="{"new" if i < 3 else ""}" style="--d:{.6 + i * .6:.1f}s"><b>{h}</b><span>{s}</span></div>' for i, (h, s) in enumerate(new))
    return f'<div class="v2u4prd">{cells}</div>'


def slides():
    return [
        # ── 기본 흐름 · 양념
        light("기본 흐름", flow([("기획서", "왜 · 누구 · 무엇"), ("PRD", "만들 것 · 완료 기준"), ("구현", "Claude Code · 태스크 단위"),
                                ("배포", "GitHub → Vercel")])
              + viz2.pair("1부", [("흐름", "기획서 → PRD → 구현 → 배포"), ("저장", "내 브라우저")],
                          "2부", [("흐름", "같음"), ("추가", "DB · 로그인 · 외부 API · MCP")]), T),
        light("양념", shot("v2_u4_spice.webp", "같은 냄비 · 양념 두 병", [
            ("요리 순서", "기획서 → PRD → 구현 → 배포 · 그대로"), ("양념", "DB · 외부 API · MCP"),
            ("레시피에 추가", "PRD 에 세 칸 · 데이터 구조 · 연동 대상 · 권한")])
              + src(GEN), T),
        # ── 주제
        light("DB · 외부 연동 주제 예", viz2.maprows([
            ("팀 회의실 예약", "예약 · 로그인", "공휴일 API"),
            ("사내 도서 대여", "책 · 대여 기록", "도서 검색 API"),
            ("팀 점심 투표", "메뉴 · 투표", "—"),
            ("출장 경비 기록", "경비 · 영수증", "환율 API"),
            ("외근 일정표", "일정 · 담당자", "날씨 API")], "주제", "DB 에 저장 · 외부 연동")
              + note("공통점", "여러 사람이 같은 데이터를 보고 씀 · 외부 정보 하나"), T),
        light("주제 고르기 기준", viz2.tiles([
            ("여러 사람", "같은 화면 · 같은 데이터"), ("로그인", "누가 썼는지 구분"),
            ("외부 정보 하나", "공휴일 · 날씨 · 환율"), ("작게", "표 2~3개 · 화면 3~4개")], 4)
              + note("피할 것", "결제 · 실시간 채팅 · 파일 대량 업로드"), T),
        light("실습 주제 팀 회의실 예약", viz2.pair(
            "1부 회의실 예약", [("저장", "각자 브라우저 · localStorage"), ("예약자", "이름 칸에 아무나 입력"),
                            ("취소", "누구나 아무 예약"), ("공휴일", "구분 없음")],
            "2부 팀 회의실 예약", [("저장", "Supabase DB · 모두 같은 시간표"), ("예약자", "로그인 계정"),
                              ("취소", "내 예약만"), ("공휴일", "공휴일 API · 예약 차단")])
              + note("파일", "labs/room_booking_v2/예시/"), T),
        # ── 기획서 v2
        light("기획서 v2 변경 칸", viz2.maprows([
            ("배경", "1부 앱을 팀이 쓰기 시작", "예약은 각자 브라우저에만"), ("문제점", "공유 안 됨 · 남의 예약 취소", "공휴일에도 예약"),
            ("목표 이용자", "회사 이메일 로그인", "PC · 휴대폰"), ("화면 구성", "로그인 화면 추가", "공휴일 표시 · 내 예약 강조")], "칸", "v2 에서 바뀐 내용")
              + note("파일", "labs/room_booking_v2/예시/기획서.md"), T),
        light("소크라테스식 대화 예", chat([
            ("me", "1부 회의실 예약을 팀이 같이 쓰게 키우려고 해. 소크라테스식 대화로 진행해 줘"),
            ("ai", "지금 버전에서 팀원이 실제로 겪은 문제는 무엇인가요?"),
            ("me", "내가 한 예약이 팀원 휴대폰에서는 안 보여"),
            ("ai", "예약을 취소할 수 있는 사람은 누구여야 하나요?"),
            ("me", "예약한 본인만")], "Claude · 대화 예")
              + note("1-3 과 같은 방식", "질문 하나 · 내 답 · 다음 질문 · 답은 실제 장면"), T),
        # ── PRD v2
        light("PRD v2 추가 세 칸", _prdmap()
              + note("새 칸", "데이터 구조 · 연동 대상 · 권한 · 2-5 · 2-6 구현의 입력"), T),
        light("새 세 칸 예", _three()
              + note("파일", "labs/room_booking_v2/예시/PRD.md · 5 · 6 · 7 칸"), T),
        ba("확인 가능한 완료 기준 v2", T, "「예약이 공유된다」\n「보안이 된다」",
           "「내 노트북에서 한 예약이 팀원 휴대폰 시간표에도 보인다」\n「다른 사람 예약에는 취소 버튼이 없다」",
           "기기 · 사람 · 결과가 다 들어간 문장"),
        light("Claude Code와 PRD v2 만들기", flow([("기획서 v2", "소크라테스식 대화"), ("1부 PRD.md", "그대로 열기"), ("세 칸 추가 요청", "Claude Code"),
                                                ("빈 칸 질문", "키 보관 · 권한"), ("PRD v2", "파일 저장"), ("확인", "완료 기준 · 사람")], hl=2)
              + note("사람이 정할 것", "누가 무엇을 할 수 있나 · 어떤 외부 정보를 쓰나"), T),
        # ── 실습
        lab("2-4", "기획서 v2 · PRD v2", T, "내 1부 앱 → 기획서 v2 · PRD v2 · 데이터 구조 · 연동 대상 · 권한",
            ["1부 프로젝트 폴더를 VS Code로 열기", "Claude와 소크라테스식 대화 · 기획서 v2", "Claude Code에 PRD v2 요청", "세 칸 · 완료 기준 확인"],
            ["PRD 에 데이터 구조 · 연동 대상 · 권한 칸", "공유 · 권한 · 외부 연동 완료 기준 각 1개 이상"],
            files="예시/기획서.md · 예시/PRD.md (비교용)"),
        brief("2-4", T, ["1부 폴더 열기", "기획서 v2 · 소크라테스식 대화", "PRD v2 요청", "빈 칸 질문에 답하기", "PRD.md 확인"],
              [("목표", "PRD v2 · 세 칸 추가"), ("입력", "1부 PRD.md · 기획서 v2"), ("진행 방식", "정해지지 않은 것은 먼저 질문"),
               ("하지 말 것", "코드 작성 · 결제 · 실시간 채팅")],
              ["데이터 구조", "연동 대상", "권한", "완료 기준"],
              ["PRD.md 에 5 · 6 · 7 칸이 생김", "권한 표에 「내 예약만」 같은 줄"],
              "코드부터 만들기 시작하면 Esc 로 멈추고 「문서만」을 덧붙여 다시"),
        light("실습 2-4 확인", checks([
            ("표마다 열 이름 · 예가 있나", "2-5 표 만들기의 입력"), ("외부 서비스 키 보관 위치가 적혀 있나", "브라우저 · 서버"),
            ("로그인 전 · 후 권한이 나뉘어 있나", "보기 · 추가 · 취소"), ("완료 기준을 두 기기 · 두 계정으로 확인할 수 있나", "공유 · 권한")],
            "넷 다 「예」 → PRD v2 저장 · 2-5 구현의 입력"), T),
    ]
