"""
Database schema description.
"""
from sqlalchemy import (
    MetaData, Table, Column, Computed,
    Integer, String, Date, Boolean, Index
)
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TSVECTOR

from datetime import datetime

metadata = MetaData()


vacancies_table = Table(
    'vacancies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('created_at', Date, default=datetime.utcnow().date()),
    Column(
        'modified_at',
        Date,
        default=datetime.utcnow().date(),
        onupdate=datetime.utcnow().date()
    ),
    Column('name', String(264), nullable=False),
    Column('source', String(264), nullable=True, unique=True),
    Column('source_name', String(16), nullable=False),
    Column('description', String(1024), nullable=True),
    Column('is_published', Boolean, server_default='t', nullable=False),
    Column('search_index', TSVECTOR, Computed(text("to_tsvector('russian', name)"))),
    Index('vacancies_idx_column', 'search_index', postgresql_using='gin')
)


users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('password_hash', String(256), nullable=False, unique=True)
)


jwt_blacklist_table = Table(
    'jwt_blacklist',
    metadata,
    Column('token', String(256), primary_key=True),
)
