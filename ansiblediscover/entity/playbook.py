import logging
import os
import re
from typing import Any, Dict, List, Optional, Union

from ansiblediscover.utils.fs import FS
from ansiblediscover.entity import EntityFactoryABC
from ansiblediscover.entity.play import Play
from ansiblediscover.entity.role import RoleFactory
from ansiblediscover.entity.tasklist import TasklistFactory

logger = logging.getLogger(__name__)


class Playbook:
    PLAYBOOK_IMPORT_STATEMENTS = ['include', 'import_playbook']

    def __init__(self, content: list, path: str):
        self.content = content
        self.path = path

    @staticmethod
    def build(path: str) -> 'Playbook':
        try:
            content = FS.load_yaml(path)
            return Playbook(content, path) if content is not None else None
        except (TypeError, OSError) as e:
            raise RuntimeError(e)

    @staticmethod
    def extract_name(path: str) -> str:
        return re.search('^(.+)\.yml$', path).group(1)

    def name(self) -> str:
        return Playbook.extract_name(self.path)

    def dependencies(self) -> List['EntityFactoryABC']:
        return self.playbook_dependencies() + self.play_dependencies()

    def playbook_dependencies(self) -> List['PlaybookFactory']:
        def first_matching_import(play: Dict[str, Any], keys: List[str]) -> Optional[str]:
            for key in keys:
                if key in play:
                    return play[key]

        dependencies = set()

        for play in self.content:
            dependency = first_matching_import(play, Playbook.PLAYBOOK_IMPORT_STATEMENTS)
            if dependency is None:
                continue
            if type(dependency) != str:
                logger.debug('Ignoring malformed playbook import statement in play: {}'.format(play))
                continue
            if not dependency.endswith('.yml'):
                logger.debug('Ignoring playbook import with unsupported file type: {}'.format(dependency))
                continue

            dependencies.add(dependency)

        return [PlaybookFactory(path) for path in dependencies]

    def play_dependencies(self) -> List[Union[RoleFactory, TasklistFactory]]:
        dependencies = []

        for play in self.content:
            play_model = Play.build(play)
            dependencies += play_model.dependencies

        return dependencies


class PlaybookFactory:
    def __init__(self, path: str):
        self._path = path
        self._name = None

    def is_valid(self) -> bool:
        return all(attrib is not None for attrib in [self.path, self.name])

    @property
    def path(self):
        return self._path

    @property
    def name(self) -> str:
        if self._name is None:
            match = re.match('^(.+)\.yml$', os.path.basename(self.path))
            self._name = match.group(1) if match is not None else None
        return self._name

    @property
    def typestring(self) -> str:
        return 'playbook'

    def build(self) -> Optional['Playbook']:
        try:
            return Playbook.build(self.path)
        except RuntimeError as e:
            logger.warning(str(e))


class PlaybookOrTasklistFactory:
    def __init__(self, path: str):
        self.path = path
        self._data = None
        self._typestring = None
        self._name = None

    def is_valid(self) -> bool:
        return all(attrib is not None for attrib in [self.path, self.name, self.typestring])

    @property
    def name(self) -> str:
        if self._name is None:
            matches = re.match('^(.+)\.yml$', os.path.basename(self.path))
            if matches is not None:
                self._name = matches.group(1)
        return self._name

    # TODO Should return None if file is of bad format
    @property
    def typestring(self) -> Optional[str]:
        if self._typestring is None:
            self._typestring = 'tasklist'

            for play in self.data:
                if any(stmt in play for stmt in
                       ['hosts', 'pre_tasks', 'tasks', 'post_tasks', 'roles'] + Playbook.PLAYBOOK_IMPORT_STATEMENTS):
                    self._typestring = 'playbook'
                    break

        return self._typestring

    @property
    def data(self) -> List[dict]:
        if self._data is None:
            try:
                self._data = FS.load_yaml(self.path)
                if self._data is None:
                    self._data = []
            except (TypeError, OSError) as e:
                logger.warning(str(e))
                self._data = []

        return self._data

    # TODO Support tasklist includes/imports on playbook level
    def build(self) -> Optional['Playbook']:
        if self.typestring == 'playbook':
            try:
                return Playbook.build(self.path)
            except RuntimeError as e:
                # TODO Currently dead branch as `typestring` through `data` catches read/parse errors
                logger.warning(str(e))
