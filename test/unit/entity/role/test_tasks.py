import os

import pytest
from ruamel import yaml

from ansiblediscover.entity.role import RoleFactory, Tasks


@pytest.mark.parametrize('contents, expected_content', [
    ({'main.yml': []}, [[]]),
    ({'main.yml': [{'import_tasks': 'task.yml'}],
      'task.yml': [{'include_tasks': 'sub_task.yml'}],
      'sub_task.yml': [{'debug': {'msg': 'foo'}}, {'include': 'missing.yml'}]},
     [[{'import_tasks': 'task.yml'}],
      [{'include_tasks': 'sub_task.yml'}],
      [{'debug': {'msg': 'foo'}}, {'include': 'missing.yml'}]]),
])
def test_build_success(tmpdir, contents, expected_content):
    role_path = tmpdir.join('roles', 'my_role')
    tasks_path = role_path.join('tasks')
    tasks_path.ensure(dir=True)

    for (file, content) in contents.items():
        task_path = tasks_path.join(file)
        task_path.write(yaml.dump(content))

    assert expected_content == Tasks.build(role_path).content


@pytest.mark.parametrize('content, expected', [
    (None, []),
    ([], []),
    ([{'foo': 'bar'}], [{'foo': 'bar'}]),
])
def test_build_task_success(tmpdir, content, expected):
    tasks_path = tmpdir.join('roles', 'my_role', 'tasks')
    task_file = tasks_path.join('main.yml')

    tasks_path.ensure(dir=True)
    task_file.write(yaml.dump(content))

    assert expected == Tasks.build_task(str(task_file))


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


@pytest.mark.parametrize('content, expected', [
    ([], []),
    ([{'foo': 'bar'}], []),
    ([{'debug': {'msg': 'irrelevant'}}], []),
    ([{'include': {'name': 'config.yml'}}], []),
    ([{'include': 'config.yml'}], ['config.yml']),
    ([{'include': 'config.yml'}, {'include': 'config.yml'}], ['config.yml']),
    ([{'include': 'install.yml'}, {'include': 'config.yml'}], ['config.yml', 'install.yml']),
    ([{'include_tasks': {'name': 'config.yml'}}], []),
    ([{'include_tasks': 'config.yml'}], ['config.yml']),
    ([{'include_tasks': 'config.yml'}, {'include_tasks': 'config.yml'}], ['config.yml']),
    ([{'include_tasks': 'install.yml'}, {'include_tasks': 'config.yml'}], ['config.yml', 'install.yml']),
    ([{'import_tasks': {'name': 'config.yml'}}], []),
    ([{'import_tasks': 'config.yml'}], ['config.yml']),
    ([{'import_tasks': 'config.yml'}, {'import_tasks': 'config.yml'}], ['config.yml']),
    ([{'import_tasks': 'install.yml'}, {'import_tasks': 'config.yml'}], ['config.yml', 'install.yml']),
    ([{'include': 'install.yml'}, {'include_tasks': 'config.yml'}, {'import_tasks': 'ssh.yml'}],
     ['config.yml', 'install.yml', 'ssh.yml']),
])
def test_task_includes(content, expected):
    assert set(expected) == set(Tasks.task_includes(content))


def test_role_path():
    role_path = os.path.join('my', 'custom', 'roles', 'path', 'foobar')
    assert role_path == Tasks(None, role_path).role_path


def test_tasks_path():
    role_path = os.path.join('my', 'custom', 'roles', 'path', 'foobar')
    assert os.path.join(role_path, 'tasks') == Tasks.tasks_path(role_path)


def test_task_path():
    role_path = os.path.join('my', 'custom', 'roles', 'path', 'foobar')
    assert os.path.join(role_path, 'tasks', 'install.yml') == Tasks.task_path(role_path, 'install.yml')


def test_main_path():
    role_path = os.path.join('my', 'custom', 'roles', 'path', 'foobar')
    assert os.path.join(role_path, 'tasks', 'main.yml') == Tasks.main_path(role_path)


def test_dependencies():
    content = [
        {'include_role': {'name': 'foo'}},
        {'import_role': {'name': 'bar', 'tasks_from': 'install.yml'}}
    ]
    task_dependencies = {RoleFactory('foo'), RoleFactory('bar', 'install.yml')}

    tasks = Tasks(content, 'irrelevant')

    assert task_dependencies == set(tasks.dependencies())
