from datetime import datetime
import pytest

from api.utils import get_pagination_params

from config import SELF_SOURCE_NAME


async def test_vacancy_list(api_client, aio_patch, views_vacancy_list):
    expected_vacancies = views_vacancy_list(3, 3)

    mock_filter = aio_patch('api.views.public.Vacancies.handle_filter')
    mock_filter.return_value = expected_vacancies

    url = api_client.app.router['vacancy_public_list'].url_for()
    
    resp = await api_client.get(url)
    result = await resp.json()
    expected = get_pagination_params(
        resp.url,
        count=9,
        limit=20
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == expected
    mock_filter.assert_awaited_with(is_published=True)


async def test_vacancy_list_pagination(api_client, aio_patch, views_vacancy_list):
    expected_vacancies = views_vacancy_list(3, 3)[4:7]

    mock_filter = aio_patch('api.views.public.Vacancies.handle_filter')
    mock_filter.return_value = expected_vacancies

    url = api_client.app.router['vacancy_public_list'].url_for().with_query({
        "limit": 3, "offset": 3
    })
    
    resp = await api_client.get(url)
    result = await resp.json()
    expected = get_pagination_params(
        resp.url,
        count=9,
        limit=3,
        offset=3
    )
    expected.update({'results': expected_vacancies})
    
    assert resp.status == 200
    assert result == expected
    mock_filter.assert_awaited_with(is_published=True)


async def test_vacancy_search(api_client, aio_patch, views_vacancy_list):
    expected_vacancies = views_vacancy_list(3, 3)

    mock_search = aio_patch('api.views.public.Vacancies.handle_search')
    mock_search.return_value = expected_vacancies

    search_query_params = {
        "date_from": '2021-09-01',
        "date_to": '2021-09-04',
        "search_query": 'Jedi Teacher',
        "source_name": 'hh',
    }

    url = api_client.app.router['vacancy_public_list'].url_for().with_query(search_query_params)
    
    resp = await api_client.get(url)
    result = await resp.json()
    expected = get_pagination_params(
        resp.url,
        count=9,
        limit=20,
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == expected
    mock_search.assert_awaited_with(
        date_from=datetime.fromisoformat(search_query_params.pop('date_from')).date(),
        date_to=datetime.fromisoformat(search_query_params.pop('date_to')).date(),
        **search_query_params
    )


async def test_vacancy_detail_get(api_client, aio_patch, fake_vacancies_data):
    expected = fake_vacancies_data(1, 1)[0]
    expected.update({'id': 1})

    mock_filter = aio_patch('api.views.public.Vacancies.handle_filter')
    mock_filter.return_value = [expected]
    
    url = api_client.app.router['vacancy_public_detail'].url_for(id='1')

    resp = await api_client.get(url)
    result = await resp.json()

    assert resp.status == 200
    assert result == expected
    mock_filter.assert_awaited_with(is_published=True, id=1)


async def test_vacancy_detail_get_404(api_client, aio_patch):
    mock_filter = aio_patch('api.views.public.Vacancies.handle_filter')
    mock_filter.return_value = []

    url = api_client.app.router['vacancy_public_detail'].url_for(id='1')

    resp = await api_client.get(url)
    result = await resp.json()

    assert resp.status == 404
    assert result == {}


async def test_vacancy_post_valid(api_client, aio_patch):
    data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    expected_create_data = data.copy()
    expected_create_data.update({
        'is_published': False,
        'source_name': SELF_SOURCE_NAME,
        'source': None
    })
    mock_create = aio_patch('api.views.public.Vacancies.handle_create')
    mock_create.return_value = expected_create_data

    url = api_client.app.router['vacancy_public_list'].url_for()

    resp = await api_client.post(url, json=data)
    result = await resp.json()

    assert resp.status == 201
    assert result == expected_create_data
    mock_create.assert_awaited_with(**expected_create_data)


async def test_vacancy_post_invalid(api_client, aio_patch):
    data = {
        'name': 'Jedi Master',
    }

    url = api_client.app.router['vacancy_public_list'].url_for()

    resp = await api_client.post(url, json=data)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'__root__': 'Vacancy must have source or description.'}
