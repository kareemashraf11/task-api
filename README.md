# Task Management API

A modern, production-ready RESTful API built with FastAPI for managing tasks. This project demonstrates best practices in Python web development, including proper project structure, data validation, database integration, and comprehensive API documentation.

## Understanding the Architecture

This application follows a layered architecture pattern that separates concerns and makes the code maintainable and testable. The main components work together as follows:

The **database layer** (using SQLModel) handles all data persistence. SQLModel is particularly powerful because it combines SQLAlchemy's ORM capabilities with Pydantic's data validation, giving us type safety from the database all the way to the API responses.

The **schema layer** (using Pydantic) provides data validation and serialization. By separating our API schemas from our database models, we maintain flexibility in how we expose data to clients without being tied to our database structure.

The **API layer** (using FastAPI) handles HTTP requests and responses. FastAPI's dependency injection system makes it easy to manage database sessions and other resources cleanly.

## Installation and Setup

First, ensure you have Python 3.9 or higher installed on your system. You can verify this by running `python --version` in your terminal.

Clone this repository and navigate to the project directory:

```bash
git clone <repository-url>
cd task-api
```

Now install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the development server, simply run:

```bash
python app/main.py
```

The application will start on `http://localhost:8000`. You'll see output indicating that the database tables have been created and the server is running.

Once your server is running, visit:

- **Swagger UI**: http://localhost:8000/docs - This provides an interactive interface where you can test all API endpoints

## Understanding the API Endpoints

The API follows RESTful principles, which means it uses standard HTTP methods to perform operations on resources. Here's what each endpoint does and why:

### Root and Health Endpoints

The root endpoint (`GET /`) provides a welcome message and lists all available endpoints. This is helpful for developers discovering your API for the first time.

The health check endpoint (`GET /health`) is crucial for production deployments. Load balancers and monitoring systems use this endpoint to verify that your application is running correctly.

### Task Management Endpoints

The core of our API revolves around the `/api/v1/tasks` endpoints. Let me explain the design decisions behind each:

**Creating Tasks** (`POST /api/v1/tasks`): When you create a task, the API validates the input data, ensures the title isn't empty, checks that any due date is in the future, and then saves the task to the database. The response includes the generated ID and timestamps.

**Listing Tasks** (`GET /api/v1/tasks`): This endpoint supports pagination through `skip` and `limit` parameters. Pagination is essential for performance when dealing with large datasets. You can also filter by status and priority.

**Retrieving a Single Task** (`GET /api/v1/tasks/{task_id}`): Fetches complete details for a specific task. Returns a 404 error if the task doesn't exist.

**Updating Tasks** (`PUT /api/v1/tasks/{task_id}`): Supports partial updates, meaning you only need to send the fields you want to change. The API automatically updates the `updated_at` timestamp.

**Deleting Tasks** (`DELETE /api/v1/tasks/{task_id}`): Removes a task from the database. Following REST conventions, this returns a 204 No Content status on success.

### Filtering Endpoints

The specialized filtering endpoints (`GET /api/v1/tasks/status/{status}` and `GET /api/v1/tasks/priority/{priority}`) provide convenient ways to retrieve tasks by specific criteria. While you could achieve the same result using query parameters on the main list endpoint, these dedicated endpoints make common operations more intuitive.

## Testing the API

### Using the Interactive Documentation

The easiest way to test the API is through the Swagger UI at http://localhost:8000/docs. Click on any endpoint to expand it, then click "Try it out" to send test requests. This is incredibly helpful during development.

### Using cURL

Here are some example cURL commands to interact with the API:

Creating a task:
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Task 1",
       "description": "Finish API docs",
       "priority": "high",
       "due_date": "2024-12-31T23:59:59"
     }'
```

Listing all tasks with pagination:
```bash
curl "http://localhost:8000/api/v1/tasks?skip=0&limit=10"
```

Updating a task (replace `{task_id}` with an actual ID):
```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "in_progress",
       "assigned_to": "John Doe"
     }'
```

### Using HTTPie

HTTPie provides a more user-friendly command-line interface. If you installed it from the requirements file:

```bash
# Create a task
http POST localhost:8000/api/v1/tasks \
    title="Learn FastAPI" \
    priority="high"

# Fetch tasks
http GET localhost:8000/api/v1/tasks

# Update a task
http PUT localhost:8000/api/v1/tasks/1 \
    status="completed"
```

## Data Validation

The application implements comprehensive validation to ensure data integrity:

**Title Validation**: Titles are required and must contain actual content (not just whitespace). They're automatically trimmed of leading and trailing spaces.

**Due Date Validation**: Any provided due date must be in the future. This prevents creating tasks that are already overdue.

**Enum Validation**: Status and priority fields only accept predefined values, preventing invalid data from entering the system.

**Length Constraints**: Fields like title (200 chars), description (1000 chars), and assigned_to (100 chars) have maximum lengths to ensure database efficiency.

## Database Schema

The application uses SQLite for simplicity, but the SQLModel ORM makes it easy to switch to PostgreSQL or MySQL in production. The database file (`tasks.db`) is created automatically when you first run the application.

The Task table includes several thoughtful design decisions:

- The `created_at` field uses `default_factory=datetime.now` to automatically set the creation time
- The `updated_at` field is optional and only set when a task is modified
- Status and priority use enums to ensure data consistency
- All string fields have appropriate length constraints

## Project Structure Explained

The project follows a modular structure that separates concerns:

```
app/
├── main.py           # Application entry point and configuration
├── database.py       # Database connection and session management
├── models.py         # SQLModel database models
├── schemas.py        # Pydantic validation schemas
└── api/
    └── tasks.py      # Task-related API endpoints
```

This structure makes it easy to add new features. For example, if you wanted to add user authentication, you would create new files like `app/models/user.py`, `app/schemas/auth.py`, and `app/api/auth.py`.

