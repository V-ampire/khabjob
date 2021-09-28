"""Views for searching."""
from aiopg.sa.result import RowProxy

from typing import List

from api.validation.vacancies import SearchOptions
from api.validation.utils import validate_request_query
from api.views.base import BaseView
from api.views.mixins import DbViewMixin, ListMixin

from core.services.vacancies import search_vacancies


class SearchVacancies(DbViewMixin, ListMixin, BaseView):
    """Base view to handle search vacancies."""

    async def list(self, **options) -> List[RowProxy]:
        """Return vacancy list by search service."""
        validated_options = validate_request_query(
            SearchOptions,
            options,
            exclude_unset=True
        )
        if self.request.get('user', None) is None:
            validated_options.update({'published_only': True})
        async with self.db.acquire() as conn:
            vacancies_data = await search_vacancies(
                conn, limit=self.limit, offset=self.offset, **validated_options
            )
        return vacancies_data