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

    @root_validator
    def validate_source_or_description_required(cls, values):
        """For public added vacancies should be source or description."""
        source = values.get('source', None)
        description = values.get('description', None)
        if source is None and description is None:
            raise ValueError('Vacancy must have source or description.')
        return values

    @validator('source')
    def convert_source_to_str(cls, source_http):
        return str(source_http)


class PublicVacancy(BaseVacancy):
    """Model to validate vacancy data to create by public API."""

    class Config:
        extra = 'forbid'


class PrivateVacancy(BaseVacancy):
    """Model to validate vacancy data to create by admin API."""
    
    is_published: Optional[StrictBool]

    class Config:
        extra = 'forbid'


class SearchOptions(BaseModel):
    """Pydantic model to validate serach options."""
    date_from: Optional[date]
    date_to: Optional[date]
    search_query: Optional[str]

    @validator('date_from', pre=True)
    def validate_date_from_format(cls, date_from):
        return validate_date_field_type(date_from)


class PublicFilterOptions(BaseModel):
    """Model to validate filter options for public API."""
    source_name: Optional[str]


class PrivateFilterOptions(BaseModel):
    """Model to validate filter options for private API."""
    source_name: Optional[str]
    is_published: Optional[bool]



