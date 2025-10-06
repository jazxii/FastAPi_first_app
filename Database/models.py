from pydantic import BaseModel, Field
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    is_completed: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    creation: int = int( datetime.timestamp(datetime.now()) )
    update: int = int( datetime.timestamp(datetime.now()) )