# Импорты моделей для удобства использования
from app.models.operator import Operator
from app.models.lead import Lead
from app.models.source import Source
from app.models.contact import Contact, ContactStatus
from app.models.operator_source_weight import OperatorSourceWeight

__all__ = [
    "Operator",
    "Lead",
    "Source",
    "Contact",
    "ContactStatus",
    "OperatorSourceWeight",
]

