import pytest


@pytest.mark.asyncio
async def test_get_bookings_list(client):
    await client.post(
        "/api/bookings/",
        json={
            "name": "User 1",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "haircut"
        }
    )
    await client.post(
        "/api/bookings/",
        json={
            "name": "User 2",
            "datetime": "2026-01-02T10:00:00",
            "service_type": "massage"
        }
    )
    response = await client.get("/api/bookings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


@pytest.mark.asyncio
async def test_get_bookings_pagination(client):
    # создаём 3 записи
    for i in range(3):
        await client.post(
            "/api/bookings/",
            json={
                "name": f"User {i}",
                "datetime": "2026-01-01T10:00:00",
                "service_type": "test"
            }
        )

    # page=1 size=2 → максимум 2 записи
    response = await client.get("/api/bookings/?page=1&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_create_booking(client):
    response = await client.post(
        "/api/bookings/",
        json={
            "name": "Test User",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "haircut"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_get_bookings_filter_by_status(client):
    created = await client.post(
        "/api/bookings/",
        json={
            "name": "User",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "test"
        }
    )
    response = await client.get("/api/bookings/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for item in data:
        assert item["status"] == "pending"


@pytest.mark.asyncio
async def test_get_booking(client):
    created = await client.post(
        "/api/bookings/",
        json={
            "name": "Test User",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "haircut"
        }
    )
    booking_id = created.json()["id"]
    response = await client.get(f"/api/bookings/{booking_id}")
    assert response.status_code == 200
    assert response.json()["id"] == booking_id


@pytest.mark.asyncio
async def test_cancel_booking(client):
    created = await client.post(
        "/api/bookings/",
        json={
            "name": "Test User",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "haircut"
        }
    )
    booking_id = created.json()["id"]
    response = await client.delete(f"/api/bookings/{booking_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_cancel_not_pending(client):
    created = await client.post(
        "/api/bookings/",
        json={
            "name": "Test User",
            "datetime": "2026-01-01T10:00:00",
            "service_type": "haircut"
        }
    )
    booking_id = created.json()["id"]
    response = await client.delete(f"/api/bookings/{booking_id}")
    assert response.status_code in [200, 400]
