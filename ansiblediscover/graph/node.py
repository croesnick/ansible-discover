import logging

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, name: str, typestring: str, path: str):
        self.name = name
        self.typestring = typestring
        self.path = path

        self.predecessors = set()
        self.successors = set()

    def __key__(self):
        return self.typestring, self.name, self.path

    def __str__(self):
        return str(self.__key__())

    def __eq__(self, other):
        return type(self) == type(other) and self.__key__() == other.__key__()

    def __hash__(self):
        return hash(self.__key__())

    @staticmethod
    def build_identifier(node_name: str, node_type: str):
        return '{}:{}'.format(node_type, node_name)

    def identifier(self):
        return '{}:{}'.format(self.typestring, self.name)

    def add_successor(self, node: 'Node'):
        self.successors.add(node)
        node.predecessors.add(self)

    def add_predecessor(self, node: 'Node'):
        self.predecessors.add(node)
        node.successors.add(self)
