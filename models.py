from app import db_instance as db
from app import flask_app
from datetime import datetime
from flask_login import UserMixin
from flask_login import LoginManager

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    priority = db.Column(db.String(8),nullable=False,default="LOW")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return f'<Task {self.title}>'


login_manager = LoginManager()
login_manager.init_app(flask_app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with flask_app.app_context():
    db.create_all()