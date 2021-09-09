from aiohttp import web

from psycopg2.errors import UniqueViolation

import json
from typing import List, Mapping, Dict, Union

from api.views.mixins import DbViewMixin

from core.services import vacancies
from core.db.utils import parse_unique_violation_fields


class BaseView(web.View):
    """Base class for rest api views."""

    validator_class = None
    
    async def filter_by(self, *args, **kwargs) -> List:
        """Implement handler to return filtered list of items."""
        raise NotImplementedError

    async def search(self, *args, **kwargs) -> List:
        """Implement handler to return list of items by search."""
        raise NotImplementedError

    async def detail(self, *args, **kwargs)  -> Dict:
        """Implement handler to return info about one item."""
        raise NotImplementedError

    async def create(self, *args, **kwargs) -> Dict:
        """Implement handler to create item."""
        raise NotImplementedError

    async def update(self, *args, **kwargs) -> Dict:
        """Implement handler to full update item."""
        raise NotImplementedError
    
        """Implement handler to partial update item."""
        raise NotImplementedError
    
    async def delete(self, *args, **kwargs) -> None:
        """Implement handler to delete item."""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        """
        Return self.get_detail if self.lookup_field attribute in url,
        else return self.get_list.
        """
        if self.lookup_field in self.request.match_info:
            return await self.get_detail(*args, **kwargs)
        return await self.get_list(*args, **kwargs)


class BaseVacancyView(DbViewMixin, BaseView):
    """Base view to handle vacancies."""

    def validate_vacancy_id(self, vacancy_id):
        """If vacancy_id is invalid raise 404."""
        try:
            vacancy_id = int(vacancy_id)
        except ValueError:
            raise web.HTTPNotFound()
        return vacancy_id

    async def filter_by(self, **options) -> List[Mapping]:
        """Return vacancy list by filter service."""
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.filter_vacancies(
                conn, limit=self.limit, offset=self.offset, **options
            )
        return vacancies_data

    async def search(self, **options) -> List[Mapping]:
        """Return vacancy list by serach service."""
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.search_vacancies(
                conn, limit=self.limit, offset=self.offset, **options
            )
        return vacancies_data
    
    async def detail(self, vacancy_id: int, **options) -> Mapping:
        """Return info about one vacancy using vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.filter_vacancies(
                conn, limit=1, id=vacancy_id, **options
            )
        if len(vacancies_data) == 0:
            raise web.HTTPNotFound()
        return vacancies_data[0]

    async def create(self, **vacancy_data) -> Mapping:
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
                raise web.HTTPBadRequest(text=json.dumps(error_data), content_type='application/json')
        return created_vacancy

    async def update(self, vacancy_id: int, **update_data) -> Mapping:
        """Update vacancy by vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            vacancy = await vacancies.update_vacancy(
                conn, id=vacancy_id, **update_data
            )
        return vacancy

    async def delete(self, vacancy_id: int) -> int:
        """Delete vacancy by vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            result = await vacancies.delete_vacancy(
                conn, id=vacancy_id,
            )
        return result

