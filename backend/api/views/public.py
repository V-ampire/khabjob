from aiohttp import web

from api.views.base import BaseVacancyView
from api import validation
from api.utils import get_pagination_params


class Vacancies(BaseVacancyView):
    """View for vacancies resource."""

    search_options = [
        'date_from',
        'date_to',
        'search_query'
    ]

    async def get(self):
        """Get publiched vacancies list."""
        if self.request.query.keys() & set(self.search_options):
            validated_options = validation.validate_request_query(
                validation.SearchOptions, self.request.query
            )
            vacancies_data = await self.handle_search(**validated_options)
        else:
            vacancies_data = await self.handle_filter(is_published=True)

        count = vacancies_data[0].get('count', None) if len(vacancies_data) > 0 else 0
        response_data = get_pagination_params(
            self.request.url, 
            count=count,
            limit=self.limit, offset=self.offset
        )
        response_data.update({'results': vacancies_data})
        return validation.validate_response_data(
            validation.PublishedVacancyList, response_data
        )
