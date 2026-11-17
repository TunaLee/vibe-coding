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


def slides():
    return [
        # ── 도구 네 개
        light("1부의 도구 네 개", flow([("Claude", "대화형 AI · 기획서 · PRD (1-3 · 1-4)"), ("Claude Code", "위임형 AI · 앱 코드 (1-6)"),
                                      ("GitHub", "코드 · 변경 기록 보관 (1-5 · 1-7)"), ("Vercel", "배포 · 공개 주소 (1-7)")]), T),
        # ── Claude
        light("Claude", '<div class="twocol"><div>'
              + viz2.tiles([("대화형 AI", "claude.ai · 웹 · 데스크톱 · 휴대폰 앱"), ("1부에서 맡는 일", "아이디어 → 기획서 → PRD"),
                            ("못 하는 일", "내 컴퓨터 파일 직접 수정 · 명령 실행")], 1)
              + "</div><div>"
              + chat([("me", "할 일 목록 앱을 만들려고 해. 바로 답하지 말고 소크라테스식 대화로 질문을 하나씩 이어 가 줘"),
                      ("ai", "이 앱은 누가 쓰나요? 혼자인가요, 팀인가요?"),
                      ("me", "나 혼자 써. 주로 휴대폰에서 볼 거야"),
                      ("ai", "끝낸 일은 지우나요, 남겨 두나요?")], "Claude 대화 예")
              + "</div></div>"
              + note("소크라테스식 대화", "답 대신 질문을 하나씩 · 내 답으로 다음 질문 (1-3)"), T),
        light("Claude 요금제", table(["요금제", "월 요금", "사용량", "Claude Code"], [
            ["Free", "$0", "기본", "✕"],
            ["<b>Pro</b>", "<b>$20</b> · 연 결제 시 월 $17", "기준", "<b>○</b>"],
            ["Max", "$100", "Pro 의 5배", "○"],
            ["Ultra", "$200", "Pro 의 10배", "○"]])
              + note("1부 기준", "Claude Code 는 Pro 이상 · 회사 Team · Enterprise 계정도 가능")
              + src(("claude.com/pricing · 2026-11", "https://claude.com/pricing"), ("Claude Code setup", "https://code.claude.com/docs/en/setup")), T),
        # ── Claude Code
        light("Claude와 Claude Code", '<div class="v1u2cmp">'
              + '<figure><img src="img/v1_brain1.webp" alt="LLM"/><figcaption><b>Claude</b> · 대화형</figcaption></figure>'
              + '<figure><img src="img/v1_brain3.webp" alt="코딩 에이전트"/><figcaption><b>Claude Code</b> · 위임형</figcaption></figure></div>'
              + viz2.pair(
                  "Claude", [("결과", "답변 글 · 코드 조각"), ("파일", "사람이 복사 · 붙여넣기")],
                  "Claude Code", [("결과", "내 폴더의 파일"), ("파일", "직접 읽기 · 만들기 · 고치기 · 실행")], hl="r")
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("Claude Code를 쓰는 곳", viz2.tiles([
            ("터미널", "명령어 창 · 기능이 가장 많음"), ("VS Code", "확장 프로그램 · 파일을 보며"),
            ("JetBrains", "플러그인"), ("데스크톱 앱", "macOS · Windows"), ("웹", "claude.ai/code · 클라우드")], 5)
              + note("공통", "어디서 쓰든 같은 엔진 · 같은 설정 · 같은 CLAUDE.md")
              + src(("Claude Code 문서 · platforms", "https://code.claude.com/docs/en/platforms")), T),
        light("이 강의의 선택 · VS Code", viz2.tiles([
            ("편집기 (IDE)", "코드를 보고 고치는 프로그램 · VS Code"), ("터미널", "마우스 클릭 대신 글자 명령으로 컴퓨터를 다루는 창"),
            ("VS Code 한 화면", "파일 트리 · 편집기 · Claude Code 대화 · 터미널")], 3)
              + flow([("VS Code 설치", "code.visualstudio.com"), ("확장 검색", "「Claude Code」"), ("설치", "공식 확장"),
                      ("폴더 열기", "내 프로젝트 폴더"), ("로그인", "Claude 계정")])
              + src(("참고 · 혼잡스 「바이브코딩 이 지도 한장으로」", "https://www.youtube.com/watch?v=HNtS6WGGhNU"),
                    ("참고 · 비디오머그 「나만 안 해 바이브 코딩」", "https://www.youtube.com/watch?v=C9aQKsL2NVM")), T),
        light("Claude Code 설치", '<div class="twocol"><div>'
              + code("macOS · 터미널", esc("curl -fsSL https://claude.ai/install.sh | bash"))
              + code("Windows · PowerShell", esc("irm https://claude.ai/install.ps1 | iex"))
              + "</div><div>"
              + code("설치 확인 · 실행", esc("claude --version\nclaude"))
              + viz2.tiles([("Windows", "Git for Windows 설치 권장"), ("요구 사항", "macOS 13 이상 · Windows 10 1809 이상")], 1)
              + "</div></div>"
              + src(("Claude Code 문서 · setup", "https://code.claude.com/docs/en/setup")), T),
        light("첫 실행 · 로그인", flow([("claude 실행", "또는 VS Code 확장"), ("로그인 방법 선택", "Claude 계정"),
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
              "회사 PC 에서 설치가 막히면 웹 claude.ai/code · 1-6 전까지 해결", folder="바탕화면/내 프로젝트 폴더"),
        brief("1-2 ②", T, ["VS Code → 폴더 열기", "Claude Code 열기 · 로그인", "폴더 신뢰 허용", "첫 요청 보내기", "답 읽기"],
              [("목표", "이 폴더의 현재 상태 듣기"), ("범위", "이 폴더 안만"),
               ("하지 말 것", "아직 파일 만들지 않기")],
              ["폴더 열기", "로그인", "첫 요청"],
              ["Claude Code 가 폴더 내용을 답함", "파일이 새로 생기지 않음"],
              "로그인 창이 안 뜨면 VS Code 재시작", folder="바탕화면/내 프로젝트 폴더"),
        light("첫 요청 결과 예", '<div class="twocol"><div>'
              + chat([("me", "이 폴더에 지금 뭐가 있는지 알려 줘. 아직 파일은 만들지 마"),
                      ("ai", "이 폴더는 비어 있다.\n파일 · 하위 폴더가 없다.\n만들 앱을 알려 주면 구조를 제안한다.")], "Claude Code 대화 예")
              + "</div><div>"
              + viz2.tiles([("계정", "Claude Pro 이상 로그인"), ("설치", "claude --version 이 버전 번호 표시"),
                            ("폴더", "새 파일 없음")], 1)
              + "</div></div>", T),
        # ── 실습 ③ 위임형 첫 작업
        light("delegate_todo · 시작 상태", shot("v1_u2_todo_start.webp", "delegate_todo · index.html 을 브라우저로 연 화면", [
            ("보이는 것", "할 일 두 개 · 입력칸 · 추가 버튼"), ("동작 안 함", "추가 버튼 · 체크 줄 긋기 · 남은 개수"),
            ("파일", "index.html · style.css · app.js")]), T),
        brief("1-2 ③", T, ["delegate_todo 폴더를 VS Code 로 열기", "index.html 을 브라우저로 열어 추가 버튼 눌러 보기",
                            "Claude Code 에 목표 한 줄 요청", "진행 화면에서 ① 읽기 ② 수정 ③ 확인 찾기", "새로고침 · 직접 확인 → 다음 기능"],
              [("목표", "기능 하나씩 · 추가 → 체크 → 남은 개수"), ("확인 방법", "브라우저에서 직접 누르기"),
               ("하지 말 것", "코드 직접 수정 · 세 기능 한 번에 요청")],
              ["목표 한 줄", "브라우저 확인", "하나씩"],
              ["추가한 할 일이 목록에 생김", "체크하면 줄이 그어짐", "「남은 할 일: N」 표시"],
              "버튼이 그대로면 브라우저 새로고침 · 증상 그대로 전달", folder="delegate_todo", example=""),
        light("위임형 진행 화면 · 예", '<div class="twocol"><div>'
              + chat([("me", "추가 버튼을 누르면 입력한 할 일이 목록에 생기게 해 줘"),
                      ("ai", "① index.html · app.js 를 읽었다.\n② app.js 에 추가 버튼 처리 코드를 넣었다.\n③ 입력칸이 비면 추가하지 않게 했다.\n브라우저를 새로고침해 확인해 줘.")], "Claude Code 화면 예")
              + "</div><div>"
              + viz2.tiles([("① 맥락 파악", "파일 읽기"), ("② 작업", "app.js 수정"), ("③ 결과 확인", "빈 입력 처리 · 사람 확인 요청")], 1)
              + "</div></div>"
              + note("요청 = 결과 ?", "브라우저에서 직접 눌러 요청과 같은지 확인"), T),
        light("막히는 곳", viz2.tiles([
            ("claude 명령 없음", "터미널 새로 열기 · 설치 다시"), ("Free 계정", "Claude Code 로그인 불가 · Pro 이상"),
            ("Windows · Git 없음", "Git for Windows 설치"), ("회사 PC 설치 막힘", "웹 claude.ai/code")], 2)
              + src(("Claude Code 문서 · setup", "https://code.claude.com/docs/en/setup")), T),
    ]


CSS = """
  /* 1-2 · Claude 와 Claude Code 그림 */
  .v1u2cmp{display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-bottom:14px;}
  .v1u2cmp figure{margin:0; display:flex; align-items:center; gap:14px; background:#F7EEDB; border-radius:14px; padding:8px 16px;}
  .v1u2cmp img{width:150px; height:84px; object-fit:cover; border-radius:10px;}
  .v1u2cmp figcaption{font-size:16px; color:#3A4657;} .v1u2cmp figcaption b{font-size:21px; color:#16233A;}
"""
