from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.distribution import distribute_contact

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


@router.post("", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    """
    Зарегистрировать обращение от лида.
    
    Система автоматически:
    - Найдет или создаст лида по external_id
    - Найдет источник по source_code
    - Выберет оператора по алгоритму распределения (с учетом весов и лимитов)
    - Создаст обращение
    """
    try:
        created_contact = distribute_contact(
            db=db,
            external_id=contact.external_id,
            source_code=contact.source_code
        )
        
        # Загружаем связанные объекты для ответа
        db.refresh(created_contact)
        return created_contact
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании обращения: {str(e)}")


@router.get("", response_model=List[ContactResponse])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    operator_id: int = None,
    source_id: int = None,
    lead_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Получить список обращений.
    
    Поддерживает фильтрацию по:
    - operator_id: ID оператора
    - source_id: ID источника
    - lead_id: ID лида
    """
    query = db.query(Contact)
    
    if operator_id is not None:
        query = query.filter(Contact.operator_id == operator_id)
    if source_id is not None:
        query = query.filter(Contact.source_id == source_id)
    if lead_id is not None:
        query = query.filter(Contact.lead_id == lead_id)
    
    contacts = query.offset(skip).limit(limit).all()
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """Получить обращение по ID"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Обращение не найдено")
    return contact

