"""1-5 Git · GitHub 기초 (10분).

배경(최종_진짜최종) → 비유(세이브 포인트) → Git · commit · 되돌리기 → 말로 시키기 → GitHub · push / pull → 실습(첫 커밋).
사실 출처: git-scm.com/docs/git-commit · git-scm.com/docs/git · docs.github.com/en/get-started/using-git/about-git
"""
import viz2
from deck import flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
from v1kit import brief, chat, labcard, tstep
from v3kit import phmap

T = "1-5"

LOG = [("dfb369b", "첫 화면 완성", "index.html 생성"), ("8fcbe80", "버튼 추가", "로그인 버튼"), ("0b491e3", "색상 수정", "버튼 주황색")]


def stack():
    """커밋이 아래에서 위로 하나씩 쌓임(v1 → v3) + 같은 기록의 터미널 출력. 실제 git 으로 만든 해시."""
    cards = "".join(
        f'<div class="v1cm" style="animation-delay:{.4 + i * .9:.1f}s"><span class="v">v{i + 1}</span><code>{h}</code><b>{m}</b><small>{d}</small></div>'
        for i, (h, m, d) in enumerate(LOG))
    term = code("터미널 · git log --oneline", esc("\n".join(f"{h} {m}" for h, m, _ in reversed(LOG))))
    return f'<div class="v1cmw"><div class="v1cms"><div class="v1cmh">기록 저장소</div>{cards}</div><div>{term}</div></div>'


FILES = [("발표자료.pptx", "10월 2일"), ("발표자료_v2.pptx", "10월 5일"), ("발표자료_최종.pptx", "10월 8일"),
         ("발표자료_최종_수정.pptx", "10월 9일"), ("발표자료_진짜최종.pptx", "10월 10일"), ("발표자료_진짜진짜마지막.pptx", "10월 11일")]


def files():
    """폴더 창에 pptx 사본이 하나씩 늘어남 + 생기는 문제 세 줄."""
    rows = "".join(f'<div class="v1fr" style="--d:{.3 + i * .55:.2f}s"><i>P</i><b>{n}</b><small>{d}</small></div>'
                   for i, (n, d) in enumerate(FILES))
    d0 = .3 + len(FILES) * .55
    probs = "".join(f'<div class="v1fp" style="--d:{d0 + i * .4:.2f}s"><b>{h}</b><span>{t}</span></div>' for i, (h, t) in enumerate([
        ("어느 게 최신", "날짜 · 파일을 열어 봐야 앎"), ("무엇이 바뀌었나", "두 파일을 나란히 놓고 비교"),
        ("이전 상태 복구", "사본을 지웠으면 불가")]))
    return (f'<div class="v1fnw"><div class="v1fd"><div class="v1fdh">내 문서 › 팀 발표</div>{rows}</div>'
            f'<div class="v1fps">{probs}</div></div>')


def gitflow():
    """작업 폴더 → (add) 스테이징 → (commit) 로컬 저장소 → (push) GitHub · (pull) 되돌아옴. 구조는 Pro Git 「세 가지 상태」 + 원격."""
    K = 2.2  # 장면 사이 간격 배율 (전체 약 27초)

    def chip(t, d, o=None, cls=""):
        st = f"--d:{d * K:.2f}s" + (f"; --o:{o * K:.2f}s" if o else "")
        return f'<div class="v1gc {cls}{" o" if o else ""}" style="{st}">{t}</div>'

    def cm(h, m, d, cls=""):
        return f'<div class="v1gk {cls}" style="--d:{d * K:.2f}s">{f"<tt>{h}</tt>" if h else ""}<b>{m}</b></div>'

    def pill(cmd, d1, d2=None):
        an = f"--d1:{d1 * K:.2f}s; --d2:{(d2 if d2 else d1) * K:.2f}s"
        return f'<div class="v1gp" style="{an}"><tt>{cmd}</tt><i>→</i></div>'

    wd = (chip("index.html · 수정", 1.0, 2.0) + chip("style.css · 수정", 6.0, 6.8)
          + chip("index.html · 문구 바뀜", 11.6, cls="pl"))
    stg = chip("index.html", 2.2, 3.4) + chip("style.css", 7.0, 7.8)
    loc = cm("dfb369b", "첫 화면 완성", .2) + cm("8fcbe80", "버튼 추가", 3.6) + cm("0b491e3", "색상 수정", 8.0) + cm("", "문구 수정 · 받아 옴", 11.2, "pl")
    rem = cm("dfb369b", "첫 화면 완성", .2) + cm("8fcbe80", "버튼 추가", 5.0) + cm("0b491e3", "색상 수정", 9.0) + cm("", "문구 수정 · 다른 컴퓨터", 10.0, "pl")

    def col(name, en, body, cls=""):
        return f'<div class="v1gz {cls}"><div class="v1gzh"><b>{name}</b><small>{en}</small></div><div class="v1gzb">{body}</div></div>'

    return ('<div class="v1g"><div class="v1gtop"><span class="me">내 컴퓨터</span><span class="net">인터넷</span></div>'
            '<div class="v1grow">'
            + col("작업 폴더", "working directory · 파일 수정", wd)
            + pill("git add", 1.8, 6.6)
            + col("스테이징 영역", "staging area · 커밋할 파일", stg)
            + pill("git commit", 3.2, 7.6)
            + col("로컬 저장소", "repository · 커밋 기록", loc)
            + pill("git push", 4.6, 8.6)
            + col("GitHub", "remote · 원격 저장소", rem, "rm")
            + f'</div><div class="v1gpull" style="--d1:{10.8 * K:.2f}s; --d2:{10.8 * K:.2f}s"><i>←</i><tt>git pull</tt><span>원격의 새 커밋을 받아 내 폴더에 합침</span></div></div>')


def diffflow():
    """Git 이 계속 비교하는 모습 — 네 구역에 파일 내용이 그대로 보이고, 이웃 구역 사이의 차이가 diff 창 두 개에 나타난다.
    편집 두 번(색 바꿈 · 줄 추가) → diff 가 늘어남 → add (diff 가 스테이징↔저장소 쪽으로 이동) → commit (diff 0) → push. 15초 · 한 번."""
    A, B, C = ".btn { color: navy; }", ".btn { color: orange; }", ".btn { padding: 8px; }"
    V0 = [("body { margin: 0; }", ""), (A, "")]
    V1 = [("body { margin: 0; }", ""), (B, "c")]
    V2 = [("body { margin: 0; }", ""), (B, "c"), (C, "c")]

    def snap(lines, a, b=99, tag="", hl=True):
        ln = "".join(f'<div class="v2l{" c" if (k and hl) else ""}"><i>{i + 1}</i><tt>{t}</tt></div>' for i, (t, k) in enumerate(lines))
        return f'<div class="v2s" style="--a:{a}s;--b:{b}s">{ln}{f"<em>{tag}</em>" if tag else ""}</div>'

    zones = [
        ("작업 폴더", "내가 고치는 파일", snap(V0, 0, 2, "", False) + snap(V1, 2, 4, "수정됨 · 1줄") + snap(V2, 4, 10, "수정됨 · 2줄") + snap(V2, 10, 99, "", False)),
        ("스테이징", "git add 로 담은 것", snap(V0, 0, 7, "", False) + snap(V2, 7, 10, "커밋 대기") + snap(V2, 10, 99, "", False)),
        ("로컬 저장소", "마지막 커밋", snap(V0, 0, 10, "", False) + snap(V2, 10, 99, "새 커밋", False)),
        ("GitHub", "push 한 커밋", snap(V0, 0, 13, "", False) + snap(V2, 13, 99, "새 커밋", False)),
    ]
    zs = "".join(f'<div class="v2z{" gh" if i == 3 else ""}"><div class="v2zh"><b>{n}</b><small>{sub}</small></div><div class="v2zb">{body}</div></div>'
                 for i, (n, sub, body) in enumerate(zones))

    def dl(rows):
        return "".join(f'<div class="v2d {k}"><b>{"−" if k == "m" else "+"}</b><tt>{t}</tt></div>' for k, t in rows)

    empty = '<div class="v2d0">차이 없음</div>'
    d1 = (f'<div class="v2s" style="--a:0s;--b:2s">{empty}</div>'
          f'<div class="v2s" style="--a:2s;--b:4s">{dl([("m", A), ("p", B)])}</div>'
          f'<div class="v2s" style="--a:4s;--b:7s">{dl([("m", A), ("p", B), ("p", C)])}</div>'
          f'<div class="v2s" style="--a:7s;--b:99s">{empty}</div>')
    d2 = (f'<div class="v2s" style="--a:0s;--b:7s">{empty}</div>'
          f'<div class="v2s" style="--a:7s;--b:10s">{dl([("m", A), ("p", B), ("p", C)])}</div>'
          f'<div class="v2s" style="--a:10s;--b:99s">{empty}</div>')
    diffs = (f'<div class="v2dw"><div class="v2dp a"><div class="v2dh"><tt>git diff</tt><span>작업 폴더 ↔ 스테이징</span></div><div class="v2db">{d1}</div></div>'
             f'<div class="v2dp b"><div class="v2dh"><tt>git diff --staged</tt><span>스테이징 ↔ 로컬 저장소</span></div><div class="v2db">{d2}</div></div></div>')
    steps = [("편집 1 · 색 바꿈", 2), ("편집 2 · 줄 추가", 4), ("git add", 7), ("git commit", 10), ("git push", 13)]
    st = "".join(f'<span class="v2q" style="--d1:{t}s">{x}</span>' for x, t in steps)
    return f'<div class="v2q0">{st}</div><div class="v2zs">{zs}</div>{diffs}'

CSS = """
  /* 1-5 · diff — 네 구역의 파일 내용과 이웃 구역 사이 차이 (v2) */
  .v2q0{display:flex; gap:10px; margin-bottom:12px;}
  .v2q{font-family:var(--mono); font-size:14px; font-weight:700; color:#16233A; background:#EAF0F7; border-radius:14px; padding:5px 12px;
    animation:v1gHi 1.6s var(--d1);}
  .v2zs{display:grid; grid-template-columns:repeat(4,1fr); gap:10px;}
  .v2z{border:2px solid #C9D6E6; border-radius:12px; background:#F7F8FA; overflow:hidden;} .v2z.gh{border-color:#16233A;}
  .v2zh{padding:7px 10px; border-bottom:1.5px solid #D9DDE3; background:#fff;}
  .v2zh b{font-size:17px; color:#16233A; margin-right:6px;} .v2zh small{font-size:12px; color:#6B7785;}
  .v2zb{display:grid; padding:8px; min-height:118px;}
  .v2s{grid-area:1/1; opacity:0; animation:v2In .3s var(--a) forwards, v2Out .25s var(--b) forwards;}
  .v2l{display:grid; grid-template-columns:16px 1fr; align-items:center; padding:3px 4px; border-radius:5px;}
  .v2l i{font-style:normal; font-size:11px; color:#9AA6B5; font-family:var(--mono);}
  .v2l tt{font-family:var(--mono); font-size:13px; color:#16233A; white-space:nowrap;}
  .v2l.c{background:#FFE7CC;}
  .v2s em{display:inline-block; margin-top:6px; font-style:normal; font-size:12px; font-weight:800; color:#fff; background:#F28C28; border-radius:9px; padding:2px 9px;}
  .v2dw{display:grid; grid-template-columns:repeat(8,1fr); column-gap:10px; margin-top:12px;}
  .v2dp{border:1.5px solid #D9DDE3; border-radius:12px; background:#fff; overflow:hidden;}
  .v2dp.a{grid-column:1 / span 3; margin-left:50%;} .v2dp.b{grid-column:4 / span 3; margin-left:50%;}
  .v2dp{width:calc(100% + 0px);}
  .v2dh{display:flex; gap:10px; align-items:baseline; padding:7px 12px; background:#F4F6F9; border-bottom:1px solid #E3E6EA;}
  .v2dh tt{font-family:var(--mono); font-size:14px; font-weight:800; color:#16233A;} .v2dh span{font-size:12.5px; color:#6B7785;}
  .v2db{display:grid; min-height:96px;}
  .v2d{display:grid; grid-template-columns:18px 1fr; padding:4px 12px; background:#FDECEA;}
  .v2d.p{background:#E8F5E9;} .v2d b{color:#C62828; font-family:var(--mono);} .v2d.p b{color:#2E7D32;}
  .v2d tt{font-family:var(--mono); font-size:14px; color:#16233A;}
  .v2d0{padding:14px 12px; font-size:15px; font-weight:700; color:#6B7785;}
  @keyframes v2In{from{opacity:0; transform:translateY(-4px)} to{opacity:1; transform:none}}
  @keyframes v2Out{to{opacity:0; visibility:hidden}}
  @media print{.v2s{animation:none; opacity:0} .v2s[style*="--b:99s"]{opacity:1} .v2q{animation:none}}
  /* 1-5 · Git 작업 흐름 (v1g) */
  .v1gtop{display:grid; grid-template-columns:3fr 1fr; gap:10px; margin-bottom:8px;}
  .v1gtop span{font-size:14px; font-weight:800; text-align:center; padding:5px 0; border-radius:8px;}
  .v1gtop .me{background:#EAF0F7; color:#16233A;} .v1gtop .net{background:#16233A; color:#fff;}
  .v1grow{display:grid; grid-template-columns:1fr 86px 1fr 96px 1fr 86px 1fr; align-items:stretch;}
  .v1gz{border:2px solid #C9D6E6; border-radius:14px; background:#F7F8FA; display:flex; flex-direction:column; min-height:300px;}
  .v1gz.rm{border-color:#16233A;}
  .v1gzh{padding:10px 10px 8px; border-bottom:1.5px solid #D9DDE3; text-align:center;}
  .v1gzh b{display:block; font-size:19px; color:#16233A;} .v1gzh small{font-size:12px; color:#6B7785;}
  .v1gzb{flex:1; display:flex; flex-direction:column-reverse; justify-content:flex-end; gap:7px; padding:10px;}
  .v1gc{background:#FFF1E2; border:2px solid #F28C28; border-radius:9px; padding:8px 9px; font-size:15px; font-weight:700; color:#16233A; text-align:center;
    opacity:0; animation:v1gIn .6s var(--d) forwards;}
  .v1gc.o{animation:v1gIn .6s var(--d) forwards, v1gOut .6s var(--o) forwards;}
  .v1gk{background:#fff; border:2px solid #1F3A5F; border-radius:9px; padding:7px 9px; opacity:0; animation:v1gIn .4s var(--d) forwards;}
  .v1gk tt{display:block; font-family:var(--mono); font-size:12.5px; color:#6B7785; background:none; padding:0;}
  .v1gk b{font-size:15px; color:#16233A;}
  .v1gk.pl,.v1gc.pl{border-color:#2E7D5B; background:#EAF6EF;}
  .v1gp{display:flex; flex-direction:column; align-items:center; justify-content:center; gap:4px;}
  .v1gp tt{font-family:var(--mono); font-size:13.5px; font-weight:700; color:#16233A; background:#EAF0F7; border-radius:14px; padding:5px 8px; white-space:nowrap;
    animation:v1gHi 2.4s var(--d1), v1gHi 2.4s var(--d2);}
  .v1gp i{font-style:normal; font-size:26px; font-weight:800; color:#F28C28;}
  .v1gpull{margin-top:12px; display:flex; align-items:center; gap:12px; justify-content:center; border:2px dashed #2E7D5B; border-radius:12px; padding:9px;
    opacity:0; animation:v1gIn .4s var(--d1) forwards;}
  .v1gpull i{font-style:normal; font-size:24px; font-weight:800; color:#2E7D5B;}
  .v1gpull tt{font-family:var(--mono); font-size:15px; font-weight:700; color:#fff; background:#2E7D5B; border-radius:14px; padding:5px 12px;}
  .v1gpull span{font-size:16px; color:#16233A; font-weight:600;}
  @keyframes v1gIn{from{opacity:0; transform:translateY(-8px)} to{opacity:1; transform:none}}
  @keyframes v1gOut{from{opacity:1} to{opacity:0; height:0; padding:0; margin:0; border-width:0}}
  @keyframes v1gHi{0%,100%{background:#EAF0F7; color:#16233A} 15%,75%{background:#F28C28; color:#fff}}
  @media print{.v1gc,.v1gk,.v1gpull{opacity:1; animation:none} .v1gc.o{display:none} .v1gp tt{animation:none}}
  /* 1-5 · 파일 이름 버전 관리 (v1f) */
  .v1fnw{display:grid; grid-template-columns:1.25fr 1fr; gap:30px; align-items:center; margin-top:14px;}
  .v1fd{border:1.5px solid #D9DDE3; border-radius:14px; background:#fff; overflow:hidden;}
  .v1fdh{background:#F2F4F7; padding:10px 18px; font-size:15px; font-weight:800; color:#6B7785; border-bottom:1.5px solid #D9DDE3;}
  .v1fr{display:grid; grid-template-columns:34px 1fr auto; gap:12px; align-items:center; padding:11px 18px; border-bottom:1px solid #EEF0F3;
    opacity:0; animation:v1fIn .45s var(--d) forwards;}
  .v1fr:last-child{border-bottom:none; background:#FFF8F0;}
  .v1fr i{display:inline-flex; width:30px; height:36px; border-radius:4px; background:#D35230; color:#fff; font-style:normal; font-weight:900;
    font-size:15px; align-items:center; justify-content:center;}
  .v1fr b{font-size:20px; color:#16233A; font-weight:700;} .v1fr small{font-size:14px; color:#6B7785;}
  .v1fps{display:flex; flex-direction:column; gap:14px;}
  .v1fp{border-left:5px solid #F28C28; background:#FFF1E2; border-radius:10px; padding:14px 18px; opacity:0; animation:v1fIn .45s var(--d) forwards;}
  .v1fp b{display:block; font-size:21px; color:#16233A; margin-bottom:4px;} .v1fp span{font-size:16px; color:#4A5563;}
  @keyframes v1fIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v1fr,.v1fp{opacity:1; animation:none}}
  .v1cmw{display:grid; grid-template-columns:1.1fr 1fr; gap:26px; align-items:center;}
  .v1cms{display:flex; flex-direction:column-reverse; gap:10px; border:2px dashed #D9DDE3; border-radius:16px; padding:18px 18px 14px; background:#F7F8FA; min-height:280px; justify-content:flex-start;}
  .v1cmh{order:-1; font-size:14px; font-weight:800; color:#6B7785; text-align:center; margin-top:6px;}
  .v1cm{display:grid; grid-template-columns:44px 84px 1fr; align-items:baseline; gap:8px; padding:12px 16px; border-radius:12px; background:#fff; border:2px solid #1F3A5F;
        opacity:0; animation:v1cmIn .5s ease-out forwards;}
  .v1cm:last-of-type{border-color:#F28C28; background:#FFF8F0;}
  .v1cm .v{font-weight:900; color:#F28C28; font-size:18px;} .v1cm code{font-family:var(--mono); font-size:15px; color:#6B7785; background:none;}
  .v1cm b{font-size:19px; color:#16233A;} .v1cm small{grid-column:3; font-size:14.5px; color:#6B7785;}
  @keyframes v1cmIn{from{opacity:0; transform:translateY(-24px)} to{opacity:1; transform:none}}
  @media print{.v1cm{opacity:1; animation:none}}
"""


def slides():
    return [
        # ── 배경 → 비유
        light("파일 이름 버전 관리", files(), T),
        light("세이브 포인트", phmap(
            "v1_u5_savepoint.webp", "세이브 포인트 · 저장한 지점부터 다시 시작", "AI 생성 그림 · Z-Image Turbo (Apache 2.0)",
            "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo",
            viz2.maprows([
                ("세이브 포인트에서 저장", "커밋 (commit)", "지금 상태를 기록"), ("저장 슬롯 이름", "커밋 메시지", "「버튼 추가」"),
                ("저장 목록", "기록 (log)", "언제 · 무엇을"), ("불러오기", "되돌리기", "저장 시점 복원"),
                ("클라우드 저장", "GitHub", "다른 컴퓨터에서도")], "게임", "Git")), T),
        # ── Git · commit · 되돌리기
        light("커밋 구성", viz2.tiles([
            ("바뀐 내용", "어느 파일의 어느 줄"), ("메시지", "「버튼 추가」"),
            ("시각 · 작성자", "언제 · 누가"), ("고유 번호", "8fcbe80 같은 해시")], 4)
              + note("메시지", "무엇을 바꿨는지 한 줄 · 되돌릴 시점을 찾는 이름표"), T),
        light("커밋 기록 쌓기", stack()
              + src(("참고 · 혼잡스 「바이브코딩 한 장 지도」", "https://www.youtube.com/watch?v=HNtS6WGGhNU")), T),
        # ── GitHub · push / pull
        light("GitHub", viz2.pair(
            "Git", [("어디에", "내 컴퓨터"), ("하는 일", "저장 시점 기록 · 되돌리기"), ("없으면", "기록이 이 컴퓨터에만")],
            "GitHub", [("어디에", "인터넷 (원격 저장소)"), ("하는 일", "기록 보관 · 공유 · 다른 컴퓨터에서 받기"), ("배포", "Vercel 과 연결")])
              + note("원격 저장소", "내 컴퓨터 밖에 둔 같은 기록 · Free 요금제도 비공개 저장소 무제한")
              + src(("GitHub plans", "https://docs.github.com/en/get-started/learning-about-github/githubs-plans")), T),
        light("Git 작업 흐름", gitflow()
              + src(("Pro Git · What is Git?", "https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F"),
                    ("GitHub Docs · About Git", "https://docs.github.com/en/get-started/using-git/about-git")), T),
        light("Git 작업 요청", viz2.maprows([
            ("「지금 상태 커밋해 줘」", "git add · git commit", "메시지도 Claude가 씀"),
            ("「커밋 기록 보여 줘」", "git log", "시점 · 메시지 목록"),
            ("「방금 고친 거 취소해 줘」", "git restore", "커밋 전 수정 버림"),
            ("「마지막 커밋 되돌려 줘」", "git revert", "되돌리는 새 커밋")], "Claude Code에 하는 말", "실행되는 명령")
              + note("명령 실행", "Claude Code · 사람은 결과 확인"), T),
        light("커밋 시점", viz2.tiles([
            ("기능 하나가 됐을 때", "「로그인 버튼 동작」"), ("크게 바꾸기 전", "디자인을 갈아엎기 전"),
            ("확인이 끝났을 때", "브라우저로 보고 이상 없음")], 3)
              + flow([("요청", "기능 하나"), ("확인", "브라우저"), ("커밋", "세이브"), ("다음 요청", "")], hl=2)
              + note("개발할 때", "이 고리를 태스크마다 반복"), T),
        # ── Git 준비
        light("Git 준비", flow([
            ("Git 설치", "없으면 「Git 설치해 줘」"), ("GitHub 계정", "1-2 에서 가입"), ("작성자 등록", "이 컴퓨터 · 한 번"),
            ("GitHub 로그인", "브라우저 승인 · 한 번")], hl=2)
              + viz2.tiles([("작성자", "커밋의 「누가」 · 이름 · 이메일"), ("로그인", "GitHub 에 올릴 때 필요 · 1-7"),
                            ("둘 다", "처음 한 번 · 다음부터 자동")], 3), T),
        light("Git 작성자 등록", viz2.tiles([
            ("작성자", "커밋마다 남는 이름 · 이메일"), ("값", "GitHub 가입 때 쓴 이름 · 이메일"),
            ("한 번만", "이 컴퓨터에 저장 · 다음 커밋부터 자동")], 3)
              + code("Claude Code 가 실행 · 예", esc('git config --global user.name "내 이름"\ngit config --global user.email "GitHub 가입 이메일"'))
              + note("요청", "「Git 작성자를 내 GitHub 이름 · 이메일로 등록해 줘」 · 명령은 Claude Code 가")
              + src(("Pro Git · First-Time Git Setup", "https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup")), T),
        light("GitHub CLI (gh)", viz2.tiles([
            ("gh", "GitHub 공식 명령 도구 · 저장소 만들기 · 올리기"), ("설치", "Claude Code 에 「GitHub CLI 설치해 줘」"),
            ("명령 암기", "불필요 · 실행은 Claude Code")], 3)
              + '<div class="twocol"><div>' + code("Claude Code 가 실행 · macOS 예", esc("brew install gh")) + "</div><div>"
              + code("Claude Code 가 실행 · Windows 예", esc("winget install --id GitHub.cli --source winget")) + "</div></div>"
              + note("Windows", "설치 뒤 VS Code 를 다시 열면 gh 인식")
              + src(("GitHub CLI", "https://cli.github.com/")), T),
        light("gh 로그인", flow([
            ("「GitHub 로그인 도와줘」", "Claude Code 에 요청"), ("로그인 명령 실행", "Claude Code · 패널에서 허용"), ("브라우저 인증", "화면의 코드 입력 · 승인"),
            ("연결 완료", "「로그인됐는지 확인해 줘」")], hl=2)
              + note("직접 할 것", "브라우저 승인은 사람이 · 비밀번호를 Claude에게 알려 주지 않음")
              + src(("gh auth login", "https://cli.github.com/manual/gh_auth_login")), T),
        # ── 실습
        labcard(T, "첫 커밋", T, "기획서 · 개발 계획", "첫 커밋", ["작성자 등록", "GitHub 로그인", "첫 커밋"]),
        brief(T, T,
              ["Git 작성자 등록 요청", "GitHub 로그인 · 브라우저 승인", "Git 시작 + 첫 커밋 · 기록 보기"],
              [],
              ["작성자", "GitHub 로그인", "첫 커밋", "커밋 기록"],
              ["기록에 내 메시지가 보임", "작성자가 내 이름"],
              "Git 없음 → 「Git 설치해 줘」 · 로그인이 멈추면 오류 문구를 Claude Code 에 붙여 넣기"),
        tstep(T, 1, "작성자 등록", T, ask=("Claude Code 입력창", "Git 작성자를 내 GitHub 이름 · 이메일로 등록해 줘"),
              rows=[("모드", "Plan → 수정마다 승인"), ("묻는 것", "이름 · 이메일 → GitHub 가입 정보"), ("명령 승인", "패널에 뜬 git config → 허용")]),
        tstep(T, 2, "GitHub 로그인", T, ask=("Claude Code 입력창", "GitHub 로그인 도와줘\n로그인됐는지 확인해 줘"),
              rows=[("gh 없음", "Claude Code 가 설치부터"), ("브라우저", "화면의 코드 입력 → 승인"), ("막히면", "오류 문구를 Claude Code 에 붙여 넣기")]),
        tstep(T, 3, "Git 시작 · 첫 커밋", T, ask=("Claude Code 입력창", "Git 으로 관리하고 첫 커밋 남겨 줘\n커밋 기록 보여 줘"),
              rows=[("명령 승인", "패널에 뜬 git 명령 확인 → 허용"), ("기록", "번호 · 작성자 · 시각 · 메시지"), ("작성자", "등록한 내 이름")]),
        light("실습 1-5 확인", checks([
            ("기록에 커밋이 하나 있나", "작성자가 내 이름 · 메시지 한 줄"), ("GitHub 로그인이 됐나", "「로그인됐는지 확인해 줘」 → 내 계정"),
            ],
            "둘 다 「예」 → 1-6 · 이 폴더에 앱 만들기"), T),
    ]
