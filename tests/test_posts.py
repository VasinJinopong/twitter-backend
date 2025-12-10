import pytest


@pytest.fixture
def test_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "postuser@test.com", "username": "postuser", "password": "password123"}
    )
    return response.json()


@pytest.fixture
def token(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "postuser@test.com", "password": "password123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# Tests
def test_create_post(authorized_client):
    response = authorized_client.post(
        "/api/v1/posts",
        json={"title": "Test Post", "content": "My first post"}  # ← เพิ่ม title
    )
    assert response.status_code == 201


def test_create_post_unauthorized(client):
    response = client.post(
        "/api/v1/posts",
        json={"title": "Test", "content": "Should fail"}  # ← เพิ่ม title
    )
    assert response.status_code == 401


def test_create_post_empty_title(authorized_client):
    response = authorized_client.post(
        "/api/v1/posts",
        json={"title": "", "content": "Content"}  # ← title ว่าง
    )
    assert response.status_code == 422


def test_create_post_empty_content(authorized_client):
    response = authorized_client.post(
        "/api/v1/posts",
        json={"title": "Title", "content": ""}  # ← content ว่าง
    )
    assert response.status_code == 422


def test_get_all_posts(authorized_client):
    authorized_client.post("/api/v1/posts", json={"title": "Post 1", "content": "Content 1"})
    authorized_client.post("/api/v1/posts", json={"title": "Post 2", "content": "Content 2"})
    response = authorized_client.get("/api/v1/posts")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_post_by_id(authorized_client):
    create = authorized_client.post(
        "/api/v1/posts",
        json={"title": "Test Post", "content": "Test content"}
    )
    post_id = create.json()["id"]
    response = authorized_client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200


def test_get_post_not_found(authorized_client):
    response = authorized_client.get("/api/v1/posts/99999")
    assert response.status_code == 404


def test_update_post(authorized_client):
    create = authorized_client.post(
        "/api/v1/posts",
        json={"title": "Original", "content": "Original content"}
    )
    post_id = create.json()["id"]
    response = authorized_client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Updated", "content": "Updated content"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_other_user_post(client):
    # User 1
    client.post("/api/v1/auth/register", json={"email": "user1@test.com", "username": "user1", "password": "password123"})
    login1 = client.post("/api/v1/auth/login", data={"username": "user1@test.com", "password": "password123"})
    token1 = login1.json()["access_token"]
    create = client.post(
        "/api/v1/posts",
        json={"title": "User 1", "content": "User 1 post"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    post_id = create.json()["id"]
    
    # User 2
    client.post("/api/v1/auth/register", json={"email": "user2@test.com", "username": "user2", "password": "password123"})
    login2 = client.post("/api/v1/auth/login", data={"username": "user2@test.com", "password": "password123"})
    token2 = login2.json()["access_token"]
    
    response = client.put(
        f"/api/v1/posts/{post_id}",
        json={"title": "Hacked", "content": "Hacked"},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403


def test_delete_post(authorized_client):
    create = authorized_client.post(
        "/api/v1/posts",
        json={"title": "To delete", "content": "Delete me"}
    )
    post_id = create.json()["id"]
    response = authorized_client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 204