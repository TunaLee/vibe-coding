// 할 일 목록 — 실습 1-2 ③ 위임형 첫 작업용 뼈대
// 지금 상태: 목록을 그리는 코드만 있다. 「추가」 버튼과 「남은 할 일」 개수는 아직 동작하지 않는다.
const todos = [
  { text: "기획서 초안 쓰기", done: false },
  { text: "미니 노션 아이디어 정리", done: true },
];

function render() {
  const list = document.getElementById("list");
  list.innerHTML = "";
  for (const t of todos) {
    const li = document.createElement("li");
    li.className = t.done ? "done" : "";
    li.innerHTML = `<input type="checkbox" ${t.done ? "checked" : ""} /><span>${t.text}</span>`;
    list.appendChild(li);
  }
}

render();
