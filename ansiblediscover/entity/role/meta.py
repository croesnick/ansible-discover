import logging
import os
from typing import List, Optional

logger = logging.getLogger(__name__)


class Meta:
    def __init__(self, content: Optional[dict], role_path: str):
        self.role_path = role_path
        self.content = content

    @staticmethod
    def path_main(role_path: str):
        return os.path.join(role_path, 'meta', 'main.yml')

    def dependencies(self) -> List[str]:
        if self.content is None:
            return []

        dependencies = self.content.get('dependencies', [])
        if dependencies is None:
            return []

        dependencies_normalized = set()

        for dependency in dependencies:
            if type(dependency) == str:
                dependencies_normalized.add(dependency)

            elif type(dependency) == dict:
                if 'role' not in dependency:
                    logger.debug(
                        'role {}: ignoring dependency in meta without a specified role dependency: '.format(
                            self.role_path, dependency))
                    continue
                dependencies_normalized.add(dependency['role'])

            else:
                logger.warning(
                    'role {}: can\'t read dependency from meta due to unexpected format: {}'.format(
                        self.role_path, dependency))

        return sorted(list(dependencies_normalized))
