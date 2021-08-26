from core.services import vacancies
from core.db.schema import vacancies_table

from sqlalchemy import select


async def test_create_vacancy(aio_engine, fake_vacancies_data):
    vacancy_data = fake_vacancies_data(1, 1)[0]

    async with aio_engine.acquire() as conn:
        await vacancies.create_vacancy(conn, **vacancy_data)

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(vacancies_table).where(vacancies_table.c.source == vacancy_data['source'])
        )
        result_vacancy = await cursor.fetchone()
        
        assert cursor.rowcount == 1
        assert result_vacancy['name'] == vacancy_data['name']
        assert result_vacancy['source'] == vacancy_data['source']
        assert result_vacancy['source_name'] == vacancy_data['source_name']


async def test_create_vacancy_batch(aio_engine, fake_vacancies_data):
    vacancies_data = fake_vacancies_data(3, 3)

    async with aio_engine.acquire() as conn:
        await vacancies.create_vacancy_batch(conn, vacancies_data)

    async with aio_engine.acquire() as conn:
        cursor = await conn.execute(
            select(vacancies_table)
        )
        result_vacancies = await cursor.fetchall()
        
        assert cursor.rowcount == 9
        for vacancy in result_vacancies:
            assert {
                'name': vacancy.name,
                'source': vacancy.source,
                'source_name': vacancy.source_name,
            } in vacancies_data
