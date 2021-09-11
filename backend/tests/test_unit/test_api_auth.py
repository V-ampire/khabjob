from aiohttp.web import HTTPForbidden
from aiohttp.test_utils import make_mocked_request

import jwt

from freezegun import freeze_time
from datetime import datetime, timedelta
import json
import pytest

from api import auth
from api.app import init_app

from config import AUTH_CONFIG


def test_authenticate_headers(make_jwt_token):
    token = make_jwt_token({'user_id': 1})
    headers = {
        AUTH_CONFIG['JWT_HEADER_NAME']: 'Bearer {0}'.format(token)
    }
    request = make_mocked_request('GET', '/', headers=headers)

    assert auth.authenticate_headers(request) == token


def test_authenticate_headers_no_header():
    request = make_mocked_request('GET', '/')
    assert auth.authenticate_headers(request) is None


def test_authenticate_headers_empty_header():
    request = make_mocked_request(
        'GET', 
        '/', 
        headers={AUTH_CONFIG['JWT_HEADER_NAME']: ''}
    )
    assert auth.authenticate_headers(request) is None


def test_authenticate_headers_invalid_auth_scheme():
    request = make_mocked_request(
        'GET', 
        '/', 
        headers={AUTH_CONFIG['JWT_HEADER_NAME']: 'Basic 123'}
    )
    assert auth.authenticate_headers(request) is None


def test_authenticate_headers_invalid_header():
    request = make_mocked_request(
        'GET', 
        '/', 
        headers={AUTH_CONFIG['JWT_HEADER_NAME']: 'Bearer 123 456'}
    )
    with pytest.raises(HTTPForbidden):
        auth.authenticate_headers(request)



async def test_authenticate_request_success(create_user, jwt_request):
    expected_user = await create_user()
    expired = datetime.utcnow() + timedelta(days=1)
    request, expected_token = jwt_request({
        'user_id': expected_user.id,
        'jwt_exp': expired.isoformat()
    })

    result = await auth.authenticate(request)

    assert result == (auth.User(
        id=expected_user.id,
        username=expected_user.username,
        password_hash=expected_user.password_hash
    ), expected_token)


async def test_authenticate_request_no_token(jwt_request, mocker):
    mock_auth_headers = mocker.patch('api.auth.authenticate_headers')
    mock_auth_headers.return_value = None

    request, token  = jwt_request({})

    result = await auth.authenticate(request)

    assert result == (None, None)


async def test_authenticate_request_token_expired(jwt_request, mocker):
    expected_expired = '2021-01-14 03:21:34'
    request, token = jwt_request({'jwt_exp': expected_expired})

    mock_check_exp = mocker.patch('api.auth.check_jwt_token_expired')
    mock_check_exp.side_effect = [auth.TokenError('Expired')]

    with pytest.raises(HTTPForbidden) as err_403:
        result = await auth.authenticate(request)

    assert err_403.value.text == json.dumps({'reason': 'Expired'})
    mock_check_exp.assert_called_with(expected_expired)


async def test_authenticate_request_token_blacklisted(jwt_request, aio_patch, mocker):
    request, token = jwt_request({})
    mock_check_exp = mocker.patch('api.auth.check_jwt_token_expired')
    mock_is_blacklist = aio_patch('api.auth.check_token_blacklist')
    mock_is_blacklist.side_effect = [auth.TokenError('Blacklisted')]

    with pytest.raises(HTTPForbidden) as err_403:
        result = await auth.authenticate(request)

    assert err_403.value.text == json.dumps({'reason': 'Blacklisted'})
    assert mock_check_exp.call_count == 1
    assert mock_is_blacklist.await_count == 1


async def test_authenticate_request_user_not_found(jwt_request, aio_patch, mocker):
    request, token = jwt_request({})
    mock_check_exp = mocker.patch('api.auth.check_jwt_token_expired')
    mock_is_blacklist = aio_patch('api.auth.check_token_blacklist')
    mock_get_user = aio_patch('api.auth.get_jwt_token_user')
    mock_get_user.side_effect = [auth.TokenError('No user')]

    with pytest.raises(HTTPForbidden) as err_403:
        result = await auth.authenticate(request)
    
    assert err_403.value.text == json.dumps({'reason': 'No user'})
    assert mock_check_exp.call_count == 1
    assert mock_is_blacklist.await_count == 1
    assert mock_get_user.await_count == 1


@freeze_time("2012-01-14 03:21:34")
def test_make_jwt_token_for_user():
    user_id = 1
    jwt_exp_dt = datetime.utcnow() + AUTH_CONFIG['JWT_LIFETIME']
    
    expected = jwt.encode(
        {
            'user_id': user_id,
            'jwt_exp': jwt_exp_dt.isoformat()
        }, 
        AUTH_CONFIG['SECRET_KEY'],
        algorithm=AUTH_CONFIG['ALGORITHM']
    )

    assert expected == auth.make_jwt_token_for_user(user_id)


def test_check_jwt_token_expired_format_err():
    with pytest.raises(auth.TokenError) as format_err:
        auth.check_jwt_token_expired('2012.01.14 03:21:34')

    with pytest.raises(auth.TokenError) as type_err:
        auth.check_jwt_token_expired(None)
    
    assert format_err.value.message == 'Invalid token expired datetime format.'
    assert type_err.value.message == 'Invalid token expired datetime format.'


@freeze_time("2012-01-14 03:21:34")
def test_check_jwt_token_expired_expired_err():
    expired_less_dt = datetime.utcnow() - timedelta(seconds=1)
    expired_now_dt = datetime.utcnow()
    not_expired_dt = datetime.utcnow() + timedelta(seconds=1)

    auth.check_jwt_token_expired(not_expired_dt.isoformat())

    with pytest.raises(auth.TokenError) as expired_less_err:
        auth.check_jwt_token_expired(expired_less_dt.isoformat())

    with pytest.raises(auth.TokenError) as expired_now_err:
        auth.check_jwt_token_expired(expired_now_dt.isoformat())
    
    assert expired_less_err.value.message == 'Token has expired.'
    assert expired_now_err.value.message == 'Token has expired.'


async def test_get_jwt_token_user_id_error(mocker):
    invald_id = '1'

    with pytest.raises(auth.TokenError) as id_error:
        await auth.get_jwt_token_user(mocker.Mock(), invald_id)

    assert id_error.value.message == 'Invalid jwt token payload.'


async def test_get_jwt_token_user_no_user(mocker, aio_patch):
    mock_get_user = aio_patch('api.auth.get_user')
    mock_get_user.return_value = None

    with pytest.raises(auth.TokenError) as user_error:
        await auth.get_jwt_token_user(mocker.Mock(), 1)

    assert user_error.value.message == 'Access authenticated only.'


async def test_get_jwt_token_user_success(mocker, aio_patch):
    expected_id = 1
    expected_username = 'Yoda777Jedi'
    expected_password_hash = '123456'
    mock_get_user = aio_patch('api.auth.get_user')
    mock_get_user.return_value = auth.User(
        id=expected_id,
        username=expected_username,
        password_hash=expected_password_hash
    )

    result = await auth.get_jwt_token_user(mocker.Mock(), 1)

    assert result == auth.User(
        id=expected_id,
        username=expected_username,
        password_hash=expected_password_hash
    )


async def test_check_token_blacklist_error(mocker, aio_patch, make_jwt_token):
    expected_token = make_jwt_token({})
    mock_conn = mocker.Mock()
    mock_is_blacklist = aio_patch('api.auth.is_token_blacklisted')
    mock_is_blacklist.return_value = True

    with pytest.raises(auth.TokenError) as bl_error:
        await auth.check_token_blacklist(mock_conn, expected_token)

    assert bl_error.value.message == 'Token is invalid.'
    mock_is_blacklist.assert_awaited_with(mock_conn, expected_token)


async def test_check_token_blacklist_success(mocker, aio_patch, make_jwt_token):
    expected_token = make_jwt_token({})
    mock_conn = mocker.Mock()
    mock_is_blacklist = aio_patch('api.auth.is_token_blacklisted')
    mock_is_blacklist.return_value = False

    await auth.check_token_blacklist(mock_conn, expected_token)

    mock_is_blacklist.assert_awaited_with(mock_conn, expected_token)


async def test_check_authentication(mocker, aio_patch, jwt_request):
    expected_user = auth.User(id=1, username='Joda777', password_hash='123456')
    request, expected_token = jwt_request({})
    mock_auth = aio_patch('api.auth.authenticate')
    mock_auth.return_value = (expected_user, expected_token)

    result = await auth.check_authentication(request)

    assert result['user'] == expected_user
    assert result['token'] == expected_token
    assert result is request


async def test_authenticate_user_not_found(aio_patch, mocker):
    conn = mocker.Mock()

    user_credentials = {
        'username': 'ObiOne777',
        'password': 'Qwerty777$$'
    }
    mock_get_user = aio_patch('api.auth.get_user')
    mock_get_user.return_value = None

    with pytest.raises(HTTPForbidden) as err_403:
        await auth.authenticate_user(conn, **user_credentials)

    assert err_403.value.text == json.dumps({'reason': 'Invalid user credentials.'})
    mock_get_user.assert_awaited_with(conn, username=user_credentials['username'])


async def test_authenticate_user_invalid_password(aio_patch, mocker):
    conn = mocker.Mock()

    user_credentials = {
        'username': 'ObiOne777',
        'password': 'Qwerty777$$'
    }
    mock_get_user = aio_patch('api.auth.get_user')
    mock_conf_password = mocker.patch('api.auth.is_password_confirm')
    mock_conf_password.return_value = False

    with pytest.raises(HTTPForbidden) as err_403:
        await auth.authenticate_user(conn, **user_credentials)

    assert err_403.value.text == json.dumps({'reason': 'Invalid user credentials.'})
    mock_get_user.assert_awaited_with(conn, username=user_credentials['username'])


async def test_authenticate_user_success(aio_patch, mocker):
    conn = mocker.Mock()
    expected_user = mocker.Mock()

    user_credentials = {
        'username': 'ObiOne777',
        'password': 'Qwerty777$$'
    }
    mock_get_user = aio_patch('api.auth.get_user')
    mock_get_user.return_value = expected_user
    mock_conf_password = mocker.patch('api.auth.is_password_confirm')
    mock_conf_password.return_value = True

    result = await auth.authenticate_user(conn, **user_credentials)

    assert result == expected_user
    mock_get_user.assert_awaited_with(conn, username=user_credentials['username']) 