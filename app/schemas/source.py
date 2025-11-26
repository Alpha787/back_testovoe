from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.operator_source_weight import OperatorSourceWeightResponse


class SourceBase(BaseModel):
    """Базовая схема источника"""
    name: str = Field(..., description="Название источника")
    code: str = Field(..., description="Уникальный код источника (например, bot_telegram)")


class SourceCreate(SourceBase):
    """Схема для создания источника"""
    pass


class SourceResponse(SourceBase):
    """Схема ответа с источником"""
    id: int
    operator_weights: Optional[List["OperatorSourceWeightResponse"]] = None

    class Config:
        from_attributes = True
