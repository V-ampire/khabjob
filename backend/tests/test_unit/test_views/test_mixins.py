from aiohttp import web, PAYLOAD_REGISTRY

import pytest
from unittest.mock import AsyncMock, Mock
from typing import Dict, Mapping
from types import MappingProxyType

from api.views.base import BaseView
from api.views import mixins
from api.payloads import JsonPayload
from api.utils import get_pagination_params


class ListView(mixins.ListMixin, mixins.CreateMixin, BaseView):

    lookup_field = 'id'

    filter_by = AsyncMock()
    search = AsyncMock()
    create = AsyncMock()

    validator_class = Mock()

class DetailView(
    mixins.DetailMixin, 
    mixins.UpdateMixin, 
    mixins.DeleteMixin, 
    BaseView
):

    lookup_field = 'id'

    detail = AsyncMock()
    update = AsyncMock()
    partial_update = AsyncMock()
    delete = AsyncMock()

    validator_class = Mock()


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
    ListView.search.return_value = []

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
    ListView.search.assert_awaited_with(search_query='Jedi')


async def test_list_by_filter(mocker, api):
    # mock_validate = mocker.patch(
    #     'api.views.mixins.validation_utils.validate_request_query'
    # )
    # mock_validate.return_value = {'source_name': 'khabjob'}

    ListView.filter_by.return_value = []

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
    ListView.filter_by.assert_awaited_with(source_name='khabjob')


async def test_list_without_query(api):
    ListView.filter_by.return_value = []

    response = await api.get('/list')
    results = await response.json()

    assert response.status == 200
    assert results == {
        'results': []
    }
    ListView.filter_by.assert_awaited_with()


async def test_list_with_pagination(api, views_vacancy_list, mocker):
    # mock_validate = mocker.patch(
    #     'api.views.mixins.validation_utils.validate_request_query'
    # )
    # mock_validate.return_value = {}

    expected_vacancies = views_vacancy_list(3, 3)[4:7]

    ListView.filter_by.return_value = expected_vacancies

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
    ListView.filter_by.assert_awaited_with(limit='3', offset='3')


async def test_detail_mixin(api):
    DetailView.detail.return_value = {
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
    DetailView.detail.assert_awaited_with('1')


async def test_create_by_json(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    post_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    mock_validate.return_value = post_data
    ListView.create.return_value = post_data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, json=post_data)
    result = await response.json()

    assert response.status == 201
    assert result == post_data
    ListView.create.assert_awaited_with(**post_data)
    mock_validate.assert_called_with(
        ListView.validator_class,
        post_data,
    )


async def test_create_by_form_data(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    post_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_validate.return_value = post_data
    ListView.create.return_value = post_data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, data=post_data)
    result = await response.json()

    assert response.status == 201
    assert result == post_data
    ListView.create.assert_awaited_with(**post_data)
    mock_validate.assert_called_with(
        ListView.validator_class,
        post_data,
    )
    

async def test_create_by_unsupported_type(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    post_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    ListView.create.return_value = post_data
    
    url = api.app.router['list'].url_for()

    response = await api.post(url, data=str(post_data), headers={'Content-Type': 'text/plain'})

    assert response.status == 415
    ListView.create.await_count == 0


async def test_update_mixin_full_update_by_json(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    put_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_validate.return_value = put_data
    DetailView.update.return_value = put_data

    url = api.app.router['detail'].url_for(id='1')

    response = await api.put(url, json=put_data)
    result = await response.json()

    assert response.status == 200
    assert result == put_data
    DetailView.update.assert_awaited_with('1', **put_data)
    mock_validate.assert_called_with(
        DetailView.validator_class,
        put_data,
    )


async def test_update_mixin_full_update_by_form_data(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    put_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_validate.return_value = put_data
    DetailView.update.return_value = put_data

    url = api.app.router['detail'].url_for(id='1')

    response = await api.put(url, data=put_data)
    result = await response.json()

    assert response.status == 200
    assert result == put_data
    DetailView.update.assert_awaited_with('1', **put_data)
    mock_validate.assert_called_with(
        DetailView.validator_class,
        put_data,
    )


async def test_update_mixin_full_update_by_unsupported_type(api, mocker):
    put_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    url = api.app.router['detail'].url_for(id='1')

    response = await api.put(url, data=str(put_data), headers={'Content-Type': 'text/plain'})

    assert response.status == 415
    DetailView.update.await_count == 0


async def test_update_mixin_partial_update_by_json(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    patch_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_validate.return_value = patch_data
    DetailView.partial_update.return_value = patch_data

    url = api.app.router['detail'].url_for(id='1')

    response = await api.patch(url, json=patch_data)
    result = await response.json()

    assert response.status == 200
    assert result == patch_data
    DetailView.partial_update.assert_awaited_with('1', **patch_data)
    mock_validate.assert_called_with(
        DetailView.validator_class,
        patch_data,
        exclude_none=True
    )


async def test_update_mixin_partial_update_by_form_data(api, mocker):
    mock_validate = mocker.patch(
        'api.views.mixins.validation_utils.validate_request_data'
    )
    patch_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_validate.return_value = patch_data
    DetailView.partial_update.return_value = patch_data

    url = api.app.router['detail'].url_for(id='1')

    response = await api.patch(url, data=patch_data)
    result = await response.json()

    assert response.status == 200
    assert result == patch_data
    DetailView.partial_update.assert_awaited_with('1', **patch_data)
    mock_validate.assert_called_with(
        DetailView.validator_class,
        patch_data,
        exclude_none=True
    )


async def test_update_mixin_partial_update_by_unsupported_type(api, mocker):
    patch_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }

    url = api.app.router['detail'].url_for(id='1')

    response = await api.patch(url, data=str(patch_data), headers={'Content-Type': 'text/plain'})

    assert response.status == 415
    DetailView.partial_update.await_count == 0


async def test_update_mixin_invalid_lookup(api, mocker):
    patch_data = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    DetailView.lookup_field = 'slug'

    url = api.app.router['detail'].url_for(id='1')

    response = await api.patch(url, data=patch_data)

    assert response.status == 404
    DetailView.partial_update.await_count == 0

@pytest.mark.skip(reason='Freezes during request')
async def test_delete_mixin(api):
    url = api.app.router['detail'].url_for(id='1')
    response = await api.delete(url)

    assert response.status == 204
    DetailView.delete.assert_awaited_with('1')
