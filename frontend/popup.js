////특정 날짜 팝업 열기
function showPopup(date) {
  const title = document.getElementById("popupTitle");
  const popup = document.getElementById("popup");
  const todoList = document.getElementById("todoList"); //todoList: 할일 목록 담을 ul

  title.innerText = `${date}의 일정`;
  popup.style.display = "block"; //block는 보이게하는것!

  // 할 일 목록 초기화
  todoList.innerHTML = ""; //매번 새로 그림

  // 서버에서 할 일 목록 불러오기
  fetch(`/api/todos?date=${date}`) //서버에서 date에 해당하는 배열 가져오기.
    .then(res => res.json())
    .then(data => {
      data.forEach(todo => {
        const li = document.createElement("li"); //li는 한개의 할일 항목
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox"; //checkbox 생성
        checkbox.checked = todo.is_done == "true"; //is_done값이 true면 체크됨!
        
        //색상 스타일
        checkbox.style.marginRight="8px";
        
        if (checkbox.checked) checkbox.style.accentColor = "#8BC34A"; //체크되면 초록색으로 표시 
        
        //체크 변경시 서버에 상태 없뎃해줘야함. patch요청
        checkbox.addEventListener("change",()=> {
	        updateTodoStatus(todo.id, checkbox.checked);
	        checkbox.style.accentColor = checkbox.checked ? "#8BC34A" : "white";
	       });
	       
	      li.appendChild(checkbox); //요소들 화면에 추가하기
	      li.append(todo.content);
	      todoList.appendChild(li);
      });
    });

  // 추가 버튼에 이벤트 연결
  const addBtn = document.getElementById("addTodoBtn");
  addBtn.onclick = () => addTodo(date);
}

//할일 추가하는 함수
function addTodo(date) {
  const input = document.getElementById("newTodo"); //입력창에서 내용 가져오기
  const content = input.value.trim();
  if (!content) return; //공백이면 추가안함

  fetch('/api/todos', { //서버에 할일 등록
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ date, content })
  })
  .then(() => {
    input.value = "";
    showPopup(date); // 다시 로딩(새 항목 반영됨)
  });
}

//팝업 닫기
function closePopup() {
  document.getElementById("popup").style.display = "none";
}

//서버에 체크상태 업뎃 요청 보내기
function updateTodoStatus(todoId, isDone) { 
	fetch(`/api/todos/${todoId}`, {
		method: "PATCH",
		headers: { "Content-Type" : "application/json" },
		body: JSON.stringify({is_done:isDone })
	});
}