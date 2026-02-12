def test_review_creates_notification(client):
    # Register user A
    client.post("/auth/register", json={
        "email": "usera@example.com",
        "password": "test123"
    })
    login_a = client.post("/auth/login", json={
        "email": "usera@example.com",
        "password": "test123"
    })
    token_a = login_a.json()["access_token"]

    # Register user B
    client.post("/auth/register", json={
        "email": "userb@example.com",
        "password": "test123"
    })
    login_b = client.post("/auth/login", json={
        "email": "userb@example.com",
        "password": "test123"
    })
    token_b = login_b.json()["access_token"]

    # Create restaurant manually (since no seed)
    restaurant = client.post("/restaurants", json={
        "name": "Test Cafe",
        "location": "Chennai",
        "address": "Some address"
    })

    restaurant_id = restaurant.json()["id"]

    # User A posts review
    client.post(
        "/reviews",
        json={
            "restaurant_id": restaurant_id,
            "content": "Good food",
            "rating": 5,
            "photo_url": None
        },
        headers={"Authorization": f"Bearer {token_a}"}
    )

    # User B posts review (should notify A)
    client.post(
        "/reviews",
        json={
            "restaurant_id": restaurant_id,
            "content": "Nice place",
            "rating": 4,
            "photo_url": None
        },
        headers={"Authorization": f"Bearer {token_b}"}
    )

    # Check notifications for A
    notifications = client.get(
        "/notifications",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    assert notifications.status_code == 200
    assert len(notifications.json()) == 1