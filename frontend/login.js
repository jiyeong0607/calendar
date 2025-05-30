function login() {
  const studentId = document.getElementById("studentId").value;
  const password = document.getElementById("password").value;

  fetch('/api/login', {
    method: 'POST', //<!--서버에 post 방식으로 학번,비번 보냄-->
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ studentId, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) { //data.success 가 true일때-->
      window.location.href = 'calendar.html';
    } else {
      document.getElementById("loginResult").innerText = "로그인 실패: 정보를 다시 확인하세요.";
    }
  })
  .catch(() => { //서버 죽었거나 에러날때
    document.getElementById("loginResult").innerText = "서버 오류 발생";
  });
}
