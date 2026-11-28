"""2-3 기획 · 요구사항.

기본 흐름 복습(1부와 같음) → DB · 외부 연동 주제 예 → 실습 주제(미니 노션 v2)
→ 기획서 v2(기획자 페르소나) → 개발 계획 v2 에 늘어나는 세 칸(데이터 구조 · 연동 대상 · 권한) → 완료 기준 → 실습.
예시 문장은 labs/mini_notion_v2/예시/ 의 기획서.md · 개발계획.md 에서 그대로 읽는다. 산출물 개발 계획 v2 는 2-4 · 2-5 구현의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v2kit import brief, chat, shot

T = "2-3"
EX = Path(__file__).resolve().parent.parent / "labs" / "mini_notion_v2" / "예시"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def _prd():
    return (EX / "개발계획.md").read_text(encoding="utf-8").strip()


def _sec(no):
    """개발계획.md 의 「## no.」 칸을 제목 줄과 함께 그대로."""
    t = _prd()
    i = t.index(f"## {no}.")
    j = t.find("\n## ", i + 1)
    return t[i: j if j > 0 else None].strip()


CSS = """
  /* 2-3 · 개발 계획 칸 지도 */
  .v2u4prd{display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:8px 0 16px;}
  .v2u4prd div{border:1.5px solid #D9DDE3; border-radius:12px; background:#fff; padding:14px 16px; min-height:84px;}
  .v2u4prd div b{display:block; font-size:19px; color:#16233A;} .v2u4prd div span{font-size:14.5px; color:#6B7785;}
  .v2u4prd div.new{border-color:#F28C28; background:#FFF3E6; opacity:0; animation:v2u4pop .5s ease-out var(--d) forwards;}
  .v2u4prd div.new span{color:#E07A12; font-weight:700;}
  @keyframes v2u4pop{from{opacity:0; transform:translateY(14px) scale(.96)} to{opacity:1; transform:none}}
  /* 2-3 · 새 세 칸 예 */
  .v2u4three{display:grid; grid-template-columns:1.1fr 1.45fr .9fr; gap:14px; align-items:start;}
  .v2u4c{border:1.5px solid #F7C99A; border-radius:14px; background:#fff; overflow:hidden; opacity:0; animation:v2u4pop .55s ease-out var(--d) forwards;}
  .v2u4c .h{background:#FFF3E6; padding:10px 14px; display:flex; gap:8px; align-items:baseline; flex-wrap:wrap;}
  .v2u4c .h span{font-family:var(--mono); font-weight:800; color:#E07A12;} .v2u4c .h b{font-size:19px; color:#16233A;}
  .v2u4c .h small{font-size:13.5px; color:#6B7785;}
  .v2u4c table{border-collapse:collapse; width:100%;} .v2u4c th{background:#F4F6F9; font-size:13px; color:#3A4657; text-align:left; padding:6px 9px;}
  .v2u4c td{font-size:13.5px; color:#16233A; padding:6px 9px; border-top:1px solid #EEF0F3; line-height:1.4; vertical-align:top;}
  @media print{.v2u4prd div.new, .v2u4c{opacity:1; animation:none}}
"""


def _mdtable(sec):
    """개발 계획 칸의 마크다운 표 → 작은 HTML 표 (머리 줄 · 본문 줄)."""
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
        light("기본 흐름", flow([("기획서", "왜 · 누구 · 무엇"), ("개발 계획", "만들 것 · 완료 기준 · 태스크"), ("개발", "Claude Code · 태스크 단위"),
                                ("배포", "GitHub → Vercel")])
              + viz2.pair("1부", [("흐름", "기획서 → 개발 계획 → 개발 → 배포"), ("저장", "내 브라우저")],
                          "2부", [("흐름", "같음"), ("추가", "DB · 로그인 · 외부 API · MCP")]), T),
        # ── 주제
        light("2부 주제 예시", viz2.maprows([
            ("미니 노션", "페이지 · 로그인", "공휴일 API"),
            ("사내 도서 대여", "책 · 대여 기록", "도서 검색 API"),
            ("팀 점심 투표", "메뉴 · 투표", "—"),
            ("출장 경비 기록", "경비 · 영수증", "환율 API"),
            ("외근 일정표", "일정 · 작성자", "날씨 API")], "주제", "DB 에 저장 · 외부 연동")
              + note("공통점", "여러 사람이 같은 데이터를 보고 씀 · 외부 정보 하나"), T),
        light("주제 고르기 기준", viz2.tiles([
            ("여러 사람", "같은 화면 · 같은 데이터"), ("로그인", "누가 썼는지 구분"),
            ("외부 정보 하나", "공휴일 · 날씨 · 환율"), ("작게", "표 2~3개 · 화면 3~4개")], 4)
              + note("피할 것", "결제 · 실시간 채팅 · 파일 대량 업로드"), T),
        light("실습 주제 · 미니 노션 v2", viz2.pair(
            "시작 버전 · 미니 노션", [("저장", "공유 없음 · 나만 봄"), ("작성자", "아무 이름이나 선택"),
                             ("상태 변경 · 삭제", "누구나 아무 페이지"), ("날짜 공휴일", "구분 없음")],
            "2부 미니 노션 v2", [("저장", "Supabase DB · 모두 같은 페이지 목록"), ("만든 사람", "로그인 계정"),
                               ("상태 변경 · 삭제", "내가 작성자인 페이지만"), ("날짜 공휴일", "공휴일 API · 저장 차단")])
              + note("파일", "labs/mini_notion_v2/예시/"), T),
        # ── 기획서 v2
        light("기획서 v2 변경 사항", viz2.maprows([
            ("배경", "시작 버전을 팀이 쓰기 시작", "페이지 공유 없음 · 나만 봄"), ("문제점", "공유 안 됨 · 남의 페이지 삭제", "공휴일이 날짜로 들어감"),
            ("목표 이용자", "회사 이메일 로그인", "PC · 휴대폰"), ("화면 구성", "로그인 화면 추가", "공휴일 경고 · 내 페이지 강조")], "칸", "v2 에서 바뀐 내용")
              + note("파일", "labs/mini_notion_v2/예시/기획서.md"), T),
        light("기획자 페르소나 대화 예", chat([
            ("me", "/plan 기획자.md 페르소나로 미니 노션 시작 버전을 팀이 같이 쓰게 키우는 기획서 v2 를 쓰자"),
            ("ai", "지금 버전에서 팀원이 실제로 겪은 문제는 무엇인가요?"),
            ("me", "내가 추가한 페이지가 팀원 휴대폰에서는 안 보여"),
            ("ai", "페이지를 완료로 옮기거나 지울 수 있는 사람은 누구여야 하나요?"),
            ("me", "그 페이지의 작성자만")], "Claude Code · plan 모드 대화 예")
              + note("1-3 과 같은 방식", "기획자 페르소나 · 질문 하나씩 · 답은 실제 장면"), T),
        # ── 개발 계획 v2
        light("개발 계획 v2 추가 항목", _prdmap()
              + note("새 칸", "데이터 구조 · 연동 대상 · 권한 · 2-4 · 2-5 구현의 입력"), T),
        light("개발 계획 v2 추가 항목 예시", _three()
              + note("파일", "labs/mini_notion_v2/예시/개발계획.md · 데이터 구조 · 연동 대상 · 권한"), T),
        ba("확인 가능한 완료 기준 v2", T, "「페이지가 공유된다」\n「보안이 된다」",
           "「내 노트북에서 추가한 페이지가 팀원 휴대폰 목록에도 보인다」\n「다른 사람이 작성자인 페이지에는 삭제 버튼이 없다」",
           "기기 · 사람 · 결과가 다 들어간 문장"),
        light("Claude Code로 개발 계획 v2 세우기", flow([("plan 모드", "개발자 페르소나"), ("1부 계획", "개발계획.md · 기획서 v2"), ("세 칸 추가 요청", "데이터 · 연동 · 권한"),
                                                ("빈 칸 질문", "키 보관 · 권한"), ("승인", "개발계획.md v2 저장")], hl=2)
              + note("사람이 정할 것", "누가 무엇을 할 수 있나 · 어떤 외부 정보를 쓰나"), T),
        # ── 실습
        lab("2-3", "기획서 v2 · 개발 계획 v2", T, "내 1부 앱 → 기획서 v2 · 개발 계획 v2 · 데이터 구조 · 연동 대상 · 권한",
            ["1부 프로젝트 폴더를 VS Code로 열기", "기획자 페르소나로 기획서 v2", "개발자 페르소나로 개발 계획 v2", "세 칸 · 완료 기준 확인"],
            ["개발 계획에 데이터 구조 · 연동 대상 · 권한 칸", "공유 · 권한 · 외부 연동 완료 기준 각 1개 이상"],
            files="예시/기획서.md · 예시/개발계획.md (비교용)"),
        brief("2-3", T, ["1부 폴더 열기", "기획자 페르소나 · 기획서 v2", "개발자 페르소나 · 개발 계획 v2 요청", "빈 칸 질문에 답하기", "승인 → 개발계획.md 확인"],
              [("목표", "개발 계획 v2 · 세 칸 추가"), ("입력", "1부 개발계획.md · 기획서 v2"), ("진행 방식", "plan 모드 · 정해지지 않은 것은 먼저 질문"),
               ("하지 말 것", "코드 작성 · 결제 · 실시간 채팅")],
              ["데이터 구조", "연동 대상", "권한", "완료 기준"],
              ["개발계획.md 에 데이터 구조 · 연동 대상 · 권한이 생김", "권한 표에 「내가 작성자인 페이지만」 같은 줄"],
              "코드부터 만들기 시작하면 Esc 로 멈추고 「문서만」을 덧붙여 다시"),
        light("실습 2-3 확인", checks([
            ("표마다 열 이름 · 예가 있나", "2-4 표 만들기의 입력"), ("외부 서비스 키 보관 위치가 적혀 있나", "브라우저 · 서버"),
            ("로그인 전 · 후 권한이 나뉘어 있나", "보기 · 추가 · 취소"), ("완료 기준을 두 기기 · 두 계정으로 확인할 수 있나", "공유 · 권한")],
            "넷 다 「예」 → 개발 계획 v2 저장 · 2-4 개발의 입력"), T),
    ]
