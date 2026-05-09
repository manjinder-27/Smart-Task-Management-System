from flask import Flask,render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from flask_socketio import SocketIO, emit,join_room

flask_app = Flask(__name__)

flask_app.config['SECRET_KEY'] = 'unsecure-key-for-testing'

flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tester:mypasswd@localhost/testdb'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_instance = SQLAlchemy(flask_app)

api_instance = Api(flask_app)

socketio = SocketIO(flask_app, cors_allowed_origins="*")

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        join_room(f"user_{current_user.id}")

@flask_app.route('/')
def home_page():
    return render_template('home.html')

@flask_app.route('/register')
def register_page():
    return render_template('register.html')

@flask_app.route('/login')
def login_page():
    return render_template('login.html')

@flask_app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

@flask_app.route('/add-task')
@login_required
def add_task_page():
    return render_template('add_task.html')

@flask_app.route('/edit-task/<int:task_id>')
@login_required
def edit_task_page(task_id):
    # task_id passed to the template so JS knows which task to edit
    return render_template('edit_task.html', task_id=task_id)