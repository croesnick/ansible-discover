import os

from ansiblediscover.entity import EntityFactoryABC


class Tasklist:
    pass


class TasklistFactory(EntityFactoryABC):
    def __init__(self, path: str):
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    @property
    def typestring(self) -> str:
        return 'tasklist'

    def build(self) -> 'Tasklist':
        pass
