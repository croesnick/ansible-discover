import logging
import os
import re
from fnmatch import fnmatch
from typing import Dict

from ansiblediscover.graph.node import Node
from ansiblediscover.entity.playbook import Playbook
from ansiblediscover.entity.role import Role

logger = logging.getLogger(__name__)


class Dependencies:
    @staticmethod
    def discover() -> Dict[str, 'Node']:
        logger.debug("Testing debug")
        dependency_map = {}

        files = os.listdir('.')
        playbooks = [file for file in files if fnmatch(file, '*.yml')]

        for playbook in playbooks:
            try:
                model = Playbook.build(playbook)
            except RuntimeError as e:
                logger.warning(str(e))
                continue
            else:
                name = re.search('^(.+)\.yml$', playbook).group(1)

                playbook_node = Node(name, 'playbook', playbook)
                logger.debug('Adding playbook to dependency map: {}'.format(name))
                dependency_map[playbook_node.identifier()] = playbook_node

                roles = model.roles_from_plays()

                for role in roles:
                    Dependencies.dive_into_role_and_relate(role, playbook_node, dependency_map)

        return dependency_map

    @staticmethod
    def dive_into_role_and_relate(name: str, base_node, dependency_map: Dict[str, 'Node']):
        node = dependency_map.get(Node.build_identifier(name, 'role'), None)

        if node is None:
            logger.debug('Building role path from name: {}'.format(name))
            role_path = os.path.join('roles', name)
            node = Node(name, 'role', role_path)

            dependency_map[node.identifier()] = node

            model = Role.build(role_path)

            if model is None:
                logger.warning('Could not load/locate role at: {}'.format(role_path))
            else:
                for dependent_role in model.dependencies():
                    Dependencies.dive_into_role_and_relate(dependent_role, node, dependency_map)

        if base_node is not None:
            base_node.add_successor(node)
