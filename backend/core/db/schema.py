from core.utils import now_with_tz

from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Date, Boolean
)


metadata = MetaData()


vacancies_table = Table(
    'vacancies',
    metadata,
    Column('vacancy_id', Integer, primary_key=True),
    Column('created_at', Date, default=now_with_tz),
    Column('modified_at', Date, default=now_with_tz, onupdate=now_with_tz),
    Column('name', String(128), nullable=False),
    Column('source', String(128), nullable=False, unique=True),
    Column('source_name', String(16), nullable=False),
    Column('is_published', Boolean, server_default='f', nullable=False)
)