"""
Based on https://github.com/alvassin/backendschool2019/blob/master/analyzer/api/payloads.py

In this module implements helpers to convert to json such special objects as
aiopg.RowProxy and date object.
"""
import json
from datetime import date
from functools import partial, singledispatch
from typing import Any

from aiohttp.payload import JsonPayload as BaseJsonPayload, Payload
from aiohttp.typedefs import JSONEncoder

from aiopg.sa.result import RowProxy


@singledispatch
def convert(value):
    """
    Serialize value.
    """
    raise TypeError(f'Unserializable value: {value!r}')


@convert.register(RowProxy)
def convert_aiopg_row(value: RowProxy):
    """
    Serialize to aiopg.RowProxy object.
    """
    return dict(value)


@convert.register(date)
def convert_date(value: date):
    """
    Serialize date to string in isoformat.
    """
    return value.isoformat()


dumps = partial(json.dumps, default=convert)


class JsonPayload(BaseJsonPayload):
    def __init__(self,
                 value: Any,
                 encoding: str = 'utf-8',
                 content_type: str = 'application/json',
                 dumps: JSONEncoder = dumps,
                 *args: Any,
                 **kwargs: Any) -> None:
        super().__init__(value, encoding, content_type, dumps, *args, **kwargs)