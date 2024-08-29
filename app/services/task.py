from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Task
from models import TaskModel
from services.exception import ResourceNotFoundError, InvalidInputError
from services import user as UserService

async def get_tasks(async_db: AsyncSession) -> list[Task]:
    result = await async_db.scalars(select(Task))
    return result.all()

def get_tasks_by_user_id(db: Session, id: UUID) -> list[Task]:
    user = UserService.get_user_by_id(db, id)
    if user is None:
        raise InvalidInputError("Invalid user")
    query = select(Task).filter(Task.user_id == id)
    result = db.scalars(query)
    return result.all()

def get_task_by_id(db: Session, id: UUID) -> Task:
    query = select(Task).filter(Task.id == id)
    task = db.scalars(query).first()
    if task is None:
        raise ResourceNotFoundError()
    return task

def add_new_task(db: Session, data: TaskModel) -> Task:
    task = Task(**data.model_dump())
    user = UserService.get_user_by_id(db, task.user_id)
    if user is None:
        raise InvalidInputError("Invalid user")

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()
    task.summary = data.summary
    task.description = data.description
    task.priority = data.priority
    task.status = data.status
    db.commit()
    db.refresh(task)
    return task
