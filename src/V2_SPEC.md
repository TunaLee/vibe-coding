# 2부 공통 결정 (단원 모듈 작성자용 · 덱에 나오지 않음)

## 공통 예제 — 팀 할 일 보드 v2 (labs/team_board_v2)
1부 앱(labs/team_board/예시/app · 정적 HTML/JS · localStorage)을 이어서 키운다. 빌드업: 1-2 개인 할 일 목록 → 1부 팀 할 일 보드 → 2부 v2 → 3부 회의록 에이전트가 보드에 할 일을 올림.
- 2-5 DB: Supabase · 할 일을 모두가 같은 곳에 저장 (1-8 「팀원 휴대폰에서 빈 보드」 문제 해결)
  - 표 members(id → auth.users, name, email) · tasks(id, title, owner_id → members, due, status, created_by → auth.users, created_at)
  - 로그인: Supabase Auth 이메일 · 권한(RLS): 모두 읽기 · 로그인한 사람은 추가 · 상태 변경/삭제는 내가 담당인 할 일만
  - 브라우저에 두는 키 = publishable(anon) 키 (RLS 로 보호) · secret(service_role) 키는 절대 브라우저 · 코드 금지
- 2-6 외부 API: 공공데이터포털 「한국천문연구원_특일 정보」 공휴일 조회 → 기한이 공휴일이면 「공휴일 · 이름」 경고 · 저장 막기
  - 서비스 키는 .env → Vercel 서버 함수(api/holidays.js)에서만 사용 · .gitignore 에 .env
- 2-6 MCP: Claude Code 에 Supabase MCP 연결(표 만들기 · 조회를 말로) · 2-7 에서 브라우저 MCP(Playwright)로 화면 테스트
- 2-7: 테스트(기한 지남 판정 · 공휴일 차단 · 남의 할 일 삭제 불가) · 디버깅(재현 → 에러 · 로그 전달 → 수정 → 재테스트) · /review · /security-review
- 2-8: Vercel 환경변수 · Vercel 로그 · Vercel Web Analytics · 문제 대응 = 2-7 흐름 + push 재배포
- 2-9: 결과 공유 · 회고 · 운영 체크리스트 · 3부 회의록 에이전트로 연결

## 이어지는 장치
- 2-4 에 「기본 흐름(기획서 → PRD → 구현 → 배포)은 그대로 · DB · MCP 는 양념」
- PRD v2 에 추가하는 칸: 데이터 구조 · 연동 대상 · 권한

## 규격
- 모듈 src/v2_uN.py · slides() · CSS(접두어 v2uN) · from v2kit import brief, chat, shot, codemap · T = "2-N"
- 빌드 python3 src/build.py (docs/part2.html) · lint ~/.claude/skills/lecture-deck/scripts/lint.py
- 그림: ~/Workspace/ai-gen/queue.tsv 에 「v2_uN_이름<TAB>프롬프트<TAB>2부-그림」 줄 추가 (genq.sh 가 순서대로 생성)
  - 고른 그림 → docs/img/v2_uN_이름.webp 800×450 q82 · 캡션 아래 출처 「AI 생성 그림 · Z-Image Turbo (Apache 2.0)」
- 사실 · 숫자 · 명령은 공식 문서(2026) 링크를 장 아래 src(...) 로
