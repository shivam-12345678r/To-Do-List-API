from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from hashlib import sha256
from typing import Optional
from models import User, Task

app = FastAPI()

# Temporary storage
users_db = []
tasks_db = []

# Authentication middleware
def authenticate_user(username: str, password: str):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    for user in users_db:
        if user.username == username and user.password == hashed_password:
            return True
    return False

# Dependency for authentication
def get_current_user(username: str = Depends(authenticate_user)):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=401, detail="Invalid credentials")

# CRUD operations for tasks
@app.post("/tasks/", response_model=Task)
def create_task(task: Task, current_user: User = Depends(get_current_user)):
    task.id = len(tasks_db) + 1
    task.owner = current_user.username
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def read_tasks(status: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if status:
        return [task for task in tasks_db if task.status == status and task.owner == current_user.username]
    return [task for task in tasks_db if task.owner == current_user.username]

@app.put("/tasks/{task_id}/", response_model=Task)
def update_task(task_id: int, status: str, current_user: User = Depends(get_current_user)):
    for task in tasks_db:
        if task.id == task_id and task.owner == current_user.username:
            task.status = status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}/", response_model=Task)
def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    for index, task in enumerate(tasks_db):
        if task.id == task_id and task.owner == current_user.username:
            tasks_db.pop(index)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# User management
@app.post("/users/", response_model=User)
def create_user(user: User):
    hashed_password = sha256(user.password.encode('utf-8')).hexdigest()
    new_user = User(username=user.username, password=hashed_password)
    users_db.append(new_user)
    return new_user
