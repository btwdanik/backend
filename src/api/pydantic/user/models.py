from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Mapped


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserSchemaResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserSchemaLogin(BaseModel):
    username: str
    password: str

class UserSchemaAccessToken(BaseModel):
    sub: str

class UserSchemaRefreshToken(BaseModel):
    sub: str

class TokenAccessResponse(BaseModel):
    access_token: str
    token_type: str