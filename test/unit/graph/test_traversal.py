import pytest
from typing import Dict, Set, Union

from ansiblediscover.graph.node import Node
from ansiblediscover.graph.traversal import Traversal


DAG = Dict[str, Union[str, 'DAG']]


class NodeStub(Node):
    def __init__(self, name: str):
        Node.__init__(self, name, 'role', '')

    @staticmethod
    def build_dag(hierarchy: DAG) -> Dict[Union[int, str], Set['NodeStub']]:
        nodes = {}
        nodes.setdefault('leafs', set())
        nodes.setdefault('all', set())

        return NodeStub._build_dag(hierarchy, nodes)

    @staticmethod
    # TODO How to properly type recurring data structures?
    def _build_dag(hierarchy: Dict[str, dict],
                   nodes: Dict[Union[int, str], Set['NodeStub']],
                   level: int = 0):
        nodes.setdefault(level, set())

        for name in hierarchy:
            # TODO Fixme: linear-time search
            if any(name == node.name for node in nodes['all']):
                continue

            if len(hierarchy[name]) == 0:
                leaf = NodeStub(name)

                nodes[level].add(leaf)
                nodes['leafs'].add(leaf)
                nodes['all'].add(leaf)

                continue

            node = NodeStub(name)
            nodes[level].add(node)
            nodes['all'].add(node)

            NodeStub._build_dag(hierarchy[name], nodes, level + 1)
            for child in nodes[level + 1]:
                node.add_successor(child)

        return nodes


@pytest.fixture(params=[
    {},
    {'0': {}},
    {'0': {'00': {}, '01': {}}},
    {'0': {'00': {}, '01': {'010': {'0100': {}}}}},
    {'0': {'00': {}, '01': {}}, '1': {'10': {}}},
    {'0': {'00': {'000': {'0000': {}}, '001': {}}}, '1': {'10': {'000': {'0000': {}}}}},
], ids=[
    'no nodes',
    'single root',
    'only one level',
    'balanced tree',
    'unbalanced tree',
    'dag',
])
def f_hierarchy(request):
    return request.param


def test_succ_traversal_all(f_hierarchy):
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_successors = sorted(n.name for n in nodes['all'] - nodes[0])
    assert expected_successors == sorted(n.name for n in Traversal.all(nodes[0], (lambda n: n.successors)))


def test_succ_traversal_direct(f_hierarchy):
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_successors = sorted(n.name for n in nodes.get(1, []))
    assert expected_successors == sorted(n.name for n in Traversal.direct(nodes[0], (lambda n: n.successors)))


def test_succ_traversal_leafs(f_hierarchy):
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_successors = sorted(n.name for n in nodes['leafs'] - nodes[0])
    assert expected_successors == sorted(n.name for n in Traversal.leafs(nodes[0], (lambda n: n.successors)))


def test_pred_traversal_all(f_hierarchy):
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_predecessors = sorted(n.name for n in nodes['all'] - nodes['leafs'])
    assert expected_predecessors == sorted(n.name for n in Traversal.all(nodes['leafs'], (lambda n: n.predecessors)))


def test_pred_traversal_direct(f_hierarchy):
    pred_func = (lambda n: n.predecessors)
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_predecessors = sorted(set(pred.name for n in nodes['leafs'] for pred in pred_func(n)))
    assert expected_predecessors == sorted(n.name for n in Traversal.direct(nodes['leafs'], pred_func))


def test_pred_traversal_leafs(f_hierarchy):
    pred_func = (lambda n: n.predecessors)
    nodes = NodeStub.build_dag(f_hierarchy)
    expected_predecessors = sorted(n.name for n in nodes[0] - nodes['leafs'])
    assert expected_predecessors == sorted(n.name for n in Traversal.leafs(nodes['leafs'], pred_func))
