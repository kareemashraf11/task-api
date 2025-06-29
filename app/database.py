# app/database.py
"""
Database configuration module.
Handles SQLite connection and session management for SQLModel.
"""

from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

# SQLite database URL - creates a file named 'tasks.db' in the project root
DATABASE_URL = "sqlite:///./tasks.db"

# Create the database engine
# connect_args={"check_same_thread": False} is needed for SQLite to work with FastAPI
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production - this logs all SQL queries
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """
    Create all database tables defined by SQLModel models.
    This function should be called when the application starts.
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.
    This ensures that sessions are properly closed after each request.
    
    Yields:
        Session: A SQLModel database session
    """
    with Session(engine) as session:
        yield session