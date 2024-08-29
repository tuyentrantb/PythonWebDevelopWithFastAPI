from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.orm import Session
from schemas import User
from database import get_db_context
from models import TaskViewModel, TaskModel, SearchTaskModel
from services import task as TaskService
from services import auth as AuthService
from services.exception import AccessDeniedError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_all_tasks(
    summary: str = Query(default=None),
    description: str = Query(default=None),
    priority: int = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context)):
    conds = SearchTaskModel(summary, description, priority, page, size)
    return TaskService.get_tasks(db, conds)

@router.get("/{user_id}/assignments",\
    status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_tasks_by_user(
    user_id: UUID,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)):
    if (not user.is_admin) and (user.id != user_id):
        raise AccessDeniedError()
    return TaskService.get_tasks_by_user_id(db, user_id)

@router.get("/{task_id}", response_model=TaskViewModel)
async def get_user_detail(task_id: UUID, db: Session=Depends(get_db_context)):
    return TaskService.get_task_by_id(db, task_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)
    ):
    if not user.is_admin:
        request.user_id = user.id
    return TaskService.add_new_task(db, request)

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: UUID,
    request: TaskModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session=Depends(get_db_context)
    ):
    if (not user.is_admin) and (user.id != request.user_id):
        raise AccessDeniedError()
    return TaskService.update_task(db, task_id, request)
