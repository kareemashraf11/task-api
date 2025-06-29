# app/api/tasks.py
"""
Task API endpoints.
This module contains all the RESTful endpoints for task management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.models import Task, TaskStatus, TaskPriority
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

# Create a router instance - this groups related endpoints together
router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
) -> Task:
    """
    Create a new task.
    
    This endpoint:
    1. Receives task data validated by TaskCreate schema
    2. Creates a new Task instance
    3. Saves it to the database
    4. Returns the created task with generated ID and timestamps
    """
    # Create a new Task instance from the validated data
    db_task = Task(**task.model_dump())
    
    # Add to session and commit to database
    session.add(db_task)
    session.commit()
    session.refresh(db_task)  # Refresh to get the generated ID
    
    return db_task

@router.get("/", response_model=TaskListResponse)
def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    session: Session = Depends(get_session)
) -> dict:
    """
    List all tasks with optional filtering and pagination.
    
    Features:
    - Pagination with skip/limit parameters
    - Optional filtering by status and priority
    - Returns total count for pagination UI
    """
    # Build the base query
    query = select(Task)
    
    # Apply filters if provided
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    
    # Get total count before pagination
    total_query = select(Task)
    if status:
        total_query = total_query.where(Task.status == status)
    if priority:
        total_query = total_query.where(Task.priority == priority)
    total = len(session.exec(total_query).all())
    
    # Apply pagination
    tasks = session.exec(query.offset(skip).limit(limit)).all()
    
    return {
        "tasks": tasks,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> Task:
    """
    Retrieve a specific task by ID.
    
    Raises 404 if task not found.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
) -> Task:
    """
    Update an existing task.
    
    This endpoint:
    1. Finds the task by ID
    2. Updates only the provided fields (partial update)
    3. Sets the updated_at timestamp
    4. Returns the updated task
    """
    # Find the task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # Update the timestamp
    task.updated_at = datetime.now()
    
    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a task.
    
    Returns 204 No Content on success.
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    session.delete(task)
    session.commit()

@router.get("/status/{status}", response_model=List[TaskResponse])
def get_tasks_by_status(
    status: TaskStatus,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
) -> List[Task]:
    """
    Get tasks filtered by status.
    
    This is a convenience endpoint that makes it easy to get all tasks
    with a specific status.
    """
    statement = select(Task).where(Task.status == status).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks

@router.get("/priority/{priority}", response_model=List[TaskResponse])
def get_tasks_by_priority(
    priority: TaskPriority,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
) -> List[Task]:
    """
    Get tasks filtered by priority.
    
    Similar to the status filter, but for priority levels.
    """
    statement = select(Task).where(Task.priority == priority).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks