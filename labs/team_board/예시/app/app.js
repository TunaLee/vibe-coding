// 팀 할 일 보드 — PRD F1~F5. 할 일은 이 브라우저(localStorage)에만 저장된다.
const TEAM = ["김하늘", "이도윤", "박서준", "최유나"];
const STEPS = ["할 일", "진행 중", "완료"];
const KEY = "team-tasks";

const $ = (id) => document.getElementById(id);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
const save = (list) => localStorage.setItem(KEY, JSON.stringify(list));
const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const late = (t) => t.status !== "완료" && t.due < today(); // F4 기한 지남
const md = (d) => `${Number(d.slice(5, 7))}/${Number(d.slice(8, 10))}`;

let opened = null; // 상세 창의 할 일

// F2 담당자별 보기
$("who").innerHTML = ["전체", ...TEAM].map((n) => `<option>${n}</option>`).join("");
$("who").onchange = render;

// F1 보드
function render() {
  const who = $("who").value;
  const list = load().filter((t) => who === "전체" || t.owner === who);
  $("board").innerHTML = STEPS.map((s) => {
    const cards = list.filter((t) => t.status === s)
      .sort((a, b) => late(b) - late(a) || a.due.localeCompare(b.due)); // 기한 지남이 맨 위
    return `<section class="col"><h2>${s} <span>${cards.length}</span></h2>${cards.map((t) =>
      `<div class="card${late(t) ? " late" : ""}" data-id="${t.id}"><b>${t.title}</b>
       <small>${t.owner} · ${md(t.due)}${late(t) ? ' <em>기한 지남</em>' : ""}</small></div>`).join("")}</section>`;
  }).join("");
  document.querySelectorAll(".card").forEach((c) => (c.onclick = () => openDetail(Number(c.dataset.id))));
}

// F3 할 일 추가
$("add").onclick = () => {
  const f = $("taskForm");
  f.reset();
  f.owner.innerHTML = TEAM.map((n) => `<option>${n}</option>`).join("");
  $("err").textContent = "";
  $("form").showModal();
};
$("taskForm").addEventListener("submit", (e) => {
  const f = e.target;
  const t = { id: Date.now(), title: f.title.value.trim(), owner: f.owner.value, due: f.due.value, status: "할 일" };
  if (!t.title) { e.preventDefault(); $("err").textContent = "할 일을 적어야 저장된다"; return; }
  save([...load(), t]);
  render();
});
$("close").onclick = () => $("form").close();

// F5 상태 변경 · 삭제
function openDetail(id) {
  opened = load().find((t) => t.id === id);
  $("dTitle").textContent = opened.title;
  $("dInfo").textContent = `${opened.owner} · 기한 ${opened.due} · ${opened.status}`;
  const i = STEPS.indexOf(opened.status);
  $("dPrev").disabled = i === 0;
  $("dNext").disabled = i === STEPS.length - 1;
  $("detail").showModal();
}
const move = (n) => {
  save(load().map((t) => (t.id === opened.id ? { ...t, status: STEPS[STEPS.indexOf(t.status) + n] } : t)));
  $("detail").close();
  render();
};
$("dNext").onclick = () => move(1);
$("dPrev").onclick = () => move(-1);
$("dDel").onclick = () => { save(load().filter((t) => t.id !== opened.id)); $("detail").close(); render(); };
$("dClose").onclick = () => $("detail").close();

render();
