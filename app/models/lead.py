from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, nullable=False, index=True)
    # external_id - уникальный идентификатор лида (телефон, email, ID из бота и т.п.)

    # Связь с contact
    contacts = relationship("Contact", back_populates="lead", cascade="all, delete-orphan")
