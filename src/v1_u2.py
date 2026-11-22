"""1-2 도구 · 실습 환경.

도구 네 개 → Claude · Claude Code · GitHub · Vercel 한 장씩(정의 · 요금 · 쓰는 단원) → 실습 1-2(계정 · 설치 · 첫 요청) — 실습마다 단계별 화면 장(실제 캡처 · 번호 상자 · macOS / Windows 차이).
사실 출처: scratchpad/v1_facts.md (claude.com/pricing · code.claude.com/docs setup · overview · docs.github.com · vercel.com/docs)
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note, table
from stats_hx import big, src
from v1kit import brief, chat, shot, labcard

T = "1-2"


def pic(img, cap, side):
    """그림 + 오른쪽 정보 카드 — 1-1 의 뇌 · 생성 그림을 다시 쓴다."""
    return shot(img, cap, side)


VSDOC = ("그림 · VS Code 문서 (Microsoft) · CC BY 3.0", "https://github.com/microsoft/vscode-docs")


def annot(img, alt, boxes, cap):
    """공식 화면 캡처 위에 번호 상자가 차례로 켜진다. boxes: (번호, 이름, left, top, width, height) — % 단위."""
    b = "".join(f'<div class="v1anb" style="--d:{.4 + i * .7:.1f}s; left:{l}%; top:{t}%; width:{w}%; height:{h}%">'
                f'<em>{n}</em><span>{lab}</span></div>' for i, (n, lab, l, t, w, h) in enumerate(boxes))
    return (f'<figure class="v1an"><div class="v1anw"><img src="img/{img}" alt="{alt}"/>{b}</div>'
            + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>')


def cc_lanes():
    """같은 요청 · 두 길 — Claude 는 사람 손이 네 번, Claude Code 는 AI 가 끝까지."""
    req = '<div class="v1ccq">요청 · 「미니 노션 만들어 줘」</div>'
    rows = [
        ("v1_brain1.webp", "Claude", "claude.ai · 대화형", 0.6, [
            ("AI", "코드를 글로 답함"), ("사람", "코드 복사"), ("사람", "파일 만들어 붙여넣기"),
            ("사람", "저장 · 브라우저로 열기"), ("사람", "오류 나면 다시 질문")], "사람 손 4번"),
        ("v1_brain3.webp", "Claude Code", "VS Code · 터미널 · 위임형", 4.4, [
            ("AI", "폴더 파일 읽기"), ("AI", "index.html 만들기"), ("AI", "실행 · 확인"),
            ("AI", "오류 직접 고침"), ("사람", "결과 확인")], "사람 손 1번")]
    out = req
    for img, name, sub, d0, steps, tot in rows:
        st = "".join(f'<div class="v1ccs {"h" if who == "사람" else "a"}" style="--d:{d0 + i * .55:.2f}s"><em>{who}</em><span>{t}</span></div>'
                     for i, (who, t) in enumerate(steps))
        out += (f'<div class="v1ccr"><div class="v1cch"><img src="img/{img}" alt="{name}"/><b>{name}</b><small>{sub}</small></div>'
                f'<div class="v1ccl">{st}</div><div class="v1cct" style="--d:{d0 + len(steps) * .55:.2f}s">{tot}</div></div>')
    return f'<div class="v1cc">{out}</div>'


def _lg(img, name, cls=""):
    """도구 이름 위 로고."""
    return f'<img class="v1tlg {cls}" src="img/{img}.svg" alt=""/>{name}'


CCDOC = ("그림 · Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code")


def step(no, i, name, img, alt, boxes, rows, srcs=()):
    """실습 단계 화면 — 왼쪽 실제 화면(번호 상자) · 오른쪽 할 일 · Mac / Windows 차이."""
    left = annot(img, alt, boxes, "") if img else img_need(alt)
    return light(f"실습 {no} · {i}단계 {name}", '<div class="twocol v1vsgrid v1stp"><div>' + left + "</div><div>"
                 + viz2.tiles(rows, 1) + "</div></div>" + (src(*srcs) if srcs else ""), T)


def img_need(what):
    return (f'<div class="need-img"><span class="nk">캡처 필요</span><span class="nd">{what}</span>'
            '<span class="nm2">자동 접속 차단 · 강사 화면 캡처로 교체</span></div>')


def term(title, lines):
    return code(title, esc(lines))


def slides():
    return [
        # ── 도구 네 개
        light("1부 실습 도구", '<div class="v1tools">' + flow([(_lg("claude_symbol", "Claude Code"), "아이디어 · 기획서 · 개발 계획 · 앱 코드"),
                                      (_lg("github_logo", "GitHub"), "코드 · 변경 기록 보관"), (_lg("vercel_logo", "Vercel", "w"), "배포 · 공개 주소")]) + '</div>'
              + src(("GitHub 로고 · GitHub · CC BY 4.0 · Wikimedia Commons",
                     "https://commons.wikimedia.org/wiki/File:GitHub_Invertocat_Logo.svg")), T),
        # ── Claude Code
        light("Claude와 Claude Code", cc_lanes()
              + note("차이", "내 컴퓨터 파일에 AI 손이 닿는가 · Claude 는 글로 답함 · Claude Code 는 파일을 직접 만들고 고침"), T),
        light("Claude Code 사용 환경", viz2.tiles([
            ("터미널", "명령어 창 · 기능이 가장 많음"), ("VS Code", "확장 프로그램 · 파일을 보며"),
            ("JetBrains", "플러그인"), ("데스크톱 앱", "macOS · Windows"), ("웹", "claude.ai/code · 클라우드")], 5)
              + note("공통", "어디서 쓰든 같은 엔진 · 같은 설정 · 같은 CLAUDE.md")
              + src(("Claude Code 문서 · platforms", "https://code.claude.com/docs/en/platforms")), T),
        light("VS Code", '<div class="twocol v1vsgrid"><div>' + annot("vscode_overview.webp", "VS Code 화면", [
                  ("①", "탐색기", 4.1, 4.5, 14.9, 92), ("②", "편집기", 19.1, 4.5, 58, 65),
                  ("③", "터미널", 19.1, 69.8, 58, 27.5), ("④", "AI 대화", 77.4, 4.5, 22.4, 92.8)], "") + "</div><div>"
              + viz2.tiles([("① 탐색기", "파일 목록"), ("② 편집기", "파일 내용"),
                            ("③ 터미널", "명령어 창"), ("④ AI 대화", "Claude Code 패널")], 1)
              + "</div></div>"
              + src(VSDOC), T),
        light("확장 프로그램", '<div class="twocol v1vsgrid"><div>' + annot("vscode_ext_list.webp", "Marketplace 확장 목록", [
                  ("①", "검색", 10.5, 12.2, 88, 9.8), ("②", "확장 목록", 9, 23, 82, 76), ("③", "Install", 91, 36, 8, 63)],
                  "") + "</div><div>"
              + viz2.maprows([("휴대폰", "VS Code", ""), ("앱 스토어", "Marketplace", ""), ("앱", "확장 프로그램", "")])
              + "</div></div>"
              + src(("VS Code 문서 · Extensions", "https://code.visualstudio.com/docs/getstarted/extensions"), VSDOC), T),
        light("Claude Code 확장 설치", '<div class="twocol v1vsgrid"><div>' + annot("vscode_ext_install.webp", "확장 설치 화면", [
                  ("①", "확장 보기", 0, 69, 6.8, 13), ("②", "검색", 9.6, 22.5, 30.4, 7.5), ("③", "Install", 31, 45.5, 10, 8.5)],
                  "") + "</div><div>"
              + viz2.tiles([("① 확장 보기", "⇧⌘X · Ctrl+Shift+X"), ("② 검색", "Claude Code · Anthropic"),
                            ("③ Install", "설치"), ("④ Spark 아이콘", "로그인")], 1)
              + "</div></div>"
              + src(("Claude Code 문서 · VS Code", "https://code.claude.com/docs/en/vs-code"), VSDOC), T),
        light("Claude Code 설치", '<div class="twocol"><div>'
              + code("macOS · 터미널", esc("curl -fsSL https://claude.ai/install.sh | bash"))
              + code("Windows · PowerShell", esc("irm https://claude.ai/install.ps1 | iex"))
              + "</div><div>"
              + code("설치 확인 · 실행", esc("claude --version\nclaude"))
              + viz2.tiles([("Windows", "Git for Windows 설치 권장"), ("요구 사항", "macOS 13 이상 · Windows 10 1809 이상")], 1)
              + "</div></div>"
              + src(("Claude Code 문서 · setup", "https://code.claude.com/docs/en/setup")), T),
        light("첫 실행과 로그인", flow([("claude 실행", "또는 VS Code 확장"), ("로그인 방법 선택", "Claude 계정"),
                                     ("브라우저 인증", "Pro 이상 계정"), ("폴더 신뢰", "이 폴더에서 작업 허용"), ("입력창", "첫 요청")], hl=2)
              + viz2.tiles([("로그인", "처음 한 번 · 다음부터 바로 입력창"), ("폴더 신뢰", "처음 여는 폴더마다 확인"),
                            ("Free 계정", "로그인 단계에서 막힘 · Pro 이상 필요")], 3), T),
        # ── GitHub · Vercel
        light("GitHub", pic("v1_u2_github.webp", "GitHub · 코드 보관함 (AI 생성 그림)", [
            ("코드 보관함", "인터넷에 둔 내 프로젝트 폴더"), ("변경 기록", "언제 · 무엇을 바꿨는지"),
            ("배포 출발점", "Vercel 이 여기서 코드를 가져감"), ("요금", "Free · 비공개 저장소 무제한")])
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("Vercel", pic("v1_u2_vercel.webp", "Vercel · 공개 주소 (AI 생성 그림)", [
            ("공개 주소", "프로젝트이름.vercel.app"), ("자동 배포", "GitHub 에 올리면 다시 배포"),
            ("가입", "GitHub 계정으로 · 비밀번호 따로 없음"), ("요금", "Hobby 무료 · 개인 · 비상업용 · 회사 업무 공개는 Pro $20")])
              + src(("Vercel pricing", "https://vercel.com/pricing"), ("Hobby plan", "https://vercel.com/docs/plans/hobby")), T),
        # ── 실습
        labcard("1-2", "실습 환경 준비 · 첫 위임", T, "새 PC", "동작하는 할 일 목록", ["① 계정 · 설치 · 작업 폴더", "② 첫 요청", "③ 할 일 목록 위임"], files='<a class="dl" href="dl/workspace.zip" download>workspace.zip</a>'),
        brief("1-2 ①", T, ["claude.ai 가입 · 요금제 확인", "github.com 가입", "vercel.com → GitHub 로 계속하기",
                            "VS Code 설치 → 확장 「Claude Code」", "터미널에서 claude --version", "바탕화면에 workspace 폴더 만들기"],
              [("계정", "Claude (Pro 이상) · GitHub · Vercel"), ("설치", "VS Code · Claude Code 확장"),
               ("폴더", "바탕화면/workspace/mini_notion")],
              ["Pro", "GitHub로 계속하기", "Claude Code 확장", "claude --version"],
              ["세 사이트 모두 로그인된 상태", "VS Code 왼쪽에 Claude 아이콘"],
              "회사 PC 에서 설치가 막히면 웹 claude.ai/code", folder="바탕화면/workspace/mini_notion", slot_title="준비"),
        *[step("1-2 ①", 1, "Claude 가입 · 요금제", "lab12_pricing.webp", "Claude 요금제 화면", [("①", "Pro", 42, 45, 32, 54)],
               [("주소", "claude.ai → 가입"), ("요금제", "Pro 이상 · Claude Code 사용 조건"), ("Free", "Claude Code 로그인에서 막힘")],
               (("화면 · claude.com/pricing", "https://claude.com/pricing"),)),
          step("1-2 ①", 2, "GitHub 가입", None, "github.com/signup 가입 화면", [],
               [("주소", "github.com → Sign up"), ("입력", "이메일 · 비밀번호 · 사용자 이름"), ("막히는 곳", "이메일 인증 코드")]),
          step("1-2 ①", 3, "Vercel 가입", "lab12_vercel.webp", "Vercel 가입 화면", [("①", "Continue with GitHub", 21, 61, 57, 8.5)],
               [("주소", "vercel.com/signup"), ("선택", "Continue with GitHub"), ("막히는 곳", "이메일로 가입하면 GitHub 연결이 따로 필요")],
               (("화면 · vercel.com/signup", "https://vercel.com/signup"),)),
          step("1-2 ①", 4, "VS Code 설치", "lab12_vscode_dl.webp", "VS Code 다운로드 화면",
               [("①", "Windows", 25, 36, 30, 23), ("②", "macOS", 57, 36, 30, 23)],
               [("macOS", "macOS 버튼 · .dmg"), ("Windows", "Windows 버튼 · User Installer"), ("주소", "code.visualstudio.com/download")],
               (("화면 · code.visualstudio.com/download", "https://code.visualstudio.com/download"),)),
          step("1-2 ①", 4, "Claude Code 확장", "lab12_market.webp", "Marketplace · Claude Code for VS Code",
               [("①", "Install", 20, 46, 14, 13)],
               [("확장 보기", "macOS ⇧⌘X · Windows Ctrl+Shift+X"), ("검색", "Claude Code · Anthropic"), ("설치", "Install")],
               (("화면 · VS Marketplace · Claude Code", "https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code"),)),
          light("실습 1-2 ① · 5단계 설치 확인", '<div class="twocol"><div>'
                + term("macOS · 터미널", "$ claude --version\n2.1.322 (Claude Code)")
                + term("Windows · PowerShell", "> claude --version")
                + "</div><div>" + viz2.tiles([("결과", "버전 번호 · 숫자는 설치 시점마다 다름"),
                                             ("안 나오면", "터미널 창을 새로 열고 다시"), ("Windows", "Git for Windows 설치 권장")], 1)
                + "</div></div>", T),
          light("실습 1-2 ① · 6단계 작업 폴더 구조", '<div class="twocol"><div>'
                + term("바탕화면/workspace", """바탕화면/
└── workspace/            작업 공간
    ├── todo_list/        실습 1-2 ③
    │   └── index.html · style.css · app.js
    └── mini_notion/      내 앱 · VS Code 로 여는 폴더
        ├── 페르소나/      1-3 · 1-4
        ├── 기획서.md      1-3
        ├── 개발계획.md    1-4
        └── index.html    1-6""")
                + "</div><div>" + viz2.tiles([("workspace", "실습 폴더를 모아 두는 곳"),
                                             ("mini_notion", "내 앱 · VS Code 로 여는 폴더 · 1부 끝에 노션 같은 앱"),
                                             ("todo_list", "실습 1-2 ③ 예제"),
                                             ("한 번에 받기", '<a class="dl" href="dl/workspace.zip" download>workspace.zip</a> → 바탕화면에 압축 풀기')], 1)
                + "</div></div>", T),
          light("실습 1-2 ① · 6단계 Windows 폴더 만들기", '<div class="twocol"><div>'
                + flow([("탐색기", "Win+E"), ("바탕 화면", "왼쪽 목록"), ("새 폴더", "Ctrl+Shift+N"), ("이름", "workspace → mini_notion")])
                + term("PowerShell · 한 번에", 'cd ([Environment]::GetFolderPath("Desktop"))\nmkdir workspace\\mini_notion')
                + "</div><div>" + viz2.tiles([("zip 풀기", "우클릭 → 모두 압축 풀기 → 바탕 화면"),
                                             ("OneDrive", "바탕 화면이 OneDrive 안일 수 있음 · 명령은 자동으로 찾음"),
                                             ("VS Code 로 열기", "mini_notion 우클릭 → Code(으)로 열기 · 또는 File → Open Folder")], 1)
                + "</div></div>", T),
          light("실습 1-2 ① · 6단계 macOS 폴더 만들기", '<div class="twocol"><div>'
                + flow([("Finder", "⌘N"), ("데스크탑", "왼쪽 목록"), ("새 폴더", "⇧⌘N"), ("이름", "workspace → mini_notion")])
                + term("터미널 · 한 번에", "cd ~/Desktop\nmkdir -p workspace/mini_notion")
                + "</div><div>" + viz2.tiles([("zip 풀기", "더블클릭 → 같은 위치에 풀림"),
                                             ("VS Code 로 열기", "mini_notion 을 VS Code 아이콘에 끌어 놓기 · 또는 File → Open Folder")], 1)
                + "</div></div>", T)],
        brief("1-2 ②", T, ["VS Code → 폴더 열기", "Claude Code 열기 · 로그인", "폴더 신뢰 허용", "첫 요청 보내기", "답 읽기"],
              [("목표", "이 폴더의 현재 상태 듣기"), ("범위", "이 폴더 안만"),
               ("하지 말 것", "아직 파일 만들지 않기")],
              ["폴더 열기", "로그인", "첫 요청"],
              ["Claude Code 가 폴더 내용을 답함", "파일이 새로 생기지 않음"],
              "로그인 창이 안 뜨면 VS Code 재시작", folder="바탕화면/workspace/mini_notion"),
        *[step("1-2 ②", 1, "폴더 열기", "lab12_folder.webp", "VS Code 탐색기 · 폴더를 연 화면", [("①", "열린 폴더", 18, 15, 80, 22)],
               [("메뉴", "File → Open Folder"), ("macOS", "⌘O"), ("Windows", "Ctrl+K → Ctrl+O"), ("폴더", "바탕화면/workspace/mini_notion")], (VSDOC,)),
          step("1-2 ②", 2, "Claude Code 열기 · 로그인", "lab12_spark.webp", "편집기 오른쪽 위 Spark 아이콘", [("①", "Spark 아이콘", 87.5, 2, 5, 14)],
               [("열기", "편집기 오른쪽 위 Spark 아이콘"), ("로그인", "Claude 계정 · 브라우저 인증"), ("계정", "Pro 이상")], (CCDOC,)),
          step("1-2 ②", 3, "폴더 신뢰", "lab12_trust.webp", "폴더 신뢰 확인 창", [("①", "Yes, I trust the authors", 17, 80, 40, 8)],
               [("선택", "Yes, I trust the authors"), ("뜻", "이 폴더에서 작업 허용"), ("화면", "Windows 경로 예 · macOS 도 같은 창")], (VSDOC,)),
          step("1-2 ②", 4, "첫 요청 · 답 읽기", "lab12_prompt.webp", "Claude Code 패널 · 요청과 답",
               [("①", "입력창", 70, 78, 28, 13), ("②", "답", 70, 30, 28, 47)],
               [("① 입력창", "패널 아래 · Enter 로 보내기"), ("② 답", "패널 가운데"), ("확인", "폴더 내용 설명 · 새 파일 없음")], (CCDOC,))],
        light("첫 요청 결과", '<div class="twocol"><div>'
              + chat([("me", "이 폴더에 지금 뭐가 있는지 알려 줘. 아직 파일은 만들지 마"),
                      ("ai", "이 폴더는 비어 있다.\n파일 · 하위 폴더가 없다.\n만들 앱을 알려 주면 구조를 제안한다.")], "Claude Code 대화")
              + "</div><div>"
              + viz2.tiles([("계정", "Claude Pro 이상 로그인"), ("설치", "claude --version 이 버전 번호 표시"),
                            ("폴더", "새 파일 없음")], 1)
              + "</div></div>", T),
        # ── 실습 ③ 위임형 첫 작업
        light("할 일 목록 예제", shot("v1_u2_todo_start.webp", "index.html 을 브라우저로 연 화면", [
            ("예제", "버튼이 동작하지 않는 미완성 할 일 목록"), ("동작 안 함", "추가 버튼 · 체크 줄 긋기 · 남은 개수"),
            ("폴더", "todo_list · index.html · style.css · app.js")]), T),
        brief("1-2 ③", T, ["todo_list 폴더를 VS Code 로 열기", "index.html 을 브라우저로 열어 추가 버튼 눌러 보기",
                            "Claude Code 에 목표 한 줄 요청", "진행 화면에서 ① 읽기 ② 수정 ③ 확인 찾기", "새로고침 · 직접 확인 → 다음 기능"],
              [("목표", "기능 하나씩 · 추가 → 체크 → 남은 개수"), ("확인 방법", "브라우저에서 직접 누르기"),
               ("하지 말 것", "코드 직접 수정 · 세 기능 한 번에 요청")],
              ["목표 한 줄", "브라우저 확인", "하나씩"],
              ["추가한 할 일이 목록에 생김", "체크하면 줄이 그어짐", "「남은 할 일: N」 표시"],
              "버튼이 그대로면 브라우저 새로고침 · 증상 그대로 전달", folder="todo_list", example=""),
        *[light("실습 1-2 ③ · 1단계 폴더 열기", '<div class="twocol"><div>'
                + term("todo_list 폴더", "todo_list/\n├── index.html\n├── style.css\n└── app.js")
                + "</div><div>" + viz2.tiles([("받기", "workspace 안에 todo_list · workspace.zip 에 포함"), ("열기", "VS Code → File → Open Folder → workspace/todo_list"),
                                             ("macOS · Windows", "⌘O · Ctrl+K → Ctrl+O")], 1) + "</div></div>", T),
          step("1-2 ③", 2, "브라우저로 확인", "v1_u2_todo_start.webp", "index.html 을 브라우저로 연 화면", [],
               [("열기", "index.html 더블클릭 → 브라우저"), ("눌러 보기", "추가 · 체크 · 남은 개수"), ("현재", "버튼을 눌러도 변화 없음")]),
          light("실습 1-2 ③ · 3단계 목표 한 줄 요청", '<div class="twocol"><div>'
                + chat([("me", "추가 버튼을 누르면 입력한 할 일이 목록에 생기게 해 줘"),
                        ("ai", "app.js 를 고쳐서 「추가」 버튼을 누르거나 Enter 를 치면 입력한 할 일이 목록 맨 아래에 생기도록 했다.\n빈 입력은 추가되지 않는다.\n체크 줄 긋기 · 남은 개수는 요청 범위가 아니어서 건드리지 않았다.")],
                       "Claude Code 실제 답 · 요약 (2026-11-23)")
                + "</div><div>" + viz2.tiles([("요청", "기능 하나 · 목표 한 줄"), ("답", "바뀐 파일 · 한 일 · 안 한 일"),
                                             ("하지 말 것", "세 기능 한 번에 요청")], 1) + "</div></div>", T),
          step("1-2 ③", 4, "진행 화면 읽기", "lab12_edits.webp", "Claude Code 수정 승인 화면",
               [("①", "바뀐 코드", 11, 10, 53, 26), ("②", "수정 승인", 70, 57, 28, 34)],
               [("① 바뀐 코드", "초록 줄 = 추가 · 바뀐 부분"), ("② 수정 승인", "Yes 반영 · No 거절"), ("읽기", "패널의 Read · 파일 이름")], (CCDOC,)),
          step("1-2 ③", 5, "새로고침 · 확인", "lab12_todo_after.webp", "추가 버튼을 누른 뒤 화면", [("①", "새 할 일", 10, 63, 81, 8)],
               [("새로고침", "macOS ⌘R · Windows F5"), ("확인", "입력한 할 일이 목록에 추가"), ("다음", "체크 → 남은 개수 하나씩")])],
        light("Claude Code 작업 화면", '<div class="twocol"><div>'
              + chat([("me", "추가 버튼을 누르면 입력한 할 일이 목록에 생기게 해 줘"),
                      ("ai", "① index.html · app.js 를 읽었다.\n② app.js 에 추가 버튼 처리 코드를 넣었다.\n③ 입력칸이 비면 추가하지 않게 했다.\n브라우저를 새로고침해 확인해 줘.")], "Claude Code 화면 예")
              + "</div><div>"
              + viz2.tiles([("① 맥락 파악", "파일 읽기"), ("② 작업", "app.js 수정"), ("③ 결과 확인", "빈 입력 처리 · 사람 확인 요청")], 1)
              + "</div></div>"
              + note("요청 = 결과 ?", "브라우저에서 직접 눌러 요청과 같은지 확인"), T),
    ]


CSS = """
  /* 1-2 · 도구 로고 */
  .v1tools .fs b{display:flex; flex-direction:column; align-items:center; gap:12px;}
  .v1tlg{height:52px; width:auto;} .v1tlg.w{height:auto; width:120px; margin:14px 0 8px;}
  .v1clogo{height:46px; width:auto; display:block; margin:0 0 18px 4px;}
  /* 1-2 · Claude 와 Claude Code — 같은 요청 두 길 (v1cc) */
  .v1ccq{display:inline-block; background:#16233A; color:#fff; font-size:18px; font-weight:700; padding:9px 18px; border-radius:22px; margin-bottom:16px;}
  .v1ccr{display:grid; grid-template-columns:170px 1fr 120px; gap:14px; align-items:center; margin-bottom:16px;}
  .v1cch{display:flex; flex-direction:column; align-items:flex-start;}
  .v1cch img{width:120px; height:68px; object-fit:cover; border-radius:10px; margin-bottom:6px;}
  .v1cch b{font-size:21px; color:#16233A;} .v1cch small{font-size:13px; color:#6B7785;}
  .v1ccl{display:grid; grid-template-columns:repeat(5,1fr); gap:8px;}
  .v1ccs{border-radius:12px; padding:12px 10px; min-height:84px; opacity:0; animation:v1ccIn .45s var(--d) forwards;}
  .v1ccs em{display:inline-block; font-style:normal; font-size:12.5px; font-weight:800; padding:2px 9px; border-radius:10px; margin-bottom:7px;}
  .v1ccs span{display:block; font-size:16px; font-weight:600; color:#16233A; line-height:1.35;}
  .v1ccs.h{background:#FFF1E2; border:2px solid #F28C28;} .v1ccs.h em{background:#F28C28; color:#fff;}
  .v1ccs.a{background:#EAF0F7; border:2px solid #C9D6E6;} .v1ccs.a em{background:#16233A; color:#fff;}
  .v1cct{font-size:19px; font-weight:800; color:#C76A12; text-align:center; opacity:0; animation:v1ccIn .45s var(--d) forwards;}
  @keyframes v1ccIn{from{opacity:0; transform:translateX(-10px)} to{opacity:1; transform:none}}
  @media print{.v1ccs,.v1cct{opacity:1; animation:none}}
  /* 1-2 · 공식 화면 캡처 + 번호 상자 (v1an) */
  .v1an{margin:0;} .v1anw{position:relative; border-radius:10px; overflow:hidden; box-shadow:0 8px 24px rgba(22,35,58,.18);}
  .v1anw img{display:block; width:100%;}
  .v1stp > div:first-child{display:flex; justify-content:center;}
  .v1stp .v1anw{width:fit-content; max-width:100%; margin:0 auto;}
  .v1stp .v1anw img{width:auto; max-width:100%; max-height:440px;}
  .v1stp .need-img{min-height:300px; width:100%;}
  .v1anb{position:absolute; border:3px solid #F28C28; border-radius:6px; background:rgba(242,140,40,.12); opacity:0; animation:v1anIn .5s var(--d) forwards;}
  .v1anb em{position:absolute; left:-3px; top:-3px; background:#F28C28; color:#fff; font-style:normal; font-weight:800; font-size:14px; padding:2px 7px; border-radius:5px 0 6px 0; white-space:nowrap;}
  .v1anb span{display:none;}
  .v1an figcaption{font-size:13px; color:#8A94A3; margin-top:8px;}
  @keyframes v1anIn{from{opacity:0; transform:scale(1.04)} to{opacity:1; transform:none}}
  @media print{.v1anb{opacity:1; animation:none}}
  .v1vsgrid{grid-template-columns:1.7fr 1fr; align-items:center;}
  /* 1-2 · Claude 와 Claude Code 그림 */
  .v1u2cmp{display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-bottom:14px;}
  .v1u2cmp figure{margin:0; display:flex; align-items:center; gap:14px; background:#F7EEDB; border-radius:14px; padding:8px 16px;}
  .v1u2cmp img{width:150px; height:84px; object-fit:cover; border-radius:10px;}
  .v1u2cmp figcaption{font-size:16px; color:#3A4657;} .v1u2cmp figcaption b{font-size:21px; color:#16233A;}
"""
