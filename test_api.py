"""
Скрипт для тестирования API.
Запустите сервер (uvicorn app.main:app --reload) перед выполнением этого скрипта.
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api"


def test_api():
    """Тестирование основных функций API"""
    
    print("=" * 60)
    print("Тестирование Mini-CRM API")
    print("=" * 60)
    
    # 1. Создание операторов
    print("\n1. Создание операторов...")
    operator1 = requests.post(
        f"{BASE_URL}/operators",
        json={"name": "Оператор 1", "is_active": True, "max_load": 10}
    ).json()
    print(f"   ✓ Создан оператор: {operator1['name']} (ID: {operator1['id']})")
    
    operator2 = requests.post(
        f"{BASE_URL}/operators",
        json={"name": "Оператор 2", "is_active": True, "max_load": 15}
    ).json()
    print(f"   ✓ Создан оператор: {operator2['name']} (ID: {operator2['id']})")
    
    # 2. Создание источника
    print("\n2. Создание источника...")
    source = requests.post(
        f"{BASE_URL}/sources",
        json={"name": "Telegram бот", "code": "bot_telegram"}
    ).json()
    print(f"   ✓ Создан источник: {source['name']} (ID: {source['id']}, код: {source['code']})")
    
    # 3. Настройка распределения
    print("\n3. Настройка распределения операторов для источника...")
    weights = requests.post(
        f"{BASE_URL}/sources/{source['id']}/operators",
        json={
            "operator_weights": [
                {"operator_id": operator1['id'], "weight": 10},
                {"operator_id": operator2['id'], "weight": 30}
            ]
        }
    ).json()
    print(f"   ✓ Настроены веса: Оператор 1 (вес 10), Оператор 2 (вес 30)")
    print(f"   Ожидаемое распределение: ~25% и ~75% соответственно")
    
    # 4. Регистрация обращений
    print("\n4. Регистрация обращений от разных лидов...")
    contacts_created = []
    
    for i in range(5):
        contact = requests.post(
            f"{BASE_URL}/contacts",
            json={
                "external_id": f"user_{i+1}",
                "source_code": "bot_telegram",
                "message": f"Обращение #{i+1}"
            }
        ).json()
        contacts_created.append(contact)
        operator_name = contact.get('operator', {}).get('name') if contact.get('operator') else "НЕ НАЗНАЧЕН"
        print(f"   ✓ Обращение {i+1}: лид {contact['lead_id']}, оператор: {operator_name}")
    
    # 5. Проверка распределения
    print("\n5. Проверка распределения обращений...")
    operator1_contacts = requests.get(
        f"{BASE_URL}/contacts?operator_id={operator1['id']}"
    ).json()
    operator2_contacts = requests.get(
        f"{BASE_URL}/contacts?operator_id={operator2['id']}"
    ).json()
    
    print(f"   Оператор 1: {len(operator1_contacts)} обращений")
    print(f"   Оператор 2: {len(operator2_contacts)} обращений")
    
    # 6. Просмотр лидов
    print("\n6. Просмотр лидов...")
    leads = requests.get(f"{BASE_URL}/leads").json()
    print(f"   ✓ Всего лидов: {len(leads)}")
    for lead in leads:
        contacts_count = len(lead.get('contacts', []))
        print(f"   - Лид {lead['id']} (external_id: {lead['external_id']}): {contacts_count} обращений")
    
    # 7. Проверка нагрузки операторов
    print("\n7. Проверка нагрузки операторов...")
    op1 = requests.get(f"{BASE_URL}/operators/{operator1['id']}").json()
    op2 = requests.get(f"{BASE_URL}/operators/{operator2['id']}").json()
    
    op1_load = len(operator1_contacts)
    op2_load = len(operator2_contacts)
    
    print(f"   Оператор 1: {op1_load}/{op1['max_load']} контактов")
    print(f"   Оператор 2: {op2_load}/{op2['max_load']} контактов")
    
    print("\n" + "=" * 60)
    print("Тестирование завершено!")
    print("=" * 60)
    print(f"\nДокументация API: http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу.")
        print("Убедитесь, что сервер запущен: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"Ошибка: {e}")

