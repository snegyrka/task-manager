from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_register_success():
    r = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "StrongPass1"
    })
    assert r.status_code == 200
    assert r.json()["username"] == "testuser"


def test_register_duplicate():
    r = client.post("/register", json={
        "username": "testuser",
        "email": "test2@test.com",
        "password": "StrongPass1"
    })
    assert r.status_code == 400


def test_weak_password():
    r = client.post("/register", json={
        "username": "user2",
        "email": "user2@test.com",
        "password": "123"
    })
    assert r.status_code == 422


def test_invalid_email():
    r = client.post("/register", json={
        "username": "user3",
        "email": "bad",
        "password": "StrongPass1"
    })
    assert r.status_code == 422


def get_token():
    r = client.post("/token", data={
        "username": "testuser",
        "password": "StrongPass1"
    })
    return r.json()["access_token"]


def test_login():
    token = get_token()
    assert token is not None
    assert len(token) > 0


def test_unauthorized():
    assert client.get("/projects/").status_code == 401


def test_create_project():
    t = get_token()
    r = client.post("/projects/", json={
        "name": "My Project",
        "description": "Test"
    }, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200
    assert r.json()["name"] == "My Project"


def test_create_task():
    t = get_token()
    r = client.post("/tasks/", json={
        "title": "My Task",
        "project_id": 1,
        "estimated_hours": 5
    }, headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200


def test_workload():
    t = get_token()
    r = client.get("/workload/1", headers={
        "Authorization": f"Bearer {t}"
    })
    assert r.status_code == 200


def test_suggest():
    t = get_token()
    r = client.get("/suggest-assignee/1", headers={
        "Authorization": f"Bearer {t}"
    })
    assert r.status_code == 200