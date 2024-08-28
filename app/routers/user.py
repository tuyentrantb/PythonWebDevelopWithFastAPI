from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_context, get_async_db_context
from models import UserViewModel, UserBaseModel, UserModel
from services import user as UserService
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_all_users(async_db: AsyncSession = Depends(get_async_db_context)):
    return await UserService.get_users(async_db)

@router.get("/{company_id}/staff",\
    status_code=status.HTTP_200_OK, response_model=List[UserViewModel])
async def get_users_company(company_id: UUID,\
    async_db: AsyncSession = Depends(get_async_db_context)):
    return await UserService.get_users_by_company_id(async_db, company_id)

@router.get("/{user_id}", response_model=UserViewModel)
async def get_user_detail(user_id: UUID, db: Session=Depends(get_db_context)):
    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise ResourceNotFoundError()
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: UserModel,
    db: Session = Depends(get_db_context)
    ):
    return UserService.add_new_user(db, request)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(
    user_id: UUID,
    request: UserBaseModel,
    db: Session=Depends(get_db_context)
    ):
    return UserService.update_user(db, user_id, request)
