import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from app.database import Base


class TaskPriority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(enum.Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(
        Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    status = Column(
        Enum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now,
        onupdate=datetime.now(timezone.utc))
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    result = Column(Text, nullable=True)
    err_info = Column(Text, nullable=True)
