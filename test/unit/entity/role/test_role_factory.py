import os

import pytest

from ansiblediscover.entity.role import Role, RoleFactory


@pytest.mark.parametrize('name, main_task', [
    ('myrole', None),
    ('myrole', 'main.yml'),
    ('myrole', 'install.yml'),
])
def test_init(name, main_task):
    if main_task is None:
        rf = RoleFactory(name)
        assert 'main.yml' == rf.main_task
    else:
        rf = RoleFactory(name, main_task)
        assert main_task == rf.main_task

    assert name == rf.name


@pytest.mark.parametrize('name, expected_valid', [
    ('myrole', True),
    (None, False),
])
def test_is_valid(name, expected_valid):
    rf = RoleFactory(name)
    assert expected_valid == rf.is_valid()


def test_path():
    name = 'myrole'
    rf = RoleFactory(name)
    assert os.path.join('roles', name) == rf.path


@pytest.mark.parametrize('name, expected_name', [
    ('myrole', 'myrole'),
])
def test_name(name, expected_name):
    rf = RoleFactory(name)
    assert expected_name == rf.name


def test_typestring():
    assert 'role' == RoleFactory('irrelevant').typestring


def test_build(mocker):
    name = 'myrole'
    path = os.path.join('roles', name)

    mock_role_build = mocker.patch('ansiblediscover.entity.role.Role.build')
    mock_role_build.return_value = Role(None, None, path)

    built_role = RoleFactory(name).build()

    assert Role == type(built_role)
    assert os.path.join('roles', name) == built_role.role_path
    mock_role_build.assert_called_with(path)
