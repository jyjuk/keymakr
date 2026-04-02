# Task 2 — Celery + Redis + Docker

Fetches users from a public API and saves them to CSV using Celery and Redis.

## Services

| Service | Description |
|---------|-------------|
| `redis` | Message broker and result backend |
| `api` | FastAPI app |
| `celery_worker` | Executes tasks |
| `celery_beat` | Schedules tasks every 60 seconds |

## Run

```bash
cd task2
docker-compose up --build
```

Every 60 seconds the worker fetches users from `jsonplaceholder.typicode.com/users`
and saves `id`, `name`, `email` to `data/users.csv`.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /health | Health check |
| POST | /fetch-users | Manually trigger fetch |

## Trigger manually

```bash
curl -X POST http://localhost:8000/fetch-users
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Redis broker URL |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | Redis result backend URL |

## Requirements

- Docker
- Docker Compose
