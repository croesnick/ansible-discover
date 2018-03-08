import logging
import os
import re
from typing import List, NoReturn, Optional, Set

from ansiblediscover.utils.fs import FS
from ansiblediscover.entity.role.meta import Meta
from ansiblediscover.entity.role.tasks import Tasks

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
        except OSError:
            pass

    @staticmethod
    def build_tasks(role_path: str) -> Optional['Tasks']:
        try:
            return Tasks.build(role_path)
        except RuntimeError as e:
            logger.warning('role {}: skipping role due to loading/parsing error. Details: {}'.format(role_path, str(e)))

    @staticmethod
    def normalize_role_name(name: str) -> str:
        if name.endswith('.yml'):
            return re.search('^(.+)\.yml$', name).group(1)
        return name

    def dependencies(self) -> List[str]:
        dependencies = []
        if self.tasks is not None:
            dependencies += self.tasks.dependencies()
        if self.meta is not None:
            dependencies += self.meta.dependencies()

        return list(set(Role.normalize_role_name(dependency) for dependency in dependencies))
