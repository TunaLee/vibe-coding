"""1-2 도구 · 실습 환경.

도구 네 개 → Claude · Claude Code · GitHub · Vercel 한 장씩(정의 · 요금 · 쓰는 단원) → 실습 1-2(계정 · 설치 · 첫 요청).
사실 출처: scratchpad/v1_facts.md (claude.com/pricing · code.claude.com/docs setup · overview · docs.github.com · vercel.com/docs)
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note, table
from stats_hx import big, src
from v1kit import brief, chat, shot

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
    req = '<div class="v1ccq">요청 · 「팀 할 일 보드 만들어 줘」</div>'
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


def slides():
    return [
        # ── 도구 네 개
        light("1부 실습 도구", flow([("Claude", "대화형 AI · 아이디어 고르기 (1-3)"), ("Claude Code", "위임형 AI · 기획서 · PRD · 앱 코드 (1-3 ~ 1-6)"),
                                      ("GitHub", "코드 · 변경 기록 보관 (1-5 · 1-7)"), ("Vercel", "배포 · 공개 주소 (1-7)")]), T),
        # ── Claude
        light("Claude", '<div class="twocol"><div>'
              + viz2.tiles([("대화형 AI", "claude.ai · 웹 · 데스크톱 · 휴대폰 앱"), ("1부에서 맡는 일", "아이디어 고르기 · 질문 정리"),
                            ("못 하는 일", "내 컴퓨터 파일 직접 수정 · 명령 실행")], 1)
              + "</div><div>"
              + chat([("me", "할 일 목록 앱을 만들려고 해. 소크라테스식 대화로 진행해 줘"),
                      ("ai", "이 앱은 누가 쓰나요? 혼자인가요, 팀인가요?"),
                      ("me", "나 혼자 써. 주로 휴대폰에서 볼 거야"),
                      ("ai", "끝낸 일은 지우나요, 남겨 두나요?")], "Claude 대화 예")
              + "</div></div>"
              + note("소크라테스식 대화", "답 대신 질문을 하나씩 · 내 답으로 다음 질문"), T),
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
            ("코드 보관함", "인터넷에 둔 내 프로젝트 폴더"), ("변경 기록", "언제 · 무엇을 바꿨는지 (1-5)"),
            ("배포 출발점", "Vercel 이 여기서 코드를 가져감 (1-7)"), ("요금", "Free · 비공개 저장소 무제한")])
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("Vercel", pic("v1_u2_vercel.webp", "Vercel · 공개 주소 (AI 생성 그림)", [
            ("공개 주소", "프로젝트이름.vercel.app"), ("자동 배포", "GitHub 에 올리면 다시 배포 (1-7)"),
            ("가입", "GitHub 계정으로 · 비밀번호 따로 없음"), ("요금", "Hobby 무료 · 개인 · 비상업용 · 회사 업무 공개는 Pro $20")])
              + src(("Vercel pricing", "https://vercel.com/pricing"), ("Hobby plan", "https://vercel.com/docs/plans/hobby")), T),
        # ── 실습
        lab("1-2", "실습 환경 준비 · 첫 위임", T, "계정 세 개 · Claude Code 설치 · 할 일 목록 기능을 목표 한 줄로 맡기기",
            ["Claude 가입 · Pro 이상 · GitHub · Vercel 가입", "VS Code · Claude Code 확장 설치",
             "내 프로젝트 폴더에서 첫 요청", "delegate_todo 폴더를 열고 브라우저로 확인", "기능 세 개를 목표 한 줄씩 맡기기"],
            ["claude --version 이 버전을 보여 줌", "추가 · 체크 · 남은 개수가 브라우저에서 동작", "코드는 직접 고치지 않음"],
            files='<a class="dl" href="dl/delegate_todo.zip" download>delegate_todo.zip</a>'),
        brief("1-2 ①", T, ["claude.ai 가입 · 요금제 확인", "github.com 가입", "vercel.com → GitHub 로 계속하기",
                            "VS Code 설치 → 확장 「Claude Code」", "터미널에서 claude --version"],
              [("계정", "Claude (Pro 이상) · GitHub · Vercel"), ("설치", "VS Code · Claude Code 확장"),
               ("폴더", "바탕화면에 내 아이디어 이름 폴더")],
              ["Pro", "GitHub로 계속하기", "Claude Code 확장", "claude --version"],
              ["세 사이트 모두 로그인된 상태", "VS Code 왼쪽에 Claude 아이콘"],
              "회사 PC 에서 설치가 막히면 웹 claude.ai/code · 1-6 전까지 해결", folder="바탕화면/내 프로젝트 폴더", slot_title="준비"),
        brief("1-2 ②", T, ["VS Code → 폴더 열기", "Claude Code 열기 · 로그인", "폴더 신뢰 허용", "첫 요청 보내기", "답 읽기"],
              [("목표", "이 폴더의 현재 상태 듣기"), ("범위", "이 폴더 안만"),
               ("하지 말 것", "아직 파일 만들지 않기")],
              ["폴더 열기", "로그인", "첫 요청"],
              ["Claude Code 가 폴더 내용을 답함", "파일이 새로 생기지 않음"],
              "로그인 창이 안 뜨면 VS Code 재시작", folder="바탕화면/내 프로젝트 폴더"),
        light("첫 요청 결과", '<div class="twocol"><div>'
              + chat([("me", "이 폴더에 지금 뭐가 있는지 알려 줘. 아직 파일은 만들지 마"),
                      ("ai", "이 폴더는 비어 있다.\n파일 · 하위 폴더가 없다.\n만들 앱을 알려 주면 구조를 제안한다.")], "Claude Code 대화")
              + "</div><div>"
              + viz2.tiles([("계정", "Claude Pro 이상 로그인"), ("설치", "claude --version 이 버전 번호 표시"),
                            ("폴더", "새 파일 없음")], 1)
              + "</div></div>", T),
        # ── 실습 ③ 위임형 첫 작업
        light("delegate_todo 초기 화면", shot("v1_u2_todo_start.webp", "delegate_todo · index.html 을 브라우저로 연 화면", [
            ("보이는 것", "할 일 두 개 · 입력칸 · 추가 버튼"), ("동작 안 함", "추가 버튼 · 체크 줄 긋기 · 남은 개수"),
            ("파일", "index.html · style.css · app.js")]), T),
        brief("1-2 ③", T, ["delegate_todo 폴더를 VS Code 로 열기", "index.html 을 브라우저로 열어 추가 버튼 눌러 보기",
                            "Claude Code 에 목표 한 줄 요청", "진행 화면에서 ① 읽기 ② 수정 ③ 확인 찾기", "새로고침 · 직접 확인 → 다음 기능"],
              [("목표", "기능 하나씩 · 추가 → 체크 → 남은 개수"), ("확인 방법", "브라우저에서 직접 누르기"),
               ("하지 말 것", "코드 직접 수정 · 세 기능 한 번에 요청")],
              ["목표 한 줄", "브라우저 확인", "하나씩"],
              ["추가한 할 일이 목록에 생김", "체크하면 줄이 그어짐", "「남은 할 일: N」 표시"],
              "버튼이 그대로면 브라우저 새로고침 · 증상 그대로 전달", folder="delegate_todo", example=""),
        light("Claude Code 작업 화면", '<div class="twocol"><div>'
              + chat([("me", "추가 버튼을 누르면 입력한 할 일이 목록에 생기게 해 줘"),
                      ("ai", "① index.html · app.js 를 읽었다.\n② app.js 에 추가 버튼 처리 코드를 넣었다.\n③ 입력칸이 비면 추가하지 않게 했다.\n브라우저를 새로고침해 확인해 줘.")], "Claude Code 화면 예")
              + "</div><div>"
              + viz2.tiles([("① 맥락 파악", "파일 읽기"), ("② 작업", "app.js 수정"), ("③ 결과 확인", "빈 입력 처리 · 사람 확인 요청")], 1)
              + "</div></div>"
              + note("요청 = 결과 ?", "브라우저에서 직접 눌러 요청과 같은지 확인"), T),
    ]


CSS = """
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
