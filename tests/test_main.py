from fastapi.testclient import TestClient


def _create_task(client: TestClient, **overrides) -> dict:
    payload = {"title": "Sample task", "description": "desc", "completed": False}
    payload.update(overrides)
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client: TestClient) -> None:
    body = _create_task(client, title="Write tests")
    assert body["title"] == "Write tests"
    assert body["completed"] is False
    assert isinstance(body["id"], int)
    assert "created_at" in body


def test_create_task_validation(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks_empty(client: TestClient) -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks(client: TestClient) -> None:
    _create_task(client, title="One")
    _create_task(client, title="Two")
    response = client.get("/tasks")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert [t["title"] for t in body] == ["One", "Two"]


def test_list_tasks_pagination(client: TestClient) -> None:
    for i in range(3):
        _create_task(client, title=f"Task {i}")
    response = client.get("/tasks", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "Task 1"


def test_get_task(client: TestClient) -> None:
    created = _create_task(client)
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_task_not_found(client: TestClient) -> None:
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task_partial(client: TestClient) -> None:
    created = _create_task(client, title="Original", description="keep me")
    response = client.patch(f"/tasks/{created['id']}", json={"completed": True})
    assert response.status_code == 200
    body = response.json()
    assert body["completed"] is True
    assert body["title"] == "Original"
    assert body["description"] == "keep me"


def test_update_task_not_found(client: TestClient) -> None:
    response = client.patch("/tasks/9999", json={"completed": True})
    assert response.status_code == 404


def test_delete_task(client: TestClient) -> None:
    created = _create_task(client)
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    follow_up = client.get(f"/tasks/{created['id']}")
    assert follow_up.status_code == 404


def test_delete_task_not_found(client: TestClient) -> None:
    response = client.delete("/tasks/9999")
    assert response.status_code == 404