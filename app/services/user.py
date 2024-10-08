from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import User
from schemas.user import get_password_hash
from models import UserModel
from services.exception import ResourceNotFoundError, InvalidInputError
from services import company as CompanyService
from services import utils
from settings import DEFAULT_PASSWORD

async def get_users(async_db: AsyncSession) -> list[User]:
    result = await async_db.scalars(select(User))
    return result.all()

def get_users_by_company_id(db: Session, id: UUID) -> list[User]:
    company = CompanyService.get_company_by_id(db, id)
    if company is None:
        raise InvalidInputError("Invalid company information")
    query = select(User).filter(User.company_id == id, User.is_active == True)
    return db.scalars(query).all()

def get_user_by_id(db: Session, id: UUID) -> User:
    query = select(User).filter(User.id == id)
    user = db.scalars(query).first()
    if user is None:
        raise ResourceNotFoundError()
    return user

def add_new_user(db: Session, data: UserModel) -> User:
    user = User(**data.model_dump())
    company = CompanyService.get_company_by_id(db, user.company_id)
    if company is None:
        raise InvalidInputError("Invalid company information")
    user.hashed_password = get_password_hash(DEFAULT_PASSWORD)
    user.is_active = True
    user.is_admin = False
    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, id: UUID, data: UserModel) -> User:
    user = get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()
    user.email = data.email
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.updated_at = utils.get_current_utc_time()
    db.commit()
    db.refresh(user)
    return user
