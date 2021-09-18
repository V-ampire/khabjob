import json
import pytest

from api.utils import get_pagination_params
from api.payloads import dumps

from core.services.vacancies import filter_vacancies, search_vacancies

from config import SELF_SOURCE_NAME


async def test_vacancy_list_resource(api_client, create_vacancy, aio_engine):
    [await create_vacancy() for i in range(5)]
    [await create_vacancy(is_published=False) for i in range(5)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn, is_published=True)

    url = api_client.app.router['vacancy_public_list'].url_for()
    
    resp = await api_client.get(url)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=5,
        limit=20 # Default list view limit
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_vacancy_list_resource_with_query(api_client, create_vacancy, aio_engine):
    expected_modified_at = '2021-05-04'

    [await create_vacancy() for i in range(3)]
    [await create_vacancy(source_name='hh') for i in range(3)]
    [await create_vacancy(is_published=False) for i in range(5)]
    [await create_vacancy(modified_at=expected_modified_at) for i in range(2)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(
            conn, is_published=True, modified_at=expected_modified_at
        )

    url = api_client.app.router['vacancy_public_list'].url_for().with_query({
        'modified_at': expected_modified_at,
        'is_published': 'false' # invalid option
    })
    
    resp = await api_client.get(url)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=2,
        limit=20 # Default list view limit
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_vacancy_list_resource_with_pagination(api_client, create_vacancy, aio_engine):
    [await create_vacancy() for i in range(10)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn, is_published=True, limit=3, offset=3)

    url = api_client.app.router['vacancy_public_list'].url_for().with_query({
        'limit': '3',
        'offset': '3'
    })

    resp = await api_client.get(url)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=10,
        limit=3,
        offset=3
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_vacancy_list_resource_by_search(api_client, create_vacancy, aio_engine):
    expected_name = 'Jedi Master'
    expected_date_from = '2021-05-04'
    expected_date_to = '2021-06-05'

    [await create_vacancy(
        created_at=expected_date_from, 
        modified_at=expected_date_from
    ) for i in range(5)]
    await create_vacancy(
        name='Jedi Master',
        created_at='2021-06-01',
        modified_at='2021-06-01',
    )
    await create_vacancy(name='Jedi Master')

    async with aio_engine.acquire() as conn:
        expected_vacancies = await search_vacancies(
            conn,
            search_query='Jedi',
            date_from = expected_date_from,
            date_to = expected_date_to
        )

    url = api_client.app.router['search_vacancies'].url_for().with_query({
        'search_query': 'Jedi',
        'date_from': expected_date_from,
        'date_to': expected_date_to,
        'is_published': 'false' # invalid option
    })

    resp = await api_client.get(url)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=1,
        limit=20,
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_detail_vacancy_resource(api_client, create_vacancy, aio_engine):
    await create_vacancy()
    await create_vacancy(is_published=False)

    url_id_1 = api_client.app.router['vacancy_public_detail'].url_for(id='1')
    url_id_2 = api_client.app.router['vacancy_public_detail'].url_for(id='2')

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn, id=1)

    resp_id_1 = await api_client.get(url_id_1)
    result_id_1 = await resp_id_1.json()
    resp_id_2 = await api_client.get(url_id_2)

    expected = json.loads(dumps(expected_vacancies[0]))
    
    assert resp_id_1.status == 200   
    assert result_id_1 == json.loads(dumps(expected))
    assert resp_id_2.status == 404


async def test_detail_vacancy_resource_invalid_id(api_client):
    url = api_client.app.router['vacancy_public_detail'].url_for(id='abc')
    resp = await api_client.get(url)

    assert resp.status == 404


async def test_create_vacancy_resource(api_client, aio_engine):
    url = api_client.app.router['vacancy_public_list'].url_for()

    create_data = {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58',
        'source_name': 'jedi-academy'
    }

    resp = await api_client.post(url, json=create_data)
    result = await resp.json()

    async with aio_engine.acquire() as conn:
        expected_result = await filter_vacancies(
            conn, 
            source_name='khabjob', # Default source_name for public added
            is_published=False, 
            source=create_data['source']
        )
    expected = json.loads(dumps(expected_result[0]))
    expected.pop('count')

    assert resp.status == 201
    assert result == expected


async def test_create_vacancy_resource_already_exists(api_client, create_vacancy):
    existed = await create_vacancy()

    url = api_client.app.router['vacancy_public_list'].url_for()

    create_data = {
        'name': existed['name'],
        'source': existed['source'],
        'source_name': 'jedi-academy'
    }

    resp = await api_client.post(url, json=create_data)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'source': existed['source']}


async def test_create_vacancy_resource_publihed(api_client):
    url = api_client.app.router['vacancy_public_list'].url_for()

    create_data = {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58',
        'source_name': 'jedi-academy',
        'is_publihsed': True
    }

    resp = await api_client.post(url, json=create_data)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'is_publihsed': 'extra fields not permitted'}


async def test_create_vacancy_resource_withou_source_and_description(api_client):
    url = api_client.app.router['vacancy_public_list'].url_for()

    create_data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob'
    }

    resp = await api_client.post(url, json=create_data)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'__root__': 'Vacancy must have source or description.'}
