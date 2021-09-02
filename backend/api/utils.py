from yarl import URL
from typing import List, Dict, Optional


def get_pagination_params(url: URL, count: int, limit: int=0, offset: int=0) -> Dict[str, Optional[str]]:
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
        previous_url = str(url.update_query({'offset': previous_offset, 'limit': limit}))
    return {
        'count': count,
        'next': next_url,
        'previous': previous_url,
    }
