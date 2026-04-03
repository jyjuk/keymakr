import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
import app.main as main_module


@pytest.fixture(autouse=True)
def reset_state():
    main_module.tasks.clear()
    main_module.counter = 0
    yield
    main_module.tasks.clear()
    main_module.counter = 0


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_tasks_empty(client: AsyncClient):
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post("/tasks", json={"title": "Test task", "description": "A test"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test task"
    assert data["done"] is False


@pytest.mark.asyncio
async def test_create_task_missing_title(client: AsyncClient):
    response = await client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tasks_after_create(client: AsyncClient):
    await client.post("/tasks", json={"title": "Task 1"})
    await client.post("/tasks", json={"title": "Task 2"})
    response = await client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    task_id = (await client.post("/tasks", json={"title": "Original"})).json()["id"]
    response = await client.put(f"/tasks/{task_id}", json={"title": "Updated", "done": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["done"] is True


@pytest.mark.asyncio
async def test_update_task_not_found(client: AsyncClient):
    response = await client.put("/tasks/9999", json={"title": "Ghost"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    task_id = (await client.post("/tasks", json={"title": "To delete"})).json()["id"]
    assert (await client.delete(f"/tasks/{task_id}")).status_code == 204
    assert (await client.get("/tasks")).json() == []


@pytest.mark.asyncio
async def test_delete_task_not_found(client: AsyncClient):
    response = await client.delete("/tasks/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_predict_returns_priority(client: AsyncClient):
    response = await client.post("/predict", json={"description": "Fix critical login bug"})
    assert response.status_code == 200
    assert response.json()["priority"] in ("high", "low")
