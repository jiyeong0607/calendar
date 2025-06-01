from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# 절대경로로 CSV 파일 위치 지정
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_USER_PATH = os.path.join(basedir, 'db', 'user.csv')
CSV_TODO_PATH = os.path.join(basedir, 'db', 'todolist.csv')

# 로그인 API (CSV에서 확인)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    student_id = str(data.get("studentId"))
    password = str(data.get("password"))

    try:
        df = pd.read_csv(CSV_USER_PATH, dtype=str)
    except Exception:
        return jsonify(success=False, error="파일 읽기 실패")

    user = df[(df['student_id'] == student_id) & (df['password'] == password)]
    if not user.empty:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

# 일정 등록 → 자동 ToDo 추가 (CSV에 저장)
@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    student_id = str(data.get("studentId"))
    date = str(data.get("date"))
    title = str(data.get("title"))

    try:
        users_df = pd.read_csv(CSV_USER_PATH, dtype=str)
    except Exception:
        return jsonify(success=False, error="사용자 파일 읽기 실패")

    if users_df[users_df['student_id'] == student_id].empty:
        return jsonify(success=False, error="사용자 없음"), 404

    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except FileNotFoundError:
        todos_df = pd.DataFrame(columns=['id', 'user_id', 'title', 'due_date', 'is_done'])
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    if todos_df.empty:
        new_id = 1
    else:
        new_id = todos_df['id'].astype(int).max() + 1

    new_todo = {
        'id': str(new_id),
        'user_id': student_id,
        'title': f"[일정] {title}",
        'due_date': date,
        'is_done': 'False'
    }

    todos_df = todos_df.append(new_todo, ignore_index=True)
    todos_df.to_csv(CSV_TODO_PATH, index=False)

    return jsonify(success=True)

# 할일 목록 불러오기 (특정 날짜)
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
            "content": row['title'],
            "is_done": row['is_done'].lower() == 'true'
        })

    return jsonify(result)

# 할일 추가 (CSV에 저장)
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except FileNotFoundError:
        todos_df = pd.DataFrame(columns=['id', 'user_id', 'title', 'due_date', 'is_done'])
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    if todos_df.empty:
        new_id = 1
    else:
        new_id = todos_df['id'].astype(int).max() + 1

    new_todo = {
        'id': str(new_id),
        'user_id': "temp_user",  # TODO: 로그인 사용자 ID로 교체 필요
        'title': data.get("content", ""),
        'due_date': data.get("date", ""),
        'is_done': 'False'
    }

    todos_df = todos_df.append(new_todo, ignore_index=True)
    todos_df.to_csv(CSV_TODO_PATH, index=False)

    return jsonify(success=True)

# 할일 완료 상태 변경 (CSV 수정)
@app.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    data = request.get_json()
    try:
        todos_df = pd.read_csv(CSV_TODO_PATH, dtype=str)
    except Exception:
        return jsonify(success=False, error="ToDo 파일 읽기 실패")

    index = todos_df.index[todos_df['id'].astype(int) == todo_id]
    if index.empty:
        return jsonify(success=False), 404

    is_done = data.get("is_done")
    if isinstance(is_done, bool):
        is_done_str = 'True' if is_done else 'False'
    elif isinstance(is_done, str):
        is_done_str = is_done.capitalize()
    else:
        is_done_str = 'False'

    todos_df.at[index[0], 'is_done'] = is_done_str
    todos_df.to_csv(CSV_TODO_PATH, index=False)

    return jsonify(success=True)

# 정적 파일 제공 (frontend 디렉토리)
@app.route('/')
def serve_login():
    return send_from_directory('frontend', 'login.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
