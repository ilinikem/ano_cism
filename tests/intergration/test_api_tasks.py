import pytest


@pytest.mark.asyncio
async def test_create_task_api(client):
    response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "API test task",
            "description": "API test description",
            "priority": "HIGH"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API test task"
    assert data["priority"] == "HIGH"


@pytest.mark.asyncio
async def test_get_task_list_api(client):
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_task_detail_api(client):
    # Создаём задачу
    create_response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Detail task"}
    )
    task_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_delete_task_api(client):
    create_response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Delete task"}
    )
    task_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"
