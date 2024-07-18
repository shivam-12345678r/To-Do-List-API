from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    owner: str
