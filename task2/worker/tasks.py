import csv
import logging
import os

import requests

from .celery_app import celery_app

logger = logging.getLogger(__name__)

USERS_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "users.csv"))


@celery_app.task(name="worker.tasks.fetch_and_save_users")
def fetch_and_save_users() -> str:
    response = requests.get(USERS_URL, timeout=10)
    response.raise_for_status()
    users = response.json()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email"])
        writer.writeheader()
        for user in users:
            writer.writerow({"id": user["id"], "name": user["name"], "email": user["email"]})

    logger.info("Saved %d users to %s", len(users), OUTPUT_PATH)
    return f"Saved {len(users)} users to {OUTPUT_PATH}"
