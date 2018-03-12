import pytest

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


def test_str():
    name = 'myname'
    typestring = 'mytype'
    path = 'mypath'
    node = Node(name, typestring, path)

    assert str((typestring, name, path)) == str(node)


@pytest.mark.parametrize('this, other, equal', [
    (('myname', 'mytype', 'mypath'), ('myname', 'mytype', 'mypath'), True),
    (('myname', 'mytype', 'mypath'), ('othername', 'mytype', 'mypath'), False),
    (('myname', 'mytype', 'mypath'), ('myname', 'othertype', 'mypath'), False),
    (('myname', 'mytype', 'mypath'), ('myname', 'othertype', 'otherpath'), False),
])
def test_eq(this, other, equal):
    this_node = Node(*this)
    other_node = Node(*other)

    assert (equal and (this_node == other_node)) or (not equal and (this_node != other_node))


@pytest.mark.parametrize('other', [
    None,
    [],
    ('myname', 'mytype', 'mypath'),
])
def test_eq_unequal_types(other):
    this = Node('myname', 'mytype', 'mypath')
    assert this != other
