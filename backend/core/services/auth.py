from aiopg.sa import SAConnection
from aiopg.sa.result import RowProxy

from sqlalchemy import select, insert

import hashlib
from typing import Optional

from core.db.schema import users_table, jwt_blacklist_table

from config import AUTH_CONFIG


async def create_user(conn: SAConnection, username: str, password: str) -> RowProxy:
    password_hash = hash_password(password)

    stmt =  insert(users_table).values(
        username=username,
        password_hash=password_hash
    ).returning(users_table)

    result = await conn.execute(stmt)
    return await result.first()


async def get_user(conn: SAConnection, **user_data) -> Optional[RowProxy]:
    """Return user from database."""

    stmt = select(users_table).filter_by(**user_data)

    result = await conn.execute(stmt)
    return await result.first()


def hash_password(password: str, salt: Optional[str]=None) -> str:
    """Turn a plain-text password into a hash for database storage."""
    if salt is None:
        salt = AUTH_CONFIG['SECRET_KEY']
    bytes_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        320000
    )
    return bytes_hash.hex()


def check_password(password: str, password_hash: str, salt: Optional[str]=None) -> bool:
    """Compare password with calculated hash for this password."""
    return password_hash == hash_password(password, salt=salt)


async def blacklist_token(conn: SAConnection, token: str) -> RowProxy:
    """Add token to blacklist."""
    stmt = insert(jwt_blacklist_table).values(token=token).returning(jwt_blacklist_table.c.token)
    result = await conn.execute(stmt)
    return await result.first()


async def is_token_blacklisted(conn, token: str) -> bool:
    """Check whether token in blacklist."""
    stmt = select(jwt_blacklist_table).filter_by(token=token)
    result = await conn.execute(stmt)
    return await result.first()