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
    PrivatePostVacancy,
    PrivatePutVacancy,
    PrivatePatchVacancy,
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
    """View for private(admin) vacancies resource."""

    def get_validator_class(self):
        if self.request.method == 'POST':
            return PrivatePostVacancy
        elif self.request.method == 'PUT':
            return PrivatePutVacancy
        else:
            return PrivatePatchVacancy
    
    async def list(self, **options):
        if options:
            options = validation_utils.validate_request_query(
                PrivateFilterOptions,
                options,
                exclude_unset=True
            )
        return await super().list(**options)