from aiohttp import web

from aiopg.sa import SAConnection

import jwt

from datetime import datetime
from dataclasses import dataclass
import json
from typing import Optional, Tuple, Any

from core.services.auth import (
    get_user,
    is_password_confirm,
    is_token_blacklisted
) 

from config import AUTH_CONFIG


@dataclass
class User:
    """User representation for storing in request."""

    id: int
    username: str
    password_hash: str


class TokenError(Exception):
    """Raise if token is invalid."""
    
    def __init__(self, message, **kwargs):
        self.message = message
        super().__init__(self, message, **kwargs)


async def authenticate(request: web.Request) -> Tuple[User, str, None]:
    """
    Authenticate request by jwt token.

    If user authenticated return tuple (user, token),
    where user is instance of User dataclass, else return (None, None),
    or raise 403 HTTPForbidden.
    """
    raw_token = authenticate_headers(request)

    if raw_token is None:
        return (None, None)
    
    payload = jwt.decode(
        raw_token, 
        AUTH_CONFIG['SECRET_KEY'],
        algorithms=[AUTH_CONFIG['ALGORITHM']]
    )

    user_id = payload.get('user_id', None)
    jwt_exp = payload.get('jwt_exp', None)

    try:
        check_jwt_token_expired(jwt_exp)
        async with request.app['db'].acquire() as conn:
            await check_token_blacklist(conn, raw_token)
            user = await get_jwt_token_user(conn, user_id)
    except TokenError as error:
        raise web.HTTPForbidden(
            text=json.dumps({'reason': error.message}),
            content_type='application/json',
        )

    return (user, raw_token)


def authenticate_headers(request: web.Request) -> Optional[str]:
    """
    Extract jwt token from authorization header.

    If no auth header or token return None.
    Raise HTTPForbidden 403 if token has invalid format.
    """
    header_body = request.headers.get(AUTH_CONFIG['JWT_HEADER_NAME'], None)

    if header_body is None:
        # No AUTHORIZATION header
        return None

    parts = header_body.split()

    if len(parts) == 0:
        # Empty AUTHORIZATION header sent
        return None

    if parts[0] != AUTH_CONFIG['JWT_AUTH_SCHEME']:
        # Invalid auth scheme
        return None

    if len(parts) != 2:
        raise web.HTTPForbidden(
            text=json.dumps({'reason': 'Bad authorization header.'}),
            content_type='application/json',
        )

    return parts[1]


def check_jwt_token_expired(jwt_exp: Any) -> bool:
    """
    Check whether lifetime token has expired.
    
    If token is expired or token lifetime format is invalid raise TokenError.
    """
    if not isinstance(jwt_exp, str):
        raise TokenError('Invalid token expired datetime format.')
    try:
        expired_time = datetime.fromisoformat(jwt_exp)
    except ValueError:
        raise TokenError('Invalid token expired datetime format.')
    
    current_time = datetime.utcnow()

    if current_time >= expired_time:
        raise TokenError('Token has expired.')


async def get_jwt_token_user(conn: SAConnection, user_id: Any) -> User:
    """
    Check does user exist, if user_id is invalid raise TokenError.
    
    If user exists return User.
    """
    if not isinstance(user_id, int):
        raise TokenError('Invalid jwt token payload.')

    user_db = await get_user(conn, id=user_id)
    if user_db is None:
        raise TokenError('Access authenticated only.')

    return User(
        id=user_db.id,
        username=user_db.username,
        password_hash=user_db.password_hash
    )


async def check_token_blacklist(conn: SAConnection, token: str):
    """Check that token not in blacklist."""
    if await is_token_blacklisted(conn, token):
        raise TokenError('Token is invalid.')


async def check_authentication(request: web.Request) -> web.Request:
    """
    Check request authentication.

    If authentication is successed, 
    store in request user and token via request['user'], request['token'].
    Else raise 403 Forbidden.
    """
    user, token = await authenticate(request)
    request['user'] = user
    request['token'] = token
    return request


def make_jwt_token_for_user(user_id):
    """Make jwt token with payload with user_id and token expired."""
    lifetime = AUTH_CONFIG['JWT_LIFETIME']
    jwt_exp_dt = datetime.utcnow() + lifetime
    
    payload = {
        'user_id': user_id,
        'jwt_exp': jwt_exp_dt.isoformat() 
    }

    return jwt.encode(
        payload, 
        AUTH_CONFIG['SECRET_KEY'],
        algorithm=AUTH_CONFIG['ALGORITHM']
    )


async def authenticate_user(conn: SAConnection, **user_credentials) -> User:
    """
    Authenticate user by credentials.

    If success return User, else raise HTTPForbidden 403.
    """
    password = user_credentials.pop('password')
    user = await get_user(conn, **user_credentials)

    if user is None or not is_password_confirm(password, user.password_hash):
        raise web.HTTPForbidden(
            text=json.dumps({'reason': 'Invalid user credentials.'}),
            content_type='application/json',
        )
    
    return user
