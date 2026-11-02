from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="0.1.0",
    description="REST API для управления задачами",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
) -> models.Task:
    return crud.create_task(db, task_in)


@app.get("/tasks", response_model=list[schemas.TaskRead], tags=["tasks"])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[models.Task]:
    return crud.get_tasks(db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=schemas.TaskRead, tags=["tasks"])
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> models.Task:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskRead, tags=["tasks"])
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
) -> models.Task:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return crud.update_task(db, task, task_in)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    crud.delete_task(db, task)