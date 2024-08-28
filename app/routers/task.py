from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_context, get_async_db_context
from models import TaskViewModel, TaskModel
from services import task as TaskService
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_all_tasks(async_db: AsyncSession = Depends(get_async_db_context)):
    return await TaskService.get_tasks(async_db)

@router.get("/{user_id}/assignment",\
    status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_tasks_by_user(user_id: UUID,\
    db: Session = Depends(get_db_context)):
    return TaskService.get_tasks_by_user_id(db, user_id)

@router.get("/{task_id}", response_model=TaskViewModel)
async def get_user_detail(task_id: UUID, db: Session=Depends(get_db_context)):
    task = TaskService.get_task_by_id(db, task_id)
    if task is None:
        raise ResourceNotFoundError()
    return task

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel,
    db: Session = Depends(get_db_context)
    ):
    return TaskService.add_new_task(db, request)

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    user_id: UUID,
    request: TaskModel,
    db: Session=Depends(get_db_context)
    ):
    return TaskService.update_task(db, user_id, request)
