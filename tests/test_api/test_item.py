import pytest

@pytest.mark.asyncio
async def test_create_update_delete_item(client, access_token):
    response_post = await client.post(
        url='/api/v1/users/items',
        json={
        'name': 'Chair',
        'category': 'home',
        'count': 100,
        'price': 2000,
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response_post.status_code == 201, response_post.text

    response_update = await client.put(
        url=f'/api/v1/users/items/{response_post.json()["id"]}',
        params={'id' : int(response_post.json()["id"])},
        json={
        'name': 'Table',
        'category': 'school',
        'count': 10,
        'price': 20000,
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response_update.status_code == 201, response_post.text

    response_delete = await client.delete(
        url=f'/api/v1/users/items/{response_post.json()["id"]}',
        params={'id': int(response_post.json()["id"])},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response_delete.status_code == 204, response_delete.text

@pytest.mark.asyncio
async def test_get_items(client, access_token):
    response = await client.get(
        url=f'/api/v1/users/items',
        params={
            'limit': 1,
            'offset': 10,
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code in (200, 404), response.text