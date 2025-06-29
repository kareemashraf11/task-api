# app/schemas.py
"""
Pydantic schemas for request/response validation.
These models handle data validation, serialization, and API documentation.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from app.models import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    """
    Base schema containing common task fields.
    This follows the DRY principle - we define common fields once.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(TaskStatus.PENDING, description="Task status")
    priority: Optional[TaskPriority] = Field(TaskPriority.MEDIUM, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Assignee name")
    
    # Custom validator for title
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """
        Validate title:
        - Remove leading/trailing whitespace
        - Ensure it's not empty after stripping
        """
        if v:
            v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty or whitespace only")
        return v
    
    # Custom validator for due_date
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """
        Validate due date:
        - Must be in the future if provided
        """
        if v and v < datetime.now():
            raise ValueError("Due date must be in the future")
        return v

class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    Inherits all fields from TaskBase.
    Status and priority will use defaults if not provided.
    """
    pass

class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    All fields are optional to allow partial updates.
    """
    model_config = ConfigDict(validate_assignment=True)
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[str] = Field(None, max_length=100)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace only")
        return v
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        """Validate due date if provided"""
        if v and v < datetime.now():
            raise ValueError("Due date must be in the future")
        return v

class TaskResponse(BaseModel):
    """
    Schema for task responses.
    This is what the API returns to clients.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

class TaskListResponse(BaseModel):
    """
    Schema for paginated task list responses.
    Includes metadata about the result set.
    """
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int