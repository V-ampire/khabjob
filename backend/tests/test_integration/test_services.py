from core.services import vacancies
from core.db.schema import vacancies_table
from core.utils import now_with_tz

from datetime import timedelta
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
        result = await cursor.fetchall()
        
        assert cursor.rowcount == 9
        for vacancy in result:
            assert {
                'name': vacancy.name,
                'source': vacancy.source,
                'source_name': vacancy.source_name,
            } in vacancies_data


async def test_filter_vacancies_without_options_and_default_pagination(aio_engine, create_vacancy):
    expected = [await create_vacancy() for _ in range(3)]
    
    async with aio_engine.acquire() as conn:
        results = await vacancies.filter_vacancies(conn)

    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == len(results)
        assert not 'search_index' in r.keys()
    

async def test_filter_vacancies_pagination(aio_engine, create_vacancy):
    limit = 2
    offset = 5
    expected = [await create_vacancy() for _ in range(offset*2)][offset:offset+limit]

    async with aio_engine.acquire() as conn:
        results = await vacancies.filter_vacancies(conn, limit=limit, offset=offset)

    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == offset * 2
        assert not 'search_index' in r.keys()

    
async def test_filter_vacancies_with_options(aio_engine, create_vacancy):
    expected = [await create_vacancy() for _ in range(6)][0]

    async with aio_engine.acquire() as conn:
        results = await vacancies.filter_vacancies(conn, source=expected['source'])

    assert expected['name'] == results[0]['name']
    assert expected['source'] == results[0]['source']
    assert expected['source_name'] == results[0]['source_name']
    assert results[0]['count'] == len(results)
    assert not 'search_index' in results[0].keys()


async def test_filter_vacancies_with_bool_option(aio_engine, create_vacancy):
    await create_vacancy()
    expected = await create_vacancy(is_published=False)

    async with aio_engine.acquire() as conn:
        result = await vacancies.filter_vacancies(conn, is_published=False)

    assert expected['name'] == result[0]['name']
    assert expected['source'] == result[0]['source']
    assert expected['source_name'] == result[0]['source_name']
    assert not result[0]['is_published']
    assert result[0]['count'] == len(result)
    assert not 'search_index' in result[0].keys()
        

async def test_search_vacancies_by_dates(aio_engine, create_vacancy):
    today = now_with_tz().date()
    vacancy_1 = await create_vacancy(modified_at=today - timedelta(days=6))
    vacancy_2 = await create_vacancy(modified_at=today - timedelta(days=4))
    vacancy_3 = await create_vacancy(modified_at=today - timedelta(days=2))
    vacancy_4 = await create_vacancy(modified_at=today)

    date_from = today - timedelta(days=4)
    expected_from = [vacancy_2, vacancy_3, vacancy_4]
    date_to = today - timedelta(days=2)
    expected_to = [vacancy_1, vacancy_2, vacancy_3]
    expected_from_to = [vacancy_2, vacancy_3]

    async with aio_engine.acquire() as conn:
        results_from = await vacancies.search_vacancies(conn, date_from=date_from)
        results_to = await vacancies.search_vacancies(conn, date_to=date_to)
        results_from_to = await vacancies.search_vacancies(conn, date_from=date_from, date_to=date_to)
    
    assert len(results_from) == len(expected_from)
    for r, e in zip(results_from, expected_from):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == len(expected_from)
        assert not 'search_index' in r.keys()
        assert r['is_published']

    assert len(results_to) == len(expected_to)
    for r, e in zip(results_to, expected_to):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == len(expected_to)
        assert not 'search_index' in r.keys()
        assert r['is_published']

    assert len(results_from_to) == len(expected_from_to)
    for r, e in zip(results_from_to, expected_from_to):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == len(expected_from_to)
        assert not 'search_index' in r.keys()
        assert r['is_published']


async def test_search_vacancies_by_query(aio_engine, create_vacancy):
    expected = await create_vacancy(name='Разработчик аггрегатора вакансий')
    await create_vacancy(name='Грузчик')
    await create_vacancy(name='Продавец')
    await create_vacancy(name='Мастер джедай')

    async with aio_engine.acquire() as conn:
        result = await vacancies.search_vacancies(conn, search_query='разработчик')

    assert expected['name'] == result[0]['name']
    assert expected['source'] == result[0]['source']
    assert expected['source_name'] == result[0]['source_name']
    assert result[0]['is_published']
    assert result[0]['count'] == len(result)
    assert not 'search_index' in result[0].keys()
    

async def test_search_vacancies_by_dates_and_query(aio_engine, create_vacancy):
    today = now_with_tz().date()
    date_from = today - timedelta(days=5)
    date_to = today - timedelta(days=3)
    await create_vacancy(
        modified_at=today - timedelta(days=6),
        name='Кондитер',
    )
    expected = await create_vacancy(
        modified_at=today - timedelta(days=4),
        name='Разработчик аггрегатора вакансий',
    )
    await create_vacancy(
        modified_at=today - timedelta(days=4),
        name='Менеджер самого среднего звена',
    )
    await create_vacancy(
        modified_at=today - timedelta(days=2),
        name='Разработчик на python',
    )

    async with aio_engine.acquire() as conn:
        result = await vacancies.search_vacancies(
            conn, 
            date_from=date_from,
            date_to=date_to,
            search_query='разработчик'
        )

    assert expected['name'] == result[0]['name']
    assert expected['source'] == result[0]['source']
    assert expected['source_name'] == result[0]['source_name']
    assert result[0]['count'] == len(result)
    assert result[0]['is_published']
    assert not 'search_index' in result[0].keys()


async def test_search_vacancies_defaut(aio_engine, create_vacancy):
    expected = [await create_vacancy() for _ in range(3)]
    [await create_vacancy(is_published=False) for _ in range(3)]

    async with aio_engine.acquire() as conn:
        results = await vacancies.search_vacancies(conn)

    assert len(results) == len(expected)
    for r, e in zip(results, expected):
        assert r['name'] == e['name']
        assert r['source'] == e['source']
        assert r['source_name'] == e['source_name']
        assert r['count'] == len(results)
        assert not 'search_index' in r.keys()


