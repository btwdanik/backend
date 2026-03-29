import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager

from src.main import main

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(main):
        async with AsyncClient(
            transport=ASGITransport(app=main),
            base_url="http://localhost:8080",
        ) as client:
            yield client

@pytest_asyncio.fixture
async def user(client):
    response = await client.post(
        url='/api/v1/users/auth/register',
        json={
        'username': 'TestUser',
        'password': '1234',
        'email': "TestUser@example.com"
        }
    )
    assert response.status_code in (201, 400), response.text

@pytest_asyncio.fixture
async def access_token(client, user):
    response = await client.post(
        "/api/v1/users/auth/login",
        data={
            "username": "TestUser",
            "password": "1234",
        }
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]
