import logging
import os
from typing import List

from ansiblediscover.utils.fs import FS

logger = logging.getLogger(__name__)


class Tasks:
    TASK_INCLUDE_STATEMENTS = ['include', 'include_tasks', 'import_tasks']
    ROLE_INCLUDE_STATEMENTS = ['include_role', 'import_role']

    def __init__(self, content: List[List[dict]], role_path: str):
        self.role_path = role_path
        self.content = content

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
                    'role {}: skipping task include {} due to error: {}'.format(role_path, task, str(e)))

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
                if statement not in Tasks.TASK_INCLUDE_STATEMENTS:
                    continue
                if type(argument) != str:
                    logger.warning('Skipping task include {} as it is malformed: {}'.format(statement, argument))
                    continue

                includes.add(argument)
                break

        return list(includes)

    @staticmethod
    def tasks_path(role_path: str) -> str:
        return os.path.join(role_path, 'tasks')

    @staticmethod
    def task_path(role_path: str, task: str) -> str:
        return os.path.join(Tasks.tasks_path(role_path), task)

    @staticmethod
    def main_path(role_path: str) -> str:
        return Tasks.task_path(role_path, 'main.yml')

    def dependencies(self) -> List[str]:
        return list(set(argument
                        for tasks in self.content
                        for task in tasks
                        for (statement, argument) in task.items()
                        if statement in Tasks.ROLE_INCLUDE_STATEMENTS and type(argument) == str))
