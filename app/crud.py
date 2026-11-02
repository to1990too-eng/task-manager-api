from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task = models.Task(
        title=task_in.title,
        description=task_in.description,
        completed=task_in.completed,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[models.Task]:
    stmt = select(models.Task).offset(skip).limit(limit).order_by(models.Task.id)
    return list(db.scalars(stmt).all())


def update_task(
    db: Session,
    task: models.Task,
    task_in: schemas.TaskUpdate,
) -> models.Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()