from pydantic import BaseModel, Field, field_validator, EmailStr
from enum import Enum
from fastapi import HTTPException
from typing import List

class UserSchema(BaseModel):
    username: str
    email: EmailStr | None
