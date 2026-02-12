from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserSchemaResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserSchemaAccessToken(BaseModel):
    id: int
    sub: str

class UserSchemaRefreshToken(BaseModel):
    sub: str

class TokenAccessResponse(BaseModel):
    access_token: str
    token_type: str