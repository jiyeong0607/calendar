let selectedDate = null; 
let cachedStatusMap = {}; // 체크 상태 캐시

// 팝업 열기
function showPopup(dateStr) {
  selectedDate = dateStr;
  document.getElementById("popupTitle").innerText = dateStr;
  document.getElementById("popup").style.display = "block";
  loadTodos(); // 할 일 불러오기
}

// 팝업 닫기
function closePopup() {
  document.getElementById("popup").style.display = "none";
  selectedDate = null;
  cachedStatusMap = {}; // 초기화
}

// 할 일 불러오기
function loadTodos() {
  const studentId = localStorage.getItem("studentId");
  const todoList = document.getElementById("todoList");
  todoList.innerHTML = "";

  fetch(`/api/todos?date=${selectedDate}`)
    .then(res => res.json())
    .then(todos => {
      fetch(`/api/status/${studentId}`)
        .then(res => res.json())
        .then(statusList => {
          const statusMap = {};
          statusList.forEach(item => {
            statusMap[item.todo_id] = item.is_done;
          });
          cachedStatusMap = statusMap;

          todos.forEach(todo => { 
            const li = document.createElement("li");
            li.className = "todo-item";

            const checkbox = document.createElement("input"); 
            checkbox.type = "checkbox";
            checkbox.checked = statusMap[todo.id] === true;

            checkbox.onchange = () => {
              fetch("/api/status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  student_id: studentId,
                  todo_id: todo.id,
                  is_done: checkbox.checked
                })
              }).then(() => {
                cachedStatusMap[todo.id] = checkbox.checked;
              });
            };

            const span = document.createElement("span");
            span.innerText = todo.content;

            const deleteBtn = document.createElement("button");
            deleteBtn.innerText = "삭제";
            deleteBtn.className = "delete-btn";
            deleteBtn.onclick = () => {
              fetch(`/api/todos/${todo.id}`, { method: "DELETE" })
                .then(() => {
                  loadTodos();
                  renderCalendar(currentYear, currentMonth); // 삭제되면 달력도 다시 그림
                });
            };

            li.appendChild(checkbox);
            li.appendChild(span);
            li.appendChild(deleteBtn);
            todoList.appendChild(li);
          });
        });
    });
}

// 일정 추가 버튼
window.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("addTodoBtn");
  if (addBtn) {
    addBtn.onclick = () => {
      const input = document.getElementById("newTodo");
      const title = input.value.trim();
      const studentId = localStorage.getItem("studentId");

      if (!title || !selectedDate || !studentId) {
        alert("할 일 내용을 입력해주세요.");
        return;
      }

      fetch("/api/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          studentId,
          title,
          date: selectedDate
        })
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            input.value = "";
            loadTodos(); // 추가 후 목록 다시 불러옴
            renderCalendar(currentYear, currentMonth); // 색상 반영용
          } else {
            alert("일정 추가 실패: " + (data.error || "서버 오류"));
          }
        })
        .catch(() => {
          alert("서버 요청 실패");
        });
    };
  }
});


