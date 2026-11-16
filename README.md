# 바이브코딩 온라인 강의

슬라이드는 단원마다 HTML 한 파일이다(1280×720 · ← → 넘김 · PDF 인쇄).

| 1부 · 입문 | 3부 · 하네스 엔지니어링 |
|---|---|
| [1-1 바이브코딩이란](docs/1-1-vibe-coding.html) | [3-1 하네스 엔지니어링](docs/3-1-harness.html) |
| [1-2 도구 · 실습 환경](docs/1-2-setup.html) | [3-2 업무 분석 · 에이전트 설계](docs/3-2-agent-design.html) |
| [1-3 기획서 작성](docs/1-3-planning.html) | [3-3 MCP 연결](docs/3-3-mcp.html) |
| [1-4 요구사항 정의 (PRD)](docs/1-4-prd.html) | [3-4 CLAUDE.md](docs/3-4-claude-md.html) |
| [1-5 Git · GitHub 기초](docs/1-5-git.html) | [3-5 Skill 제작](docs/3-5-skill.html) |
| [1-6 바이브코딩 실습](docs/1-6-build.html) | [3-6 통제 · 안전장치](docs/3-6-guardrails.html) |
| [1-7 배포](docs/1-7-deploy.html) | [3-7 검증 루프](docs/3-7-verify.html) |
| [1-8 마무리](docs/1-8-wrap-up.html) | [3-8 운영하며 키우기](docs/3-8-operate.html) |

3부 합본: [docs/3-all.html](docs/3-all.html)

## 실습 자료

- `labs/room_booking` — 1부 공통 예제(회의실 예약 페이지): 기획서 · PRD · 완성 앱
- `labs/meeting_agent` — 3부 실습(회의록 에이전트)

## 빌드

```
python3 src/build.py          # 전체
python3 src/build.py part1    # 1부만 (P1_ONLY=3,6 으로 일부 단원만)
python3 src/build.py part3    # 3부만
```
