from fastapi import FastAPI, HTTPException, status

from .models import Task, TaskCreate, TaskUpdate

tasks: dict[int, Task] = {}
counter: int = 0

app = FastAPI(title="Task Manager API", version="1.0.0")


def _get_task_or_404(task_id: int) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found.",
        )
    return task


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return list(tasks.values())


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global counter
    counter += 1
    task = Task(id=counter, **payload.model_dump())
    tasks[counter] = task
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    task = _get_task_or_404(task_id)
    updated = Task.model_validate({**task.model_dump(), **payload.model_dump(exclude_unset=True)})
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    _get_task_or_404(task_id)
    del tasks[task_id]
