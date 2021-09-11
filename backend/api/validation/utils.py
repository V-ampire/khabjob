from aiohttp.web import HTTPBadRequest

from pydantic import BaseModel, ValidationError

from datetime import date
import json
import logging
from typing import Dict, Any, Union


logger = logging.getLogger(__name__)


def validate_date_field_type(raw_date: Any) -> date:
    """
    Value for date field must be only str in iso format or datetime.date instance.

    :param raw_date: Raw date value, e.g. extracted from GET params.
    """
    if isinstance(raw_date, str):
        return date.fromisoformat(raw_date)
    elif isinstance(raw_date, date):
        return raw_date
    else:
        raise TypeError('Invalid date format.')
  

def validate_request_data(
    validator: BaseModel, 
    data: Dict[str, Any], 
    exclude_unset: bool=False
) -> Dict[str, Any]:
    """
    Validate data for such methods as POST, PUT, PATCH.

    :param validator: Validation validator.
    :param data: Request data.
    :param exclude_unset: whether fields which aren't passed 
    should be excluded from the returned dictionary.

    If data is not valid raise Bad request error.
    """
    try:
        return validator(**data).dict(exclude_unset=exclude_unset)
    except ValidationError as exc:
        error_msg = '{0},\nPayload: {1}'.format(exc, data)
        logger.error(error_msg)
        errors_info = {err['loc'][0]: err['msg'] for err in exc.errors()}
        raise HTTPBadRequest(
            text=json.dumps(errors_info),
            content_type='application/json'
        )


QueryType = Union[str, int, date]

def validate_request_query(
    validator: BaseModel, 
    query_params: Dict[str, Any],
    exclude_unset: bool=False
) -> Dict[str, QueryType]:
    """
    Validate request query params.

    :param validator: Validation validator.
    :param data: Query parameters.
    :param exclude_unset: whether fields which are aren't passed 
    should be excluded from the returned dictionary.

    If params is not valid return empty dict.
    """
    try:
        return validator(**query_params).dict(exclude_unset=exclude_unset)
    except ValidationError as exc:
        error_msg = '{0},\nQuery params: {1}'.format(exc, query_params)
        logger.error(error_msg)
        return {}
