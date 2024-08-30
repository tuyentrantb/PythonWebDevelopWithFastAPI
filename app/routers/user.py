from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_context, get_async_db_context

from models import UserViewModel, UserModel
from schemas import User
from services import user as UserService
from services import auth as AuthService
from services.exception import AccessDeniedError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_all_users(async_db: AsyncSession = Depends(get_async_db_context)):
    return await UserService.get_users(async_db)

@router.get("/{company_id}/staffs",\
    status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_users_company(
    company_id: UUID,
    db: Session=Depends(get_db_context)):
    return UserService.get_users_by_company_id(db, company_id)

@router.get("/{user_id}", response_model=UserViewModel)
async def get_user_detail(
    user_id: UUID,
    user: User = Depends(AuthService.token_interceptor),
    db: Session=Depends(get_db_context)):
    if (not user.is_admin) and (user.id != user_id):
        raise AccessDeniedError()
    return UserService.get_user_by_id(db, user_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: UserModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context)
    ):
    if not user.is_admin:
        raise AccessDeniedError()
    return UserService.add_new_user(db, request)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(
    user_id: UUID,
    request: UserModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session=Depends(get_db_context)
    ):
    if (not user.is_admin) and (user.id != user_id):
        raise AccessDeniedError()
    return UserService.update_user(db, user_id, request)
