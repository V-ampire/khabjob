from aiohttp import web, PAYLOAD_REGISTRY

import pytest
from unittest.mock import AsyncMock
from typing import Dict, Mapping
from types import MappingProxyType

from api.views.base import BaseView
from api.views import mixins
from api.payloads import JsonPayload
from api.utils import get_pagination_params


class ListView(mixins.ListMixin, mixins.CreateMixin, BaseView):

    handle_filter = AsyncMock()
    handle_search = AsyncMock()
    handle_create = AsyncMock()

class DetailView(mixins.DetailMixin, BaseView):
    handle_detail = AsyncMock()



@pytest.fixture
def api(aiohttp_client, loop):
    app = web.Application()
    app.router.add_view('/list', ListView, name='list')
    app.router.add_view('/list/{id}', DetailView, name='detail')
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return loop.run_until_complete(aiohttp_client(app))


async def test_list_by_search(mocker, api):
    # mock_validate = mocker.patch(
    #     'api.views.mixins.validation_utils.validate_request_query'
    # )
    # mock_validate.return_value = {'search_query': 'Jedi'}

    ListView.search_options = ['search_query']
    ListView.handle_search.return_value = []

    response = await api.get('/list?search_query=Jedi')
    results = await response.json()

    assert response.status == 200
    assert results == {
        'results': []
    }
    # mock_validate.assert_called_with(
    #     ListView.search_validator,
    #     {'search_query': 'Jedi'},
    #     exclude_none=True
    # )
    ListView.handle_search.assert_awaited_with(search_query='Jedi')


async def test_list_by_filter(mocker, api):
    # mock_validate = mocker.patch(
    #     'api.views.mixins.validation_utils.validate_request_query'
    # )
    # mock_validate.return_value = {'source_name': 'khabjob'}

    ListView.handle_filter.return_value = []

    response = await api.get('/list?source_name=khabjob')
    results = await response.json()

    assert response.status == 200
    assert results == {
        'results': []
    }
    # mock_validate.assert_called_with(
    #     ListView.filter_validator,
    #     {'source_name': 'khabjob'},
    #     exclude_none=True
    # )
    ListView.handle_filter.assert_awaited_with(source_name='khabjob')


async def test_list_without_query(api):
    ListView.handle_filter.return_value = []

    response = await api.get('/list')
    results = await response.json()

    assert response.status == 200
    assert results == {
        'results': []
    }
    ListView.handle_filter.assert_awaited_with()


async def test_list_with_pagination(api, views_vacancy_list, mocker):
    # mock_validate = mocker.patch(
    #     'api.views.mixins.validation_utils.validate_request_query'
    # )
    # mock_validate.return_value = {}

    expected_vacancies = views_vacancy_list(3, 3)[4:7]

    ListView.handle_filter.return_value = expected_vacancies

    url = api.app.router['list'].url_for().with_query({
        "limit": 3, "offset": 3
    })

    response = await api.get(url)
    result = await response.json()

    expected = get_pagination_params(
        response.url,
        count=9,
        limit=3,
        offset=3
    )
    expected.update({'results': expected_vacancies})
    
    assert response.status == 200
    assert result == expected
    ListView.handle_filter.assert_awaited_with(limit='3', offset='3')


async def test_detail(api):
    DetailView.handle_detail.return_value = {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58'
    }

    url = api.app.router['detail'].url_for(id='1')

    response = await api.get(url)
    result = await response.json()

    assert response.status == 200
    assert result == {
        'name': 'Jedi Master',
        'source': 'https://jedi-academy.co/vacancies/58'
    }
    DetailView.handle_detail.assert_awaited_with(id='1')


async def test_create_by_json(api):
    data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    ListView.handle_create.return_value = data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, json=data)
    result = await response.json()

    assert response.status == 201
    assert result == data
    ListView.handle_create.assert_awaited_with(**data)


async def test_create_by_form_data(api):
    data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    ListView.handle_create.return_value = data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, data=data)
    result = await response.json()

    assert response.status == 201
    assert result == data
    ListView.handle_create.assert_awaited_with(**data)


async def test_create_by_unsupported_type(api):
    data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    ListView.handle_create.return_value = data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, data=str(data), headers={'Content-Type': 'text/plain'})
    result = await response.json()

    assert response.status == 415
    ListView.handle_create.call_count == 0






