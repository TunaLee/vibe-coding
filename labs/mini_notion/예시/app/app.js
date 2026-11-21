// 미니 노션 — 개발계획.md F1~F5. 페이지 · 블록은 이 브라우저(localStorage)에만 저장된다.
const KEY = "mini-notion";
const uid = () => Math.random().toString(36).slice(2, 9);

function sample() {
  const id = uid();
  return {
    current: id,
    pages: [{ id, title: "시작하기", blocks: [
      { id: uid(), type: "h", text: "미니 노션" },
      { id: uid(), type: "p", text: "글을 쓰다가 「/」 를 입력해 보세요." },
      { id: uid(), type: "todo", text: "새 페이지 만들기", done: false },
      { id: uid(), type: "hr", text: "" },
      { id: uid(), type: "p", text: "" },
    ] }],
  };
}

let state;
try { state = JSON.parse(localStorage.getItem(KEY)) || sample(); } catch { state = sample(); }
const save = () => localStorage.setItem(KEY, JSON.stringify(state));
const page = () => state.pages.find(p => p.id === state.current) || state.pages[0];

const $pages = document.getElementById("pages");
const $title = document.getElementById("title");
const $blocks = document.getElementById("blocks");
const $slash = document.getElementById("slash");

// F1 페이지 목록
function renderPages() {
  $pages.innerHTML = "";
  for (const p of state.pages) {
    const li = document.createElement("li");
    li.textContent = p.title || "제목 없음";
    if (p.id === page().id) li.className = "on";
    li.onclick = () => { state.current = p.id; save(); render(); };
    $pages.append(li);
  }
}
document.getElementById("newPage").onclick = () => {
  const p = { id: uid(), title: "", blocks: [{ id: uid(), type: "p", text: "" }] };
  state.pages.push(p); state.current = p.id; save(); render(); $title.focus();
};
document.getElementById("delPage").onclick = () => {
  if (state.pages.length === 1) return alert("마지막 페이지는 지울 수 없다");
  if (!confirm(`「${page().title || "제목 없음"}」 페이지를 지울까요?`)) return;
  state.pages = state.pages.filter(p => p.id !== page().id);
  state.current = state.pages[0].id; save(); render();
};
$title.oninput = () => { page().title = $title.textContent; save(); renderPages(); };
$title.onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); focusBlock(0); } };

// F2 블록 편집
function renderBlocks() {
  $blocks.innerHTML = "";
  page().blocks.forEach((b, i) => $blocks.append(blockEl(b, i)));
}
function blockEl(b, i) {
  const row = document.createElement("div");
  row.className = `block ${b.type}${b.done ? " done" : ""}`;
  row.dataset.i = i;
  const handle = document.createElement("span");
  handle.className = "handle"; handle.textContent = "⋮⋮"; handle.title = "끌어서 옮기기";
  row.append(handle);
  if (b.type === "hr") { row.append(document.createElement("hr")); row.tabIndex = 0; row.onkeydown = e => { if (e.key === "Backspace") removeBlock(i); }; }
  else {
    if (b.type === "todo") {
      const cb = document.createElement("input");
      cb.type = "checkbox"; cb.checked = !!b.done;
      cb.onchange = () => { b.done = cb.checked; row.classList.toggle("done", b.done); save(); };
      row.append(cb);
    }
    const t = document.createElement("div");
    t.className = "text"; t.contentEditable = "true"; t.spellcheck = false;
    t.textContent = b.text;
    t.dataset.ph = b.type === "h" ? "제목" : b.type === "todo" ? "할 일" : "";
    t.oninput = () => { b.text = t.textContent; save(); slashCheck(t, i); };
    t.onkeydown = e => keydown(e, t, i);
    row.append(t);
  }
  dragSetup(row, handle, i);
  return row;
}
function keydown(e, t, i) {
  if (!$slash.hidden && ["ArrowDown", "ArrowUp", "Enter", "Escape"].includes(e.key)) return slashKey(e, i);
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    const cur = page().blocks[i];
    const type = cur.type === "todo" ? "todo" : "p";
    page().blocks.splice(i + 1, 0, { id: uid(), type, text: "", done: false });
    save(); renderBlocks(); focusBlock(i + 1);
  } else if (e.key === "Backspace" && t.textContent === "" && page().blocks.length > 1) {
    e.preventDefault(); removeBlock(i);
  }
}
function removeBlock(i) { page().blocks.splice(i, 1); save(); renderBlocks(); focusBlock(Math.max(0, i - 1), true); }
function focusBlock(i, end) {
  const t = $blocks.children[i]?.querySelector(".text");
  if (!t) return;
  t.focus();
  if (end) { const r = document.createRange(); r.selectNodeContents(t); r.collapse(false); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
}

// F3 「/」 메뉴
let slashFor = -1;
function slashCheck(t, i) {
  if (t.textContent === "/") {
    const r = t.getBoundingClientRect();
    $slash.style.left = `${r.left + scrollX}px`; $slash.style.top = `${r.bottom + scrollY + 4}px`;
    $slash.hidden = false; slashFor = i; mark(0);
  } else $slash.hidden = true;
}
const items = () => [...$slash.children];
const mark = k => items().forEach((li, j) => li.classList.toggle("on", j === k));
function slashKey(e, i) {
  e.preventDefault();
  const k = items().findIndex(li => li.classList.contains("on"));
  if (e.key === "ArrowDown") mark((k + 1) % items().length);
  else if (e.key === "ArrowUp") mark((k + items().length - 1) % items().length);
  else if (e.key === "Enter") choose(items()[k].dataset.type);
  else { $slash.hidden = true; }
}
items().forEach(li => li.onmousedown = e => { e.preventDefault(); choose(li.dataset.type); });
function choose(type) {
  const b = page().blocks[slashFor];
  Object.assign(b, { type, text: "", done: false });
  if (type === "hr") page().blocks.splice(slashFor + 1, 0, { id: uid(), type: "p", text: "" });
  $slash.hidden = true; save(); renderBlocks(); focusBlock(type === "hr" ? slashFor + 1 : slashFor);
}

// F4 블록 끌어 옮기기
let dragFrom = -1;
function dragSetup(row, handle, i) {
  handle.draggable = true;
  handle.ondragstart = e => { dragFrom = i; e.dataTransfer.effectAllowed = "move"; e.dataTransfer.setDragImage(row, 10, 10); };
  row.ondragover = e => { if (dragFrom < 0) return; e.preventDefault(); row.classList.add("over"); };
  row.ondragleave = () => row.classList.remove("over");
  row.ondrop = e => {
    e.preventDefault(); row.classList.remove("over");
    if (dragFrom < 0 || dragFrom === i) return;
    const [b] = page().blocks.splice(dragFrom, 1);
    page().blocks.splice(dragFrom < i ? i - 1 : i, 0, b);
    dragFrom = -1; save(); renderBlocks();
  };
  handle.ondragend = () => { dragFrom = -1; };
}

// F5 저장 · 마지막 페이지 열기
function render() { $title.textContent = page().title; renderPages(); renderBlocks(); }
render();
