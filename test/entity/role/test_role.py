import pytest
from ansiblediscover.entity.role import Role


@pytest.mark.parametrize('tasks, include_statements, expected_includes', [
    ([], [], set()),
    ([{'include': 'good1.yml'}], [], set()),
    ([{'include': 'good1.yml'}], ['include'], {'good1.yml'}),
    ([{'include': 'good1.yml'}, {'import': 'ignored1.yml'}], ['include'], {'good1.yml'}),
    ([{'include': 'good1.yml'}, {'import': 'good2.yml'}], ['include', 'import'], {'good1.yml', 'good2.yml'}),
])
def test_extract_task_includes(tasks, include_statements, expected_includes):
    assert Role.task_includes(tasks, include_statements) == expected_includes
