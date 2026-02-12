from abc import ABC, abstractmethod
from api.pydantic.user.models import UserSchema, UserSchemaLogin


class AbstractCreateUserUC(ABC):
    @abstractmethod
    def create(self, schema: UserSchema):
        pass
    @abstractmethod
    def login(self, schema: UserSchemaLogin):
        pass
    @abstractmethod
    def get(self, number: int):
        pass
