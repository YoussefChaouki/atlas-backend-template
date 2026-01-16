import pytest


@pytest.mark.live
def test_lifecycle_create_read(api_client):
    """Scenario: Create -> Get List -> Get Detail."""

    # 1. CREATE
    payload = {
        "title": "Live Test",
        "content": "Running inside Docker",
        "is_active": True,
    }
    res_post = api_client.post("/notes/", json=payload)
    assert res_post.status_code == 201
    data = res_post.json()
    assert data["title"] == payload["title"]
    note_id = data["id"]

    # 2. GET LIST
    res_list = api_client.get("/notes/")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # 3. GET DETAIL
    res_get = api_client.get(f"/notes/{note_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == note_id


@pytest.mark.live
def test_not_found(api_client):
    """Scenario: 404 on fake ID."""
    res = api_client.get("/notes/999999999")
    assert res.status_code == 404


@pytest.mark.live
def test_validation_error(api_client):
    """Scenario: Invalid payload (title too short)."""
    payload = {"title": "No", "content": "Valid Content"}
    res = api_client.post("/notes/", json=payload)
    assert res.status_code == 422
