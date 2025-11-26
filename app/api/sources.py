from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.source import Source
from app.models.operator_source_weight import OperatorSourceWeight
from app.schemas.source import SourceCreate, SourceResponse
from app.schemas.operator_source_weight import SourceOperatorsConfig, OperatorSourceWeightResponse

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.post("", response_model=SourceResponse, status_code=201)
def create_source(
    source: SourceCreate,
    db: Session = Depends(get_db)
):
    """Создать новый источник (бота)"""
    # Проверяем, что код уникален
    existing_source = db.query(Source).filter(Source.code == source.code).first()
    if existing_source:
        raise HTTPException(
            status_code=400,
            detail=f"Источник с кодом '{source.code}' уже существует"
        )
    
    db_source = Source(
        name=source.name,
        code=source.code
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


@router.get("", response_model=List[SourceResponse])
def get_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список всех источников"""
    sources = db.query(Source).offset(skip).limit(limit).all()
    return sources


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """Получить источник по ID"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    return source


@router.post("/{source_id}/operators", response_model=List[OperatorSourceWeightResponse])
def configure_source_operators(
    source_id: int,
    config: SourceOperatorsConfig,
    db: Session = Depends(get_db)
):
    """
    Настроить операторов для источника с весами.
    
    Удаляет существующие веса и создает новые согласно переданной конфигурации.
    """
    # Проверяем, что источник существует
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    # Удаляем существующие веса для этого источника
    db.query(OperatorSourceWeight).filter(
        OperatorSourceWeight.source_id == source_id
    ).delete()
    
    # Создаем новые веса
    created_weights = []
    for op_weight in config.operator_weights:
        # Проверяем, что оператор существует
        from app.models.operator import Operator
        operator = db.query(Operator).filter(Operator.id == op_weight.operator_id).first()
        if not operator:
            raise HTTPException(
                status_code=404,
                detail=f"Оператор с ID {op_weight.operator_id} не найден"
            )
        
        weight = OperatorSourceWeight(
            operator_id=op_weight.operator_id,
            source_id=source_id,
            weight=op_weight.weight
        )
        db.add(weight)
        created_weights.append(weight)
    
    db.commit()
    
    # Обновляем объекты для ответа
    for weight in created_weights:
        db.refresh(weight)
    
    return created_weights


@router.get("/{source_id}/operators", response_model=List[OperatorSourceWeightResponse])
def get_source_operators(
    source_id: int,
    db: Session = Depends(get_db)
):
    """Получить список операторов с весами для источника"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    
    weights = db.query(OperatorSourceWeight).filter(
        OperatorSourceWeight.source_id == source_id
    ).all()
    
    return weights

