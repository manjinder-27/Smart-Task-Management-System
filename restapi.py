from flask import request
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,Task
from app import api_instance as api
from app import db_instance as db
from app import socketio
import pandas as pd
import numpy as np

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {"message": "User already exists"}, 400

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()

        if user and check_password_hash(user.password, data.get('password')):
            login_user(user)
            return {"message": "Login successful"}, 200
        
        return {"message": "Invalid credentials"}, 401

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200


class TaskList(Resource):
    @login_required
    def get(self):
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
        
        return [{
            "id": t.id,
            "title": t.title,
            "desc": t.desc,
            "priority": t.priority,
            "status": t.status,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for t in tasks], 200

    @login_required
    def post(self):
        data = request.get_json()
        
        if not data.get('title'):
            return {"message": "Title is required"}, 400

        new_task = Task(
            title=data['title'],
            desc=data.get('desc', ''),
            priority=data.get('priority', 'LOW'),
            status='Pending',
            user_id=current_user.id
        )
        
        db.session.add(new_task)
        db.session.commit()
        socketio.emit('task_updated', {'data': "Updated"}, to=f"user_{current_user.id}")
        return {"message": "Task created successfully", "task_id": new_task.id}, 201


class TaskResource(Resource):
    @login_required
    def put(self, task_id):
        data = request.get_json()
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

        task.title = data.get('title', task.title)
        task.desc = data.get('desc', task.desc)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)

        db.session.commit()
        socketio.emit('task_updated', {'data': "Updated"}, to=f"user_{current_user.id}")
        return {"message": "Task updated successfully"}, 200

    @login_required
    def delete(self, task_id):
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
        
        db.session.delete(task)
        db.session.commit()
        socketio.emit('task_updated', {'data': "Updated"}, to=f"user_{current_user.id}")
        return {"message": "Task deleted successfully"}, 200


class Analytics(Resource):
    @login_required
    def get(self):
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        if not tasks:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "pending_tasks": 0,
                "completion_percentage": 0.0
            }, 200

        task_data = [
            {"status": t.status} for t in tasks
        ]
        
        df = pd.DataFrame(task_data)
        total_tasks = len(df)
        completed_tasks = int(np.sum(df['status'].values == 'Completed'))
        pending_tasks = total_tasks - completed_tasks
        completion_percentage = (completed_tasks / total_tasks) * 100
        completion_percentage = float(np.round(completion_percentage, 2))
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_percentage": completion_percentage
        }, 200