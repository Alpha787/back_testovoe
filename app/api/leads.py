from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadResponse

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.get("", response_model=List[LeadResponse])
def get_leads(
    skip: int = 0,
    limit: int = 100,
    external_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Получить список лидов.
    
    Поддерживает фильтрацию по external_id.
    """
    query = db.query(Lead)
    
    if external_id is not None:
        query = query.filter(Lead.external_id == external_id)
    
    leads = query.options(joinedload(Lead.contacts)).offset(skip).limit(limit).all()
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """Получить лида по ID с его обращениями"""
    lead = db.query(Lead).options(joinedload(Lead.contacts)).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Лид не найден")
    return lead

