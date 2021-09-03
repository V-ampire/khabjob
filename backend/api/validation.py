"""
Validation requests and responses data.
"""
from aiohttp.web import Response, HTTPBadRequest
from datetime import date
import json
import logging
from pydantic import BaseModel, ValidationError, validator,  StrictBool
from pytz import timezone
from typing import List, Optional, Dict, Any, Union

from config import TIMEZONE


logger = logging.getLogger(__name__)


class PublishedVacancyCreate(BaseModel):
    """Pydantic model to validate published vacancy data to create."""
    name: str
    source: Optional[str]
    source_name: str
    description: Optional[str]
    is_published: StrictBool

    class Config:
        extra = 'forbid'

    @validator('is_published')
    def validate_is_published_only_false(cls, is_published):
        if is_published:
            raise TypeError('Public added vacancy cant be pusblished.')
        return is_published

    @validator('source', 'description')
    def validate_source_or_description_required(cls, values):
        """For public added vacancies should be source or description."""
        source, description = values
        if source is None and description is None:
            raise ValueError('Vacancy must have source or description.')
    

class SearchOptions(BaseModel):
    """Pydantic model to validate serach options."""
    date_from: Optional[date]
    date_to: Optional[date]
    search_query: Optional[str]
    source_name: Optional[str]

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
  

def validate_request_data(schema: BaseModel, data: Dict[str, Any]):
    """
    Validate data for such methods as POST, PUT, PATCH.

    :param schema: Validation schema.
    :param data: Request data.

    If data is not valid raise Bad request error.
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
