import logging
import yaml
from typing import Iterable, Set, Union

logger = logging.getLogger(__name__)


class Playbook:
    def __init__(self, contents: list):
        self.contents = contents

    @staticmethod
    def from_file(path: str) -> 'Playbook':
        with open(path) as fh:
            raw_content = fh.read()
            yaml_content = yaml.load(raw_content)
            return Playbook(yaml_content)

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

    def roles_from_plays(self) -> Set:
        return set(list(self._roles_from_plays()))

    def _roles_from_plays(self) -> Iterable[str]:
        for play in self.contents:
            for role in play.get('roles', []):
                try:
                    name = Playbook.role_from_play(role)
                    yield name
                except ValueError as e:
                    logger.warning(str(e))
                    pass

        return
        yield

