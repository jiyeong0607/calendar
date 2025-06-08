function login() {
  const studentId = document.getElementById("studentId").value; //학번가져와서 넣기
  const password = document.getElementById("password").value;//비밀번호 가져와서 넣기

  fetch('/api/login', { //서버 요청
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ studentId, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) { 
      // 로그인 성공시 studentId를 localStorage에 저장
      localStorage.setItem("studentId", studentId);

      // 캘린더 페이지로 이동
      window.location.href = 'calendar.html';
    } else { //로그인 실패시
      document.getElementById("loginResult").innerText = "로그인 실패: 정보를 다시 확인하세요.";
    }
  })
  .catch(() => { //서버 오류 발생시
    document.getElementById("loginResult").innerText = "서버 오류 발생";
  });
}

