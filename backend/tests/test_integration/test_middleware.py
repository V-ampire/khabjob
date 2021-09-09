from aiohttp import web

import jwt

import pytest
from unittest.mock import AsyncMock

from api.auth import User, make_jwt_token_for_user
from api.middleware import jwt_auth_middleware

from config import AUTH_CONFIG


handler = AsyncMock(return_value=web.Response())


@pytest.fixture
def api(loop, aiohttp_client, aio_engine):
    app = web.Application(middlewares=[jwt_auth_middleware])
    app['db'] = aio_engine
    app.router.add_get('/', handler)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def make_jwt_token():
    def gen_token(payload={}):
        return jwt.encode(
            payload,
            AUTH_CONFIG['SECRET_KEY'],
            algorithm=AUTH_CONFIG['ALGORITHM']
        )
    return gen_token


async def test_authenticate_user_with_user(api, create_user):
    user = await create_user()
    token = make_jwt_token_for_user(user.id)
    headers = {
        AUTH_CONFIG['JWT_HEADER_NAME']: '{0} {1}'.format(AUTH_CONFIG['JWT_AUTH_SCHEME'], token)
    }
    resp = await api.get('/', headers=headers)
    result_user = handler.await_args.args[0]['user']
    expected_user = User(
        id=user.id,
        username=user.username,
        password_hash=user.password_hash
    )

    assert result_user == expected_user

