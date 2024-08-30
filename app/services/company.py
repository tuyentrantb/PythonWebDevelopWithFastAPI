from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Company
from models import CompanyModel
from services import utils
from services.exception import ResourceNotFoundError

async def get_companies(async_db: AsyncSession) -> list[Company]:
    result = await async_db.scalars(select(Company))
    return result.all()

def get_company_by_id(db: Session, id: UUID) -> Company:
    query = select(Company).filter(Company.id == id)
    company = db.scalars(query).first()
    if company is None:
        raise ResourceNotFoundError()
    return company

def add_new_company(db: Session, data: CompanyModel) -> Company:
    company = Company(**data.model_dump())
    company.created_at = utils.get_current_utc_time()
    company.updated_at = utils.get_current_utc_time()

    db.add(company)
    db.commit()
    db.refresh(company)
    return company

def update_company(db: Session, id: UUID, data: CompanyModel) -> Company:
    company = get_company_by_id(db, id)

    if company is None:
        raise ResourceNotFoundError()
    company.name = data.name
    company.description = data.description
    company.mode = data.mode
    company.rating = data.rating
    company.updated_at = utils.get_current_utc_time()
    db.commit()
    db.refresh(company)
    return company
