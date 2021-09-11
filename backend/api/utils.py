from aiohttp import web

import json
from yarl import URL
from typing import Dict, Optional, Any


def get_pagination_params(
    url: URL,
    count: int,
    limit: int=0,
    offset: int=0
) -> Dict[str, Optional[str]]:
    """
    Return pagination params for resource.
    """
    next_url = None
    previous_url = None
    limit = limit if limit >= 0 else 0
    offset = offset if offset >= 0 else 0

    next_offset = offset + limit
    previous_offset = offset - limit

    if offset < count and next_offset < count:
        next_url = str(url.update_query({'offset': next_offset, 'limit': limit}))

    if previous_offset >= 0:
        previous_url = str(url.update_query({
            'offset': previous_offset,
            'limit': limit
        }))
    
    return {
        'count': count,
        'next': next_url,
        'previous': previous_url,
    }


async def get_request_payload(request: web.Request) -> Dict[str, Any]:
    """
    Return dict with request payload data.
    
    Supported types:
        - application/json
        - multipart/form-data
        - application/x-www-form-urlencoded

    If type is not supported return HTTPUnsupportedMediaType 415.
    """
    if request.content_type == 'application/json':
        return await request.json()
    elif request.content_type in [
        'multipart/form-data',
        'application/x-www-form-urlencoded'
    ]:
        return await request.post()
    else:
        raise web.HTTPUnsupportedMediaType(
            text=json.dumps({'reason': 'Unsupported type of update data.'}),
            content_type='application/json',
        )
