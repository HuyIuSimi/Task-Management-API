# main.py

# Import the tools we need
from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import enum
import os
from dotenv import load_dotenv

# Load database settings from .env file
load_dotenv()

# Get database connection info 
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1@localhost/taskdb")

# Set up database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoload=True, bind=engine)
Base = declarative_base()


# Status should only accept specified values
class TaskStatus(str, enum.Enum):
    PENDING = "pending"     
    COMPLETED = "completed"

# Create PostgreSQL database schema
class TaskModel(Base):
    __tablename__ = "tasks"  # This is our table name
    
    # Define all the columns in our table
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, nullable=False)  
    description = Column(String)            
    status = Column(
        SQLAlchemyEnum(TaskStatus),        # Can only be pending or completed
        default=TaskStatus.PENDING         # New tasks start as pending
    )
    created_at = Column(DateTime, default=datetime.utcnow)    
    updated_at = Column(DateTime, default=datetime.utcnow)   

# Define how our data should look when creating a task
class TaskBase(BaseModel):
    # Title is required
    title: str = Field(..., min_length=1, description="Task title (required)")
    description: Optional[str] = None               
    status: Optional[TaskStatus] = TaskStatus.PENDING  # Default to pending

class TaskCreate(TaskBase):
    pass

# Define how task updates should look
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

# Define how tasks look when we send them back
class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Define how our list of tasks looks when we return them
# Return paginated results
class PaginatedTasks(BaseModel):
    total: int            # Total number of tasks
    page: int            # Current page number
    pages: int           # Total number of pages
    items_per_page: int  # How many tasks per page
    items: List[Task]    # The actual tasks

# Create our FastAPI application
app = FastAPI(
    title="Task Management API",
    description="Simple API to manage your task",
    version="1.0.0"
)

# Helper function to get database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes 

# Create a new task
# Return structured JSON with appropriate status codes
@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task - title is required!"""
    try:
        # Create new task in database
        db_task = TaskModel(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Get list of tasks with pagination and filtering
# Pagination and filtering
@app.get("/tasks/", response_model=PaginatedTasks)
def list_tasks(
    status: Optional[TaskStatus] = None,  # Filter by status if provided
    page: int = Query(1, gt=0),          # Page number (starts at 1)
    items_per_page: int = Query(10, gt=0, le=100),  # Items per page (max 100)
    db: Session = Depends(get_db)
):
    """Get all tasks with pagination. Can filter by status."""
    # Start building our database query
    query = db.query(TaskModel)
    
    # Filter by status if provided
    if status:
        query = query.filter(TaskModel.status == status)
    
    # Count total tasks
    total = query.count()
    
    # Calculate total pages
    total_pages = (total + items_per_page - 1) // items_per_page
    
    # Get the requested page of tasks
    tasks = query.offset((page - 1) * items_per_page).limit(items_per_page).all()
    
    # Return the results
    return {
        "total": total,
        "page": page,
        "pages": total_pages,
        "items_per_page": items_per_page,
        "items": tasks
    }

# Get a single task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by its ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task."""
    # Find the task
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        # Update only the fields that were provided
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        db.delete(db_task)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Create all database tables
Base.metadata.create_all(bind=engine)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)