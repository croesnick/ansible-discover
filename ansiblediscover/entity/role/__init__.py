import logging
import os
import re
import yaml
from typing import List, Optional, Set, Union

logger = logging.getLogger(__name__)


class Role:
    TASK_INCLUDE_STATEMENTS = ['include', 'include_tasks', 'import', 'import_tasks']
    ROLE_INCLUDE_STATEMENTS = ['include_role', 'import_role']

    def __init__(self, contents: list, role_path: str):
        self.contents = contents
        self.role_path = role_path

        self._determine_dependencies()

    @staticmethod
    def is_valid_role_filename(role: str) -> bool:
        return role.endswith('.yml')

    @staticmethod
    def file_to_role_name(filename: str) -> str:
        return re.match('^(.+)\.yml$', filename).group(1)

    @staticmethod
    def from_dir(path: str) -> Optional['Role']:
        try:
            role_path_main = os.path.join(path, 'main.yml')
            content = Role._file_contents(role_path_main)
        except FileNotFoundError:
            logger.warning('Could not find role at path: {}. Ignoring.'.format(path))
        except TypeError as e:
            logger.warning('Could not parse role at path: {}. Ignoring. Details: {}'.format(path, str(e)))
        else:
            return Role(content, path) if type(content) == list else None

    @staticmethod
    def _file_contents(path: str) -> Optional[Union[list, dict]]:
        if not os.path.exists(path):
            raise FileNotFoundError('Attempted to read non-existing file: {}'.format(path))

        with open(path) as fh:
            raw_content = fh.read()
            try:
                return yaml.load(raw_content)
            except yaml.scanner.ScannerError as e:
                raise TypeError('Failed to parse yaml file: {}. Details: {}'.format(path, str(e)))

    @staticmethod
    def task_includes(tasks: list, include_statements: list) -> Set:
        # TODO Remove the None check as only lists are expected.
        if tasks is None or len(tasks) == 0:
            return set()
        return set([includee for task in tasks for (stmt, includee) in task.items() if stmt in include_statements])

    @staticmethod
    def dependencies_from_meta(role_path: str) -> List[str]:
        try:
            content = Role._file_contents(Role.Meta.path_main(role_path))
        except (FileNotFoundError, TypeError) as e:
            logger.warning(str(e))
        else:
            return Role.Meta(content, role_path).dependencies() if content is not None else []

    def _determine_dependencies(self):
        self.dependencies = set()

        self.dependencies.update(self.dependencies_from_meta(self.role_path))
        self.dependencies.update(self.task_includes(self.contents, self.ROLE_INCLUDE_STATEMENTS))
        logger.debug('role {}: main.yml dependencies: {}'.format(self.role_path, self.dependencies))

        task_includes = self.task_includes(self.contents, self.TASK_INCLUDE_STATEMENTS)

        while task_includes:
            task_include = task_includes.pop()
            logger.debug('role {}: reading task include {}'.format(self.role_path, task_include))
            task_include_path = '{path}/{file}'.format(path=self.role_path, file=task_include)
            try:
                task_contents = self._file_contents(task_include_path)

                self.dependencies.update(self.task_includes(task_contents, self.ROLE_INCLUDE_STATEMENTS))
                logger.debug(
                    'role {}: task include {} dependencies: {}'.format(self.role_path, task_include, self.dependencies))
                task_includes.update(self.task_includes(task_contents, self.TASK_INCLUDE_STATEMENTS))
            except TypeError as e:
                logger.error(
                    'role {}: skipping task include {} due to error: {}'.format(self.role_path, task_include, str(e)))

        self.dependencies = [re.search('^(.+)\.yml$', dependency).group(1) for dependency in self.dependencies]
