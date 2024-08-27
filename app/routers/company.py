from typing import List
from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db_context, get_db_context
from services import company as CompanyService
from services.exception import ResourceNotFoundError
from models import CompanyModel, CompanyViewModel

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyViewModel])
async def get_all_companies(async_db: AsyncSession = Depends(get_async_db_context)):
    return await CompanyService.get_companies(async_db)

@router.get("/{company_id}", response_model=CompanyViewModel)
async def get_company_detail(company_id: UUID, db: Session=Depends(get_db_context)):
    company = CompanyService.get_company_by_id(db, company_id)
    if company is None:
        raise ResourceNotFoundError()

    return company

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def create_company(
    request: CompanyModel,
    db: Session = Depends(get_db_context)
    ):
    return CompanyService.add_new_company(db, request)

@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company(
    company_id: UUID,
    request: CompanyModel,
    db: Session=Depends(get_db_context)
    ):
    return CompanyService.update_company(db, company_id, request)
