from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class UserUpdateResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    user_role: str
    created_at: Optional[datetime] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    #full_name: Optional[str] = None

    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters')
        return value

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters')
        return value

    # @field_validator('full_name')
    # def validate_full_name(cls, value: Optional[str]) -> Optional[str]:
    #     if value is None:
    #         return value
    #     value = value.strip()
    #     if not value:
    #         raise ValueError('Name cannot be empty')
    #     return value

class UserPublic(BaseModel):
    username: str
    user_role: str


    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('Username cannot be empty')
        return value
    
    @field_validator('user_role')
    def validate_user_role(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError('User_role cannot be empty')
        return value

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    new_username: str = Field(..., min_length=3, max_length=20)



class UserUpdateResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    user_role: str
    created_at: Optional[datetime] = None