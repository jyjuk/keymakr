from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = None
    done: bool | None = None


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    done: bool = False
