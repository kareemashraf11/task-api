# app/main.py
"""
Main FastAPI application module.
This is the entry point of our API - it ties everything together.
"""

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.api import tasks

# Application metadata - this appears in the auto-generated documentation
APP_TITLE = "Task Management API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = """
## Task Management API

A RESTful API for managing tasks with the following features:

### Features
- **Full CRUD Operations**: Create, Read, Update, and Delete tasks
- **Status Management**: Track tasks through different status stages
- **Priority Levels**: Organize tasks by priority
- **Filtering**: Filter tasks by status and priority
- **Pagination**: Efficient handling of large task lists
- **Data Validation**: Comprehensive input validation
- **Auto-documentation**: Interactive API documentation

### Technical Stack
- **FastAPI**: Modern, fast web framework
- **SQLModel**: SQL databases with Python type hints
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for persistence
"""

# Define startup and shutdown events using lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle events.
    This runs code at startup and shutdown.
    """
    # Startup: Create database tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    
    # This yield separates startup from shutdown code
    yield
    
    # Shutdown: Cleanup code would go here
    print("Application shutting down...")

# Create the FastAPI application instance
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan,
    # Custom documentation URLs
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc UI
    openapi_url="/openapi.json"  # OpenAPI schema
)

# Add CORS middleware - allows the API to be called from web browsers
# In production, you'd want to restrict origins to your specific frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the task router - this adds all task endpoints to our app
app.include_router(tasks.router, prefix="/api/v1")

@app.get("/", tags=["root"])
def read_root():
    """
    Root endpoint - provides API information and available endpoints.
    
    This is helpful for developers discovering your API.
    """
    return {
        "message": "Welcome to Task Management API",
        "version": APP_VERSION,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json"
        },
        "endpoints": {
            "tasks": "/api/v1/tasks",
            "health": "/health"
        }
    }

@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint.
    
    This is used by monitoring systems and load balancers to verify
    that the application is running correctly.
    """
    return {
        "status": "healthy",
        "service": APP_TITLE,
        "version": APP_VERSION
    }

# This allows the app to be run directly with: python main.py
if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # reload=True enables hot reloading during development
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )