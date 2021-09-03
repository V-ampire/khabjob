from aiohttp import web

from api.views.base import BaseVacancyView
from api import validation
from api.utils import get_pagination_params


class Vacancies(BaseVacancyView):
    """View for vacancies resource."""

    search_options = [
        'date_from',
        'date_to',
        'search_query',
        'source_name',
    ]

    async def get_list(self):
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
        return web.Response(body=response_data)

    async def get_detail(self):
        """Get info of vacancy."""
        vacancy_id = self.request.match_info[self.lookup_field]
        vacancies = await self.handle_filter(is_published=True, id=vacancy_id)
        if len(vacancies) == 0:
            return web.json_response({}, status=404)
        return web.Response(body=vacancies[0])

    async def post(self):
        """Offer new vacancy via site feedback."""
        vacancy_data = self.request.json()
        vacancy_data.update({'is_published': False})
        validated_data = validation.validate_request_data(
            validation.PublishedVacancyCreate, vacancy_data
        )
        created_vacancy = await self.handle_create(**validated_data)
        return web.Response(body=created_vacancy)

        