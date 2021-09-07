import json
import pytest

from api.utils import get_pagination_params
from api.payloads import dumps

from core.services.vacancies import filter_vacancies, search_vacancies


async def test_vacancy_list_private_resource(api_client, create_vacancy, aio_engine):
    [await create_vacancy() for i in range(5)]
    [await create_vacancy(is_published=False) for i in range(5)]

    async with aio_engine.acquire() as conn:
        expected_vacancies = await filter_vacancies(conn)

    url = api_client.app.router['vacancy_private_list'].url_for()
    
    resp = await api_client.get(url)
    result = await resp.json()
    
    expected = get_pagination_params(
        resp.url,
        count=10,
        limit=20 # Default list view limit
    )
    expected.update({'results': expected_vacancies})

    assert resp.status == 200
    assert result == json.loads(dumps(expected))
