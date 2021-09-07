"""
Views for public API interface.
"""
from api.views.base import BaseVacancyView
from api.views.mixins import (
    ListMixin,
    DetailMixin,
    CreateMixin
)
from api.validation import utils as validation_utils
from api.validation.vacancies import (
    PublicVacancy,
    SearchOptions,
    PublicFilterOptions,
)

from config import SELF_SOURCE_NAME


class Vacancies(
    ListMixin,
    DetailMixin,
    CreateMixin,
    BaseVacancyView
):
    """View for vacancies resource."""

    validator_class = PublicVacancy
    
    search_options = [
        'date_from',
        'date_to',
        'search_query',
    ]

    async def filter_by(self, **options):
        if options:
            options = validation_utils.validate_request_query(
                PublicFilterOptions,
                options,
                exclude_none=True
            )
        options.update({'is_published': True})
        return await super().filter_by(**options)

    async def search(self, **options):
        validated_options = validation_utils.validate_request_query(
            SearchOptions,
            options,
            exclude_none=True
        )
        return await super().search(**validated_options)

    async def detail(self, vacancy_id):
        return await super().detail(vacancy_id, is_published=True)

    async def create(self, **vacancy_data):
        vacancy_data.update({
            'source_name': SELF_SOURCE_NAME,
            'is_published': False,
        })
        return await super().create(**vacancy_data)
