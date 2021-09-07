from aiohttp import web

from aiopg.sa import Engine

from api.validation import utils as validation_utils
from api.utils import get_pagination_params

from typing import Tuple, Dict, Any


class DbViewMixin:
    """Provide property db to access database."""

    @property
    def db(self) -> Engine:
        """Return database engine for current instance of app."""
        return self.request.app['db']


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
            results = await self.search(**search_query)
        
        elif self.request.query:
            results = await self.filter_by(**self.request.query)
        
        else:
            results = await self.filter_by()

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

    Use ID as lookup field by default.
    Override lookup_field attribute to change lookup field.
    """

    lookup_field = 'id'

    async def get_detail(self, *args, **kwargs):
        """Get info about item."""
        if not self.lookup_field in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]
        result = await self.detail(lookup)
        return web.Response(body=result)


class CreateMixin:
    """Mixin implements post method to create item."""

    async def _get_create_data(self) -> Dict[str, Any]:
        """Return request POST data or raise HTTPUnsupportedMediaType."""
        if self.request.content_type == 'application/json':
            create_data = await self.request.json()
        elif self.request.content_type in ['multipart/form-data', 'application/x-www-form-urlencoded']:
            create_data = await self.request.post()
        else:
            raise web.HTTPUnsupportedMediaType(reason='Unsupported type of post data.')
        return create_data


    async def post(self, *args, **kwargs):
        """Create new item."""
        create_data = await self._get_create_data()
        validated_data = validation_utils.validate_request_data(
            self.validator_class,
            create_data,
        )
        created_item = await self.create(**validated_data)
        return web.Response(body=created_item, status=201)


class UpdateMixin:
    """
    Mixin implements patch and put methods to create item.
    
    Use ID as lookup field by default.
    Override lookup_field attribute to change lookup field.
    """

    async def _get_update_data(self) -> Tuple[str, int, Dict[str, Any]]:
        """
        Return request data or raise HTTPUnsupportedMediaType.
        
        :return: Tuple (lookup, data) where lookup is value of lookup field.
        """
        if not self.lookup_field in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]

        if self.request.content_type == 'application/json':
            create_data = await self.request.json()
        elif self.request.content_type in ['multipart/form-data', 'application/x-www-form-urlencoded']:
            create_data = await self.request.post()
        else:
            raise web.HTTPUnsupportedMediaType(reason='Unsupported type of update data.')
        
        return (lookup, create_data)

    async def put(self, *args, **kwargs):
        """Full update item."""
        lookup, update_data = await self._get_update_data()
        validated_data = validation_utils.validate_request_data(
            self.validator_class,
            update_data,
        )
        updated_item = await self.update(lookup, **validated_data)
        return web.Response(body=updated_item, status=200)

    async def patch(self, *args, **kwargs):
        """Partitial update item."""
        lookup, update_data = await self._get_update_data()
        validated_data = validated_data = validation_utils.validate_request_data(
            self.validator_class,
            update_data,
            exclude_none=True
        )
        updated_item = await self.update(lookup, **validated_data)
        return web.Response(body=updated_item, status=200)


class DeleteMixin:
    """
    Mixin implements delete method to remove item.
    
    Use ID as lookup field by default.
    Override lookup_field attribute to change lookup field.
    """
    
    async def delete(self, *args, **kwargs):
        """Delete item."""
        if not self.lookup_field in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]
        await self.delete(lookup)
        return web.Response(status=204)