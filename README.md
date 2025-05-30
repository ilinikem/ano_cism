# Асинхронный сервис управления задачами

## Описание

Сервис для асинхронной обработки задач с возможностью масштабирования и отказоустойчивости.

### Функциональные возможности

- Создание задач через REST API
- Асинхронная обработка задач в фоновом режиме
- Параллельная обработка нескольких задач
- Поддержка приоритетов задач (LOW, MEDIUM, HIGH)
- Статусная модель задач: NEW, PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED

### Структура задачи

- Уникальный идентификатор
- Название
- Описание
- Приоритет
- Статус
- Время создания, начала и завершения выполнения
- Результат выполнения
- Информация об ошибках

---

## Технологии

Python 3.12,
FastAPI,
PostgreSQL 14,
RabbitMQ,
SQLAlchemy,
Alembic,
OpenAPI (Swagger),
Docker/Docker Compose

---

## API Endpoints

- POST /api/v1/tasks - создание задачи
- GET /api/v1/tasks - получение списка задач с фильтрацией и пагинацией
- GET /api/v1/tasks/{task_id} - получение информации о задаче
- DELETE /api/v1/tasks/{task_id} - отмена задачи
- GET /api/v1/tasks/{task_id}/status - получение статуса задачи

---

## Локальный запуск

### Создайте файл `.env` с такими переменными:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=task_service
DB_USER=myuser
DB_PASSWORD=t1a2s3k_s4e5r6v7i8ce!

### Запуск приложения:
```
uvicorn app.main:app --reload
```
### Alembic

Инициализация:
```
alembic init -t async migrations
```
Создание миграций:
```
alembic revision --autogenerate -m "initial revision"
```
Применение миграций:
```
alembic upgrade head
```
### Запуск воркера:
```
python -m app.worker
```
**Важно:** 
RabbitMQ должен быть запущен.

---

## Запуск через Docker Compose

Собрать:
```
docker compose build
```

Запустить:
```
docker compose up   
```

## Тестирование

Запуск unit и интеграционных тестов с подробным выводом:
```
python -m pytest -v --asyncio-mode=auto
```

Запуск тестов с покрытием:
```
python -m pytest --cov=app tests/
```
