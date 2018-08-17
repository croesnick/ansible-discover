import logging
import os
from typing import Any, Dict, List

from ansiblediscover.entity import EntityFactoryABC
from ansiblediscover.utils.fs import FS

logger = logging.getLogger(__name__)


class Tasklist:
    def __init__(self, content: List[Dict[str, Any]], path: str) -> 'Tasklist':
        self.content = content
        self.path = path

    @staticmethod
    def build(path: str):
        try:
            content = FS.load_yaml(path)
            return Tasklist(content, path)
        except (OSError, TypeError) as e:
            logger.error(e)

    def dependencies(self) -> List['EntityFactoryABC']:
        return [dependency for task in self.content for dependency in Task.dependencies(task)]


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
        return Tasklist.build(self.path)

from ansiblediscover.entity.task import Task
