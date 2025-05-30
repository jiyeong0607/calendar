from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

from models import db, User, ToDo

app = Flask(__name__)

# SQLite DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# CSV 경로 설정
CSV_USER_PATH = '/app/db/user.csv'
CSV_TODO_PATH = '/app/db/todolist.csv'

# 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    student_id = str(data.get("studentId"))
    password = str(data.get("password"))

    try:
        df = pd.read_csv(CSV_USER_PATH, dtype=str)
    except Exception as e:
        return jsonify(success=False, error="파일 읽기 실패")

    user = df[(df['student_id'] == student_id) & (df['password'] == password)]
    if not user.empty:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

# 일정 등록 → 자동 ToDo 추가
@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    student_id = str(data.get("studentId"))
    date = str(data.get("date"))
    title = str(data.get("title"))

    user = User.query.filter_by(student_id=student_id).first()
    if not user:
        return jsonify(success=False, error="사용자 없음"), 404

    todo = ToDo(user_id=user.student_id, title=f"[일정] {title}", due_date=date)
    db.session.add(todo)
    db.session.commit()

    return jsonify(success=True)

# ✅ 할일 목록 불러오기
@app.route('/api/todos', methods=['GET'])
def get_todos():
    date = request.args.get("date")
    todos = ToDo.query.filter_by(due_date=date).all()
    result = []
    for t in todos:
        result.append({
            "id": t.id,
            "content": t.title,
            "is_done": str(t.is_done).lower()
        })
    return jsonify(result)

# ✅ 할일 추가
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = ToDo(
        title=data["content"],
        due_date=data["date"],
        is_done=False,
        user_id="temp_user"  # 임시 ID → 실제로는 로그인 사용자 ID로 대체
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(success=True)

# ✅ 할일 완료 상태 변경
@app.route('/api/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    data = request.get_json()
    todo = ToDo.query.get(todo_id)
    if not todo:
        return jsonify(success=False), 404
    todo.is_done = data["is_done"]
    db.session.commit()
    return jsonify(success=True)

# 테이블 자동 생성
@app.before_first_request
def create_tables():
    db.create_all()

# 서버 시작
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
