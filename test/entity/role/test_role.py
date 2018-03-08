import pytest

from ansiblediscover.entity.role import Role


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
