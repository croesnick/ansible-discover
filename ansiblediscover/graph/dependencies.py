import logging
import os
from fnmatch import fnmatch
from typing import Dict

from ansiblediscover.graph.node import Node
from ansiblediscover.entity.playbook import PlaybookOrTasklistFactory

logger = logging.getLogger(__name__)


class Dependencies:
    @staticmethod
    def discover() -> Dict[str, 'Node']:
        files = os.listdir('.')

        dependency_map = {}
        processing_queue = {PlaybookOrTasklistFactory(file) for file in files if fnmatch(file, '*.yml')}

        # TODO #GH-10 Add roles to the initial processing queue
        # processing_queue += [RoleInclude(path) for path in roles_path if ...]

        while processing_queue:
            entity = processing_queue.pop()
            identifier = Node.build_identifier(entity.name, entity.typestring)

            logger.debug('Processing entity type={} name={}'.format(entity.typestring, entity.name))

            if identifier in dependency_map:
                node = dependency_map[identifier]
            else:
                node = Node(entity.name, entity.typestring, entity.path)
                dependency_map[identifier] = node

            # TODO model.build() should raise if something weird happens instead of swallowing any exception.
            model = entity.build()
            if model is None:
                logger.warning('Entity type={} name={} not supported. Ignoring.'.format(entity.typestring, entity.name))
                continue

            for dependency in model.dependencies():
                dependency_identifier = Node.build_identifier(dependency.name, dependency.typestring)

                if dependency_identifier in dependency_map:
                    dependency_node = dependency_map[dependency_identifier]
                else:
                    dependency_node = Node(dependency.name, dependency.typestring, dependency.path)
                    dependency_map[dependency_identifier] = dependency_node

                node.add_successor(dependency_node)
                processing_queue.add(dependency)

        return dependency_map
