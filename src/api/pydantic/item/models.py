from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from typing import List

class Pagination(BaseModel):
    limit: int = Field(10, le=100)
    offset: int = Field(0, ge=0)

categories: List[str] = ['home', 'school', 'college']

class ItemSchemaResponse(BaseModel):
    id: int
    name: str
    category: str
    count: int
    price: int

class ItemSchema(BaseModel):
    name: str
    category: str
    count: int
    price: int

    @field_validator('name')
    @classmethod
    def validate_name(cls, v : str):
        if 30 >= len(v) >= 1:
            return v
        else:
            raise HTTPException(status_code=400, detail=f"Invalid name")

    @field_validator('category')
    @classmethod
    def validate_category(cls, v : str):
        if v.lower() in categories:
            return v
        else:
            raise HTTPException(status_code=400, detail=f"Invalid category")

    @field_validator('count')
    @classmethod
    def validate_count(cls, v: int):
        if 10**7 >= v >= 0:
            return v
        else:
            raise HTTPException(status_code=400, detail=f"Count must be > 0 and <= 10**6")

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: int):
        if 10**7 >= v > 0:
            return v
        else:
            raise HTTPException(status_code=400, detail=f"Price must be > 0 and <= 10**7")