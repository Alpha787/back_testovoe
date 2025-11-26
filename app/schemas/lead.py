from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.contact import ContactResponse


class LeadBase(BaseModel):
    """Базовая схема лида"""
    external_id: str = Field(..., description="Уникальный идентификатор лида (телефон, email, ID из бота)")


class LeadCreate(LeadBase):
    """Схема для создания лида"""
    pass


class LeadResponse(LeadBase):
    """Схема ответа с лидом"""
    id: int
    contacts: Optional[List["ContactResponse"]] = None

    class Config:
        from_attributes = True
