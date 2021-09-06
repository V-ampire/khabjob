from aiohttp.web import Response, HTTPBadRequest
import json
import logging
from pydantic import BaseModel, StrictBool
import pytest

from api import validation


class User(BaseModel):
    username: str


class QueryParams(BaseModel):
    id: int


class PostData(BaseModel):
    username: str
    is_jedi: StrictBool

    class Config:
        extra = 'forbid'


def test_validate_date_field_type_with():
    date_date = datetime.now().date()
    valid_date_str = date_date.isoformat()
    invalid_date_str = '2021.09.02'
    date_int = 123
    date_float = 3.14

    assert validation.validate_date_field_type(date_date) == date_date
    assert validation.validate_date_field_type(valid_date_str) == date_date
    with pytest.raises(ValueError):
        assert validation.validate_date_field_type(invalid_date_str) == date_date
    with pytest.raises(TypeError):
        assert validation.validate_date_field_type(date_int) == date_date
    with pytest.raises(TypeError):
        assert validation.validate_date_field_type(date_float) == date_date


def test_validate_request_query_with_invalid_params(caplog):
    result_type = validation.validate_request_query(QueryParams, {'id': 'abc'})
    result_no_param = validation.validate_request_query(QueryParams, {'uuid': 123})
    assert result_type == {}
    assert result_type == {}
    assert str({'id': 'abc'}) in caplog.text
    assert str({'uuid': 123}) in caplog.text


def test_validate_request_query_with_valid_params():
    result = validation.validate_request_query(QueryParams, {'id': 123})
    assert result == {'id': 123}


def test_validate_request_data_with_invalid_payload(caplog):
    post_data = {'username': 'ObiOne', 'is_jedi': 'yes'}
    with pytest.raises(HTTPBadRequest) as err:
        error = err
        validation.validate_request_data(PostData, post_data)
    assert str(post_data) in caplog.text
    assert error.value.text == json.dumps(
        {'is_jedi': 'value is not a valid boolean'}
    )
    assert error.value.content_type == 'application/json'


def test_validate_request_data_with_valid_payload(caplog):
    post_data = {'username': 'ObiOne', 'is_jedi': True}
    assert validation.validate_request_data(PostData, post_data) == post_data


def test_published_vacancy_create_is_published_only():
    data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob',
        'source': 'http://jedi-academy.co/vacancies/58',
        'is_published': True
    }
    with pytest.raises(ValueError):
        validation.PublishedVacancyCreate(**data)


def test_published_vacancy_create_validate_source_or_description_required():
    data = {
        'name': 'Jedi Master',
        'source_name': 'khabjob',
        'is_published': False
    }
    data_source = {
        'name': 'Jedi Master',
        'source_name': 'khabjob',
        'source': 'http://jedi-academy.co/vacancies/58',
        'is_published': False
    }
    data_description = {
        'name': 'Jedi Master',
        'source_name': 'khabjob',
        'description': 'Mater Jedi for new padavans classes',
        'is_published': False
    }
    with pytest.raises(ValueError):
        validation.PublishedVacancyCreate(**data)
    
    validation.PublishedVacancyCreate(**data_source)
    validation.PublishedVacancyCreate(**data_description)
