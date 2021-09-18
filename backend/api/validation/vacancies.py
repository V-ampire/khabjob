from pydantic import (
    BaseModel,
    validator,
    root_validator,
    StrictBool, 
    HttpUrl
)

from datetime import date
from typing import Optional

from api.validation.utils import validate_date_field_type

from config import SELF_SOURCE_NAME


class BaseVacancy(BaseModel):
    """Base vacancy model."""

    name: Optional[str]
    source: Optional[HttpUrl]
    source_name: Optional[str]
    description: Optional[str]

    @validator('source')
    def convert_source_to_str(cls, source_http):
        """Convert HttpUrl type to string."""
        return str(source_http)

    class Config:
        extra = 'forbid'


class PublicVacancy(BaseVacancy):
    """
    Model to validate vacancy data to create by public API.
    
    Fields should include name and source or description.
    Source name always the sitename.
    """

    name: str
    source_name: str = SELF_SOURCE_NAME

    @root_validator
    def validate_source_or_description_required(cls, values):
        """For public added vacancies should be source or description."""
        source = values.get('source', None)
        description = values.get('description', None)
        if source is None and description is None:
            raise ValueError('Vacancy must have source or description.')
        return values


class PrivatePostVacancy(BaseVacancy):
    """
    Model to validate vacancy data to create by admin API.
    
    Requires name and is_published fields.
    """
    
    name: str
    is_published: StrictBool
   

class PrivatePutVacancy(BaseVacancy):
    """
    Model to validate vacancy data to full update vacancy by admin API.
    
    For full update doesn't allow optional values.
    """
    
    name: str
    source: HttpUrl
    source_name: str
    description: str
    is_published: StrictBool


class PrivatePatchVacancy(BaseVacancy):
    """
    Model to validate vacancy data to partial update vacancy by admin API.
    
    All fields are optional.
    """


class SearchOptions(BaseModel):
    """Pydantic model to validate serach options."""
    date_from: Optional[date]
    date_to: Optional[date]
    search_query: Optional[str]
    published_only: Optional[bool]

    @validator('date_from', pre=True)
    def validate_date_from_format(cls, date_from):
        """Limits input date formats."""
        return validate_date_field_type(date_from)


class PublicFilterOptions(BaseModel):
    """Model to validate filter options for public API."""
    modified_at: Optional[date]

    @validator('modified_at', pre=True)
    def validate_modified_at_format(cls, modified_at):
        """Limits input date formats."""
        return validate_date_field_type(modified_at)


class PrivateFilterOptions(BaseModel):
    """Model to validate filter options for private API."""
    source_name: Optional[str]
    is_published: Optional[bool]
    modified_at: Optional[date]

    @validator('modified_at', pre=True)
    def validate_modified_at_format(cls, modified_at):
        """Limits input date formats."""
        return validate_date_field_type(modified_at)



