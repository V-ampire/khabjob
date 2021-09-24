from aiohttp.web import Application
from aiohttp.test_utils import make_mocked_request

from alembic.config import Config
from alembic.command import upgrade

from aiopg.sa import create_engine

from sqlalchemy import insert

import jwt

import pytest
import os
from unittest import mock

from api.app import init_app

from core.db import utils
from core.db.schema import vacancies_table, users_table
from core.services.auth import hash_password

from config import POSTGRES_CONFIG, BASE_DIR, AUTH_CONFIG


@pytest.fixture(autouse=True, scope='session')
def mock_config_db_name():
    """Override database name on test name."""
    test_db_name = '{0}_test'.format(POSTGRES_CONFIG['POSTGRES_DB'])
    with mock.patch.dict(POSTGRES_CONFIG, {"POSTGRES_DB": test_db_name}):
        yield


@pytest.fixture
def postgres():
    """
    Create test postgres database.

    Return dsn for created database.    
    """
    utils.create_db()
    try:
        yield utils.get_postgres_dsn()
    finally:
        utils.drop_db()


@pytest.fixture
def migrated_postgres(postgres):
    """Apply migrations for test db."""
    alembic_config = Config(str(BASE_DIR.joinpath('alembic.ini')))
    alembic_config.set_main_option("sqlalchemy.url", postgres)
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
async def aio_engine(loop, migrated_postgres):
    """Return async engine for test database."""
    engine = await create_engine(migrated_postgres)
    try:
        yield engine
    finally:
        engine.close()
        await engine.wait_closed()


@pytest.fixture
def fake_vacancies_data(faker):
    """Return data fabric to generate fake vacancies data."""
    def gen_vacancies(sources_count=1, vacancies_count=3):
        vacancies_data = []
        for s in range(sources_count):
            source_name = faker.company()
            for v in range(vacancies_count):
                vacancies_data.append({
                    'source': faker.uri(),
                    'source_name': source_name[:16],
                    'name': faker.job()
                })
        return vacancies_data
    return gen_vacancies


@pytest.fixture
async def create_vacancy_return_data(loop, aio_engine, fake_vacancies_data):
    async def create(**options):
        vacancy_data = fake_vacancies_data(1, 1)[0]
        vacancy_data.update(**options)
        async with aio_engine.acquire() as conn:
            stmt = insert(vacancies_table).values(**vacancy_data)
            await conn.execute(stmt)
        return vacancy_data
    return create


@pytest.fixture
async def create_vacancy(loop, aio_engine, fake_vacancies_data):
    async def create(**options):
        vacancy_data = fake_vacancies_data(1, 1)[0]
        vacancy_data.update(**options)
        async with aio_engine.acquire() as conn:
            stmt = insert(vacancies_table).values(**vacancy_data).returning(vacancies_table)
            result = await conn.execute(stmt)
            return await result.fetchone()
    return create


@pytest.fixture
def fake_user_data(faker):
    return {
        'username': faker.user_name(),
        'password': faker.password()
    }


@pytest.fixture
async def create_user(aio_engine, fake_user_data):
    async def create(**user_data):
        create_data = fake_user_data
        create_data.update(user_data)
        password_hash = hash_password(create_data.pop('password'))
        async with aio_engine.acquire() as conn:
            stmt = insert(users_table).values(
                password_hash=password_hash, **create_data
            ).returning(users_table)
            result = await conn.execute(stmt)
            return await result.fetchone()
    return create


@pytest.fixture
def aio_patch(mocker):
    """Return function which patch async functions."""
    def a_patch(target):
        """Patch function and return AsyncMock."""
        async_mock = mock.AsyncMock()
        return mocker.patch(target, new_callable=mock.AsyncMock)
    return a_patch


@pytest.fixture
def api_client(loop, aiohttp_client, migrated_postgres):
    app = init_app()
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


@pytest.fixture
def jwt_request(aio_engine, make_jwt_token, migrated_postgres):
    def make_request(jwt_payload={}):
        app = Application()
        app['db'] = aio_engine
        token = make_jwt_token(jwt_payload)
        headers = {
            AUTH_CONFIG['JWT_HEADER_NAME']: '{0} {1}'.format(AUTH_CONFIG['JWT_AUTH_SCHEME'], token)
        }
        return (make_mocked_request('GET', '/', headers=headers, app=app), token)
    return make_request