from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.LOW
    status: TaskStatus = TaskStatus.NEW
    result: Optional[str] = None
    err_info: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[str] = None
    err_info: Optional[str] = None


class TaskInDB(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskOutDB(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: TaskPriority
    status: TaskStatus
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    result: Optional[str] = None
    err_info: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)