# 바이브코딩 온라인 강의

슬라이드는 1부 · 2부 · 3부 전체가 HTML 한 파일이다 — [docs/index.html](docs/index.html) (1280×720 · ← → 넘김 · 숫자+Enter 이동 · ≡ 목차 · PDF 인쇄).
두 번째 장 「과정 지도」에서 단원을 누르면 그 단원 표지로 이동한다.

## 실습 자료

- `labs/room_booking` — 1부 공통 예제(회의실 예약 페이지): 기획서 · PRD · 완성 앱
- `labs/meeting_agent` — 3부 실습(회의록 에이전트)

## 빌드

```
python3 src/build.py          # docs/index.html 한 파일
python3 ~/.claude/skills/lecture-deck/scripts/lint.py docs/index.html
```
