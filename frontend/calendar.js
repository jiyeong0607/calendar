//새로운let currentYear = new Date().getFullYear(); //현재 연도와 월 가져와 
let currentMonth = 4; // 0-indexed (4 = May)

function renderCalendar(year, month) {
  const monthTitle = document.getElementById("monthTitle"); //월 제목 넣기
  const calendarBody = document.getElementById("calendarBody"); //날짜칸 여기에 넣기 

  const firstDay = new Date(year, month, 1).getDay(); //이번달 1일이 무슨 요일?
  const lastDate = new Date(year, month + 1, 0).getDate(); //이번달이 며칠까지 있지? 

  monthTitle.innerText = `${year}년 ${month + 1}월`;
  calendarBody.innerHTML = "";

  let row = document.createElement("tr"); //달력 한 줄 만드는 tr.

  // 1일이 수욜이면 앞에 칸 3개 빈칸으로하기.
  for (let i = 0; i < firstDay; i++) {
    row.appendChild(document.createElement("td"));
  }
	//1일부터 마지막날짜까지 반복하며 td 만들기(날짜 숫자 표시) 
  for (let date = 1; date <= lastDate; date++) {
    const cell = document.createElement("td");
    cell.innerText = date;
    cell.onclick = () => showPopup(`${year}-${month+1}-${date}`); //날짜 클릭하면 팝업띄움
    row.appendChild(cell); //현재 날짜 셀을 한 주에 넣음 

    if ((firstDay + date) % 7 === 0 || date === lastDate) { //한주 끝났거나 막날까지 다 돌았으면 지금 만든 줄을 calendarBody에 추가! 
      calendarBody.appendChild(row);
      row = document.createElement("tr"); //새로운 줄 시작.
    }
  }
}

function prevMonth() { //이전달로 이동
  if (currentMonth <=2) return;
    currentMonth--;
    renderCalendar(currentYear,currentMonth); 
  }

function nextMonth() {
	if (currentMonth >=5) return;
	currentMonth++;
	renderCalendar(currentYear,currentMonth);
}

// 초기 렌더링 (페이지 처음 로딩될때 달력 한번 그리기)
renderCalendar(currentYear, currentMonth);
