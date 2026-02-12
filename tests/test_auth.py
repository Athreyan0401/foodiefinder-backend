def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "test123"
    })

    assert response.status_code == 200
    data = response.json()

    # Since register returns JWT
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user(client):
    # Register first
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "test123"
    })

    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "test123"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"