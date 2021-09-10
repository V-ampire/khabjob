import pytest

from api.auth import make_jwt_token_for_user


@pytest.fixture
async def auth_headers(create_user):
    user = await create_user()
    token = make_jwt_token_for_user(user.id)
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    return (user, headers)