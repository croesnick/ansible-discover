import pytest

from ansiblediscover.entity.role import RoleFactory
from ansiblediscover.entity.task import Task


@pytest.mark.parametrize('task, expected', [
    ({}, []),
    ({'include_role': {'name': 'foo'}}, [RoleFactory('foo')]),
    ({'block': [{}]}, []),
    ({'block': [
        {'include_role': {'name': 'foo'}},
        {'import_role': {'name': 'bar', 'tasks_from': 'install.yml'}},
    ]}, [RoleFactory('foo'), RoleFactory('bar', 'install.yml')]),
])
def test_dependencies(task, expected):
    assert set(expected) == set(Task.dependencies(task))


@pytest.mark.parametrize('task, expected', [
    ({}, None),
    ({'debug': 'msg'}, None),
    ({'include': 'foo'}, None),
    ({'include_tasks': 'foo'}, None),
    ({'include_role': 'foo'}, None),
    ({'include_role': {'irrelevant': 'foo'}}, None),
    ({'include_role': {'name': 'foo'}}, RoleFactory('foo')),
    ({'include_role': {'name': 'foo', 'tasks_from': 'install.yml'}}, RoleFactory('foo', 'install.yml')),
    ({'import_playbook': 'foo'}, None),
    ({'import_tasks': 'foo'}, None),
    ({'import_role': 'foo'}, None),
    ({'import_role': {'irrelevant': 'foo'}}, None),
    ({'import_role': {'name': 'foo'}}, RoleFactory('foo')),
    ({'import_role': {'name': 'foo', 'tasks_from': 'install.yml'}}, RoleFactory('foo', 'install.yml')),
])
def test_dependency(task, expected):
    assert expected == Task.dependency(task)


@pytest.mark.parametrize('task, keys, expected_key', [
    ({}, [], None),
    ({'foo': 'bar'}, [], None),
    ({'foo': 'bar'}, ['missing'], None),
    ({'foo': 'bar'}, ['missing', 'irrelevant'], None),
    ({}, ['foo'], None),
    ({'foo': 'bar'}, ['foo'], 'foo'),
    ({'foo': 1, 'bar': 2, 'baz': 3}, ['foo', 'missing', 'bar', 'irrelevant', 'baz'], 'foo'),
    ({'foo': 1, 'bar': 2, 'baz': 3}, ['missing', 'bar', 'foo', 'irrelevant', 'baz'], 'bar'),
])
def test_any_matching_key(task, keys, expected_key):
    assert expected_key == Task.any_matching_key(task, keys)
