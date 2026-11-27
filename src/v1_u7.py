"""1-7 배포.

배포란 → 비유(내 컴퓨터의 문서 파일 → 공유 링크 · 애니메이션) → localhost · 내부망 · 외부망(애니메이션) · 주소별 접속 범위 → 흐름(GitHub → Vercel → 주소)
→ GitHub에서 저장소 만들기(github.com/new) → 공개 · 비공개(배포 · 공유 → 공개) → 올리기 전 점검 → 올리기(말로) → Vercel 가져오기 · 주소 → push 하면 자동 재배포 → 실습.
사실 출처: docs.github.com (Creating a new repository · Adding locally hosted code to GitHub) · cli.github.com (gh auth login) · vercel.com/docs/git · vercel.com/docs/deployments/generated-urls
· vercel.com/docs/plans/hobby · docs.github.com (plans)
Git 개념(commit · push)은 1-5 에서 설명 — 여기서는 다시 설명하지 않는다.
"""
import viz2
from deck import flow, lab, light
from hx import code, esc, note
from stats_hx import src
from v1kit import brief, chat, shot, labcard, tstep, go

T = "1-7"


def slides():
    return [
        # ── 배포란 · 비유
        light("배포", viz2.pair(
            "배포 전", [("주소", "file:// · localhost — 내 컴퓨터 안"), ("열 수 있는 사람", "나 혼자"), ("컴퓨터를 끄면", "앱도 꺼짐")],
            "배포 후", [("주소", "mini-notion.vercel.app 형식"), ("열 수 있는 사람", "주소를 받은 누구나"), ("컴퓨터를 끄면", "그대로 열림")])
              + note("배포", "내 컴퓨터에서 돌던 앱을 인터넷 주소로 공개하는 일"), T),
        light("문서 파일과 공유 링크", _share(), T),
        light("localhost · 내부망 · 외부망", _net(), T),
        light("주소별 접속 범위", viz2.maprows([
            ("file:// · localhost", "이 컴퓨터만", "만들며 확인"),
            ("192.168.0.12:8000", "같은 Wi-Fi · 회사망 기기", "내 휴대폰 화면 확인"),
            ("mini-notion.vercel.app", "인터넷의 누구나", "공유")], "주소", "열리는 범위")
              + src(("RFC 1918 · 사설 주소", "https://www.rfc-editor.org/rfc/rfc1918")), T),
        light("배포 흐름", flow([
            ("내 컴퓨터", "앱 · 커밋"), ("GitHub", "코드 보관"), ("Vercel", "코드를 가져가 공개"),
            ("주소", "*.vercel.app"), ("팀원", "링크로 접속")], hl=2)
              + viz2.tiles([
                  ("연결 ① 내 폴더 → GitHub", "github.com 에서 빈 저장소 생성 · Claude Code 가 업로드"),
                  ("연결 ② GitHub → Vercel", "한 번 연결해 두면 이후 자동")], 2), T),
        # ── GitHub 에 올리기
        light("GitHub 저장소 만들기", _ghnew()
              + src(("GitHub Docs · Creating a new repository", "https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository")), T),
        light("공개 · 비공개 저장소", viz2.pair(
            "공개 (public)", [("누가 보나", "인터넷의 누구나 · 코드 · 커밋 기록까지"), ("맞는 경우", "배포 · 공유하는 앱 · 이 실습")],
            "비공개 (private)", [("누가 보나", "나와 초대한 사람만"), ("맞는 경우", "회사 업무 코드")], hl="l")
              + note("공개 저장소", "올린 파일 · 커밋 기록 전부 공개 → 올리기 전 점검 필수")
              + src(("GitHub Docs · About repositories", "https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories")), T),
        light("올리기 전 점검", viz2.tiles([
            ("키 · 비밀번호", "코드 · 파일에 들어 있지 않은가"), ("개인정보", "기획서 · 예시 페이지에 실제 이름 · 연락처 없음"),
            ("커밋 이메일", "공개 저장소면 누구나 봄 · GitHub noreply 이메일"), ("Hobby 는 개인 · 비상업", "회사 서비스는 Pro 이상")], 2)
              + note("점검 요청 예", "「올리기 전에 키 · 개인정보가 들어간 파일이 있는지 찾아 줘」")
              + src(("GitHub Docs · commit email", "https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address"),
                    ("Vercel Terms", "https://vercel.com/legal/terms"), ("Hobby", "https://vercel.com/docs/plans/hobby")), T),
        light("GitHub 업로드 요청", chat([
            ("me", "이 폴더를 GitHub 저장소 https://github.com/내계정/mini-notion 에 올려 줘"),
            ("ai", "git remote add origin … 과 git push -u origin main 을 실행해도 될까요?"),
            ("me", "응"),
            ("ai", "완료 · 지금까지의 커밋을 mini-notion 저장소에 올림")], "Claude Code 대화")
              + note("Claude가 쓰는 명령", "git remote add — 저장소 주소 등록 · git push — 지금까지의 커밋 올리기")
              + src(("GitHub Docs · Adding locally hosted code to GitHub", "https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github")), T),
        light("업로드한 저장소 확인", '<div class="twocol"><div>'
              + code("github.com/내계정/mini-notion · 예", esc(
                  "mini-notion/\n├── index.html\n├── style.css\n├── app.js\n├── 기획서.md\n└── 개발계획.md"))
              + "</div><div>" + viz2.tiles([
                  ("파일 목록", "내 폴더와 동일"), ("커밋 기록", "태스크마다 남긴 커밋"), ("Public 표시", "저장소 이름 옆")], 1)
              + "</div></div>", T),
        # ── Vercel
        light("Vercel 프로젝트 가져오기", flow([
            ("Vercel 로그인", "GitHub 계정"), ("새 프로젝트", "Git 저장소 가져오기"), ("mini-notion 선택", "저장소 접근 허용"),
            ("Deploy", "설정은 기본값"), ("주소 발급", "1분 안팎")], hl=2)
              + note("저장소가 안 보이면", "GitHub 쪽에서 Vercel 에 그 저장소 접근을 허용")
              + note("설정", "HTML · CSS · JS 만 있는 폴더 → 빌드 설정을 바꿀 것 없음"), T),
        light("배포 주소", viz2.tiles([
            ("프로젝트 기본 주소", "프로젝트명.vercel.app"), ("배포마다 고유 주소", "버전마다 따로 생김 · 기본 공개")], 2)
              + code("배포 완료 · 예", esc("✓ Production   https://mini-notion.vercel.app\n  이번 배포     https://mini-notion-a1b2c3.vercel.app"))
              + note("공유할 주소", "프로젝트 기본 주소 · 다시 배포해도 바뀌지 않음")
              + src(("Vercel · Generated URLs", "https://vercel.com/docs/deployments/generated-urls")), T),
        light("배포 화면", shot("notion_mobile.webp", "배포 주소 · 390px 휴대폰 화면", [
            ("내 컴퓨터와 차이", "주소만 다름 · 코드 동일"), ("개발 계획 완료 기준", "모바일 폭에서 가로 스크롤 없음"),
            ("확인 방법", "주소를 휴대폰으로 보내 열기"), ("깨질 때", "화면 캡처 첨부 · 수정 요청")]), T),
        # ── 재배포
        light("수정 → 재배포", '<div class="twocol"><div>'
              + chat([("me", "체크한 할 일 글자를 연한 초록으로 바꿔 줘"),
                      ("ai", "style.css 의 체크 상자 블록 색 변경 완료"),
                      ("me", "커밋하고 GitHub에 올려 줘"),
                      ("ai", "커밋 「체크한 할 일 색 변경」 → push 완료 · Vercel 새 배포 시작")], "Claude Code 대화")
              + "</div><div>"
              + viz2.tiles([("① 수정 요청", "Claude Code"), ("② 내 컴퓨터에서 확인", "만들 때와 같음"), ("③ 커밋 · push", "업로드 요청"),
                            ("④ Vercel 자동 배포", "push 감지 · 1~2분"), ("⑤ 같은 주소에 반영", "새 링크 없음")], 1)
              + "</div></div>"
              + src(("Vercel · Git", "https://vercel.com/docs/git")), T),
        # ── 실습
        labcard("1-7", "내 앱 배포", T, "내 앱 폴더", "공개 주소", ["GitHub 공개 저장소", "Vercel 배포"]),
        brief("1-7", T,
              ["올리기 전 키 · 개인정보 점검 요청", "github.com 에서 공개 저장소 만들기", "올리기 요청",
               "Vercel 가져오기 · Deploy", "수정 → 커밋 · push 요청"],
              [("목표", "이 폴더를 GitHub 에 올리기"), ("저장소", "이름 · 공개"), ("올리기 전", "키 · 개인정보 점검"),
               ("하지 말 것", "기존 커밋 지우기 · 키 · 개인정보 올리기")],
              ["GitHub", "공개", "push", "Vercel"],
              ["저장소 주소가 열림", "배포 주소가 열림", "수정 뒤 같은 주소에 반영"],
              "오류 문구 그대로 전달", folder="내 앱 폴더"),
        tstep("1-7", 3, "올리기", T, ask=("Claude Code 입력창", "이 폴더를 GitHub 저장소\nhttps://github.com/내계정/mini-notion 에 올려 줘"),
              rows=[("주소", "2단계에서 복사한 주소"), ("승인", "패널에 뜬 명령 확인 → 허용"), ("다음", "올린 결과 확인")]),
        light("실습 1-7 확인", viz2.maprows([
            ("저장소", "github.com/내계정/저장소 이름", "파일 · 커밋 · Public"), ("배포 주소", "프로젝트명.vercel.app", "PC · 휴대폰에서 열림"),
            ("재배포", "push 1~2분 뒤 새로고침", "고친 곳이 보임"), ("올리기 전 점검", "키 · 개인정보 없음", "Claude Code 점검 결과")], "볼 것", "확인")
              + note("공유", "배포 주소로 결과 공유"), T),
    ]


def _ghnew():
    """github.com/new 화면 모형 — 이름 · Public · README 끔 → Create repository → 빈 저장소 주소."""
    def row(n, k, v, d):
        return f'<div class="v17gR" style="--d:{d}s"><i>{n}</i><b>{k}</b>{v}</div>'
    form = ('<div class="v17gW"><div class="v17gU">github.com/new</div><div class="v17gF">'
            '<div class="v17gH">Create a new repository</div>'
            + row("①", "Repository name", '<span class="v17gI">mini-notion</span>', .4)
            + row("②", "Visibility", '<span class="v17gI">Public</span>', 1.2)
            + row("③", "Add README", '<span class="v17gO">Off</span>', 2.0)
            + row("④", "", '<span class="v17gB">Create repository</span>', 2.8)
            + '</div></div>')
    side = ('<div class="v17gS">'
            '<p style="--d:.4s"><i>①</i><b>이름</b><span>mini-notion · 영문 · 하이픈</span></p>'
            '<p style="--d:1.2s"><i>②</i><b>Public</b><span>누구나 열람 · 배포 · 공유용</span></p>'
            '<p style="--d:2.0s"><i>③</i><b>README · .gitignore · 라이선스 없이</b><span>빈 저장소 · 내 커밋과 충돌 없음</span></p>'
            '<p style="--d:2.8s"><i>④</i><b>Create repository</b><span>빈 저장소 생성</span></p></div>')
    res = ('<div class="v17gX" style="--d:3.8s"><b>만든 뒤 화면</b><span>빈 저장소 · Quick setup</span>'
           '<tt>https://github.com/내계정/mini-notion.git</tt><em>이 주소를 Claude Code 에 전달</em></div>')
    return f'<div class="v17g">{form}{side}</div>{res}'


def _net():
    """내 컴퓨터(localhost) → 공유기 안 내부망(사설 주소 · 같은 Wi-Fi) → 외부망(인터넷 · 밖에서 사설 주소 X → 배포 서버 주소 O)."""
    def dev(name, addr, ok, d, cls=""):
        return (f'<div class="v1nwd {cls}" style="--d:{d}s"><b>{name}</b><tt>{addr}</tt>'
                f'<i class="{"y" if ok else "n"}">{"열림" if ok else "안 열림"}</i></div>')
    return ('<div class="v1nwO" style="--d:5s; --bc:#8FA3BC; --bg:#F6F8FB">'
            '<div class="v1nwT" style="--d:5s">외부망 · 인터넷</div>'
            '<div class="v1nwI" style="--d:2.6s; --bc:#2B579A; --bg:#EEF3FA">'
            '<div class="v1nwT" style="--d:2.6s">내부망 · 공유기 안 · 같은 Wi-Fi</div>'
            '<div class="v1nwP" style="--d:.3s"><div class="v1nwh">내 컴퓨터</div>'
            + dev("내 브라우저", "localhost:8000", True, .9) + '</div>'
            '<div class="v1nwG">'
            + dev("팀원 노트북", "192.168.0.12:8000", True, 3.2) + dev("내 휴대폰", "192.168.0.12:8000", True, 3.8)
            + '</div></div>'
            '<div class="v1nwX">'
            + dev("집 · LTE 휴대폰", "192.168.0.12:8000", False, 5.8)
            + '<div class="v1nwS" style="--d:8.2s"><div class="v1nwh">Vercel 서버</div><tt>mini-notion.vercel.app</tt></div>'
            + dev("집 · LTE 휴대폰", "mini-notion.vercel.app", True, 9.6, "on")
            + '</div></div>')


def _share():
    """비유 — 내 컴퓨터의 문서 파일(나만 열림) → 공유 링크(링크를 받은 누구나) → 문서를 고치면 링크로 보는 사람에게 바로 반영."""
    ppl = "".join(f'<span class="v1shp" style="--d:{2.6 + i * .5:.1f}s">{n}</span>' for i, n in enumerate(("팀장", "팀원", "휴대폰")))
    return ('<div class="v1sh">'
            '<div class="v1shc" style="--d:.3s"><div class="v1shh">내 컴퓨터의 문서 파일</div>'
            '<div class="v1shf"><b>회의록.docx</b><small>내 컴퓨터 · 바탕화면</small></div>'
            '<div class="v1shw">열 수 있는 사람 · 나</div><div class="v1shm">= localhost</div></div>'
            '<i class="v1sha" style="--d:1.4s">→</i>'
            '<div class="v1shc on" style="--d:1.8s"><div class="v1shh">공유 링크</div>'
            '<div class="v1shl">https://… /회의록</div>'
            f'<div class="v1shps">{ppl}</div><div class="v1shm">= 배포 주소 · *.vercel.app</div></div></div>'
            '<div class="v1shu" style="--d:4.4s"><b>문서를 고치면</b><span>링크로 보는 사람에게 바로 반영</span><em>= 재배포 · push 하면 자동</em></div>')


CSS = """
  /* 1-7 · GitHub 저장소 만들기 (v17g) */
  .v17g{display:grid; grid-template-columns:600px 1fr; gap:26px; align-items:start; margin:0 0 16px;}
  .v17gW{border:1.5px solid #D0D7DE; border-radius:12px; background:#fff; overflow:hidden; box-shadow:0 6px 18px rgba(22,35,58,.12);}
  .v17gU{background:#F6F8FA; border-bottom:1px solid #D0D7DE; padding:8px 14px; font-family:var(--mono); font-size:14px; color:#57606A;}
  .v17gF{padding:16px 22px 20px; display:flex; flex-direction:column; gap:14px;}
  .v17gH{font-size:22px; font-weight:800; color:#1F2328; padding-bottom:10px; border-bottom:1px solid #D8DEE4;}
  .v17gR{display:grid; grid-template-columns:30px 170px 1fr; align-items:center; gap:10px; opacity:.35; animation:v17gOn .5s var(--d) forwards;}
  .v17gR i,.v17gS i{font-style:normal; font-size:18px; font-weight:800; color:#F28C28;}
  .v17gR b{font-size:16px; color:#1F2328;}
  .v17gI{border:1.5px solid #D0D7DE; border-radius:6px; padding:6px 12px; font-family:var(--mono); font-size:16px; color:#1F2328; background:#F6F8FA;}
  .v17gO{justify-self:start; border:1.5px solid #D0D7DE; border-radius:14px; padding:4px 14px; font-size:15px; font-weight:700; color:#57606A;}
  .v17gB{grid-column:2/span 2; justify-self:start; background:#1F883D; color:#fff; font-size:16px; font-weight:700; border-radius:6px; padding:8px 18px;}
  .v17gS{display:flex; flex-direction:column; gap:12px;}
  .v17gS p{margin:0; display:grid; grid-template-columns:30px 1fr; gap:2px 10px; background:#fff; border:1.5px solid #C9D6E6; border-radius:12px; padding:10px 14px;
    opacity:0; animation:v17gIn .5s var(--d) forwards;}
  .v17gS b{font-size:18px; color:#16233A;} .v17gS span{grid-column:2; font-size:16px; color:#3A4657;}
  .v17gX{display:flex; gap:16px; align-items:baseline; border:2px dashed #F28C28; border-radius:14px; padding:12px 20px; opacity:0; animation:v17gIn .6s var(--d) forwards;}
  .v17gX b{font-size:19px; color:#16233A;} .v17gX span{font-size:16px; color:#3A4657;}
  .v17gX tt{font-family:var(--mono); font-size:17px; font-weight:700; color:#1F3A5F; background:#EAF0F7; border-radius:16px; padding:5px 14px;}
  .v17gX em{margin-left:auto; font-style:normal; font-size:16px; font-weight:800; color:#E07A12;}
  @keyframes v17gOn{to{opacity:1}}
  @keyframes v17gIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v17gR,.v17gS p,.v17gX{opacity:1; animation:none}}
  /* 1-7 · 비유 두 컷 */
  /* 1-7 · 문서 파일과 공유 링크 (v1sh) */
  .v1sh{display:grid; grid-template-columns:1fr 50px 1fr; gap:12px; align-items:stretch; margin:4px 0 16px;}
  .v1shc{border:2px solid #C9D6E6; border-radius:16px; background:#fff; padding:18px 22px; display:flex; flex-direction:column; gap:12px;
    opacity:0; animation:v1shIn .6s var(--d) forwards;}
  .v1shc.on{border-color:#F28C28; background:#FFF8F0;}
  .v1shh{font-size:22px; font-weight:800; color:#16233A;}
  .v1shf{display:flex; flex-direction:column; gap:2px; border-left:6px solid #2B579A; background:#F4F6F9; border-radius:8px; padding:10px 14px;}
  .v1shf b{font-size:19px; color:#16233A;} .v1shf small{font-size:14px; color:#6B7785;}
  .v1shl{font-family:var(--mono); font-size:16px; font-weight:700; color:#1F3A5F; background:#EAF0F7; border-radius:20px; padding:9px 16px;}
  .v1shw{font-size:17px; color:#3A4657; font-weight:600;}
  .v1shps{display:flex; gap:10px;}
  .v1shp{font-size:15px; font-weight:700; color:#fff; background:#1F3A5F; border-radius:16px; padding:6px 14px; opacity:0; animation:v1shIn .5s var(--d) forwards;}
  .v1shm{margin-top:auto; font-size:17px; font-weight:800; color:#E07A12;}
  .v1sha{font-style:normal; align-self:center; text-align:center; font-size:34px; font-weight:800; color:#F28C28; opacity:0; animation:v1shIn .5s var(--d) forwards;}
  .v1shu{display:flex; gap:16px; align-items:baseline; border:2px dashed #F28C28; border-radius:14px; padding:14px 22px; opacity:0; animation:v1shIn .6s var(--d) forwards;}
  .v1shu b{font-size:20px; color:#16233A;} .v1shu span{font-size:18px; color:#3A4657;} .v1shu em{margin-left:auto; font-style:normal; font-size:17px; font-weight:800; color:#E07A12;}
  @keyframes v1shIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  /* 1-7 · localhost · 내부망 · 외부망 (v1nw) */
  .v1nwO{display:grid; grid-template-columns:1.6fr 1fr; gap:16px; border:2px dashed transparent; border-radius:18px; padding:34px 16px 16px; position:relative;
    animation:v1nwB .8s var(--d) forwards;}
  .v1nwI{display:grid; grid-template-columns:1fr 1fr; gap:14px; border:2px solid transparent; border-radius:16px; padding:34px 14px 14px; position:relative;
    animation:v1nwB .8s var(--d) forwards;}
  .v1nwT{position:absolute; top:7px; left:16px; font-size:18px; font-weight:800; color:#1F3A5F; opacity:0; animation:v1nwIn .6s var(--d) forwards;}
  .v1nwO > .v1nwT{color:#5A6B80;}
  .v1nwP,.v1nwS{border:2px solid #16233A; border-radius:14px; background:#fff; padding:12px 14px; display:flex; flex-direction:column; gap:10px;
    opacity:0; animation:v1nwIn .6s var(--d) forwards;}
  .v1nwS{border-color:#F28C28; background:#FFF8F0;}
  .v1nwS tt{font-family:var(--mono); font-size:18px; font-weight:700; color:#B45F06;}
  .v1nwh{font-size:22px; font-weight:800; color:#16233A;}
  .v1nwG,.v1nwX{display:flex; flex-direction:column; gap:12px;}
  .v1nwd{display:grid; grid-template-columns:1fr auto; gap:2px 10px; align-items:center; background:#fff; border:1.5px solid #C9D6E6; border-radius:12px;
    padding:12px 14px; opacity:0; animation:v1nwIn .6s var(--d) forwards;}
  .v1nwd b{font-size:19px; color:#16233A;}
  .v1nwd tt{grid-column:1; font-family:var(--mono); font-size:17px; color:#3A4657;}
  .v1nwd i{grid-row:1/span 2; grid-column:2; font-style:normal; font-size:16px; font-weight:800; border-radius:12px; padding:6px 12px;}
  .v1nwd i.y{color:#fff; background:#2E8B57;} .v1nwd i.n{color:#fff; background:#C0392B;}
  .v1nwd.on{border-color:#F28C28;}
  @keyframes v1nwB{to{border-color:var(--bc); background:var(--bg)}}
  @keyframes v1nwIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v1nwT,.v1nwP,.v1nwS,.v1nwd{opacity:1; animation:none} .v1nwO,.v1nwI{animation:none; border-color:var(--bc); background:var(--bg)}}
  @media print{.v1shc,.v1shp,.v1sha,.v1shu{opacity:1; animation:none}}
"""
