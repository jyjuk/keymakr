import csv
from unittest.mock import MagicMock, patch

from worker.tasks import fetch_and_save_users


def test_fetch_and_save_users(tmp_path):
    fake_users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    mock_response = MagicMock()
    mock_response.json.return_value = fake_users
    csv_path = tmp_path / "users.csv"

    with patch("worker.tasks.requests.get", return_value=mock_response), \
         patch("worker.tasks.OUTPUT_PATH", str(csv_path)):
        result = fetch_and_save_users()

    mock_response.raise_for_status.assert_called_once()

    assert csv_path.exists()
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0] == {"id": "1", "name": "Alice", "email": "alice@example.com"}
    assert rows[1] == {"id": "2", "name": "Bob", "email": "bob@example.com"}
    assert "Saved 2 users" in result
