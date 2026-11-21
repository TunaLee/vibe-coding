"""1-8 마무리.

1부 회고(요청 = 결과 ? · 1-1 「1부의 핵심」과 이어짐) → 결과 공유 · 회고 질문 → 저장 위치 → 한계별 2부 단원 → 2부 지도.
2부 목차: 노션 「바이브코딩 온라인 강의 커리큘럼」 2. 바이브 코딩 심화 (2-1 ~ 2-9).
"""
import viz2
from deck import flow, light
from hx import code, esc, note, table
from stats_hx import src
from v1kit import shot

T = "1-8"


def slides():
    return [
        light("1부 회고", '<div class="v1u8q"><span>내 요청</span><i>=</i><span>결과</span><em>?</em></div>'
              + flow([("기획서.md", "무엇을 · 누구를 (1-3)"), ("개발계획.md", "기능 · 태스크 (1-4)"), ("커밋 기록", "되돌릴 지점 (1-5)"),
                      ("동작하는 앱", "작게 요청 · 확인 (1-6)"), ("배포 주소", "점검 · 공유 (1-7)")], hl=-1)
              + note("다섯 단계", "요청과 결과의 차이를 줄이는 순서 · 2부에서도 같음")
              + src(("참고 · 혼잡스 「바이브코딩 한 장 지도」 아이디어 → 코드 → 배포 → 서비스", "https://www.youtube.com/watch?v=HNtS6WGGhNU")), T),
        light("결과 공유", viz2.tiles([
            ("배포 주소", "프로젝트명.vercel.app"), ("한 줄 소개", "기획서의 서비스 컨셉"),
            ("완료 기준", "완료 기준 통과 수"), ("가장 오래 걸린 곳", "다시 요청이 많았던 기능")], 4)
              + code("공유 글 · 예", esc("미니 노션 · https://mini-notion.vercel.app\n페이지마다 블록으로 쓰는 메모장 · 할 일은 체크 상자\n완료 기준 5개 중 5개 · 블록 끌어 옮기기에서 요청 3번")), T),
        light("회고 질문", viz2.tiles([
            ("요청과 결과가 달랐던 곳", "첫 요청에 빠져 있던 말"), ("기획서와 달라진 것", "만들면서 빼거나 더한 기능"),
            ("되돌린 적", "커밋으로 돌아간 순간"), ("다음에 붙일 것", "쓰다 보니 아쉬운 기능")], 2)
              + note("기록", "개발계획.md 맨 아래 「회고」 칸 · 2부 기획의 입력"), T),
        # ── 한계 → 2부
        light("데이터 저장 위치 · localStorage", '<div class="v1u8s">' + shot("notion_fresh.webp", "같은 주소 · 팀원 브라우저에서 연 화면 — 「주간 회의록」 없음", [
            ("저장 위치", "localStorage · 각 브라우저 안"), ("내 노트북", "주간 회의록 · 아이디어 메모"), ("팀원 휴대폰", "「시작하기」 한 장")]) + "</div>"
              + note("필요한 것", "모두가 같은 곳에 쓰고 읽는 저장소 = 데이터베이스 (2-2 · 2-5)"), T),
        light("1부의 한계와 2부", viz2.maprows([
            ("페이지 공유 불가 · 브라우저마다 따로 저장", "데이터베이스 (Supabase)", "2-2 · 2-5"),
            ("다른 서비스와 따로 · 날짜 · 캘린더 정보 직접 확인", "외부 API · MCP", "2-3 · 2-6"),
            ("수동 오류 확인 · 기능마다 직접 클릭", "테스트 · 디버깅", "2-7"),
            ("운영 상태 확인 불가 · 사용자 제보에 의존", "모니터링 · 로그", "2-8")], "예제 앱의 한계", "2부")
              + note("2부 공통 예제", "팀 할 일 보드 · 여럿이 함께 쓰는 앱으로 같은 순서를 한 번 더"), T),
        light("2부 커리큘럼", viz2.tiles([
            ("2-1 미리보기", "DB · MCP 개요"), ("2-2 데이터베이스", "표 · 행 · 열 · Supabase"), ("2-3 MCP", "API 와 MCP"),
            ("2-4 기획 · 요구사항", "개발 계획에 데이터 · 연동 · 권한"), ("2-5 데이터 다루기", "저장 · 조회 · 로그인"), ("2-6 외부 서비스", "API 키 · MCP"),
            ("2-7 품질 관리", "테스트 · 디버깅"), ("2-8 배포 · 모니터링", "환경변수 · 로그"), ("2-9 마무리", "운영 체크리스트")], 3), T),
        light("회고 기록", table(["질문", "내 답"], [
            ["배포 주소", ""], ["완료 기준 통과", "  개 중   개"], ["요청과 결과가 달랐던 곳", ""], ["기획서와 달라진 것", ""], ["2부에서 붙이고 싶은 것", ""]])
              + note("가져갈 것", "이 표 · 기획서.md · 개발계획.md → 2-4 기획의 입력"), T),
    ]


CSS = """
  /* v1 · 1-8 화면 캡처 높이 (메모가 내비 바에 걸리지 않게) */
  .v1u8s .v1shot img{max-height:340px;}
  /* 1-8 · 요청 = 결과 ? */
  .v1u8q{display:flex; justify-content:center; align-items:center; gap:18px; margin:0 0 22px; padding:18px; border-radius:16px; background:#FFF8F0; border:2px solid #F28C28;}
  .v1u8q span{font-size:26px; font-weight:800; color:#16233A; padding:8px 22px; border-radius:12px; background:#fff; border:2px solid #D9DDE3;}
  .v1u8q i{font-style:normal; font-size:30px; font-weight:900; color:#F28C28;} .v1u8q em{font-style:normal; font-size:30px; font-weight:900; color:#F28C28;}
"""
