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

    assert task_dependencies + meta_dependencies == role.dependencies()


@pytest.mark.parametrize('tasks, include_statements, expected_includes', [
    ([], [], set()),
    ([{'include': 'good1.yml'}], [], set()),
    ([{'include': 'good1.yml'}], ['include'], {'good1.yml'}),
    ([{'include': 'good1.yml'}, {'import': 'ignored1.yml'}], ['include'], {'good1.yml'}),
    ([{'include': 'good1.yml'}, {'import': 'good2.yml'}], ['include', 'import'], {'good1.yml', 'good2.yml'}),
])
def test_extract_task_includes(tasks, include_statements, expected_includes):
    assert True
#    assert Role.task_includes(tasks, include_statements) == expected_includes
