from abc import ABC, abstractmethod
from api.pydantic.user.models import UserSchema


class AbstractCreateUserUC(ABC):
    @abstractmethod
    def create(self, schema: UserSchema):
        pass
    @abstractmethod
    def get(self, number: int):
        pass
    @abstractmethod
    def delete(self, number: int):
        pass
