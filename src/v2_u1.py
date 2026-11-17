"""2-1 미리보기.

1부 앱과 2부 앱 → DB · API · MCP 의 위치(앱이 쓰는 것 · 만들 때 쓰는 것) → 2부 도구 → 2부 산출물 흐름.
2부 목차: 노션 「바이브코딩 온라인 강의 커리큘럼」 2. 바이브 코딩 심화 (2-1 ~ 2-9).
"""
import viz2
from deck import flow, light
from hx import note

T = "2-1"


def _lane(head, sub, boxes, d0):
    """한 줄 — 머리 칸 + 상자 → 상자 … · 상자가 차례로 나타남."""
    out = []
    for i, (b, s, hl) in enumerate(boxes):
        d = d0 + i * .45
        if i:
            out.append(f'<i class="v2u1ar" style="--d:{d - .2:.2f}s">→</i>')
        out.append(f'<div class="v2u1bx{" hl" if hl else ""}" style="--d:{d:.2f}s"><b>{b}</b><span>{s}</span></div>')
    return f'<div class="v2u1ln"><div class="v2u1hd"><b>{head}</b><span>{sub}</span></div><div class="v2u1row">{"".join(out)}</div></div>'


def where():
    return ('<div class="v2u1map">'
            + _lane("앱이 쓰는 것", "배포한 뒤 · 이용자가 쓸 때", [
                ("이용자 브라우저", "예약 화면", False), ("내 앱", "Vercel", False),
                ("데이터베이스", "Supabase · 예약 저장", True), ("외부 API", "공휴일 정보", True)], .3)
            + _lane("만들 때 쓰는 것", "개발 중 · 내 컴퓨터", [
                ("나", "말로 요청", False), ("Claude Code", "코드 작성", False),
                ("MCP", "연결 규격", True), ("Supabase · 브라우저", "표 만들기 · 화면 눌러 보기", False)], 2.3)
            + "</div>")


def slides():
    return [
        light("1부 앱과 2부 앱", viz2.pair(
            "1부 · 회의실 예약", [("저장 위치", "내 브라우저 안 · localStorage"), ("이용자", "누구나 · 이름만 입력"),
                               ("공휴일", "직접 달력 확인"), ("확인 방법", "기능마다 직접 클릭")],
            "2부 · 팀 회의실 예약", [("저장 위치", "데이터베이스 · 팀 전체가 같은 곳"), ("이용자", "로그인 · 내 예약만 취소"),
                                 ("공휴일", "외부 API · 자동 표시"), ("확인 방법", "테스트 · 로그")])
              + note("이어서 만들기", "1부 PRD · 코드 · 배포 주소를 그대로 씀"), T),
        light("DB · API · MCP의 위치", where()
              + note("구분", "DB · API 는 앱 안의 부품 · MCP 는 Claude Code 의 연결 통로"), T),
        light("2부 도구", viz2.tiles([
            ("Supabase", "데이터베이스 · 로그인 (2-2 · 2-5)"), ("공공데이터포털", "공휴일 API · 서비스 키 (2-6)"),
            ("MCP", "Claude Code ↔ Supabase · 브라우저 (2-3 · 2-6 · 2-7)"), ("GitHub · Vercel", "1부 연결 그대로 · 환경변수 · 로그 (2-8)")], 2), T),
        light("2부 산출물 흐름", flow([
            ("기획서 · PRD v2", "데이터 · 연동 · 권한 (2-4)"), ("DB 저장 · 로그인", "Supabase (2-5)"), ("공휴일 API · MCP", "키 보관 (2-6)"),
            ("테스트 · 수정", "품질 관리 (2-7)"), ("배포 · 로그", "모니터링 (2-8)")], hl=1)
              + note("기본 흐름", "기획서 → PRD → 구현 → 배포 · 1부와 같은 순서"), T),
    ]


CSS = """
  /* 2-1 · DB · API · MCP 위치 */
  .v2u1map{display:flex; flex-direction:column; gap:22px; margin:6px 0 18px;}
  .v2u1ln{display:grid; grid-template-columns:170px 1fr; gap:18px; align-items:center;}
  .v2u1hd b{display:block; font-size:21px; color:#16233A;} .v2u1hd span{font-size:14px; color:#6B7785;}
  .v2u1row{display:flex; align-items:center; gap:10px;}
  .v2u1bx{flex:1; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:14px 14px; min-height:92px;
    opacity:0; animation:v2u1in .5s ease-out var(--d) forwards;}
  .v2u1bx b{display:block; font-size:19px; color:#16233A;} .v2u1bx span{font-size:14.5px; color:#3A4657; line-height:1.4;}
  .v2u1bx.hl{border-color:#F28C28; background:#FFF3E6;} .v2u1bx.hl b{color:#E07A12;}
  .v2u1ar{font-style:normal; font-size:24px; font-weight:800; color:#F28C28; opacity:0; animation:v2u1in .3s ease-out var(--d) forwards;}
  @keyframes v2u1in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u1bx,.v2u1ar{opacity:1; animation:none}}
"""
