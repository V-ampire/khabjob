from aiohttp import web

from aiohttp_cors import CorsViewMixin

from aiopg.sa.result import RowProxy

from psycopg2.errors import UniqueViolation

import logging
import json
from typing import List, Mapping

from api.views.mixins import DbViewMixin

from core.services import vacancies
from core.db.utils import parse_unique_violation_fields


logger = logging.getLogger(__name__)


class BaseView(CorsViewMixin, web.View):
    """
    Base class for rest api views.
    
    Use ID as lookup field by default.
    Override lookup_field attribute to change lookup field.
    """

    validator_class = None
    lookup_field = 'id'

    def get_validator_class(self):
        """Override this method to customize getting validator class."""
        return self.validator_class
    
    async def list(self, *args, **kwargs) -> List:
        """Implement handler to return filtered list of items."""
        raise NotImplementedError

    async def detail(self, *args, **kwargs)  -> Mapping:
        """Implement handler to return info about one item."""
        raise NotImplementedError

    async def create(self, *args, **kwargs) -> Mapping:
        """Implement handler to create item."""
        raise NotImplementedError

    async def update(self, *args, **kwargs) -> Mapping:
        """Implement handler to full update item."""
        raise NotImplementedError
    
    async def destroy(self, *args, **kwargs) -> None:
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

    async def list(self, **options) -> List[RowProxy]:
        """Return vacancy list by filter service."""
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.filter_vacancies(
                conn, limit=self.limit, offset=self.offset, **options
            )
        return vacancies_data
  
    async def detail(self, vacancy_id: int, **options) -> RowProxy:
        """Return info about one vacancy using vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            vacancies_data = await vacancies.filter_vacancies(
                conn, limit=1, id=vacancy_id, **options
            )
        if len(vacancies_data) == 0:
            raise web.HTTPNotFound()
        return vacancies_data[0]

    async def create(self, **vacancy_data) -> RowProxy:
        """
        Create and return new vacancy data.
        
        If while creation raises UniqueViolation error,
        return dict with field name and invalid value.
        """
        async with self.db.acquire() as conn:
            try:
                created_vacancy = await vacancies.create_vacancy(conn, **vacancy_data)
            except UniqueViolation as error:
                nonunique_fields = parse_unique_violation_fields(error)
                error_data = {}
                for field in nonunique_fields.keys():
                    error_data[field] = 'Вакансия со значением {0} уже существует.'.format(
                        nonunique_fields[field]
                    )
                logger.error(
                    'Attempt to create vacancy with non-unique fields: {0}'.format(
                        nonunique_fields
                    )
                )
                raise web.HTTPBadRequest(
                    text=json.dumps(error_data),
                    content_type='application/json',
                )
        return created_vacancy

    async def update(self, vacancy_id: int, **update_data) -> RowProxy:
        """Update vacancy by vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            vacancy = await vacancies.update_vacancy(
                conn, vacancy_id, **update_data
            )
        return vacancy

    async def destroy(self, vacancy_id: int) -> int:
        """Delete vacancy by vacancy ID."""
        vacancy_id = self.validate_vacancy_id(vacancy_id)
        async with self.db.acquire() as conn:
            result = await vacancies.delete_vacancy(
                conn, vacancy_id,
            )
        return result
