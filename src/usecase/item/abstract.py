from abc import ABC, abstractmethod
from api.pydantic.item.models import ItemSchema


class AbstractCreateItemUC(ABC):
    @abstractmethod
    def create(self, schema: ItemSchema):
        pass
    @abstractmethod
    def get(self, number: int):
        pass
    @abstractmethod
    def gets(self, limits: int, offset: int):
        pass
    @abstractmethod
    def delete(self, number: int):
        pass
    @abstractmethod
    def update(self, number: int, schema: ItemSchema):
        pass
