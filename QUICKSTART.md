# Быстрый старт

## 1. Установка зависимостей

```bash
pipenv install
```

Или через pip:
```bash
pip install fastapi[standard] sqlalchemy
```

## 2. Запуск сервера

```bash
uvicorn app.main:app --reload
```

Сервер будет доступен на: http://127.0.0.1:8000

## 3. Проверка работы

### Вариант 1: Через браузер
Откройте http://127.0.0.1:8000/docs - там будет интерактивная документация API

### Вариант 2: Через тестовый скрипт
В другом терминале:
```bash
python test_api.py
```

### Вариант 3: Через curl

```bash
# Проверка работы сервера
curl http://127.0.0.1:8000/

# Создание оператора
curl -X POST "http://127.0.0.1:8000/api/operators" \
  -H "Content-Type: application/json" \
  -d '{"name": "Тест", "is_active": true, "max_load": 10}'

# Создание источника
curl -X POST "http://127.0.0.1:8000/api/sources" \
  -H "Content-Type: application/json" \
  -d '{"name": "Тест бот", "code": "test_bot"}'
```

## 4. Документация

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Подробная документация в файле README.md

