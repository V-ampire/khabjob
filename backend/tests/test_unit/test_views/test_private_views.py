from datetime import datetime
import pytest

from api.utils import get_pagination_params

from config import SELF_SOURCE_NAME


async def test_vacancy_private_list(api_client, aio_patch, views_vacancy_list):
    expected_vacancies = views_vacancy_list(3, 3)

    mock_filter = aio_patch('api.views.private.Vacancies.handle_filter')
    mock_filter.return_value = expected_vacancies

    url = api_client.app.router['vacancy_private_list'].url_for()
    
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
    mock_filter.assert_awaited_with()


async def test_vacancy_list_pagination(api_client, aio_patch, views_vacancy_list):
    expected_vacancies = views_vacancy_list(3, 3)[4:7]

    mock_filter = aio_patch('api.views.private.Vacancies.handle_filter')
    mock_filter.return_value = expected_vacancies

    url = api_client.app.router['vacancy_private_list'].url_for().with_query({
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
    mock_filter.assert_awaited_with()