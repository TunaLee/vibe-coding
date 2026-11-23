"""1-4 개발 계획.

기획서만 넘겼을 때 → 비유(조감도 · 설계 도면 · 공정표) → 개발 계획 정의 · 기획서와 차이 · 구성 → MVP → 칸 한 장씩 → 태스크
→ 개발자 페르소나 · plan 모드로 세우기 → 실습.
입력 = 1-3 산출물 기획서.md · 예시 문장은 labs/mini_notion/예시/개발계획.md 에서 그대로 읽는다. 산출물 개발계획.md 는 1-6 개발의 입력.
"""
from pathlib import Path

import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import brief, chat, labcard, tstep
from v3kit import phmap

GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")

T = "1-4"
EX = Path(__file__).resolve().parent.parent / "labs" / "mini_notion" / "예시"
PERSONA = Path(__file__).resolve().parent.parent / "labs" / "persona"


def _persona(who):
    """페르소나 파일 전체 — 수강생이 그대로 따라 쓸 다섯 줄."""
    return (PERSONA / f"{who}.md").read_text(encoding="utf-8").strip()


def _prd():
    return (EX / "개발계획.md").read_text(encoding="utf-8").strip()


def _sec(no):
    """개발계획.md 의 「## no.」 칸을 제목 줄과 함께 그대로."""
    t = _prd()
    i = t.index(f"## {no}.")
    j = t.find("\n## ", i + 1)
    return t[i: j if j > 0 else None].strip()


def _line(no, key):
    """개발계획.md 의 「## no.」 칸에서 key 가 든 줄 하나."""
    import re
    x = next(x for x in _sec(no).split("\n") if key in x).strip()
    x = re.sub(r"^- (\[ \] )?", "", x)                       # 목록 · 체크 상자 기호
    return " · ".join(c.strip() for c in x.strip("|").split("|")) if x.startswith("|") else x


def _cards(items):
    """개발 계획 칸별 예 — (칸 이름, 개발계획.md 의 실제 한 줄, 한 줄 설명)."""
    c = "".join(f'<div class="v1px"><b>{h}</b><span class="v1pl">{esc(line)}</span><span>{sub}</span></div>' for h, line, sub in items)
    return f'<div class="v1pxs">{c}</div>'


CSS = """
  /* 1-4 · 개발 계획 칸별 예 */
  .v1pxs{display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:6px;}
  .v1px{border:1.5px solid #D9DDE3; border-radius:14px; background:#fff; padding:16px 18px; display:flex; flex-direction:column; gap:8px;}
  .v1px b{font-size:20px; color:#16233A;}
  .v1px .v1pl{display:block; font-family:inherit; font-weight:600; font-size:15.5px; color:#1F3A5F; background:#F4F6F9; border-radius:8px; padding:9px 12px; white-space:pre-wrap; letter-spacing:0; font-variant-ligatures:none;}
  .v1px > span:last-child{font-size:15.5px; color:#3A4657;}
"""


def slides():
    return [
        # ── 배경 → 비유
        light("기획서만으로는 부족한 이유", viz2.maprows([
            ("공유", "넣을지 뺄지", "기획서는 「하지 않을 것」에만 한 줄"),
            ("블록 종류", "몇 가지 · 무엇", "기획서에 「블록」만 한 단어"),
            ("저장 위치", "서버 DB · 내 브라우저", "기획서에 없음"),
            ("만들 순서", "어느 화면부터", "기획서에 없음"),
            ("완성 범위", "어디까지 만들면 끝인지", "기준 없음")], "Claude Code가 정할 것", "기획서에 있는 것")
              + note("빈 칸", "Claude Code가 추측으로 채움 · 대화마다 다른 결과"), T),
        light("AI가 추측으로 채운 결과", viz2.pair(
            "기획서만 · 예", [("블록", "표 · 이미지 · 코드까지 열 가지"), ("「/」 메뉴", "없음 · 버튼으로만 추가"), ("저장", "서버를 새로 만들려 함")],
            "개발 계획과 함께 · 예", [("블록", "제목 · 글 · 체크 상자 · 구분선"), ("「/」 메뉴", "빈 블록에 「/」 → 메뉴"), ("저장", "브라우저 localStorage")])
              + note("예", "같은 기획서로도 결과가 달라지는 지점 · 실제 결과는 대화마다 다름"), T),
        light("조감도와 설계 도면", phmap("v1_u4_blueprint.webp", "조감도와 설계 도면", *GEN, viz2.maprows([
                  ("조감도", "기획서", "어떤 집인지 · 왜"), ("설계 도면", "개발 계획", "기능 · 화면 · 데이터"),
                  ("공정표", "태스크", "무엇부터 짓나"), ("준공 검사", "완료 기준", "도면대로 지었나")], "집 짓기", "앱 만들기")), T),
        # ── 개발 계획
        light("개발 계획", viz2.tiles([
            ("만들 것", "기능 · 화면 · 데이터"), ("범위", "MVP 포함 · 제외"), ("완료 기준", "확인할 수 있는 문장"),
            ("태스크", "만들 순서 · 한 번에 하나")], 4)
              + note("현업 문서", "PRD (제품 요구사항 문서) + 개발 일정 · 1부는 한 파일 개발계획.md"), T),
        light("기획서와 개발 계획", viz2.pair(
            "기획서", [("목적", "왜 만드는지 정리"), ("함께 쓰는 페르소나", "기획자"), ("내용", "배경 · 문제점 · 이용자 · 컨셉 · 화면")],
            "개발 계획", [("목적", "무엇을 · 어떤 순서로 만들지 확정"), ("함께 쓰는 페르소나", "개발자"), ("내용", "기능 · 화면 요소 · 데이터 · 완료 기준 · 태스크")]), T),
        light("개발 계획 구성", flow([("목표", "한 문장"), ("MVP 범위", "포함 · 제외"), ("기능", "F1 ~ F5"),
                                  ("화면", "요소 · 데이터"), ("완료 기준", "확인할 문장"), ("태스크", "T1 ~ T6")], hl=5)
              + note("파일", "개발계획.md · 칸마다 「## 번호. 제목」"), T),
        light("기획서.md → 개발계획.md", viz2.maprows([
            ("서비스 컨셉", "1. 목표 · 3. 기능 명세", "한 문장 → 기능 F1~F5"),
            ("화면 구성", "4. 화면별 요소", "화면 이름 → 화면마다 보이는 것"),
            ("이번에 하지 않을 것", "2. MVP 범위 · 제외", "공유 · 로그인 · 이미지 · 데이터베이스 표"),
            ("문제점", "6. 완료 기준", "「할 일이 글 사이에 묻힘」 → 「체크 상자 추가 후 새로고침해도 남음」")], "기획서.md", "개발계획.md")
              + note("새로 정하는 것", "5. 데이터 항목 · 저장 위치 · 7. 태스크 순서"), T),
        # ── MVP
        light("개발 계획 작성 예시", _cards([
            ("기능 명세", _line("3", "F3"), "번호 = 태스크와 연결 · 한 줄에 기능 하나"),
            ("데이터 항목", _line("5", "블록 종류"), "저장할 값마다 실제 예 하나 · 저장 위치"),
            ("완료 기준", _line("6", "「/」"), "체크 상자 · 브라우저에서 직접 확인"),
            ("태스크", _line("7", "T3"), "끝나면 보이는 화면 · 만들 순서")])
              + note("파일", "labs/mini_notion/예시/개발계획.md"), T),
        ba("확인 가능한 완료 기준", T, "「메모가 잘 저장된다」\n「블록을 쉽게 바꾼다」",
           "「주간 회의록에 체크 상자 「보고서 초안」 추가 후 새로고침해도 남아 있다」\n「빈 블록에 「/」 → 「체크 상자」 고르면 체크 상자로 바뀐다」",
           "값 · 동작 · 결과가 다 들어간 문장"),
        # ── 태스크
        light("태스크", viz2.maprows([
            ("T1 화면 뼈대 · 페이지 목록", "F1", "왼쪽 목록 · 새 페이지 · 삭제"), ("T2 블록 편집", "F2", "엔터로 새 블록 · 체크 상자 체크"),
            ("T3 「/」 메뉴", "F3", "「/」 → 메뉴 → 블록 종류 바뀜"), ("T4 블록 끌어 옮기기", "F4", "손잡이로 순서 바뀜"),
            ("T5 저장", "F5", "새로고침 뒤 그대로"), ("T6 완료 기준 점검", "6", "모바일 폭 · 다섯 줄 모두 ✓")], "태스크", "기능 하나 = 태스크 하나"), T),
        # ── 개발자 페르소나 · plan 모드
        light("개발자 페르소나", '<div class="twocol"><div>' + code("개발자.md", esc(_persona("개발자")))
              + '</div><div>' + viz2.tiles([("만들기", "기획자.md 옆에 새 파일 · 다섯 줄"), ("기획자.md 와 차이", "역할 · 마지막 줄 칸"),
                                          ("둘째 줄", "기획서에 없는 것은 먼저 질문")], 1) + "</div></div>", T),
        light("개발 계획 대화 예시", chat([
            ("me", "개발자.md 대로 기획서.md 를 읽고 개발 계획을 세워 줘"),
            ("ai", "블록 종류는 몇 가지로 할까요? 페이지는 어디에 저장할까요?\n저장 위치 · 서버 또는 내 브라우저 (서버는 로그인 필요)"),
            ("me", "제목 · 글 · 체크 상자 · 구분선 네 가지 · 내 브라우저에 저장"),
            ("ai", "계획: 기능 F1~F5 · 태스크 T1~T6 · 완료 기준 5개\n승인하면 개발계획.md 로 저장한다.")], "Plan Mode 대화 예"), T),
        # ── 실습
        labcard("1-4", "기획서로 개발 계획 세우기", T, "기획서.md", "개발계획.md", ["개발자 페르소나", "Plan Mode"]),
        brief("1-4", T, ["개발자.md 만들기", "모드 표시 → Plan", "「개발자.md 대로 개발 계획 세워 줘」", "질문에 답하기 · 피드백", "승인 → 개발계획.md"],
              [("목표", "개발계획.md · 일곱 칸"), ("입력", "기획서.md · 개발자.md"), ("진행 방식", "Plan Mode · 질문에 답하기"),
               ("하지 말 것", "코드 작성")],
              ["개발자 페르소나", "MVP", "완료 기준", "태스크"],
              ["개발계획.md 파일이 생김", "태스크마다 끝나면 보이는 화면이 적힘"],
              "계획이 너무 길면 「태스크를 여섯 개 안으로 줄여 줘」"),
        tstep("1-4", 1, "개발자.md 만들기", T, term=("mini_notion/개발자.md", _persona("개발자")),
              rows=[("만들기", "VS Code 탐색기 → 새 파일 → 개발자.md"), ("쓰기", "다섯 줄 · 경력 · 말투는 바꿔도 됨"), ("저장", "macOS ⌘S · Windows Ctrl+S")]),
        tstep("1-4", 2, "Plan Mode 요청 · 질문", T, "lab14_q1.webp", "개발자 페르소나의 선택 질문",
              rows=[("Plan Mode", "모드 표시 → Plan · 1-3 과 같음"), ("질문", "저장 방식 · 기술 · 기획서에 없던 것"), ("1부 선택", "순수 HTML/JS · localStorage")]),
        tstep("1-4", 3, "계획에 피드백", T, "lab14_feedback.webp", "3번 고칠 점 적기",
              rows=[("3번", "Tell Claude what to change"), ("피드백", "정렬 순서 · 파일 이름"), ("다시", "고친 계획 → 승인")]),
        tstep("1-4", 4, "개발계획.md 저장", T, "lab14_saved.webp", "개발계획.md 저장 결과",
              rows=[("결과", "개발계획.md · F 번호 · T 번호"), ("반영", "피드백 두 가지"), ("코드", "아직 없음")]),
        light("실습 1-4 확인", checks([
            ("기획서의 「하지 않을 것」이 제외 칸에 있나", "없으면 추가 요청"), ("태스크마다 F 번호가 있나", "기능 하나 = 태스크 하나"),
            ("저장 위치가 적혀 있나", "MVP 는 내 브라우저"), ("완료 기준을 눌러서 확인할 수 있나", "값 · 동작 · 결과")],
            "넷 다 「예」 → 개발계획.md 저장"), T),
    ]
