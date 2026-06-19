# Booking Service

Сервис для создания и обработки бронирований.

---

## Запуск проекта

### 1. Запуск всего стека (обязательно)

```bash
docker-compose up --build
```
Поднимает:

* FastAPI API
* PostgreSQL
* Redis
* Celery worker

### Переменные окружения

Используется .env файл:
```bash
cp .env.example .env
```

### API

#### Создать бронирование
```
POST /api/bookings
```
```
{
  "name": "John",
  "datetime": "2026-01-01T10:00:00",
  "service_type": "haircut"
}
```

#### Получить бронирование
```
GET /bookings/{id}
```
#### Список бронирований
```
GET /bookings?status=pending&page=1&size=10
```
#### Отмена
```
DELETE /bookings/{id}
```
### Фоновая обработка

После создания бронирования задача отправляется в Celery.

Поведение воркера:
* ~15% задач → failed
* остальное → confirmed
* логируется mock-уведомление
* задача идемпотентна (повтор не ломает статус)

### Стэк
* FastAPI — быстрый async REST API
* SQLAlchemy (async) — ORM
* Celery + Redis — фоновые задачи
* PostgreSQL — основная БД
* idempotency через проверку статуса брони



