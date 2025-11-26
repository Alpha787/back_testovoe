import random
from typing import Optional
from sqlalchemy.orm import Session

from app.models.operator import Operator
from app.models.source import Source
from app.models.contact import Contact, ContactStatus
from app.models.operator_source_weight import OperatorSourceWeight
from app.services.lead_service import get_or_create_lead


def get_operator_current_load(db: Session, operator_id: int) -> int:
    """
    Получить текущую нагрузку оператора (количество активных контактов).
    
    Args:
        db: Сессия БД
        operator_id: ID оператора
    
    Returns:
        int: Количество активных контактов
    """
    return db.query(Contact).filter(
        Contact.operator_id == operator_id,
        Contact.status == ContactStatus.ACTIVE.value
    ).count()


def get_available_operators(
    db: Session, 
    source_id: int
) -> list[tuple[Operator, int]]:
    """
    Найти доступных операторов для источника.
    
    Оператор считается доступным, если:
    - Он активен (is_active = True)
    - Его текущая нагрузка не превышает лимит (max_load)
    - Для него задан вес для данного источника
    
    Args:
        db: Сессия БД
        source_id: ID источника
    
    Returns:
        list[tuple[Operator, int]]: Список кортежей (оператор, вес)
    """
    # Получаем всех операторов с весами для данного источника
    operator_weights = db.query(OperatorSourceWeight).filter(
        OperatorSourceWeight.source_id == source_id
    ).all()
    
    available_operators = []
    
    for op_weight in operator_weights:
        operator = op_weight.operator
        
        # Проверяем, что оператор активен
        if not operator.is_active:
            continue
        
        # Проверяем лимит нагрузки
        current_load = get_operator_current_load(db, operator.id)
        if current_load >= operator.max_load:
            continue
        
        available_operators.append((operator, op_weight.weight))
    
    return available_operators


def select_operator_by_weights(
    available_operators: list[tuple[Operator, int]]
) -> Optional[Operator]:
    """
    Выбрать оператора по весам (вероятностный выбор).
    
    Алгоритм:
    1. Вычисляем сумму всех весов
    2. Генерируем случайное число от 0 до суммы весов
    3. Выбираем оператора, в диапазон веса которого попало число
    
    Args:
        available_operators: Список кортежей (оператор, вес)
    
    Returns:
        Optional[Operator]: Выбранный оператор или None, если список пуст
    """
    if not available_operators:
        return None
    
    # Вычисляем сумму весов
    total_weight = sum(weight for _, weight in available_operators)
    
    if total_weight == 0:
        return None
    
    # Генерируем случайное число от 0 до total_weight
    random_value = random.uniform(0, total_weight)
    
    # Выбираем оператора по весам
    current_sum = 0
    for operator, weight in available_operators:
        current_sum += weight
        if random_value <= current_sum:
            return operator
    
    # На всякий случай возвращаем последнего (не должно произойти)
    return available_operators[-1][0]


def distribute_contact(
    db: Session,
    external_id: str,
    source_code: str
) -> Contact:
    """
    Распределить обращение лида между операторами.
    
    Алгоритм:
    1. Найти или создать лида по external_id
    2. Найти источник по code
    3. Найти доступных операторов (активные, не превысили лимит)
    4. Выбрать оператора по весам (вероятностный выбор)
    5. Создать обращение
    
    Если подходящих операторов нет, создается обращение без оператора.
    
    Args:
        db: Сессия БД
        external_id: Уникальный идентификатор лида
        source_code: Код источника (бота)
    
    Returns:
        Contact: Созданное обращение
    """
    # 1. Найти или создать лида
    lead = get_or_create_lead(db, external_id)
    
    # 2. Найти источник
    source = db.query(Source).filter(Source.code == source_code).first()
    if not source:
        raise ValueError(f"Источник с кодом '{source_code}' не найден")
    
    # 3. Найти доступных операторов
    available_operators = get_available_operators(db, source.id)
    
    # 4. Выбрать оператора по весам
    selected_operator = None
    if available_operators:
        # Проверяем лимиты еще раз перед выбором (защита от race condition)
        # Фильтруем только тех, кто еще не превысил лимит
        valid_operators = [
            (op, weight) for op, weight in available_operators
            if get_operator_current_load(db, op.id) < op.max_load
        ]
        
        if valid_operators:
            selected_operator = select_operator_by_weights(valid_operators)
            # Финальная проверка лимита перед созданием (дополнительная защита)
            if selected_operator and get_operator_current_load(db, selected_operator.id) >= selected_operator.max_load:
                selected_operator = None
    
    # 5. Создать обращение
    contact = Contact(
        lead_id=lead.id,
        source_id=source.id,
        operator_id=selected_operator.id if selected_operator else None,
        status=ContactStatus.ACTIVE.value
    )
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return contact

