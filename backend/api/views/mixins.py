from aiohttp import web

from api.validation import utils as validation_utils
from api.utils import get_pagination_params


class ListMixin:
    """
    Mixin implements get_list method returns list of items.

    If you want to use search you should override search_options on
    list of options for searching.
    """
    pagination_limit = 20

    search_options = []

    @property
    def offset(self) -> int:
        """Return offset option."""
        offset =  int(self.request.query.get('offset', 0))
        return offset if offset >= 0 else 0

    @property
    def limit(self) -> int:
        """Return limit option."""
        limit = int(self.request.query.get('limit', self.pagination_limit))
        return limit if limit > 0 else self.pagination_limit

    async def get_list(self, *args, **kwargs):
        """Get list of items."""
        results = []

        if self.request.query.keys() & set(self.search_options):
            search_query = {
                opt: self.request.query[opt] for opt in self.search_options
            }
            results = await self.handle_search(**search_query)
        
        elif self.request.query:
            results = await self.handle_filter(**self.request.query)
        
        else:
            results = await self.handle_filter()

        count = results[0].get('count', 0) if len(results) > 0 else 0

        # If handler returned results with count then use pagination
        if count > 0:
            response_data = get_pagination_params(
                self.request.url, 
                count=count,
                limit=self.limit,
                offset=self.offset
            )
            response_data.update({'results': results})
        else:
            response_data = {'results': results}
        
        return web.Response(body=response_data)

    
class DetailMixin:
    """
    Mixin implements get_detail method returns information about the item.
    """

    async def get_detail(self, *args, **kwargs):
        """Get info about item."""
        detail_data = {}
        detail_data[self.lookup_field] = self.request.match_info[self.lookup_field]
        result = await self.handle_detail(**detail_data)
        return web.Response(body=result)


class CreateMixin:
    """
    Mixin implements post method to create item.
    """

    async def post(self, *args, **kwargs):
        """Create new item."""
        if self.request.content_type == 'application/json':
            create_data = await self.request.json()
        elif self.request.content_type == 'multipart/form-data':
            create_data = await self.request.post()
        else:
            return web.Response(body={'reason': 'Unsupported type of post data.'}, status=415)
        created_item = await self.handle_create(**create_data)
        return web.Response(body=created_item, status=201)

