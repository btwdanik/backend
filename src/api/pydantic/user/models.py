from pydantic import BaseModel, EmailStr
from enum import Enum
# from fastapi import HTTPException
# from typing import List

class Info(str, Enum):
    user_id_info = 'Info of ID user'
    user_create = 'Create user'
    user_delete = 'Delete user'

class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    title: str = None

class UserSchemaResponse(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    title: str