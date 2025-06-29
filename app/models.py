from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, description="Task title")
    description: Optional[str] = Field(
        default=None, 
        max_length=1000, 
        description="Detailed task description"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status of the task"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Priority level of the task"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When the task was created"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="When the task was last updated"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline"
    )
    assigned_to: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Person assigned to the task"
    )