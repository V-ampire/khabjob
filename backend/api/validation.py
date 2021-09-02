"""
Validation requests and responses data.
"""
from aiohttp.web import Response, HTTPBadRequest
from datetime import date
import json
import logging
from pydantic import BaseModel, ValidationError, validator
from pytz import timezone
from typing import List, Optional, Dict, Any, Union

from config import TIMEZONE


logger = logging.getLogger(__name__)


class PublishedVacancy(BaseModel):
    """Pydantic model to validate published vacancy data."""
    id: int
    name: str
    source: Optional[str]
    source_name: str
    description: Optional[str]
    modified_at: date


class PublishedVacancyList(BaseModel):
    """Pydantic model to validate published list vacancy data."""
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PublishedVacancy]


class SearchOptions(BaseModel):
    """Pydantic model to validate serach options."""
    date_from: Optional[date]
    date_to: Optional[date]
    search_query: Optional[str]

    @validator('date_from', pre=True)
    def validate_date_from_format(cls, date_from):
        return validate_date_field_type(date_from)


def validate_date_field_type(raw_date: Any) -> date:
    """Value for date field must be only str in iso format or datetime.date instance."""
    if isinstance(raw_date, str):
        return date.fromisoformat(raw_date)
    elif isinstance(raw_date, date):
        return raw_date
    else:
        raise TypeError('Invalid date format.')


def validate_response_data(schema: BaseModel, data: Dict[str, Any]) -> Response:
    """
    Validate response data and return aiohttp Response.
 
    :param schema: Validation schema.
    :param data: Response data.

    If data is not valid return response with empty dict.
    """
    try:
        response_json = schema(**data).json()
    except ValidationError as exc:
        error_msg = '{0},\nResponse data: {1}'.format(exc, data)
        logger.error(error_msg)
        response_json = json.dumps({})

    return Response(text=response_json, content_type='application/json')
    

def validate_request_payload(schema: BaseModel, payload: Dict[str, Any]):
    """
    Validate payload for such methods as POST, PUT, PATCH.

    :param schema: Validation schema.
    :param data: Request payload.

    If payload is not valid raise Bad request error.
    """
    try:
        return schema(**payload).dict()
    except ValidationError as exc:
        error_msg = '{0},\nPayload: {1}'.format(exc, payload)
        logger.error(error_msg)
        errors_info = {err['loc'][0]: err['msg'] for err in exc.errors()}
        raise HTTPBadRequest(text=json.dumps(errors_info), content_type='application/json')


QueryType = Union[str, int, date]

def validate_request_query(schema: BaseModel, 
                            query_params: Dict[str, Any]) -> Dict[str, QueryType]:
    """
    Validate request query params.

    :param schema: Validation schema.
    :param data: Query parameters.

    If params is not valid return empty dict.
    """
    try:
        return schema(**query_params).dict()
    except ValidationError as exc:
        error_msg = '{0},\nQuery params: {1}'.format(exc, query_params)
        logger.error(error_msg)
        return {}
