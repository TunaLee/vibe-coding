# 바이브코딩 온라인 강의

슬라이드는 부마다 HTML 한 파일이다(1280×720 · ← → 넘김 · 숫자+Enter 이동 · ≡ 목차 · PDF 인쇄).

| 파일 | 내용 |
|---|---|
| [docs/part1.html](docs/part1.html) | 1부 바이브코딩 입문 · 1-1 ~ 1-8 |
| [docs/part2.html](docs/part2.html) | 2부 바이브코딩 심화 · 2-1 ~ 2-9 |
| [docs/part3.html](docs/part3.html) | 3부 하네스 엔지니어링 · 3-1 ~ 3-8 |

[docs/index.html](docs/index.html) 은 단원 목록 — `part1.html#u-1-3` 처럼 단원 표지로 바로 열린다.

## 실습 자료

- `labs/delegate_todo` — 1-2 첫 위임 · 개인 할 일 목록 뼈대
- `labs/team_board` — 1부 공통 예제(팀 할 일 보드): 기획서 · PRD · 완성 앱
- `labs/team_board_v2` — 2부 공통 예제(DB · 로그인 · 공휴일 API · MCP): 기획서 v2 · PRD v2
- `labs/meeting_agent` — 3부 실습(회의록 에이전트)

## 빌드

```
python3 src/build.py          # docs/part1~3.html + index.html
python3 ~/.claude/skills/lecture-deck/scripts/lint.py docs/part1.html
```
