"""1-6 바이브코딩 실습 (40분).

권한 모드 → 개발계획.md(1-4)의 태스크 단위 진행 → 서버(비유: 식당 주방) → 태스크별 화면 → 수정 · 되돌리기 → 실습.
공통 예제: labs/mini_notion/예시 (개발계획.md F1~F5 · T1~T6 · 완성본 app/). Git 개념은 1-5 에서 · 여기서는 「커밋해 줘 · 되돌려 줘」로만.
사실 출처: code.claude.com/docs/en/permission-modes · code.claude.com/docs/en/checkpointing
"""
import viz2
from deck import ba, flow, lab, light
from hx import code, esc, note, table
from stats_hx import src
from v1kit import brief, chat, shot, labcard, tstep
from v3kit import phmap

T = "1-6"



FILES = [("index.html", "34줄", "뼈대", "화면에 어떤 칸이 있나", "집 · 골조",
          [("aside", "왼쪽 · 페이지 목록"), ("main", "오른쪽 · 편집 화면"), ("#slash", "「/」 메뉴")]),
         ("style.css", "45줄", "모양", "칸이 어떻게 보이나", "집 · 인테리어",
          [("aside", "폭 240px · 연회색 바탕"), ("h1", "제목 글씨 34px"), (".handle", "손잡이 · 마우스 올릴 때만")]),
         ("app.js", "150줄", "동작 · 저장", "누르면 무슨 일이 생기나", "집 · 전기 · 배관",
          [("renderPages", "F1 · 목록 그리기"), ("slashCheck", "F3 · 「/」 보이면 메뉴"),
           ("dragSetup", "F4 · 끌어 옮기기"), ("save", "F5 · 브라우저에 저장")])]


def _code():
    """화면 뒤의 코드 — 개발계획.md → 파일 세 개(뼈대 · 모양 · 동작)가 차례로 · 마지막에 데이터 모양. 예시 앱 실제 이름 · 줄 수."""
    cols = ""
    for i, (f, n, role, q, house, rows) in enumerate(FILES):
        d = .8 + i * 1.6
        r = "".join(f'<li style="--d:{d + .4 + j * .25:.2f}s"><code>{esc(c)}</code><span>{x}</span></li>' for j, (c, x) in enumerate(rows))
        cols += (f'<div class="v16c c{i}" style="--d:{d:.1f}s"><div class="hd"><b>{f}</b><small>{n}</small></div>'
                 f'<div class="rl"><strong>{role}</strong><span>{q}</span></div><ul>{r}</ul><div class="hs">{house}</div></div>')
    data = ('<div class="v16d" style="--d:6.0s"><div class="lb">데이터<small>개발계획 3칸 → app.js 가 기억</small></div>'
            '<div class="pg"><b>페이지</b><span class="k">제목 · 주간 회의</span><span class="k">블록들</span>'
            '<span class="bk"><i>종류 · 제목</i>주간 회의</span><span class="bk"><i>종류 · 체크 상자</i>보고서 초안 · 체크 안 함</span>'
            '<span class="bk"><i>종류 · 구분선</i></span></div><div class="ls">→ localStorage</div></div>')
    return ('<div class="v16top" style="--d:.2s"><span>개발계획.md</span><i>→</i><span class="cc">Claude Code</span><i>→</i>'
            '<span>파일 세 개 · labs/mini_notion/예시/app</span></div>'
            f'<div class="v16cs">{cols}</div>{data}')


CSS = """
  /* 1-6 · 화면 뒤의 코드 (v16c) */
  .v16top{display:flex; gap:12px; align-items:center; font-size:16px; font-weight:800; color:#16233A; opacity:0; animation:v16In .4s var(--d) forwards;}
  .v16top span{background:#F4F6F9; border:1.5px solid #C9D6E6; border-radius:8px; padding:5px 12px;} .v16top span.cc{background:#16233A; color:#fff; border-color:#16233A;}
  .v16top i{font-style:normal; color:#F28C28;}
  .v16cs{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:14px;}
  .v16c{border:2px solid #C9D6E6; border-radius:14px; background:#fff; padding:12px 14px; opacity:0; transform:translateY(10px); animation:v16In .5s var(--d) forwards;}
  .v16c .hd{display:flex; justify-content:space-between; align-items:baseline; border-bottom:2px solid #E3E6EA; padding-bottom:6px;}
  .v16c .hd b{font-family:var(--mono); font-size:18px; color:#16233A;} .v16c .hd small{font-size:13px; color:#6B7785;}
  .v16c .rl{margin:8px 0 6px;} .v16c .rl strong{font-size:20px; color:#C76A12; margin-right:8px;} .v16c .rl span{font-size:14px; color:#3A4657;}
  .v16c ul{list-style:none; margin:0; padding:0;}
  .v16c li{display:flex; flex-direction:column; padding:5px 0; border-top:1px dashed #E3E6EA; opacity:0; animation:v16In .3s var(--d) forwards;}
  .v16c li code{font-size:13px; color:#6B7785;} .v16c li span{font-size:15.5px; font-weight:700; color:#16233A;}
  .v16c .hs{margin-top:8px; display:inline-block; font-size:13px; font-weight:700; color:#6B7785; background:#F4F6F9; border-radius:6px; padding:2px 8px;}
  .v16c.c0{border-top:5px solid #16233A;} .v16c.c1{border-top:5px solid #2383E2;} .v16c.c2{border-top:5px solid #F28C28;}
  .v16d{display:grid; grid-template-columns:170px 1fr auto; gap:14px; align-items:center; margin-top:14px; background:#FFF8F0; border:2px dashed #F2B880; border-radius:14px; padding:10px 14px;
    opacity:0; animation:v16In .5s var(--d) forwards;}
  .v16d .lb{font-size:19px; font-weight:800; color:#C76A12;} .v16d .lb small{display:block; font-size:12.5px; color:#6B7785;}
  .v16d .pg{display:flex; flex-wrap:wrap; gap:6px; align-items:center;} .v16d .pg b{font-size:16px; color:#16233A; margin-right:4px;}
  .v16d .k{font-size:13.5px; background:#fff; border:1.5px solid #E3E6EA; border-radius:6px; padding:2px 8px; color:#3A4657;}
  .v16d .bk{font-size:13.5px; background:#fff; border:1.5px solid #F2B880; border-radius:6px; padding:2px 8px; color:#16233A;} .v16d .bk i{font-style:normal; color:#C76A12; font-weight:700; margin-right:6px;}
  .v16d .ls{font-family:var(--mono); font-size:14px; font-weight:700; color:#16233A;}
  @keyframes v16In{to{opacity:1; transform:none;}}
  @media print{.v16top,.v16c,.v16c li,.v16d{opacity:1; animation:none; transform:none}}
"""


def slides():
    return [
        # ── 권한 모드
        light("권한 모드", viz2.maprows([
            ("Manual (default)", "읽기만 자동", "파일 수정 · 명령마다 물어봄"),
            ("acceptEdits", "파일 수정까지 자동", "흔한 파일 명령도 자동"),
            ("plan", "읽고 계획만", "소스 파일은 고치지 않음"),
            ("auto", "백그라운드 안전 검사 후 진행", "쓸 수 있는 환경에서만")], "모드", "Claude Code가 묻지 않고 하는 일")
              + note("이 강의에서 쓰지 않음", "dontAsk · bypassPermissions (격리된 컨테이너 · VM 전용)")
              + src(("Claude Code · Permission modes", "https://code.claude.com/docs/en/permission-modes")), T),
        light("모드 전환", viz2.tiles([
                  ("모드 표시", "입력창 아래 · 눌러서 고르기"), ("/plan", "요청 앞에 붙이면 plan"),
                  ("다음 대화", "고른 모드가 이어짐")], 3)
              + viz2.maprows([
            ("기획서 · 개발 계획", "plan", "파일 변경 없이 계획만"),
            ("첫 태스크 몇 개", "Manual", "수정마다 확인 · 승인"),
            ("흐름에 익숙해진 뒤", "acceptEdits", "수정은 자동 · 결과는 브라우저 확인")], "단계", "모드")
              + note("auto", "계정 · 환경에 따라 목록에 없을 수 있음"), T),
        # ── 한 번에 하나씩
        light("한 번에 구현할 때의 문제", viz2.tiles([
            ("오류 위치 파악 어려움", "여러 파일이 동시에 바뀜"), ("연쇄 오류", "「/」 메뉴 수정 → 엔터 동작 고장"),
            ("복구 지점 없음", "중간 커밋 없음")], 3)
              + viz2.pair(
                  "한 번에", [("요청 1번", "T1~T6 전부"), ("확인", "끝나고 한꺼번에")],
                  "하나씩", [("요청 6번", "T1 · T2 · … · T6"), ("확인", "태스크마다 · 문제 범위가 태스크 하나")]), T),
        # ── 테스트 케이스 · 디버깅
        light("순서도와 테스트 케이스", viz2.maprows([
            ("회사 이메일 · 비밀번호 일치", "로그인 완료", "kim@company.com · 맞는 비밀번호"),
            ("회사 이메일 아님", "거절", "kim@gmail.com"),
            ("비밀번호 틀림", "다시 입력", "회사 이메일 · 틀린 비밀번호 1번"),
            ("5번째 틀림", "10분 잠금", "틀린 비밀번호 5번")], "순서도 갈래", "기대 결과 · 입력")
              + note("테스트 케이스", "로그인 순서도의 갈래 하나 = 확인 하나 · 만들기 전에 AI에게 먼저 줌"), T),
        light("태스크 진행 순서", flow([
            ("테스트 케이스", "입력 → 기대 결과"), ("태스크 요청", "「T3만 · 이 케이스로 확인」"), ("브라우저 확인", "케이스대로 직접 눌러 보기"),
            ("수정 요청", "기대 · 실제 · 오류 원문"), ("커밋", "케이스 모두 통과 뒤")], hl=0)
              + note("반복", "테스트 케이스 통과까지 확인 · 수정 반복 · 문제는 그 태스크 안에서 해결")
              + src(("참고 · 비디오머그 「나만 안 해 바이브 코딩」", "https://www.youtube.com/watch?v=C9aQKsL2NVM"),
                    ("참고 · 코딩애플 「AI 에이전트 만드는 기초 기술」", "https://www.youtube.com/watch?v=eu5H0iRJsJ4")), T),
        ba("태스크 요청 예시", T, "「나머지 다 만들어 줘」",
           "「개발 계획의 T3만 진행해 줘.\n빈 블록에 「/」 → 「체크 상자」 고르면 그 블록이 체크 상자로 · 이 케이스로 확인해 줘」",
           "태스크 번호 + 테스트 케이스 (입력 → 기대 결과)"),
        # ── 서버
        light("식당 주방 비유", phmap(
            "v1_u6_kitchen.webp", "식당 주방과 손님", "AI 생성 그림 · Z-Image Turbo (Apache 2.0)",
            "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo",
            viz2.maprows([
                ("주방", "서버", "요청을 받아 화면 파일 전달"), ("손님", "브라우저", "화면을 보는 쪽"), ("주문", "요청", "「첫 화면 주세요」"),
                ("요리", "화면 파일", "index.html · app.js"), ("주방 위치", "localhost:8000", "내 컴퓨터 안")], "식당", "웹")), T),
        light("로컬 서버 실행", flow([("「서버 띄워 줘」", "Claude Code에 요청"), ("실행 명령", "Claude가 고름"), ("주소", "http://localhost:8000"), ("브라우저로 열기", "화면 확인")], hl=2)
              + code("실행 명령 · 예", esc("python3 -m http.server 8000\n→ http://localhost:8000 에서 열림"))
              + note("localhost", "내 컴퓨터에서만 열림 · 다른 사람에게 보이게 하는 일은 배포"), T),
        light("서버 관련 요청", viz2.tiles([
            ("파일 수정 뒤", "브라우저 새로고침"), ("주소 접속 불가", "「서버 다시 띄워 줘」"),
            ("포트 충돌", "「다른 포트로 띄워 줘」"), ("종료", "「서버 꺼 줘」")], 2), T),
        # ── 태스크별 화면 (실제 캡처)
        light("화면 뒤의 코드", _code(), T),
        light("T1 화면 뼈대 · 페이지 목록", shot("notion_empty.webp", "T1 직후 · 새 페이지를 연 화면", [
            ("F1", "왼쪽 페이지 목록 · 「+ 새 페이지」"), ("새 페이지", "「제목 없음」 · 목록에 바로 추가"), ("테스트 케이스", "새 페이지 → 목록 맨 아래에 생김")]), T),
        light("T2 블록 편집", shot("notion_main.webp", "T2 직후 · 주간 회의록 페이지", [
            ("F2", "제목 · 글 · 체크 상자 · 구분선"), ("엔터", "아래에 새 블록 · 체크 상자 다음은 체크 상자"), ("테스트 케이스", "체크하면 줄이 그어지고 회색")]), T),
        light("T3 「/」 메뉴", shot("notion_slash.webp", "T3 직후 · 빈 블록에 「/」 입력", [
            ("F3", "빈 블록에 「/」 → 메뉴"), ("고르기", "화살표 · 엔터 · 마우스 클릭"), ("테스트 케이스", "「체크 상자」 → 그 블록이 체크 상자로")]), T),
        light("T4 블록 끌어 옮기기", viz2.tiles([
            ("손잡이", "블록 왼쪽 「⋮⋮」 · 마우스를 올리면 보임"), ("끌어 놓기", "놓을 자리 위에 파란 줄"), ("새로고침", "바뀐 순서 그대로")], 3)
              + flow([("손잡이 잡기", "「발표 자료 검토」"), ("할 일 맨 위로 끌기", "파란 줄 확인"), ("놓기", ""), ("새로고침", "첫 번째 할 일 그대로")], hl=2), T),
        light("T5 저장", viz2.tiles([
            ("F5", "입력할 때마다 저장"), ("저장 위치", "이 브라우저 · localStorage"), ("테스트 케이스", "새로고침해도 쓴 내용 그대로")], 3)
              + flow([("체크 상자 추가", "「주간 회의록」 · 「보고서 초안」"), ("새로고침", "⌘R · F5"), ("다시 보기", "「보고서 초안」 그대로"),
                      ("다른 브라우저", "보이지 않음 · 정상")], hl=2), T),
        light("T6 완료 기준 점검 · 모바일 화면", shot("notion_mobile.webp", "폭 390px · 페이지 목록이 위로", [
            ("완료 기준", "390px 에서 가로 스크롤 없음"), ("확인 방법", "브라우저 창을 좁히기"), ("수정 요청 예", "「폭 390px 에서 가로 스크롤이 생겨」")]), T),
        light("완료 기준 확인", table(["개발 계획 완료 기준", "확인 방법", "결과"], [
            ["페이지 목록 · 「시작하기」가 첫 화면", "주소 열기", "✓"], ["체크 상자 추가 후 새로고침해도 남음", "「주간 회의록」에 「보고서 초안」 → 새로고침", "✓"],
            ["「/」 → 체크 상자로 바뀜", "빈 블록에 「/」 → 체크 상자", "✓"], ["끌어 옮긴 순서 유지", "세 번째 블록 → 맨 위 → 새로고침", "✓"],
            ["390px 에서 가로 스크롤 없음", "창 좁히기", "✓"]])
              + note("확인 방식", "완료 기준 다섯 줄 하나씩 대조"), T),
        # ── 마음에 안 들 때
        light("오류 해결 과정 비교", viz2.pair(
            "검색으로 해결", [("① 오류 메시지 복사", "빨간 글씨 그대로"), ("② 검색", "구글 · Stack Overflow"), ("③ 비슷한 질문 찾기", "영어 답변 해석"),
                         ("④ 내 코드에 맞게 고치기", "직접 수정"), ("⑤ 실행 → 다른 오류면 ①부터", "반복")],
            "바이브코딩", [("① 증상 · 오류 화면 전달", "「버튼을 눌러도 반응 없음」 + 화면 캡처"), ("② AI가 원인 파악 · 수정", "파일 읽기 · 고치기"),
                       ("③ 실행해 확인", "브라우저에서 다시 눌러 보기"), ("④ 안 되면 증상 다시 전달", "달라진 점 그대로")], hl="r")
              + src(("참고 · 이동훈의 루트AI 「바이브코딩 15분」", "https://www.youtube.com/watch?v=TImjZnT87ys")), T),
        ba("버그 알리는 방법", T, "「로그인이 안 돼요」",
           "「kim@gmail.com 으로 넣으면\n기대 · 거절 / 실제 · 로그인됨\n오류 메시지 원문 · 화면 캡처 첨부」",
           "재현 순서 · 기대 결과 · 실제 결과 · 오류 원문"),
        ba("구체적 수정 요청", T, "「더 예쁘게 해 줘」",
           "「왼쪽 목록에서 긴 페이지 제목이 잘려.\n목록 폭은 그대로, 제목은 두 줄까지 보이게」",
           "세 칸 · 어디 · 지금 상태 · 원하는 결과 · 한 번에 하나"),
        light("화면 캡처 첨부", viz2.tiles([
            ("화면 캡처 붙이기", "입력창에 붙여 넣기 · 끌어다 놓기"), ("가리키기", "「캡처에서 오른쪽 위 버튼」"),
            ("오류 문구", "브라우저 오류는 그대로 복사해 붙이기")], 3)
              + chat([("me", "[화면 캡처 붙임]\n「/」 메뉴가 화면 아래로 잘려서 「구분선」이 안 보여. 메뉴가 화면 안에 다 보이게 해 줘."),
                      ("ai", "메뉴 아래 공간이 모자라면 블록 위쪽에 열리게 바꿨다. 새로고침해서 확인해 줘.")], "캡처와 함께 요청 · 예")
              , T),
        light("Git으로 되돌리기", flow([
            ("수정 요청", "디자인 변경"), ("확인", "전보다 나빠짐"), ("「마지막 커밋 상태로 되돌려 줘」", ""), ("다시 요청", "수정 요청 세 칸 형식")], hl=2)
              + chat([("me", "방금 바꾼 디자인이 전보다 별로야. 마지막 커밋 상태로 되돌려 줘."),
                      ("ai", "마지막 커밋(T5 저장) 뒤에 고친 style.css 를 되돌렸다.")], "되돌리기 대화 예")
              + note("커밋", "태스크마다 남긴 커밋이 돌아갈 세이브 포인트"), T),
        light("체크포인트와 Git", viz2.pair(
            "체크포인트 (/rewind · Esc 두 번)", [("남는 때", "요청마다 자동"), ("되감기", "코드 · 대화 · 둘 다"),
                                              ("못 잡는 것", "Bash 명령으로 바뀐 파일 · Claude Code 밖에서 고친 파일")],
            "Git 커밋", [("남는 때", "내가 「커밋해 줘」 한 시점"), ("보관", "지우기 전까지 · GitHub 에도"), ("배포", "커밋을 가져가 공개")], hl="r")
              + note("공식 문서", "체크포인트는 버전 관리를 대신하지 않음")
              + src(("Claude Code · Checkpointing", "https://code.claude.com/docs/en/checkpointing")), T),
        light("바이브 디버깅 순서", flow([
            ("증상 전달", "재현 · 기대 · 실제 · 오류 원문"),
            ("원인 먼저", "「고치기 전에 원인부터」"), ("통과 · 저장", "테스트 통과 → 커밋"), ("두 번 실패", "되돌리고 새 대화")], hl=0)
              + src(("Claude Code 문서 · Best practices", "https://code.claude.com/docs/en/best-practices")), T),
        # ── 실습
        labcard(T, "개발 계획으로 앱 만들기", T, "개발계획.md", "동작하는 앱", ["태스크 하나씩", "브라우저 확인", "커밋"]),
        brief("1-6", T,
              ["태스크 하나 요청 · 「T1만」", "브라우저로 눌러 보기", "완료 기준 대조", "「커밋해 줘」 → 다음 태스크"],
              [],
              ["태스크 번호", "서버 띄워 줘", "커밋해 줘", "되돌려 줘"],
              ["태스크마다 브라우저로 직접 눌러 봄", "커밋 기록이 태스크 수만큼 쌓임"],
              "엉뚱하게 만들기 시작하면 Esc 로 멈추고 다시 요청 · 망가지면 「마지막 커밋으로 되돌려 줘」"),
        tstep(T, 1, "태스크 하나 요청", T, ask=("Claude Code 입력창", "개발계획.md 의 T1만 만들어 줘"),
              rows=[("한 번에", "태스크 하나만"), ("승인", "파일마다 패널에서 승인"), ("자동 승인", "이 대화 동안 · 익숙해진 뒤")]),
        tstep(T, 2, "브라우저 확인", T, "lab16_app.webp", "첫 태스크 뒤 화면 · 새 페이지 두 번 누름",
              rows=[("열기", "서버 주소 또는 index.html"), ("눌러 보기", "「+ 새 페이지」 → 목록에 추가"), ("새로고침", "macOS ⌘R · Windows F5")]),
        tstep(T, 3, "완료 기준 대조", T, need="VS Code Claude Code 패널 캡처 · 첫 태스크 작업 보고 (만든 것 · 아직 없는 것)",
              rows=[("보고", "만든 것 · 아직 없는 것"), ("대조", "개발계획.md 완료 기준"), ("아직", "저장 전 · 새로고침하면 사라짐 → T5")]),
        tstep(T, 4, "커밋해 줘", T, ask=("Claude Code 입력창", "커밋해 줘"),
              rows=[("메시지", "Claude Code 가 작성"), ("커밋", "태스크마다 하나"), ("다음", "T2 → 같은 순서 · T6 까지")]),
        light("실습 1-6 확인", code("커밋 기록 · 예", esc(
            "e41a0b2  T6 모바일 폭 정리\n"
            "c9d3f17  T5 새로고침 뒤 저장 유지\n"
            "5a8e2c0  T4 블록 끌어 옮기기\n"
            "91f6b3d  T3 「/」 메뉴\n"
            "2d7c4e9  T2 블록 편집\n"
            "a3b8e51  T1 화면 뼈대 · 페이지 목록\n"
            "7b21d04  기획서 · 개발 계획 첫 버전"))
              + viz2.tiles([
                  ("완료 기준", "개발 계획 다섯 줄 모두 ✓"), ("커밋", "태스크마다 하나"), ("막히면", "labs/mini_notion/예시/app 과 비교")], 3), T),
    ]
