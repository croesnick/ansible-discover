import os

import pytest
from ruamel import yaml

from ansiblediscover.entity.role import Meta, Role, Tasks


@pytest.mark.parametrize('name, expected_name', [
    ('main.yml', 'main'),
    ('main', 'main'),
])
def test_file_to_role_name(name, expected_name):
    assert expected_name == Role.normalize_role_name(name)


def test_dependencies_with_none_tasks_and_meta():
    role = Role(None, None, 'roles/sample')
    assert [] == role.dependencies()


def test_dependencies(mocker):
    task_dependencies = ['roleT1', 'roleT2']
    meta_dependencies = ['roleM1', 'roleM2']

    mock_tasks = mocker.patch('ansiblediscover.entity.role.Tasks').return_value
    mock_tasks.dependencies.return_value = task_dependencies

    mock_meta = mocker.patch('ansiblediscover.entity.role.Meta').return_value
    mock_meta.dependencies.return_value = meta_dependencies

    role = Role(mock_tasks, mock_meta, 'roles/sample')

    assert sorted(task_dependencies + meta_dependencies) == sorted(role.dependencies())


def test_build_meta_success(tmpdir):
    file = 'main.yml'
    content = ['foo', 'bar']

    role_path = tmpdir.join('myrole')
    file_path = role_path.join('meta', file)
    file_path.ensure(file=True)
    file_path.write(yaml.dump(content))

    meta = Role.build_meta(str(role_path))

    assert content == meta.content
    assert str(role_path) == meta.role_path


def test_build_meta_invalid_yaml(tmpdir):
    file = 'main.yml'

    role_path = tmpdir.join('myrole')
    file_path = role_path.join('meta', file)
    file_path.ensure(file=True)
    file_path.write('foo: bar: baz')

    assert Role.build_meta(str(role_path)) is None


def test_build_meta_invalid_file_not_found(tmpdir):
    role_path = tmpdir.join('myrole')
    assert Role.build_meta(str(role_path)) is None


def test_build_task_success(mocker):
    content = []
    role_path = os.path.join('path', 'to', 'myrole')

    mock_build_tasks = mocker.patch('ansiblediscover.entity.role.Tasks.build')
    mock_build_tasks.return_value = Tasks(content, role_path)

    tasks = Role.build_tasks(role_path)

    assert content == tasks.content
    assert role_path == tasks.role_path
    mock_build_tasks.assert_called_with(role_path)


def test_build_tasks_failure(mocker):
    role_path = os.path.join('path', 'to', 'myrole')

    mock_build_tasks = mocker.patch('ansiblediscover.entity.role.Tasks.build')
    mock_build_tasks.side_effect = RuntimeError()

    assert Role.build_tasks(role_path) is None
    mock_build_tasks.assert_called_with(role_path)


def test_build_success(tmpdir):
    role_path = tmpdir.join('path', 'to', 'myrole')
    meta_main_path = role_path.join('meta', 'main.yml')
    tasks_main_path = role_path.join('tasks', 'main.yml')

    meta_main_path.ensure(file=True)
    meta_main_path.write(yaml.dump({}))
    tasks_main_path.ensure(file=True)
    tasks_main_path.write(yaml.dump([]))

    role = Role.build(role_path)

    assert {} == role.meta.content
    assert role_path == role.meta.role_path
    assert [[]] == role.tasks.content
    assert role_path == role.tasks.role_path


def test_build_failure(tmpdir):
    role_path = tmpdir.join('path', 'to', 'myrole')
    assert Role.build(role_path) is None
