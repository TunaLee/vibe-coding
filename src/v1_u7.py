"""1-7 배포.

배포란 → 비유(주방 안 시식 → 가게 문 열기 · 생성 그림) → localhost 의 범위 → 흐름(GitHub → Vercel → 주소)
→ GitHub에 올리기(gh · 말로) → Vercel 가져오기 · 주소 → push 하면 자동 재배포 · Production / Preview → 공개 전 확인 → 실습.
사실 출처: cli.github.com (gh 설치 · gh auth login · gh repo create) · vercel.com/docs/git · vercel.com/docs/deployments/generated-urls
· vercel.com/docs/plans/hobby · docs.github.com (plans)
Git 개념(commit · push)은 1-5 에서 설명 — 여기서는 다시 설명하지 않는다.
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v1kit import brief, chat, shot

T = "1-7"


def slides():
    return [
        # ── 배포란 · 비유
        light("배포", viz2.pair(
            "배포 전", [("주소", "localhost — 내 컴퓨터 안"), ("열 수 있는 사람", "나 혼자"), ("컴퓨터를 끄면", "앱도 꺼짐")],
            "배포 후", [("주소", "room-booking.vercel.app 형식"), ("열 수 있는 사람", "주소를 받은 누구나"), ("컴퓨터를 끄면", "그대로 열림")])
              + note("배포", "내 컴퓨터에서 돌던 앱을 인터넷 주소로 공개하는 일"), T),
        light("비유 · 가게 문 열기", '<div class="v1u7cut">'
              '<figure><img src="img/v1_u7_kitchen.webp" alt="주방 안에서 혼자 맛보기"/><figcaption><b>주방 안 시식</b><span>localhost · 나만 확인</span></figcaption></figure>'
              '<i>→</i>'
              '<figure><img src="img/v1_u7_open.webp" alt="가게 문 열기"/><figcaption><b>가게 문 열기</b><span>배포 · 주소로 누구나</span></figcaption></figure></div>'
              + viz2.tiles([("가게 주소", "배포 주소 · *.vercel.app"), ("메뉴 교체 · 재진열", "재배포 · push 하면 자동")], 2)
              + src(("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")), T),
        light("localhost의 범위", viz2.tiles([
            ("내 브라우저", "localhost 주소로 열림"), ("팀원 노트북", "같은 주소를 넣어도 안 열림"), ("내 휴대폰", "안 열림 · 다른 기기")], 3)
              + code("1-6 에서 띄운 주소 · 예", esc("http://localhost:3000"))
              + note("localhost", "「지금 이 컴퓨터」를 가리키는 주소 · 다른 기기에서는 그 기기 자신"), T),
        light("배포 흐름", flow([
            ("내 컴퓨터", "앱 · 커밋"), ("GitHub", "코드 보관 (1-5)"), ("Vercel", "코드를 가져가 공개"),
            ("주소", "*.vercel.app"), ("팀원", "링크로 접속")], hl=2)
              + viz2.tiles([
                  ("연결 ① Claude Code → GitHub", "gh 로 저장소 생성 · 업로드 · 요청 한 줄"),
                  ("연결 ② GitHub → Vercel", "한 번 연결해 두면 이후 자동")], 2), T),
        # ── GitHub 에 올리기
        light("gh · GitHub 명령 도구", viz2.tiles([
            ("gh", "GitHub 공식 명령 도구 · 저장소 만들기 · 올리기"), ("Claude Code가 실행", "명령 암기 불필요"),
            ("한 번만", "설치 · 로그인 연결")], 3)
              + '<div class="twocol"><div>' + code("macOS", esc("brew install gh")) + "</div><div>"
              + code("Windows", esc("winget install --id GitHub.cli --source winget")) + "</div></div>"
              + note("Windows", "설치 뒤 터미널 새 창에서 gh 인식")
              + src(("GitHub CLI", "https://cli.github.com/")), T),
        light("gh 로그인 연결", flow([
            ("gh auth login", "터미널에서 실행"), ("GitHub.com · HTTPS", "기본값 선택"), ("브라우저 인증", "코드 입력 · 승인"),
            ("연결 완료", "내 계정으로 명령 실행")], hl=2)
              + code("터미널 · 예", esc("$ gh auth login\n? Where do you use GitHub?  GitHub.com\n...\n✓ Logged in as 내계정"))
              + note("직접 할 것", "브라우저 승인은 사람이 · 비밀번호를 Claude에게 알려 주지 않음")
              + src(("gh auth login", "https://cli.github.com/manual/gh_auth_login")), T),
        light("GitHub 업로드 요청", chat([
            ("me", "이 폴더를 GitHub 비공개 저장소 room-booking 으로 올려 줘"),
            ("ai", "gh repo create room-booking --private --source=. --push 를 실행해도 될까요?"),
            ("me", "응"),
            ("ai", "완료 · https://github.com/내계정/room-booking")], "Claude Code 대화 예")
              + note("Claude가 쓰는 명령", "gh repo create — 원격 저장소 만들기 + 지금까지의 커밋 올리기")
              + src(("gh repo create", "https://cli.github.com/manual/gh_repo_create")), T),
        light("공개 · 비공개 저장소", viz2.pair(
            "공개 (public)", [("누가 보나", "인터넷의 누구나 코드를 봄"), ("맞는 경우", "공개해도 되는 연습 코드")],
            "비공개 (private)", [("누가 보나", "나와 초대한 사람만"), ("맞는 경우", "회사 업무 · 이 실습")], hl="r")
              + note("GitHub Free", "비공개 저장소도 개수 제한 없음 · 일부 기능만 유료")
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("올라간 저장소 확인", '<div class="twocol"><div>'
              + code("github.com/내계정/room-booking · 예", esc(
                  "room-booking/\n├── index.html\n├── style.css\n├── app.js\n├── 기획서.md     1-3\n└── PRD.md        1-4"))
              + "</div><div>" + viz2.tiles([
                  ("파일 목록", "내 폴더와 동일"), ("커밋 기록", "1-5 · 1-6 커밋"), ("자물쇠 표시", "비공개 저장소")], 1)
              + "</div></div>", T),
        # ── Vercel
        light("Vercel 프로젝트 가져오기", flow([
            ("Vercel 로그인", "GitHub 계정 (1-2)"), ("새 프로젝트", "Git 저장소 가져오기"), ("room-booking 선택", "저장소 접근 허용"),
            ("Deploy", "설정은 기본값"), ("주소 발급", "1분 안팎")], hl=2)
              + note("저장소가 안 보이면", "GitHub 쪽에서 Vercel 에 그 저장소 접근을 허용")
              + note("설정", "HTML · CSS · JS 만 있는 폴더 → 빌드 설정을 바꿀 것 없음"), T),
        light("배포 주소", viz2.tiles([
            ("프로젝트 기본 주소", "프로젝트명.vercel.app"), ("배포마다 고유 주소", "버전마다 따로 생김 · 기본 공개")], 2)
              + code("배포 완료 · 예", esc("✓ Production   https://room-booking.vercel.app\n  이번 배포     https://room-booking-a1b2c3.vercel.app"))
              + note("공유할 주소", "프로젝트 기본 주소 · 다시 배포해도 바뀌지 않음")
              + src(("Vercel · Generated URLs", "https://vercel.com/docs/deployments/generated-urls")), T),
        light("배포 주소로 연 화면", shot("room_mobile.webp", "배포 주소 · 390px 휴대폰 화면", [
            ("localhost 와 차이", "주소만 다름 · 코드 동일"), ("PRD 완료 기준", "모바일 폭에서 가로 스크롤 없음"),
            ("확인 방법", "주소를 휴대폰으로 보내 열기"), ("깨질 때", "화면 캡처 첨부 · 수정 요청 (1-6)")]), T),
        # ── 재배포
        light("수정 → 재배포", '<div class="twocol"><div>'
              + chat([("me", "예약 칸 색을 연한 초록으로 바꿔 줘"),
                      ("ai", "style.css 의 .cell.busy 색 변경 완료"),
                      ("me", "커밋하고 GitHub에 올려 줘"),
                      ("ai", "커밋 「예약 칸 색 변경」 → push 완료 · Vercel 새 배포 시작")], "Claude Code 대화 예")
              + "</div><div>"
              + viz2.tiles([("① 수정 요청", "Claude Code"), ("② localhost 확인", "1-6 과 같음"), ("③ 커밋 · push", "업로드 요청"),
                            ("④ Vercel 자동 배포", "push 감지 · 1~2분"), ("⑤ 같은 주소에 반영", "새 링크 없음")], 1)
              + "</div></div>"
              + src(("Vercel · Git", "https://vercel.com/docs/git")), T),
        # ── 공개 전 확인
        light("공개 전 확인", viz2.tiles([
            ("키 · 비밀번호", "코드 · 파일에 들어 있지 않은가"), ("개인정보", "실제 이름 · 연락처 대신 예시 값"),
            ("배포 주소는 공개", "주소를 아는 누구나 열 수 있음"), ("Hobby 는 개인 · 비상업", "회사 서비스는 Pro 이상")], 2)
              + note("점검 요청 예", "「올리기 전에 키 · 개인정보가 들어간 파일이 있는지 찾아 줘」")
              + src(("Vercel Terms", "https://vercel.com/legal/terms"), ("Hobby", "https://vercel.com/docs/plans/hobby")), T),
        # ── 실습
        lab("1-7", "내 앱 배포", T, "1-6 에서 만든 앱을 GitHub 에 올리고 Vercel 주소로 공개",
            ["gh 설치 · 로그인 연결", "Claude Code 에 저장소 생성 · 업로드 요청",
             "Vercel 에서 저장소 가져오기 · Deploy → 휴대폰으로 열기", "한 곳 고쳐 push → 같은 주소에 반영 확인"],
            ["저장소에 내 파일 · 커밋 기록", "*.vercel.app 주소로 앱이 열림", "수정 한 번이 재배포로 반영"],
            files="1-6 의 내 앱 폴더"),
        brief("1-7", T,
              ["gh auth login (브라우저 승인)", "올리기 전 키 · 개인정보 점검 요청", "저장소 만들고 올리기 요청",
               "Vercel 가져오기 · Deploy", "수정 → 커밋 · push 요청"],
              [("목표", "이 폴더를 GitHub 에 올리기"), ("저장소", "이름 · 비공개"), ("올리기 전", "키 · 개인정보 점검"),
               ("하지 말 것", "기존 커밋 지우기 · 공개 저장소")],
              ["GitHub", "비공개", "gh", "push", "Vercel"],
              ["저장소 주소가 열림", "배포 주소가 열림", "수정 뒤 같은 주소에 반영"],
              "오류 문구 그대로 전달", folder="1-6 의 내 앱 폴더"),
        light("실습 1-7 확인", viz2.maprows([
            ("저장소", "github.com/내계정/저장소 이름", "파일 · 커밋 · 자물쇠"), ("배포 주소", "프로젝트명.vercel.app", "PC · 휴대폰에서 열림"),
            ("재배포", "push 1~2분 뒤 새로고침", "고친 곳이 보임"), ("공개 전 점검", "키 · 개인정보 없음", "Claude Code 점검 결과")], "볼 것", "확인")
              + note("공유", "배포 주소를 1-8 결과 공유에 사용"), T),
    ]


CSS = """
  /* 1-7 · 비유 두 컷 */
  .v1u7cut{display:grid; grid-template-columns:1fr 40px 1fr; gap:10px; align-items:center; margin:0 0 16px;}
  .v1u7cut figure{margin:0; border:1.5px solid #D9DDE3; border-radius:14px; overflow:hidden; background:#F7EEDB;}
  .v1u7cut img{display:block; width:100%; aspect-ratio:16/9; object-fit:cover;}
  .v1u7cut figcaption{display:flex; gap:12px; align-items:baseline; padding:10px 14px; background:#fff;}
  .v1u7cut figcaption b{font-size:19px; color:#16233A;} .v1u7cut figcaption span{font-size:15px; color:#E07A12; font-weight:700;}
  .v1u7cut i{font-style:normal; text-align:center; font-size:28px; font-weight:800; color:#F28C28;}
"""
