from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    # code - уникальный код источника (например, "bot_telegram", "bot_whatsapp")

    # Связи с contacts, operator_weights
    contacts = relationship("Contact", back_populates="source")
    operator_weights = relationship(
        "OperatorSourceWeight", back_populates="source", cascade="all, delete-orphan"
    )
