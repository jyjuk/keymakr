# Keymakr Hiring Test

Три незалежних завдання в одному репозиторії.

```
task1/   — RESTful API (FastAPI, Pydantic, unit-тести)
task2/   — Celery + Redis + Docker
task3/   — ML-інтеграція (/predict endpoint)
```

---

## Task 1 — RESTful API

```bash
cd task1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Запуск тестів:
```bash
pytest tests/ -v
```

Документація: http://localhost:8000/docs

---

## Task 2 — Celery + Redis + Docker

```bash
cd task2
docker-compose up --build
```

Піднімає чотири сервіси: `redis`, `api` (task1), `celery_worker`, `celery_beat`.  
Кожні 60 секунд worker отримує список користувачів з `jsonplaceholder.typicode.com/users`
і зберігає `id, name, email` у `data/users.csv`.

---

## Task 3 — ML-інтеграція

```bash
cd task3
pip install -r requirements.txt
uvicorn app.main:app --reload
```

При першому запуску автоматично навчається модель (`TfidfVectorizer` + `LogisticRegression`)
і зберігається у `ml/model.pkl`.

Запит на передбачення пріоритету:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"description": "Fix critical authentication bug"}'
# {"priority": "high"}
```

Запуск тестів:
```bash
pytest tests/ -v
```
