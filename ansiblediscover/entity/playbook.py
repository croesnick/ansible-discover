import logging
import re
from typing import Any, Dict, Iterable, List, Optional, Set, Union

from ansiblediscover.utils.fs import FS

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

    @staticmethod
    def role_from_play(role_in_play: Union[str, dict]) -> str:
        # TODO Handle Ansible's "=" syntax if that's allowed here
        if type(role_in_play) is str:
            return role_in_play
        if type(role_in_play) is dict:
            name = role_in_play.get('role', None)
            if name is not None:
                return name

        raise ValueError('Role usage in play does not properly reference a role: {}'.format(role_in_play))

    def playbook_dependencies(self) -> List[str]:
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

        return sorted(list(dependencies))

    def name(self) -> str:
        return Playbook.extract_name(self.path)

    def roles_from_plays(self) -> Set:
        return set(list(self._roles_from_plays()))

    def _roles_from_plays(self) -> Iterable[str]:
        for play in self.content:
            for role in play.get('roles', []):
                try:
                    name = Playbook.role_from_play(role)
                    yield name
                except ValueError as e:
                    logger.warning(str(e))
                    pass

        return
