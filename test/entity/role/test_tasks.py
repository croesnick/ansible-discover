import os
from ruamel import yaml

import pytest

from ansiblediscover.entity.role.tasks import Tasks


@pytest.mark.parametrize('content, expected_dependencies', [
    ([], []),
    ([[]], []),
    ([[{'debug': 'msg'}]], []),
    ([[{'include': 'foo'}]], []),
    ([[{'include_tasks': 'foo'}]], []),
    ([[{'import': 'foo'}]], []),
    ([[{'import_playbook': 'foo'}]], []),
    ([[{'import_tasks': 'foo'}]], []),
    ([[{'import_role': 'foo'}]], ['foo']),
    ([[{'import_role': 'r1'}, {'debug': 'msg'}, {'import_role': 'r2'}]], ['r1', 'r2']),
    ([[{'import_role': 'r1'}, {'debug': 'msg'}], [{'import_role': 'r2'}]], ['r1', 'r2']),
])
def test_dependencies(content, expected_dependencies):
    tasks = Tasks(content, 'irrelevant_path')
    assert sorted(expected_dependencies) == sorted(tasks.dependencies())


def test_tasks_path():
    role_path = os.path.join('path', 'to', 'my', 'role')
    assert os.path.join(role_path, 'tasks') == Tasks.tasks_path(role_path)


def test_task_path():
    role_path = os.path.join('path', 'to', 'my', 'role')
    task = 'install.yml'
    assert os.path.join(role_path, 'tasks', task) == Tasks.task_path(role_path, task)


def test_main_path():
    role_path = os.path.join('path', 'to', 'my', 'role')
    assert os.path.join(role_path, 'tasks', 'main.yml') == Tasks.main_path(role_path)


@pytest.mark.parametrize('content, expected_includes', [
    ([], []),
    ([{'debug': 'msg'}], []),
    ([{'include': 't1'}], ['t1']),
    ([{'include_tasks': 't1'}], ['t1']),
    ([{'import_tasks': 't1'}], ['t1']),
    ([{'import_role': 't1'}], []),
    ([{'import_playbook': 't1'}], []),
    ([{'include_tasks': None}], []),
    ([{'include_tasks': {'foo': 'bar'}}], []),
])
def test_task_includes(content, expected_includes):
    assert sorted(expected_includes) == sorted(Tasks.task_includes(content))


def test_build_task_with_list(tmpdir):
    content = ['some', 'items']

    task_file = tmpdir.join("mytask.yml")
    task_file.write(yaml.dump(content))

    assert content == Tasks.build_task(str(task_file))


def test_build_task_file_not_found(tmpdir):
    task_file = tmpdir.join("mytask.yml")
    with pytest.raises(RuntimeError):
        Tasks.build_task(str(task_file))


def test_build_task_content_not_a_list(tmpdir):
    task_file = tmpdir.join("mytask.yml")
    task_file.write(yaml.dump({'some': 'item'}))

    with pytest.raises(ValueError):
        Tasks.build_task(str(task_file))


def test_build_task_content_invalid_yaml(tmpdir):
    task_file = tmpdir.join("mytask.yml")
    task_file.write('foo: bar: baz')

    with pytest.raises(RuntimeError):
        Tasks.build_task(str(task_file))
