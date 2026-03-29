import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        url='/api/v1/users/auth/register',
        json={
        'username': 'TestUser',
        'password': '1234',
        'email': "TestUser@example.com"
        }
    )
    assert response.status_code in (201, 400), response.text

@pytest.mark.asyncio
async def test_login_user(client):
    response = await client.post(
        url='/api/v1/users/auth/login',
        data={
        'username': 'TestUser',
        'password': '1234',
        }
    )
    assert response.status_code == 200, response.text

@pytest.mark.asyncio
async def test_get_info_user(client, access_token):
    response = await client.get(
        url='/api/v1/users/auth/me',
        headers={
            'Authorization': f'Bearer {access_token}',
        }
    )
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_refresh_token_user(client, access_token):
    response = await client.get(
        url='/api/v1/users/auth/refresh',
        headers={
            'Authorization': f'Bearer {access_token}',
        }
    )
    assert response.status_code == 200, response.text