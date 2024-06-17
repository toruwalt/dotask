#!/usr/binpython3
"""
from sqlalchemy import create_engine, DeclarativeBase, text, Column, Integer, String, Boolean, ForeignKey, Date, Enum

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("mysql://rootd@localhost:3306/doTask", echo=True)


class Base(DeclarativeBase):
    pass

class User(db):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    
    username: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[str]
    last_name: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.first_name + " " + self.last_name!r}, email={self.email!r})"
    

class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    due_date: Mapped[Date]
    status: TaskStatus = mapped_column(Enum(TaskStatus))
    user_id = mapped_column(ForeignKey("user_account.id"))
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, description={self.description!r}, due_date={self.due_date!r},status={self.status!r})"

"""