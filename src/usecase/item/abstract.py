from abc import ABC, abstractmethod

from api.pydantic.item.models import ItemSchema

class AbstractCreateItemUC(ABC):
    @abstractmethod
    def create(self, schema: ItemSchema, token: str):
        pass
    @abstractmethod
    def get(self, number: int, token: str):
        pass
    @abstractmethod
    def gets(self, limits: int, offset: int, token: str):
        pass
    @abstractmethod
    def delete(self, number: int, token: str):
        pass
    @abstractmethod
    def update(self, number: int, schema: ItemSchema, token: str):
        pass
