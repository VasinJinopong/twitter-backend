

endpoint = "/api/v1/auth/register"

def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@test.com",
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data



def test_register_duplicate_email(client):
    """Test register with duplicate email fails"""
    # สร้าง user แรก
    client.post(
        "/api/v1/auth/register",
        json={
            "email" : "duplicate@test.com",
            "username" : "user1",
            "password" : "password123"
        }
    )

    # พยายามสร้างซ้ำ
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email" : "duplicate@test.com",
            "username" :"user2",
            "password" : "passww1asdads"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()['detail'].lower()




def test_register_duplicate_username(client):
    """Test registering with dupliate username fails"""

    endpoint = "/api/v1/auth/register"

    #สร้าง User แรก
    client.post(
        endpoint, json={
            "email" : "testuser1@test.com",
            "username" : "test1",
            "password" : "password123"
        }
    )

    #สร้าง User ครั้งที่สอง
    response = client.post(
        endpoint, json={
            "email" : "testuser2@test.com",
            "username" : "test1",
            "password" : "password123"
        }
    )

    assert response.status_code == 400


def test_register_invalid_email(client):
    """Test invalid email"""

    response = client.post(
        endpoint,json={
            "email" : "notanemail",
            "username" : "ddddddd",
            "password" : "kdosfopdkf"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):
    """Test short password"""
    response = client.post(
        endpoint, json={
            "email" : "treedd@gmail.com",
            "username" : "aseasdasdasd",
            "password" : "pa"
        }
    )
    assert response.status_code == 422

    
def test_register_short_username(client):
    """Test short username"""

    response = client.post(
        endpoint, json={
            "email" : "treedd@gmail.com",
            "username" : "a",
            "password" : "dsdfsdfdsf"
        }
    )
    assert response.status_code == 422





def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@test.com", "username": "testuser", "password": "password123", "full_name": "Test User"}
    )
    assert response.status_code == 201


def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={"email": "dup@test.com", "username": "user1", "password": "password123"})
    response = client.post("/api/v1/auth/register", json={"email": "dup@test.com", "username": "user2", "password": "password123"})
    assert response.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={"email": "test@test.com", "username": "testuser", "password": "password123"})
    response = client.post("/api/v1/auth/login", data={"username": "test@test.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={"email": "test@test.com", "username": "testuser", "password": "password123"})
    response = client.post("/api/v1/auth/login", data={"username": "test@test.com", "password": "wrongpass"})
    assert response.status_code == 401