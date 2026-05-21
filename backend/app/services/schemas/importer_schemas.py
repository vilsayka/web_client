from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class ImporterCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=1, max_length=100)
    telephone: str = Field(..., pattern=r'^\+?[0-9\s\-\(\)]+$')
    email: EmailStr

class ImporterPublic(BaseModel):
    id_importer: int
    username: str
    full_name: str
    telephone: str
    email: str
    is_active: bool
    created_at: datetime


    