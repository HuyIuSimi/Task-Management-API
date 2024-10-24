# Task Management API 

Hi! I'm an intern, and this is my Task Management API project. I'll guide you through setting it up step by step!

## What This API Can Do 

- Create new tasks 
- List all tasks 
- Update tasks 
- Delete tasks 
- Mark tasks as completed 

## Why I Made These Choices 

1. **FastAPI**
   - Really easy to learn and use
   - Creates automatic API documentation
   - Helps catch errors before they happen
   - Super fast!

2. **Simple Status System**
   - Just two statuses: 'pending' and 'completed'
   - Easy to understand and use
   - Covers the basic needs of task management

## Let's Set It Up! 

### 1. Database Setup

First, we need to set up PostgreSQL. After installing PostgreSQL, open your terminal and run these commands:

```sql
-- Log into PostgreSQL (it will ask for your password)
psql -U postgres

-- Create our database and user you can change the password
CREATE DATABASE taskdb;
CREATE USER taskuser WITH PASSWORD 'password123';

-- Give our user permissions
GRANT ALL PRIVILEGES ON DATABASE taskdb TO taskuser;

-- Connect to our new database
\c taskdb

-- Give additional permissions needed for tables
GRANT ALL ON SCHEMA public TO taskuser;

-- Now we can exit
\q
```

### 2. Python Setup

```bash
# Create a virtual environment
python -m venv .venv

# Activate it:
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install required packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
```

### 3. Environment Setup

Create a file named `.env` in your project folder and add:
```
DATABASE_URL=postgresql://taskuser:{yourpassword}@localhost/taskdb
```

### 4. Run the API

```bash
uvicorn main:app --reload --port 8000
```

## Testing The API 🧪

The easiest way to test is through the automatic documentation:
1. Go to: http://localhost:8000/docs
2. You'll see all available endpoints
3. Click on any endpoint to try it out!

### Example API Calls

#### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "My First Task",
           "description": "Testing the API!"
         }'
```

#### Get All Tasks
```bash
# Get first page of tasks
curl "http://localhost:8000/tasks/"

# Get pending tasks only
curl "http://localhost:8000/tasks/?status=pending"

# Get second page with 5 tasks per page
curl "http://localhost:8000/tasks/?page=2&items_per_page=5"
```

#### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
           "status": "completed"
         }'
```

#### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## What Could Go Wrong? 

If you get errors:

1. **Can't Connect to Database?**
   - Make sure PostgreSQL is running
   - Check your database username and password
   - Make sure you created the database and user

2. **Port Already in Use?**
   - Try a different port number:
   ```bash
   uvicorn main:app --reload --port 8002,8003,...
   ```

3. **Package Not Found?**
   - Make sure your virtual environment is activated
   - Try installing packages again

## Future Improvements 🚀

Here's how we could make this even better:

1. **New Features**
   - Add user accounts
   - Add task priorities
   - Add due dates
   - Add task categories
   - Add task notes
   - Add task search

2. **Technical Improvements**
   - Add data backup
   - Add user authentication
   - Add email notifications
   - Add task import/export

3. **Database Improvements**
   - Add more indexes for speed
   - Add data validation
   - Add task history tracking

#   T a s k - M a n a g e m e n t - A P I  
 