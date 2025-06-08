let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth();
const todayDateStr = new Date().toISOString().slice(0, 10);

// 로그인 상태 확인: studentId 없으면 로그인 페이지로 이동
if (!localStorage.getItem("studentId")) {
  window.location.href = "login.html";
}

function renderCalendar(year, month) {
  const studentId = localStorage.getItem("studentId");
  if (!studentId) return;

  const monthTitle = document.getElementById("monthTitle");
  const calendarBody = document.getElementById("calendarBody");
  monthTitle.innerText = `${year}년 ${month + 1}월`;
  calendarBody.innerHTML = "";

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();

  let row = document.createElement("tr");
  for (let i = 0; i < firstDay; i++) row.appendChild(document.createElement("td"));

  for (let date = 1; date <= lastDate; date++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(date).padStart(2, "0")}`;
    const cell = document.createElement("td");
    cell.innerText = date;
    if (dateStr === todayDateStr) cell.classList.add("today");

    fetch(`/api/todos?date=${dateStr}`)
      .then(res => res.json())
      .then(todos => {
        if (todos.length > 0) {
          const maxCount = 5;
          const level = Math.min(todos.length, maxCount);
          const r = Math.max(0, 47 - level * 5);
          const g = Math.max(0, 93 - level * 5);
          const b = Math.max(0, 80 - level * 5);
          cell.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
          cell.style.color = "white";
        } else {
          cell.style.backgroundColor = "white";
          cell.style.color = "black";
        }
      });

    cell.onclick = () => showPopup(dateStr);
    row.appendChild(cell);

    if ((firstDay + date) % 7 === 0) {
      calendarBody.appendChild(row);
      row = document.createElement("tr");
    }
  }

  if (row.children.length > 0) {
    while (row.children.length < 7) row.appendChild(document.createElement("td"));
    calendarBody.appendChild(row);
  }
}

function prevMonth() {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar(currentYear, currentMonth);
}

function nextMonth() {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar(currentYear, currentMonth);
}

// 로그아웃 함수
function logout() {
  localStorage.removeItem("studentId");
  window.location.href = "login.html";
}

renderCalendar(currentYear, currentMonth);

