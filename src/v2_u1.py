"""2-1 웹 앱의 데이터 흐름.

클라이언트 · 서버 · DB(1-6 웹 구조 복습 · 한 장)
→ 요청과 응답(장면: 로딩 → GET → SQL → 행 → JSON → 화면) → 요청 · 응답 읽기 → 쓰기 요청(POST → insert → 201 → 목록 추가)
→ 상태 코드 → API(서버가 열어 둔 창구 · 메뉴판 비유).
외부 API(공휴일)는 2-5 · MCP 는 2-6.
사실 출처: supabase.com/docs/guides/api (REST · /rest/v1/표이름) · developer.mozilla.org HTTP 메서드 · 상태 코드
· developer.chrome.com/docs/devtools/network
"""
import viz2
from deck import light
from hx import note
from stats_hx import src
from v2kit import codemap
from v3kit import phmap
import v2scene
from v2scene import reqres, steps

T = "2-1"
GEN = ("AI 생성 그림 · Z-Image Turbo (Apache 2.0)", "https://huggingface.co/Tongyi-MAI/Z-Image-Turbo")
SB_API = ("Supabase · REST API", "https://supabase.com/docs/guides/api")
MDN_M = ("MDN · HTTP 요청 메서드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Methods")
MDN_S = ("MDN · HTTP 상태 코드", "https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status")
NETP = ("Chrome DevTools · Network", "https://developer.chrome.com/docs/devtools/network")

CSS = ""


def slides():
    return [
        light("클라이언트 · 서버 · DB", viz2.maprows([
            ("클라이언트", "브라우저 · 화면", "요청을 보내고 받은 데이터로 화면을 그림"),
            ("서버", "요청을 받는 프로그램", "누가 무엇을 원하는지 확인 · DB 에 묻기"),
            ("DB", "데이터 저장소", "표에 행으로 보관 · 서버만 직접 접근")], "칸", "하는 일")
              + note("1-6 웹 구조", "같은 세 칸 · 2부는 서버 · DB 를 Supabase 가 맡음"), T),
        light("요청과 응답", reqres()
              + steps([("①", "화면이 데이터 요청", 1.0), ("②", "서버가 SQL 로 DB 조회", 2.1), ("③", "DB 가 행 3개 돌려줌", 2.6),
                       ("④", "서버가 JSON 으로 응답", 4.5), ("⑤", "받은 데이터로 화면 그림", 5.8)])
              + src(SB_API, NETP), T),
        light("요청과 응답 읽기", codemap([
            ("GET", "방식 · 가져오기"),
            ("/rest/v1/tasks?select=*", "주소 · tasks 표의 모든 열"),
            ("200 OK", "상태 · 성공"),
            ('[{ "id": 41, "title": "주간 보고서 작성", … }]', "내용 · JSON · 할 일 한 건이 { } 하나"),
        ], title="Network 탭의 요청 한 줄")
              + note("직접 보기", "F12 → Network → 새로고침 · 요청 줄을 눌러 Response")
              + src(MDN_M, NETP), T),
        light("쓰기 요청", reqres(write=True)
              + steps([("①", "「추가」 클릭 · POST", 1.0), ("②", "서버가 insert", 2.1), ("③", "DB 에 새 행", 2.6),
                       ("④", "201 · 만든 행 응답", 4.5), ("⑤", "목록에 한 줄 추가", 5.8)])
              + src(SB_API, MDN_M), T),
        light("요청 방식과 상태 코드", viz2.pair(
            "방식", [("GET", "가져오기 · 보드 보기"), ("POST", "새로 만들기 · 할 일 추가"),
                    ("PATCH", "고치기 · 상태 변경"), ("DELETE", "지우기 · 할 일 삭제")],
            "상태 코드", [("200 · 201", "성공 · 만듦"), ("401 · 403", "로그인 필요 · 권한 없음"),
                       ("404", "주소 · 행 없음"), ("500", "서버 안의 오류")], hl="")
              + note("에러를 전할 때", "방식 · 주소 · 상태 코드 세 가지를 같이")
              + src(MDN_M, MDN_S), T),
        light("API", phmap("v2_u3_menu.webp", "메뉴판을 보고 주문하는 손님", *GEN, viz2.maprows([
            ("주방", "서버", "요청을 처리"), ("메뉴판", "API 목록", "받는 요청 · 주소 · 형식"),
            ("주문서", "요청", "GET /rest/v1/tasks"), ("나온 음식", "응답", "200 · JSON"),
            ("다른 가게 메뉴판", "외부 API", "공휴일 · 날씨 (2-5)")], "식당", "API"))
              + note("API", "서버가 정해 둔 요청 창구 · 형식대로 요청하면 응답"), T),
    ]
