"""2-2 데이터베이스.

배경 → 데이터 기록의 변화(종이 → 엑셀 → DB → 클라우드 DB) → 비유(엑셀 · 원시인 돌판 그림) → 할 일 표 애니메이션(행 · 열)
→ 엑셀과 데이터베이스(동시 쓰기 · 형식 거절 애니메이션) → 관계(members · tasks) → SQL 한 줄 뜻 → SQL 작성의 변화(손 → SQL → 말 → MCP) → Supabase 구성 · 이유 → 무료 플랜.
사실 출처
- Supabase 무료 플랜: supabase.com/pricing (프로젝트 2개 · DB 500 MB · 월 이용자 50,000 · 1주 미사용 시 일시정지 · Pro $25/월)
- 프로젝트마다 Postgres 전체: supabase.com/docs/guides/database/overview
- Supabase MCP: supabase.com/docs/guides/getting-started/mcp
"""
import viz2
from hx import note, table
from deck import light
from stats_hx import big, src
from v2kit import codemap
from v3kit import phmap

T = "2-2"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")


def sheet():
    """할 일 표 — 행이 차례로 쌓이고, 행 하나 · 열 하나가 차례로 강조됨."""
    head = ["할 일", "기한", "담당자", "상태"]
    rows = [["주간 보고서 작성", "2026-11-27", "김하늘", "할 일"],
            ["신규 입사자 교육 자료", "2026-11-25", "이준호", "진행 중"],
            ["내년 예산안 검토", "2026-11-18", "박서연", "진행 중"],
            ["10월 실적 정리", "2026-11-14", "최민재", "완료"]]
    th = '<th class="v2u2rn"></th>' + "".join(f'<th class="{"v2u2col" if i == 1 else ""}">{h}</th>' for i, h in enumerate(head))
    tr = ""
    for r, row in enumerate(rows):
        cls = "v2u2tr v2u2row" if r == 1 else "v2u2tr"
        tds = "".join(f'<td class="{"v2u2col" if i == 1 else ""}">{c}</td>' for i, c in enumerate(row))
        tr += f'<tr class="{cls}" style="--d:{.3 + r * .4:.2f}s"><td class="v2u2rn">{r + 1}</td>{tds}</tr>'
    tags = ('<div class="v2u2tags"><span class="v2u2tag t1">행 · 할 일 한 건</span>'
            '<span class="v2u2tag t2">열 · 항목 하나 (기한)</span><span class="v2u2tag t3">표 · tasks</span></div>')
    return f'<div class="v2u2sheet"><div class="v2u2tab">tasks</div><table class="v2u2t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>{tags}'


def relation():
    """두 표와 관계 — tasks.owner_id 칸과 같은 번호의 members 행이 같은 색으로 차례로 강조됨."""
    members = [("1", "김하늘", "haneul@company.com"), ("2", "이준호", "junho@company.com"), ("3", "박서연", "seoyeon@company.com")]
    tk = [("1", "1", "주간 보고서 작성", "2026-11-27"), ("2", "2", "신규 입사자 교육 자료", "2026-11-25"),
          ("3", "1", "고객 설문 결과 정리", "2026-11-19")]
    mt = "".join(f'<tr class="v2u2r{a}"><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in members)
    bt = "".join(f'<tr><td>{a}</td><td class="v2u2k v2u2r{b}">{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in tk)
    return ('<div class="v2u2rel">'
            f'<div><div class="v2u2tab">tasks · 할 일</div><table class="v2u2t sm"><thead><tr><th>id</th><th class="v2u2kh">owner_id</th>'
            f'<th>title</th><th>due</th></tr></thead><tbody>{bt}</tbody></table></div>'
            '<i class="v2u2link">owner_id → id</i>'
            f'<div><div class="v2u2tab">members · 팀원</div><table class="v2u2t sm"><thead><tr><th>id</th><th>name</th><th>email</th></tr></thead>'
            f'<tbody>{mt}</tbody></table></div></div>')


def rules():
    """세 사람이 동시에 할 일을 보냄 → 표에 들어감 · 기한 형식이 틀린 하나는 거절."""
    sends = [("김하늘", "주간 보고서 작성 · 2026-11-27", False, .3), ("이준호", "신규 입사자 교육 자료 · 2026-11-25", False, .5),
             ("박서연", "내년 예산안 검토 · 「월말쯤」", True, .7)]
    left = "".join(f'<div class="v2u2snd{" bad" if bad else ""}" style="--d:{d:.2f}s"><b>{who}</b><span>{x}</span></div>'
                   for who, x, bad, d in sends)
    ok = "".join(f'<tr class="v2u2tr" style="--d:{d:.2f}s"><td>{t}</td><td>{dt}</td><td>{w}</td></tr>'
                 for t, dt, w, d in [("주간 보고서 작성", "2026-11-27", "김하늘", 1.7), ("신규 입사자 교육 자료", "2026-11-25", "이준호", 1.9)])
    return ('<div class="v2u2rules"><div class="v2u2snds"><div class="v2u2h">동시에 보낸 할 일</div>' + left + '</div>'
            '<div class="v2u2go"><i style="--d:1.2s">→</i><i style="--d:1.3s">→</i><i style="--d:1.4s">→</i></div>'
            '<div><div class="v2u2sheet"><div class="v2u2tab">tasks</div><table class="v2u2t sm"><thead><tr>'
            '<th>할 일</th><th class="v2u2kh">기한 · date 형식</th><th>담당자</th></tr></thead>'
            f'<tbody>{ok}</tbody></table></div>'
            '<div class="v2u2rej" style="--d:2.4s">✕ 박서연 · 「월말쯤」 · 날짜 형식 아님 → 저장 거절</div></div></div>')


def result():
    """SQL 실행 결과 — 코드 줄 뒤에 나타나는 결과 표."""
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [("내년 예산안 검토", "2026-11-18"), ("신규 입사자 교육 자료", "2026-11-25")])
    return (f'<div class="v2u2res"><span>결과 · 2행</span><table class="v2u2t sm"><thead><tr><th>title</th><th>due</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def history():
    """데이터 기록의 변화 — 종이 장부 → 엑셀 파일 → 데이터베이스 → 클라우드 DB.
    같은 할 일 한 건이 단계마다 어떤 모양으로 남는지 + 쌓이는 방식 · 쌓이는 양 막대. 평택대 교안 「데이터 관리의 변화」 구조."""
    R = ("주간 보고서 작성", "11/27", "김하늘")
    paper = (f'<div class="v2hP"><p>{R[1]} {R[0]} — {R[2]}</p><p>11/25 신규 입사자 교육 — 이준호</p>'
             '<p class="x">11/18 예산안 검토 — 박서연</p></div>')
    def grid(rows, head, idcol=False):
        th = "".join(f"<th>{h}</th>" for h in head)
        tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
        return f'<table class="v2hT{" db" if idcol else ""}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
    xl = ('<div class="v2hX"><div class="f">할일_최종_v3.xlsx</div>'
          + grid([(R[0], R[1], R[2]), ("교육 자료", "11/25", "이준호")], ["A 할 일", "B 기한", "C 담당"]) + '</div>')
    db = grid([("41", R[0], "2026-11-27", "1"), ("42", "교육 자료", "2026-11-25", "2"), ("43", "<em>새 행</em>", "…", "…")],
              ["id", "title", "due", "owner_id"], True)
    cl = ('<div class="v2hC">' + grid([("41", R[0], "2026-11-27"), ("42", "교육 자료", "2026-11-25")], ["id", "title", "due"], True)
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
    """SQL 작성의 변화 — 손으로 찾기 → SQL 직접 작성 → 말로 요청(Claude Code 가 SQL) → MCP 로 직접 실행.
    같은 질문 「진행 중인 할 일」이 단계마다 어떤 모양인지 + 사람 · AI 가 하는 일. 평택대 교안 「분석 도구의 변화」 구조."""
    pic = [
        '<div class="v2qF"><span>상태 ▾ 필터</span><p>진행 중 ✓</p><p class="x">완료</p><p class="x">할 일</p></div>',
        '<pre class="v2qS">select title, due\nfrom tasks\nwhere status = \'진행 중\'\norder by due;</pre>',
        '<div class="v2qM"><p class="me">진행 중인 할 일만 보여 줘</p><pre class="v2qS sm">select title, due …</pre><small>SQL Editor 에 붙여 넣기 · 실행</small></div>',
        '<div class="v2qM"><p class="me">진행 중인 할 일만 보여 줘</p><p class="ai">진행 중 2건 · 내년 예산안 검토 · 신규 입사자 교육 자료</p></div>',
    ]
    st = [("손으로 찾기", "엑셀 필터 · 장부", "줄마다 눈으로 찾음", "—"),
          ("SQL 직접 작성", "개발자 · 분석가", "문법 학습 · 작성 · 실행", "—"),
          ("말로 요청", "Claude Code · 2-4", "요청 · 붙여 넣어 실행 · 결과 확인", "SQL 작성"),
          ("MCP 연결", "Claude Code · 2-5", "요청 · 결과 확인", "SQL 작성 · 실행 · 보고")]
    c = ""
    for i, (name, who, me, ai) in enumerate(st):
        d = .3 + i * 1.0
        if i:
            c += f'<i class="v2hA" style="--d:{d - .2:.1f}s">→</i>'
        c += (f'<div class="v2hK{" on" if i == 3 else ""}" style="--d:{d:.1f}s"><b class="n">{name}</b><small class="w">{who}</small>'
              f'<div class="pic">{pic[i]}</div>'
              f'<dl><dt>사람이 하는 일</dt><dd>{me}</dd><dt>AI 가 하는 일</dt><dd>{ai}</dd></dl></div>')
    return ('<div class="v2hTop"><span>예전</span><i></i><span>바이브코딩</span></div>'
            f'<div class="v2hQ">「진행 중인 할 일만 보여 줘」 · 같은 질문</div><div class="v2h">{c}</div>')


def slides():
    return [
        light("데이터 기록의 변화", history()
              + note("2부", "Supabase · 클라우드 DB 한 곳에 할 일 기록"), T),
        light("엑셀 표", phmap("v2_u2_tablet.webp", "칸을 나눠 기록하는 돌판", *GEN, viz2.maprows([
            ("엑셀 파일", "데이터베이스", "Supabase 프로젝트 하나"), ("시트", "표 (테이블)", "tasks · members"),
            ("가로 한 줄", "행", "할 일 한 건"), ("세로 한 칸", "열", "할 일 · 기한 · 담당자"),
            ("칸 하나", "값", "2026-11-27")], "엑셀", "데이터베이스")), T),
        light("할 일 표의 행과 열", sheet()
              + note("관계형 데이터베이스", "데이터를 행 · 열로 된 표에 담는 방식 · 표끼리 서로 연결"), T),
        light("엑셀과 데이터베이스", rules()
              + note("엑셀과 차이", "엑셀 · 아무 칸에 아무 값 / 데이터베이스 · 열마다 형식 · 여러 사람이 동시에"), T),
        light("표와 표의 관계", relation()
              + viz2.pair(
                  "한 표에 다 넣기", [("팀원 이메일 변경", "할 일 행마다 고치기"), ("오타", "「김하늘」 「김 하늘」 섞임")],
                  "표 두 개 · 번호로 연결", [("팀원 이메일 변경", "members 한 칸만 고치기"), ("오타", "번호라 섞이지 않음")]), T),
        light("SQL", codemap([
            ("select title, due", "할 일 · 기한 열만"),
            ("from tasks", "tasks 표에서"),
            ("where status = '진행 중'", "상태가 진행 중인 행만"),
            ("order by due;", "기한이 빠른 순서")], ask="「진행 중인 할 일만 보여 줘」", title="SQL")
              + result()
              + note("SQL 작성", "Claude Code 가 씀 · 사람은 결과 표를 확인"), T),
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
  /* 2-1 · 할 일 표 */
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
"""
