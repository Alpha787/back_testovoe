from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class OperatorSourceWeight(Base):
    """Промежуточная таблица для связи операторов и источников с весами"""
    __tablename__ = "operator_source_weights"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    weight = Column(Integer, nullable=False, default=1)
    # weight - числовой вес для распределения трафика

    # Уникальная пара оператор-источник
    __table_args__ = (
        UniqueConstraint("operator_id", "source_id", name="uq_operator_source"),
    )

    # Связи с operator, source
    operator = relationship("Operator", back_populates="source_weights")
    source = relationship("Source", back_populates="operator_weights")

