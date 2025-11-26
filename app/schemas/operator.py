from pydantic import BaseModel, Field
from typing import Optional


class OperatorBase(BaseModel):
    """Базовая схема оператора"""
    name: str = Field(..., description="Имя оператора")
    is_active: bool = Field(default=True, description="Активен ли оператор")
    max_load: int = Field(default=10, ge=1, description="Лимит активных контактов")


class OperatorCreate(OperatorBase):
    """Схема для создания оператора"""
    pass


class OperatorUpdate(BaseModel):
    """Схема для обновления оператора"""
    name: Optional[str] = None
    is_active: Optional[bool] = None
    max_load: Optional[int] = Field(None, ge=1)


class OperatorResponse(OperatorBase):
    """Схема ответа с оператором"""
    id: int

    class Config:
        from_attributes = True
