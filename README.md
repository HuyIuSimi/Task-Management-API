# Task Management API

A fast, simple, and powerful REST API for managing tasks built with FastAPI and PostgreSQL.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Features

- ✨ Create, read, update, and delete tasks
- 📋 List all tasks with pagination
- ✅ Mark tasks as completed
- 📝 Simple status system (pending/completed)
- 📚 Auto-generated API documentation

## Why FastAPI?

- 🚀 High performance
- 📖 Automatic API documentation
- 🛡️ Built-in data validation
- 🔧 Easy to learn and use

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL

### 1. Database Setup

```sql
-- Log into PostgreSQL
psql -U postgres

-- Create database and user
CREATE DATABASE taskdb;
CREATE USER taskuser WITH PASSWORD 'password123';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;
\c taskdb
GRANT ALL ON SCHEMA public TO taskuser;

\q
```

### 2. Environment Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
```

### 3. Configuration

Create `.env` file in the project root:

```env
DATABASE_URL=postgresql://taskuser:password123@localhost/taskdb
```

### 4. Run the API

```bash
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` to see the interactive API documentation.

## API Usage

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "My First Task",
           "description": "Testing the API!"
         }'
```

### List Tasks

```bash
# Get all tasks (paginated)
curl "http://localhost:8000/tasks/"

# Filter by status
curl "http://localhost:8000/tasks/?status=pending"

# Pagination
curl "http://localhost:8000/tasks/?page=2&items_per_page=5"
```

### Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
           "status": "completed"
         }'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database and user exist

2. **Port Conflict**
   - Use an alternative port:
     ```bash
     uvicorn main:app --reload --port 8002
     ```

3. **Missing Packages**
   - Verify virtual environment is activated
   - Reinstall dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Roadmap

### Feature Enhancements
- [ ] User authentication
- [ ] Task priorities
- [ ] Due dates
- [ ] Categories/Tags
- [ ] Task notes
- [ ] Search functionality

### Technical Improvements
- [ ] Data backup system
- [ ] Email notifications
- [ ] Task import/export
- [ ] Performance optimization
- [ ] Enhanced data validation
- [ ] Audit logging
