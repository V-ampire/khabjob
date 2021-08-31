import pytest
import os
from unittest import mock

from alembic.config import Config
from alembic.command import upgrade
from aiopg.sa import create_engine
from sqlalchemy import insert

from core.db import utils
from core.db.schema import vacancies_table
from config import POSTGRES_CONFIG, BASE_DIR


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
async def create_vacancy(loop, aio_engine, fake_vacancies_data):
    async def create(**options):
        vacancy_data = fake_vacancies_data(1, 1)[0]
        vacancy_data.update(**options)
        async with aio_engine.acquire() as conn:
            stmt = insert(vacancies_table).values(**vacancy_data)
            await conn.execute(stmt)
        return vacancy_data
    return create


@pytest.fixture
def aio_patch(mocker):
    """Return function which patcj async functions."""
    def a_patch(target):
        """Patch function and return AsyncMock."""
        async_mock = mock.AsyncMock()
        return mocker.patch(target, new_callable=mock.AsyncMock)
    return a_patch