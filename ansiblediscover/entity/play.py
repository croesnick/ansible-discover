import logging
from typing import Any, Dict, List, Tuple, Union

from ansiblediscover.entity.role import RoleFactory
from ansiblediscover.entity.tasklist import TasklistFactory

logger = logging.getLogger(__name__)


class Play:
    def __init__(self, roles: List[RoleFactory] = list(), tasklists: List[TasklistFactory] = list()):
        self._roles = roles
        self._tasklists = tasklists

    @staticmethod
    def build(play: Dict[str, list]) -> 'Play':
        if len(play) == 0:
            return Play()

        roles = Play.parse_roles(play.get('roles', []))
        tasklists = []

        for task_type in ['pre_tasks', 'tasks', 'post_tasks']:
            rs, tls = Play.parse_tasks(play.get(task_type, []))
            roles += rs
            tasklists += tls

        # TODO Unique the lists of roles and tasklists before building a Play
        return Play(roles, tasklists)

    @staticmethod
    def parse_roles(roles: List[Union[str, Dict[str, Any]]]) -> List[RoleFactory]:
        rs = []

        for role in roles:
            try:
                role_name = Play.parse_role(role)
            except ValueError as e:
                logger.info(str(e))
            else:
                rs.append(RoleFactory(role_name))

        return rs

    @staticmethod
    def parse_role(role: Union[str, Dict[str, Any]]) -> str:
        if type(role) is str:
            return role
        if type(role) is dict:
            name = role.get('role', None)
            if name is not None:
                return name

        raise ValueError('Role usage in play does not properly reference a role: {}'.format(role))

    @staticmethod
    def parse_tasks(tasks: List[dict]) -> Tuple[List[RoleFactory], List[TasklistFactory]]:
        roles = []
        tasklists = []

        # for task in tasks:
        #     if type(task) != dict or len(task) == 0:
        #         continue
        #
        #     if 'block' in task:
        #         for block_task in task['block']:
        #             include = Play.build_include(block_task)
        #             if include is None:
        #                 continue
        #             includes[include.identifier()] = include
        #     else:
        #         include = IncludesList.build_include(task)
        #         if include is not None:
        #             includes[include.identifier()] = include
        return [], []

    # @staticmethod
    # def build_include(task: Dict[str, Any]) -> Optional[Union[RoleInclude, TaskInclude]]:
    #     if not Include.is_include(task):
    #         return
    #
    #     try:
    #         include = Include.build(task)
    #     except ValueError as e:
    #         logger.warning(str(e))
    #     else:
    #         return include

    @property
    def dependencies(self):
        return self.role_dependencies + self.tasklist_dependencies

    @property
    def role_dependencies(self):
        return self._roles

    @property
    def tasklist_dependencies(self):
        return self._tasklists
