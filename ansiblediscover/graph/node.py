import logging

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, node_name: str, node_type: str, node_path: str):
        self.name = node_name
        self.node_type = node_type
        self.path = node_path

        self.predecessors = set()
        self.successors = set()

    @staticmethod
    def build_identifier(node_name: str, node_type: str):
        return '{}:{}'.format(node_type, node_name)

    def identifier(self):
        return '{}:{}'.format(self.node_type, self.name)

    def add_successor(self, node: 'Node'):
        self.successors.add(node)
        node.predecessors.add(self)

    def add_predecessor(self, node: 'Node'):
        self.predecessors.add(node)
        node.successors.add(self)
