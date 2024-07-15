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

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    #tasks = relationship('Task', back_populates='user')
    assigned_tasks = relationship('Task', secondary=user_task, backref='assigned_to')

class Notifications(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
    #users = relationship('User', back_populates='tasks')
    users = relationship('User', secondary=user_task, backref='tasks')


def create_notification(mapper, connection, target):
    session = Session.object_session(target)
    if isinstance(target, Task):
        notification_message = f"Task '{target.title}' was added/updated/removed."
    else:
        notification_message = f"Unknown change detected."

    for user in target.users:
        notification = Notifications(
            notification=notification_message,
            user_id=user.id
        )
        session.add(notification)
    session.commit()
    return notification_message

event.listen(Task, 'after_insert', create_notification)
event.listen(Task, 'after_update', create_notification)
event.listen(Task, 'after_delete', create_notification)



with app.app_context():
    db.create_all()