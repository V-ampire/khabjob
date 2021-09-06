from pydantic import (
    BaseModel, 
    ValidationError,
    Field,
    validator,
    root_validator,
    StrictBool, 
    HttpUrl)

from datetime import date
from typing import Optional

from api.validation.utils import validate_date_field_type


class BaseVacancy(BaseModel):
    """Base vacancy model."""

    name: str
    source: Optional[HttpUrl]
    source_name: str
    description: Optional[str]
    is_published: StrictBool


class PublicVacancyCreate(BaseVacancy):
    """Model to validate vacancy data to create by public API."""

    class Config:
        extra = 'forbid'

    @validator('is_published')
    def validate_is_published_only_false(cls, is_published):
        if is_published:
            raise ValueError('Public added vacancy cant be pusblished.')
        return is_published

    @root_validator
    def validate_source_or_description_required(cls, values):
        """For public added vacancies should be source or description."""
        source = values.get('source', None)
        description = values.get('description', None)
        if source is None and description is None:
            raise ValueError('Vacancy must have source or description.')
        return values
    

class SearchVacancyOptions(BaseModel):
    """Pydantic model to validate serach options."""
    date_from: Optional[date]
    date_to: Optional[date]
    search_query: Optional[str]

    @validator('date_from', pre=True)
    def validate_date_from_format(cls, date_from):
        return validate_date_field_type(date_from)


class PublicFilterVacancyOptions(BaseModel):
    """Model to validate filter options for public API."""
    source_name: str
    is_published: StrictBool = Field(False, const=True)


class PrivateFiltervacancyOptions(PublicFilterVacancyOptions):
    """Model to validate filter options for private API."""
    is_published: StrictBool
