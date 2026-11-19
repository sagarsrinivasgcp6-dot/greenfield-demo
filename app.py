import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(title="Task Manager Backend", version="1.0.0")

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(default="", max_length=500, description="Task description")
    completed: bool = Field(default=False, description="Completion status")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    completed: Optional[bool] = Field(None, description="Completion status")

class Task(TaskBase):
    id: int = Field(..., description="Task ID")

# In-memory storage
tasks_db: dict[int, Task] = {}
next_task_id: int = 1

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def list_tasks():
    return list(tasks_db.values())

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    global next_task_id
    task = Task(id=next_task_id, **task_in.model_dump())
    tasks_db[next_task_id] = task
    next_task_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_in: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    current_task = tasks_db[task_id]
    update_data = task_in.model_dump(exclude_unset=True)
    updated_task = current_task.model_copy(update=update_data)
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    del tasks_db[task_id]
    return None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
