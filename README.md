# Keymakr Hiring Test

## Task 1 — RESTful API

REST API для управління списком задач (to-do list) на базі FastAPI.

### Запуск

```bash
cd task1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Документація: http://localhost:8000/docs

### Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| GET | /tasks | Список всіх задач |
| POST | /tasks | Створити задачу |
| PUT | /tasks/{task_id} | Оновити задачу |
| DELETE | /tasks/{task_id} | Видалити задачу |

### Тести

```bash
cd task1
pytest tests/ -v
```
