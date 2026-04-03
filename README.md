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

---

## Task 2 — Celery + Redis + Docker

Фонова задача на Celery, яка щохвилини отримує список користувачів з публічного API і зберігає їх у CSV.

### Запуск

```bash
cd task2
docker-compose up --build
```

### Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| GET | /health | Health check |
| POST | /fetch-users | Запустити задачу вручну |

Детальніше: [task2/README.md](task2/README.md)

### Тести

```bash
cd task2
pytest tests/ -v
```

---

## Task 3 — ML Integration

REST API для управління задачами з ML-класифікацією пріоритету (high/low) на базі FastAPI + scikit-learn.

Модель (TF-IDF + LogisticRegression) навчається автоматично при першому старті на даних з `data/tasks.csv`.

### Запуск

```bash
cd task3
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Документація: http://localhost:8000/docs

### Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| GET | /tasks | Список всіх задач |
| POST | /tasks | Створити задачу |
| PUT | /tasks/{id} | Оновити задачу |
| DELETE | /tasks/{id} | Видалити задачу |
| POST | /predict | Передбачити пріоритет за описом |

### Тести

```bash
cd task3
pytest tests/ -v
```
