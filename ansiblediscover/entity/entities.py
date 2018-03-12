import logging
import os
import re
from typing import Dict, List, Iterable, Tuple

logger = logging.getLogger(__name__)


class Entities:
    @staticmethod
    def from_paths(paths: Iterable[str]) -> Dict[str, List[str]]:
        entities = {'playbook': [], 'role': []}

        for path in paths:
            try:
                entity_type, entity_name = Entities.from_path(path)
                entities[entity_type].append(entity_name)
            except ValueError as e:
                logger.warning(e)

        return entities

    @staticmethod
    def from_path(path: str, curdir: str = os.curdir) -> Tuple[str, str]:
        if len(path.strip()) == 0:
            raise ValueError('Blank path')

        path_rel_to_curdir = os.path.relpath(path, start=curdir)

        if os.path.dirname(path_rel_to_curdir) in {'', '.'}:
            file_name = os.path.basename(path)
            name_search = re.search('^(.+)\.yml$', file_name)
            if name_search is None or len(name_search.groups()) == 0:
                raise ValueError(
                    'File path indicated a playbook, but filename does not path pattern ^.+\.yml$ for: {}'.format(
                        file_name, ))
            return 'playbook', name_search.group(1)

        file_path_parts = path_rel_to_curdir.split(os.sep)
        if file_path_parts[0] == 'roles':
            if len(file_path_parts) >= 2:
                return 'role', str(file_path_parts[1])

        raise ValueError('Unsupported file type or location: {}'.format(path,))
