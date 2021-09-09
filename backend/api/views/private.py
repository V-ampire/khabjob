"""
Views for private API interface.
Access only for authenticated users.
"""
from api.views.base import BaseVacancyView
from api.views.mixins import (
    ListMixin,
    DetailMixin,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    AuthenticatedRequiredMixin,
)
from api.validation import utils as validation_utils
from api.validation.vacancies import (
    PrivateVacancy,
    SearchOptions,
    PrivateFilterOptions,
)


class Vacancies(
    AuthenticatedRequiredMixin,
    ListMixin,
    DetailMixin,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
    BaseVacancyView
):
    """View for vacancies resource."""

    validator_class = PrivateVacancy
    
    search_options = [
        'date_from',
        'date_to',
        'search_query',
    ]

    async def filter_by(self, **options):
        if options:
            options = validation_utils.validate_request_query(
                PrivateFilterOptions,
                options,
                exclude_none=True
            )
        return await super().filter_by(**options)
    
    async def search(self, **options):
        validated_options = validation_utils.validate_request_query(
            SearchOptions,
            options,
            exclude_none=True
        )
        return await super().search(**validated_options)
