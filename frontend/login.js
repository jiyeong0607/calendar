function login() {
  const studentId = document.getElementById("studentId").value;
  const password = document.getElementById("password").value;

  fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ studentId, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // studentId를 localStorage에 저장
      localStorage.setItem("studentId", studentId);

      // 캘린더 페이지로 이동
      window.location.href = 'calendar.html';
    } else {
      document.getElementById("loginResult").innerText = "로그인 실패: 정보를 다시 확인하세요.";
    }
  })
  .catch(() => {
    document.getElementById("loginResult").innerText = "서버 오류 발생";
  });
}

