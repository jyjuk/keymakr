from fastapi import FastAPI

from worker.tasks import fetch_and_save_users

app = FastAPI(title="Task 2 — User Fetcher", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/fetch-users", status_code=202)
def trigger_fetch():
    fetch_and_save_users.delay()
    return {"message": "Task queued"}
