from sqlalchemy import Enum, event
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from dotask import app, db, enum, UserMixin

user_task = db.Table(
    "user_task",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("task_id", db.Integer, db.ForeignKey("task.id"), primary_key=True),
)

user_notification = db.Table(
    "user_notification",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("notification_id", db.Integer, db.ForeignKey("notification.id"), primary_key=True),
)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    assigned_tasks = relationship('Task', secondary=user_task, backref='assigned_to')
    notes = relationship('Notification', secondary=user_notification, backref='notes')

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
    users = relationship('User', secondary=user_task, 
    backref='tasks')
    

class Notification(db.Model):
    __tablename__ = "notification"
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(100), nullable=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)
    task_title = db.Column(db.String(100), nullable=False)
    users_to_notify = relationship('User', secondary=user_notification, backref='notices')

with app.app_context():
    db.create_all()