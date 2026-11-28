"""2-5 키 관리.

키 종류(Supabase URL · publishable · secret · DB 비밀번호) → 비유(출입증) → 키를 두는 곳(.env.local · 이름은 Claude Code 가 정함)
→ push 와 .env.local(장면) → 실습(키 점검).
사실 출처: nextjs.org/docs (환경변수 · NEXT_PUBLIC_ 은 브라우저 번들에 포함) · supabase.com/docs/guides/api/api-keys
"""
import viz2
from deck import ba, flow, lab, light
from hx import checks, code, esc, note
from stats_hx import src
import v2scene
from v2kit import brief, chat, codemap, shot

T = "2-5"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
NEXTENV = ("Next.js · Environment Variables", "https://nextjs.org/docs/app/guides/environment-variables")
KEYS = ("Supabase · API keys", "https://supabase.com/docs/guides/api/api-keys")
FUNC = ("Vercel · Functions", "https://vercel.com/docs/functions")
CSS = """
  /* 2-5 · push 와 .env (v26p) */
  .v26p{display:grid; grid-template-columns:1fr 220px 1fr; gap:22px; align-items:center; margin:6px 0 14px;}
  .v26p .pn{border:1.5px solid #C9CFD8; border-radius:12px; background:#fff; padding:10px 14px; display:flex; flex-direction:column; gap:7px; min-height:230px;}
  .v26p .pn .h{font-size:17px; font-weight:800; color:#16233A; margin-bottom:4px;}
  .v26p .f{display:flex; align-items:center; gap:10px; border:1px solid #E3E7EC; border-radius:8px; padding:7px 12px; background:#F6F8FA;}
  .v26p .f b{font-family:var(--mono); font-size:15px; color:#1F3A5F;} .v26p .f em{margin-left:auto; font-style:normal; font-size:12.5px; font-weight:800; border-radius:8px; padding:2px 8px;}
  .v26p .f.key em{color:#B85A00; background:#FFE3C4;}
  .v26p .f.nw{opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .f.no{opacity:0; border-style:dashed; background:#FDECEA; animation:v26in .35s var(--d) forwards;} .v26p .f.no b{text-decoration:line-through; color:#C0392B;} .v26p .f.no em{color:#C0392B;}
  .v26p .mid{display:flex; flex-direction:column; gap:16px; align-items:stretch;}
  .v26p .gi{border:2px solid #F28C28; background:#FFF8F0; border-radius:10px; padding:8px 12px; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .gi span{display:block; font-size:13px; font-weight:800; color:#E07A12;} .v26p .gi code{font-size:17px; font-weight:700;}
  .v26p .cmd{text-align:center; font-family:var(--mono); font-size:16px; font-weight:700; color:#fff; background:#1F3A5F; border-radius:10px; padding:8px; opacity:0; animation:v26in .35s var(--d) forwards;}
  .v26p .gh{border-color:#1F3A5F;}
  @keyframes v26in{from{opacity:0} to{opacity:1}}
  @media print{.v26p .f.nw,.v26p .f.no,.v26p .gi,.v26p .cmd,.v26k .warn,.v26k .nk{opacity:1; animation:none}}
"""
SMCP = ("Supabase · MCP", "https://supabase.com/docs/guides/getting-started/mcp")


def push_scene():
    """push 와 .env — 내 폴더 파일 4개 · .gitignore · GitHub 저장소. 저장소에 파일이 하나씩 생기고 .env 자리는 「없음」."""
    loc = [("app/page.tsx", ""), ("app/api/pages/route.ts", ""), (".gitignore", ""), (".env.local", "key")]
    lf = "".join(f'<div class="f {k}"><b>{n}</b>{"<em>키</em>" if k else ""}</div>' for n, k in loc)
    gh = [("app/page.tsx", 1.6), ("app/api/pages/route.ts", 1.9), (".gitignore", 2.2)]
    rf = "".join(f'<div class="f nw" style="--d:{d}s"><b>{n}</b></div>' for n, d in gh)
    rf += '<div class="f no" style="--d:2.8s"><b>.env.local</b><em>없음 · 제외됨</em></div>'
    return ('<div class="v26p"><div class="pn"><div class="h">내 컴퓨터 · 프로젝트 폴더</div>' + lf + '</div>'
            '<div class="mid"><div class="gi" style="--d:.6s"><span>.gitignore</span><code>.env*.local</code></div>'
            '<div class="cmd" style="--d:1.2s">git push</div></div>'
            '<div class="pn gh"><div class="h">GitHub 저장소</div>' + rf + '</div></div>')


def slides():
    return [
        light("키 종류", viz2.maprows([
            ("NEXT_PUBLIC_SUPABASE_URL", "프로젝트 주소", "브라우저에 보여도 됨"),
            ("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY", "publishable 키", "브라우저에 보여도 됨 · RLS 로 보호"),
            ("SUPABASE_SECRET_KEY", "secret 키", "서버에서만 · RLS 무시"),
            ("DB 비밀번호 · MCP 토큰", "DB · 외부 서비스 접속", "서버 · 내 컴퓨터에만")], "이름 · 예", "무엇 · 어디까지")
              + note("Connect 화면 (2-4)", ".env.local 에 URL · publishable 키가 들어감 · secret 키는 직접 넣을 때만")
              + src(KEYS), T),
        light("출입증 비유", shot("v2_u6_key.webp", "출입증 · 잠긴 서랍에 보관", [
            ("출입증", "키"), ("출입문", "Supabase · 외부 서비스"), ("잠긴 서랍", ".env.local · Vercel 환경변수"), ("게시판에 붙인 출입증", "코드 · GitHub 에 적은 키")])
              + src(GEN), T),
        light("키를 두는 곳", viz2.pair(
            "코드에 직접", [("위치", "page.tsx 안 문자열"), ("GitHub 에 올리면", "누구나 검색 · 복사"), ("키 교체", "코드 수정 · 다시 커밋")],
            ".env.local 파일", [("위치", "프로젝트 폴더의 .env.local"), ("GitHub 에 올리면", ".gitignore 로 제외 · 안 올라감"), ("키 교체", ".env.local 한 줄")])
              + note("환경변수", "코드 밖에 둔 설정 값 · 키 이름과 넣을 곳은 Claude Code 가 정함 · 사람은 값만 붙여 넣기"), T),
        light("push 와 .env.local", push_scene()
              + note(".gitignore", "목록에 있는 파일은 커밋 · push 에서 빠짐 · 키는 내 컴퓨터에만 · 배포는 Vercel 환경변수 (2-4)"), T),
        # ── 실습
        lab("2-5", "키 점검", T, "키가 .env.local 에만 있고 GitHub 에 올라가지 않는지 확인한다",
            ["코드에 직접 적힌 키 찾기 요청", "있으면 .env.local 로 옮기기 · 이름은 Claude Code 가 정함", ".env.local 이 .gitignore 에 있는지 확인",
             "GitHub 저장소에서 키 검색"],
            ["코드에 직접 적힌 키 0건", "git status · GitHub 어디에도 .env.local · 키 없음"], files="2-4 까지의 앱"),
        brief("2-5", T, ["코드에서 키 찾기", ".env.local 로 옮기기", ".gitignore 확인", "GitHub 에서 검색"],
              [("목표", "키가 새는 곳 찾기 · 막기"), ("범위", ".env.local · 코드 · 커밋 기록"),
               ("진행 방식", "찾은 것부터 보여 주기 · 고치기는 승인 뒤"), ("하지 말 것", "키를 대화창에 붙여 넣기")],
              ["환경변수", ".env.local", ".gitignore", "secret 키"],
              ["코드에 직접 적힌 키 0건", "GitHub 검색 결과 0건"],
              "이미 커밋한 키는 지우는 것으로 끝나지 않음 · Supabase 에서 새 키로 교체"),
        light("실습 2-5 확인", checks([
            ("코드에 직접 적힌 키가 없나", "키는 .env.local 에만"), (".env.local 이 .gitignore 에 있나", "git status 에 안 보임"),
            ("GitHub 저장소에 키가 없나", "저장소 검색"), ("앱이 그대로 동작하나", "페이지 목록이 보임")],
            "넷 다 「예」 → 커밋 · 2-6 MCP"), T),
    ]
