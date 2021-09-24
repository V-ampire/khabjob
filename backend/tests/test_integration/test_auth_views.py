from freezegun import freeze_time
import pytest

from api.auth import make_jwt_token_for_user

from core.services.auth import (
    is_token_blacklisted,
    get_user,
    is_password_confirm
)


async def test_login_view_with_invalid_password(api_client, create_user):
    user = await create_user()

    url = api_client.app.router['login'].url_for()

    credentials = {
        'username': user.username,
        'password': 'qwerty123'
    }

    resp = await api_client.post(url, json=credentials)
    result = await resp.json()

    assert resp.status == 401
    assert result['reason'] == 'Invalid user credentials.'


async def test_login_view_with_invalid_username(api_client):

    url = api_client.app.router['login'].url_for()

    credentials = {
        'username': 'Hacker',
        'password': 'qwerty123'
    }

    resp = await api_client.post(url, json=credentials)
    result = await resp.json()

    assert resp.status == 401
    assert result['reason'] == 'Invalid user credentials.'


@freeze_time("2021-01-14 03:21:34")
async def test_login_view_success(api_client, create_user):
    user = await create_user(password='qwerty123')

    url = api_client.app.router['login'].url_for()

    credentials = {
        'username': user.username,
        'password': 'qwerty123'
    }

    resp = await api_client.post(url, json=credentials)
    result = await resp.json()

    assert resp.status == 200
    assert result == {
        'jwt_token': make_jwt_token_for_user(user.id),
        'user': user.username
    }


@freeze_time("2021-01-14 03:21:34")
async def test_logout_view_success(api_client, create_user, aio_engine):
    user = await create_user()

    headers = {
        'Authorization': 'Bearer {0}'.format(make_jwt_token_for_user(user.id))
    }

    expected_token = make_jwt_token_for_user(user.id)

    url = api_client.app.router['logout'].url_for()

    resp = await api_client.get(url, headers=headers)
    result = await resp.json()

    resp_401 = await api_client.get("/private/vacancies", headers=headers)

    async with aio_engine.acquire() as conn:
        assert await is_token_blacklisted(conn, expected_token)

    resp.status == 200
    result == {'status': 'logout'}
    assert resp_401.status == 401


async def test_logout_view_unauthorized(api_client, create_user, aio_engine):

    url = api_client.app.router['logout'].url_for()

    resp = await api_client.get(url)
    
    assert resp.status == 403


async def test_logout_view_invalid_token(api_client, make_jwt_token):
    headers = {
        'Authorization': 'Bearer {0}'.format(make_jwt_token())
    }

    url = api_client.app.router['logout'].url_for()

    resp = await api_client.get(url, headers=headers)
    
    assert resp.status == 401


async def test_reset_password_view_with_invalid_credentials(api_client, create_user, aio_engine):
    user = await create_user(password='qwerty123')

    url = api_client.app.router['reset_password'].url_for()

    invalid_username_data = {
        'username': 'Hacker',
        'old_password': 'qwerty123',
        'new_password1': 'qWerty%56',
        'new_password2': 'qWerty%56',
    }

    invalid_password_data = {
        'username': user.username,
        'old_password': 'qwerty456',
        'new_password1': 'qWerty%56',
        'new_password2': 'qWerty%56',
    }

    resp_username = await api_client.post(url, json=invalid_username_data)
    resp_password = await api_client.post(url, json=invalid_password_data)

    async with aio_engine.acquire() as conn:
        expected_user =  await get_user(conn, username=user.username)

    assert resp_username.status == 401
    assert resp_password.status == 401
    assert not is_password_confirm('qWerty%56', expected_user.password_hash)


async def test_reset_password_view_with_invalid_new_password(api_client, create_user, aio_engine):
    user = await create_user(password='qwerty123')

    url = api_client.app.router['reset_password'].url_for()

    invalid_format_data = {
        'username': 'Joda777',
        'old_password': 'qwerty123',
        'new_password1': 'qwerty456',
        'new_password2': 'qwerty456',
    }

    invalid_repeat_data = {
        'username': 'Joda777',
        'old_password': 'qwerty123',
        'new_password1': 'qWerty%56',
        'new_password2': 'qwerty789',
    }

    resp_format = await api_client.post(url, json=invalid_format_data)
    resp_repeat = await api_client.post(url, json=invalid_repeat_data)

    async with aio_engine.acquire() as conn:
        expected_user =  await get_user(conn, username=user.username)

    assert resp_format.status == 400
    assert resp_repeat.status == 400
    assert not is_password_confirm('qwerty456', expected_user.password_hash)


async def test_reset_password_view_success_reset(api_client, create_user, aio_engine):
    user = await create_user(password='qwerty123')

    url = api_client.app.router['reset_password'].url_for()

    password_data = {
        'username': user.username,
        'old_password': 'qwerty123',
        'new_password1': 'qWerty%56',
        'new_password2': 'qWerty%56',
    }


    resp = await api_client.post(url, json=password_data)

    async with aio_engine.acquire() as conn:
        expected_user =  await get_user(conn, username=user.username)

    assert resp.status == 200
    assert is_password_confirm('qWerty%56', expected_user.password_hash)