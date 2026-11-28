"""2-2 데이터베이스.

배경 → 데이터 기록의 변화(종이 → 엑셀 → DB → 클라우드 DB) → 비유(엑셀 · 원시인 돌판 그림) → 페이지 표 애니메이션(행 · 열)
→ 엑셀과 데이터베이스(동시 쓰기 · 형식 거절 애니메이션) → 관계(members · pages) → 블로그 예(표 하나 문제 · 다음 장 세 표 · 번호로 연결) → SQL 한 줄 뜻 → SQL 작성의 변화(손 → SQL → 말 · MCP) → Supabase 구성 · 이유 → 무료 플랜.
사실 출처
- Supabase 무료 플랜: supabase.com/pricing (프로젝트 2개 · DB 500 MB · 월 이용자 50,000 · 1주 미사용 시 일시정지 · Pro $25/월)
- 프로젝트마다 Postgres 전체: supabase.com/docs/guides/database/overview
- Supabase MCP: supabase.com/docs/guides/getting-started/mcp
"""
import viz2
from v1kit import go
from hx import note, table
from deck import lab, light
from stats_hx import big, src
from v2kit import codemap
from v3kit import phmap

T = "2-2"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def sheet():
    """페이지 표 — 행이 차례로 쌓이고, 행 하나 · 열 하나가 차례로 강조됨."""
    head = ["제목", "날짜", "작성자", "상태"]
    rows = [["주간 회의록", "2026-11-27", "김하늘", "초안"],
            ["신규 입사자 교육 자료", "2026-11-25", "이준호", "작성 중"],
            ["내년 예산안", "2026-11-18", "박서연", "작성 중"],
            ["10월 실적 보고", "2026-11-14", "최민재", "완료"]]
    th = '<th class="v2u2rn"></th>' + "".join(f'<th class="{"v2u2col" if i == 1 else ""}">{h}</th>' for i, h in enumerate(head))
    tr = ""
    for r, row in enumerate(rows):
        cls = "v2u2tr v2u2row" if r == 1 else "v2u2tr"
        tds = "".join(f'<td class="{"v2u2col" if i == 1 else ""}">{c}</td>' for i, c in enumerate(row))
        tr += f'<tr class="{cls}" style="--d:{.3 + r * .4:.2f}s"><td class="v2u2rn">{r + 1}</td>{tds}</tr>'
    tags = ('<div class="v2u2tags"><span class="v2u2tag t1">행 · 페이지 한 개</span>'
            '<span class="v2u2tag t2">열 · 항목 하나 (날짜)</span><span class="v2u2tag t3">표 · pages</span></div>')
    return f'<div class="v2u2sheet"><div class="v2u2tab">pages</div><table class="v2u2t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>{tags}'


def relation():
    """두 표와 관계 — pages.owner_id 칸과 같은 번호의 members 행이 같은 색으로 차례로 강조됨."""
    members = [("1", "김하늘", "haneul@company.com"), ("2", "이준호", "junho@company.com"), ("3", "박서연", "seoyeon@company.com")]
    tk = [("1", "1", "주간 회의록", "2026-11-27"), ("2", "2", "신규 입사자 교육 자료", "2026-11-25"),
          ("3", "1", "고객 설문 결과", "2026-11-19")]
    mt = "".join(f'<tr class="v2u2r{a}"><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in members)
    bt = "".join(f'<tr><td>{a}</td><td class="v2u2k v2u2r{b}">{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in tk)
    return ('<div class="v2u2rel">'
            f'<div><div class="v2u2tab">pages · 페이지</div><table class="v2u2t sm"><thead><tr><th>id</th><th class="v2u2kh">owner_id</th>'
            f'<th>title</th><th>date</th></tr></thead><tbody>{bt}</tbody></table></div>'
            '<i class="v2u2link">owner_id → id</i>'
            f'<div><div class="v2u2tab">members · 팀원</div><table class="v2u2t sm"><thead><tr><th>id</th><th>name</th><th>email</th></tr></thead>'
            f'<tbody>{mt}</tbody></table></div></div>')


def rules():
    """세 사람이 동시에 페이지를 보냄 → 표에 들어감 · 날짜 형식이 틀린 하나는 거절."""
    sends = [("김하늘", "주간 회의록 · 2026-11-27", False, .3), ("이준호", "신규 입사자 교육 자료 · 2026-11-25", False, .5),
             ("박서연", "내년 예산안 · 「월말쯤」", True, .7)]
    left = "".join(f'<div class="v2u2snd{" bad" if bad else ""}" style="--d:{d:.2f}s"><b>{who}</b><span>{x}</span></div>'
                   for who, x, bad, d in sends)
    ok = "".join(f'<tr class="v2u2tr" style="--d:{d:.2f}s"><td>{t}</td><td>{dt}</td><td>{w}</td></tr>'
                 for t, dt, w, d in [("주간 회의록", "2026-11-27", "김하늘", 1.7), ("신규 입사자 교육 자료", "2026-11-25", "이준호", 1.9)])
    return ('<div class="v2u2rules"><div class="v2u2snds"><div class="v2u2h">동시에 보낸 페이지</div>' + left + '</div>'
            '<div class="v2u2go"><i style="--d:1.2s">→</i><i style="--d:1.3s">→</i><i style="--d:1.4s">→</i></div>'
            '<div><div class="v2u2sheet"><div class="v2u2tab">pages</div><table class="v2u2t sm"><thead><tr>'
            '<th>제목</th><th class="v2u2kh">날짜 · date 형식</th><th>작성자</th></tr></thead>'
            f'<tbody>{ok}</tbody></table></div>'
            '<div class="v2u2rej" style="--d:2.4s">✕ 박서연 · 「월말쯤」 · 날짜 형식 아님 → 저장 거절</div></div></div>')


def result():
    """SQL 실행 결과 — 코드 줄 뒤에 나타나는 결과 표."""
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [("내년 예산안", "2026-11-18"), ("신규 입사자 교육 자료", "2026-11-25")])
    return (f'<div class="v2u2res"><span>결과 · 2행</span><table class="v2u2t sm"><thead><tr><th>title</th><th>date</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def history():
    """데이터 기록의 변화 — 종이 장부 → 엑셀 파일 → 데이터베이스 → 클라우드 DB.
    같은 페이지 한 개가 단계마다 어떤 모양으로 남는지 + 쌓이는 방식 · 쌓이는 양 막대. 평택대 교안 「데이터 관리의 변화」 구조."""
    R = ("주간 회의록", "11/27", "김하늘")
    paper = (f'<div class="v2hP"><p>{R[1]} {R[0]} — {R[2]}</p><p>11/25 신규 입사자 교육 — 이준호</p>'
             '<p class="x">11/18 예산안 메모 — 박서연</p></div>')
    def grid(rows, head, idcol=False):
        th = "".join(f"<th>{h}</th>" for h in head)
        tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        return f'<table class="v2hT{" db" if idcol else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    xl = ('<div class="v2hX"><div class="f">할일_최종_v3.xlsx</div>'
          + grid([(R[0], R[1], R[2]), ("교육 자료", "11/25", "이준호")], ["A 제목", "B 날짜", "C 작성자"]) + '</div>')
    db = grid([("41", R[0], "2026-11-27", "1"), ("42", "교육 자료", "2026-11-25", "2"), ("43", "<em>새 행</em>", "…", "…")],
              ["id", "title", "date", "owner_id"], True)
    cl = ('<div class="v2hC">' + grid([("41", R[0], "2026-11-27"), ("42", "교육 자료", "2026-11-25")], ["id", "title", "date"], True)
          + '<div class="v2hDv"><span>노트북</span><span>휴대폰</span><span>Vercel 앱</span></div></div>')
    st = [  # (이름, 그림, 기록, 보관, 쌓이는 방식, 막대 %)
        ("종이 장부", paper, "사람이 손으로 적음", "장부 · 화이트보드", "페이지가 늘어남 · 찾기 어려움", 8),
        ("엑셀 파일", xl, "사람이 PC 에 입력", "파일 · 메일로 사본 전달", "사본마다 내용이 갈림", 30),
        ("데이터베이스", db, "앱이 서버로 보냄", "회사 서버 한 곳", "한 표에 행이 추가 · 형식 검사", 65),
        ("클라우드 DB", cl, "앱이 인터넷으로 보냄", "Supabase 같은 서비스", "설치 없이 · 어디서나 같은 표", 100),
    ]
    c = ""
    for i, (name, pic, rec, keep, how, bar) in enumerate(st):
        d = .3 + i * 1.0
        if i:
            c += f'<i class="v2hA" style="--d:{d - .2:.1f}s">→</i>'
        c += (f'<div class="v2hK{" on" if i == 3 else ""}" style="--d:{d:.1f}s"><b class="n">{name}</b><div class="pic">{pic}</div>'
              f'<dl><dt>기록</dt><dd>{rec}</dd><dt>보관</dt><dd>{keep}</dd><dt>쌓이는 방식</dt><dd>{how}</dd></dl>'
              f'<div class="bar"><span>쌓이는 양</span><i style="--w:{bar}%; --d:{d + .6:.1f}s"></i></div></div>')
    return (f'<div class="v2hTop"><span>예전</span><i></i><span>지금 · 2부</span></div><div class="v2h">{c}</div>')


def sql_change():
    """SQL 작성의 변화 — 손으로 찾기 → SQL 직접 작성 → 말로 요청(Claude Code 가 MCP 로 SQL 작성 · 실행).
    같은 질문 「작성 중인 페이지」가 단계마다 어떤 모양인지 + 사람 · AI 가 하는 일. 평택대 교안 「분석 도구의 변화」 구조."""
    pic = [
        '<div class="v2qF"><span>상태 ▾ 필터</span><p>작성 중 ✓</p><p class="x">완료</p><p class="x">초안</p></div>',
        '<pre class="v2qS">select title, date\nfrom pages\nwhere status = \'작성 중\'\norder by date;</pre>',
        '<div class="v2qM"><p class="me">작성 중인 페이지만 보여 줘</p><small class="tl">Supabase MCP · SQL 작성 → 실행</small>'
        '<p class="ai">작성 중 2개 · 내년 예산안 · 신규 입사자 교육 자료</p></div>',
    ]
    st = [("손으로 찾기", "엑셀 필터 · 장부", "줄마다 눈으로 찾음", "—"),
          ("SQL 직접 작성", "개발자 · 분석가", "문법 학습 · 작성 · 실행", "—"),
          ("말로 요청 · MCP", "Claude Code + Supabase MCP · 2-6", "요청 · 결과 확인", "SQL 작성 · 실행 · 보고")]
    c = ""
    for i, (name, who, me, ai) in enumerate(st):
        d = .3 + i * 1.0
        if i:
            c += f'<i class="v2hA" style="--d:{d - .2:.1f}s">→</i>'
        c += (f'<div class="v2hK{" on" if i == 2 else ""}" style="--d:{d:.1f}s"><b class="n">{name}</b><small class="w">{who}</small>'
              f'<div class="pic">{pic[i]}</div>'
              f'<dl><dt>사람이 하는 일</dt><dd>{me}</dd><dt>AI 가 하는 일</dt><dd>{ai}</dd></dl></div>')
    return ('<div class="v2hTop"><span>예전</span><i></i><span>바이브코딩</span></div>'
            f'<div class="v2hQ">「작성 중인 페이지만 보여 줘」 · 같은 질문</div><div class="v2h v2h3">{c}</div>')


def blog():
    """블로그 예 — users · posts · comments 세 표. 번호 칸으로 이어진 행이 같은 색으로 차례로 켜짐.
    ① 글 1번의 author_id 1 → users 1번(주황) ② post_id 1 인 댓글 2개 → 글 1번(파랑) ③ 댓글의 user_id 2 → users 2번(초록)."""
    def tb(name, ko, head, rows, keys=()):
        th = "".join(f'<th class="{"k" if h in keys else ""}">{h}</th>' for h in head)
        tr = "".join(f'<tr class="{c}">' + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for c, r in rows)
        return f'<div class="tb"><div class="v2u2tab">{name} · {ko}</div><table class="v2u2t sm"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    users = tb("users", "회원", ["id", "name"], [("a", ["1", "김하늘"]), ("c", ["2", "이준호"]), ("", ["3", "박서연"])])
    posts = tb("posts", "글", ["id", "title", "author_id"],
               [("a b", ["1", "첫 바이브코딩 후기", "1"]), ("", ["2", "Supabase 써 보기", "2"]), ("", ["3", "MCP 정리", "1"])], ("author_id",))
    cmts = tb("comments", "댓글", ["id", "post_id", "user_id", "body"],
              [("b c", ["1", "1", "2", "잘 읽었어요"]), ("b", ["2", "1", "3", "저도 해 볼게요"]), ("", ["3", "2", "1", "좋은 정리"])], ("post_id", "user_id"))
    tags = ('<div class="lk"><span class="a">① 글 → 쓴 사람 · posts.author_id = users.id</span>'
            '<span class="b">② 글 → 댓글 여러 개 · comments.post_id = posts.id</span>'
            '<span class="c">③ 댓글 → 쓴 사람 · comments.user_id = users.id</span></div>')
    return f'<div class="v22blog"><div class="tbs">{users}{posts}{cmts}</div>{tags}</div>'


def blog_one():
    """한 표에 모두 넣은 블로그 — ① 같은 내용 반복(노랑) ② 이메일 하나만 고쳐 어긋남(빨강) ③ 댓글 없는 글은 빈칸(회색)
    ④ 칸이 세 덩어리(회원 · 글 · 댓글)로 색이 갈림 → 다음 장에서 세 표로."""
    head = [("글 제목", "p"), ("글쓴이", "u"), ("글쓴이 이메일", "u"), ("댓글", "c"), ("댓글 쓴 사람", "u"), ("댓글 쓴 사람 이메일", "u")]
    R = [
        [("첫 바이브코딩 후기", "rp"), ("김하늘", "rp"), ("haneul@a.com", "rp ch"), ("잘 읽었어요", ""), ("이준호", ""), ("junho@a.com", "")],
        [("첫 바이브코딩 후기", "rp"), ("김하늘", "rp"), ("haneul@a.com", "rp bad"), ("저도 해 볼게요", ""), ("박서연", ""), ("seoyeon@a.com", "")],
        [("Supabase 써 보기", ""), ("이준호", ""), ("junho@a.com", ""), ("좋은 정리", ""), ("김하늘", "rp"), ("haneul@a.com", "rp bad")],
        [("MCP 정리", ""), ("김하늘", "rp"), ("haneul@a.com", "rp bad"), ("", "em"), ("", "em"), ("", "em")],
    ]
    th = "".join(f'<th class="g{g}">{h}</th>' for h, g in head)
    tr = ""
    for r in R:
        tds = ""
        for j, (v, c) in enumerate(r):
            g = head[j][1]
            if "ch" in c:
                v = f'<i class="o">{v}</i><i class="n">haneul@new.com</i>'
            tds += f'<td class="g{g} {c}">{v}</td>'
        tr += f"<tr>{tds}</tr>"
    probs = ('<div class="pb"><span class="p1">① 같은 내용 반복 · 글 제목 · 김하늘 · 이메일이 여러 줄</span>'
             '<span class="p2">② 고칠 때 어긋남 · 이메일을 한 줄만 고침 → 나머지는 옛 주소</span>'
             '<span class="p3">③ 빈칸 · 댓글 없는 글은 댓글 칸을 비워 둠</span>'
             '<span class="p4">④ 칸이 세 덩어리 · 회원 · 글 · 댓글 → 세 표로 나누기</span></div>')
    return f'<div class="v22one"><div class="v2u2tab">blog · 한 표에 모두</div><table class="v2u2t sm">{"<tr>" + th + "</tr>"}{tr}</table>{probs}</div>'


def sbstep(i, name, img, alt, boxes, rows, no="2-2", u=None):
    """실습 2-2 단계 화면 — 왼쪽 실제 화면(번호 상자가 차례로 켜짐) · 오른쪽 번호별 할 일."""
    from v1_u2 import annot
    title = f"실습 {no} · {i}단계 {name}" if i != "" else f"{name}"
    return light(title, '<div class="twocol v1vsgrid v1stp v22stp"><div>' + annot(img, alt, boxes, "")
                 + "</div><div>" + viz2.tiles(rows, 1) + "</div></div>", u or T)


def gh_auth():
    """GitHub 승인 화면(Authorize Supabase) 재구성 — 계정 이름은 「내 GitHub 계정」. 번호 상자 ① 권한 ② 승인 버튼이 차례로 켜짐."""
    return ('<div class="v22au"><div class="top"><span class="sb"><svg viewBox="0 0 24 24" width="26" height="26"><path d="M13 2 4 14h7l-1 8 9-12h-7z" fill="#3ECF8E"/></svg></span><i></i><span class="ck">✓</span><i></i>'
            '<span class="gh"><img src="img/github_logo.svg" alt=""/></span></div>'
            '<h3>Authorize Supabase</h3><div class="box"><div class="who"><b>Supabase</b> by <em>Supabase</em><br/>'
            '<small>wants to access your <b>내 GitHub 계정</b> account</small></div>'
            '<div class="perm" style="--d:.6s"><b>Personal user data</b><small>Email addresses (read-only)</small><u data-n="①"></u></div>'
            '<div class="btns"><span class="cc">Cancel</span><span class="ok" style="--d:1.4s">Authorize supabase<u data-n="②"></u></span></div>'
            '<div class="rd">Authorizing will redirect to <b>https://auth.supabase.io</b></div></div></div>')


def slides():
    return [
        light("데이터 기록의 변화", history()
              + note("2부", "Supabase · 클라우드 DB 한 곳에 페이지 기록"), T),
        light("엑셀 표", phmap("v2_u2_tablet.webp", "칸을 나눠 기록하는 돌판", *GEN, viz2.maprows([
            ("엑셀 파일", "데이터베이스", "Supabase 프로젝트 하나"), ("시트", "표 (테이블)", "pages · members"),
            ("가로 한 줄", "행", "페이지 한 개"), ("세로 한 칸", "열", "제목 · 날짜 · 작성자"),
            ("칸 하나", "값", "2026-11-27")], "엑셀", "데이터베이스")), T),
        light("페이지 표의 행과 열", sheet()
              + note("관계형 데이터베이스", "데이터를 행 · 열로 된 표에 담는 방식 · 표끼리 서로 연결"), T),
        light("엑셀과 데이터베이스", rules()
              + note("엑셀과 차이", "엑셀 · 아무 칸에 아무 값 / 데이터베이스 · 열마다 형식 · 여러 사람이 동시에"), T),
        light("블로그 · 표 하나", blog_one(), T),
        light("블로그 · 표 나누기", blog()
              + note("관계", "같은 내용을 두 번 적지 않고 번호로 가리킴 · 글 하나에 댓글 여러 개"), T),
        light("표와 표의 관계", relation()
              + note("미니 노션", "같은 구조 · 작성자 한 명 ↔ 페이지 여러 개 · owner_id 로 연결"), T),
        light("SQL 작성의 변화", sql_change()
              + note("사람이 남기는 일", "질문 · 결과가 맞는지 판단"), T),
        light("Supabase", viz2.tiles([
            ("Postgres 데이터베이스", "프로젝트마다 Postgres 전체 하나"), ("로그인 (Auth)", "이메일 · 소셜 로그인"),
            ("표 편집 화면", "Table Editor · 엑셀처럼 행 보기 · 고치기"), ("Claude Code 연결", "공식 MCP 서버 · 표 만들기 · 조회")], 2)
              + note("바이브코딩에서", "데이터베이스 · 로그인을 한 서비스에서 · 무료로 시작")
              + src(("Supabase Database", "https://supabase.com/docs/guides/database/overview"),
                    ("Supabase MCP", "https://supabase.com/docs/guides/getting-started/mcp")), T),
        light("Supabase 무료 플랜", big([
            ("2", "개", "프로젝트"), ("500", "MB", "데이터베이스 용량"), ("5만", "명", "월 로그인 이용자", True), ("1", "주", "미사용 시 일시정지")])
              + note("유료", "Pro 월 $25부터 · 2부 실습은 무료 플랜으로 충분")
              + src(("supabase.com/pricing · 2026-11", "https://supabase.com/pricing")), T),
        # ── 실습
        lab("2-2", "Supabase 가입 · 프로젝트 만들기", T, "Supabase 에 가입하고 미니 노션이 쓸 프로젝트를 만든다",
            ["supabase.com 가입 · Continue with GitHub", "조직 만들기 · Free", "새 프로젝트 · mini_notion · DB 비밀번호",
             "프로젝트 화면 확인"],
            ["대시보드에 mini_notion 프로젝트", "프로젝트 URL · Connect 위치 확인"]),
        sbstep(1, "가입", "v2_u2_sb_signup.webp", "Supabase 가입 화면",
               [("①", "Continue with GitHub", 9.8, 37.2, 76.4, 12.3)],
               [("주소", go("supabase.com/dashboard/sign-up", "https://supabase.com/dashboard/sign-up")),
                ("① Continue with GitHub", "1-2 의 GitHub 계정 → Authorize supabase"), ("누르지 않을 것", "ChatGPT · SSO · 이메일 가입")]),
        light("실습 2-2 · 1단계 GitHub 승인", '<div class="twocol v1vsgrid v22stp"><div>' + gh_auth() + '</div><div>' + viz2.tiles([
            ("① 권한", "Email addresses (read-only) · 이메일 읽기만"), ("② Authorize supabase", "누르면 Supabase 로 돌아감"),
            ("처음 한 번", "다음부터는 Continue with GitHub 만 누르면 로그인")], 1) + '</div></div>'
              + note("화면", "GitHub 승인 화면 재구성 · 계정 이름 자리 바꿈"), T),
        sbstep(2, "조직 만들기", "v2_u2_sb_orgform.webp", "Create a new organization 화면",
               [("①", "Name", 35.2, 19.6, 61.6, 5.5), ("②", "Plan", 35.2, 38.4, 61.6, 5.5), ("③", "Create", 77.6, 92.8, 19.2, 4.2)],
               [("시작", "Your organizations → New organization"), ("① Name", "팀 · 회사 이름 · 나중에 변경 가능"),
                ("② Plan", "Free - $0/month"), ("③ Create organization", "선택 질문은 비워도 됨")]),
        sbstep(3, "새 프로젝트", "v2_u2_sb_project.webp", "Create a new project 화면",
               [("①", "Project name", 35, 2.4, 61.7, 5.9), ("②", "Password", 35, 14.3, 61.7, 13.4), ("③", "Region", 35, 33.4, 61.7, 6),
                ("④", "Data access", 34.8, 49.2, 61, 26.1), ("⑤", "Create", 78, 92.2, 18.7, 4.5)],
               [("① Project name", "mini_notion · 조직은 2단계 것 그대로"), ("② Database password", "Generate → Copy → 따로 보관"), ("③ Region", "Auto 그대로"),
                ("④ Data access", "세 칸 모두 체크 · RLS 포함"), ("⑤ Create new project", "준비될 때까지 대기")]),
        sbstep(4, "프로젝트 화면", "v2_u2_sb_home.webp", "프로젝트 대시보드",
               [("①", "URL", 18, 36.1, 56.4, 4), ("②", "Connect", 76.6, 1, 12.8, 4.5), ("③", "Table Editor", 1.1, 15.1, 4.5, 4.5)],
               [("① 프로젝트 URL", "앱이 요청을 보낼 주소 · Copy"), ("② Connect", "앱에 연결하는 방법 · 2-4"),
                ("③ Table Editor", "왼쪽 두 번째 · 표는 2-4 에서 마이그레이션으로")]),
    ]


CSS = """
  /* 2-1 · SQL 작성의 변화 (v2q · 카드는 v2h 공용) */
  .v2hQ{font-size:16px; font-weight:700; color:#1F3A5F; margin:-4px 0 10px;}
  .v2hK .w{font-size:13px; color:#6B7785; margin-top:-6px;}
  .v2qF{width:100%; border:1.5px solid #C9CFD8; border-radius:6px; background:#fff; font-size:13px; overflow:hidden;}
  .v2qF span{display:block; background:#1D6F42; color:#fff; font-weight:700; padding:3px 8px;}
  .v2qF p{margin:0; padding:3px 8px; border-top:1px solid #E3E7EC; color:#16233A;} .v2qF p.x{color:#A0A8B4;}
  .v2qS{margin:0; width:100%; box-sizing:border-box; background:#16233A; color:#E8ECF1; border-radius:8px; padding:8px 10px; font-family:var(--mono);
    font-size:12.5px; line-height:1.5; white-space:pre;}
  .v2qS.sm{font-size:11.5px; padding:4px 8px;}
  .v2qM{width:100%; display:flex; flex-direction:column; gap:5px;}
  .v2qM p{margin:0; font-size:13px; border-radius:10px; padding:5px 9px;}
  .v2qM p.me{align-self:flex-end; background:#FFF1E0; color:#16233A; font-weight:600;}
  .v2qM p.ai{background:#EEF3FA; color:#16233A; border:1px solid #C9D6E6;}
  .v2h.v2h3{grid-template-columns:1fr 26px 1fr 26px 1.25fr;}
  .v2qM small.tl{color:#1F9D63; font-family:var(--mono); font-size:12px;}
  .v2qM small{font-size:12px; color:#C0392B; font-weight:700;}
  /* 2-1 · 데이터 기록의 변화 (v2h) */
  .v2hTop{display:flex; align-items:center; gap:12px; margin:0 0 10px; font-size:15px; font-weight:700; color:#5A6B80;}
  .v2hTop i{flex:1; height:2px; background:#1F3A5F; position:relative;}
  .v2hTop i:after{content:""; position:absolute; right:-2px; top:-5px; border:6px solid transparent; border-left:10px solid #1F3A5F;}
  .v2h{display:grid; grid-template-columns:1fr 26px 1fr 26px 1fr 26px 1fr; align-items:stretch;}
  .v2hK{border:2px solid #D9DDE3; border-radius:14px; background:#fff; padding:12px 14px; display:flex; flex-direction:column; gap:8px;
    opacity:0; animation:v2hIn .6s var(--d) forwards;}
  .v2hK.on{border-color:#F28C28; background:#FFF8F0;} .v2hK.on .n{color:#E07A12;}
  .v2hK .n{font-size:21px; color:#16233A;}
  .v2hK .pic{height:112px; display:flex; align-items:center; justify-content:center;}
  .v2hK dl{margin:0; display:grid; gap:1px;} .v2hK dt{font-size:12.5px; color:#6B7785; margin-top:4px;} .v2hK dd{margin:0; font-size:15px; font-weight:600; color:#16233A;}
  .v2hK .bar{margin-top:auto; padding-top:6px;} .v2hK .bar span{font-size:12.5px; color:#6B7785;}
  .v2hK .bar i{display:block; height:11px; border-radius:6px; background:#1F3A5F; margin-top:3px; width:0; animation:v2hW .9s var(--d) ease-out forwards;}
  .v2hK.on .bar i{background:#F28C28;}
  .v2hA{font-style:normal; align-self:center; text-align:center; font-size:24px; font-weight:800; color:#F28C28; opacity:0; animation:v2hIn .4s var(--d) forwards;}
  .v2hP{width:100%; background:#FFFBF0; border:1.5px solid #CDBF9C; border-radius:4px; padding:8px 10px; transform:rotate(-1.2deg);
    background-image:repeating-linear-gradient(#FFFBF0 0 25px, #E6DCC2 25px 26px);}
  .v2hP p{margin:0; font-size:13.5px; line-height:26px; color:#3A3A5A; font-style:italic; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  .v2hP p.x{text-decoration:line-through; color:#8A8AA0;}
  .v2hX{width:100%;} .v2hX .f{font-size:12px; color:#1D6F42; font-weight:700; margin-bottom:3px;}
  .v2hT{width:100%; border-collapse:collapse; font-size:12.5px;}
  .v2hT th{background:#1D6F42; color:#fff; font-weight:600; padding:3px 5px; text-align:left;}
  .v2hT td{border:1px solid #C9CFD8; padding:3px 5px; color:#16233A; white-space:nowrap; overflow:hidden; max-width:110px; text-overflow:ellipsis;}
  .v2hT.db th{background:#1F3A5F; font-family:var(--mono);} .v2hT.db td{font-family:var(--mono); font-size:12px;}
  .v2hT em{font-style:normal; color:#E07A12; font-weight:700;}
  .v2hC{width:100%;} .v2hC .v2hT.db th{background:#3ECF8E; color:#0F2A1D;}
  .v2hDv{display:flex; gap:5px; margin-top:6px;} .v2hDv span{font-size:11.5px; font-weight:700; color:#fff; background:#1F3A5F; border-radius:10px; padding:2px 8px;}
  @keyframes v2hIn{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @keyframes v2hW{to{width:var(--w)}}
  @media print{.v2hK,.v2hA{opacity:1; animation:none} .v2hK .bar i{width:var(--w); animation:none}}
  /* 2-1 · 저장 위치 */
  .v2u2where{display:grid; grid-template-columns:1fr 50px 1fr; gap:10px; align-items:start; margin:4px 0 16px;}
  .v2u2side{border:2px solid #D9DDE3; border-radius:16px; padding:16px 18px; background:#fff;}
  .v2u2side.on{border-color:#F28C28; background:#FFF8F0;}
  .v2u2h{font-size:17px; font-weight:800; color:#16233A; margin-bottom:12px;}
  .v2u2devs{display:grid; grid-template-columns:repeat(3,1fr); gap:10px;}
  .v2u2dv{border:1.5px solid #D9DDE3; border-radius:12px; padding:10px 10px; background:#fff; text-align:center; opacity:0; animation:v2u2in .5s ease-out var(--d) forwards;}
  .v2u2dv b{display:block; font-size:16px; color:#16233A;} .v2u2dv span{font-size:15px; color:#E07A12; font-weight:700;}
  .v2u2cap{margin-top:14px; font-size:16px; color:#C0392B; font-weight:700; text-align:center; opacity:0; animation:v2u2in .5s ease-out var(--d) forwards;}
  .v2u2pipe{text-align:center; letter-spacing:46px; font-size:20px; color:#F28C28; font-weight:800; margin:6px 0; opacity:0; animation:v2u2in .4s ease-out var(--d) forwards;}
  .v2u2db{border:2px solid #F28C28; border-radius:14px; background:#FFF3E6; padding:12px 14px; text-align:center; opacity:0; animation:v2u2in .5s ease-out var(--d) forwards;}
  .v2u2db b{display:block; font-size:19px; color:#E07A12;} .v2u2db span{font-size:15px; color:#16233A;}
  .v2u2ar{font-style:normal; align-self:center; text-align:center; font-size:30px; font-weight:800; color:#F28C28;}
  /* 2-1 · 페이지 표 */
  .v2u2sheet{border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#fff; margin:4px 0 12px;}
  .v2u2tab{display:inline-block; font-family:var(--mono); font-size:14px; font-weight:800; color:#fff; background:#1F3A5F; padding:5px 14px; border-radius:8px 8px 0 0;}
  .v2u2sheet .v2u2tab{border-radius:0 0 8px 0;}
  .v2u2t{width:100%; border-collapse:collapse; font-size:17px;}
  .v2u2t th{background:#F4F6F9; color:#3A4657; font-weight:800; padding:9px 12px; text-align:left; border-bottom:1.5px solid #D9DDE3;}
  .v2u2t td{padding:9px 12px; border-bottom:1px solid #EEF0F3; color:#16233A;}
  .v2u2t .v2u2rn{width:34px; color:#9AA6B5; font-family:var(--mono); font-size:14px; background:#F9FAFB;}
  .v2u2tr{opacity:0; animation:v2u2in .45s ease-out var(--d) forwards;}
  .v2u2row td{animation:v2u2row .6s ease-out 2.2s forwards;}
  .v2u2t .v2u2col{animation:v2u2col .6s ease-out 3.2s forwards;}
  .v2u2tags{display:flex; gap:14px;}
  .v2u2tag{font-size:16px; font-weight:800; padding:7px 14px; border-radius:10px; opacity:0;}
  .v2u2tag.t1{background:#FFE3C4; color:#B85A00; animation:v2u2in .4s ease-out 2.4s forwards;}
  .v2u2tag.t2{background:#DCEBFF; color:#1F4E8C; animation:v2u2in .4s ease-out 3.4s forwards;}
  .v2u2tag.t3{background:#1F3A5F; color:#fff; animation:v2u2in .4s ease-out 4.0s forwards;}
  @keyframes v2u2row{to{background:#FFE3C4;}}
  @keyframes v2u2col{to{background:#DCEBFF;}}
  /* 2-1 · 관계 */
  .v2u2rel{display:grid; grid-template-columns:1.5fr 110px 1fr; gap:8px; align-items:center; margin:0 0 14px;}
  .v2u2rel > div{border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#fff;}
  .v2u2rel .v2u2tab{border-radius:0 0 8px 0;}
  .v2u2t.sm{font-size:15.5px;} .v2u2t.sm td, .v2u2t.sm th{padding:7px 10px;}
  .v2u2kh{color:#E07A12 !important;}
  .v2u2link{font-style:normal; text-align:center; font-family:var(--mono); font-size:14px; font-weight:800; color:#E07A12; opacity:0; animation:v2u2in .4s ease-out .4s forwards;}
  .v2u2t .v2u2r1{animation:v2u2r1 .6s ease-out 1.0s forwards;}
  .v2u2t .v2u2r2{animation:v2u2r2 .6s ease-out 1.8s forwards;}
  @keyframes v2u2r1{to{background:#FFE3C4;}}
  @keyframes v2u2r2{to{background:#DCEBFF;}}
  /* 2-1 · 동시에 쓰기 · 형식 규칙 */
  .v2u2rules{display:grid; grid-template-columns:1fr 60px 1.3fr; gap:12px; align-items:center; margin:4px 0 16px;}
  .v2u2snds{display:flex; flex-direction:column; gap:10px;}
  .v2u2snd{border:1.5px solid #D9DDE3; border-radius:12px; padding:10px 14px; background:#fff; opacity:0; animation:v2u2in .45s ease-out var(--d) forwards;}
  .v2u2snd b{display:block; font-size:17px; color:#16233A;} .v2u2snd span{font-size:15px; color:#3A4657;}
  .v2u2snd.bad{animation:v2u2in .45s ease-out var(--d) forwards, v2u2bad .5s ease-out 2.4s forwards;}
  @keyframes v2u2bad{to{border-color:#C0392B; background:#FDECEA; opacity:.75}}
  .v2u2go{display:flex; flex-direction:column; gap:22px; align-items:center;}
  .v2u2go i{font-style:normal; font-size:26px; font-weight:800; color:#F28C28; opacity:0; animation:v2u2in .3s ease-out var(--d) forwards;}
  .v2u2rej{margin-top:12px; padding:10px 14px; border-radius:10px; background:#FDECEA; border:1.5px solid #E8A39B; color:#C0392B; font-size:16px; font-weight:700; opacity:0; animation:v2u2in .45s ease-out var(--d) forwards;}
  /* 2-1 · SQL 결과 */
  .v2u2res{display:flex; gap:14px; align-items:flex-start; margin:14px 0 10px; opacity:0; animation:v2u2in .5s ease-out 2.0s forwards;}
  .v2u2res > span{font-size:14px; font-weight:800; color:#fff; background:#F28C28; padding:6px 12px; border-radius:8px; white-space:nowrap;}
  .v2u2res table{width:auto; min-width:360px; border:1.5px solid #D9DDE3;}
  @keyframes v2u2in{from{opacity:0; transform:translateY(8px)} to{opacity:1; transform:none}}
  @media print{.v2u2snd,.v2u2go i,.v2u2rej,.v2u2res,.v2u2dv,.v2u2cap,.v2u2pipe,.v2u2db,.v2u2tr,.v2u2tag,.v2u2link{opacity:1; animation:none}}
  /* 2-2 · 블로그의 표 관계 (v22blog) */
  .v22blog .tbs{display:grid; grid-template-columns:.8fr 1.3fr 1.6fr; gap:18px; align-items:start; margin:0 0 14px;}
  .v22blog .v2u2t td,.v22blog .v2u2t th{font-size:14.5px; padding:7px 9px;}
  .v22blog .v2u2t th.k{color:#E07A12;}
  .v22blog tr.a td{animation:v22a .4s calc(var(--o,0s) + .6s) forwards;} .v22blog tr.b td{animation:v22b .4s calc(var(--o,0s) + 2s) forwards;} .v22blog tr.c td{animation:v22c .4s calc(var(--o,0s) + 3.4s) forwards;}
  .v22blog tr.a.b td{animation:v22a .4s calc(var(--o,0s) + .6s) forwards, v22b .4s calc(var(--o,0s) + 2s) forwards;}
  .v22blog tr.b.c td{animation:v22b .4s calc(var(--o,0s) + 2s) forwards, v22c .4s calc(var(--o,0s) + 3.4s) forwards;}
  .v22blog .lk{display:flex; flex-direction:column; gap:6px; margin:0 0 10px;}
  .v22blog .lk span{font-size:15.5px; font-weight:700; border-left:5px solid; padding:4px 12px; border-radius:4px; opacity:0;}
  .v22blog .lk .a{border-color:#F28C28; background:#FFF3E0; color:#B85A00; animation:v22in .4s calc(var(--o,0s) + .6s) forwards;}
  .v22blog .lk .b{border-color:#264DE4; background:#E8EEFF; color:#1F3A9F; animation:v22in .4s calc(var(--o,0s) + 2s) forwards;}
  .v22blog .lk .c{border-color:#2E8B57; background:#E6F4EC; color:#1E7B45; animation:v22in .4s calc(var(--o,0s) + 3.4s) forwards;}
  @keyframes v22a{to{background:#FFE3C4}} @keyframes v22b{to{background:#D9E3FF}} @keyframes v22c{to{background:#CDEBD9}}
  @keyframes v22in{to{opacity:1}}
  @media print{.v22blog .lk span{opacity:1; animation:none}}
  /* 2-2 · 한 표에 모두 넣으면 (v22one) */
  .v22one .v2u2t td,.v22one .v2u2t th{font-size:14px; padding:7px 9px; position:relative;}
  .v22one .v2u2t th{animation:v22gh .5s 5.4s forwards;}
  .v22one td.rp{animation:v22rp .4s 1.0s forwards;}
  .v22one td.bad{animation:v22rp .4s 1.0s forwards, v22bad .4s 2.6s forwards;}
  .v22one td.ch .o{animation:v22o .3s 2.4s forwards;} .v22one td.ch .n{position:absolute; left:9px; opacity:0; font-style:normal; font-weight:800; color:#1E7B45; animation:v22in .3s 2.4s forwards;}
  .v22one td.ch i{font-style:normal;}
  .v22one td.em{animation:v22em .4s 4.0s forwards;}
  .v22one th.gu{--gc:#D9E3FF;} .v22one th.gp{--gc:#FFE3C4;} .v22one th.gc{--gc:#CDEBD9;}
  .v22one td.gu{--gc:#EEF2FF;} .v22one td.gp{--gc:#FFF6EC;} .v22one td.gc{--gc:#EDF8F1;}
  .v22one td{animation-fill-mode:forwards;}
  .v22one tr td:not(.rp):not(.em){animation:v22g .5s 5.4s forwards;}
  .v22one .pb{display:grid; grid-template-columns:1fr 1fr; gap:6px 12px; margin:12px 0 8px;}
  .v22one .pb span{font-size:15px; font-weight:700; border-left:5px solid; padding:5px 12px; border-radius:4px; opacity:0;}
  .v22one .pb .p1{border-color:#E0B000; background:#FFF6CC; color:#7A5C00; animation:v22in .4s 1.0s forwards;}
  .v22one .pb .p2{border-color:#C0392B; background:#FDECEA; color:#C0392B; animation:v22in .4s 2.6s forwards;}
  .v22one .pb .p3{border-color:#9AA5B1; background:#F1F3F6; color:#3A4657; animation:v22in .4s 4.0s forwards;}
  .v22one .pb .p4{border-color:#1F3A5F; background:#EEF2FF; color:#1F3A5F; animation:v22in .4s 5.4s forwards;}
  @keyframes v22rp{to{background:#FFF0A8}}
  @keyframes v22bad{to{background:#F9C9C3; color:#C0392B; font-weight:800}}
  @keyframes v22o{to{opacity:0}}
  @keyframes v22em{to{background:repeating-linear-gradient(45deg,#E3E7EC 0 6px,#F4F6F9 6px 12px)}}
  @keyframes v22gh{to{background:var(--gc)}}
  @keyframes v22g{to{background:var(--gc)}}
  @media print{.v22one .pb span{opacity:1; animation:none}}
  .v22blog .tb:nth-child(1) .v2u2tab{background:#264DE4;} .v22blog .tb:nth-child(2) .v2u2tab{background:#E07A12;} .v22blog .tb:nth-child(3) .v2u2tab{background:#2E8B57;}
  /* 2-2 · 실습 화면 + 번호 상자 (1-2 와 같은 모양) */
  .v1an{margin:0;} .v1anw{position:relative; border-radius:10px; overflow:hidden; box-shadow:0 8px 24px rgba(22,35,58,.18);}
  .v1anw img{display:block; width:100%;}
  .v1stp > div:first-child{display:flex; justify-content:center;}
  .v1stp .v1anw{width:fit-content; max-width:100%; margin:0 auto;}
  .v1stp .v1anw img{width:auto; max-width:100%; max-height:440px;}
  .v1anb{position:absolute; border:3px solid #F28C28; border-radius:6px; background:rgba(242,140,40,.12); opacity:0; animation:v1anIn .5s var(--d) forwards;}
  .v1anb em{position:absolute; left:-3px; top:-3px; background:#F28C28; color:#fff; font-style:normal; font-weight:800; font-size:14px; padding:2px 7px; border-radius:5px 0 6px 0; white-space:nowrap;}
  .v1anb span{display:none;}
  @keyframes v1anIn{from{opacity:0; transform:scale(1.04)} to{opacity:1; transform:none}}
  @media print{.v1anb{opacity:1; animation:none}}
  .v1vsgrid{grid-template-columns:1.7fr 1fr; align-items:center;}
  .v22stp{grid-template-columns:1.25fr 1fr;} .v22stp .v2tile{padding:10px 14px;}
  .v22stp .v1anw{overflow:visible;} .v22stp .v1anw img{border-radius:10px;}
  .v22stp .v1anb em{left:-3px; top:-24px; border-radius:5px 5px 0 0;}
  /* 2-2 · GitHub 승인 화면 재구성 (v22au) */
  .v22au{width:430px; margin:0 auto; background:#0D1117; border-radius:12px; padding:18px 22px; color:#E6EDF3; font-family:-apple-system,"Segoe UI",sans-serif;}
  .v22au .top{display:flex; align-items:center; justify-content:center; gap:6px;}
  .v22au .top i{width:26px; border-top:2px dashed #484F58;}
  .v22au .sb,.v22au .gh{width:52px; height:52px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px;}
  .v22au .sb{background:#1C1C1C; color:#3ECF8E;} .v22au .gh{background:#F0F6FC;} .v22au .gh img{width:30px;}
  .v22au .ck{width:24px; height:24px; border-radius:50%; background:#2EA043; color:#fff; font-size:13px; font-weight:800; display:flex; align-items:center; justify-content:center;}
  .v22au h3{text-align:center; font-size:22px; font-weight:500; margin:10px 0 12px; color:#E6EDF3;}
  .v22au .box{border:1px solid #30363D; border-radius:8px; padding:12px 14px; display:flex; flex-direction:column; gap:10px;}
  .v22au .who{font-size:14px;} .v22au .who em{font-style:normal; color:#4493F8; font-weight:700;} .v22au .who small{color:#9198A1; font-size:13px;} .v22au .who small b{color:#E6EDF3;}
  .v22au .perm,.v22au .ok{position:relative;}
  .v22au .perm{border-top:1px solid #30363D; padding-top:8px; font-size:14px;} .v22au .perm small{display:block; color:#9198A1; font-size:12.5px;}
  .v22au .btns{display:grid; grid-template-columns:1fr 1fr; gap:8px; border-top:1px solid #30363D; padding-top:10px;}
  .v22au .btns span{text-align:center; font-size:13.5px; font-weight:600; border-radius:6px; padding:7px 0;}
  .v22au .cc{background:#212830; border:1px solid #3D444D;} .v22au .ok{background:#238636; color:#fff;}
  .v22au .rd{text-align:center; font-size:11.5px; color:#9198A1;} .v22au .rd b{color:#E6EDF3;}
  .v22au u{position:absolute; inset:-4px; border:3px solid #F28C28; border-radius:6px; text-decoration:none; font-size:12px; font-weight:800; color:#fff;
    opacity:0; animation:v1anIn .5s var(--d) forwards;}
  .v22au .perm u{top:4px;}
  .v22au u::before{content:attr(data-n); position:absolute; left:-3px; top:-22px; background:#F28C28; padding:1px 7px; border-radius:5px 5px 0 0;}
  @media print{.v22au u{opacity:1; animation:none}}
"""
