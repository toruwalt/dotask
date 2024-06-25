from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from dotask import app, db, enum, UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    tasks = relationship('Task', back_populates='user')

class TaskStatus(enum.Enum):
    In_Progress = "In_Progress"
    Completed = "Completed"
    Cancelled = "Cancelled"

class TaskTag(enum.Enum):
    Work = "Work"
    Personal = "Personal"
    Errands = "Errands"
    Home = "Home"


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(Enum(TaskStatus))
    tag = db.Column(Enum(TaskTag))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='tasks')


with app.app_context():
    db.create_all()