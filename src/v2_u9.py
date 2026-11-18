"""2-9 마무리 (10분).

2부 회고(요청 = 결과 ? · 1-8 과 같은 구조) → 1부 앱 → 2부 앱 비교(1-8 한계가 풀린 모습) → 결과 공유 · 회고 질문
→ 운영 체크리스트(카드 8칸) → 내 회고 기록 → 3부 연결.
1-8 과 겹치지 않게: 1부 회고 질문 · 공유 항목을 다시 설명하지 않고 2부에서 더해진 것(데이터 · 키 · 테스트 · 로그)만.
사실 출처: supabase.com/docs/guides/platform/free-project-pausing (무료 프로젝트 1주 비활성 시 일시 중지)
· vercel.com/docs/instant-rollback · vercel.com/docs/logs/runtime
"""
import viz2
from deck import flow, light
from hx import code, esc, note, table
from stats_hx import src

T = "2-9"


def slides():
    return [
        light("2부 회고", '<div class="v2u9q"><span>내 요청</span><i>=</i><span>결과</span><em>?</em></div>'
              + flow([("PRD v2", "2-4 · 데이터 · 권한"), ("DB · 로그인", "2-5 · Supabase"), ("API · MCP", "2-6 · 공휴일"),
                      ("테스트 · 리뷰", "2-7 · 자동 확인"), ("환경변수 · 로그", "2-8 · 배포 뒤")], hl=-1)
              + note("흐름", "1부와 같은 순서 · 데이터 · 외부 연결 · 검사가 더해짐"), T),
        light("1부 앱 → 2부 앱", viz2.maprows([
            ("예약 저장 · 브라우저마다 따로", "Supabase 한 곳", "팀원 모두 같은 시간표"),
            ("수정 · 삭제 · 누구나", "로그인 · 내 예약만", "RLS 권한"),
            ("공휴일 · 달력 직접 확인", "공휴일 API", "공휴일 예약 자동 차단"),
            ("확인 · 기능마다 직접 클릭", "자동 테스트 · 브라우저 MCP", "push 전 전체 검사"),
            ("장애 · 사용자 제보", "로그 · Web Analytics", "에러 · 방문 기록")], "1부 (1-8 한계)", "2부"), T),
        light("결과 공유", viz2.tiles([
            ("배포 주소", "프로젝트명.vercel.app"), ("붙인 것", "DB · 로그인 · API · MCP"),
            ("테스트", "통과 수 / 전체"), ("가장 오래 걸린 곳", "에러가 많았던 기능")], 4)
              + code("공유 글 · 예", esc("팀 회의실 예약 · https://room-booking.vercel.app\n"
                                       "로그인 · 팀원 모두 같은 시간표 · 공휴일 예약 차단\n"
                                       "테스트 8개 통과 · 가장 오래 걸린 곳: 권한(RLS) 설정")), T),
        light("운영 체크리스트", '<div class="v2u9ck">' + "".join(
            f'<div style="--d:{i * .07:.2f}s"><b>{h}</b><span>{x}</span></div>' for i, (h, x) in enumerate([
                ("키", "코드 · GitHub 에 키 없음 · .env 는 .gitignore"), ("환경변수", "Vercel 에 등록 · 바꾸면 Redeploy"),
                ("권한", "RLS 켜짐 · 남의 예약 수정 · 삭제 불가"), ("테스트", "push 전 전체 통과"),
                ("로그", "배포 직후 Live 확인 · Hobby 1시간 보관"), ("방문 기록", "주 1회 Analytics 확인"),
                ("되돌리기", "Instant Rollback · 직전 배포"), ("Supabase 무료", "1주 비활성 시 일시 중지 · 대시보드에서 재시작")]))
              + "</div>"
              + src(("Supabase · Project Pausing", "https://supabase.com/docs/guides/platform/free-project-pausing"),
                    ("Vercel · Instant Rollback", "https://vercel.com/docs/instant-rollback")), T),
        light("내 회고 기록", table(["질문", "내 답"], [
            ["테스트 통과", "  개 중   개"], ["데이터 구조에서 바뀐 것", ""], ["테스트 · 점검이 잡아낸 버그", ""],
            ["배포 뒤 로그에서 본 에러", ""], ["3부에서 맡기고 싶은 반복 업무", ""]])
              + note("기록", "PRD.md v2 맨 아래 「회고」 칸 · 3부 업무 분석의 입력"), T),
        light("2부 → 3부", viz2.pair(
            "2부", [("만든 것", "팀이 쓰는 웹 서비스"), ("AI 역할", "코드 작성 · 테스트 · 리뷰"), ("사람 역할", "기획 · 기준 · 확인")],
            "3부", [("만들 것", "내 반복 업무를 맡을 에이전트"), ("핵심", "하네스 · 규칙 · 스킬 · 안전장치"), ("이어지는 것", "MCP · 테스트 · 검증")], hl="r"), T),
    ]


CSS = """
  /* 2-9 · 요청 = 결과 ? */
  .v2u9q{display:flex; justify-content:center; align-items:center; gap:18px; margin:0 0 22px; padding:18px; border-radius:16px; background:#FFF8F0; border:2px solid #F28C28;}
  .v2u9q span{font-size:26px; font-weight:800; color:#16233A; padding:8px 22px; border-radius:12px; background:#fff; border:2px solid #D9DDE3;}
  .v2u9q i, .v2u9q em{font-style:normal; font-size:30px; font-weight:900; color:#F28C28;}
  /* 2-9 · 운영 체크리스트 카드 8칸 */
  .v2u9ck{display:grid; grid-template-columns:repeat(4,1fr); gap:14px;}
  .v2u9ck div{position:relative; border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:16px 16px 16px 46px; min-height:118px;
              opacity:0; animation:v2u9in .4s ease-out var(--d) forwards;}
  .v2u9ck div::before{content:"☐"; position:absolute; left:14px; top:13px; font-size:24px; color:#F28C28;}
  .v2u9ck b{display:block; font-size:21px; color:#16233A;} .v2u9ck span{display:block; margin-top:6px; font-size:16px; line-height:1.45; color:#3A4657;}
  @keyframes v2u9in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u9ck div{opacity:1; animation:none}}
"""
