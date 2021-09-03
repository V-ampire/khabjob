from aiohttp.web import Response, HTTPBadRequest
import json
import logging
from pydantic import BaseModel, StrictBool
import pytest

from api import validation

from core.utils import now_with_tz


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
    date_date = now_with_tz().date()
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


def test_validate_response_data_with_invalid_data(caplog):
    result = validation.validate_response_data(
        User, {'username': {}}
    )
    assert isinstance(result, Response)
    assert result.text == json.dumps({})
    assert result.content_type == 'application/json'
    assert 'username' in caplog.text
    assert str({'username': {}}) in caplog.text


def test_validate_response_data_with_valid_data():
    result = validation.validate_response_data(
        User, {'username': 'Yoda777Master'}
    )
    assert isinstance(result, Response)
    assert result.text == User(username='Yoda777Master').json()
    assert result.content_type == 'application/json'


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
    