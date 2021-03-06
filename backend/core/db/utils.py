"""
Utils to operate with database.
"""
from alembic.config import Config
from alembic.command import upgrade

from psycopg2.errors import UniqueViolation

from sqlalchemy import create_engine, Table, Column
from sqlalchemy.dialects.postgresql import TSVECTOR

import re
from typing import Dict, List

from config import POSTGRES_CONFIG, BASE_DIR


def get_postgres_dsn(**options) -> str:
    """
    Return DSN for postgresql from options,
    if options is not passed then default option takes from config.
    """
    return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=options.get('user', POSTGRES_CONFIG['POSTGRES_USER']),
        password=options.get('password', POSTGRES_CONFIG['POSTGRES_PASSWORD']),
        host=options.get('host', POSTGRES_CONFIG['POSTGRES_HOST']),
        port=options.get('port', POSTGRES_CONFIG['POSTGRES_PORT']),
        database=options.get('database', POSTGRES_CONFIG['POSTGRES_DB'])
    )


def except_tsvector_columns(table: Table) -> List[Column]:
    """Return table columns except postgresql tsvector columns."""
    return list(filter(lambda c: not isinstance(c.type, TSVECTOR), table.c))


def parse_unique_violation_fields(error: UniqueViolation) -> Dict[str, str]:
    """Parse UniqueViolation error and return field that did not passed constraint."""
    field_str_list = re.findall(r'\(.+\)=\(.+\)', error.pgerror)
    # Generate dict {'field_name': 'value'} from strings
    return {
        k.strip('()'): v.strip('()') for k,v in [
            elem.split(sep='=') for elem in field_str_list
        ]
    }


def create_db(**options) -> None:
    """Create database."""
    db_name = options.get('database', POSTGRES_CONFIG['POSTGRES_DB'])
    db_user = options.get('user', POSTGRES_CONFIG['POSTGRES_USER'])

    options.update({'database': db_user}) # connect to default user db
    dsn = get_postgres_dsn(**options)

    engine = create_engine(dsn, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    try:
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
        conn.execute('CREATE DATABASE %s ENCODING "UTF8"' % db_name)
    finally:
        conn.close()


def drop_db(**options) -> None:
    """Drop database."""
    db_name = options.get('database', POSTGRES_CONFIG['POSTGRES_DB'])
    db_user = options.get('user', POSTGRES_CONFIG['POSTGRES_USER'])

    options.update({'database': db_user})  # connect to default user db
    dsn = get_postgres_dsn(**options)

    engine = create_engine(dsn, isolation_level='AUTOCOMMIT')
    conn = engine.connect()
    try:
        conn.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '%s'
                AND pid <> pg_backend_pid();""" % db_name)  # close all db sessions
        conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
    finally:
        conn.close()


def apply_migrations():
    """Apply database migrations."""
    alembic_config = Config(str(BASE_DIR.joinpath('alembic.ini')))
    alembic_config.set_main_option('sqlalchemy.url', get_postgres_dsn())
    upgrade(alembic_config, 'head')
