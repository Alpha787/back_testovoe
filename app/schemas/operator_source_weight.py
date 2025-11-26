from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.operator import OperatorResponse
    from app.schemas.source import SourceResponse


class OperatorSourceWeightBase(BaseModel):
    """Базовая схема веса оператора по источнику"""
    operator_id: int = Field(..., description="ID оператора")
    weight: int = Field(..., ge=1, description="Вес для распределения трафика")


class OperatorSourceWeightCreate(OperatorSourceWeightBase):
    """Схема для создания веса"""
    source_id: int = Field(..., description="ID источника")


class OperatorSourceWeightResponse(OperatorSourceWeightBase):
    """Схема ответа с весом"""
    id: int
    source_id: int
    operator: Optional["OperatorResponse"] = None
    source: Optional["SourceResponse"] = None

    class Config:
        from_attributes = True


class SourceOperatorsConfig(BaseModel):
    """Схема для настройки операторов источника с весами"""
    operator_weights: list[OperatorSourceWeightBase] = Field(
        ..., 
        description="Список операторов с их весами для данного источника"
    )

