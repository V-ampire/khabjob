from aiohttp.web import View
from aiopg.sa import Engine
from typing import List, Mapping

from core.services import vacancies


class BaseView(View):
    """
    Base class for views.
    
    Provide access via property to db, offset, limit.
    """
    pagination_limit = 20

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
