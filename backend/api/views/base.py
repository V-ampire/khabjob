from aiohttp.web import View
from aiopg.sa import Engine
from psycopg2.errors import UniqueViolation
from typing import List, Mapping

from core.services import vacancies
from core.db.utils import parse_unique_violation_fields


class BaseView(View):
    """
    Base class for views.
    
    Provide access via property to db, offset, limit.
    """
    pagination_limit = 20

    lookup_field = 'id'

    async def get_list(self, *args, **kwargs):
        """Implement handler to return list of items."""
        raise NotImplementedError

    async def get_detail(self, *args, **kwargs):
        """Implement handler to return detail item."""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        """
        Return self.get_detail if self.lookup_field in url,
        else return self.get_list.
        """
        if self.lookup_field in self.request.match_info:
            return await self.get_detail(*args, **kwargs)
        return await self.get_list(*args, **kwargs)

    @property
    def db(self) -> Engine:
        """Return database engine for current instance of app."""
        return self.request.app['db']

    @property
    def offset(self) -> int:
        """Return dict with limit and offset options."""
        offset =  int(self.request.query.get('offset', 0))
        return offset if offset >= 0 else 0

    @property
    def limit(self) -> int:
        """Return dict with limit and offset options."""
        limit = int(self.request.query.get('limit', self.pagination_limit))
        return limit if limit > 0 else self.pagination_limit


class BaseVacancyView(BaseView):
    """Base view to handle vacancies."""

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
                return parse_unique_violation_fields(error)
        return created_vacancy


