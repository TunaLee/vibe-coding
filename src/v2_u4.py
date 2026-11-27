"""2-4 데이터 다루기 (DB).

데이터 구조 설계(표 두 개 · AI 와 설계) → Supabase 연결(키 두 종류) → CRUD(우리말 뜻 · 코드 뜻)
→ 로그인 → 권한 RLS(배경 → 비유 → 정책 뜻 → 두 계정 확인) → 실습.
DB 개념(표 · 행 · 열 · Supabase 소개)은 2-1 에서 설명 — 여기서는 다시 설명하지 않는다.
사실 출처: supabase.com/docs/guides/api/api-keys · /database/postgres/row-level-security · /auth · /pricing
"""
import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
import v2scene
from v2kit import brief, chat, codemap, shot

T = "2-4"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
KEYS = ("Supabase · API keys", "https://supabase.com/docs/guides/api/api-keys")
RLS = ("Supabase · Row Level Security", "https://supabase.com/docs/guides/database/postgres/row-level-security")

CSS = """
  /* 2-4 · RLS 동작 (v25r) */
  .v25r{grid-template-columns:380px 1fr 260px 1fr 250px;}
  .v25l{display:flex; flex-direction:column; gap:14px; justify-content:center;}
  .v25b .net{margin-top:0;} .v25b .nr{grid-template-columns:0 1fr 60px 150px;} .v25b .nr .ok.no{color:#C0392B;}
  .v25r .cl.bad{animation:v25bad .35s var(--d) forwards;}
  .v25r tr.del td{animation:v25del .5s var(--d) forwards;}
  @keyframes v25bad{to{opacity:1; background:#FDECEA; color:#C0392B}}
  @keyframes v25del{to{text-decoration:line-through; color:#9AA5B1; background:#F4F6F9}}
  /* 2-4 · 표 그림 */
  .v2u5sheets{display:grid; grid-template-columns:.8fr 1.6fr; gap:22px; align-items:start;}
  .v2u5sh{border:1.5px solid #D9DDE3; border-radius:12px; overflow:hidden; background:#fff;}
  .v2u5sh .nm{padding:8px 14px; font-family:var(--mono); font-size:15px; font-weight:800; color:#fff; background:#1F3A5F;}
  .v2u5sh table{border-collapse:collapse; width:100%;}
  .v2u5sh th{background:#F4F6F9; font-family:var(--mono); font-size:13px; color:#3A4657; padding:7px 9px; text-align:left; border-bottom:1px solid #E3E6EA;}
  .v2u5sh td{font-size:15px; color:#16233A; padding:7px 9px; border-bottom:1px solid #EEF0F3; white-space:nowrap;}
  .v2u5sh td.k, .v2u5sh th.k{background:#FFF3E6; color:#E07A12; font-weight:800;}
  .v2u5lb{font-size:15px; font-weight:800; color:#6B7785; margin:4px 0 0;} .v2u5lb b{color:#E07A12;}
  .v2u5link{margin-top:12px; font-size:16px; color:#3A4657;} .v2u5link b{color:#E07A12;}
"""


def _sheet(name, head, rows, key=()):
    th = "".join(f'<th class="{"k" if h in key else ""}">{h}</th>' for h in head)
    tr = "".join("<tr>" + "".join(f'<td class="{"k" if head[i] in key else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="v2u5sh"><div class="nm">{name}</div><table><tr>{th}</tr>{tr}</table></div>'


def _tables():
    members = _sheet("members · 팀원", ["id", "name", "email"],
                     [["하늘", "김하늘", "haneul@…"], ["준호", "이준호", "junho@…"], ["서연", "박서연", "seoyeon@…"]], key=("id",))
    pages = _sheet("pages · 페이지", ["id", "title", "owner_id", "date", "status"],
                   [["7", "주간 회의록", "하늘", "12-04", "초안"],
                    ["8", "입사자 교육 자료", "준호", "11-25", "작성 중"],
                    ["9", "고객 설문 결과", "하늘", "11-19", "완료"]], key=("owner_id",))
    return (f'<div class="v2u5sheets">{members}{pages}</div>'
            '<div class="v2u5link"><b>owner_id 하늘</b> → members 의 김하늘 · <b>id</b> = 로그인 계정 (표에는 긴 고유 번호 · 그림은 이름)</div>')


def rls_scene():
    """RLS 동작 — 계정 B · 계정 A 브라우저가 같은 7번 삭제 요청 · Supabase 가 행마다 규칙 확인 · B 는 지운 행 0개 · A 는 1개."""
    def br(who, d_req, d_res, res, cls):
        return (f'<div class="v2sBr v25b"><div class="bar"><i></i><i></i><i></i><span>계정 {who} · 페이지 목록</span></div>'
                f'<div class="net"><div class="nr" style="--d:{d_req}s"><span class="fn">pages?id=eq.7</span><span>DELETE</span>'
                f'<span class="st"><i class="pd" style="--d:{d_res}s">(pending)</i><b class="ok {cls}" style="--d:{d_res}s">{res}</b></span></div></div></div>')
    left = '<div class="v25l">' + br("B", .4, 2.2, "200 · 지운 행 0개", "no") + br("A", 3.0, 4.8, "200 · 지운 행 1개", "") + '</div>'
    mid = ('<div class="v2sBx srv"><div class="bh"><b>Supabase</b><small>RLS 규칙</small></div>'
           '<div class="cl" style="--d:.9s">규칙 · 로그인 계정 = 작성자</div>'
           '<div class="cl bad" style="--d:1.5s">B ≠ A → 해당 행 없음</div>'
           '<div class="cl" style="--d:3.6s">A = A → 7번 삭제</div></div>')
    db = ('<div class="v2sBx db"><div class="bh"><b>pages</b><small>DB</small></div><table><tr><th>id</th><th>title · 작성자</th></tr>'
          '<tr class="del" style="--d:4.2s"><td>7</td><td>주간 회의록 · A</td></tr><tr><td>8</td><td>교육 자료 정리 · B</td></tr></table></div>')
    return ('<div class="v2s v25r">' + left + v2scene.wire("삭제 요청", "결과", .4, 2.2) + mid
            + v2scene.wire("규칙에 맞는 행만", "", 1.0, 4.2) + db + '</div>')


def slides():
    return [
        # ── 데이터 구조
        light("미니 노션 데이터 구조", _tables()
              + note("행 하나", "팀원 한 명 · 페이지 하나"), T),
        light("AI와 데이터 구조 설계", chat([
            ("me", "개발 계획 5칸 데이터 구조를 읽고 Supabase 표 설계를 제안해 줘. 만들기 전에 표 모양부터 보여 줘"),
            ("ai", "제안 · members · pages 두 표. 상태는 초안 · 작성 중 · 완료 셋만 받게 DB 에서도 막을까요?"),
            ("me", "응 · 화면과 DB 둘 다에서 막아 줘"),
            ("ai", "표 설계 · SQL 파일 저장 완료 · SQL Editor 에서 실행 필요")], "Claude Code 대화 예")
              + note("사람이 정할 것", "표 이름 · 열 · 지켜야 할 규칙 · SQL 은 Claude Code"), T),
        # ── Supabase 연결
        light("Supabase 연결 순서", flow([("프로젝트", "2-2 실습에서 만든 것"), ("표 만들기", "SQL Editor · 실행"),
                                       ("URL · 키 확인", "Settings › API Keys"), ("앱에 연결", "Claude Code"), ("확인", "Table Editor")], hl=3)
              + viz2.tiles([("무료 플랜", "프로젝트 2개 · DB 500MB"), ("일시 정지", "1주일 사용 없으면 · 대시보드에서 다시 켜기")], 2)
              + src(("Supabase · Pricing", "https://supabase.com/pricing"), KEYS), T),
        light("Supabase 키 두 종류", viz2.pair(
            "publishable 키", [("모양", "sb_publishable_…"), ("두는 곳", "브라우저 · 앱 코드"), ("할 수 있는 일", "RLS 규칙 안에서만")],
            "secret 키", [("모양", "sb_secret_…"), ("두는 곳", "서버 전용 · 브라우저 · GitHub 금지"), ("할 수 있는 일", "RLS 무시 · 모든 행")], hl="l")
              + note("이전 이름", "anon 키 = publishable · service_role 키 = secret · 2026년 말 지원 종료")
              + src(KEYS), T),
        # ── CRUD
        light("Supabase Auth 로그인", flow([("가입", "이메일 · 비밀번호"), ("확인 메일", "링크 클릭"), ("로그인", "signInWithPassword"),
                                            ("페이지 저장", "created_by = 로그인 계정")], hl=3)
              + viz2.tiles([("계정 목록", "대시보드 Authentication › Users"), ("만든 사람", "입력 칸 대신 로그인 계정")], 2)
              + src(("Supabase · Auth", "https://supabase.com/docs/guides/auth")), T),
        # ── 권한 RLS
        light("로그인만으로는 부족한 이유", viz2.pair(
            "RLS 꺼짐", [("publishable 키를 가진 누구나", "모든 페이지 읽기 · 수정 · 삭제"), ("남의 페이지 삭제", "가능"),
                       ("화면에서 버튼 숨기기", "개발자 도구로 우회")],
            "RLS 켜짐", [("규칙", "DB 가 행마다 확인"), ("남의 페이지 삭제", "DB 에서 거절"), ("화면 우회", "소용없음")])
              + note("RLS", "Row Level Security · 행 단위 권한 · 표마다 켜기")
              + src(RLS), T),
        light("팀 게시판 비유", shot("v2_u5_board.webp", "팀 게시판 · 내 쪽지만 떼기", [
            ("게시판 보기", "모두 읽기 · 로그인 전에도"), ("쪽지 붙이기", "로그인한 팀원"), ("쪽지 떼기", "내 이름표가 붙은 쪽지만")])
              + src(GEN), T),
        light("RLS 동작", rls_scene()
              + note("규칙 위치", "DB 안 · 화면 · 코드를 우회해도 같은 결과"), T),
        light("계정 두 개로 권한 확인", flow([("계정 A 로그인", "A 작성 새 페이지"), ("계정 B 로그인", "다른 브라우저 · 시크릿 창"),
                                          ("A 의 페이지 열기", "삭제 버튼 없음"), ("B 로 삭제 시도", "DB 에서 거절"), ("A 로 삭제", "성공")], hl=3)
              + note("시크릿 창", "같은 컴퓨터에서 두 번째 계정 · 로그인 정보가 따로"), T),
        # ── 실습
        lab("2-4", "Supabase 저장 · 로그인 · 권한", T, "내 앱 → 모두 같은 페이지 목록 · 로그인 · 내 페이지만 수정",
            ["2-2 의 Supabase 프로젝트 열기", "Claude Code에 표 설계 요청 · SQL 실행", "저장 위치 교체 요청", "로그인 · RLS 요청", "계정 두 개로 확인"],
            ["다른 기기에서 같은 페이지가 보임", "다른 계정 작성 페이지는 삭제 불가"],
            files="예시/개발계획.md 5 · 7 칸 (비교용)"),
        brief("2-4", T, ["Supabase 프로젝트 만들기", "표 설계 · SQL 실행", "저장 · 조회를 DB 로 교체", "로그인 · RLS", "두 계정 확인"],
              [("목표", "페이지 DB 저장 · 로그인 · 내 페이지만 수정 · 삭제"), ("입력", "개발 계획 v2 · 5 · 7 칸"),
               ("진행 방식", "표 설계 먼저 보여 주기 · 태스크 하나씩"), ("하지 말 것", "secret 키를 앱 코드에 넣기")],
              ["Supabase", "publishable 키", "RLS", "로그인"],
              ["Table Editor 에 페이지 행이 생김", "계정 B 로 계정 A 페이지 삭제 불가"],
              "SQL 오류는 SQL Editor 의 빨간 문구를 그대로 Claude Code에 붙여 넣기"),
        light("실습 2-4 확인", checks([
            ("다른 기기 · 브라우저에서 같은 페이지가 보이나", "DB 저장"), ("로그인 전에 「+ 새 페이지」가 안 보이나", "추가 권한"),
            ("다른 계정 작성 페이지를 삭제할 수 없나", "RLS"), ("앱 코드에 sb_secret_ 이 없나", "키 검색")],
            "넷 다 「예」 → 커밋 · 2-5 외부 서비스 연결"), T),
    ]
