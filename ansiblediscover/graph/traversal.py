import logging
from typing import Callable, Set

from ansiblediscover.graph.node import Node

logger = logging.getLogger(__name__)


class Traversal:
    @staticmethod
    def direct(nodes: Set[Node], succ: Callable[[Node], Set[Node]]):
        return {successor for node in nodes for successor in succ(node)}

    @staticmethod
    def all(nodes: Set[Node], succ: Callable[[Node], Set[Node]]):
        nodes_to_visit = {successor for node in nodes for successor in succ(node)}
        all_nodes = set()

        while len(nodes_to_visit) > 0:
            all_nodes.update(nodes_to_visit)
            nodes_to_visit = {successor for node in nodes_to_visit for successor in succ(node)}

        return all_nodes

    @staticmethod
    def leafs(nodes: Set[Node], succ: Callable[[Node], Set[Node]]):
        nodes_to_visit = {successor for node in nodes for successor in succ(node)}
        all_nodes = set()

        while len(nodes_to_visit) > 0:
            leafs = {node for node in nodes_to_visit if len(succ(node)) == 0}
            all_nodes.update(leafs)

            nodes_to_visit = {successor for node in nodes_to_visit for successor in succ(node)}

        return all_nodes
