# Task 3 — ML Integration

REST API for task management with ML-based priority prediction.

## Run

```bash
cd task3
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The model trains automatically on first startup using `data/tasks.csv`.

Documentation: http://localhost:8000/docs

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /tasks | List all tasks |
| POST | /tasks | Create a task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| POST | /predict | Predict task priority |

## Predict example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"description": "Fix login bug on website"}'
```

Response:
```json
{"priority": "high"}
```

## Tests

```bash
cd task3
pytest tests/ -v
```
