"""
Views for public API interface.
"""
from api.views.base import BaseVacancyView
from api.views.mixins import (
    ListMixin,
    DetailMixin,
    CreateMixin,
)
from api.validation import utils as validation_utils
from api.validation.vacancies import (
    PublicVacancy,
    PublicFilterOptions,
)

from aiohttp import web
from config import SELF_SOURCE_NAME


class Vacancies(
    ListMixin,
    DetailMixin,
    CreateMixin,
    BaseVacancyView
):
    """View for vacancies resource."""

    validator_class = PublicVacancy
    
    async def list(self, **options):
        if options:
            options = validation_utils.validate_request_query(
                PublicFilterOptions,
                options,
                exclude_unset=True
            )
        options.update({'is_published': True})
        return await super().list(**options)

    async def detail(self, vacancy_id):
        return await super().detail(vacancy_id, is_published=True)

    async def create(self, **vacancy_data):
        vacancy_data.update({
            'source_name': SELF_SOURCE_NAME,
            'is_published': False,
        })
        return await super().create(**vacancy_data)
