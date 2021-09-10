import json
import pytest

from api.auth import make_jwt_token_for_user
from api.utils import get_pagination_params
from api.payloads import dumps

from core.services.vacancies import filter_vacancies, search_vacancies


@pytest.fixture
async def auth_headers(create_user):
    user = await create_user()
    token = make_jwt_token_for_user(user.id)
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    return (user, headers)
    



async def test_unauthorized_requests_private_views(api_client):
    list_url = api_client.app.router['vacancy_private_list'].url_for()
    detail_url = api_client.app.router['vacancy_private_detail'].url_for(id='1')

    request_data = {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58',
        'source_name': 'jedi-academy'
    }

    list_resp = await api_client.get(list_url)
    detail_resp = await api_client.get(detail_url)
    create_resp = await api_client.post(detail_url, json=request_data)
    update_resp = await api_client.put(detail_url, json=request_data)
    part_update_resp = await api_client.patch(detail_url, json=request_data)
    delete_resp = await api_client.delete(detail_url)
    delete_list_resp = await api_client.delete(list_url)

    assert list_resp.status == 403
    assert detail_resp.status == 403
    assert create_resp.status == 403
    assert list_resp.status == 403
    assert update_resp.status == 403
    assert part_update_resp.status == 403
    assert delete_resp.status == 403
    assert delete_list_resp.status == 403


async def test_private_vacancy_list_resource(api_client, auth_headers, create_vacancy, aio_engine):
    user, headers = auth_headers

    [await create_vacancy() for i in range(5)]
    [await create_vacancy(is_published=False) for i in range(5)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn)

    url = api_client.app.router['vacancy_private_list'].url_for()
    
    resp = await api_client.get(url, headers=headers)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=10,
        limit=20 # Default list view limit
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_private_vacancy_list_resource_with_query(api_client, create_vacancy, aio_engine, auth_headers):
    user, headers = auth_headers

    [await create_vacancy() for i in range(3)]
    [await create_vacancy(source_name='hh') for i in range(3)]
    [await create_vacancy(is_published=False, source_name='vk') for i in range(5)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn, is_published=False, source_name='vk')

    url = api_client.app.router['vacancy_private_list'].url_for().with_query({
        'source_name': 'vk',
        'is_published': 'false'
    })
    
    resp = await api_client.get(url, headers=headers)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=5,
        limit=20 # Default list view limit
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_private_vacancy_list_resource_with_pagination(api_client, create_vacancy, aio_engine, auth_headers):
    user, headers = auth_headers

    [await create_vacancy() for i in range(10)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn, limit=3, offset=3)

    url = api_client.app.router['vacancy_private_list'].url_for().with_query({
        'limit': '3',
        'offset': '3'
    })

    resp = await api_client.get(url, headers=headers)
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


async def test_private_vacancy_list_resource_by_search(api_client, create_vacancy, aio_engine, auth_headers):
    user, headers = auth_headers

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

    url = api_client.app.router['vacancy_private_list'].url_for().with_query({
        'search_query': 'Jedi',
        'date_from': expected_date_from,
        'date_to': expected_date_to,
        'is_published': 'false' # invalid option
    })

    resp = await api_client.get(url, headers=headers)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=1,
        limit=20,
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))


async def test_private_detail_vacancy_resource(api_client, create_vacancy, aio_engine, auth_headers):
    user, headers = auth_headers

    await create_vacancy()
    await create_vacancy(is_published=False)

    url_id_1 = api_client.app.router['vacancy_private_detail'].url_for(id='1')
    url_id_2 = api_client.app.router['vacancy_private_detail'].url_for(id='2')

    async with aio_engine.acquire() as conn:
        expected_vacancies_1 = await filter_vacancies(conn, id=1)
        expected_vacancies_2 = await filter_vacancies(conn, id=2)

    resp_id_1 = await api_client.get(url_id_1, headers=headers)
    result_id_1 = await resp_id_1.json()
    resp_id_2 = await api_client.get(url_id_2, headers=headers)
    result_id_2 = await resp_id_2.json()

    expected_1 = json.loads(dumps(expected_vacancies_1[0]))
    expected_2 = json.loads(dumps(expected_vacancies_2[0]))
    
    assert resp_id_1.status == 200   
    assert result_id_1 == json.loads(dumps(expected_1))
    assert resp_id_2.status == 200
    assert result_id_2 == json.loads(dumps(expected_2))


async def test_private_detail_vacancy_resource_invalid_id(api_client, auth_headers):
    user, headers = auth_headers

    url = api_client.app.router['vacancy_private_detail'].url_for(id='abc')
    resp = await api_client.get(url, headers=headers)

    assert resp.status == 404


async def test_private_create_vacancy_resource(api_client, aio_engine, auth_headers):
    user, headers = auth_headers

    url = api_client.app.router['vacancy_private_list'].url_for()

    create_data = {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58',
        'source_name': 'jedi-academy',
        'is_published': True

    }

    resp = await api_client.post(url, json=create_data, headers=headers)
    result = await resp.json()

    async with aio_engine.acquire() as conn:
        expected_result = await filter_vacancies(
            conn, 
            source_name='jedi-academy',
            is_published=True, 
            source=create_data['source']
        )
    expected = json.loads(dumps(expected_result[0]))
    expected.pop('count')

    assert resp.status == 201
    assert result == expected


async def test_private_create_vacancy_resource_already_exists(api_client, create_vacancy, auth_headers):
    user, headers = auth_headers

    existed = await create_vacancy()

    url = api_client.app.router['vacancy_private_list'].url_for()

    create_data = {
        'name': existed['name'],
        'source': existed['source'],
        'source_name': 'jedi-academy',
        'is_published': True
    }

    resp = await api_client.post(url, json=create_data, headers=headers)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'source': existed['source']}


async def test_private_full_update_vacancy_resource_without_all_fields(api_client, create_vacancy, auth_headers):
    user, headers = auth_headers

    vacancy = await create_vacancy()

    url = api_client.app.router['vacancy_private_detail'].url_for(id='1')

    partial_update_data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob'
    }

    resp = await api_client.put(url, json=partial_update_data, headers=headers)
    result = await resp.json()

    assert resp.status == 400
    assert result == {
        'source': 'field required', 
        'description': 'field required', 
        'is_published': 'field required', 
    }


async def test_private_full_update_vacancy_resource_with_all_fields(api_client, create_vacancy, auth_headers, aio_engine):
    user, headers = auth_headers

    vacancy = await create_vacancy()

    url = api_client.app.router['vacancy_private_detail'].url_for(id='1')

    update_data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob',
        'source': 'https://jedi-academy.co/vacancies/58', 
        'description': 'We are looking for high skilled jedi master', 
        'is_published': False,
    }

    resp = await api_client.put(url, json=update_data, headers=headers)
    result = await resp.json()

    async with aio_engine.acquire() as conn:
        expected_vacancy = await filter_vacancies(
            conn, 
            id=1,
            is_published=False
        )

    expected = json.loads(dumps(expected_vacancy[0]))
    expected.pop('count')

    assert resp.status == 200
    assert result == expected


async def test_private_partial_update_vacancy_resource(api_client, create_vacancy, auth_headers, aio_engine):
    user, headers = auth_headers

    vacancy = await create_vacancy()

    url = api_client.app.router['vacancy_private_detail'].url_for(id='1')

    partial_update_data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob'
    }

    resp = await api_client.patch(url, json=partial_update_data, headers=headers)
    result = await resp.json()

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(
            conn, 
            id=1,
        )

    expected = json.loads(dumps(expected_vacancies[0]))
    expected.pop('count')

    assert resp.status == 200
    assert result == expected
    assert expected_vacancies[0].name == 'Jedi Master'
    assert expected_vacancies[0].source_name == 'khabjob'


async def test_private_delete_vacancy(api_client, create_vacancy, auth_headers, aio_engine):
    user, headers = auth_headers

    vacancy = await create_vacancy()

    url = api_client.app.router['vacancy_private_detail'].url_for(id='1')

    resp = await api_client.delete(url, headers=headers)

    async with aio_engine.acquire() as conn:
        expected = await filter_vacancies(
            conn, 
            id=1,
        )

    assert resp.status == 204
    assert len(expected) == 0
