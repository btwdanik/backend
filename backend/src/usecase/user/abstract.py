from abc import ABC, abstractmethod
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.api.pydantic.user.models import UserSchema

class AbstractCreateUserUC(ABC):
    @abstractmethod
    def create(self, schema: UserSchema):
        pass
    @abstractmethod
    def login(self, schema: OAuth2PasswordRequestForm):
        pass
    @abstractmethod
    def get(self, number: int):
        pass
