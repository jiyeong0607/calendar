from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # CORS 허용 (프론트랑 백 연결될 수 있게)

# 파일 경로들 미리 지정
basedir = os.path.abspath(os.path.dirname(__file__))
CSV_USER_PATH = os.path.join(basedir, 'db', 'user.csv')
CSV_TODO_PATH = os.path.join(basedir, 'db', 'todolist.csv')
CSV_STATUS_PATH = os.path.join(basedir, 'db', 'task_status.csv')

# 로그인 기능
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify(success=False, error="잘못된 요청"), 400

    student_id = str(data.get("studentId", "")).strip()
    password = str(data.get("password", "")).strip()

    try:
        df = pd.read_csv(CSV_USER_PATH, dtype=str)
    except Exception:
        return jsonify(success=False, error="파일 읽기 실패")

    user = df[(df['student_id'] == student_id) & (df['password'] == password)]
    return jsonify(success=not user.empty)

# 사용자 일정 추가
@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    print("일정 추가 호출됨")
    data = request.get_json()
    student_id = str(data.get("studentId"))
    date = str(data.get("date"))
    title = str(data.get("title"))

    # 사용자 확인
    try:
        users_df = pd.read_csv(CSV_USER_PATH, dtype=str)
    except Exception as e:
        return jsonify(success=False, error="사용자 파일 읽기 실패")

    if users_df[users_df['student_id'] == student_id].empty:
        return jsonify(success=False, error="사용자 없음"), 404

    # todo 불러오기
    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except FileNotFoundError:
        todos_df = pd.DataFrame(columns=['id', 'user_id', 'title', 'due_date'])
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    new_id = 1 if todos_df.empty else todos_df['id'].astype(int).max() + 1

    new_todo = pd.DataFrame([{
        'id': str(new_id),
        'user_id': student_id,
        'title': title,
        'due_date': date
    }])

    todos_df = pd.concat([todos_df, new_todo], ignore_index=True)
    try:
        todos_df.to_csv(CSV_TODO_PATH, index=False)
    except Exception:
        return jsonify(success=False, error="일정 저장 실패")

    return jsonify(success=True)

# 특정 날짜의 일정들 불러오기
@app.route('/api/todos', methods=['GET'])
def get_todos():
    date = request.args.get("date")
    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except Exception:
        return jsonify([])

    filtered = todos_df[todos_df['due_date'] == date]

    result = []
    for _, row in filtered.iterrows():
        result.append({
            "id": int(row['id']),
            "content": row['title']
        })

    return jsonify(result)

# 일정 추가 (공용 or 미로그인 용도 등)
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except FileNotFoundError:
        todos_df = pd.DataFrame(columns=['id', 'user_id', 'title', 'due_date'])
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    new_id = 1 if todos_df.empty else todos_df['id'].astype(int).max() + 1

    new_todo = pd.DataFrame([{
        'id': str(new_id),
        'user_id': "shared",  # 사용자 구분 없이 저장됨
        'title': data.get("content", ""),
        'due_date': data.get("date", "")
    }])

    todos_df = pd.concat([todos_df, new_todo], ignore_index=True)
    todos_df.to_csv(CSV_TODO_PATH, index=False)

    return jsonify(success=True)

# 일정 삭제
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    todos_df = todos_df[todos_df['id'].astype(int) != todo_id]
    todos_df.to_csv(CSV_TODO_PATH, index=False)
    return jsonify(success=True)

# 체크 여부 조회
@app.route('/api/status/<student_id>', methods=['GET'])
def get_status(student_id):
    try:
        df = pd.read_csv(CSV_STATUS_PATH, dtype=str)
    except FileNotFoundError:
        return jsonify([])

    filtered = df[df['student_id'] == student_id]
    return jsonify([
        {"todo_id": int(row['todo_id']), "is_done": row['is_done'].lower() == 'true'}
        for _, row in filtered.iterrows()
    ])

# 체크 여부 업데이트
@app.route('/api/status', methods=['POST'])
def update_status():
    data = request.get_json()
    student_id = str(data.get("student_id"))
    todo_id = str(data.get("todo_id"))
    is_done = str(data.get("is_done"))

    try:
        df = pd.read_csv(CSV_STATUS_PATH, dtype=str)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['student_id', 'todo_id', 'is_done'])

    match = (df['student_id'] == student_id) & (df['todo_id'] == todo_id)
    if match.any():
        df.loc[match, 'is_done'] = is_done
    else:
        new_row = pd.DataFrame([{
            'student_id': student_id,
            'todo_id': todo_id,
            'is_done': is_done
        }])
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(CSV_STATUS_PATH, index=False)
    return jsonify(success=True)

# 기본 페이지(login.html) 서비스
@app.route('/')
def serve_login():
    return send_from_directory('frontend', 'login.html')

# 정적 파일 서비스 (html, js 등)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # 외부에서 접속 가능하게 0.0.0.0으로 설정

