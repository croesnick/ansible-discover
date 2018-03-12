from abc import ABC, abstractmethod


class EntityFactoryABC(ABC):
    def __key__(self):
        return self.typestring, self.name, self.path

    def __str__(self):
        return str(self.__key__())

    def __eq__(self, other):
        return type(self) == type(other) and self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())

    def is_valid(self) -> bool:
        return all(attrib is not None for attrib in [self.path, self.name])

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @property
    @abstractmethod
    def typestring(self) -> str:
        pass

    @abstractmethod
    def build(self) -> 'EntityFactoryABC':
        pass
