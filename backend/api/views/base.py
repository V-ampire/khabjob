from aiohttp.web import View, HTTPBadRequest

from aiopg.sa import Engine

from psycopg2.errors import UniqueViolation

import json
from typing import List, Mapping, Dict, Union

from api.validation import utils as validation_utils

from core.services import vacancies
from core.db.utils import parse_unique_violation_fields


class BaseView(View):
    """Base class for views."""

    lookup_field = 'id'
    
    async def handle_filter(self, *args, **kwargs) -> List:
        """Implement handler to return filtered list of items."""
        raise NotImplementedError

    async def handle_search(self, *args, **kwargs) -> List:
        """Implement handler to return list of items by search."""
        raise NotImplementedError

    async def handle_detail(self, *args, **kwargs)  -> Dict:
        """Implement handler to return info about one item."""
        raise NotImplementedError

    async def handle_create(self, *args, **kwargs) -> Dict:
        """Implement handler to rcreate item."""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        """
        Return self.get_detail if 'id' attribute in url,
        else return self.get_list.
        """
        if self.lookup_field in self.request.match_info:
            return await self.get_detail(*args, **kwargs)
        return await self.get_list(*args, **kwargs)

    @property
    def db(self) -> Engine:
        """Return database engine for current instance of app."""
        return self.request.app['db']

    


class BaseVacancyView(BaseView):
    """Base view to handle vacancies."""

    search_validator = None
    filter_validator = None

    async def handle_filter(self, **options) -> List[Mapping]:
        """Return vacancy list by filter service."""
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.filter_vacancies(
                conn, limit=self.limit, offset=self.offset, **options
            )
        return vacancies_data

    async def handle_search(self, **options) -> List[Mapping]:
        """Return vacancy list by serach service."""
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.search_vacancies(
                conn, limit=self.limit, offset=self.offset, **options
            )
        return vacancies_data

    async def handle_create(self, **vacancy_data) -> Mapping:
        """
        Create and return new vacancy data.
        
        If while creation raises UniqueViolation error,
        return dict with field name and invalid value.
        """
        async with self.db.acquire() as conn:
            try:
                created_vacancy = await vacancies.create_vacancy(conn, **vacancy_data)
            except UniqueViolation as error:
                error_data = parse_unique_violation_fields(error)
                raise HTTPBadRequest(text=json.dumps(error_data), content_type='application/json')
        return created_vacancy
