from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.operator import Operator
from app.schemas.operator import OperatorCreate, OperatorUpdate, OperatorResponse

router = APIRouter(prefix="/api/operators", tags=["operators"])


@router.post("", response_model=OperatorResponse, status_code=201)
def create_operator(
    operator: OperatorCreate,
    db: Session = Depends(get_db)
):
    """Создать нового оператора"""
    db_operator = Operator(
        name=operator.name,
        is_active=operator.is_active,
        max_load=operator.max_load
    )
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


@router.get("", response_model=List[OperatorResponse])
def get_operators(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список всех операторов"""
    operators = db.query(Operator).offset(skip).limit(limit).all()
    return operators


@router.get("/{operator_id}", response_model=OperatorResponse)
def get_operator(
    operator_id: int,
    db: Session = Depends(get_db)
):
    """Получить оператора по ID"""
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Оператор не найден")
    return operator


@router.patch("/{operator_id}", response_model=OperatorResponse)
def update_operator(
    operator_id: int,
    operator_update: OperatorUpdate,
    db: Session = Depends(get_db)
):
    """Обновить оператора (активность, лимит нагрузки, имя)"""
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Оператор не найден")
    
    if operator_update.name is not None:
        operator.name = operator_update.name
    if operator_update.is_active is not None:
        operator.is_active = operator_update.is_active
    if operator_update.max_load is not None:
        operator.max_load = operator_update.max_load
    
    db.commit()
    db.refresh(operator)
    return operator

