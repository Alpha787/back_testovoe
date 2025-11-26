from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.api import operators, sources, contacts, leads

# Разрешаем forward references в Pydantic схемах ДО создания FastAPI app
# Это необходимо для корректной генерации OpenAPI схемы
# Импортируем все схемы, которые используются в forward references
from app.schemas.operator import OperatorResponse
from app.schemas.contact import ContactResponse
from app.schemas.lead import LeadResponse
from app.schemas.source import SourceResponse
from app.schemas.operator_source_weight import OperatorSourceWeightResponse

# Создаем локальное пространство имен для разрешения forward references
_localns = {
    "OperatorResponse": OperatorResponse,
    "ContactResponse": ContactResponse,
    "LeadResponse": LeadResponse,
    "SourceResponse": SourceResponse,
    "OperatorSourceWeightResponse": OperatorSourceWeightResponse,
}

# Вызываем model_rebuild для всех схем с forward references
# Передаем локальное пространство имен для разрешения циклических зависимостей
OperatorSourceWeightResponse.model_rebuild(_types_namespace=_localns)
SourceResponse.model_rebuild(_types_namespace=_localns)
ContactResponse.model_rebuild(_types_namespace=_localns)
LeadResponse.model_rebuild(_types_namespace=_localns)


@asynccontextmanager
async def lifespan(app: FastAPI):
     # Startup: инициализация БД при старте
    init_db()
    yield
    # Shutdown: можно добавить логику закрытия соединений при необходимости


app = FastAPI(title="Мини-CRM распределения лидов между операторами и источниками", lifespan=lifespan)

# Подключение роутеров
app.include_router(operators.router)
app.include_router(sources.router)
app.include_router(contacts.router)
app.include_router(leads.router)


@app.get("/")
async def root():
    return {"message": "Mini-CRM API"}
