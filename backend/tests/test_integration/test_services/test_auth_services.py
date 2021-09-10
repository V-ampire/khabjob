from sqlalchemy import select, insert

import jwt

import pytest

from core.db.schema import users_table, jwt_blacklist_table
from core.services import auth


async def test_create_user(aio_engine):
    user_data = {
        'username': 'Joda777',
        'password': 'maytheforcebewithyou'
    }

    async with aio_engine.acquire() as conn:
        user = await auth.create_user(conn, **user_data)

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(users_table).filter_by(username=user_data['username'])
        )
        result = await cursor.fetchone()

    assert result == user
    assert user.username == user_data['username']
    assert auth.is_password_confirm(user_data['password'], user.password_hash)


async def test_get_user(aio_engine, create_user):
    expected = await create_user()
    async with aio_engine.acquire() as conn:
        result = await auth.get_user(conn, id=expected.id)

    assert result == expected


async def test_get_user_not_exists(aio_engine):
    async with aio_engine.acquire() as conn:
        result = await auth.get_user(conn, id=1)

    assert result is None


async def test_blacklist_token(aio_engine, make_jwt_token):
    expected_token = make_jwt_token({'user_id': 1})

    async with aio_engine.acquire() as conn:
        blacklist_row = await auth.blacklist_token(conn, expected_token)

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(jwt_blacklist_table).filter_by(token=expected_token)
        )
        result = await cursor.fetchone()

    assert blacklist_row.token == expected_token
    assert result == blacklist_row
    

async def test_is_token_blacklisted_true(aio_engine, make_jwt_token):
    expected_token = make_jwt_token({'user_id': 1})

    async with aio_engine.acquire() as conn:
        stmt = insert(jwt_blacklist_table).values(token=expected_token)
        await conn.execute(stmt)

    async with aio_engine.acquire() as conn:
        result = await auth.is_token_blacklisted(conn, expected_token)

    assert result


async def test_is_token_blacklisted_false(aio_engine, make_jwt_token):
    expected_token = make_jwt_token({'user_id': 1})

    async with aio_engine.acquire() as conn:
        result = await auth.is_token_blacklisted(conn, expected_token)

    assert not result


async def test_update_user_without_password(aio_engine, create_user):
    user = await create_user()

    async with aio_engine.acquire() as conn:
        await auth.update_user(conn, user.id, username='New_cool_username')

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(users_table).filter_by(id=user.id)
        )
        result = await cursor.fetchone()

    assert result.username == 'New_cool_username'


async def test_update_user_with_password(aio_engine, create_user):
    user = await create_user()

    async with aio_engine.acquire() as conn:
        await auth.update_user(conn, user.id, password='More_strength_pswd')

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(users_table).filter_by(id=user.id)
        )
        result = await cursor.fetchone()

    assert auth.is_password_confirm('More_strength_pswd', result.password_hash)