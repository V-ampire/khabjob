"""
Mixins for views.
Mixins for REST API views.
"""
from aiohttp import web

from aiopg.sa import Engine

from api.validation import utils as validation_utils
from api.utils import get_pagination_params, get_request_payload

import json
from typing import Tuple, Dict, Any


class DbViewMixin:
    """Provide property db to access database."""

    @property
    def db(self) -> Engine:
        """Return database engine for current instance of app."""
        return self.request.app['db']


class AuthenticatedRequiredMixin:
    """
    Mixin limits access only for authenticated requests.
    
    :attr ALLOW_OPTIONS_REQUEST: Allow process OPTIONS requests withou authentication,
    for example OPTIONS for CORS preflight cases.
    #############################################
    WARNING: Could be potentially security issue.
    #############################################
    https://stackoverflow.com/questions/20805058/options-request-authentication
    https://github.com/aio-libs/aiohttp-cors/issues/193
    """

    ALLOW_OPTIONS_REQUEST = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.request.method == 'OPTIONS' and self.ALLOW_OPTIONS_REQUEST:
            return
            
        if self.request.get('user', None) is None:
            raise web.HTTPForbidden(
                text=json.dumps({'reason': 'Access authenticated only.'}),
                content_type='application/json',
            )


class ListMixin:
    """
    Mixin implements get_list method returns list of items.

    If you want to use search you should override search_options on
    list of options for searching.
    """
    
    pagination_limit = 20

    @property
    def offset(self) -> int:
        """Return offset option."""
        offset = int(self.request.query.get('offset', 0))
        return offset if offset >= 0 else 0

    @property
    def limit(self) -> int:
        """Return limit option."""
        limit = int(self.request.query.get('limit', self.pagination_limit))
        return limit if limit > 0 else self.pagination_limit

    async def get_list(self, *args, **kwargs):
        """Handler for method GET for list of items."""
        results = await self.list(**self.request.query)
        
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
    """Mixin implements get_detail method returns information about the item."""

    async def get_detail(self, *args, **kwargs):
        """Handler for method GET for one item."""
        if self.lookup_field not in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]
        result = await self.detail(lookup)
        return web.Response(body=result)


class CreateMixin:
    """Mixin implements post method to create item."""

    async def post(self, *args, **kwargs):
        """Create new item."""
        create_data = await get_request_payload(self.request)
        validated_data = validation_utils.validate_request_data(
            self.get_validator_class(),
            create_data,
        )
        created_item = await self.create(**validated_data)
        return web.Response(body=created_item, status=201)


class UpdateMixin:
    """Mixin implements patch and put methods to create item."""

    async def _get_update_data(self) -> Tuple[str, int, Dict[str, Any]]:
        """
        Return request data and lookup field.
        
        :return: Tuple (lookup, data) where lookup is value of lookup field.
        """
        if self.lookup_field not in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]

        update_data = await get_request_payload(self.request)
        
        return (lookup, update_data)

    async def put(self, *args, **kwargs):
        """Full update item."""
        lookup, update_data = await self._get_update_data()
        validated_data = validation_utils.validate_request_data(
            self.get_validator_class(),
            update_data,
        )
        updated_item = await self.update(lookup, **validated_data)
        return web.Response(body=updated_item, status=200)

    async def patch(self, *args, **kwargs):
        """Partial update item."""
        lookup, update_data = await self._get_update_data()
        validated_data = validation_utils.validate_request_data(
            self.get_validator_class(),
            update_data,
            exclude_unset=True
        )
        updated_item = await self.update(lookup, **validated_data)
        return web.Response(body=updated_item, status=200)


class DeleteMixin:
    """Mixin implements delete method to remove item."""
    
    async def delete_one(self, *args, **kwargs):
        """Delete item."""
        if self.lookup_field not in self.request.match_info:
            raise web.HTTPNotFound()
        lookup = self.request.match_info[self.lookup_field]
        deleted_count = await self.destroy(lookup)
        return web.Response(body={'delete': deleted_count}, status=204)

    async def delete_list(self, *args, **kwargs):
        """
        Delete items.
        
        Use request query params to filter deleted items.
        """
        deleted_count = await self.destroy_batch(self.request.query)
        return web.Response(body={'delete': deleted_count}, status=200)
