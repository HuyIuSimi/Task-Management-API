# Task Management API

> A simple REST API for managing tasks, built with FastAPI and PostgreSQL.

## Features

* Create, read, update, and delete tasks
* Filter tasks by status (pending/completed)
* Paginated task listing
* Automatic API documentation

## Tech Stack

* FastAPI - Web framework
* PostgreSQL - Database
* SQLAlchemy - ORM
* Pydantic - Data validation

## Getting Started

### Database Setup

1. Log into PostgreSQL:
```bash
psql -U postgres
```

2. Run these commands:
```sql
CREATE DATABASE taskdb;
CREATE USER taskuser WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
\c taskdb
GRANT ALL ON SCHEMA public TO taskuser;
\q
```

### Project Setup

1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/yourusername/task-api.git
cd task-api
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
```

4. Create `.env` file:
```plaintext
DATABASE_URL=postgresql://taskuser:password123@localhost/taskdb
```

5. Run the API:
```bash
uvicorn main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

## API Usage

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

### Endpoints

#### Create Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "My First Task",
           "description": "Testing the API!"
         }'
```

#### List Tasks
```bash
# Get all tasks
curl "http://localhost:8000/tasks/"

# Filter by status
curl "http://localhost:8000/tasks/?status=pending"

# Pagination
curl "http://localhost:8000/tasks/?page=2&items_per_page=5"
```

#### Update Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
           "status": "completed"
         }'
```

#### Delete Task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Design Decisions

### Why FastAPI?
* Automatic API documentation
* Built-in data validation
* Developer-friendly

### Status System
* Simple two-state system:
  * `pending` - Task not completed
  * `completed` - Task finished
* Clear and straightforward

## Troubleshooting

### Database Connection Issues
1. Verify PostgreSQL is running
2. Check database credentials
3. Ensure database and user exist
4. Verify permissions

### API Won't Start
1. Check if port 8001 is available
2. Ensure virtual environment is activated
3. Verify all packages are installed

### Common Errors
* "Port already in use": Try different port
* "Package not found": Reinstall requirements
* "Permission denied": Check database permissions

## Future Improvements

### Features
- [ ] User authentication
- [ ] Task priorities
- [ ] Due dates
- [ ] Categories/tags
- [ ] Task search
- [ ] Batch operations

### Technical
- [ ] Caching layer
- [ ] Rate limiting
- [ ] Better error logging
- [ ] Database migrations

### Database
- [ ] Performance indexes
- [ ] Data archiving
