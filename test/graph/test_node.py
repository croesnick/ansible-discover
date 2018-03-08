from ansiblediscover.graph.node import Node


def test_build_identifier():
    assert 'role:server_base' == Node.build_identifier('server_base', 'role')


def test_identifier():
    node = Node('server_base', 'role', 'irrelevant')
    assert 'role:server_base' == node.identifier()


def test_add_successor():
    parent = Node('appserver', 'playbook', 'appserver.yml')
    child = Node('server_base', 'role', 'roles/server_base')

    parent.add_successor(child)

    assert child in parent.successors
    assert parent in child.predecessors


def test_add_predecessor():
    parent = Node('appserver', 'playbook', 'appserver.yml')
    child = Node('server_base', 'role', 'roles/server_base')

    child.add_predecessor(parent)

    assert child in parent.successors
    assert parent in child.predecessors
