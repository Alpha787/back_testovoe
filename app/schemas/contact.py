from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.lead import LeadResponse
    from app.schemas.source import SourceResponse
    from app.schemas.operator import OperatorResponse


class ContactBase(BaseModel):
    """Базовая схема обращения"""
    status: str = Field(default="active", description="Статус обращения (active/completed)")


class ContactCreate(BaseModel):
    """Схема для создания обращения (регистрация обращения от лида)"""
    external_id: str = Field(..., description="Уникальный идентификатор лида")
    source_code: str = Field(..., description="Код источника (бота)")
    message: Optional[str] = Field(None, description="Текст обращения (опционально)")


class ContactResponse(ContactBase):
    """Схема ответа с обращением"""
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int] = None
    created_at: datetime
    
    # Вложенные объекты (опционально, для детального ответа)
    lead: Optional["LeadResponse"] = None
    source: Optional["SourceResponse"] = None
    operator: Optional["OperatorResponse"] = None

    class Config:
        from_attributes = True
