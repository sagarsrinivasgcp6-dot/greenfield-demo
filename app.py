import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Backend API for Task Management"
)

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    status: str = Field("pending", description="Task status: pending, in_progress, completed")
    priority: str = Field("medium", description="Task priority: low, medium, high")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = None
    priority: Optional[str] = None

class Task(TaskBase):
    id: int

# In-memory storage
tasks_db = {}
next_task_id = 1

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}

@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def list_tasks():
    return list(tasks_db.values())

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global next_task_id
    task = Task(
        id=next_task_id,
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority
    )
    tasks_db[next_task_id] = task
    next_task_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    existing = tasks_db[task_id]
    update_data = task_in.model_dump(exclude_unset=True)
    updated_task = existing.model_copy(update=update_data)
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    del tasks_db[task_id]
    return None

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
