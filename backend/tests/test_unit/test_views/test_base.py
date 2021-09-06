from aiohttp import web

import pytest
from unittest.mock import AsyncMock

from api.views.base import BaseVacancyView

from config import SELF_SOURCE_NAME


async def test_vacancy_view_handle_create_db_unique_error(api_client, create_vacancy):
    vacancy = await create_vacancy()

    data = {
        'name': vacancy['name'],
        'source': vacancy['source'],
    }

    url = api_client.app.router['vacancy_public_list'].url_for()

    resp = await api_client.post(url, json=data)
    result = await resp.json()

    assert resp.status == 400
    assert result == {'source': data['source']}


async def test_vacancy_view_handle_create_created_vacancy(api_client, aio_patch):
    expected = {
        'name': 'Jedi Master',
        'description': 'Master Jedi for new padavans classes',
    }
    mock_create = aio_patch('api.views.base.vacancies.create_vacancy')
    mock_create.return_value = expected

    url = api_client.app.router['vacancy_public_list'].url_for()

    resp = await api_client.post(url, json=expected)
    result = await resp.json()

    assert resp.status == 201
    mock_create.assert_awaited_once()
    

