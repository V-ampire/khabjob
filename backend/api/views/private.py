"""
Views for private API interface.
Access only for authenticated users.
"""
from aiohttp import web

from api.views.base import BaseVacancyView
from api import validation


class Vacancies(BaseVacancyView):
    """View for vacancies resource."""

    async def get_list(self):
        """Get publiched vacancies list."""
        vacancies_data = await self.handle_filter()
        count = vacancies_data[0].get('count', None) if len(vacancies_data) > 0 else 0
        response_data = get_pagination_params(
            self.request.url, 
            count=count,
            limit=self.limit, offset=self.offset
        )
        response_data.update({'results': vacancies_data})
        return web.Response(body=response_data)