"""Њ®¤Ґ«Ё Ў §л ¤ ­­ле."""

import datetime

import enum



from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum

from sqlalchemy.orm import relationship



from app.database import Base





class TaskStatus(str, enum.Enum):

    TODO = "todo"

    IN_PROGRESS = "in_progress"

    DONE = "done"





class TaskPriority(str, enum.Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"





class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    projects = relationship("Project", back_populates="owner")

    tasks = relationship("Task", back_populates="assignee")





class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(String, default="")

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="projects")

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")





class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, default="")

    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)

    estimated_hours = Column(Integer, default=0)

    deadline = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")

    assignee = relationship("User", back_populates="tasks")

