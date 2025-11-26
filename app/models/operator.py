from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    max_load = Column(Integer, nullable=False, default=10)  # Лимит активных контактов

    # Связи с contacts, source_weights
    contacts = relationship("Contact", back_populates="operator")
    source_weights = relationship(
        "OperatorSourceWeight", back_populates="operator", cascade="all, delete-orphan"
    )
