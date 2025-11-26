from sqlalchemy.orm import Session
from app.models.lead import Lead


def get_or_create_lead(db: Session, external_id: str) -> Lead:
    """
    Найти существующего лида по external_id или создать нового.
    
    Args:
        db: Сессия БД
        external_id: Уникальный идентификатор лида (телефон, email, ID из бота)
    
    Returns:
        Lead: Найденный или созданный лид
    """
    lead = db.query(Lead).filter(Lead.external_id == external_id).first()
    
    if not lead:
        lead = Lead(external_id=external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)
    
    return lead

