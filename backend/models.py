from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # CSV에서 사용하므로 필요

    todos = db.relationship('ToDo', backref='user', lazy=True)


class ToDo(db.Model):
    __tablename__ = 'to_do'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)  # [일정] 제목 형식 저장
    due_date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    is_done = db.Column(db.Boolean, default=False)
    
    user_id = db.Column(db.String(20), db.ForeignKey('user.student_id'), nullable=False)
