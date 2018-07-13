import logging
from typing import Dict, Any, List, Optional, Iterable

from ansiblediscover.entity.role import RoleFactory

logger = logging.getLogger(__name__)


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
