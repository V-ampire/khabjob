from pydantic import (
    BaseModel, 
    ValidationError,
    validator,
)

import re
from typing import Optional


DEFAULT_PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'


class UserCredentials(BaseModel):
    username: str
    password: str

    class Config:
        extra = 'forbid'


class ResetPasswordData(BaseModel):
    username: str
    old_password: str
    new_password1: str
    new_password2: str

    @validator('new_password1')
    def validate_password_format(cls, password):
        validate_password_format(password)
        return password

    @validator('new_password2')
    def validate_passwords_match(cls, password2, values):
        password1 = values.get('new_password1')
        if password1 != password2:
            raise ValueError('Password mismatch.')


def validate_password_format(password: str, pattern: Optional[str]=None):
    """Validate password by regexp pattern."""
    pattern = pattern or DEFAULT_PASSWORD_PATTERN
    result = re.match(pattern, password)
    if result is None:
        raise ValueError(
            'Password too weak. Password must contain at least eight characters,'
            'at least one number and both lower and uppercase letters,'
            'and special characters.'
        )
    
    


        


