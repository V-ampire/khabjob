"""
Validation requests and responses data.
"""
from pydantic import BaseModel


class Vacancy(BaseModel):
    """Pydantic model to validate vacancy data."""
    id: int
    modified_at: date
    name: str
    source: Optional[str]
    source_name: str
    description: Optional[str]
    is_published: bool