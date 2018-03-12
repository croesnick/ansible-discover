import logging
import os
import re
from typing import Any, Dict, List, Optional, Iterable

from ansiblediscover.entity import EntityFactoryABC
from ansiblediscover.utils.fs import FS

logger = logging.getLogger(__name__)


class Role:
    def __init__(self, tasks: Optional['Tasks'], meta: Optional['Meta'], role_path: str):
        self.tasks = tasks
        self.meta = meta
        self.role_path = role_path

    @staticmethod
    def build(role_path: str) -> Optional['Role']:
        if not os.path.exists(role_path):
            logger.warning('Could not find role at path: {}. Ignoring.'.format(role_path))
            return

        tasks = Role.build_tasks(role_path)
        meta = Role.build_meta(role_path)

        return Role(tasks, meta, role_path)

    @staticmethod
    def build_meta(role_path: str) -> Optional['Meta']:
        try:
            content = FS.load_yaml(Meta.main_path(role_path))
            return Meta(content, role_path) if content is not None else None
        except TypeError as e:
            logger.warning(str(e))
        except OSError as e:
            logger.debug(str(e))

    @staticmethod
    def build_tasks(role_path: str) -> 'Tasks':
        try:
            return Tasks.build(role_path)
        except RuntimeError as e:
            logger.warning('role {}: skipping role due to loading/parsing error. Details: {}'.format(role_path, str(e)))

    @staticmethod
    def normalize_role_name(name: str) -> str:
        if name.endswith('.yml'):
            return re.search('^(.+)\.yml$', name).group(1)
        return name

    def dependencies(self) -> List['EntityFactoryABC']:
        dependencies = []

        if self.meta is not None:
            dependencies += self.meta.dependencies()

        if self.tasks is not None:
            dependencies += self.tasks.dependencies()

        return dependencies


class Meta:
    def __init__(self, content: Optional[dict], role_path: str):
        self.role_path = role_path
        self.content = content

    @staticmethod
    def main_path(role_path: str):
        return os.path.join(role_path, 'meta', 'main.yml')

    def dependencies(self) -> List['RoleFactory']:
        if self.content is None:
            return []

        dependencies = self.content.get('dependencies', [])
        if dependencies is None:
            return []

        roles = set()

        for dependency in dependencies:
            if type(dependency) == str:
                roles.add(dependency)

            elif type(dependency) == dict:
                if 'role' not in dependency:
                    logger.debug(
                        'role {}: ignoring dependency in meta without a specified role dependency: '.format(
                            self.role_path, dependency))
                    continue
                roles.add(dependency['role'])

            else:
                logger.warning(
                    'role {}: can\'t read dependency from meta due to unexpected format: {}'.format(
                        self.role_path, dependency))

        return [RoleFactory(role) for role in roles]


class Tasks:
    def __init__(self, content, role_path):
        self._content = content
        self._role_path = role_path

    @staticmethod
    def build(role_path: str) -> 'Tasks':
        content = []

        main_content = Tasks.build_task(Tasks.main_path(role_path))
        content.append(main_content)

        includes = Tasks.task_includes(main_content)
        logger.debug('role {}: main.yml dependencies: {}'.format(role_path, includes))

        while includes:
            task = includes.pop()
            logger.debug('role {}: reading task include {}'.format(role_path, task))

            try:
                task_content = Tasks.build_task(Tasks.task_path(role_path, task))
                content.append(task_content)

                task_includes = Tasks.task_includes(task_content)
                includes += task_includes
            except RuntimeError as e:
                logger.error(
                    'role {}: task include {} due to error: {}'.format(role_path, task, str(e)))

        return Tasks(content, role_path)

    @staticmethod
    def build_task(task_path: str) -> List[dict]:
        try:
            content = FS.load_yaml(task_path)
        except (TypeError, OSError) as e:
            raise RuntimeError('role task {}: load/parse failure. Details: {}'.format(task_path, str(e)))
        else:
            if content is None:
                return []
            if type(content) != list:
                raise ValueError(
                    'role task {}: expected content to be a list, got: {}'.format(task_path, type(content)))

            return content

    @staticmethod
    def task_includes(content: List[dict]) -> List[str]:
        includes = set()

        for task in content:
            for (statement, argument) in task.items():
                if statement not in Task.TASK_INCLUDE_STATEMENTS:
                    continue
                if type(argument) != str:
                    logger.warning('Skipping task include {} as it is malformed: {}'.format(statement, argument))
                    continue

                includes.add(argument)
                break

        return list(includes)

    @property
    def content(self):
        return self._content

    @property
    def role_path(self):
        return self._role_path

    @staticmethod
    def tasks_path(role_path: str) -> str:
        return os.path.join(role_path, 'tasks')

    @staticmethod
    def task_path(role_path: str, task: str) -> str:
        return os.path.join(Tasks.tasks_path(role_path), task)

    @staticmethod
    def main_path(role_path: str) -> str:
        return Tasks.task_path(role_path, 'main.yml')

    def dependencies(self) -> List['EntityFactoryABC']:
        dependencies = set()
        for task in self._content:
            dependencies.update(Task.dependencies(task))

        return list(dependencies)


class Task:
    TASK_INCLUDE_STATEMENTS = {'include', 'include_tasks', 'import_tasks'}
    ROLE_INCLUDE_STATEMENTS = {'include_role', 'import_role'}

    @staticmethod
    def dependencies(task: Dict[str, Any]) -> List['EntityFactoryABC']:
        if type(task) != dict or len(task) == 0:
            return []

        dependencies = set()

        if 'block' in task:
            for block_task in task['block']:
                dependency = Task.dependency(block_task)
                if dependency is not None:
                    dependencies.add(dependency)
        else:
            dependency = Task.dependency(task)
            if dependency is not None:
                dependencies.add(dependency)

        return list(dependencies)

    @staticmethod
    def dependency(task: Dict[str, Any]) -> Optional['EntityFactoryABC']:
        # TODO Ignore includes within roles for now.
        #      We currently only handle the simple case of task include in role means a file from
        #      within the role's tasks/ directory.
        #
        # task_include_stmt = Task.first_matching_include_stmt(task, Task.TASK_INCLUDE_STATEMENTS)
        # if task_include_stmt:
        #     name = task[task_include_stmt]
        #
        #     if type(name) != str:
        #         logger.warning('task include argument is of unexpected format/type: {}'.format(task))
        #     elif not name.endswith('.yml'):
        #         logger.warning('task include has to have a .yml suffix, got: {}'.format(name))
        #     else:
        #         from ansiblediscover.entity.tasklist import TasklistFactory
        #         return TasklistFactory(name)
        #
        #     return

        role_include_stmt = Task.any_matching_key(task, Task.ROLE_INCLUDE_STATEMENTS)
        if role_include_stmt:
            include = task[role_include_stmt]

            if type(include) != dict:
                logger.warning('role include arguments are of unexpected format/type: {}'.format(task))
            elif 'name' not in include:
                logger.warning('role include is missing expected argument "name": {}'.format(task))
            else:
                return RoleFactory(include['name'], include.get('tasks_from', 'main.yml'))

    @staticmethod
    def any_matching_key(task: Dict[str, Any], keys: Iterable[str]) -> Optional[str]:
        for key in keys:
            if key in task:
                return key


class RoleFactory(EntityFactoryABC):
    def __init__(self, name: str, main_task: str = 'main.yml'):
        self._name = name
        # TODO Not evaluated so far! Must also be part of __eq__.
        self._main_task = main_task

    @property
    def name(self):
        return self._name

    @property
    def main_task(self):
        return self._main_task

    @property
    def path(self):
        if self.name is None:
            return

        return os.path.join('roles', self.name)

    @property
    def typestring(self):
        return 'role'

    def build(self):
        return Role.build(self.path)
